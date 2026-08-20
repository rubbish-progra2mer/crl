# Production retrieval v006: calibration judgment invocation

- Task ID: `prod-v006-calibration-annotator`
- Started at: `2026-07-20T21:34:00+08:00`
- Purpose: independently annotate expected relevant knowledge for the visible calibration split before any v006 retrieval result exists.

## Frozen snapshot

- Papers: 87
- Passages: 3498
- Evidence: 191
- Paper Cards: 87
- Operator Cards: 54
- Failure Cards: 51
- `CORPUS_SCOPE.md`: `af6c39170861e646491d874907598785024d06deace6d23e74314fd2486e516d`
- `CARD_SCHEMA.md`: `31f25ba79e842f232c52218351e39a01f231c1ff3cbdafa26f1a71b6905dce95`
- `manifest.json`: `801d44135f74a05653c4ee26c2731694460bd75047996dd22557d50ac0dc29bf`
- `evidence.json`: `704731a935eafaa921f55d812259d96b44ad38b0de463d0e40b793ee4de60bfd`
- `knowledge.plan06_next.sqlite`: `29b43f517af5e3f04b46a681e128ce4cde132740cfdf4b32568b722f411ac56c`
- `passages.plan06_next.npz`: `0c2554340178942c029464eb92359ab9e7381ba178e7cb8df8b563a13a0f464b`
- `cards_fts.plan06_next.sqlite`: `174198091e3200eec9d0c89c571325d8b8aa9e05ea784e7f630969546842e8fc`
- Paper Card aggregate: `ea1c7f89427656ede5eea9d69529666f8a3714e59d0a0524e8c4477167c9f72b`
- Operator Card aggregate: `7362f3405777889ba88ead056bd898ac822cf5c919129cbdc55fd797fcb3ee28`
- Failure Card aggregate: `81c6af3081825163811b35862af99eccc8d76fc754f2ac087bbffe4b5ce992de`
- `calibration_queries.json`: `5c6b08c2e1d63f66c68c159a52a5611a03267139ba285b04e4ec000e84e293c3`

No Card, Evidence, manifest, source or query may change during this task.

## Required output

Write only:

`crl_agent_v3/knowledge_base/evaluation/production_eval/v006/calibration_judgments.json`

The root object must contain `schema_version`, `split`, `attempt`, `annotation_protocol`, `snapshot`, `invocation_provenance`, and `judgments`. Use `attempt: v006`. For every query, produce exactly one judgment with:

- `query_id`
- `critical`
- `corpus_gap`
- `relevant_card_ids`
- `relevant_evidence_ids`
- `relevant_passage_ids`
- `rationale`

Relevance standard: Card top-k tests whether CRL can discover knowledge that materially bears on the research question. A source need not already satisfy every requested future control; missing controls remain evidence boundaries. Set `corpus_gap: true` only if no current Card/Evidence chain materially informs the requested Failure, Operator or source role without semantic overstatement. Every listed Card must resolve through current Evidence to exact Passage SHA records. Do not list a Card just because its title shares words.

## Allowed reads

- `AGENTS.md`, `crl_agent_v3/AGENTS.md`
- this invocation and v006 `calibration_queries.json`
- `crl_agent_v3/knowledge_base/CARD_SCHEMA.md`
- current `cards/paper`, `cards/operator`, `cards/failure`
- current `corpus/evidence.json`, `corpus/manifest.json`
- current PDFs only when a Card/Evidence boundary genuinely needs source confirmation
- `knowledge.plan06_next.sqlite` only for exact selected Passage-ID/SHA validation, never FTS or ranked search

## Forbidden reads and actions

- v006 hidden blind-query files or future blind outputs
- all v001–v005 evaluation files and results
- `cards_fts.plan06_next.sqlite`, `passages.plan06_next.npz`
- all Run, Candidate, experiment, reviewer, history and memory material
- Card FTS, hybrid retrieval, embedding search, rank inspection or query execution
- modification of any source, Card, Evidence, query, database or index

This is an independent annotation task, not scientific review. On completion, return only judgment count, corpus-gap query IDs, critical-gap query IDs and output SHA-256; do not include judgment contents.
