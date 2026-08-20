<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-smt-preexecution-policy-guard","card_kind":"operator","paper_id":"P046","evidence_ids":["ev-p046-operator-core"],"source_refs":[{"path":"papers/P046_solver_aided_verification.pdf","sha256":"0b29985358a4735f7e2ad032225cf5299080be4ef33cf8539f2550c8bbf06807"}]} -->
# SMT Pre-Execution Policy Guard

## Intervention target
[CODEX_SYNTHESIS] Policy compliance of a planned tool call before an irreversible side effect.

## Before and after computation
[CODEX_SYNTHESIS] The LLM sees natural-language policies and directly executes its call. The changed computation extracts state, checks formal constraints with Z3, blocks UNSAT calls, and may replan from a conflict core.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: planned API call, arguments, observable state, formal policy. Output: SAT/UNSAT and optional conflict explanation. Timing: between planning and tool execution.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] A formal satisfiability check can enforce encoded constraints that prompt-following alone violates.

## Predicted observable signature
[CODEX_HYPOTHESIS] Policy precision should rise while false blocks, recall loss, solver/replanning cost, and encoding errors are reported.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Guarantees stop at the reviewed encoding and extracted state; automatic formalization can be incomplete or underconstrained.

## Source lineage
[CODEX_SYNTHESIS] Prompted compliance → natural-language reviewer → solver-enforced precondition.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p046-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] SMT; Z3; pre-execution guard; tool policy; satisfiability; unsat core

