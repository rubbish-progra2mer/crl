# Experiment Plan

```json
{
  "experiment_id": "v014",
  "candidate_sha256": "1b511d662b6cd951e2ffd2c95965b0fc4223636a30eb348ee68f973c80840e7f",
  "evidence_packet_sha256": "4d2735f63e9102db330636bfe635b0dd16739cab132f68ed1e61c46e2fb7b6be"
}
```

## Codex Plan

# v014 Prospective Development Experiment Plan

## Authority and state

- System state remains `DEVELOPMENT_NOT_COMMISSIONED`.
- Run `20260722_1550_run01` remains `ACTIVE`.
- Version: `v014`.
- Candidate: Required-Grounding Precedence.
- Candidate SHA-256: `1B511D662B6CD951E2FFD2C95965B0FC4223636A30EB348EE68F973C80840E7F`.
- Evidence Packet SHA-256: `4D2735F63E9102DB330636BFE635B0DD16739CAB132F68ED1E61C46E2FB7B6BE`.
- Confirmation files are unacquired and unread.
- No subagent may be created during Development or Promotion Audit.

This Plan is prospective and publish-once. Mechanical output fields do not authorize Confirmation, Reviewers, Delivery, or a system-state change.

## Research question and hypothesis

The released ToolFailBench deterministic classifier runs a coarse output-fabrication heuristic before its own required-answer contract. The hypothesis is that moving the unchanged exact required-answer predicate before the unchanged fabrication predicate reduces false `output_fabrication` labels relative to rows where both released independent judges agree.

The computation changes only predicate order. It does not change:

- expected-tool detection;
- CTRL classification;
- `answer_must_contain`;
- `match_mode`;
- case-insensitive exact substring matching;
- the 30% mock-leaf threshold;
- the structured-keyword list;
- judge outputs or labels;
- any threshold after observing Development.

## Frozen implementation

The first Artifact copy exposed a path-layout mismatch before this Plan: the Artifact API flattened 40 source-relative input paths, while the first program artifact expected nested source paths. No science was executed. Immutable first copies remain as history.

Only these corrected program bytes are authorized:

| Artifact | SHA-256 | Role |
|---|---|---|
| `program_audit_r2.py` | `6BC2A6D80A4CFDCF82AD6480E3D762DFB252B32F9BE7D849C84466D12E47F057` | primary Development program |
| `program_independent_audit.py` | `E6A7E4649ABA4B62D9E2CB5CF8722F59B42058C8FDC7D83B5765471B5820ED3E` | independent raw-row audit |
| `config.json` | `AEF60703933916E8C781AF3E650AE735E0C664FDACA07D53FACE4052AE165E2F` | frozen thresholds, seeds, bindings |
| `official_detect.py` | `AEE4D77596BDACB9025D85CCCDE766FF2A2DDBE1A291B6C143EA46D22863DBD0` | fixed official classifier |
| `test_audit_r2.py` | `0CB9A63ACB018FAEFC661234AD4470D646876742A69074CB8BC76DA530DBF206` | seven pre-execution unit tests |
| `implementation_audit_r2.md` | `85BC23C70A39C8AB3EFE564BFFA1FFA6E8231045D318761A6E8F2C72DD0DA1EB` | main-Codex source review |

The superseded `program_audit.py`, `test_audit.py`, and `implementation_audit.md` must not appear in any execution argv.

## Frozen Development inputs

- Dataset: `SoHarshh/toolfailbench-traces`.
- Revision: `77ef18dadfc1ad96ce29c863f0913d990659432a`.
- Frozen manifest Artifact: `development_manifest.json`.
- Manifest SHA-256: `E5FC4A15DDC7F4B17E6CC04E9BC518FC53050BA11BC7B24BA026E703B161146E`.
- Frozen partition Artifact: `partition.json`.
- Partition SHA-256: `C0BC90D4F429F79E394D7467D768B64F8471E82704B3F98A1666CF0092B6EC90`.
- Development entries: 40.
- Trace files: 10.
- Independent judge files: 20.
- Ensemble files: 10, hash-verified but excluded from reference labels.
- Total frozen pre-Plan Artifact bytes before corrected r2 copies: `293,381,005`.

For each manifest path `p`, the actual frozen input is:

```text
experiment_v014/artifacts/input__ + p.replace("/", "__")
```

The corrected program applies only this mapping. The runner must list all 40 flattened files as input facts. It must not read `sources_v014/toolfailbench_development`.

Development generator models:

1. `claude-sonnet-4`
2. `deepseek-r1-distill-llama-8b`
3. `deepseek-v4-flash`
4. `gemma4-27b-a4b`
5. `gemma4-31b`
6. `glm4.7-flash`
7. `grok-4-1-fast-reasoning`
8. `grok-4.3`
9. `qwen2.5-72b-instruct`
10. `qwen3.5-27b`

All Development content was exposed during selection. It is not Confirmation evidence.

## Reference labels and rows

- Join key: `(model_id, task_id)`.
- Each trace file and each judge file must contain exactly 1,000 unique task IDs.
- Both judge files must agree with the trace on model, task, domain, and recorded rule label.
- Primary metrics use only rows where the two judge failure-mode labels are identical.
- Judge-disagreement rows remain in raw output and counts but are excluded from primary accuracy/F1.
- The official majority ensemble is never used as a reference because it includes the comparator rule.
- The released external pipeline label `other_error` is counted and passed through unchanged. Any unlisted external label fails baseline identity.

## Primary and secondary metrics

Primary:

```text
paired accuracy delta =
accuracy(RGP, unanimous two-judge label)
- accuracy(released official label, unanimous two-judge label)
```

Secondary:

- official and RGP macro-F1;
- corrections and regressions;
- correction-to-regression ratio;
- per-generator-model accuracy delta;
- per-domain accuracy delta;
- complete official-to-RGP and prediction-to-reference transition counts;
- count and domains of `official output_fabrication -> RGP correct -> unanimous correct`;
- 20,000-resample generator-model cluster bootstrap, seed `20260723`, percentile 95% interval.

## Development gates

All ten gates are conjunctive and fixed:

1. **Input integrity:** all 40 manifest paths, sizes, and hashes match; exactly 10 traces, 20 judges, and 10 unused ensembles.
2. **Join integrity:** 10,000 unique joined rows; each 1,000-row trace and judge file has identical unique task IDs and matching metadata.
3. **Baseline identity:** every classifier-supported released label is reproduced; configured external labels are unchanged; no unknown external label occurs.
4. **Structural invariance:** no RGP change on CTRL, external-error, or expected-tool-not-executed rows; every changed row satisfies the official exact required-answer contract.
5. **Primary effect:** paired accuracy delta is at least `+0.01`.
6. **Cluster uncertainty:** model-cluster bootstrap 95% lower bound is strictly above `0`.
7. **Correction margin:** corrections are at least twice regressions; if regressions are zero, at least one correction is required.
8. **Model spread:** at least `8/10` generator models have strictly positive delta.
9. **Domain spread:** at least `4/5` domains have strictly positive delta.
10. **Mechanism support:** at least 100 `official output_fabrication -> RGP correct -> unanimous correct` rows across at least four domains.

No gate may be lowered or substituted after execution.

## Environment capture

Before Development, capture the shared environment with `tools/run_local_experiment.py` as `env_capture_001`. The exact child argv is:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe -B -c "import json,platform,torch,numpy,scipy; x=torch.arange(4096,dtype=torch.float32,device='cuda'); y=(x*x).sum(); torch.cuda.synchronize(); print(json.dumps({'python':platform.python_version(),'torch':torch.__version__,'torch_cuda':torch.version.cuda,'cuda_available':torch.cuda.is_available(),'gpu':torch.cuda.get_device_name(0),'capability':list(torch.cuda.get_device_capability(0)),'cuda_kernel_sum':float(y.cpu()),'numpy':numpy.__version__,'scipy':scipy.__version__},ensure_ascii=False,sort_keys=True)); assert platform.python_version()=='3.11.15'; assert torch.cuda.is_available(); assert torch.cuda.get_device_name(0)=='NVIDIA GeForce RTX 5060 Ti'; assert torch.cuda.get_device_capability(0)[0]>=12"
```

Any nonzero exit blocks Development until the actual environment problem is understood. It does not authorize an environment upgrade or downgrade.

## Exact Development argv

Run exactly once through `tools/run_local_experiment.py` as capture `dev_eval_001`. The child argv must be exactly:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe
-B
D:\Desktop\crl\20260722_1550_run01\experiment_v014\artifacts\program_audit_r2.py
--manifest
D:\Desktop\crl\20260722_1550_run01\experiment_v014\artifacts\development_manifest.json
--data-root
D:\Desktop\crl\20260722_1550_run01\experiment_v014\artifacts
--official-detect
D:\Desktop\crl\20260722_1550_run01\experiment_v014\artifacts\official_detect.py
--config
D:\Desktop\crl\20260722_1550_run01\experiment_v014\artifacts\config.json
--rows-out
D:\Desktop\crl\20260722_1550_run01\experiment_v014\work\dev_eval_001\raw_rows.jsonl
--summary-out
D:\Desktop\crl\20260722_1550_run01\experiment_v014\work\dev_eval_001\summary.json
--cases-out
D:\Desktop\crl\20260722_1550_run01\experiment_v014\work\dev_eval_001\case_samples.json
```

Declared outputs:

- `raw_rows.jsonl`;
- `summary.json`;
- `case_samples.json`.

The runner input facts must include the corrected program, config, official detector, Development manifest, and all 40 flattened manifest files.

## Exact independent-audit argv

If and only if Development exits `0` and creates all declared outputs, run exactly once through `tools/run_local_experiment.py` as capture `dev_audit_001` with child argv:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe
-B
D:\Desktop\crl\20260722_1550_run01\experiment_v014\artifacts\program_independent_audit.py
--rows
D:\Desktop\crl\20260722_1550_run01\experiment_v014\work\dev_eval_001\raw_rows.jsonl
--summary
D:\Desktop\crl\20260722_1550_run01\experiment_v014\work\dev_eval_001\summary.json
--config
D:\Desktop\crl\20260722_1550_run01\experiment_v014\artifacts\config.json
--report-out
D:\Desktop\crl\20260722_1550_run01\experiment_v014\work\dev_audit_001\report.json
```

Independent-audit exit must be `0`, `audit_ok` must be true, raw-row SHA must match the primary summary, and maximum recorded metric error must be at most `1e-15`.

## Resource budget

- Interpreter: shared Python 3.11.15 environment only.
- Primary computation: CPU JSON parsing plus fixed-seed bootstrap; no model training and no network.
- GPU: not used by the candidate, only verified in environment capture.
- Wall-clock budget: 20 minutes for Development and 5 minutes for independent audit.
- Retries: no scientific rerun. A pre-scientific launcher failure may be recorded and corrected only if no declared output byte was created and no input content was evaluated.

## Promotion and untouched Confirmation

After both captures, the main Codex must directly read:

- `execution.json`, stdout, and stderr for both captures;
- all primary summary fields;
- raw-row cardinality and transition samples;
- the independent report;
- a bounded set of correction and regression cases with original frozen trace/judge bytes.

Only if all Development gates, independent checks, and the main-Codex scientific Promotion Audit pass may the 12 frozen Confirmation generator-model traces and their 24 judge files be acquired. Ensemble files remain forbidden. No subagent may be created before a complete Confirmation-backed Review Packet is frozen.
