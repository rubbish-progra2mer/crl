# P046 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P046/read_2_attempts/r2-20260719-p046-a1/invocation.md`
- 论文：*Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents*
- PDF SHA-256：`0b29985358a4735f7e2ad032225cf5299080be4ef33cf8539f2550c8bbf06807`
- [AUTHOR_FACT] 已读取全部 5 个物理页。

## 1. changed computation 与 I/O

- [AUTHOR_FACT] 系统在计划工具调用与实际执行之间插入 SMT guard：把自然语言政策编码成 SMT-LIB；运行时由 LLM 从对话/工具参数抽取可观察状态，添加断言并用 Z3 检查。SAT 放行，UNSAT 拦截，并把最小 unsat core 注入重规划提示，最多重试 3 次。（物理页 2–3，System design；短定位：“minimum unsat core”“three”）
- [AUTHOR_FACT] 输入包括人工审核的形式化政策、工具 schema、对话中抽取的状态与待执行调用；输出是 allow/block 以及重规划约束。干预发生在写操作执行前。（物理页 2–3，图 1/流程）
- [READER_INTERPRETATION] 形式保证只覆盖“给定编码与状态抽取均正确”时的谓词可满足性，不是从自然语言政策到真实世界动作的端到端安全证明。

## 2. 基线、结果与预算

- [AUTHOR_FACT] 实验只在 tau2 airline 的 50 个任务、13 个工具、1,242 词政策上进行；每题 k=4，customer/service agent 为 GPT-4.1，验证抽取使用 GPT-4o。（物理页 3–4，Evaluation setup）
- [AUTHOR_FACT] 写调用 precision 从基线约 .51 提高到 .70，但 recall 从 .61 降至 .49；无效写比例降到约 29%，同时有效调用也减少。（物理页 4，图 3）
- [AUTHOR_FACT] pass^1..4：基线约 .560/.433/.375/.340，solver 约 .625/.543/.495/.460；文本还报告 policy checker 略改善、跨重复运行的不一致下降约 26% 对 40%。（物理页 4，图 4 与结果段）
- [READER_INTERPRETATION] 最接近基线是相同 GPT-4.1 agent、无 SMT guard；但 guard 额外使用 GPT-4o 抽取、Z3 与最多 3 次重规划，计算/调用预算并不相同。结果应解释为“额外验证预算下的 precision/pass 改善”。

## 3. 自动化失败、泄漏与未测边界

- [AUTHOR_FACT] 自然语言政策自动转 SMT 的多种方案均失败：直接 Proof-of-Thought 有语法错误；修复后仍遗漏/欠约束；AWS 自动推理生成约 600 行、LLM judge 称约 95% coverage 的版本仍欠约束；最终使用人工调优版本。（物理页 3–4，RQ1；短定位：“underconstrained”“manual tuning”）
- [AUTHOR_FACT] 人工调优包含“运行 benchmark 并修复欠约束 implication”。（物理页 4，RQ1 讨论）
- [READER_INTERPRETATION] 这构成 benchmark-guided policy artifact 开发；没有独立 holdout 或冻结后的政策编码评估，存在测试适配/泄漏风险。主要数值不能代表从未见政策自动部署。
- [OPEN_QUESTION] 原文未单独评估运行时状态抽取的准确率，也未测试单域外、其他模型、政策漂移、恶意提示或形式化规则自身冲突。

## 4. Operator、Failure 与建议

- [READER_INTERPRETATION] Operator 候选：在人审形式政策与可信状态抽取前提下，对高风险工具调用做 pre-execution SMT satisfiability check，并用最小冲突核定向重规划。
- [READER_INTERPRETATION] Failure 候选：LLM 自动形式化产生语法正确但语义欠约束的规范；提高 precision 的 guard 会牺牲 recall；形式验证可因错误事实抽取或漏编码给出虚假安全感。
- [READER_INTERPRETATION] 建议保留 changed-computation，但结论限于“单域、人工且 benchmark-guided 的政策 artifact”；自动政策翻译失败本身是更强的负向证据。

## 5. 可视核验

- [AUTHOR_FACT] 物理页 4 的图 3/4 数值与正文方向一致。页面渲染与文本抽取未显示结论性冲突。

