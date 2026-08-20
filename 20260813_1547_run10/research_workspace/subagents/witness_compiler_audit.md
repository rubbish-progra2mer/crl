# `witness_compiler` 非权威独立实现审计

## 0. 范围与总判断

- 本审计仅读取当前 Run 的 `witness_compiler.py`、`run_unselected_clean_coverage.py`、`unselected_clean_coverage.json`，以及固定 AppWorld 提交 `a072b7a86e7c1d5b1d7175659d750ebb9b79f10a` 中必要的公共 API 文档与实现源码。
- 没有读取或使用任何测试集 ground truth，没有编辑主文件，也没有运行 AppWorld 任务或科研实验。为确认确定性静态选择原因，只用公共 API 文档和合成参数形状重新调用了纯函数 `compile_witness`；没有创建 world 或改变数据库。
- 当前 10 个洁净开发夹具均通过官方终局评价；其中 7 个编译成功，5 个 witness 返回 `true`，2 个返回 `false`，另 3 个不可编译。两个 `false` 是确认的洁净误报，但 5 个 `true` 不能视为“检测覆盖”：至少前四个只是重新读到写入前已经存在的目标实体，silent-no-op 后同样会返回 `true`。
- 根因不是缺少几个动词或字段别名，而是当前编译器把“能从某个读接口找到与写参数同名的值”误当成“该读结果证明写副作用发生”。最小通用修订应把词法打分降为候选生成器，并增加同权限、穷尽、隔离的写前—写后可见差分校准；没有可见差分时返回 `UNKNOWN`，不能强行生成布尔 witness。

## 1. 两个洁净误报

### 1.1 `spotify.create_playlist`：非穷尽集合读压过稳定对象句柄

记录结果：`6171bbc_1` 的写入真实成功，返回 `playlist_id=654`；编译器选择 `search_playlists`，随后 witness 为 `false`，官方终局评价为成功。

确定性因果链：

1. 写 API 路径为 `/spotify/playlists`，`search_playlists` 路径也为 `/spotify/playlists`。当前总分给路径交并比乘以 3，因此集合搜索获得最大路径奖励。
2. 实际写调用没有显式传默认的 `is_public`，所以生成的唯一关系是“请求 `title` 等于某条搜索结果的 `title`”；`query` 没有被绑定到 `title`。
3. 读调用只带写请求中的 `access_token`。公共实现显示 `search_playlists` 默认 `page_index=0`、`page_limit=5`，且无查询时按 `-like_count` 排序；它只返回第一页。
4. 新建的私有播放列表对该用户可见，但没有进入默认第一页，因此 `any(...)` 找不到标题并返回 `false`。
5. 同一公共 API 集中存在更强的 `show_playlist(playlist_id=...)`：其必需参数可由写成功响应的 `playlist_id` 精确绑定，且返回单个对象。但当前评分对“来自写响应的绑定”反而每项扣 0.25，最终让弱的集合搜索胜出。

这不是 `title -> query` 别名缺失。加入该别名只能缓解当前任务，还会引入模糊搜索、同名对象和排序行为。通用修复是优先稳定写响应句柄，并把未穷尽集合的“不匹配”判为 `UNKNOWN`。

### 1.2 `venmo.remind_payment_request`：方向错误只是表象，副作用对调用者不可见才是本质

记录结果：`4fab96f_1` 的提醒真实成功；编译器选择 `show_received_payment_requests`，关系为 `payment_request_id == payment_request_id`，witness 为 `false`，官方终局评价为成功。

确定性因果链：

1. `show_received_payment_requests` 与 `show_sent_payment_requests` 的参数、响应模式和静态路径重叠分完全相同。
2. 当前 `max` 在同分时由公共文档迭代顺序决定；`received` 先出现，所以被意外选中。这不是科学上的方向推断。
3. 公共实现要求只有付款请求的发送方能调用 `remind_payment_request`；`show_received_payment_requests` 则固定筛选 `receiver_id == 当前用户`。因此目标请求不在该集合，洁净误报是必然的。
4. 不能把读接口改成 `show_sent_payment_requests` 就算修复。提醒写入只为接收方创建一条 `Notification`，不修改原 `PaymentRequest`。发送方在提醒前后都能在“已发送请求”中看到相同 `payment_request_id`。
5. `show_notifications` 只返回当前令牌用户自己的通知；写入产生的通知属于接收方。若保持与候选/基线相同权限，调用者没有可见公共读接口能确认提醒通知已经生成。

所以该实例在当前权限契约下应编译为 `UNKNOWN / UNOBSERVABLE`。让 witness 使用另一用户凭据会扩大方法权限，破坏公平性；让 `show_sent_payment_requests` 返回 `true` 则会把 silent-no-op 错判为成功。

## 2. 三个不可编译根因

### 2.1 `file_system.move_file`：后置目标在响应中，关系生成器却只读请求

- 写请求含 `source_file_path`、`destination_file_path` 和控制参数；成功响应含规范化后的 `destination_file_path`。
- `show_file` 的必需参数叫 `file_path`。当前贪心绑定对源路径和目标路径得到相同词法分，随后因“请求来源加 0.15”及参数插入顺序，稳定选择先出现的 `source_file_path`。
- 对关系生成，`_relations` 完全不接收写响应。`source_file_path` / `destination_file_path` 与读响应叶子 `path` 的名称匹配分只有约 0.533，低于 0.7 阈值；因此任何候选都没有 relation，最终返回 `None`。
- 这同时丢掉两个必要后置条件：目标路径存在、源路径不存在。只证明目标存在会把“复制但未删除”也算作移动成功。

通用可计算方式是枚举 `file_path` 的所有相容来源，并用隔离的写前—写后读差分选择：对公共 `file_exists`，源路径应从 `true -> false`，目标路径应从 `false -> true`。成功响应中的规范化目标路径应作为一等来源，而不是通过 `destination -> file` 别名硬编码。

### 2.2 `spotify.previous_song` / `spotify.next_song`：唯一锚点在写响应，且目标实体本来就在队列中

- 两个写请求除 `access_token` 外没有语义参数；成功响应含新的当前 `song_id`。
- `_relations` 只遍历 `write_arguments`，控制字段被排除后为空，所以必然不可编译。
- 仅把响应 `song_id` 映射到 `show_song(song_id)` 仍不充分：歌曲实体在移动播放游标前就存在。
- 仅在 `show_song_queue` 中找到该 `song_id` 也不充分：该歌曲在移动前已经位于同一个循环队列。
- 公共 `show_song_queue` 返回每行的 `song_id`、`position`、`is_current`、`is_playing`。真正可辨别的后置条件是：由写响应 `song_id` 锚定的同一队列行，在写后具有 `is_current=true`；同时旧当前行发生相反变化。这一限定只能由同权限的写前—写后差分一般性学得，不能由“previous/next”任务规则硬编码。

## 3. 绑定审计

当前 `_best_binding` 的主要风险：

1. **逐参数独立贪心**：没有做全局一一匹配。多个读参数可绑定到同一来源；源路径/目标路径这种同分歧义由字典顺序决定。
2. **请求偏置方向错误**：请求来源固定加 0.15，写响应来源在计划总分中还被扣分。对 create/move 类写入，响应 ID 或规范化路径通常才是最强后置句柄。
3. **必需参数低阈值放行**：只要必需参数存在任何正分候选，即使低于 0.7 也会被接受；“必需”不等于“词义正确”。
4. **类型检查过宽**：未知类型恒相容，`None` 与所有类型相容；没有检查枚举、格式、路径规范、身份主体或访问令牌归属。
5. **关系没有来源标签**：`Relation` 只能引用请求字段；写响应只能用于读参数绑定，不能成为期望值或对象身份关系。
6. **硬编码控制字段不完备**：`CONTROL_FIELDS` 只覆盖少数字段；增加更多任务/API 名称只会把错误推迟。控制性应来自调用模式和数据流角色，而不是持续扩充字段表。
7. **动词角色只是软猜测**：`ROLE_BY_WRITE_VERB` 不含 move/remind/previous/next，且从 API 名和描述的首个匹配词决定角色。它不应承担可见性或因果证明。

最小修订：让一个读参数保留所有类型相容的请求/响应绑定候选，进行全局组合；词法分只剪枝。响应中的精确标识符和规范化句柄优先于请求字段；存在同分且写前—写后差分无法消歧时返回 `UNKNOWN`。

## 4. 集合匹配审计

- 根集合上当前实现使用 `any(_item_satisfies(...))`，所有 relation 至少在同一个根元素上合取，这一层是合理的。
- 但 `_extract_path` 会把嵌套数组完全拍平；多个 relation 分别做 `any`，可能由不同嵌套元素分别满足。例如一个艺术家的 ID 与另一艺术家的名字可以共同让根对象通过。
- `used_paths` 禁止两个来源占用同一响应路径，但冲突时静默丢掉后一个关系；它没有证明哪个来源才是正确身份。
- 只有 `equals` / `contains`，没有不存在、状态迁移、计数变化、顺序、当前项或集合差分。对 move 和播放游标操作，这些恰是核心效应。
- 没有基数约束。预先存在的同名播放列表、同一首已在队列中的歌曲、已经存在的资源实体，都可以让 identity-only witness 通过。
- 5 个洁净 `true` 中，`follow_artist -> show_artist`、`download_song -> show_song`、`like_transaction -> show_transaction`、`like_song -> show_song` 的计划都只验证目标 ID。写 API 必须先作用于已存在的目标，所以这些 ID 在写前已经可读；它们结构上不能区分 silent-no-op。`add_to_queue -> show_song_queue` 只验证成员存在，也未排除歌曲本来已在队列中。

最小修订：路径提取保留数组索引/父对象谱系，以同一谱系连接多个关系；更重要的是，计划必须至少包含一个经写前—写后验证发生变化的 effect relation。纯资源身份关系只能做定位锚点，不能单独构成成功证明。

## 5. 穷尽性与可见性审计

### 穷尽性

- 当前编译器从公共文档知道 `page_index` / `page_limit`，但执行器只调用默认第一页。
- 对集合响应，“第一页没有匹配项”不能推出全集合没有匹配项。`create_playlist` 已实际暴露这一错误。
- 查询/排序/过滤未绑定时，默认值可能让对象落在任意页；集合为非空也不能说明已穷尽。

通用修订：只要读 API 暴露分页参数，就以文档允许的最大 `page_limit` 从 `page_index=0` 迭代，直至返回空页或短页；记录页响应摘要以防服务忽略页码而循环。遇到页错误、重复页、达到安全上限仍未终止时，结果必须为 `UNKNOWN`。只有证明穷尽后，“无匹配”才可为 `FALSE`。

### 可见性与读纯度

- 同一令牌下，不同端点可能只展示公开资源、自己的私有资源、自己发送的对象或自己接收的对象。路径和响应模式相同不能证明主体范围相同。
- 写副作用可能落在另一主体名下；提醒通知就是明确例子。不得为 witness 借用额外凭据。
- HTTP `GET` 也不能先验视为无副作用。固定源码中的 `show_song_queue` 在没有 MusicPlayer 时会创建并保存一个。当前 coverage 直接在官方解法中途调用读 API，理论上可能污染终局；本次 10 条官方评价均通过只说明这些具体轨迹未被判为污染。

通用修订：所有候选读在与真实轨迹隔离的 checkpoint/克隆上执行，并比较读前后模型哈希；发生状态变化的读计划淘汰或判 `UNKNOWN`。可见性只用候选/基线本来持有的令牌实测，不能用数据库或其他用户权限补洞。

## 6. 三值判定审计

当前 `evaluate_witness` 只返回 `bool`；coverage 又把所有读异常直接压成 `False`。这混合了至少五类状态：

1. 完整、授权的观察明确满足后置条件；
2. 完整、授权的观察明确违反后置条件；
3. 集合只读到部分页；
4. 权限不覆盖真实副作用；
5. 请求错误、超时、模式漂移、绑定歧义或编译失败。

建议固定三值：

```text
TRUE     = 所有必需 effect relation 在完整、同权限观察中成立
FALSE    = 至少一个必需 effect relation 在完整、同权限观察中被明确反证
UNKNOWN  = 不可编译、不可见、未穷尽、绑定歧义、读错误或读自身有副作用
```

对于多个互补读计划，成功应要求覆盖所有已校准的必需效应；失败只由明确反证产生；任何尚未覆盖的必需效应或观察不完备都保持 `UNKNOWN`。`UNKNOWN` 不能在统计代码中自动转成失败或成功，应单列可观测覆盖率。

## 7. 最小通用计算修订

不增加任何任务特定别名、API 白名单或 `remind/move/next` 规则，建议只改三层计算。

### A. 从“选最高分一条”改为“枚举候选绑定/读计划”

- `Binding.source` 保留 `request | response`；`Relation` 同样增加来源标签。
- 请求和成功响应都参与关系生成；`message` 这类无结构字段只作低优先级候选。
- 为一个读参数保留多个相容来源，做全局组合；优先精确响应句柄、必需参数可执行、单对象读、同权限读。
- 集合路径相同和词法重叠仅用于限制搜索空间，不再直接决定最终计划。

### B. 用一次真实成功调用做写前—写后差分校准

在调度器已有的注入前 checkpoint 上，对每个候选计划做：

```python
pre  = observe(candidate, checkpoint="before_write", exhaustive=True, isolated=True)
post = observe(candidate, checkpoint="after_real_success", exhaustive=True, isolated=True)
delta = anchored_visible_delta(pre, post, write_request, write_response)
```

- 观察必须使用与智能体相同的公开 API、令牌和调用权限。
- 集合须穷尽；每次观察在克隆上运行并检查读纯度。
- 只有 `post` 相对 `pre` 出现由请求/响应句柄锚定的可见变化，才能生成 effect relation。
- 纯身份不变（目标对象写前已存在）不能成为 effect relation。
- 若不同候选共同覆盖一个操作的多个变化，可保留最小合取计划；无法观察到变化则 `UNKNOWN`。

这一步与 ground truth 和任务文本无关，是对已实例化真实 API 调用的因果可观察性校准。

### C. 运行时返回三值并保存证据

- 单对象读的权威“未找到”只有在权限与响应类别可确认时才是 `FALSE`；认证、网络、模式错误是 `UNKNOWN`。
- 集合无匹配只有在分页穷尽后才是 `FALSE`。
- 匹配保持父子谱系，不允许跨嵌套元素拼接。
- 日志保存计划来源、绑定歧义、分页完成证明、pre/post 差分摘要、运行时原始响应和判定理由。

## 8. 修订后五类重点行为的预期

| 写 API | 通用差分编译结果 | 原因 |
|---|---|---|
| `create_playlist` | 可编译 | 用响应 `playlist_id` 绑定单对象 `show_playlist`；写前权威不存在，写后 ID、标题等成立 |
| `move_file` | 可编译为合取 | 枚举源/目标绑定；`file_exists` 显示源 `true->false`、目标 `false->true`，响应目标路径提供规范化锚点 |
| `previous_song` / `next_song` | 可编译 | 响应 `song_id` 锚定队列行；差分学习该行 `is_current: false->true`，而非仅检查歌曲存在 |
| `remind_payment_request` | `UNKNOWN / UNOBSERVABLE` | 调用者可见请求不变，真实通知属于另一用户；同权限公共读无可见差分 |
| follow/download/like 等现有洁净 `true` | 需重新校准 | identity-only 计划必须淘汰；只有库成员、点赞状态或计数等真实可见差分才能成为 witness |

## 9. 对当前 coverage 产物的解释边界

- `terminal_success=true` 的 10/10 是有价值的基础设施一致性检查：这些额外读没有让官方解法在当前夹具上失败。
- “7/10 可编译、5/7 洁净通过”只能说明静态编译和单页读的表面可执行性，不能支持 fault detection、恢复或 witness 声明。
- 两个洁净 `false` 是已观测的误报；五个洁净 `true` 尚未经过 no-op 反例，且静态结构已经显示多条会在 fault 下继续为真。
- 在差分校准、三值判定和同权限可见性落实前，不宜把未编译、读错误、未找到或不可观察统一算入二元准确率。

本草案只提供非权威实现审计与修订建议，不产生 Seed、Decision 或科学裁决。
