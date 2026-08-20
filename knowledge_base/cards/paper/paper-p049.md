<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p049","card_kind":"paper","paper_id":"P049","evidence_ids":["ev-p049-operator-core"],"source_refs":[{"path":"papers/P049_reinforced_agent.pdf","sha256":"352a4f39ae64d07722a7e63bfed3d9afad20f7529c406ee764af37d3503b40c8"}]} -->
# Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] Pre-execution reviewer operator for tool-calling agents.

## Problem and setting
[CODEX_SYNTHESIS] A provisional tool call can be inspected and revised before side effects.

## Changed computation
[CODEX_SYNTHESIS] An independent reviewer supplies bounded progressive feedback until approval or a maximum revision count.

## Evidence-backed findings
[AUTHOR_FACT] The evidence defines reviewer-before-execution computation. [[evidence:ev-p049-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Gains are domain-dependent, latency rises sharply, and selector/prompt optimization is not independently held out.

## Lineage and baselines
[CODEX_SYNTHESIS] Natural-language counterpart to formal SMT guards and tool-grounded critique.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p049-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Reinforced Agent; progressive feedback; provisional tool call; pre-execution reviewer; bounded revision

