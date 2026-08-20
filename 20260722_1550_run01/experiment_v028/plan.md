# Experiment Plan

```json
{
  "experiment_id": "v028",
  "candidate_sha256": "249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3",
  "evidence_packet_sha256": "ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972"
}
```

## Codex Plan

# v028 Frozen MFCR Execution-Only Plan

Status: `FROZEN_BEFORE_CORRECTED_MODEL_DIRECTORY_PREPARATION_AND_DEVELOPMENT`.

v028 is an execution-only continuation of v027. v027 exited `1` during post-Plan directory preparation because Windows PowerShell 5.1 rejected `New-Item -LiteralPath`; no directory, model copy, Development computation or Confirmation byte was produced. v028 changes only that preparation operation to `New-Item -Path` and advances emitted experiment identity strings. All scientific bytes and choices remain frozen.

No script, gate count or file existence may authorize Confirmation, Review, Decision, Delivery or system-state transition. No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity

- Candidate `249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3`; Evidence Packet `ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972`.
- Problem `9951f4cb537e79ebb56925f1bbd093c07ca911e2f5a621a98f360c2e611ea81e`; Research Map `e1cb8a5cf8f540fd7251d0a3d0053d8ae17c67c81b23c98b17c849615019e10d`.
- Program `9a13e18bfffab4d44b5d185c003a8c8fbe7639de2ddb8fb6a6d5cf985351d9fb`; auditor `37d93688c96618d2423a77fc3377e21023a023f9a8ac71dd510092a018530674`; config `8c64c396dd095a689cc7da63036d92b6b9fcde02c7cc6b8016616e174d28a656`; acquisition `11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c`; tests `b5e6c8733588346043d0f9b991ca9b575951d232002f09fdf0530a794b5c4429`; runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.
- Development questions `aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a`; expanded menus `1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b`; gold `244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047`.
- Frozen model files: config `380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc`; weights `821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae`; special tokens `3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6`; tokenizer `d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66`; tokenizer config `a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8`; vocabulary `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3`. Total 91,815,758 bytes.
- All 37 preexecution artifacts totaling 97,333,976 bytes are immutable API copies under `experiment_v028/artifacts/`.

The structural preflight already parsed 200 queries, 1,121 tools and 3,363 field pairs without model inference. The v027 failure record proves no scientific execution occurred.

## Fixed computation and controls

The same cross-encoder scores deterministic `full`, `operation` and recursive `arguments` views. Query fold is `SHA256(query_id)[1] mod 5`. Training-only standardization and L2 liblinear C=1 use seed `12027`. MFCR fits a zero-intercept ranker on both orientations of every gold/non-gold within-menu difference with total pair weight one per query.

Frozen controls are `full_cross_encoder`, `equal_fields`, `pointwise_fields` and `pairwise_full`. The strongest comparator is chosen by Development OOF top-1, then MRR, then lexicographically greatest name. Tool ties use tool-name SHA-256. There is no generated text, TPPA span, assignment, hierarchy, per-query threshold or adaptive rule.

The Claim is limited to top-1 gold-name membership and first-gold MRR on the two pinned compact BFCL menu datasets. It excludes argument correctness, complete multi-call recall, execution, Agent success, large-registry retrieval, open-world and first-ever claims.

## Exact corrected preparation

After Plan publication, verify `experiment_v028/captures`, `experiment_v028/model_cross`, `dev_output_001`, and `dev_audit_output_001` are absent. Create only the first two empty directories with Windows PowerShell 5.1 `New-Item -ItemType Directory -Path`.

Copy the six frozen `artifacts/model_cross__*` files into `model_cross/` under canonical names `config.json`, `model.safetensors`, `special_tokens_map.json`, `tokenizer.json`, `tokenizer_config.json`, `vocab.txt`. Verify exactly six regular files and the frozen hashes. This is byte preparation, not model acquisition or experiment.

## One Development execution

Invoke the frozen runner exactly once, with cwd `experiment_v028/artifacts`, capture `captures/dev_001`, declared inputs program/config/Candidate/Evidence, all three Development files, and all six prepared model files. Declare these outputs under `dev_output_001`: `model.joblib`, `raw.jsonl`, `query_hashes.json`, `summary.json`, `environment.json`.

Exact payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v028\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v028\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v028\artifacts\candidate_v028.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v028\artifacts\evidence_packet_v028.md --expanded D:\Desktop\crl\20260722_1550_run01\experiment_v028\artifacts\development_expanded.jsonl --questions D:\Desktop\crl\20260722_1550_run01\experiment_v028\artifacts\development_questions.jsonl --gold D:\Desktop\crl\20260722_1550_run01\experiment_v028\artifacts\development_gold.jsonl --model-dir D:\Desktop\crl\20260722_1550_run01\experiment_v028\model_cross --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v028\dev_output_001
```

Fixed cost is 3,363 local GPU pairs, five OOF bundles, one full bundle and 20,000 query-row bootstrap samples. There is no LLM generation, paid API or retry. Preserve all bytes regardless of exit. On exit `0`, API-freeze all five outputs and the three capture files before audit.

## One independent Development replay

Invoke `audit.py` exactly once through the runner with `captures/dev_audit_001`, all frozen inputs and Development outputs, declaring `dev_audit_output_001/report.json`. It independently reconstructs all 3,363 cross-encoder pairs and replays all five method scores/rankings without fitting.

Support requires runner exit `0`, report `AUDIT_OK`, exact bindings, repeated field-score error `<=1e-6`, frozen linear-score error `<=1e-9`, metric/gate error `<=1e-12`, and zero identity/ranking errors. Freeze report and capture.

## Development gates and main audit

All gates are conjunctive: Candidate top-1 `>=0.95`; Candidate-minus-full top-1 `>=+0.015`; strict top-1 superiority over all four controls; Candidate-minus-strongest MRR bootstrap lower `>0`; corrections exceed regressions; all five fold MRR deltas are nonnegative with at least three positive; complete integrity.

The main Codex must inspect every query/menu/tool/field score, ranking, correction/regression, fold, menu size and nearest distractor, and distinguish the claimed pairwise field contrast from field segmentation, pointwise supervision and generic pairwise calibration. Only a positive written `promotion_audit_v028.md` authorizes Confirmation.

## Conditional untouched Confirmation

Only after a positive Promotion Audit may frozen `acquire_confirmation.py` run exactly once. It must acquire only `BFCL_v4_live_multiple.json` and `possible_answer/BFCL_v4_live_multiple.json` from `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`, plus its manifest. Freeze all three outputs and capture before reading or scoring.

Then run `program.py --phase confirmation` exactly once using the frozen Development model, six model files and acquired bytes. No fitting, comparator reselection or rule change is allowed. Freeze outputs/capture, run one independent audit, freeze it and perform the main raw audit.

Confirmation gates: Candidate top-1 and MRR strictly above the frozen strongest comparator; paired top-1 bootstrap lower `>=0`; corrections exceed regressions; Candidate top-1 strictly above every control; exact normalized-query hash disjointness; complete integrity.

Only a positive main Confirmation Audit permits freezing a formal Review Packet. Only after the Packet is fully frozen may exactly three simultaneous fresh `default`, `fork_turns=none`, direct leaf Reviewers start; each exact request must contain `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Failure handling

Any nonzero scientific/capture execution, missing declared output, audit mismatch, failed gate or negative main audit freezes v028 and advances the same Run. No same-version retry, field/weight/fold/gate/Claim retuning, reduced controls, post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is allowed. Run stays `ACTIVE`; system stays `DEVELOPMENT_NOT_COMMISSIONED`.

