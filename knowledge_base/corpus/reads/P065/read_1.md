# P065 first read — anchor-state step credit

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Group-in-Group Policy Optimization for LLM Agent Training
- Authors: Lang Feng et al.
- Venue: NeurIPS 2025
- PDF: `knowledge_base/staging/plan05_sat_a1/P065_gigpo.pdf`
- PDF SHA-256: `f6a4d4559c41048be67a0e4a062f9957996fc79e6a80f65fe66f1140fac82dcd`
- Parse check: 27 physical pages

## Changed computation

GiGPO keeps an episode-level group-relative advantage and adds a step-level advantage without new rollouts. It retroactively groups actions taken from the same repeated environment state across trajectories, compares their discounted returns, and adds this micro advantage to the macro trajectory advantage. Exact or longest-common-subsequence state matching supplies the anchors.

## Evidence and closest lineage

With matched rollout groups and hyperparameters, GiGPO beats GRPO/RLOO/PPO on ALFWorld and WebShop for Qwen2.5 1.5B/7B and improves search-augmented QA at 3B/7B. Three-seed results and structural ablations show that removing either episode or step advantage hurts. Most states in the studied environments recur enough to create non-singleton groups, and grouping/arithmetic adds negligible time relative to rollout/training.

## Measurement and fairness boundaries

- The mechanism requires repeated or matchable states. In open-ended text/tool traces, exact states can be rare and similarity thresholds may merge non-equivalent situations.
- Grouped actions inherit downstream discounted return; shared later choices can still confound a step's causal value.
- The strongest evidence includes ALFWorld, an embodied carrier outside CRL scope; WebShop and search QA remain relevant text/tool carriers.
- Claimed overhead excludes the base RL rollout and GPU training cost; it means “little extra versus GRPO,” not cheap training.
- Normalization choice is task-dependent, and some per-subtask variance is large.

## Draft knowledge objects

### Operator draft: `Anchor-State Relative Credit Assignment`

Reuse naturally repeated states across trajectory groups as counterfactual anchors: compare the downstream return of different actions from a matched state and combine the local preference with the episode-level signal.

### Failure draft: `Anchor Credit Collapses When States Are Not Reliably Matchable`

Exact matching produces few anchors in open-ended environments, while approximate matching can group materially different states and assign misleading relative credit; without anchors the method reduces to trajectory-level GRPO.

## Draft Evidence locators

- pp.1–6: two-level advantage, anchor grouping, discounted return and objective.
- pp.7–9: matched experiments, three-seed results, ablations and group-size dynamics.
- p.10: cost accounting and state-matching limitation.

All claims remain draft until independent read and reconciliation.
