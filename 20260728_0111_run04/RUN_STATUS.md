# RUN_STATUS

RUN_ID: 20260728_0111_run04
RUN_NUMBER: run04
STATUS: ACTIVE
MODE: COMMISSIONING
CURRENT_VERSION: v004
CURRENT_PHASE: V003_PROBLEM_LEVEL_KILL_RECORDED_V004_PROBLEM_DISCOVERY
LAST_DURABLE_ARTIFACT: research_map_v003.md
NEXT_ACTION: MAIN_CODEX_IDENTIFY_EXECUTION_CONSTRAINED_V004_NODE
UPDATED_AT: 2026-07-28T01:49:19.8477991+08:00

## Versioned root artifacts

Candidate-scoped artifacts are versioned at the Run root. `manage_run.py` does not create or judge them:

The Main Codex must publish them through `ResearchWorkspace(..., version="v001")`; plain Markdown without formal Workspace metadata is invalid.

- `problem_v001.md`
- `research_map_v001.md`
- `candidate_v001.md`
- `evidence_packet_v001.md`
- `implementation_v001/`
- `experiment_v001/`
- `review_v001/`
- `decision_v001.md`
