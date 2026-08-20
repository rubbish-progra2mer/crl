<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p041","card_kind":"paper","paper_id":"P041","evidence_ids":["ev-p041-operator-core"],"source_refs":[{"path":"papers/P041_tool_call_necessity.pdf","sha256":"a05f71b904209ea49cbc9cd13434255aab4037f96640477810fb78a61b701ba0"}]} -->
# LLM Agents Already Know When to Call Tools - Even Without Reasoning

## Role in the knowledge base
[CODEX_SYNTHESIS] Tool-efficiency operator source for pre-generation necessity gating.

## Problem and setting
[CODEX_SYNTHESIS] Controlled tool-necessary and tool-unnecessary tasks across computation, knowledge, and reliability boundaries.

## Changed computation
[CODEX_SYNTHESIS] A probe reads the final input token's hidden states before generation to decide whether to call a tool.

## Evidence-backed findings
[AUTHOR_FACT] The evidence supports latent tool-necessity information in model hidden states. [[evidence:ev-p041-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Labels use forced no-tool outcomes and correctness oracles; probes require model access and per-model calibration.

## Lineage and baselines
[CODEX_SYNTHESIS] Separates whether-to-call control from API selection and argument generation.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p041-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] WHEN2TOOL; hidden-state probe; tool necessity; pre-generation gate; unnecessary call

