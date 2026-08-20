# v034 Result

DISPOSITION: `NO_GO_FOR_CONFIRMATION`

RUN_STATUS: `ACTIVE`

SYSTEM_STATUS: `DEVELOPMENT_NOT_COMMISSIONED`

## Frozen identity

- Candidate:
  `8f78b67bfa14e3f9cbbd94207143e2574c6898913f2045cbb38f1cdb1d750a09`
- Evidence Packet:
  `56d2c6e8b911056fafb6c23b856ccbd0992fc20e2205d709694729e2e4f89ead`
- Artifact Manifest:
  `771a15c6f815f223d6945ccbf2cbbf5fffca8a2ebee3d51e82641cf7164a9acf`
- Plan:
  `97268348f2cd75d4e595dc0890e7b7ab2e11d867ac21939c436e8ad01d380010`
- Program:
  `a98b6f16b270fa4350bd1cf024bbf240f692d5658eb3be298117867e1d4a8ca4`
- Auditor:
  `b43735617e0e09c0294f467b187bf4b2c8771c78d35d79e420ae40fd06e629c2`

## Execution integrity

Development:

- exit code `0`;
- duration `1391.8097116999998s`;
- execution
  `7be16670fae2340c3d6daca2d65916d4ca360a9c8e0bd001e8db0ca5114943be`;
- pointwise scores
  `e872af3036dd871cdeef255b2e5b20c36022b760132d162db00869e7e6640087`;
- raw predictions
  `ad13327743ea10015c3d663d975b1aa5f2064a676659b17f3f3c95bc30c150bc`;
- summary
  `2d4f8b27620d68e06ceddd5f5bb3fe23ca6990dec23cffdec3ff1fb6ad4f9c1f`;
- environment
  `3fb5285e5e0d326af7ad0eca572fadd860c9c9bd605ec74803b93d2ef2fbbedd`;
- frozen state
  `189da3eec5add74582c1d2bf5445cc4587b844dcd5d045fc16b529af194c2de2`.

Independent model-replay audit:

- exit code `0`;
- duration `1160.6648085000052s`;
- execution
  `c6cf853e6527329f60a8bc1e52ea01f858a638b26ba5793646dbf2b85f2a14b9`;
- report
  `bbf1c7ff5c57c8117d552456dde28f23b94a82c29ca9b7498b0eb107c48f649a`;
- status `AUDIT_OK`;
- rows/actions/prompts `315/630/3780`;
- prompt-hash mismatches `0`;
- pointwise and derived maximum numeric errors `0.0`.

The shared environment is Python 3.11.15, NumPy 2.3.5, scikit-learn 1.9.0,
PyTorch 2.12.0+cu130, CUDA 13.0, Transformers 5.14.1 and NVIDIA GeForce RTX
5060 Ti. `PYTHONDONTWRITEBYTECODE=1`; the Run contains zero `.pyc` files.

One pre-capture runner invocation failed before scientific execution because
the parent `captures` directory did not exist. It created no capture or output.
The exact evidence is frozen under `pre_capture_attempt_001`; only that parent
directory was then created before the identical frozen payload ran.

Attempts Manifest:
`0f07e237119938fd861431f6b99bcd2bd26f888a03b58277b5a4caf8e195ce83`.

## Development result

Strongest mandatory comparator: `arguments`.

| Metric | CCCB | Strongest | Delta |
|---|---:|---:|---:|
| Overall accuracy | 0.682540 | 0.700000 | -0.017460 |
| GTA | 0.796610 | 0.855932 | -0.059322 |
| BFCL | 0.590090 | 0.653153 | -0.063063 |
| ToolTalk | 0.645349 | 0.546512 | +0.098837 |

Candidate-minus-strongest cluster-bootstrap 95% interval:
`[-0.0860941, 0.0458934]`.

Development gates: `3/8`.

Passed:

- Candidate accuracy `>=0.60`;
- each source Candidate accuracy `>=0.50`;
- exact action-swap integrity.

Failed:

- required `+0.03` overall delta;
- positive bootstrap lower bound;
- strict superiority to every comparator;
- nonnegative delta on all three sources;
- positive delta on at least two sources.

## Main-Codex judgment

Raw Analysis:
`d399676df25ff1161581380445d7b483a9d4dca213ae756f731722aa68fac6f2`.

Promotion Audit:
`0c82b5e52865e91d27d4f04a7c0feda6f487e3b1cd50df34d6a646a8de6c77fb`.

The fixed Candidate is above chance and better than the holistic prompt, but
the claimed conjunctive contribution is not identified. A single argument
obligation is stronger overall; CCCB regresses on two of three sources; and
raw regressions include the same prerequisite, evidence and ordering failures
the Candidate was designed to prevent.

The positive ToolTalk slice cannot be promoted as a post-hoc subgroup Claim.
No prompt, obligation, calibration, aggregation, model, source, control or gate
retuning is permitted under v034.

## Downstream boundary

- ToolSandbox acquired: `false`
- ToolSandbox read: `false`
- Confirmation executed: `false`
- Review Packet created: `false`
- Reviewer started: `false`
- Decision created: `false`
- Delivery created: `false`

v034 is frozen and closed. The same Run advances to v035 with a scientifically
different computation. No CCCB softening, reweighting, prompt retuning,
larger-model retry or ToolTalk-only narrowing is allowed.
