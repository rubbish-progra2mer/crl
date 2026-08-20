# Research Problem v030

## Problem

Function-calling benchmarks couple user text, tool schemas and reference calls. A file can remain valid JSON while these layers disagree: a reference parameter may not exist in the schema, a path written in one call may differ from the path consumed by the next, a query unit may contradict the tool contract, or a stated weekday may contradict its date.

Existing validation frequently checks one layer at a time. A broad LLM or multi-agent audit can detect more cases, but its generated judgments make it difficult to separate localization quality from the auditor's own labels. The BFCL repository contains merged data repairs with preserved pre-fix bytes and maintainer-accepted changed entries. This permits a narrower empirical question:

> Can a deterministic, typed cross-layer contract audit rank entries that were later patched, using only their pre-fix bytes, better than standalone schema, surface-literal, date/unit and size baselines?

## Observable

For each fixed repair PR:

1. build the candidate pool from every entry in the modified pre-fix data file;
2. label only the entry IDs changed by the merged patch;
3. compute every score from pre-fix query/schema/reference bytes;
4. rank entries without reading the repaired value;
5. measure reciprocal rank, Recall@10 and pooled average precision.

The endpoint is patch localization, not proof that every patch is semantically correct and not automatic benchmark repair.

## Scope

- Development: merged BFCL PRs `865, 870, 871, 872, 876, 892, 962, 963`.
- Confirmation, conditional and currently unacquired: `1084, 1085, 1086, 1087, 1175, 1177`.
- No LLM, generated label, subagent, paid API, training, threshold fitting or post-fix feature is used.
- GitHub merge status and changed IDs are labels; patch content is retained only for provenance and independent audit.
- The method is not claimed to detect grammar edits, all ambiguous intents, implementation bugs or all benchmark defects.
