<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p003","card_kind":"paper","paper_id":"P003","evidence_ids":["ev-p003-search-control-loop","ev-p003-generic-reflection-local-minimum"],"source_refs":[{"path":"papers/P003_lats.pdf","sha256":"a6b84613eeeaa3beb979ac3e34cbb3575bceb7ccf6050a2c2fc677d5e3a3ab19"}]} -->
# Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models

## Role in the knowledge base
[CODEX_SYNTHESIS] Unifies language-agent reasoning, acting, planning, and reflection inside an explicit tree-search control loop.

## Problem and setting
[CODEX_SYNTHESIS] Interactive decision tasks where an agent can branch on actions, observe environment feedback, and revisit earlier choices.

## Changed computation
[CODEX_SYNTHESIS] LATS adds node expansion, value estimation, environment feedback, reflection, and backtracking around a ReAct-style trajectory.

## Evidence-backed findings
[AUTHOR_FACT] The source supports a search-controlled agent loop rather than reflection as a free-standing improvement. [[evidence:ev-p003-search-control-loop]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Search, evaluator calls, reflection, and extra rollout budget change together; gains are not a single-component causal estimate.

## Lineage and baselines
[CODEX_SYNTHESIS] Extends ReAct and Tree of Thoughts toward environment-grounded agent search.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p003-search-control-loop]] [[evidence:ev-p003-generic-reflection-local-minimum]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] LATS; language agent tree search; value-guided backtracking; environment-grounded search; reflection local minimum

