# RUN_STATUS

RUN_ID: 20260726_1955_run03
RUN_NUMBER: run03
STATUS: DELIVERED
MODE: RESEARCH
CURRENT_VERSION: v001
CURRENT_PHASE: DELIVERED_SEED_WITH_RESERVED_CONFIRMATION_HANDOVER
LAST_DURABLE_ARTIFACT: DELIVERY.md
NEXT_ACTION: NONE_RUN_CLOSED; receiver executes DELIVERY.md scale-up
  roadmap (cross-model rerun first, then reserved C-bucket plan per
  preregistered gates with the E13 power warning); run03 is read-only.
UPDATED_AT: 2026-07-26T22:40:00+08:00

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
