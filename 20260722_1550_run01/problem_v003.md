# Research Problem

## User intent

Complete a real commissioning cycle that produces a reviewable research implement rather than a fixture or interface sanity check.

## Text/tool LLM Agent scope

Audit whether target-aware instructions in a large-corpus tool-retrieval benchmark provide label-conditioned information that must be separated from query-only open-world retrieval evidence.

## Soft constraints

- Prefer a local, deterministic experiment with public data and two mechanistically different retrievers.
- Preserve the full public tool corpus at the pinned dataset revision; report any count drift from the 43,215-tool paper snapshot.
- Make development and confirmation source-disjoint.

## Hard exclusions

- No paid model or API calls.
- No fixture-only evidence, oracle-menu evaluation, or single tiny tool menu.
- No claim that the implement improves a deployable retriever.
- No claim that all ToolRet results are invalid; the audit concerns interpretation of the target-aware `w/ inst.` view.
- No non-Reviewer subagent may participate in research, implementation, experiment, audit, or decision work.

## Cost authorization

Paid API use is not authorized and is not required. The experiment uses the shared Python 3.11.15 environment, the local RTX 5060 Ti, public Hugging Face dataset endpoints, and already cached local retrieval models.
