# Research Problem

## Commissioning objective

Produce a reviewable research implement from a real public-data cycle. The implement must add a falsifiable evaluation computation, survive untouched source-disjoint Confirmation, and pass three independent Reviewers before Delivery.

## Problem after v004

v004 showed that one deterministic same-source, length-matched wrong-target instruction is an informative but selection-sensitive control. Its aggregate effects and bootstrap intervals were positive, yet MiniLM was exactly neutral on one of eight Confirmation sources. The v004 universal per-source Claim therefore failed and remains frozen at `experiment_v004/result.md` SHA-256 `33c0e0865849ae131740584fe9b3103cb3f0cbb9029251b6a951b33e69ada961`.

The v005 problem is narrower: estimate the source-cluster average target-conditioning information in ToolRet's aligned instruction view without making the estimate depend on a single wrong-target donor.

## Scope and exclusions

- Use the same pinned public ToolRet query/tool revisions and full 44,453-row served corpus.
- Use three deterministic same-source, label-disjoint, closest-length donors per query.
- Use BM25 and the fixed local all-MiniLM-L6-v2 snapshot.
- Reuse the already frozen corpus and corpus embeddings; acquire only query configs that v001-v004 never fetched.
- Do not claim a deployable retriever improvement, benchmark invalidity, universal per-source positivity, causal identification, exhaustive qrels, or end-to-end Agent benefit.
- No paid API, LLM inference, fixture menu, hyperparameter search, or non-Reviewer subagent.

## Cost authorization

Public read-only Hugging Face access, the shared Python 3.11.15 environment, local CPU, and the RTX 5060 Ti are sufficient. No user credential or paid service is required.
