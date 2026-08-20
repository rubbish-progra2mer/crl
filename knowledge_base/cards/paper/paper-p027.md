<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p027","card_kind":"paper","paper_id":"P027","evidence_ids":["ev-p027-operator-core"],"source_refs":[{"path":"papers/P027_critical_step_optimization.pdf","sha256":"2278960362823372029670a209ba7f9ce969485cd47f831c0406bb6016c1f288"}]} -->
# Verified Critical Step Optimization for LLM Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] Localized agent-learning operator for verified counterfactual repair.

## Problem and setting
[CODEX_SYNTHESIS] Failed ReAct trajectories where an alternative action can be proposed and the suffix rerun.

## Changed computation
[CODEX_SYNTHESIS] CSO forms a local preference pair only when replacing one action flips the final task outcome.

## Evidence-backed findings
[AUTHOR_FACT] The source supports verified single-branch repair rather than labeling the full failed trajectory negative. [[evidence:ev-p027-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] A strong teacher and gold terminal verifier supply information advantages; a successful suffix does not prove unique causal responsibility.

## Lineage and baselines
[CODEX_SYNTHESIS] Refines STeCa-style local calibration with outcome-flipping counterfactuals.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p027-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] critical step optimization; counterfactual repair; local DPO pair; outcome flip; trajectory credit

