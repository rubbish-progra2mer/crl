<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p040","card_kind":"paper","paper_id":"P040","evidence_ids":["ev-p040-failure-core"],"source_refs":[{"path":"papers/P040_false_success.pdf","sha256":"ab1307fdaaf97841bd09296bca225b736e8e9a712002ac123b1fab663f35ba6a"}]} -->
# From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] Core negative evidence for false-success claims after execution.

## Problem and setting
[CODEX_SYNTHESIS] Tau2 and AppWorld trajectories with text-independent environment ground truth.

## Changed computation
[CODEX_SYNTHESIS] The work compares an agent's completion language with actual terminal state and trains lightweight detectors.

## Evidence-backed findings
[AUTHOR_FACT] Environment-grounded evaluation exposes agents that claim completion despite unmet state. [[evidence:ev-p040-failure-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Only explicit self-assessment subsets are observed; prior shift, adversarial paraphrase, and new domains degrade detection.

## Lineage and baselines
[CODEX_SYNTHESIS] Extends terminal-state reliability evaluation into post-execution failure detection.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p040-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] false success; silent failure; environment ground truth; completion claim; status detector

