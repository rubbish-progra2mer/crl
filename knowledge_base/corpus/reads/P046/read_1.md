# P046 Codex 首读：Solver-Aided Verification of Agentic Workflows

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P046_solver_aided_verification.pdf`
- PDF SHA-256：`0b29985358a4735f7e2ad032225cf5299080be4ef33cf8539f2550c8bbf06807`
- 读取范围：全文（5 页），重点为 SMT 编码、运行时校验、tau2 airline 结果与形式化边界。

## Changed computation

- [AUTHOR_FACT] 在工具执行前，将 Agent 提议的动作与对话事实送入 GPT-4o 事实抽取器，再由 Z3 对手工编码的 airline policy 做 SAT/UNSAT 检查；UNSAT 时返回最小冲突核心并允许最多三次重规划。
- [AUTHOR_FACT] 形式化约束不是从政策文本可靠自动得到：直接 LLM 翻译存在语法错误和漏约束，迭代修复仍然 under-constrained；最终版本由定制提示、人工检查与 benchmark 运行调优得到。
- [CODEX_SYNTHESIS] 真正改变的是“高风险写操作在执行前多一道可执行政策门”，而不是让 LLM 再口头反思一次。

## 关键结果与边界

- tau2 airline 50 tasks、4 trials：write-tool precision 从 0.51 升至 0.70，recall 从 0.61 降至 0.49；pass^1 从 0.560 升至 0.625，pass^4 从 0.340 升至 0.460。
- 非法写调用占比降到约 29%，但正确写操作也减少；安全门同时造成有效动作拒绝。
- 最终 SMT 编码在 benchmark 运行后人工调优，存在 benchmark-specific overfitting/leakage 风险；结论只对“编码的规则 + 抽取出的事实”成立。
- 仅验证一个 domain、50 tasks；事实抽取器仍可能漏事实或误判，solver 本身不能修复输入语义错误。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P046-E01 | method | pp.1–3 | SMT gate / UNSAT core | [AUTHOR_FACT] 预执行形式化门与重规划接口。 |
| P046-E02 | result | pp.3–4 | tau2 airline table | [AUTHOR_FACT] precision/pass 提升及 recall 下降。 |
| P046-E03 | negative_result | pp.2–4 | automatic formalization attempts | [AUTHOR_FACT] 自动政策翻译 under-constrained。 |
| P046-E04 | limitation | pp.4–5 | manual tuning / extractor | [AUTHOR_FACT+CODEX_SYNTHESIS] 保证只相对编码与事实抽取成立。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Pre-Execution Formal Policy Gate`
- Baseline：Agent 读自然语言 policy 后直接调用有副作用的工具。
- Changed computation：对提议动作先执行符号可满足性检查，只让满足显式约束的写操作进入环境；冲突核心作为窄反馈返回。
- 边界：需要高质量形式化规则和可靠事实抽取，不能把 solver 的确定性误写成端到端正确性。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Under-Constrained Formalization Creates False Guarantees`
- 现象：约束求解结果看似严格，但规则翻译遗漏会让错误动作在一个不完整模型中合法。

## 首读裁决

`KEEP_FOR_SECOND_READ`。机制直接、结果有正负两面；二读必须独立检查人工调优是否使窄 Claim 失效。
