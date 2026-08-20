# Experiment Plan

```json
{
  "experiment_id": "v015",
  "candidate_sha256": "97f3e2bd1cf9363c538b3b35f703313838e20d5c6ebe17850613d87fbdd1bae3",
  "evidence_packet_sha256": "36f81572fa604082c2b92195000615581e2e7dc9c4be0bd7589678bebfc4adac"
}
```

## Codex Plan

# v015 One-Shot Untouched Confirmation Plan

## Authority and purpose

This is the prospective, publish-once Confirmation Plan for v015 Required-Grounding Precedence. v015 is an execution-only continuation of v014: it repairs the Development-specific input cardinality contract without changing the scientific computation.

The main Codex authorizes exactly one Confirmation evaluator capture and, only if its row outputs exist, exactly one independent raw-row audit capture. This Plan does not authorize Reviewer creation, a Review Packet, a decision, Delivery, or a system-state change.

## Candidate and Evidence binding

- Candidate SHA-256: `97f3e2bd1cf9363c538b3b35f703313838e20d5c6ebe17850613d87fbdd1bae3`.
- Evidence Packet SHA-256: `36f81572fa604082c2b92195000615581e2e7dc9c4be0bd7589678bebfc4adac`.
- Evidence Packet is bound to the current Candidate and contains two current formal Evidence entries.
- System state: `DEVELOPMENT_NOT_COMMISSIONED`.
- Run state: `ACTIVE`.
- Reviewers started: false.

## Inherited Development evidence

v014 Development is not rerun. Its frozen Plan, Result, all non-Confirmation Artifacts, raw 10,000-row output, summaries, case samples, capture bytes, independent audit, Promotion Audit, environment capture, and all 40 Development inputs are copied and rehashed under `experiment_v015/artifacts/development__*`.

Binding highlights:

- v014 Plan SHA-256 `d8310e4d1b0265b10a77b235e71e88bc4f4edb435cde1141cd3e84a1d081266d`;
- v014 Result SHA-256 `03c3993e877aead6bcabfa0fab1866c4ab0561d80851d1d8db37549a062323c8`;
- Development raw rows SHA-256 `5c50f38438621c18edbe1b34eb6595798b9d6980b7e96a18c3805a009f5dc8e8`;
- Development summary SHA-256 `4fd042ac7bf194452ac294c7e82534651b701fe60e778dac4fd7223eca60486a`;
- independent report SHA-256 `99ca0a6733b128454b015e0dab7f94bab2f2b89dc3bb26b3878436b76759de4c`;
- Promotion Audit SHA-256 `6cdf49c6da800891bf54a03e5306bb4745ea19c281ae694983fa45de15fc201f`.

Development passed all ten gates: accuracy delta `+0.016693418940609953`, model-cluster bootstrap 95% `[+0.010464272171620851,+0.02313872522763792]`, 157 corrections, one regression, positive effect on 9/10 models and 5/5 domains, and 157 supported mechanism transitions across all five domains. The single regression remains part of the claim limitation.

## Confirmation exposure statement

The fixed 36 Confirmation files were acquired only after the positive v014 Promotion Audit. Before this Plan, the main Codex and v015 programs used only manifest paths, byte counts, SHA-256 values, total cardinalities, and Development-overlap checks. No Confirmation trace or judge JSON was opened, parsed, sampled, searched, summarized, or used to select a threshold or implementation branch.

The source files were byte-rehashed once after acquisition and again by the Artifact API. Neither operation interpreted content.

## Frozen input and implementation bindings

| Artifact | SHA-256 |
|---|---|
| `program.py` | `9551f79cc075f45f1b59be11bfca25e79e60d9d49372f5d36d2cc2ede40d99c2` |
| `independent_audit.py` | `289965efc11d5882fe0b2f43db84960c6c1d22dda9a52b4c29474832f8b236cc` |
| `config.json` | `f5655f9edc6b85fee9b09592c6eded4bc38f93c8d948d2e40d8ac6278509ef1d` |
| `test_audit.py` | `db5d7e93c95cb13e0a0a4ced9ca1af92a864bcb26bc398ac2da81f56db02edd6` |
| `implementation_audit.md` | `9d754a6adb9cf3d2e3fc13c5276255a31064dd87613d928e1e51620ce3c2eb6a` |
| `manifest.json` | `f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944` |
| `partition.json` | `75fe902b57aa3e9a363c4efcbca7bbf0164678412089f023b385aa365acdddfe` |
| `official_detect.py` | `aee4d77596bdacb9025d85cccde766ff2a2ddbe1a291b6c143ea46d22863dbd0` |
| `confirmation_argv.json` | `20823b0828f30fe2fe0860f6efbe7d1a37457f1068d3fd54c69fbaa0058026ec` |
| `preplan_artifact_index.json` | `147d243ed77c176b5c19357fc055cc91889ef92bccbd7fc9bde018b1e5080115` |
| `capture_runner.py` | `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` |

The pre-Plan index binds 142 Artifacts and 646,461,296 bytes before the index itself. The index itself is the 143rd Artifact. All are current and immutable by artifact name.

The Confirmation manifest binds revision `77ef18dadfc1ad96ce29c863f0913d990659432a`, 36 files, 342,075,457 bytes, 12 trace files, 24 judge files, zero ensemble files, and zero path overlap with Development. Each manifest path maps to `input__` plus the POSIX path with `/` replaced by `__`.

## Scientific-code identity

The main-Codex implementation audit compared complete AST dumps without source locations. RGP classification, macro-F1, grouped accuracy, percentile, model-cluster bootstrap, per-group metrics, transition counts, and the independent recomputations are identical to v014. Aggregate result: `ALL_SCIENTIFIC_AST_IDENTICAL=true`; audit command exit `0`.

Allowed v015 changes are limited to phase-neutral manifest identity, frozen artifact prefix, expected cardinalities, the already preregistered Confirmation gates, and phase-neutral output fields.

## Environment

The shared interpreter and GPU were recaptured before this Plan through `run_local_experiment.py`:

- execution SHA-256 `8c16b67600c372e87d3f5b13a3ff2280ce68cbca7fd5bc6439ab2035bb5a3235`;
- stdout SHA-256 `3331de8d0722cc4064a6e95d3dfd1eb29e61bb84713f0a553e01052c5599ba8e`;
- stderr is empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- exit `0`, duration `3.500800800000434` seconds;
- Python `3.11.15`, NumPy `2.3.5`, SciPy `1.16.0`, PyTorch `2.12.0+cu130`, CUDA runtime `13.0`;
- NVIDIA GeForce RTX 5060 Ti, capability `12.0`;
- a real CUDA kernel over 4,096 values returned sum `22898102272.0`.

The first environment-runner invocation failed before capture creation because the `captures/` parent directory did not yet exist. Exit was `1`; no command under test ran and no capture or scientific output was created. After creating only that parent directory, the identical environment command produced the successful capture above.

## Exact execution contract

`experiment_v015/artifacts/confirmation_argv.json` is the complete machine-readable argv contract. Its Confirmation evaluator array has 111 argv items and enumerates all 40 input files: the frozen evaluator, manifest, official detector, config, and exactly 36 manifest-bound input Artifacts. Its independent-audit array has 29 argv items.

Primary capture:

- capture directory: `experiment_v015/captures/confirmation_eval_001`;
- cwd: `experiment_v015/work/confirmation_eval_001`;
- program: shared Python with `-B`, frozen `program.py`;
- outputs: `raw_rows.jsonl`, `summary.json`, and `case_samples.json` in the primary cwd;
- runner hashes every listed input before execution and requires every output to be absent.

The evaluator receives exactly:

```text
--manifest experiment_v015/artifacts/manifest.json
--data-root experiment_v015/artifacts
--official-detect experiment_v015/artifacts/official_detect.py
--config experiment_v015/artifacts/config.json
--rows-out experiment_v015/work/confirmation_eval_001/raw_rows.jsonl
--summary-out experiment_v015/work/confirmation_eval_001/summary.json
--cases-out experiment_v015/work/confirmation_eval_001/case_samples.json
```

Independent capture, only after the primary capture exits `0` and all three outputs exist:

- capture directory: `experiment_v015/captures/confirmation_audit_001`;
- cwd: `experiment_v015/work/confirmation_audit_001`;
- inputs: frozen independent auditor, frozen config, primary raw rows, and primary summary;
- output: `experiment_v015/work/confirmation_audit_001/report.json`.

No retry, threshold change, input substitution, model/domain removal, alternative judge subset, normalization, or output repair is permitted in v015. A primary crash, missing output, input mismatch, or audit failure is a real v015 Confirmation failure and requires immutable closure before any later version.

## Frozen metrics and gates

The primary reference is restricted to rows where the two released judge labels agree. The official rule and RGP consume identical traces, joins, and labels. The majority ensemble is excluded.

All ten Confirmation gates are conjunctive:

1. all 36 manifest bytes verify; exactly 12 traces, 24 judges, zero ensembles;
2. exactly 12,000 unique joined rows across 12 models and five domains, with no join error;
3. exact official reproduction on every classifier-supported released label and no unexpected external label;
4. no RGP change to CTRL, external-error, expected-tool-not-called, or required-contract-failed rows;
5. unanimous-reference paired accuracy delta at least `+0.005`;
6. 20,000-resample generator-model-cluster bootstrap with seed `20260723` has 95% lower bound `> 0`;
7. corrections strictly exceed regressions;
8. strictly positive accuracy delta on at least `9/12` generator models;
9. strictly positive accuracy delta in at least `4/5` domains;
10. at least 100 `official output_fabrication -> RGP correct -> unanimous correct` transitions across at least four domains.

Macro-F1, all transitions, judge disagreements, external passthroughs, per-model/domain results, corrections, regressions, and bounded raw case samples remain reportable even though they are not substituted for primary gates.

## Main-Codex post-execution audit

After both captures, the main Codex must personally:

1. verify capture exit codes, durations, argv, runner SHA, input/output hashes, and empty/nonempty stderr facts;
2. read the complete primary summary and independent report;
3. recompute/check manifest, row-key, baseline, structural, metric, bootstrap, and gate agreement;
4. inspect original frozen bytes for a bounded set of corrections spanning observed domains and every regression, without reopening selection or adding tests;
5. decide whether the narrow claim survives all inherited Development and Confirmation evidence.

Only a passing scientific judgment permits freezing `review_v015/packet.md`. Reviewers remain forbidden until that Packet is complete and immutable.
