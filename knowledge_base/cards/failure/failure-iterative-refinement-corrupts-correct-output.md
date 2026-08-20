<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-iterative-refinement-corrupts-correct-output","card_kind":"failure","paper_id":null,"evidence_ids":["ev-p033-operator-core","ev-p034-failure-core"],"source_refs":[{"path":"papers/P033_self_refine.pdf","sha256":"a07dfc5ada4ff818c77812dd581065a4e3e40f5736f2f36a97787a66da6e7825"},{"path":"papers/P034_refinebench.pdf","sha256":"ee5c4d93ddf6c0741f0d08042b6aca2e0f08c3d3bd70e6cc6c90378bbc2d8c7f"}]} -->
# Iterative Refinement Can Corrupt a Correct Output

## Observed failure
[AUTHOR_FACT] Repeated same-model revision can turn an initially correct answer into an incorrect one. [[evidence:ev-p033-operator-core]] [[evidence:ev-p034-failure-core]]

## Conditions and scope
[CODEX_SYNTHESIS] Self-Refine defines iterative feedback/revision; RefineBench observes transition failures under a minimal self-refinement protocol.

## Failed intervention
[CODEX_SYNTHESIS] The loop revises without a reliable defect detector, correctness gate, or monotonic acceptance rule.

## Evidence and alternative explanations
[CODEX_SYNTHESIS] The negative result is prompt-, domain-, model-, and evaluator-dependent; targeted external feedback can behave differently.

## Warning for future candidates
[CODEX_SYNTHESIS] A reflection Candidate must report correct→incorrect transitions and compare against keeping the initial answer or resampling at equal budget.

## Possible repair boundary
[CODEX_HYPOTHESIS] Verification, selective stopping, or external evidence may bound harm, but each added information source must be isolated.

## Evidence ledger
[AUTHOR_FACT] The cited passages bind this failure to admitted PDF bytes and current Passage SHA values. [[evidence:ev-p033-operator-core]] [[evidence:ev-p034-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] self-refinement degradation; correct-to-incorrect; stopping gate; keep-initial baseline; harmful revision

