# RUN_CHARTER

RUN_ID: 20260726_1640_run02
RUN_NUMBER: run02
CREATED_AT: 2026-07-26T16:40:58+08:00
MODE: COMMISSIONING
SHARED_KNOWLEDGE_BASE: crl_agent_v3/knowledge_base
AGENT_TOPOLOGY: MAIN_CODEX_PLUS_THREE_LEAF_REVIEWERS_ONLY
NON_REVIEW_SUBAGENTS: FORBIDDEN
REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN

## User intent

User-approved controlled real-chain Commissioning test. The purpose is to
exercise the full CRL research chain (problem selection, knowledge queries,
kernel formation, candidate, workbench falsifier, promotion development,
seed readiness audit, three-reviewer review, decision) under real
authenticity requirements, and to surface machine defects. The user gave no
research sub-direction; the Main Codex selects the problem from the shared
knowledge base. On any condition the Main Codex cannot resolve alone, the
Run moves to BLOCKED_EXTERNAL and reports.

## Paid API authorization boundary

PAID_API_PROVIDERS: deepseek
PAID_API_BUDGET_CEILING: USER_UNLIMITED_GRANTED_2026-07-26 (spend judiciously; report actual usage per experiment)
PAID_API_PURPOSE_BOUNDARY: experiment subject rollouts, data generation, judging/scoring within this Run's experiments

Authorization granted by the user on 2026-07-26 after v001 closed with all
kernels probe-killed under local-only constraints. The API key itself is
NEVER written to any file, argv, artifact, packet or log; it exists only
as a process-scoped temporary environment variable at experiment execution
time, per the CRL.md paid-API protocol. Experiment code must redact all
exception/debug output; readiness checks must confirm captures contain no
secret patterns. Providers or purposes outside this boundary still require
a new stop-and-ask.
