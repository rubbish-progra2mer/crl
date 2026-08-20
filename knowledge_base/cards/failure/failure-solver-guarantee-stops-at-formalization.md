<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-solver-guarantee-stops-at-formalization","card_kind":"failure","paper_id":null,"evidence_ids":["ev-p051-solver-guarantee-boundary","ev-p051-omitted-constraint-failure","ev-p052-implicit-constraint-failure","ev-p052-self-diagnosis-nontermination","ev-p052-direct-code-smt-baselines"],"source_refs":[{"path":"papers/P051_formal_verification_planning.pdf","sha256":"ba9261d6d8fbf2b43817e57c29aa6ffacc0b14ef038e6c86a33f8780490bd365"},{"path":"papers/P052_llmfp.pdf","sha256":"e59c5c55b3befeeb4774a20990b8629f487e9fb1520cc2a953f041b7bb6fdaec"}]} -->
# Solver Guarantee Stops at the Formalization Boundary

## Observed failure
[AUTHOR_FACT] P051 的 LLM 生成代码遗漏 all-different 约束，所得计划重复选择同一 block；P052 的 Definer 遗漏隐式守恒约束后，模型可用无来源的物料获得更低成本。[[evidence:ev-p051-omitted-constraint-failure]] [[evidence:ev-p052-implicit-constraint-failure]]

## Conditions and scope
[CODEX_SYNTHESIS] 自然语言目标先由 LLM 翻译为约束或可执行 solver 代码，再由形式求解器验证和优化。

## Failed intervention
[CODEX_SYNTHESIS] 仅增加 sound solver 或让同一模型检查自己的形式化，不能证明自然语言意图与编码模型等价；P052 还记录了自诊断误判后引入不终止循环。[[evidence:ev-p052-self-diagnosis-nontermination]]

## Evidence and alternative explanations
[AUTHOR_FACT] P051 明确把 solver 保证表述为对已编码且可满足的约束系统求解。[[evidence:ev-p051-solver-guarantee-boundary]] [CODEX_SYNTHESIS] 失败可能来自遗漏约束、语义误译、生成代码错误或接口状态不完整，而不是 solver 算法本身失效。

## Warning for future candidates
[CODEX_SYNTHESIS] 不得用 SAT、optimal 或同模型 self-assess 通过率替代端到端语义正确性；Candidate 必须与 Direct 和 `Code SMT` 在相同模型、信息与申明预算下比较，并单独报告形式化错误。P052 的基线共享输入信息，但没有证明调用、token 或时延预算相等。[[evidence:ev-p052-direct-code-smt-baselines]]

## Possible repair boundary
[CODEX_HYPOTHESIS] 有价值的改进应改变规格覆盖或形式化核查的计算，例如独立的约束覆盖审计或可信接口边界；不得使用答案 Oracle，也不得把更多调用、tokens 或人工任务模板偷换为机制收益。

## Evidence ledger
[CODEX_SYNTHESIS] 两篇论文的作者事实共同支持“solver 的保证不等于自然语言到形式模型的语义忠实”；同模型诊断失败只作为附加风险。[[evidence:ev-p051-solver-guarantee-boundary]] [[evidence:ev-p051-omitted-constraint-failure]] [[evidence:ev-p052-implicit-constraint-failure]] [[evidence:ev-p052-self-diagnosis-nontermination]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] formalization fidelity; omitted constraint; specification gap; sound solver wrong model; implicit constraint; early plan or decomposition error propagation; downstream solver preserves a wrong formalization; equal-budget control missing; self-diagnosis failure
