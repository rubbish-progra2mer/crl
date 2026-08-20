<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-gold-context-does-not-solve-knowledge-use","card_kind":"failure","paper_id":"P036","evidence_ids":["ev-p036-failure-core"],"source_refs":[{"path":"papers/P036_tau_knowledge.pdf","sha256":"f6fbe657daa349b1495bef6fecd7b1a3c845da3bf296d2589eedb45e051613bd"}]} -->
# Gold Context Does Not Solve Knowledge Use

## Observed failure
[AUTHOR_FACT] Providing the ground-truth documents directly still leaves substantial task failure. [[evidence:ev-p036-failure-core]]

## Conditions and scope
[CODEX_SYNTHESIS] Conversational agents must combine procedural documents, tool discovery, state changes, and user interaction.

## Failed intervention
[CODEX_SYNTHESIS] A retrieval-only diagnosis assumes that access to the right text implies correct procedural reasoning and action.

## Evidence and alternative explanations
[CODEX_SYNTHESIS] Long context, tool interface, simulator behavior, and model limits can all contribute after retrieval is removed.

## Warning for future candidates
[CODEX_SYNTHESIS] A knowledge/memory Candidate must distinguish document access from reasoning-over-evidence and state-changing execution.

## Possible repair boundary
[CODEX_HYPOTHESIS] Structured procedure extraction or decision-time evidence control may help, but should be tested against the gold-document condition.

## Evidence ledger
[AUTHOR_FACT] The cited passages bind this failure to admitted PDF bytes and current Passage SHA values. [[evidence:ev-p036-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] gold context; knowledge-use bottleneck; retrieval not sufficient; procedural reasoning; tool discovery

