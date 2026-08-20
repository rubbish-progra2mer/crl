<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-constrained-plan-surface-validity","card_kind":"failure","paper_id":"P004","evidence_ids":["ev-p004-failure-core","ev-p004-macro-constraint-failure"],"source_refs":[{"path":"papers/P004_travelplanner.pdf","sha256":"a7c7edd67c90e9997e940aaa7b435d46a8b201ed119c125b341b01b215454133"}]} -->
# Fluent Plans Fail Structured Constraints

## Observed failure
[AUTHOR_FACT] In TravelPlanner, agents may deliver plans that satisfy some individual constraints while overlooking others and failing holistic multi-constraint validity. [[evidence:ev-p004-failure-core]] [[evidence:ev-p004-macro-constraint-failure]]

## Conditions and scope
[CODEX_SYNTHESIS] Multi-day tool-grounded travel planning with structured constraints and limited interaction steps.

## Failed intervention
[CODEX_SYNTHESIS] Free-form reasoning and tool access do not reliably maintain a globally valid plan across all fields.

## Evidence and alternative explanations
[CODEX_SYNTHESIS] Failures may also arise from information extraction, unavailable environment options, or benchmark-specific constraints; the evidence does not isolate one internal cause.

## Warning for future candidates
[CODEX_SYNTHESIS] A planning Candidate must measure structured feasibility and constraint violations, not only answer quality or delivery rate.

## Possible repair boundary
[CODEX_HYPOTHESIS] A repair may add explicit constraint state, verification, or revision, but it must show benefit under matched model/tool budget.

## Evidence ledger
[AUTHOR_FACT] The cited passages bind the benchmark scope and its measured macro-constraint failure to admitted PDF bytes and current Passage SHA values. [[evidence:ev-p004-failure-core]] [[evidence:ev-p004-macro-constraint-failure]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] TravelPlanner; constraint violation; fluent invalid plan; hard constraints; commonsense constraints
