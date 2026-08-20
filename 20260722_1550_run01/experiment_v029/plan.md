# Experiment Plan

```json
{
  "experiment_id": "v029",
  "candidate_sha256": "2ea2c1ef080a1edc1b81c94161e8f215931cb4fe4fb3449580baf8ef9814c244",
  "evidence_packet_sha256": "1317d24f9a2e63826b47f330fb0510f6567ab82c3df9fea899399c5c748dea6d"
}
```

## Codex Plan

# v029 Frozen DCN Plan

Status: `FROZEN_BEFORE_MODEL_DIRECTORY_PREPARATION_AND_DEVELOPMENT`.

This publish-once Plan authorizes deterministic preparation of one six-file local model directory, exactly one fixed-formula Development execution, one independent replay and the main Codex Promotion Audit. Only a positive written Promotion Audit may acquire untouched BFCL v4 live-multiple, run one Confirmation and one audit. No gate count, script or file existence may authorize Confirmation, Review, Decision, Delivery or system-state transition. No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity

- Candidate `2ea2c1ef080a1edc1b81c94161e8f215931cb4fe4fb3449580baf8ef9814c244`; Evidence Packet `1317d24f9a2e63826b47f330fb0510f6567ab82c3df9fea899399c5c748dea6d`.
- Selection Context `44e1e9a0b65b9e4001fb1467fa560b300a3fe75a6beac2ca4169baccd57fce23`; Problem `00d875a3c31b4db89daf37d2a46868a0c323d7c96d5d84089aa8fad88a539a9f`; Research Map `4fb035a11b34fa75a6a54a86c61db3be581e078cd7d756e2c69df975d0c97b5f`; nearest prior `d10843ed0d9b7b52687165201d218417edaeaaf525d6bcb7acdb71f0c85aea8c`.
- Program `2a77cfc2cd4f3b5f0d65ba6a9a4c08541dd7318edafabd39b72c92abdcfe74d5`; auditor `be43956b4099bbc8d37b6a775e40ee3f8419566e4dfbc91077c0715dca1f7308`; config `48fc9344c937edf5007f2aabb71619bfcf070eba3274a19bbf5c19d1ab5e4431`; acquisition `11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c`; tests `1425f3e239f12cefb6dd899b5afeff12389d3bc03888cfa79c8b596a278d8d89`; runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`; Implementation Audit `29b45c61e9e091b3ccd79ce2b5c1d7f8399fbe48cc19625844ce85d006a30052`.
- Development questions `aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a`; expanded menus `1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b`; gold `244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047`.
- Cross-encoder six-file hashes: config `380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc`; weights `821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae`; special tokens `3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6`; tokenizer `d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66`; tokenizer config `a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8`; vocabulary `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3`.
- Recent prior PDFs: ToolPRM `f781b56a766748c261ab4c6c6804a6f3f85f7795c6894eaac9408e9dcecd0d55`; JTPRO `f564463c7e64bb2980f1d2b38bf5bedb25b31b8cf5bba7d6ae36818f90e9ad6b`; MagicSelector `bce125f5d225d72bba71bbe9a5ace065bb79815c7980359be0422e3e0b538527`.

All 32 preexecution artifacts totaling 98,871,942 bytes are immutable API copies under `experiment_v029/artifacts/`. Structural preflight parsed 200 queries, 1,121 tools and 4,484 planned query/view pairs without loading the model or computing a v029 score.

## Fixed computation and controls

For each query/tool, the pinned cross-encoder scores `full`, `without_operation`, `without_arguments`, and `name_only` deterministic texts. Define:

```text
operation_drop = full - without_operation
argument_drop = full - without_arguments
dual_necessity = full + min(operation_drop, argument_drop)
```

Frozen controls are `full_schema`, `operation_schema=without_arguments`, `argument_schema=without_operation`, `additive_support=full+0.5*(both drops)`, and `max_support=full+max(both drops)`. Tool ties use tool-name SHA-256. Query fold `SHA256(query_id)[1] mod 5` is an evaluation slice only. There is no fitting, normalization, generated text, task decomposition, TPPA span, assignment, hierarchy or adaptive threshold.

The Claim is limited to top-1 gold-name membership and first-gold MRR on two pinned compact BFCL related-tool menu datasets. It excludes argument correctness, complete call-set recall, execution, Agent success, large-registry, open-world, causal and first-ever claims.

## Exact preparation

After Plan publication, verify `experiment_v029/captures`, `model_cross`, `dev_output_001`, and `dev_audit_output_001` are absent. Create only empty `captures` and `model_cross` using Windows PowerShell 5.1 `New-Item -Path`.

Copy the six frozen `artifacts/model_cross__*` files to canonical model names and verify exactly six files totaling 91,815,758 bytes with the hashes above. This is byte preparation, not model acquisition or experiment.

## One Development execution

Invoke the frozen runner exactly once with cwd `experiment_v029/artifacts`, capture `captures/dev_001`, declared inputs program/config/Candidate/Evidence, all three Development files and all six prepared model files. Declare four outputs: `raw.jsonl`, `query_hashes.json`, `summary.json`, `environment.json`.

Exact payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v029\artifacts\program.py --phase development --config D:\Desktop\crl\20260722_1550_run01\experiment_v029\artifacts\config.json --candidate D:\Desktop\crl\20260722_1550_run01\experiment_v029\artifacts\candidate_v029.md --evidence-packet D:\Desktop\crl\20260722_1550_run01\experiment_v029\artifacts\evidence_packet_v029.md --expanded D:\Desktop\crl\20260722_1550_run01\experiment_v029\artifacts\development_expanded.jsonl --questions D:\Desktop\crl\20260722_1550_run01\experiment_v029\artifacts\development_questions.jsonl --gold D:\Desktop\crl\20260722_1550_run01\experiment_v029\artifacts\development_gold.jsonl --model-dir D:\Desktop\crl\20260722_1550_run01\experiment_v029\model_cross --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v029\dev_output_001
```

Fixed cost is 4,484 local GPU cross-encoder pairs and 20,000 query-row bootstrap samples. No LLM generation, fitting, paid API or retry is allowed. Preserve all bytes regardless of exit. On exit `0`, API-freeze all four outputs and three capture files before audit.

## One independent Development replay

Invoke `audit.py` exactly once through the runner with capture `captures/dev_audit_001`, all frozen inputs and Development outputs, declaring `dev_audit_output_001/report.json`. It independently rebuilds all texts, reruns 4,484 cross-encoder pairs, and replays 6,726 tool-method scores, all rankings, metrics, bootstrap and gates.

Support requires runner exit `0`, `AUDIT_OK`, exact bindings, repeated view-score error `<=1e-6`, formula/method/metric error `<=1e-12`, and zero identity/ranking errors. Freeze report and capture.

## Development gates and main audit

All gates are conjunctive: Candidate top-1 `>=0.95`; Candidate-minus-full top-1 `>=+0.015`; strict top-1 superiority over all five controls; Candidate-minus-strongest MRR bootstrap lower `>0`; corrections exceed regressions versus full; all five fold MRR deltas nonnegative and at least three positive; complete integrity.

The main Codex must inspect every query/menu/tool/view score/deletion drop/method score/ranking/correction/regression/fold/menu size and nearest distractor. It must judge whether gain comes from the smaller-drop conjunction, not an individual deletion, mean or max. Only a positive written `promotion_audit_v029.md` authorizes Confirmation.

## Conditional untouched Confirmation

Only after a positive Promotion Audit may frozen `acquire_confirmation.py` run exactly once to acquire only `BFCL_v4_live_multiple.json` and its possible-answer file at `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`, plus the manifest. Freeze all bytes before reading.

Then run `program.py --phase confirmation` exactly once with the acquired question file as expanded/questions, acquired gold and manifest, six model files, and the frozen Development `summary.json`. No fitting, control reselection or rule change is allowed. Freeze outputs/capture, run one independent audit, freeze it, and perform the main raw audit.

Confirmation gates: Candidate top-1 and MRR strictly above the frozen strongest control; paired top-1 bootstrap lower `>=0`; corrections exceed regressions; strict top-1 superiority over every control; exact normalized-query-hash disjointness; complete integrity.

Only positive main Confirmation Audit permits a formal Review Packet. Only after complete Packet freeze may exactly three simultaneous fresh `default`, `fork_turns=none`, direct leaf Reviewers start, each exact request containing `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Failure handling

Any nonzero scientific/capture execution, missing declared output, audit mismatch, failed gate or negative main audit freezes v029 and advances the same Run. No same-version retry, deletion-view/formula/control/gate/Claim retuning, reduced controls, post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is allowed. Run remains `ACTIVE`; system remains `DEVELOPMENT_NOT_COMMISSIONED`.

