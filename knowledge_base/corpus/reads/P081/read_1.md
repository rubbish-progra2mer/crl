# P081 first read — equal-budget independent reasoning aggregation baseline

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Self-Consistency Improves Chain of Thought Reasoning in Language Models
- Authors: Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou
- Venue: ICLR 2023
- PDF: `knowledge_base/staging/plan05_sat_a3/P081_self_consistency.pdf`
- PDF SHA-256: `1a49ce0373afc89d2d6e97fb1aa8230f6b818c70590d732a3187f753f4df6aba`
- Parse check: 24 physical pages

## Canonical mechanism

Self-consistency samples several independent chain-of-thought paths from the same model and prompt, extracts their final answers, and chooses the most frequent answer. There is no interaction, auxiliary verifier, additional training, or cross-sample communication. For Agent research it is primarily a compute-matched baseline against debate, search, reflection, or multi-agent coordination.

## Evidence and closest lineage

- Experiments use UL2-20B, LaMDA-137B, PaLM-540B, and GPT-3/Codex across arithmetic, commonsense, symbolic, and other reasoning tasks.
- The main setup commonly samples 40 paths; curves show much of the gain can emerge with fewer paths and then saturate.
- Unweighted majority vote performs similarly to normalized probability aggregation, while unnormalized sequence likelihood is worse.
- With the same samples or beams, self-consistency outperforms sample-and-rank and beam-search variants; prompt and model ensembles are also weaker in the reported comparisons.

## Measurement and fairness boundaries

- Inference cost grows roughly linearly with path count. The paper recommends trying five or ten paths where cost matters.
- Aggregation requires a fixed or parseable final-answer space and task-specific answer extraction; it does not directly handle open-ended implement generation.
- Paths can be nonsensical or factually wrong, and majority agreement is not evidence of grounding.
- Large portions of the evidence use unavailable proprietary models and substantial TPU inference.
- This is a reasoning-decoding method rather than a full Agent method; CRL should not inflate it into an interactive coordination Operator.

## Draft knowledge objects

### Baseline Operator draft: `Fixed-Budget Independent Path Aggregation`

Spend the same generation budget on independent paths from one model and aggregate terminal answers before attributing gains to interaction, debate, reflection, or multi-agent structure.

### Failure draft: `Interactive Gains Can Vanish Against Independent Sampling`

If an Agent method receives several generations but is compared only with one greedy path, its gain may come from test-time compute and answer aggregation rather than the proposed interaction mechanism.

## Draft Evidence locators

- pp.1–3: sampling and marginalization mechanism.
- pp.4–8: tasks, models, decoding setup, baselines and main results.
- p.9: relation to reranking and the no-extra-training boundary.
- pp.16–18: robustness, equal-path ensembles and inference resources.

All claims remain draft until independent read and reconciliation.
