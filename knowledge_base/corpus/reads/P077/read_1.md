# P077 first read — ArCHer as a bounded multi-turn credit-assignment baseline

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL
- Authors: Yifei Zhou, Andrea Zanette, Jiayi Pan, Sergey Levine, Aviral Kumar
- Venue: ICML 2024
- PDF: `knowledge_base/staging/plan05_sat_a3/P077_archer.pdf`
- PDF SHA-256: `9a25030a872732dc5fc544e04e3d20382be1d512eeefd97e7e92179dd2c5f8ec`
- Parse check: 39 physical pages

## Changed computation

ArCHer models an Agent task as a hierarchy: utterances are high-level actions and tokens form an embedded low-level MDP. An off-policy temporal-difference critic estimates long-horizon utterance value, while a token policy is updated with the utterance-level advantage. This changes credit assignment across turns rather than attaching terminal reward uniformly to all tokens.

## Evidence and closest lineage

- The online variant combines replay-based high-level Q/V learning with low-level REINFORCE; the paper also sketches an offline IQL/AWR variant.
- Experiments cover five multi-turn environments, including Twenty Questions, Guess My City, and WebShop, with PPO, filtered behavior cloning, and CHAI comparisons.
- The reported “about 100x” sample-efficiency claim is a narrow Twenty Questions comparison: PPO requires more than 100k interactions while ArCHer crosses return -17 in fewer than 1k.
- Ablations attribute stability to temporal-difference critics; Monte-Carlo critics are less stable, and offline REINFORCE collapses without regularization.

## Measurement and fairness boundaries

- The method fundamentally learns from environment rewards and repeated interaction. The user excluded environment-feedback learning as a target research direction, so this source is retained only as a canonical baseline and lineage constraint for temporal credit assignment.
- Main experiments mostly use a GPT-2 actor and RoBERTa critic; scaling evidence reaches Mistral-7B only in an ablation.
- Several environments use a simulated Flan-T5-small oracle. The results do not establish an oracle-free general Agent-learning recipe.
- The paper documents reward hacking, repetition, and out-of-distribution collapse; online learning still needs thousands of interactions.
- Offline results are explicitly preliminary and not extensively evaluated. CHAI with five samples has roughly four-times runtime in the reported comparison.

## Draft knowledge objects

### Operator draft: `Hierarchical Utterance Critic with Token Actor`

Use an utterance-level temporal-difference value signal to assign long-horizon credit, then train the within-turn token policy from the utterance advantage. Retain only as baseline/lineage because its supervision depends on environment feedback.

### Failure draft: `Token-Local or Terminal Credit Misses Turn-Level Delayed Value`

Single-turn or uniformly broadcast terminal objectives cannot distinguish an apparently weak turn that enables later success from a locally fluent but strategically harmful turn.

## Draft Evidence locators

- pp.1–6: hierarchical MDP, high-level critic, low-level actor, and algorithm definition.
- pp.7–12: online/offline instantiations, experimental environments, and baselines.
- pp.13–18: main results, sample-efficiency comparison, scaling and critic ablations.
- pp.19–24 and appendices: reward hacking, stability, offline limitations, compute and implementation details.

All claims remain draft until independent read and reconciliation.
