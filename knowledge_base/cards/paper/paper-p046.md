<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p046","card_kind":"paper","paper_id":"P046","evidence_ids":["ev-p046-operator-core"],"source_refs":[{"path":"papers/P046_solver_aided_verification.pdf","sha256":"0b29985358a4735f7e2ad032225cf5299080be4ef33cf8539f2550c8bbf06807"}]} -->
# Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] Safety operator source for formal pre-execution policy checks.

## Problem and setting
[CODEX_SYNTHESIS] Tool calls subject to domain policies in a conversational airline environment.

## Changed computation
[CODEX_SYNTHESIS] An SMT solver checks a planned call before execution and blocks or replans on unsatisfiable policy constraints.

## Evidence-backed findings
[AUTHOR_FACT] The evidence supports a side-effect guard between planning and tool execution. [[evidence:ev-p046-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Guarantees are only as sound as manual policy encoding and state extraction; evaluation is narrow and benchmark-tuned.

## Lineage and baselines
[CODEX_SYNTHESIS] Formalizes pre-execution review beyond natural-language prompting.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p046-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] SMT guard; Z3; tool policy compliance; pre-execution interception; minimal unsat core

