<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p019","card_kind":"paper","paper_id":"P019","evidence_ids":["ev-p019-step-level-calibration","ev-p019-ground-truth-calibration-oracle"],"source_refs":[{"path":"papers/P019_steca.pdf","sha256":"f0957a2acf89227b77922ee4d5a9de10759cc6ad89778077f048c178a0184703"}]} -->
# STeCa: Step-level Trajectory Calibration for LLM Agent Learning

## Role in the knowledge base
[CODEX_SYNTHESIS] Agent-learning source for local trajectory calibration and an explicit oracle boundary.

## Problem and setting
[CODEX_SYNTHESIS] Failed long-horizon agent trajectories with step-level correction targets.

## Changed computation
[CODEX_SYNTHESIS] STeCa replaces whole-trajectory negatives with calibrated local steps derived using ground-truth task feedback.

## Evidence-backed findings
[AUTHOR_FACT] The source motivates localized credit instead of treating every action in a failed trajectory as equally wrong. [[evidence:ev-p019-step-level-calibration]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Ground-truth calibration is an oracle information advantage and may not be available at deployment.

## Lineage and baselines
[CODEX_SYNTHESIS] Precedes verified critical-step and counterfactual repair methods.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p019-step-level-calibration]] [[evidence:ev-p019-ground-truth-calibration-oracle]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] STeCa; step-level trajectory calibration; local credit assignment; oracle correction; failed trajectory

