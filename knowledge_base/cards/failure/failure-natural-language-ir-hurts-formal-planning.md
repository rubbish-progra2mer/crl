<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-natural-language-ir-hurts-formal-planning","card_kind":"failure","paper_id":"P060","evidence_ids":["ev-p060-formal-ir-solver","ev-p060-ir-result-and-nl-failure"],"source_refs":[{"path":"papers/P060_unifying_planning_language.pdf","sha256":"5e3695206fd0e01347e348d606ebd206387f4fba3192ed24ea5133abdef36305"}]} -->
# Adding a Natural-Language Intermediate Plan Can Hurt

## Observed failure
[AUTHOR_FACT] P060 报告 natural-language IR 在其设置中持续降低表现，而 syntax-aligned second IR 有益。[[evidence:ev-p060-ir-result-and-nl-failure]]

## Conditions and scope
[CODEX_SYNTHESIS] 绑定论文任务与 IR pipeline，不等于所有 natural-language planning 都有害。

## Failed intervention
[CODEX_SYNTHESIS] 增加一段自由文本中间推理，却没有提供 solver 可执行的约束结构。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 伤害可能来自更长上下文、错误承诺或 representation mismatch；消融只证明该 NL-IR 方案未奏效。
[CODEX_SYNTHESIS] 论文没有同时配平 model、token 与 solver/tool-call budget；“早期错误分解传播到后续 Agent action”仍是需要受控实验验证的解释，而不是当前 Evidence 已隔离的因果结论。

## Warning for future candidates
[CODEX_SYNTHESIS] “多一步规划”不是机制；必须说明新增表示如何改变 downstream computation。

## Possible repair boundary
[AUTHOR_FACT] syntax-aligned formal IR 由 solver 执行。[[evidence:ev-p060-formal-ir-solver]]

## Evidence ledger
[CODEX_SYNTHESIS] 负向结果和 formal alternative 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] natural-language plan hurts; explicit long-form planning decomposition ablation; longer reasoning can hurt task success; early mistaken decomposition may propagate to later Agent actions; formal IR; representation mismatch; matched model/token/tool-call budget control missing
