<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-lazy-agent-effective-single-agent-collapse","card_kind":"failure","paper_id":"P025","evidence_ids":["ev-p025-failure-core"],"source_refs":[{"path":"papers/P025_lazy_agents_deliberation.pdf","sha256":"5447d5ad949dd4b0061c36b80e395c97c1dc7534960576660096a2420408fc00"}]} -->
# Nominal Multi-Agent Training Collapses to an Effective Single Agent

## Observed failure
[AUTHOR_FACT] One sequential role can contribute trivially while later roles perform the effective reasoning. [[evidence:ev-p025-failure-core]]

## Conditions and scope
[CODEX_SYNTHESIS] Sequential multi-agent reasoning trained with a shared sparse terminal reward.

## Failed intervention
[CODEX_SYNTHESIS] Uniform group advantage and turn normalization assign credit without measuring causal role contribution.

## Evidence and alternative explanations
[CODEX_SYNTHESIS] Role prompts, model capacity, ordering, and task decomposition may also cause inactivity; shared reward is not proven to be the sole cause.

## Warning for future candidates
[CODEX_SYNTHESIS] More agents or messages do not demonstrate collaboration; run role removal/replacement and contribution tests.

## Possible repair boundary
[CODEX_HYPOTHESIS] Counterfactual contribution or localized credit may help, but must be separated from restart and length-normalization changes.

## Evidence ledger
[AUTHOR_FACT] The cited passages bind this failure to admitted PDF bytes and current Passage SHA values. [[evidence:ev-p025-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] lazy agent; effective single agent; shared reward; role contribution; multi-agent collapse

