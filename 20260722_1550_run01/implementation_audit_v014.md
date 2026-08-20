# v014 Main-Codex Implementation Audit

## Audit boundary

- Auditor: current main Codex; no subagent was created.
- Candidate: Required-Grounding Precedence.
- Review time: before any v014 Development execution and before any Confirmation acquisition.
- Confirmation trace files present under the Development source root: `0/12`.
- `confirmation_content_acquired`: `false`.
- Review Packet, Reviewer report, Decision, and Delivery: absent.

## Frozen code reviewed

| File | SHA-256 |
|---|---|
| `implementation_v014/audit.py` | `6BC2A6D80A4CFDCF82AD6480E3D762DFB252B32F9BE7D849C84466D12E47F057` |
| `implementation_v014/independent_audit.py` | `E6A7E4649ABA4B62D9E2CB5CF8722F59B42058C8FDC7D83B5765471B5820ED3E` |
| `implementation_v014/config.json` | `AEF60703933916E8C781AF3E650AE735E0C664FDACA07D53FACE4052AE165E2F` |
| `implementation_v014/test_audit.py` | `0CB9A63ACB018FAEFC661234AD4470D646876742A69074CB8BC76DA530DBF206` |

The config binds the current Candidate SHA `1B511D662B6CD951E2FFD2C95965B0FC4223636A30EB348EE68F973C80840E7F`, current Evidence Packet SHA `4D2735F63E9102DB330636BFE635B0DD16739CAB132F68ED1E61C46E2FB7B6BE`, Development manifest SHA `E5FC4A15DDC7F4B17E6CC04E9BC518FC53050BA11BC7B24BA026E703B161146E`, partition SHA `C0BC90D4F429F79E394D7467D768B64F8471E82704B3F98A1666CF0092B6EC90`, and official detector SHA `AEE4D77596BDACB9025D85CCCDE766FF2A2DDBE1A291B6C143EA46D22863DBD0`.

## Main-code review findings

### Changed computation

`rgp_classify` changes one branch order only:

1. preserve CTRL behavior;
2. preserve expected-tool skip;
3. apply the official `_answer_correct` predicate;
4. apply the official `detect_output_fabrication` predicate;
5. otherwise return `result_ignore`.

The implementation imports the fixed official detector by explicit path and refuses a detector SHA mismatch. It does not add normalization, fuzzy matching, semantic similarity, threshold search, or a learned component.

### Input and join integrity

- Every one of the 40 frozen Development manifest entries is rehashed and byte-counted before parsing.
- Exactly 10 top-level trace files, 20 judge files, and 10 ensemble files are required.
- Ensemble files are hash-verified but never used as reference labels.
- Each trace and judge file must contain 1,000 unique task IDs.
- Both judge joins check model ID, task ID, domain, and the judge file's recorded rule label against the trace's released label.
- Primary metrics exclude the 655 previously observed judge-disagreement rows rather than select one judge.

### External pipeline state

The released Development bytes contain one `other_error` row whose answer is a JSON decoding error and whose task would be `tool_skip` if passed through `detect.py`. Because `other_error` is a generation-pipeline state outside the six-label classifier, the code now:

- declares it prospectively in `external_labels_passthrough`;
- reports its count;
- preserves it unchanged under RGP;
- requires every classifier-supported row to reproduce the released label;
- fails on any unlisted external label.

This correction was made before the Experiment Plan and before Development. It prevents an impossible all-row classifier-identity gate without reinterpreting the external failure as scientific evidence for RGP.

### Metrics and uncertainty

- Official and RGP predictions use identical joined rows.
- Accuracy, macro-F1, corrections, regressions, per-model and per-domain deltas are computed from unanimous rows.
- The bootstrap resamples generator-model clusters, not individual rows, for 20,000 fixed-seed resamples.
- The summary reports every label transition and binds raw row and case-sample SHA values.
- Zero-regression correction ratios are represented as JSON `null`, not nonstandard `Infinity`; the corresponding gate requires at least one correction.
- All JSON writers reject NaN/Infinity.

### Independent audit

`independent_audit.py` does not import `audit.py`. From raw output rows it independently recomputes:

- row/key cardinality;
- paired accuracy and macro-F1;
- corrections and regressions;
- per-model and per-domain metrics;
- the full fixed-seed cluster bootstrap;
- mechanism transitions;
- branch-change structural invariants;
- baseline identity and external-label consistency;
- all metric-dependent gate booleans.

It compares the recomputed metrics and gate booleans with the primary summary and exits nonzero on an audit failure.

### Scientific authority boundary

`audit.py` writes mechanical gate booleans but explicitly states that they do not authorize Confirmation or Delivery. It contains no network acquisition, no Confirmation filename, no Reviewer call, no Decision writer, and no automatic Run/system state mutation.

## Necessary pre-execution tests

Command:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe -B -m unittest -v test_audit.py
```

Result:

- exit code: `0`;
- tests: `7`;
- failures/errors: `0`;
- covered branches: CTRL unchanged, tool skip unchanged, required grounding precedence, retained fabrication, retained result-ignore, macro-F1 identity, and frozen flattened Artifact-path resolution.

All three Python files also passed AST parsing. A subsequent explicit `py_compile` syntax check created three `.pyc` files; those exact cache files and their now-empty `implementation_v014/__pycache__` directory were removed. No v014 `.pyc` remains.

## Pre-Plan Artifact-layout correction

The first Artifact freeze correctly copied and hashed all 40 Development files but flattened their manifest-relative paths into single-component names such as `input__judge__model.json`, as required by the existing versioned Artifact API. The reviewed program still resolved the original nested manifest paths and therefore would have required reading the nonfrozen source directory.

Before writing the Plan and before any Development execution, the main Codex corrected `manifest_path` to deterministically map every manifest path to its frozen flattened Artifact name. No label, metric, gate, dataset byte, or scientific computation changed. A seventh unit test now fixes this mapping. The initially frozen `program_audit.py`, `test_audit.py`, and `implementation_audit.md` remain immutable historical pre-Plan artifacts; the Plan must reference only the corrected `program_audit_r2.py`, `test_audit_r2.py`, and `implementation_audit_r2.md`.

## Workspace integrity before Plan

`tools/inspect_run.py` executed from the correct `crl_agent_v3` working directory and exited `0`:

- current version: `v014`;
- Candidate exists and both Evidence references are current;
- Evidence Packet is bound to the current Candidate;
- Research Map Evidence references are current;
- `integrity_ok`: `true`;
- errors: `[]`.

## Audit disposition

The implementation is minimal, directly tests the selected computation, preserves the untouched boundary, and has no unresolved code-level blocker found in this review. The main Codex authorizes freezing these exact bytes and writing one prospective Development Experiment Plan. This audit does not authorize Confirmation, Reviewers, Decision, Delivery, or `READY_FOR_RESEARCH_USAGE`.
