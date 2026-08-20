<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p086-required-parameter-score","ev-p086-near-identical-distribution","ev-p089-forced-alignment-proxy"]
-->
# Candidate Implement: Typed Partial Parameter Alignment

## Method Kernel

Rerank a compact function menu by fusing a frozen query-to-schema cross-encoder score with an explicit partial assignment from observable query values to required tool parameters.

## Evidence And Gap

Related-tool expansion causes wrong-function and parameter failures under fixed requests. [[evidence:ev-p084-expanded-toolkit-controlled-setting]] [[evidence:ev-p084-related-toolkit-error-types]] Meta-Tool already scores required-parameter descriptions, so description matching itself is not new. [[evidence:ev-p086-required-parameter-score]] Its independent maxima permit reuse and ignore actual query values/types; its evaluation distribution is also unusually close across splits. [[evidence:ev-p086-near-identical-distribution]] ToolDreamer shows that forced one-to-one alignment without null can turn noisy latent items into positive pairs. [[evidence:ev-p089-forced-alignment-proxy]]

The narrow gap is deterministic, inference-time, rejectable alignment between value-bearing query spans and a candidate schema's required parameters, measured against the same strong cross-encoder on real menus.

## Computation

1. Build one full-schema text per tool from name, function description, required parameter names/types/descriptions/enums, and optional parameter metadata in a fixed field order.
2. Extract query spans using only frozen deterministic rules for quoted strings, numbers with local units, explicit dates/times, booleans, and capitalized entity-like phrases. Deduplicate by normalized text and retain source offsets.
3. Map each span to a coarse observable type: `number`, `boolean`, `date_time`, or `text`. Map each required parameter to compatible schema types, with date/time specialization from its name and description.
4. Embed span text and required-parameter text with pinned `all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Form edge scores from cosine similarity, a frozen type compatibility term, and exact normalized enum support.
5. Add dummy null nodes and solve maximum-weight partial assignment. A real edge below the frozen null threshold is rejected; the threshold controls acceptance but is not subtracted a second time from accepted edge mass. Each real span and required parameter has capacity one. Normalize accepted edge mass by the number of required parameters and subtract the frozen unmatched-required penalty.
6. Score each query/tool pair once with pinned `cross-encoder/ms-marco-MiniLM-L6-v2@c5ee24cb16019beea0893ab7796b1df96625c6b8`. Z-normalize cross-encoder and TPPA scores within that query's menu, fuse with the Development-selected global weight, and break exact ties by tool-name SHA-256.

## Fair Comparators

- The same cross-encoder and full-schema text without TPPA is primary.
- MiniLM cosine and BM25 use the same query, menus, and schema bytes.
- A relaxed parameter comparator uses the identical spans, edge scores, Development-selected parameter tuple, and fusion weight but independently takes the best real parameter for each span, allowing reuse; this isolates partial capacity/null computation from generic parameter semantics.

No comparator receives gold function names, original-menu membership, generated related requests, or test labels.

## v009 Execution-Only Revision

v008 produced no scientific output because one observed BFCL schema stores required names in `properties.required` and nests the missing `family_history` schema under `symptoms`. v009 strictly expands only this observed embedded-required layout before the unchanged schema text and required-parameter computation. It raises on ambiguous or unresolved embeddings. No scientific rule, score, parameter grid, metric, gate, model, input, or Confirmation boundary changes.

## Implement And Capture Contract

The scientific program is `implementation_v009/evaluate.py`, SHA-256 `d9c03c2b43bf452da2d62c4b3e6ccb05c2ef3a8abbe82be3be6dcd708e9fe9cd`; its config is `implementation_v009/config.json`, SHA-256 `999db63c02c0b57e93f9cc6fe9efc47f11a7ff6e7058defd490cbac0a3323c2d`. It runs only with `D:\Desktop\crl\crl_agent_v3\.venv\python.exe` from cwd `implementation_v009/`.

The local dense snapshot is `all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, 11 files and 91,578,415 bytes; the copied relative-path/size/SHA manifest digest is `4b198bddf01a386c84da55537d837090679fc8d04cb464c3de90b1312cab368b`. The cross-encoder snapshot is `ms-marco-MiniLM-L6-v2@c5ee24cb16019beea0893ab7796b1df96625c6b8`, 6 files and 91,815,758 bytes; its manifest digest is `c1690f252da82d084467a98fb08169c6e16a5b574928c8af72fd86774ee2dd2a`. Every model file, both source files, config, and all three input files must be saved as Experiment Artifacts before execution and listed as capture inputs.

Development argv is fixed to `evaluate.py --phase development --config config.json --expanded inputs/BFCL_v3_multiple_tool_enrichment.json --questions inputs/BFCL_v3_multiple.json --gold inputs/BFCL_v3_multiple_possible_answer.json --output-dir ../experiment_v009/work/dev_eval_001`. The capture is `experiment_v009/captures/dev_eval_001/{execution.json,stdout.bin,stderr.bin}`. Declared scientific outputs are `raw.jsonl`, `selected_params.json`, `query_hashes.json`, `summary.json`, and `environment.json` under that work directory. All five outputs and all three capture files must become Experiment Artifacts.

The frozen grid contains 384 global tuples. Selection orders by Development top-1 membership, MRR, lower fusion weight, lower type bonus, lower unmatched-required penalty, and lower null threshold. The relaxed comparator reuses the selected TPPA tuple. The seed is `20260723`; paired item bootstrap uses 20,000 resamples. Raw output must include every query, schema, gold set, span with offsets/type, edge feature, realized edge score, threshold margin, assignment, method score, complete ranking, and deterministic tie order so the Main Codex can recompute all reported metrics.

## Isolation, Cost, And Attribution

The paired analysis unit is one benchmark row/query. P084 Development consists of 200 fixed requests rather than generated variants of the same request. Confirmation is source-version separated and must also be query-hash disjoint; this does not establish task-, template-, endpoint-, or open-world generalization.

All methods score the same menus once. The cross-encoder cost is identical for the primary baseline and Candidate. MiniLM full-schema encoding serves the dense baseline; TPPA additionally encodes the extracted spans and required-parameter texts and performs small CPU assignments. The relaxed comparator reuses those features. There are no paid APIs, generated tokens, external tools at inference, or per-item retries. Wall time, Python, dependency versions, GPU, CUDA runtime, driver, model manifests, and exact input/config hashes must be captured from the real run.

Attribution is TPPA versus the identical cross-encoder baseline. Comparison with the relaxed matcher isolates capacity/null only; because both TPPA variants still include deterministic extraction, typing, embeddings, fusion, and global Development tuning, no result may be attributed to one of those shared components without the corresponding raw comparison.

## Claim Contract

Development is the pinned 200-item P084 expanded-toolkit dataset with matching BFCL v3 gold. Confirmation is the pinned but unopened BFCL v4 live-multiple dataset and gold. Development-selected rules and hyperparameters are immutable before Confirmation acquisition.

Development requires cross-encoder+TPPA minus cross-encoder top-1 accuracy at least `+0.02`, paired bootstrap 95% lower bound for MRR above `0`, net corrections positive, and a larger TPPA advantage on the parameter-contrast subset. Confirmation requires exact query-hash disjointness, positive top-1 and MRR differences, nonnegative paired-bootstrap lower bound for top-1, and positive net corrections.

For each row, top-1 is correct only when the top-ranked function belongs to the ground-truth function set. A multi-gold row therefore measures top-1 membership, not complete call-set recall. If supported, the Claim is only that TPPA improves this metric over the frozen cross-encoder on these two pinned BFCL compact-menu datasets. It does not establish argument correctness, execution success, stateful Agent competence, or large-corpus retrieval.

Failure freezes v009 and continues the same Run. Success permits only a frozen Review Packet and three independent leaf Reviewers before any Delivery decision.
