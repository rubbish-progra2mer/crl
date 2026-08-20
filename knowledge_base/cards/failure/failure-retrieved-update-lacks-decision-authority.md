<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-retrieved-update-lacks-decision-authority","card_kind":"failure","paper_id":"P030","evidence_ids":["ev-p030-failure-core","ev-p030-recognition-application-gap"],"source_refs":[{"path":"papers/P030_stale_memory.pdf","sha256":"388f71f1eb952e7d7e7b19c2f25bfc744c47efa8ee00a548093b949432495109"}]} -->
# Retrieved Updates Do Not Automatically Control Decisions

## Observed failure
[AUTHOR_FACT] In STALE, explicit recognition of an outdated memory does not reliably transfer to applying the updated state in downstream behavior. [[evidence:ev-p030-failure-core]] [[evidence:ev-p030-recognition-application-gap]]

## Conditions and scope
[CODEX_SYNTHESIS] Implicit conflicts where a later fact invalidates an earlier belief and must affect downstream policy.

## Failed intervention
[CODEX_SYNTHESIS] Late fusion exposes both memories to the model but assigns no explicit authority to the updated state.

## Evidence and alternative explanations
[CODEX_SYNTHESIS] Recognition probes and policy tasks differ in difficulty; retrieval rank, prompt, and model capability can also affect the gap.

## Warning for future candidates
[CODEX_SYNTHESIS] Memory Candidates must test state application and policy adaptation, not only whether the new fact is retrieved or restated.

## Possible repair boundary
[CODEX_HYPOTHESIS] Write-side adjudication or constrained current-state readout is plausible if it improves application at fixed retrieval recall.

## Evidence ledger
[AUTHOR_FACT] The cited passages bind the SR/IPA distinction and measured recognition-to-application gap to admitted PDF bytes and current Passage SHA values. [[evidence:ev-p030-failure-core]] [[evidence:ev-p030-recognition-application-gap]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] stale memory; implicit conflict; recognition application gap; decision authority; policy adaptation
