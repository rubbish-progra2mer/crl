# P080 first read — capability-aware search depth with gold-supervised training

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning
- Authors: Jingbo Sun, Wenyue Chong, Songjun Tu, Qichao Zhang, Yaocheng Zhang, Jiajun Chai, Xiaohan Wang, Wei Lin, Guojun Yin, Dongbin Zhao
- Venue: Findings of ACL 2026
- PDF: `knowledge_base/staging/plan05_sat_a3/P080_autosearch.pdf`
- PDF SHA-256: `ab078ee4e0221166d92ea3856d028f92a9348899f8fa9d63ec8841764edd8a86`
- Parse check: 21 physical pages

## Canonical mechanism

AutoSearch forces an intermediate answer after each retrieval step and defines the earliest exact match to the gold answer as the capability-aware minimal sufficient search depth. Reinforcement-learning rewards then favor reaching that depth, penalize under/over-search, and reward F1 improvement between successive intermediate answers.

## Evidence and closest lineage

- The policy is trained with PPO, with retrieved tokens masked from the policy loss; a GRPO variant is reported as comparable.
- Base reward checks outcome/format, efficiency reward distinguishes under-, effective-, and over-search, and quality reward uses F1 gain over the prior intermediate answer.
- Training uses NQ and HotpotQA with Qwen2.5-3B/7B and a fixed maximum of zero to four searches; tests include in- and out-of-distribution QA datasets.
- Removing efficiency reward drives average depth upward, while removing quality reward collapses depth and accuracy, supporting the two reward components within this setup.

## Measurement and fairness boundaries

- “Minimal sufficient” is labeled during training by exact match against gold answers; F1 reward also uses gold answers. The method is therefore not oracle-free even though test-time stopping does not receive gold labels.
- Exact match can be achieved from parametric memory or contamination, so the derived depth need not prove that retrieved evidence was sufficient.
- Evaluation is bounded QA retrieval, not open-web Deep Research, and maximum search depth is deliberately low.
- Reported inference savings are not compared against the total training cost; experiments use eight H20 GPUs for the stated RL setup.
- The source diagnoses adaptive stopping but cannot by itself justify a general non-oracle stopping rule.

## Draft knowledge objects

### Operator draft: `Gold-Supervised Minimal Search-Depth Policy`

At training time, label the earliest step whose intermediate answer matches gold, then learn a policy that balances answer improvement against under- and over-search. The name must preserve the oracle boundary.

### Failure draft: `Fixed Search Depth Causes Both Under- and Over-Search`

A global retrieval budget ignores question difficulty and model capability: short questions waste calls, while complex questions stop before acquiring enough evidence.

## Draft Evidence locators

- pp.1–4: minimal sufficient depth definition and self-answering loop.
- pp.5–8: reward equations, PPO/GRPO details and oracle labels.
- pp.9–13: main results, efficiency measures, baselines and ablations.
- pp.14–17: compute, fixed-depth scope and stated limitations.

All claims remain draft until independent read and reconciliation.
