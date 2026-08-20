# P007 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P007_tau_bench.pdf`
- PDF SHA-256：`e2d45d573e1fce753ead1a44cc468ad386dd384e2668450d0a9c0e2c7920ada0`
- 读取时间：`2026-07-19T17:06:00+08:00`
- 读取范围：逐页检查 1–53 页；正文 1–10 页，参考文献与附加难度分析 10–12 页，完整 API/policy/data-generation 13–22 页，retail 数据及三类失败轨迹 23–44 页，airline 数据与成功轨迹 45–53 页。

## Changed computation / evaluation object

- [AUTHOR_FACT] τ-bench 不是新 Agent 方法，而是把隐藏 user intent、LM 模拟用户、domain policy、数据库 read/write tools 和终态标注组合成多轮 POMDP 式评测；agent 看 policy/tools，不看用户 simulator 的完整 instruction 或 ground-truth actions。
- [AUTHOR_FACT] reward 将 episode 后的数据库与唯一目标数据库比较，并检查 agent 对用户输出是否包含必要字符串；对话路径和只读调用可变化。`pass^k` 衡量同一任务的 `k` 次独立运行是否全部成功，与至少一次成功的 `pass@k` 方向相反。
- [READER_INTERPRETATION] 可迁移 changed computation 位于评测端：从单次平均 success 转为“语义相同、对话采样不同”的重复可靠性，并用终态而非轨迹模板允许多种正确交互；它不自动评价过程安全或政策合规。

## 数据、模型、基线与预算

- τ-retail 有 115 tasks、15 APIs（7 write/8 read），τ-airline 50 tasks、13 APIs（6 write/7 read）；数据/API/policy 先人工设计，GPT-4 生成采样代码并人工修 bug，任务由人工编写并反复运行 GPT-4-Turbo FC 直到认为 outcome 唯一。
- Figure 7（第 12 页）显示每个 retail task 至少跑 40 次 GPT-4-Turbo 以检查低/零成功任务；这一流程提升标注质量，也使任务措辞对该 agent 的行为具有 curation bias，作者在第 10 页明示。
- 主 agent 为各厂 API；FC 原生 function calling 对比 zero-shot 文本 ReAct 与 Act。最多 30 个 agent actions，agent temperature 0、用户 GPT-4-0613 temperature 1；主表每任务至少 3 trials。Llama-3 因无 FC 只以 text ReAct 测，不能与其他模型纯比较。
- 作者未测试 7B/13B；也没有把 planning/self-reflection 作为 agent baseline，理由是实时用户场景太慢或“一次服务”不现实。因此 benchmark 主表不能代表所有 agent architecture 上限。
- 第 8 页给出 gpt-4o FC agent 与 GPT-4 user simulator 在 retail 每任务约 `$0.38/$0.23`，价格 95.9% 来自 agent input（长 policy+function definitions）；重复可靠性需要多次运行，成本会线性增长。

## 主要结果与定位

- Table 2：FC `pass^1` retail/airline 为 GPT-4o 61.2/35.2，GPT-4-Turbo 57.7/32.4，Claude-3-Opus 44.2/34.7；表中 `avg` 是两个 domain 等权，不按 115/50 tasks 加权。
- Figure 3：在所示 OpenAI 模型上 native FC 均优于 text ReAct，ReAct 又优于 Act；另加 `think` function 没有提升，作者推测 FC 模型未按这种 reasoning 接口训练。它说明 interface/training alignment 重要，不是“显式 reasoning 普遍无效”。
- Figure 4：GPT-4o retail 单次平均 >60%，但 `pass^8 <25%`；同图 `pass@k` 随 k 增，而 `pass^k` 降，揭示高采样可发现解与稳定服务是不同目标。
- policy ablation（Table 3）：去 policy 后 GPT-4o retail 61.2→56.8、airline 33.2→10.8；GPT-3.5 20.0→14.5、10.8→9.6。复杂 airline 中 GPT-4o 明显使用规则，而 GPT-3.5 即使有 policy 也几乎未受益。
- user simulator 策略 Table 4 是对“模拟用户”而非被测 agent 的改造：在 GPT-4o FC airline、3 trials 下 vanilla/ReAct/verify/reflection accuracy 0.367/0.300/0.393/0.406；抽样 50 个错误中 user-attributed error 均 ≤4%。不能把 0.406 当成 agent reflection 成效。

## 失败边界与限制

- [AUTHOR_FACT] 第 5 页明确承认 `r=1` 只是成功的必要而非充分条件：agent 可未经用户确认就执行 return，终态仍完全匹配但违反 policy。终态 oracle 未覆盖所有过程约束。
- [AUTHOR_FACT] 115 条 retail 单次轨迹中 40 失败，人工发现 4 个由 instruction typo/ambiguity 导致并修复；剩余 36 才做 wrong argument/info、wrong decision、partial resolution 分类。失败率和类别统计依赖这一特定 run/模型。
- [AUTHOR_FACT] wrong argument/info 合计约 55%：会选错 inventory variant、漏报 tracking、算错价格或给错误信息改变用户意图；GPT-4o 每 retail task 平均 0.46 个不存在 ID 的调用，GPT-3.5 FC/Act 为 2.08/6.34。
- [AUTHOR_FACT] wrong decision 约 25%：忽略“exchange tool 每单只能调用一次”，先交换一个 item 导致其余无法处理；partial resolution 约 19%，复合请求中只完成显式提到的一部分或只查一个 order。
- [AUTHOR_FACT] 第 10 页承认 simulator 可能受 typo、缺少领域知识、推理/计算/长上下文能力限制；C.2.2 中用户甚至确认了 agent 推荐但不符合偏好的 lamp。小规模错误归因不消除 simulator 与 agent 相互诱发错误。
- [AUTHOR_FACT] 只覆盖合成 retail/airline 两域；数据库、policy 与 unique outcome 被刻意简化。作者把 medical/tax/legal、更复杂 policy 和更多 metrics 留给未来。
- [READER_INTERPRETATION] ground-truth output 用字符串子串检查，可能漏掉语义等价表述或错误上下文中碰巧出现数值；终态完全相等又可能惩罚无害额外 write，测量边界需与 claim 一起保存。
- [READER_INTERPRETATION] `pass^k` 同时混合 agent stochasticity 与 LM user simulator stochasticity；作者抽样认为 user 直接错误少，但对话变化仍是该 metric 刻意包含的压力来源，不应称为纯 agent 随机性。

## 可抽取候选（尚非正式 Card）

- Evaluation Operator：`Goal-State Equivalence under Free Interaction Paths`——隐藏唯一目标终态，允许不同对话/只读轨迹，以最终数据库和必要输出判断任务完成。
- Evaluation Operator：`All-Trials Reliability (pass^k)`——按任务估计 k 次独立试验全部通过的概率，区别于 best-of-k discovery。
- Failure：`Terminal-State Success with Process-Policy Violation`——终态吻合仍可能未经确认执行写操作，说明 oracle 覆盖不充分。
- Failure：`Compound-Request Partial Resolution`——随着目标 write actions 增多，agent 忘记早期/隐式子请求并提前结束。
- Failure：`Policy-Available but Not Operationalized`——复杂规则在 context 中存在，但弱模型或某些运行没有把规则转成正确 write decision。

## 未解决问题

- `[OPEN_QUESTION]` Figure 4 各 `pass^k` 曲线所用每任务 trial 数及置信区间在正文未逐模型给出；只知 retail GPT-4-Turbo curation 至少 40 次。
- `[OPEN_QUESTION]` ground-truth output substring matcher 的 false-positive/false-negative 率未做人评校准。
- `[OPEN_QUESTION]` 未加入过程级 policy checker，不能量化“终态正确但违规”的真实比例。
- `[OPEN_QUESTION]` 任务由 GPT-4-Turbo FC 反复调 prompt 后冻结，对其他模型难度是否系统偏移没有独立 curation baseline。
