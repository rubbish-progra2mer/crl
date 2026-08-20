# v014 Main-Codex Development Promotion Audit

## Decision

`PROMOTE_TO_UNTOUCHED_CONFIRMATION`

This is a main-Codex scientific decision after direct inspection. It is not derived from the program's `10/10` field alone and does not authorize Reviewers, Decision, Delivery, or a system-state change.

## Execution identity

### Environment capture

- capture: `env_capture_001`
- runner exit: `0`
- duration: `1.889052399998036s`
- execution SHA-256: `F301E325EF274AA5B40A3557BDE57BFA4ED84856EBC8B978FA367F47C24A933C`
- stdout SHA-256: `3331DE8D0722CC4064A6E95D3DFD1EB29E61BB84713F0A553E01052C5599BA8E`
- stderr SHA-256: `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`
- Python: `3.11.15`
- NumPy: `2.3.5`
- SciPy: `1.16.0`
- PyTorch: `2.12.0+cu130`
- CUDA runtime: `13.0`
- GPU: `NVIDIA GeForce RTX 5060 Ti`
- capability: `12.0`
- synchronized 4096-element CUDA kernel sum: `22898102272.0`

### Development

- capture: `dev_eval_001`
- child argv program: frozen `program_audit_r2.py`
- program SHA-256: `6BC2A6D80A4CFDCF82AD6480E3D762DFB252B32F9BE7D849C84466D12E47F057`
- runner exit: `0`
- duration: `4.083998599999177s`
- execution SHA-256: `6919473FCD8A8BB1210B8F125A4C581D7BB896E4DC926A3815DB713417EC81D1`
- stdout SHA-256: `7D4D1F60F7CE95713D1112359011476DE8F8802712F97B94E6D392B74A56793D`
- stderr SHA-256: `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`
- raw rows SHA-256: `5C50F38438621C18EDBE1B34EB6595798B9D6980B7E96A18C3805A009F5DC8E8`
- summary SHA-256: `4FD042AC7BF194452AC294C7E82534651B701FE60E778DAC4FD7223ECA60486A`
- case samples SHA-256: `EBD851A176AD0C02408385AFDBBA0382586B539064F0374FC4D9C27CB687F8EC`

The capture lists the corrected program, manifest, config, official detector, and all 40 flattened input Artifacts as input facts. The exact child argv matches the publish-once Plan and reads only `experiment_v014/artifacts`, not the source acquisition directory.

### Independent raw-row audit

- capture: `dev_audit_001`
- runner exit: `0`
- duration: `0.33927369999946677s`
- execution SHA-256: `77F4164ABDBD276A3D94244A4E6812B859F37DE75F53CA281E4BD2511EBDBA88`
- stdout SHA-256: `4E22B82575F53382B7ACD8F1B03EE39A4A3C223CB2429738AED1F4A880226E9A`
- stderr SHA-256: `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`
- report SHA-256: `99CA0A6733B128454B015E0DAB7F94BAB2F2B89DC3BB26B3878436B76759DE4C`
- `audit_ok`: `true`
- metric maximum absolute error: `0`
- raw-row SHA matches primary summary: `true`
- recorded metric gates match independently recomputed gates: `true`

## Integrity audit

- manifest entries verified: `40/40`
- trace files: `10`
- judge files: `20`
- ensemble files hash-verified but unused: `10`
- joined rows: `10,000`
- unique `(model_id, task_id)` keys: `10,000`
- unanimous two-judge rows: `9,345`
- judge-disagreement rows excluded from primary metrics: `655`
- join errors: `0`
- classifier-supported baseline identity errors: `0`
- external passthrough rows: `1` (`other_error`)
- unknown external labels: `0`
- structural-invariance violations: `0`

RGP changed exactly 187 rows, all from released `output_fabrication` to `correct`. It did not change CTRL, external-error, or expected-tool-not-executed rows.

## Primary result

On 9,345 unanimous-reference rows:

- official correct: `8,687`
- RGP correct: `8,843`
- official accuracy: `0.9295880149812734`
- RGP accuracy: `0.9462814339218834`
- paired accuracy delta: `+0.016693418940609953`
- model-cluster bootstrap 95% interval: `[+0.010464272171620851, +0.02313872522763792]`
- bootstrap minimum across 20,000 resamples: `+0.004522983065109919`
- corrections: `157`
- regressions: `1`
- correction-to-regression ratio: `157:1`
- positive generator models: `9/10`
- zero-delta generator models: `1/10`
- positive domains: `5/5`
- supported OF-to-correct transitions: `157`
- mechanism domains: `5/5`

All ten preregistered Development gates pass without modification.

## Secondary result and interpretation limit

- official macro-F1: `0.46603212224458035`
- RGP macro-F1: `0.46610138266536577`
- macro-F1 delta: `+0.00006926042078542194`

The macro-F1 change is effectively neutral. Development supports a narrow reduction in high-frequency false `output_fabrication` labels relative to unanimous judges, not a broad improvement across all six failure categories.

## Main-Codex direct case audit

The main Codex read the primary summary, independent report, deterministic case-sample file, raw-row facts, and original frozen trace/judge bytes. It inspected one correction from each domain and the only regression.

Representative corrections:

- cybersecurity `RI-SEC-004`: the answer reproduces PCI-DSS 4.0 requirement 8.3 details present in the return; both judges identify the same grounded values.
- finance `OF-FIN-004`: all three META Form 4 rows, dates, share counts, and prices match the mock return.
- legal `OF-LEG-045`: the UCC good-faith definition and amendment context match the returned definition.
- medical `RI-MED-005`: 2300 mg, 25 mg/kg, maintenance, AUC target, and renal note match the return.
- real estate `RI-RE-018`: zone, ADU/JADU, SB-9 eligibility, and four-unit potential match the return.

The sole regression is real:

- legal `TS-LEG-017`, generator `deepseek-v4-flash`;
- official and both judges: `output_fabrication`;
- RGP: `correct`;
- the answer includes the required `$126.4 million` value but invents intermediate HSR fee brackets and a `$252.7M` size-of-person threshold not present in the tool return.

This regression demonstrates that required-field satisfaction does not prove absence of extra fabrication. It was anticipated in the Candidate risks and is far below the preregistered correction-margin boundary. It must remain visible in Confirmation, Review, and any final claim.

## Promotion reasoning

Promotion is authorized because:

1. the changed computation is exactly the preregistered one-branch reorder;
2. inputs, joins, official-label identity, and structural invariance are exact;
3. the paired effect exceeds the fixed threshold and remains positive under generator-model cluster resampling;
4. the effect spans nine generator models and all five domains;
5. 157 corrections are supported by both independent judges, versus one genuine regression;
6. representative original bytes confirm that the mechanism is concise supported-field reporting rather than hidden normalization or label leakage;
7. the independent audit reproduces all metrics exactly.

Promotion is not based on novelty alone. The contribution remains capped at a benchmark measurement correction, and Development is fully exposed. Untouched generator-model Confirmation is therefore necessary.

## Confirmation authorization and prohibitions

The main Codex authorizes acquisition of only:

- the 12 trace files in the frozen Confirmation partition; and
- their 24 independent judge files;
- dataset revision `77ef18dadfc1ad96ce29c863f0913d990659432a`.

Forbidden:

- ensemble files;
- any change to code, predicates, config, labels, bootstrap, thresholds, or model/domain subsets;
- retuning to eliminate `TS-LEG-017`;
- semantic normalization or extra fabrication checks;
- use of Development as Confirmation;
- any subagent before a complete Confirmation-backed Review Packet is frozen.
