<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-single-turn-tool-score-overstates-agent-competence","card_kind":"failure","paper_id":"P066","evidence_ids":["ev-p066-single-to-stateful-gap","ev-p066-multiturn-state-evaluation"],"source_refs":[{"path":"papers/P066_bfcl.pdf","sha256":"5248f4770823b2a73fd52e3b12339d94121ff1b359c45163c5a47168edab7a2f"}]} -->
# Single-Turn Function Calling Does Not Establish Stateful Agent Competence

## Observed failure
[AUTHOR_FACT] 强 single-turn function calling 不能证明 memory、stateful decision 或 long-horizon competence。[[evidence:ev-p066-single-to-stateful-gap]]

## Conditions and scope
[CODEX_SYNTHESIS] 适用于把工具选择 accuracy 外推成完整 Agent 能力的论证。

## Failed intervention
[CODEX_SYNTHESIS] 单轮 evaluator 只检查一次 call mapping，没有测跨轮状态更新、缺参追问或缺函数处理。

## Evidence and alternative explanations
[AUTHOR_FACT] BFCL multi-turn 将这些失败类型分别测量。[[evidence:ev-p066-multiturn-state-evaluation]] [CODEX_SYNTHESIS] evaluator 本身对 surplus calls、嵌套值与聚合仍有边界。

## Warning for future candidates
[CODEX_SYNTHESIS] tool-use Candidate 的 claim 必须匹配被测 interaction horizon 与 evaluator semantics。

## Possible repair boundary
[CODEX_SYNTHESIS] 使用 stateful multi-turn suite 可收窄 claim，但不自动覆盖开放式任务。

## Evidence ledger
[CODEX_SYNTHESIS] 外推失败与多轮分解均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] single-turn tool metric; stateful agent evaluation; function calling overclaim; multi-turn tool use
