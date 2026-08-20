# Production retrieval v006: hidden blind judgment invocation

- Task ID: `prod-v006-blind-annotator`
- Started at: `2026-07-20T21:38:00+08:00`
- Purpose: independently annotate expected relevant knowledge for the hidden split before any v006 blind retrieval result exists.

## Frozen inputs

- Blind queries: `knowledge_base/evaluation/production_eval/v006/blind_queries.json`
- Blind-query SHA-256: `d8695840b89cf56501984e8cf0a06bcf8a10cf0a5c4098e577aa6d7473f9b743`
- Papers / Passages / Evidence: 87 / 3498 / 191
- Paper / Operator / Failure Cards: 87 / 54 / 51
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

No Card, Evidence, source, query or derived snapshot may change during this task.

## Required output

Write exactly one file:

`crl_agent_v3/knowledge_base/evaluation/production_eval/v006/blind_judgments.json`

The root object must contain `schema_version`, `split`, `attempt`, `annotation_protocol`, `snapshot`, `invocation_provenance`, `judgments`, and `summary`. Use `attempt: v006`. Preserve hidden-query order. For every query, write exactly one judgment with:

- `query_id`
- `critical`
- `corpus_gap`
- `relevant_card_ids`
- `relevant_evidence_ids`
- `relevant_passage_ids`
- `rationale`

Relevance standard: Card top-k tests knowledge discovery. A Card is relevant when its Evidence materially bears on the requested mechanism, failure, boundary or source role; it need not satisfy every future experimental control. Missing controls are evidence boundaries, not automatically corpus gaps. `corpus_gap` is true only when no current Card/Evidence chain can materially inform the request without semantic overstatement. Every listed Card must resolve through current Evidence to exact Passage SHA records. Do not infer relevance from titles alone.

The summary must report total judgments, critical queries, ordinary queries, critical corpus-gap IDs and ordinary corpus-gap IDs. A critical corpus gap is an integrity blocker and must be reported; do not conceal it or lower the label.

## Allowed reads

- `AGENTS.md`, `crl_agent_v3/AGENTS.md`
- this invocation and v006 `blind_queries.json`
- current `CARD_SCHEMA.md`, `cards/paper`, `cards/operator`, `cards/failure`
- current `corpus/evidence.json`, `corpus/manifest.json`
- current PDFs only for a genuine source-boundary question
- `knowledge.plan06_next.sqlite` only for exact selected Passage-ID/SHA validation, never FTS or ranked search

## Forbidden reads and actions

- v006 `calibration_queries.json`, calibration judgments or calibration results
- any v006 retrieval rank, result, report or evaluator output
- all v001–v005 evaluation files
- `cards_fts.plan06_next.sqlite`, `passages.plan06_next.npz`
- all Run, Candidate, experiment, reviewer, history and memory material
- Card FTS, hybrid retrieval, embedding search, rank inspection or query execution
- modification of any source, Card, Evidence, query, database or index

This is independent hidden annotation, not scientific review. On completion, return only judgment count, critical-gap IDs, ordinary-gap count, output SHA-256 and integrity concerns. Do not disclose query text or relevant identities to the main Codex.
