<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p028","card_kind":"paper","paper_id":"P028","evidence_ids":["ev-p028-operator-core"],"source_refs":[{"path":"papers/P028_memory_r1.pdf","sha256":"c206af4e792e9550f2aaec8a6c4d9b141d1ddcb587e781d7866870c8f3e4dd4f"}]} -->
# Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning

## Role in the knowledge base
[CODEX_SYNTHESIS] Learned memory-control source spanning write operations and downstream use.

## Problem and setting
[CODEX_SYNTHESIS] Long-horizon conversations with an external memory bank and QA outcomes.

## Changed computation
[CODEX_SYNTHESIS] Memory-R1 trains a Memory Manager for ADD/UPDATE/DELETE/NOOP and an Answer Agent for memory selection and reasoning.

## Evidence-backed findings
[AUTHOR_FACT] The evidence supports two-stage learned memory control rather than a static retrieval heuristic. [[evidence:ev-p028-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Reported variants, context-window descriptions, compute, and external model assets limit clean and lightweight attribution.

## Lineage and baselines
[CODEX_SYNTHESIS] Extends MemGPT-style managed storage toward outcome-trained CRUD and read control.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p028-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Memory-R1; learned memory CRUD; ADD UPDATE DELETE NOOP; answer agent; outcome-driven memory

