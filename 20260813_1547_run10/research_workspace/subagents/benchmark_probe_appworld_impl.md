# AppWorld silent-no-op 写入注入实现勘探（非权威草案）

## 0. 边界与结论摘要

- 本次只读检查了当前 Run `D:\Desktop\crl\20260813_1547_run10` 内的 AppWorld 固定源码、已下载 `dev` 数据、开发任务的官方解法与评价程序；没有读取或使用 `test_normal` / `test_challenge` 的 ground truth，也没有运行实验或修改 AppWorld 代码。
- 固定源码根：`D:\Desktop\crl\20260813_1547_run10\external\appworld`。
- Git 提交：`a072b7a86e7c1d5b1d7175659d750ebb9b79f10a`；`git describe` 为 `v0.1.3-196-ga072b7a-dirty`。现有 dirty 项全部位于 `tests/`，不是本次造成；正式实验前仍需冻结或清理出可复核的源码/数据快照，不能把 dirty 状态默认为无害。
- 可编辑安装包版本：`appworld==0.2.0.dev0`；数据版本：`0.2.0`。
- `dev.txt` 含 57 个任务，SHA-256 为 `9FA976589300EA8905708257144D801D1604B06D85FB0181E381DF8A3BA85001`。
- 最合适的最小夹具是 4 个结构互补的开发任务：`37a8675_1`、`530b157_1`、`6171bbc_1`、`6c2c621_1`。它们分别覆盖单次原子写入、跨应用部分成功、父对象已创建后的子对象漏写、批量导出中的单项漏写。
- 推荐的注入实现不是手写一个“看起来成功”的假对象，而是：在工具调度器边界显式保存状态，真实执行目标 API；仅当真实执行成功时，保存原始成功响应、回滚数据库状态，再把原始响应原样返回给智能体。这样既保证语法/模式与真实成功完全一致，也避免把智能体本来就会失败的错误参数混入故障效应。

## 1. 固定入口与状态模型

### 1.1 智能体看到的工具入口

当前提交的函数调用文档把工具命名为 `{app}__{api}`，例如 `venmo__create_transaction`。调度器可按第一个 `__` 拆分，并调用：

```python
response = world.requester.request(
    _app_name=app_name,
    _api_name=api_name,
    **arguments,
)
```

等价的 AppWorld 内部接口是 `world.apis.<app>.<api>(**arguments)`；`ApiCollection` 中每个包装函数最终也进入同一个 `Requester.request`。因此最窄且统一的注入点是候选模型之外的工具调度器，而不是改具体应用 API。

不建议 v001 用 `world.execute(code)` 的代码智能体模式做这项注入。`load_state` 会重新建立 `apis` / `requester`，在单个 Python 单元格执行到一半时回滚可能留下旧闭包；函数调用模式中每次工具调用都是独立边界，回滚后下一次调度重新解引用 `world.requester` 即可。

### 1.2 每条轨迹的克隆与隔离

```python
from appworld import AppWorld, update_root

ROOT = r"D:\Desktop\crl\20260813_1547_run10\external\appworld"
update_root(ROOT)

world = AppWorld(
    task_id=task_id,
    experiment_name=experiment_name,  # 每个条件/模型/重复均唯一
    random_seed=100,
    load_ground_truth=True,            # 仅运行器/评价器可见，不得传给模型
)
```

经源码核查，初始化会把该任务的起始数据库加载到任务专属内存数据库，并删除再创建 `experiments/outputs/{experiment_name}/tasks/{task_id}`。因此：

1. 每个 `{condition, model, repeat, task_id}` 必须使用唯一 `experiment_name`；同名会覆盖输出。
2. 每个工作进程只持有一个活动 `AppWorld`。`load_state` 内部调用类级 `AppWorld.close_all()`，同进程多 world 会互相干扰；并行应采用独立操作系统进程。
3. 当前提交中 `save_state()` 不传参数时把当前状态写到终局输出目录并返回 `None`；与 README 的无参示例不一致。注入检查点必须显式调用 `world.save_state("pre_fault_0001")`，随后 `world.load_state("pre_fault_0001")`。
4. 若工具调度绕过 `world.execute` 直接调用 `world.requester`，终止前必须显式 `world.save()`，再关闭 world；否则官方评价器可能读取不到最终数据库。

### 1.3 一次性“真实成功响应 + 状态回滚”注入伪代码

```python
fault_used = False
visible_tool_calls = 0

def dispatch(tool_name: str, arguments: dict):
    global fault_used, visible_tool_calls
    visible_tool_calls += 1  # 预算按模型发出的调用计数；检查点操作不计入任何一方
    app_name, api_name = tool_name.split("__", 1)

    if (not fault_used) and matches_target(task_id, app_name, api_name, arguments):
        state_id = "pre_fault_0001"
        world.save_state(state_id)
        try:
            # 每次都重新取当前 requester；load_state 后旧绑定不能复用。
            response = world.requester.request(
                _app_name=app_name,
                _api_name=api_name,
                **arguments,
            )
        except Exception:
            world.load_state(state_id)
            raise  # 本来失败的调用保持失败，且不消耗一次性故障

        if is_target_success(task_id, response):
            world.load_state(state_id)  # 真实副作用被撤销，成功响应保留
            fault_used = True
            injector_log.append({
                "task_id": task_id,
                "tool": tool_name,
                "arguments_digest": sha256(canonical_json(arguments)),
                "returned_response": response,
                "state_id": state_id,
            })
            return response

        world.load_state(state_id)
        return response  # 非异常失败对象原样返回，故障仍未使用

    return world.requester.request(
        _app_name=app_name,
        _api_name=api_name,
        **arguments,
    )
```

目标成功谓词不需要 ground truth：

- `venmo.create_transaction`：响应含 `transaction_id`。
- `phone.send_text_message`：响应含 `text_message_id`。
- `spotify.add_song_to_playlist`：`message == "Song added to the playlist."`。
- `file_system.create_file`：响应含 `file_path` 且 `message == "File created."`。

注入器日志必须存于方法/智能体不可见的实验产物目录。AppWorld 自身在回滚时会重建 requester，因此不能只依赖其请求追踪器保存被回滚的调用证据。

## 2. 四个固定开发任务

| task_id | 任务结构 | 一次性目标 API | 原样返回的官方成功响应形状 | 智能体可用的状态回读 | 官方终局判定为什么能抓住 no-op | 最小性/信息量 |
|---|---|---|---|---|---|---|
| `37a8675_1` | 向指定手机号对应的人私密发送 91 美元；单次原子写入 | 第一次真实成功的 `venmo.create_transaction` | `{"message":"Sent money.","transaction_id":n}` | `venmo.show_transaction` 或 `venmo.show_transactions`，核对收款人、金额、私密性 | 评价程序要求新增恰好 1 条 `venmo.Transaction`，无更新/删除，并核对 receiver、amount、private；完全 no-op 必失败 | 官方解法 11 次 API、难度 2；最适合测试“成功响应后是否验证终局” |
| `530b157_1` | 先按短信内容偿还杂货款，再发送确认短信；跨应用部分成功 | 付款真实成功后，第一次真实成功的 `phone.send_text_message` | `{"message":"Text message sent.","text_message_id":n}` | `phone.search_text_messages` 按联系人/消息内容回读；付款可用 `venmo.show_transactions` 独立回读 | 评价程序同时要求 1 条正确 Venmo 交易和 1 条正确 `phone.GlobalTextMessage`，并检查没有删除 `phone.UserTextMessage`；只完成付款仍失败 | 官方解法 18 次 API、难度 3；区分局部动作成功与整项任务成功 |
| `6171bbc_1` | 创建播放列表，再为每个专辑加入最常播放歌曲；父子依赖写入 | 播放列表已真实创建后，第一次真实成功的 `spotify.add_song_to_playlist` | `{"message":"Song added to the playlist."}` | `spotify.show_playlist` 或 `spotify.show_playlist_library`，核对新列表中的 `song_ids` | 评价程序要求只新增 1 个正确标题的 Playlist，且新增 PlaylistSong 的歌曲集合与期望集合完全相等、全部指向新列表；漏掉一个子项即失败 | 官方解法 63 次 API、难度 2；成功对象无 ID，最干净地隔离“响应可信度” |
| `6c2c621_1` | 把所有 Simple Note 笔记导出为指定目录下的 Markdown 文件；批量独立写入 | 第一次真实成功的 `file_system.create_file` | `{"message":"File created.","file_path":"<规范化路径>"}` | `file_system.show_file` 核对路径/内容，或 `file_system.show_directory` 聚合核对 | 评价程序要求新增文件的路径集合、内容集合和路径到内容映射均与期望完全相等，同时没有文件更新/删除；漏一个文件即失败 | 官方解法 71 次 API、难度 2；响应带回写路径但不依赖新实体 ID，最适合首个适配器冒烟检查 |

### 2.1 `37a8675_1`：单次原子付款

- 目标路由：函数工具 `venmo__create_transaction`；内部 `apis.venmo.create_transaction(...)`；HTTP 为 `POST /venmo/transactions`。
- 该 API 一次正常成功会联动交易、通知、付款方资金来源与收款方余额。先真实调用再回滚，能够同时撤销多表副作用，同时返回真实生成的 `transaction_id`；比人工构造 phantom ID 更贴近真实成功。
- 这是最短的终局验证夹具，但也最能暴露回滚完整性问题。正式测量前必须比较 checkpoint 前后全部允许应用数据库的模型哈希，而不是只查 `Transaction`。
- 评价文件：`data/tasks/37a8675_1/ground_truth/evaluation.py`。它不依赖智能体轨迹或注入器输出，只比较任务起始/终局模型。

### 2.2 `530b157_1`：跨应用部分成功

- 目标路由：函数工具 `phone__send_text_message`；内部 `apis.phone.send_text_message(...)`；HTTP 为 `POST /phone/messages/text/{phone_number}`。
- 注入点放在付款已经成功、确认短信即将发送时。终局中 Venmo 交易真实存在，但短信不存在；模型收到的却是官方真实成功响应。
- 该任务能检查方法是否只局部相信最后一次成功，或是否在完成前验证跨应用联合后置条件。若智能体选择重跑整段计划而不是仅补发短信，可能产生重复付款，官方“恰好一条交易”约束会惩罚这种过度恢复。
- 评价文件：`data/tasks/530b157_1/ground_truth/evaluation.py`。

### 2.3 `6171bbc_1`：父对象存在、一个子写入缺失

- 目标路由：函数工具 `spotify__add_song_to_playlist`；内部 `apis.spotify.add_song_to_playlist(...)`；HTTP 为 `POST /spotify/playlists/{playlist_id}/songs/{song_id}`。
- 不应对 `spotify.create_playlist` 做 no-op：后续调用需要真实 `playlist_id`，会把故障变成明显的级联 404。目标应是第一次成功的 `add_song_to_playlist`，其成功响应只有消息字符串，语法上完全正常，后续加入其他歌曲也仍能成功。
- 终局缺少恰好一个期望 `PlaylistSong`；若智能体在完成前读取新播放列表并做集合对账，可定点补写。
- 评价文件：`data/tasks/6171bbc_1/ground_truth/evaluation.py`。

### 2.4 `6c2c621_1`：批量文件导出中单项漏写

- 目标路由：函数工具 `file_system__create_file`；内部 `apis.file_system.create_file(...)`；HTTP 为 `POST /file_system/file`。
- API 正常响应会返回经过 AppWorld `process_path` 规范化后的 `file_path`。真实执行后回滚能保证返回值与当前账户、主目录和路径规范完全一致，避免人工拼接路径成为混杂。
- 回滚必须同时恢复隐式创建的父目录及目录时间戳；因此这是检查 checkpoint 是否覆盖 `file_system.File` 和 `file_system.Directory` 的首选夹具。
- 评价文件：`data/tasks/6c2c621_1/ground_truth/evaluation.py`。

## 3. 独立官方判终

运行器结束时只负责保存终局：

```python
world.save()
world.close()
```

随后由独立进程运行官方评价程序。单任务命令中 `--task-id` 与数据集位置参数互斥，因此不要同时传 `dev`：

```powershell
& 'D:\Desktop\crl\20260813_1547_run10\env\appworld\Scripts\appworld.exe' evaluate `
  'v001_appworld/fault/candidate/37a8675_1/r000' `
  --task-id '37a8675_1' `
  --root 'D:\Desktop\crl\20260813_1547_run10\external\appworld'
```

其实现 `evaluate_task` 会：

1. 从任务数据加载起始数据库；
2. 从 `experiments/outputs/{experiment_name}/tasks/{task_id}/dbs` 加载终局数据库；
3. 构造 `ModelCollectionPair(start, end)`；
4. 调用该开发任务自带的 `ground_truth/evaluation.py`；
5. 把逐断言报告写到 `experiments/outputs/{experiment_name}/tasks/{task_id}/evaluation/report.md`。

因此评价依据与候选方法、注入器和自然语言自报完成均不同源。智能体调用 `supervisor.complete_task(status="success")` 只是必要条件，不能替代终局数据库断言。

## 4. 最小可重放路径

### 4.1 适配器 Scratch（不算正式科研实验）

先只用 `6c2c621_1` 和一个确定性脚本控制器，不接 LLM：

1. clean 轨迹真实创建一个目标文件，保存终局；
2. fault 轨迹对同一 `create_file` 做一次真实成功后回滚，断言返回 JSON 与 clean 完全一致；
3. 立即调用 `show_file`，断言 fault 世界中文件不存在；
4. 再次真实调用同一 `create_file`，断言恢复成功；
5. 比较 checkpoint 前与 no-op 返回后的全模型哈希必须相同；
6. 运行官方单任务评价，no-retry 应失败、retry 应通过。

若这一步不能同时满足“响应一致、状态未变、重试可恢复、官方判分翻转”，不得进入 LLM Recorded。

第二个适配器 Scratch 用 `37a8675_1`，专门验证多表写入（交易、通知、余额/卡）的回滚完整性。它不是方法效果实验。

### 4.2 最小 Recorded 设计建议

- 任务：先用四个固定 task_id，不扩展整个 dev。
- 条件：`clean` 与 `one_shot_silent_noop`。
- 系统：候选与强基线；两者获得同一函数工具集合、系统提示、模型版本、温度、上下文、最大模型轮次、最大可见工具调用数、超时与完成条件。
- 注入：相同 task/API 成功谓词、同为第一次真实成功实例；内部 checkpoint/rollback 不计入任何模型的调用预算。
- 必记：注入是否触发、触发前可见调用号、响应摘要、回滚前后模型哈希、智能体是否回读、是否重试、是否重复写入、官方逐断言结果。
- 未触发故障的轨迹不能悄悄并入“故障条件成功率”；应单独报告注入覆盖率，并检查不同方法是否因路径差异受到不同故障暴露。

## 5. 泄漏、混杂与实现风险

1. **ground truth 泄漏**：候选/基线只接收任务 instruction 和同一组公开函数模式。不得向模型暴露 `world`、`Task.ground_truth`、`private_data`、SQLite/JSONL、评价报告、checkpoint/save/load 或宿主文件系统。开发 ground truth 只由离线评价器和本次夹具审计读取。
2. **测试集污染**：本草案没有读取或使用任何测试集 ground truth。后续在 Formal 前也不应通过本实现调试测试任务；四个 task_id 全部来自固定 `dev.txt`。
3. **成功资格混杂**：只在真实目标调用已经成功时才回滚并消耗故障；不能盲目把本应失败的错误参数改成成功，否则测到的是参数纠错而不是 silent no-op。
4. **轨迹/状态同源判分**：官方评价只看起始/终局数据库和任务完成字段；注入器不得调用官方评价来决定何时或如何故障。
5. **预算不公平**：预算必须按模型发出的可见工具调用计数。检查点、真实调用、回滚和注入器审计是环境内部开销，对候选和基线都不计费；智能体为了验证/重试所发出的工具调用则正常计费。
6. **回滚后旧引用**：`load_state` 会重建 `world.apis` 与 `world.requester`；调度器不能缓存 bound method、客户端或模型对象。每次工具调用都从当前 world 重新解引用。
7. **同进程多 world**：`load_state` 的类级关闭会影响同进程其他 world；每条轨迹独立进程，不能以线程并行。
8. **日志丢失**：回滚可能重置 AppWorld 请求跟踪状态。独立注入器 JSONL 是必须产物，同时在终局保存 AppWorld 原生日志和 DB diff。
9. **任务暴露不一致**：`required_apis.json` 是官方解法的最小需求，不应据此只给候选一小撮工具。候选与基线都应获得该任务允许应用的同一完整公开 API 集，否则会人为剥夺 `show_transaction`、`show_playlist`、`show_file` 等验证手段。
10. **仓库 dirty**：当前 `git status` 显示既存 `tests/` 修改。正式执行前至少记录 `git diff --name-only`、源码提交、`dev.txt` 哈希、四个任务评价文件哈希，并证明 `src/` 与 `data/` 未被改动；更稳妥的是使用当前提交的干净只读副本，不覆盖用户现有修改。

## 6. 会阻止进入正式实验的实现失败

- 显式 checkpoint 后真实成功调用、`load_state` 后的数据库模型哈希不能回到调用前；尤其是 Venmo 多表副作用或文件系统父目录时间戳残留。
- 回滚后旧 requester/API 引用导致下一次真实重试不可用，或 access token 失效。
- 注入器无法区分真实成功与失败，导致对候选/基线暴露不同类型的故障。
- 同样的模型可见调用预算下，基础设施调用被错误计入某一方法，或候选额外获得 checkpoint/rollback 能力。
- 官方 evaluator 不能在独立进程只凭保存的终局 DB 重现 per-task 结果。
- 4 个任务中故障未触发率明显依赖方法轨迹，而研究分析又没有把暴露差异单列；此时不能把任务级成功率差解释为恢复方法效应。
- 无法隔离开发 ground truth、评价报告或宿主文件系统，使模型有机会读取答案或注入标签。

这些是测量/实现障碍，不是科学版本或 Run 的裁决。本草案不生成 Seed、Decision 或 No-Delivery 结论。
