<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p038","card_kind":"paper","paper_id":"P038","evidence_ids":["ev-p038-operator-core"],"source_refs":[{"path":"papers/P038_agentdojo.pdf","sha256":"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913"}]} -->
# AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] Safety benchmark and source for pre-exposure action-surface restriction.

## Problem and setting
[CODEX_SYNTHESIS] Tool-using agents receive prompt injections through untrusted tool-returned data.

## Changed computation
[CODEX_SYNTHESIS] A tool filter selects the task-relevant action set before the agent processes untrusted content.

## Evidence-backed findings
[AUTHOR_FACT] The evidence defines an isolation-style pre-exposure defense. [[evidence:ev-p038-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Shared-tool tasks and dynamic tool selection remain hard; prompt/interface differences confound cross-model rankings.

## Lineage and baselines
[CODEX_SYNTHESIS] Connects agent safety evaluation to capability restriction before observation.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p038-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] AgentDojo; prompt injection; tool filter; untrusted tool output; action-surface restriction

