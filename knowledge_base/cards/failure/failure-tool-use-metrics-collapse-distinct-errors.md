<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-tool-use-metrics-collapse-distinct-errors","card_kind":"failure","paper_id":"P039","evidence_ids":["ev-p039-failure-core","ev-p039-aggregate-score-masking"],"source_refs":[{"path":"papers/P039_toolfailbench.pdf","sha256":"6588af66fd477d9764c20c52c2adb7d92fcbf6a788fe09713bc71916862d3009"}]} -->
# Aggregate Tool Success Collapses Distinct Failure Modes

## Observed failure
[AUTHOR_FACT] Tool skipping and result ignoring can look similar under final task accuracy; ToolFailBench separately labels them alongside fabrication and unnecessary calls. [[evidence:ev-p039-aggregate-score-masking]] [[evidence:ev-p039-failure-core]]

## Conditions and scope
[CODEX_SYNTHESIS] Paired tool-required and no-tool control tasks under a controlled function-calling protocol.

## Failed intervention
[CODEX_SYNTHESIS] An aggregate metric does not reveal whether the model selected, executed, trusted, or unnecessarily invoked a tool.

## Evidence and alternative explanations
[CODEX_SYNTHESIS] Parser/template errors and judge common modes can create apparent behavioral failures; this paper is a diagnostic carrier, not a universal taxonomy proof.

## Warning for future candidates
[CODEX_SYNTHESIS] Tool-use Candidates must report stage-specific errors and clean controls in addition to final success.

## Possible repair boundary
[CODEX_HYPOTHESIS] Separate necessity gating, result-grounding, and argument validation metrics before proposing one combined repair.

## Evidence ledger
[AUTHOR_FACT] The cited passages bind aggregate-score masking and the stage-specific taxonomy to admitted PDF bytes and current Passage SHA values. [[evidence:ev-p039-aggregate-score-masking]] [[evidence:ev-p039-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Tool-Skip; Result-Ignore; fabrication; unnecessary tool call; failure taxonomy
