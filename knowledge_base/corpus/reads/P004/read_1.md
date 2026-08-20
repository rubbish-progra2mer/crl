# P004 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P004_travelplanner.pdf`
- PDF SHA-256：`a7c7edd67c90e9997e940aaa7b435d46a8b201ed119c125b341b01b215454133`
- 读取时间：`2026-07-19T16:26:00+08:00`
- 读取范围：逐页检查 1–24 页；正文 1–9 页，参考文献 9–11 页，数据/工具/实验细节与 prompts 12–18 页，数据、标注计划及失败案例 19–24 页。

## Changed computation / evaluation object

- [AUTHOR_FACT] 本文主要贡献是 benchmark，而非新 Agent 方法：把旅行任务拆成信息收集与规划两阶段，在静态封闭 sandbox 中以 6 类检索工具和 Notebook 测试长程工具使用，再机械检查 environment、commonsense、hard constraints。
- [AUTHOR_FACT] 第 5–6 页另设 sole-planning：直接提供人工计划确定的城市和所需信息，从而移除工具收集，隔离规划能力；two-stage 则统一使用 ReAct 收集信息。
- [READER_INTERPRETATION] 可迁移资产主要是“分离信息缺失与全局约束规划”的评测干预，以及 constraint-level 负向证据；不应把 TravelPlanner 强行抽象成一个生成 Operator。

## 数据、评测与基线

- 第 4–5、12 页：45 train、180 validation、1000 test；3/5/7 天分别对应 1/2/3 个目的城市，easy 仅预算，medium 增加一个 hard constraint 和 2–8 人，hard 有三个 hard constraints（含交通偏好）。20 名研究生标注 1225 个可行 query-plan，作者复核并用人工计划成本重新校准预算。
- static database 含 3,827,361 航班、17,603 距离、9,552 餐馆、5,303 景点、5,064 住宿；部分价格、城市映射、cuisine/room rule 是随机或规则合成（第 12–13 页），因此“real-world”指数据来源和任务结构，不等于动态真实市场。
- 第 5 页：自然语言计划先由 GPT-4-Turbo 抽取为结构化字段，再由脚本评估。最终指标包括 30-step 内 Delivery、8 个 commonsense 约束、hard constraints、所有条件同时通过的 Final Pass。GPT 抽取误差是评测链中的潜在测量变量。
- 两阶段对比 Mistral/Mixtral/Gemini/GPT-3.5/GPT-4，在相同 ReAct tool-use 框架下零样本运行；sole-planning 比较 Direct、ZS-CoT、ReAct、Reflexion。由于非 Direct 策略为控制成本主要只在 GPT-3.5 上测试，模型与策略不是完整析因设计。
- Greedy Search 用最低成本交通/餐馆/住宿和随机景点；它始终交付，但不针对全部硬约束优化，不是最强通用规划器。论文因成本未运行 ToT/GoT，故 0.6% 不能外推所有搜索式 planning 方法。

## 主要结果与定位

- 表 3，第 6 页：two-stage test 上 GPT-4-Turbo Delivery 93.1%，commonsense micro/macro 63.3/2.0，hard micro/macro 10.5/5.5，Final 0.6%；其余模型 Final 均 0。论文标题式的“0.6%”是严格 all-constraints pass，不等于完全无法生成旅行计划。
- sole-planning test 上 Direct GPT-4-Turbo Final 4.4%，commonsense 80.6/15.2，hard 44.3/23.1；Direct Gemini Final 2.1%。GPT-3.5 下 ReAct 0.7、Direct 0.6、Reflexion 0.6、CoT 0.4，说明这些 prompting 策略并未稳定优于 Direct。
- validation 上 GPT-4-Turbo Reflexion（附录表 B.3）Final 3.3%，而 Direct GPT-4-Turbo 为 4.4%；两者 delivery 分别 80.6/100。Reflection 在此设置下没有带来表面最终增益。
- 表 4，第 7 页：GPT-4 两阶段 hard budget pass 随 easy/medium/hard 从 10.1/8.4 降至 4.4；sole-planning 为 37.4/35.1/25.1。Minimum Nights Stay 即使 sole-planning 也只有 37.4/28.8/30.1，显示全局约束不是单纯检索缺失。
- 表 5：GPT-4 agent 写入 Notebook 的各工具次数在 3/5/7 天均明显少于 reference；随行程变长差距扩大，支撑 incomplete information collection 这一窄解释。

## 失败边界与限制

- [AUTHOR_FACT] 第 7 页 Figure 2：GPT-4 未交付错误中，max-step 56.7%、invalid-action dead loop 37.3%、same-action loop 6.0%；它没有 argument error。该分布只以“失败终止”样本为条件，不能当全测试集发生率。
- [AUTHOR_FACT] 第 7–8 页：agent 收到无效/空 observation 后仍重复动作；日期初始假设错误持续到提前停止，说明未利用反馈修正。
- [AUTHOR_FACT] sole-planning 中仍会混淆航班/住宿条目，把去程航班复用于返程；作者联系到大量上下文下的信息混淆。该案例是定性例，不构成 Lost-in-the-Middle 的单独因果实验。
- [AUTHOR_FACT] Reflexion case 中 thought 明说降低成本，随后的 action 却随机选择可能更贵的项目；作者称为 reasoning-action disconnect。表 3 也显示 Reflexion delivery 低于 Direct。
- [AUTHOR_FACT] 第 9 页 Impact Statement 承认 commonsense 定义来自作者共识；数据包含随机价格、随机城市映射和随机属性，限制了对真实旅行偏好的外推。
- [READER_INTERPRETATION] 极低 macro/final pass 一部分来自约束的乘法效应：单项 micro 尚可，但任一错误即整例失败。该严格性对“可部署可行计划”合理，却不能用 0.6% 直接衡量一般语言理解或局部规划质量。
- [READER_INTERPRETATION] benchmark 允许完整 evaluation feedback 且 reference 证明至少一解存在；但论文没有给等信息、等 context、等调用预算的 search/backtracking 强 baseline，所以它揭示失败，不定位唯一机制解法。

## 可抽取候选（尚非正式 Card）

- Evaluation Operator：`Two-Stage Information/Planning Isolation`——同一任务分别运行工具收集+规划和人工信息供给+规划，以区分信息覆盖失败与约束合成失败。
- Evaluation Operator：`Micro-to-Macro Constraint Audit`——同时报告单约束通过率与全约束共同通过率，暴露平均局部正确掩盖整体不可行。
- Failure：`Persistent Invalid-Action Loop after Null Feedback`——收到空/无效结果仍重复同类 action，直到 step/loop 终止。
- Failure：`Reasoning–Action Constraint Disconnect`——语言诊断识别预算/约束问题，但实际选择没有落实该约束。
- Failure：`Incomplete Collection and Information Binding Confusion`——长程工具查询不足或把一条记录错误绑定到另一天/方向，导致 sandbox hallucination 和缺项。

## 未解决问题

- `[OPEN_QUESTION]` GPT-4-Turbo 结构抽取器的准确率、人工核验比例及其对最终 pass 的误差没有报告。
- `[OPEN_QUESTION]` 各模型实际 token、tool calls、上下文截断和 API snapshot 未给出，two-stage 模型差异不能严格归因于模型能力。
- `[OPEN_QUESTION]` ToT/GoT、约束求解器或强搜索 baseline 因成本未测，benchmark 尚不能区分语言模型规划上限与所选 prompting 上限。
