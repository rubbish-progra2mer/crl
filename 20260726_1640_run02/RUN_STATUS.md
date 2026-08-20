# RUN_STATUS

RUN_ID: 20260726_1640_run02
RUN_NUMBER: run02
STATUS: DELIVERED
MODE: COMMISSIONING
CURRENT_VERSION: v007
CURRENT_PHASE: DELIVERED_SEED_WITH_RESERVED_CONFIRMATION_HANDOVER
LAST_DURABLE_ARTIFACT: DELIVERY.md
NEXT_ACTION: NONE_RUN_CLOSED; receiver executes the reserved C-bucket
  plan per DELIVERY.md and decision_v007 ERRATUM E10; machine Ready
  switch is a separate user decision.
UPDATED_AT: 2026-07-27T01:15:00+08:00

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
