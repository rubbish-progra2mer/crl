# Experiment Plan

```json
{
  "experiment_id": "v027",
  "candidate_sha256": "249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3",
  "evidence_packet_sha256": "ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972"
}
```

## Codex Plan

# v027 Frozen MFCR Plan

Status: `FROZEN_BEFORE_MODEL_DIRECTORY_PREPARATION_AND_DEVELOPMENT`.

This publish-once Plan authorizes deterministic preparation of one local model directory from already frozen artifact copies, exactly one 5-fold query-OOF Development execution, one independent cross-encoder/model replay and the main Codex Promotion Audit. Only a positive written Promotion Audit may acquire the two untouched BFCL v4 live-multiple files, run one frozen Confirmation and one audit. No script, gate count or file existence can authorize Confirmation, Review, Decision, Delivery or a system-state transition. No subagent is permitted before a complete Review Packet is frozen.

## Frozen identity

- Candidate `249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3`; Evidence Packet `ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972`.
- Selection Context `f0462c31ef4224aee4e2be64d4291774311024c917e4ce1e82963fcdc314256f`; Problem `9951f4cb537e79ebb56925f1bbd093c07ca911e2f5a621a98f360c2e611ea81e`; Research Map `e1cb8a5cf8f540fd7251d0a3d0053d8ae17c67c81b23c98b17c849615019e10d`; nearest prior `1f96a9551ccd6642e7bbb4602d58fa2f71e9c2c689d529427d6200dc9bee0630`.
- Program `58e2493aaf5a9bd1f7063d28ed7153ebbc7885b53e6c205deda9d21132e91da6`; independent auditor `37d93688c96618d2423a77fc3377e21023a023f9a8ac71dd510092a018530674`; config `cd18ad8b645a2c82d98aa9009596303d10097426da2fa7649e84964500bb30c9`; conditional acquisition `11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c`; tests `b5e6c8733588346043d0f9b991ca9b575951d232002f09fdf0530a794b5c4429`; Implementation Audit `e6f6dbe077b6596a0971c31e4e937d456261fd79e822d8f38c2c6d9996b9797f`; runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.
- Development questions/original menus `aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a`; expanded menus `1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b`; gold `244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047`.
- Frozen cross-encoder has six files and 91,815,758 bytes: config `380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc`; weights `821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae`; special tokens `3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6`; tokenizer `d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66`; tokenizer config `a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8`; vocabulary `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3`.
- Prior PDFs are frozen: P084 `8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7`, P087 `0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff`, P086 `02064499a8345eb333e4fdd71abaa5ee69133af5be7b81626ba09816f48d194b`, ToolRerank `dc1d0cf7537401d602aef27160b5f854b688bf607e51d3c0e33febccc66237d4`, DTDR `099f012ad01bd8b24154093c2bfe55ad9eabdb668ddc7ecf0c2735e01d89a833`.

All 33 preexecution artifacts are immutable API copies under `experiment_v027/artifacts/`. v009 and v026 lineage bytes are included. The structural preflight parsed 200 queries, 1,121 tools and 3,363 field pairs but did not load the model for inference or compute a v027 score.

## Fixed computation and controls

Each query/tool schema is deterministically represented as `full`, `operation`, and `arguments` text and scored by the same frozen cross-encoder. Query fold is `SHA256(query_id)[1] mod 5`. Training-only standardization and L2 liblinear C=1 models use seed 12027. MFCR fits zero-intercept logistic ranking on both orientations of each gold/non-gold within-menu difference, with total pair weight one per query.

Controls are unchanged full-view cross-encoder, equal mean of standardized fields, query-weighted pointwise field classification, and the identical pairwise objective using only full-view score. The strongest control is OOF top-1, then MRR, then lexicographically greatest method name. Tool ties use tool-name SHA-256. No fold, field, serializer, learner, C, weighting, model, comparator, gate or Claim may change.

The maximum Claim is limited to top-1 gold-name membership and first-gold MRR on pinned BFCL v3/v4 compact multiple-tool menus. No parameter correctness, complete multi-call recall, execution, Agent task success, open-world or first-ever claim is allowed.

## Exact preparation

After Plan publication, create empty `experiment_v027/captures` and `experiment_v027/model_cross` directories. Copy only the six frozen `artifacts/model_cross__*` files into `model_cross/` with canonical names `config.json`, `model.safetensors`, `special_tokens_map.json`, `tokenizer.json`, `tokenizer_config.json`, and `vocab.txt`. Verify the destination contains exactly those six regular files with the hashes above. This is byte preparation, not a model download or experiment.

Verify `captures/dev_001`, `dev_output_001`, `captures/dev_audit_001` and `dev_audit_output_001` are absent.

## One Development execution

Run the frozen capture runner once with cwd `experiment_v027/artifacts`, capture `captures/dev_001`, declared inputs consisting of program/config/Candidate/Evidence, all three Development files and all six prepared model files, and declared outputs under `dev_output_001`: `model.joblib`, `raw.jsonl`, `query_hashes.json`, `summary.json`, `environment.json`. The exact payload is:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v027\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v027\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v027\artifacts\candidate_v027.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v027\artifacts\evidence_packet_v027.md --expanded D:\Desktop\crl\20260722_1550_run01\experiment_v027\artifacts\development_expanded.jsonl --questions D:\Desktop\crl\20260722_1550_run01\experiment_v027\artifacts\development_questions.jsonl --gold D:\Desktop\crl\20260722_1550_run01\experiment_v027\artifacts\development_gold.jsonl --model-dir D:\Desktop\crl\20260722_1550_run01\experiment_v027\model_cross --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v027\dev_output_001
```

Fixed cost is 3,363 local GPU cross-encoder pair scores, five OOF scaler/model bundles, one full bundle and 20,000 query-row bootstrap samples. There is no LLM generation, paid API or per-query retry. Preserve all bytes regardless of exit. On exit 0, API-freeze all five outputs and three capture files before audit.

## One independent Development replay

Run `audit.py` once through the same runner with capture `captures/dev_audit_001`, frozen program inputs, frozen Development outputs and report `dev_audit_output_001/report.json`. It must independently reconstruct and rerun all 3,363 cross-encoder pairs, then replay all five method scores for 1,121 tools without fitting. Support requires exit 0, `AUDIT_OK`, exact bindings, maximum repeated field-score error `<=1e-6`, frozen linear-score error `<=1e-9`, metric/gate error `<=1e-12`, and zero identity/ranking errors. Freeze report and capture.

## Development gates and main audit

All gates are conjunctive: Candidate top-1 `>=0.95`; Candidate-minus-full top-1 `>=+0.015`; strict top-1 superiority over all four controls; Candidate-minus-strongest MRR bootstrap lower `>0`; more full-baseline corrections than regressions; all five fold MRR deltas nonnegative and at least three positive; complete integrity.

The main Codex must inspect every query/menu/tool/field score, ranking, correction/regression, fold, menu size and nearest distractor, and determine whether any gain belongs to pairwise field contrasts rather than field segmentation, pointwise supervision or pairwise calibration. Only a positive written `promotion_audit_v027.md` may authorize Confirmation.

## Conditional untouched Confirmation

Only after a positive Promotion Audit, invoke frozen `acquire_confirmation.py` once through the runner with current config and output `confirmation_acquire_output_001`. It must download exactly `BFCL_v4_live_multiple.json` and `possible_answer/BFCL_v4_live_multiple.json` from `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`, plus one manifest. Freeze all three outputs and capture before reading/scoring.

Then run `program.py --phase confirmation` exactly once with the acquired question file passed as both `--expanded` and `--questions`, acquired gold, acquired manifest, the six frozen model files, and frozen Development `model.joblib`. No fitting or comparator reselection is allowed. Freeze raw/query-hash/summary/environment and capture, then run one frozen independent audit and freeze it.

Confirmation gates are Candidate top-1 and MRR strictly above the frozen strongest comparator; paired top-1 bootstrap lower `>=0`; more corrections than regressions; strict top-1 superiority over every control; exact normalized-query-hash disjointness; complete integrity. The main Codex must repeat raw audit. Only a positive main Confirmation Audit permits a formal Review Packet.

After the Packet is fully frozen—and not before—exactly three simultaneous fresh `default`, `fork_turns=none`, direct leaf Reviewers may start, each request containing `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Failure handling

Any nonzero execution, missing output, audit mismatch, failed gate or negative main audit freezes v027 and advances this same Run. No same-version retry, field/weight/fold/gate/Claim retuning, reduced controls, post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is allowed. Run remains `ACTIVE`; system remains `DEVELOPMENT_NOT_COMMISSIONED`.
