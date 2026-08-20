# P002 主 Codex首读

- PDF：`knowledge_base/staging/papers/P002_tree_of_thoughts.pdf`
- PDF SHA-256：`6939cadebd84c8cdcc6ff3c2082b75851a86e2ef82008848d0af692f80521fa7`
- 读取时间：`2026-07-19T15:55:00+08:00`
- 读取范围：逐页检查 1–14 页；正文 1–9 页，参考文献 10–11 页，附录任务难度、跨模型与成本分析 12–14 页。第 5、7–8 页的图中文字存在字体映射异常，但正文、表格和 caption 可读；以下裁决不依赖乱码图中文字。

## Changed computation

- [AUTHOR_FACT] 第 3–4 页把问题求解状态定义为输入加已生成 thoughts 的序列，并把单一路径自回归生成改成四个可组合部件：thought decomposition、候选生成、状态评估、搜索算法。
- [AUTHOR_FACT] 候选可以独立采样或顺序提出；状态可以独立 value 评价或在同层候选间 vote；论文分别用 BFS 和 DFS，并允许剪枝与回溯。
- [READER_INTERPRETATION] 核心不是“让模型想得更久”，而是显式保留多个中间状态，用模型启发式评估控制扩展、剪枝和回溯，从而改变下一步会被计算的路径集合。

## Baseline、预算与公平性

- 第 5–6 页 Game of 24 使用 100 个较难样本（索引 901–1000）；IO/CoT 各采样 100 次，CoT-SC 用 100 samples，IO+Refine 最多 10 次且获得方程正确性的 ground-truth feedback。ToT 用 BFS，宽度 `b=5`，每个 thought 的 value 采样 3 次。
- 表 2 的 IO/CoT `best of 100` 是作者明确称作 oracle 的事后成功统计，不能视作可部署 baseline；IO+Refine 也使用 oracle 正确性信号，不能与无 oracle 的普通单样本等价比较。
- Creative Writing（第 6–7 页）只有 100 个作者构造输入；自动 coherency 由 GPT-4 每个输出打 5 次分，人评由作者子集盲比。ToT 每层生成 5 个候选并采样 5 votes，预算显著高于单次 IO/CoT。
- Mini Crosswords（第 7–8 页）只测试间隔抽取的 20 局；IO/CoT 每题 10 samples，ToT DFS 上限 100 search steps。`+best state` 是 oracle 输出，不是实际选择规则。
- 附录 B.3 第 14 页估算 Game of 24：IO best-of-100 约 `$0.13`/题、CoT best-of-100 `$0.47`、ToT `$0.74`；Creative Writing ToT 约 `$0.32`，IO `$0.06`、CoT `$0.07`。作者概括 ToT 会生成约 5–100 倍 token，主结果不是等 token/call 比较。

## 主要结果与定位

- 表 2，第 6 页：Game of 24 成功率 IO 7.3%、CoT 4.0%、CoT-SC 9.0%、ToT `b=1` 45%、`b=5` 74%；IO+Refine 27%，IO/CoT oracle best-of-100 分别 33%/49%。约 60% CoT samples 在第一步就进入不可解状态。
- 第 6–7 页：Creative Writing 的 GPT-4 coherency 分数 IO 6.19、CoT 6.93、ToT 7.56；100 对盲比中人类偏好 ToT 41、偏好 CoT 21、相近 38。Refine 把 IO 提到 7.67、ToT 提到 7.91，说明 refine 也可作为候选生成方式。
- 表 3，第 7–8 页：Crosswords 的 letter/word/game 指标，IO 为 38.7/14/0，CoT 40.6/15.6/1，ToT 78/60/20（即 4/20 局）；oracle best state 为 82.4/67.5/35。
- 消融：去 pruning 降到 65.4/41.5/5，去 backtracking 降到 54.6/20/5。论文同时指出错误 evaluator 会剪掉实际可解状态，未剪枝版本反而找到 3 个剪枝版在 100 步内找不到的解，因此收益取决于启发式误差和预算。
- 附录 B.1 第 13 页在 100 题子集上，GSM8K IO/CoT/ToT 为 51/86/90，StrategyQA 为 73/82/83，支持作者“简单任务增益有限”的边界；B.2 中 GPT-3.5 Game of 24 ToT 仅 19%，远低于 GPT-4 的 74%。

## 失败边界与限制

- [AUTHOR_FACT] 第 8 页：LM evaluator 可能把罕见但正确的 crossword 词判为 impossible 并错误剪枝；更好的 pruning heuristic 是关键。
- [AUTHOR_FACT] 第 9 页：ToT 对 GPT-4 已擅长的任务可能没有必要；论文只覆盖三个相对简单、特意挑选的困难任务，并付出更高 API/token 成本。
- [AUTHOR_FACT] 附录 B.2 第 13–14 页跨模型组合显示生成器更可能是瓶颈：GPT-4 generator + GPT-3.5 evaluator 达 64%，反向组合只有 31%。因此不能假设弱模型仅靠搜索即可获得同等收益。
- [READER_INTERPRETATION] value/vote 由同一 LM 提供，候选与评估错误可能相关；搜索放大了生成计算，并未自动解决评价器偏差。开放式任务又存在 GPT-4 judge 与 GPT-4 generator 同源偏差。
- [READER_INTERPRETATION] 任务级 thought decomposition、prompt、BFS/DFS 和终止策略均由研究者手工设计；论文验证的是模块化搜索范式，不是无需任务适配的通用 Agent planner。

## 可抽取候选（尚非正式 Card）

- Operator：`LM-Heuristic Branch-and-Revisit Search`——显式生成多个中间状态，由 LM value/vote 选择扩展，并用剪枝、回溯或束宽保留可逆决策。
- Failure：`Correlated Generator–Evaluator Error`——同一模型生成与评估会共享盲点，错误剪枝可永久移除正确分支。
- Failure：`Search-Compute and Oracle Comparison Confound`——5–100 倍 token、best-of-k、ground-truth refine 与 oracle best state 使表面提升不能直接归为结构本身。

## 未解决问题

- `[OPEN_QUESTION]` 论文未给等总 token、等延迟且无 oracle 的统一对照；成本表只提供估算。
- `[OPEN_QUESTION]` Creative Writing 人评由作者子集完成，未报告外部标注者一致性或 evaluator 校准。
- `[OPEN_QUESTION]` 三个任务上的任务专用 decomposition/search 选择能否迁移到长程工具 Agent，原文没有直接实验。
