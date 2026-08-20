<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-grouped-masked-history-step-credit","card_kind":"operator","paper_id":"P025","evidence_ids":["ev-p025-failure-core","ev-p025-grouped-step-influence"],"source_refs":[{"path":"papers/P025_lazy_agents_deliberation.pdf","sha256":"5447d5ad949dd4b0061c36b80e395c97c1dc7534960576660096a2420408fc00"}]} -->
# Grouped Masked-History Step-Influence Credit

## Intervention target
[CODEX_SYNTHESIS] Credit assigned to individual sequential reasoning turns under a shared terminal reward.

## Before and after computation
[CODEX_SYNTHESIS] A trajectory-level advantage is broadcast uniformly across turns. The changed computation removes turn-count normalization, groups semantically similar steps across rollouts, and measures how masking one history step changes the log-probability of the next step.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: rollout steps, semantic groups, full histories, and histories with one step masked. Output: grouped one-step causal-influence estimates that contribute to step-level training advantage. Timing: during online RL credit computation after rollouts are available.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Stable step-sensitive credit should reduce incentives for one sequential agent to produce trivial turns while another carries the trajectory.

## Predicted observable signature
[CODEX_HYPOTHESIS] Influence should follow information-changing steps rather than response length, and masking high-credit steps should alter the next-step distribution more strongly.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Semantic grouping quality, log-probability access, and the combined restart/outcome-reward terms complicate attribution; one-step influence is not a complete estimate of terminal causal contribution.

## Source lineage
[CODEX_SYNTHESIS] Shared trajectory reward → lazy-turn diagnosis → grouped masked-history step influence → step-sensitive online RL credit.

## Evidence ledger
[AUTHOR_FACT] The paper reports lazy-agent collapse under uniformly assigned group advantage and defines grouped one-step influence using full versus masked histories. [[evidence:ev-p025-failure-core]] [[evidence:ev-p025-grouped-step-influence]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] lazy agents; masked history; grouped causal influence; step credit; multi-agent online RL; length normalization
