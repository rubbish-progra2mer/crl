# RUN_CHARTER

RUN_ID: 20260726_1955_run03
RUN_NUMBER: run03
CREATED_AT: 2026-07-26T19:55:49+08:00
MODE: RESEARCH
SHARED_KNOWLEDGE_BASE: crl_agent_v3/knowledge_base
AGENT_TOPOLOGY: MAIN_CODEX_PLUS_THREE_LEAF_REVIEWERS_ONLY
NON_REVIEW_SUBAGENTS: FORBIDDEN
REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN
PAID_API_PROVIDERS: deepseek
PAID_API_BUDGET_CEILING: USER_UNLIMITED_GRANTED_2026-07-26 (no ceiling set by the user; spend judiciously and report actual token usage and cost estimate per experiment)
PAID_API_PURPOSE_BOUNDARY: experiment subject rollouts, data generation, and judging/scoring inside this Run's own experiments

## User intent

First formal research Run after the machine reached
`READY_FOR_RESEARCH_USAGE`. The user issued a bare start with no research
sub-direction and explicitly instructed the Main Codex to choose the
research question autonomously from the shared paper knowledge base, to
retrieve and judge on its own, and to run without mid-way stops. The
target output is a qualified `DELIVERY.md`: a research seed worth
scaling, not a paper draft and not a proven method.

Boundary: the Main Codex performs every research action itself. The only
subagents permitted in this Run are the three fresh leaf Reviewers of the
formal review, launched after the version's scientific bytes are frozen.
On any condition the Main Codex cannot resolve alone (paid-API boundary
breach, external service failure, data licensing), the Run moves to
`BLOCKED_EXTERNAL` and reports.

## Paid API authorization notes

Authorization was granted by the user on 2026-07-26 in the same message
that started this Run. The key exists only as a process-scoped temporary
environment variable at experiment execution time; it is NEVER written to
any Markdown, source file, config, argv, artifact, capture, Reviewer
Packet or log, and is never echoed. Experiment code must redact all
exception and debug output, and every exact-execution-readiness check must
confirm that captures contain no secret pattern. Any provider, model class
or purpose outside this boundary still requires a new stop-and-ask before
cost is incurred.
