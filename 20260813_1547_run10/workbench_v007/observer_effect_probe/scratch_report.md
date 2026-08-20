# v007 验证器观察干扰 Scratch 报告

## 搜索问题

Verified Tool Calls 明确要求 postcondition verifier 是 read-only，并据此认为重复验证安全。v007 检查：工具文档或 HTTP GET 是否会把真实有副作用的操作误当作只读，从而让验证本身改变任务状态。

Run-local purpose-aware retrieval 位于 `hypotheses_v007/searches/observer_effect_verification_v007_01/`。命中 92 篇去重论文、525 条原始观测，2 条观测带机械噪声标记；知识库没有直接给出工具智能体验证器观察干扰的方法。

## AppWorld 静态扫描

`scan_appworld_get_effects.py` 对固定 AppWorld 提交 `a072b7a86e7c1d5b1d7175659d750ebb9b79f10a` 的所有 `apis.py` 做 AST 扫描，找出 GET 函数体中的 `create/save/delete/create_file` 与属性/下标赋值。第一次运行把 Run 根层级算错，扫描了不存在目标源码的产品级路径并得到 0 候选；修正为当前 Run 的 `external/appworld` 后得到 32 个静态候选。

人工核验显示多数“赋值”只是构造局部返回字典，不是持久副作用。真正明显的持久写入主要是：Amazon、Gmail、Splitwise、Todoist、Venmo 的下载端点会创建文件并递增下载次数；Spotify 的 `show_current_song`、`show_song_queue`、`show_volume` 在 MusicPlayer 不存在时会创建并保存默认播放器。前一类文档已写明 download，不是隐蔽副作用；后一类才是有信息量候选。

## 动态 A/B

在开发任务 `37a8675_1` 上复用已通过的固定付款程序。控制组在完成付款和 supervisor 协议后直接评价；处理组在完全相同行动后额外调用一次 `spotify.show_volume`。两组共同把 Venmo 余额设为充足；官方评价明确忽略 Venmo.User 变化。

第一次动态运行因未设置余额而在付款 API 返回 422；这是实现诊断，不是科学结果。修正共同夹具后：

- 控制组 6/6，通过；
- `show_volume` 组 6/6，通过；
- 两组调用前后全库 `MusicPlayer` 数量都为 106，主用户已有播放器，因此该 GET 在此状态下没有持久差分。

原始结果在 `appworld_observer_ab_results.json`。它反证了“源码存在创建分支就足以证明该真实夹具发生观察干扰”。

## 最近计算碰撞

把方法收缩为“用黑盒重放认证实际 CRUD/效果类型”仍不新。CRUDinfer（ICSE 2026）已经只依赖 OpenAPI 与 HTTP 黑盒交互，先按 HTTP 动词假设 CRUD 语义，再用 read-after-create 等 CRUD 测试模式迭代确认或修正操作语义；论文报告总体精确率 95%，相对语言模型语义推断精确率提高 15.1%。Karlsson 等人的 REST 行为测试也用调用序列与观察谓词核验 GET 不改状态等行为。

将这类已知黑盒 CRUD/行为推断接到 Verified Tool Calls 的只读验证要求上，没有新的候选排序或状态转移计算；当前真实夹具又没有观察干扰终局差异。

## 局部裁决

`h-v007-001`: `prior_collision`。不进入 Formal 或 Reviewer。杀伤范围是“黑盒效果认证 + 只读验证门”这一当前组合，不否认真实系统可能存在有害观察调用。
