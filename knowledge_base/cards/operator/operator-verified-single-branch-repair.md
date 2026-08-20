<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-verified-single-branch-repair","card_kind":"operator","paper_id":"P027","evidence_ids":["ev-p027-operator-core"],"source_refs":[{"path":"papers/P027_critical_step_optimization.pdf","sha256":"2278960362823372029670a209ba7f9ce969485cd47f831c0406bb6016c1f288"}]} -->
# Verified Single-Branch Counterfactual Repair

## Intervention target
[CODEX_SYNTHESIS] A localized decision inside a failed long-horizon trajectory.

## Before and after computation
[CODEX_SYNTHESIS] Whole failed trajectories become negative examples. The changed computation substitutes one candidate action, reruns the suffix, and creates a local preference only when terminal success flips.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: failed trajectory state, original action, proposed alternative, terminal verifier. Output: verified local preference pair. Timing: after failure and before policy update.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Local outcome-flipping comparisons reduce contamination from correct steps elsewhere in a failed trajectory.

## Predicted observable signature
[CODEX_HYPOTHESIS] Training pairs should be fewer and more causally localized; removing the verifier should increase noisy pairs.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] A strong teacher and gold verifier are information advantages; one successful branch does not prove unique causal responsibility.

## Source lineage
[CODEX_SYNTHESIS] Trajectory calibration → verified critical step → targeted preference optimization.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p027-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] CSO; verified critical step; counterfactual suffix rollout; local DPO; outcome flip

