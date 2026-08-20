<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p005","card_kind":"paper","paper_id":"P005","evidence_ids":["ev-p005-operator-core"],"source_refs":[{"path":"papers/P005_toolllm.pdf","sha256":"76f7d1a6acd0c8d86d0bd41340dd12976643b9bbcaed3008a2357ef2d492ff8a"}]} -->
# ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs

## Role in the knowledge base
[CODEX_SYNTHESIS] Tool-use ancestor for large API retrieval plus failure-aware action search.

## Problem and setting
[CODEX_SYNTHESIS] Single- and multi-tool instructions over a large collection of real APIs.

## Changed computation
[CODEX_SYNTHESIS] DFSDT lets the model branch and backtrack after tool-call errors instead of following one irreversible ReAct path.

## Evidence-backed findings
[AUTHOR_FACT] The source defines a depth-first decision-tree controller around tool calls. [[evidence:ev-p005-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Training data, API retriever, search budget, model tuning, and evaluator all contribute; DFSDT is not isolated under equal cost.

## Lineage and baselines
[CODEX_SYNTHESIS] Extends ReAct with explicit backtracking and is a baseline for later tool-orchestration search.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p005-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] ToolLLM; ToolBench; DFSDT; API retrieval; tool-call backtracking

