<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-syntax-aligned-formal-ir-planning","card_kind":"operator","paper_id":"P060","evidence_ids":["ev-p060-formal-ir-solver","ev-p060-ir-result-and-nl-failure"],"source_refs":[{"path":"papers/P060_unifying_planning_language.pdf","sha256":"5e3695206fd0e01347e348d606ebd206387f4fba3192ed24ea5133abdef36305"}]} -->
# Syntax-Aligned Formal-IR Planning

## Intervention target
[CODEX_SYNTHESIS] LLM 推理与最终答案之间的中间表示和可执行求解步骤。

## Before and after computation
[CODEX_SYNTHESIS] free-form natural-language plan → formal IR emitted by LLM and executed by symbolic solver。[[evidence:ev-p060-formal-ir-solver]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为问题与 IR grammar；输出为可解析 IR/solver result；答案生成前增加 solver 调用，不增加答案 Oracle。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 与任务操作语义对齐的 syntax 能把组合搜索从 token generation 移交给确定性求解器。

## Predicted observable signature
[CODEX_HYPOTHESIS] syntax-aligned IR 有益而同长度 NL-IR 无益；错误应集中在 formalization fidelity，而非 solver 执行。

## Preconditions and transfer risks
[AUTHOR_FACT] natural-language IR 在报告设置中持续伤害结果。[[evidence:ev-p060-ir-result-and-nl-failure]]

## Source lineage
[CODEX_SYNTHESIS] natural-language planning baseline → inference-time formal IR refinement；仍受 solver-guarantee boundary 约束。

## Evidence ledger
[CODEX_SYNTHESIS] changed computation 与 representation-sensitive result 有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] formal IR planning; syntax-aligned reasoning; symbolic solver execution; natural-language IR failure
