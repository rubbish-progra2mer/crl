# Research Map

## Frozen primary evidence

| Evidence | SHA-256 | Direct implication |
| --- | --- | --- |
| `sources_v018/saag_2607.18245.pdf` | `31C3AE9F0FD08AF039FD5D3063EDFF41A4DD8ADFE1FD867E676975AEA773091B` | Registry/structure/argument-grounding diagnostics and structured repair already exist. |
| `sources_v018/lost_in_execution_acl2026.pdf` | `39D43C3A949C7F710F23754D2D4751281A8FF2248E96EC58A5D9CBAC92CAB93A` | MLCL isolates parameter-language mismatch and already compares prompt, pre-translation, and post-translation mitigation. |
| `sources_v018/cope_acl2026.pdf` | `0D21A03DED6AE892D0818EC8E0F453B3CA0FC1C4CB3E30AE2C3B182C40868207` | CoPE includes constrained Editing and Revision, not only full regeneration. |
| `sources_v018/nl_pddl_bench_2606.29700.pdf` | `E59B44CE28468ADCAB3DC5683D91DBECB933E486CDEA24A501BEFD57B609771A` | Planner-in-the-loop localized repair is a direct recent comparator. |
| `sources_v018/contract2tool_2606.07904.pdf` | `E01ADA84E6246DC897918AA5D13320CCA06174CBB2C2D0DD6A7012290E78B201` | Missing preconditions/effects are already inferred from documentation and traces. |
| `sources_v018/partial_contracts_2607.10291.pdf` | `A4C1C5B1B239E79C35EB9F71FF5B2AF091179FF36F79552C0A6F8740B973CD89` | A sound partial-contract system returns unprovable rather than fabricating equivalence. |

The formal knowledge-base ToolGate source remains `knowledge_base/papers/P074_toolgate.pdf`, SHA-256 `7073BC0A27CF0F002EA4D1EF0EC3726D5C70C7E44A218E78F46D92284ABA289D`.

## Mechanical readback

A read-only PyMuPDF traversal exited 0 over the six v018 PDFs: 96 pages and 371,704 extracted characters. Phrase readback located the material computations, including `argument grounding`, `structured feedback`, `Post-Translation`, `Editing`, `Revision`, `localized edits`, `planner-in-the-loop`, `execution traces`, `unprovable difference`, and `sound`.

The CoPE repository was cloned from the official GitHub repository at commit `e13535ebbc581c8a7ad824ee741701cc33669695`. It contains 4,321 tracked working-tree files in total, including 4,292 data files, but no `output/` directory. Its README requires external components absent from the shared environment; the module probe returned `z3=False`, `kani=False`, and `pddl=False` while `transformers=True` and `torch=True`.

## Candidate Promotion Audit

No Candidate is promoted. The generic grounding and partial-contract routes collide with direct prior; the multilingual route lacks accessible released data; and the planning route lacks frozen model outputs and requires an out-of-scope experimental platform.

## Next-version constraint

v019 must select a computation with an immediately auditable real-data and execution path under the existing Python/GPU environment. It must not return to generic argument provenance, translation-only normalization, CoPE incremental editing, `Q=True` triage, or memory-poisoning text anomaly detection.

