# Experiment Plan

```json
{
  "experiment_id": "v016",
  "candidate_sha256": "31df88dfa09b6b5b214236f0a364bbaf7f3a417b96af1ce0aee5c9219f0de845",
  "evidence_packet_sha256": "1bc9f9d937f7cafb1e63b449e255b1032baf5a18a59fec818da19561a3204526"
}
```

## Codex Plan

# v016 One-Shot Untouched Confirmation Plan

## Authority

This is the prospective publish-once Plan for the original untouched Confirmation of Required-Grounding Precedence. v016 changes only one incorrect character in v015's frozen manifest SHA binding. It does not change the research candidate, program bytes, data, partition, metrics, or gates.

Exactly one evaluator capture is authorized. Exactly one independent raw-row audit is authorized only if the evaluator exits `0` and produces all three outputs. Same-version retry is forbidden. This Plan does not authorize Review, decision, Delivery, or system-state change.

## Candidate and Evidence

- Candidate SHA-256: `31df88dfa09b6b5b214236f0a364bbaf7f3a417b96af1ce0aee5c9219f0de845`.
- Evidence Packet SHA-256: `1bc9f9d937f7cafb1e63b449e255b1032baf5a18a59fec818da19561a3204526`.
- Candidate is current; Evidence Packet is bound to it; both formal Evidence entries are current.
- System: `DEVELOPMENT_NOT_COMMISSIONED`.
- Run: `ACTIVE`.
- Reviewers started: false.

## Inherited Development evidence

v014 Development remains frozen and is not rerun. It passed all ten gates on 10,000 rows: official accuracy `0.9295880149812734`, RGP accuracy `0.9462814339218834`, delta `+0.016693418940609953`, model-cluster bootstrap 95% `[+0.010464272171620851,+0.02313872522763792]`, 157 corrections, one regression, positive effect on 9/10 models and 5/5 domains, and 157 supported mechanism transitions across all five domains. Independent audit exit was `0`, `audit_ok=true`, maximum metric error `0`.

The v014 Plan, Result, all inputs, raw rows, summaries, samples, captures, independent report, Promotion Audit, environment capture, code, and source bytes are inherited through the frozen v015 Artifact set.

## v015 failure and untouched status

The one authorized v015 command exited `1` at `program.py:216` before scientific input parsing. Its config expected manifest SHA:

```text
f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeb49a8011944
```

The actual frozen manifest SHA was:

```text
f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944
```

No trace or judge JSON was opened by the scientific program; no raw rows, summary, cases, metric, prediction, correction, or regression was created. Independent audit was not run. v015 Result SHA-256 is `3e1ded11173fe49c1414afa002a14d47932b4a9a0f2c3cb3d4ba9e665ab2622c`.

Therefore the main Codex has no Confirmation outcome information. It has read only manifest metadata/hashes, runner metadata, and the manifest-mismatch traceback.

## Exact correction audit

The v016 evaluator, independent auditor, and tests are byte-for-byte identical to v015:

| Artifact | SHA-256 |
|---|---|
| `program.py` | `9551f79cc075f45f1b59be11bfca25e79e60d9d49372f5d36d2cc2ede40d99c2` |
| `independent_audit.py` | `289965efc11d5882fe0b2f43db84960c6c1d22dda9a52b4c29474832f8b236cc` |
| `test_audit.py` | `db5d7e93c95cb13e0a0a4ced9ca1af92a864bcb26bc398ac2da81f56db02edd6` |

All scientific-function ASTs remain identical to v014. Seven unit tests exited `0`.

The v015-to-v016 config diff contains only candidate version, corrected manifest SHA, current Candidate SHA, and current Evidence Packet SHA. Current config:

- SHA-256 `0c5cc494445d7eae922dabcbff0d2f9f45da34a46a17ee712955a468ef81d3b5`;
- expected manifest SHA `f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944`;
- actual manifest SHA `f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944`;
- direct comparison `MATCH=True`.

Implementation Audit SHA-256: `a09fb5ac2acec1c62fea673a2a2bff81572ea51d72de49ac98cad1ca2619627d`.

## Frozen inputs and artifacts

- dataset `SoHarshh/toolfailbench-traces`;
- revision `77ef18dadfc1ad96ce29c863f0913d990659432a`;
- manifest SHA-256 `f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944`;
- 36 files and 342,075,457 bytes;
- 12 trace files, 24 judge files, zero ensembles;
- zero path overlap with Development;
- official detector SHA-256 `aee4d77596bdacb9025d85cccde766ff2a2ddbe1a291b6c143ea46d22863dbd0`.

Each input is frozen under the same `input__<flattened manifest path>` name used by v015 and has the same SHA-256. The Artifact API rehashed every byte.

The final pre-Plan index has SHA-256 `05c27cc0731164fd739ae2ff063cfbe43d46ba55b4d7c82fbf8853ecca1058e3`; it binds 164 Artifacts and 646,652,883 bytes before itself. Including the index, 165 pre-execution Artifacts and 646,684,957 bytes are frozen and current. They include complete v014 Development evidence and complete v015 failure evidence.

## Environment

No package or environment change occurred between v015 and v016. The inherited current-environment capture used the shared interpreter and exited `0`:

- Python `3.11.15`;
- NumPy `2.3.5`, SciPy `1.16.0`;
- PyTorch `2.12.0+cu130`, CUDA runtime `13.0`;
- NVIDIA GeForce RTX 5060 Ti, capability `12.0`;
- real CUDA kernel sum `22898102272.0`;
- execution SHA-256 `8c16b67600c372e87d3f5b13a3ff2280ce68cbca7fd5bc6439ab2035bb5a3235`;
- stdout SHA-256 `3331de8d0722cc4064a6e95d3dfd1eb29e61bb84713f0a553e01052c5599ba8e`;
- empty stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Exact command contract

`experiment_v016/artifacts/confirmation_argv.json`, SHA-256 `72d9066fc59a1d8d31bad97b3d42d7533d6f4fba9a2c17dd5e5fd62dcf384987`, contains the complete machine-readable argv.

The evaluator argv has 111 items and declares 40 inputs to `run_local_experiment.py`: frozen program, manifest, official detector, config, and all 36 manifest inputs. The runner requires all three outputs absent and hashes every input before execution.

Primary capture:

- capture: `experiment_v016/captures/confirmation_eval_001`;
- cwd: `experiment_v016/work/confirmation_eval_001`;
- outputs: `raw_rows.jsonl`, `summary.json`, `case_samples.json`;
- child command: shared Python `-B` with frozen `program.py` and the frozen manifest/data-root/official/config/output paths.

Independent capture, only after evaluator exit `0` and all outputs exist:

- capture: `experiment_v016/captures/confirmation_audit_001`;
- cwd: `experiment_v016/work/confirmation_audit_001`;
- inputs: frozen independent auditor, frozen config, primary raw rows, and primary summary;
- output: `report.json`.

No retry, output repair, threshold change, input substitution, model/domain deletion, judge change, or normalization is permitted.

## Metrics and conjunctive gates

Primary reference: only rows where both released independent judges agree. The official rule and RGP consume identical rows. The majority ensemble remains excluded.

1. all 36 manifest bytes verify; exactly 12 traces, 24 judges, zero ensembles;
2. exactly 12,000 unique joins across 12 models and five domains with no join error;
3. exact official reproduction on every classifier-supported released label and no unexpected external label;
4. no RGP change to CTRL, external-error, expected-tool-not-called, or required-contract-failed rows;
5. paired accuracy delta at least `+0.005`;
6. 20,000-resample model-cluster bootstrap with seed `20260723` has 95% lower bound `> 0`;
7. corrections strictly exceed regressions;
8. positive delta on at least `9/12` models;
9. positive delta in at least `4/5` domains;
10. at least 100 supported `official output_fabrication -> RGP correct -> unanimous correct` transitions across at least four domains.

Macro-F1, all transitions, disagreements, external passthroughs, per-model/domain metrics, corrections, regressions, and bounded raw case samples remain reportable. Mechanical booleans do not authorize Review.

## Main-Codex audit and Review boundary

After both captures, the main Codex must verify full execution provenance and hashes, read the entire summary and independent report, verify all integrity and metric agreements, and inspect original frozen bytes for a bounded cross-domain correction set and every regression. This cannot reopen selection or add experiments.

Only a passing main-Codex judgment permits freezing a complete `review_v016/packet.md`. Until then, no subagent is permitted.
