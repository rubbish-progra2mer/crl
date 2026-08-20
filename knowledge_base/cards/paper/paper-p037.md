<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p037","card_kind":"paper","paper_id":"P037","evidence_ids":["ev-p037-evaluation-core"],"source_refs":[{"path":"papers/P037_toolsandbox.pdf","sha256":"3449baed1d8e0f4c07dbc859621899685eed8a6a0445a1ae8909c178e6b6173e"}]} -->
# ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities

## Role in the knowledge base
[CODEX_SYNTHESIS] Stateful tool-use evaluation carrier with multi-path trajectory scoring.

## Problem and setting
[CODEX_SYNTHESIS] Conversational tool use over mutable world state and a simulated user.

## Changed computation
[CODEX_SYNTHESIS] Milestone/Minefield DAGs score valid temporal progress without requiring one exact reference trajectory.

## Evidence-backed findings
[AUTHOR_FACT] The evidence supports multi-path stateful evaluation. [[evidence:ev-p037-evaluation-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Human-authored milestones encode process priors; simulator errors and inaction rewards can distort scores.

## Lineage and baselines
[CODEX_SYNTHESIS] Complements terminal-state evaluation and dual-control benchmarks.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p037-evaluation-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] ToolSandbox; milestone DAG; minefield; stateful tool use; multi-path evaluation

