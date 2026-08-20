# Implementation Audit v021

Status: `PASS_FOR_ONE_SHOT_DEVELOPMENT_FREEZE`.

This is a main-Codex source and structural audit. It is not Development evidence, does not authorize Confirmation, and does not substitute for the later independent replay audit.

## Allowed delta

v021 leaves the v020 Candidate, data, reference selection, split, vocabulary, learner, hyperparameters, threshold rule, bootstrap and gates unchanged. The implementation adds only two comparator feature maps and the unavoidable seven-method/version bindings:

- `triple_text = [x,x,x]`;
- `duplicated_absolute = [x,abs(x-r),abs(x-r)]`.

The executable and auditor load the frozen v020 sources from sibling files and reject them unless their SHA-256 values equal the config bindings. They then replace only `METHODS`, `COMPARATORS`, and the feature-map function. The v020 training loop, model construction, validation threshold selection, Development split, strongest-comparator selection, task bootstrap, raw-row writer, model bundle, Confirmation path and environment capture remain the frozen base implementation.

## Source review

- `implementation_v021/program.py` SHA-256 `98e1f01451bfb6bc592dc2a8f24f23b10ac709fe665d40c5885ee20f6c5ef8d7`.
- `implementation_v021/audit.py` SHA-256 `ff499a10f80fb4d428291d3fa43142a3248705d93fcefc506eeba74cb3c6c4a5`.
- `implementation_v021/config.json` SHA-256 `8d6eee0a9fdb29e286b918eb13a02bbf5ad246b5467b4ea2f93e9fe93ee50eb0`.
- `implementation_v021/test_capacity_controls.py` SHA-256 `9a631beea14c1345554cb4ac936d99150496616d1f8d0f11a0a62462799bbc7`.
- Required v020 program SHA-256 `67ac151b6817d6619f915aad581da6c70f9ecdafeb780d87e31816c36009de92`.
- Required v020 auditor SHA-256 `2f42878764989288ee44a68d287af2cccfb2e25f72f7eb2fde40e9d81a898607`.
- Required v012 base SHA-256 `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`.

The program's seven-method tuple is used by training, validation scoring, threshold selection, Development scoring, metric generation, raw per-row score output, feature-dimension capture and model serialization. The six-comparator tuple is used by strongest-comparator selection and strict pairwise superiority. The auditor independently reconstructs both new sparse maps from source rows and the serialized vectorizer, replays all seven fitted models, recalculates every metric/gate and selects the strongest of all six comparators.

## Executed checks

All counted checks used the fixed interpreter `D:\Desktop\crl\crl_agent_v3\.venv\python.exe` from the v021 implementation directory.

1. `python.exe -m py_compile program.py audit.py test_capacity_controls.py`
   - exit code `0`.
2. `python.exe -m pytest -q -p no:cacheprovider test_capacity_controls.py`
   - exit code `0`;
   - result `1 passed in 0.17s`.
3. Read-only structural preflight on the fixed Development dataset and v012 base
   - exit code `0`;
   - `PREFLIGHT_OK`;
   - source rows `1,729`;
   - eligible references `94`;
   - evaluated rows `1,613`;
   - ineligible tasks `2`;
   - training rows `943`;
   - fitted vocabulary `30,000`;
   - Candidate, triple-text and duplicated-absolute dimensions all exactly `90,000`;
   - every repeated block was byte-value equivalent to the intended source sparse matrix.

An earlier shell diagnostic referenced the nonexistent `\.venv\Scripts\python.exe`; neither Python check started and it is not counted as evidence. The commands above are the corrected authoritative executions.

## Binding and disposition

- Current Candidate SHA-256: `fd3978d343d0ca33a2301a3c2e7e7b2897c37b2b2c3e5ab74ae393608ee4e917`.
- Current Evidence Packet SHA-256: `bb17ab6db299968bba3fcbba599f2f6e9a0fe4095497be2c2d47d36674a825cf`.
- The Evidence Packet binds the current Candidate SHA exactly.
- No bucket-3 byte was acquired or read by these checks.
- No model was fitted and no scientific metric was produced by these checks.
- No Reviewer was started.

The implementation is sufficiently specified and structurally verified for exactly one frozen v021 Development fit/score capture followed by exactly one independent audit capture.
