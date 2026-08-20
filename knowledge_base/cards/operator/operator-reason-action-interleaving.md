<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-reason-action-interleaving","card_kind":"operator","paper_id":"P001","evidence_ids":["ev-p001-react-interleaved"],"source_refs":[{"path":"papers/P001_react.pdf","sha256":"f285b0971ae4a790e402fb93966bed3adde2cf0a04977d08b2b40d6ab0cace69"}]} -->
# Reason–Action Interleaving

## Intervention target
[AUTHOR_FACT] 在语言模型的顺序决策中交错生成 reasoning trace 与 environment action。[[evidence:ev-p001-react-interleaved]]

## Before and after computation
[CODEX_SYNTHESIS] Baseline 是只生成推理或只生成动作；changed computation 是 Thought → Action → Observation 的循环。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为任务与历史轨迹，输出为思考或动作；Observation 在下一次决策前进入上下文，增加工具调用与外部信息。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 动作把外部状态反馈给推理，而推理维护并修正高层行动计划。

## Predicted observable signature
[CODEX_HYPOTHESIS] 若交错而非单纯更多 token 起作用，优势应集中在需要根据新 Observation 改计划的步骤。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 需要动作接口、可解释 Observation 与足够可靠的行动格式；工具错误会污染后续推理。

## Source lineage
[CODEX_SYNTHESIS] ReAct 是直接来源；后续树搜索、反思与工具规划可在此循环外增加控制，但不等同于本 Operator。

## Evidence ledger
[AUTHOR_FACT] `ev-p001-react-interleaved` 定位到 PDF p.2 的交错计算描述。[[evidence:ev-p001-react-interleaved]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] ReAct；reason-act-observe；interleaved reasoning and acting；行动—观察闭环；tool-grounded planning。

