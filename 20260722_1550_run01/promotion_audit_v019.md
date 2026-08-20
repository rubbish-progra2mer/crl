# Main-Codex Promotion Audit v019

Disposition: `NO_GO_FOR_CONFIRMATION`

System status remains `DEVELOPMENT_NOT_COMMISSIONED`. Run status remains `ACTIVE`. This audit is the main Codex's scientific judgment over the frozen v019 Development bytes; it is not a script gate, Reviewer vote, Decision, or Delivery.

## Execution and integrity facts

- Development capture `experiment_v019/captures/dev_001/execution.json`: exit `0`, duration `3271.7866745000065` seconds, SHA-256 `6596B0748ACBFA6804DB05173E2F108DBAC295BE2678A52E27ED20CD9B0B6C00`.
- Program summary: 2,160 rows, 400 source queries, 120 fixed Development-test queries, registry/candidate size 370, 18 policy groups, 96 controller updates, and 12 models.
- Development raw rows SHA-256 `68DC0BC02218C853245B00AF22FFBF539873C42A2A48D85A6DB3CB1BB9AB6897`.
- Development summary SHA-256 `928AF6F01551C033BBCCBC1004C35EC0CB255322CFA930D5CF7D9AB465105AEF`.
- Controller history SHA-256 `9F5901F7C6EF739BA53C8668DBC0299733646A9B850788C8866A5D9FC5C41AE0`.
- Development stdout SHA-256 `91435CADE294C11CC503F10926C75F4AF52AD87B0C7AE9A0E5B0B8C56A99E4BA`; stderr was empty.
- Independent audit capture `experiment_v019/captures/dev_audit_001/execution.json`: exit `0`, duration `59.28443289999268` seconds, SHA-256 `D19EC3E75A491689F5022A6FF87A9D14C0BA013AC29FEFEB62AB2F3C6434B365`.
- Audit report SHA-256 `F4D75DE02331B89014CE60A77BC2FFCB92026848A8A6AAC4DF77E5AC493A2128`; status `AUDIT_OK`, zero errors, 2,160 rows, 18 groups, 120 query IDs, 96 controller updates, 12 models, and 1,440 independently replayed learned-policy actions.
- Maximum raw-row, controller-update, and policy-K errors were exactly zero. Maximum summary metric error was `1.3322676295501878e-14`, below the Candidate's frozen `1e-12` tolerance. The Experiment Plan also contained the stricter prose phrase “every maximum error equal to zero”; that phrase was not literally met. It is recorded as a mechanical Plan miss and is not used to rescue or reinterpret the outcome.

## Frozen Development outcome

Policy means on the fixed 120-query Development split:

| Policy | Coverage | Mean K | Defined BoR |
|---|---:|---:|---:|
| Candidate coverage-constrained chance DQN | 1.000000 | 370.000000 | 0.000000 |
| Target BoR-DQN | 0.791667 | 5.150000 | 5.830157 |
| Target F1-DQN | 0.772222 | 2.313889 | 7.037896 |
| Unconstrained ratio DQN | 0.963889 | 278.736111 | 0.387529 |
| Fixed K=10 | 0.900000 | 10.000000 | 5.057450 |
| Fixed K=20 | 0.908333 | 20.000000 | 4.070747 |
| Fixed K=50 | 0.925000 | 50.000000 | 2.775051 |

Candidate minus target BoR-DQN:

- coverage `+0.208333` — coverage condition passed;
- mean K `+364.85` — required `<= -1.0`, failed in the opposite direction;
- defined BoR `-5.830157` — required `>= +0.25`, failed in the opposite direction;
- matched-seed condition count `0/3` — required at least `2/3`;
- nondominance flag was true only because no listed comparator achieved exactly 1.0 coverage with lower K; this does not compensate for the three failed primary conditions.

## Raw-case and trajectory readback

The Candidate chose exactly `K=370` for all 120 queries in all three seeds: minimum K 370, maximum K 370, one distinct depth, and 120 hits per seed. Against matched target BoR-DQN rows, every seed had 0 lower-K cases, 1 equal-K case, 119 higher-K cases, 25 coverage corrections, and 0 coverage regressions. Thus the extra coverage came entirely from near-universal maximum exposure, not selective preservation of difficult cases.

The Candidate training probe was already at approximately 0.996-1.0 coverage and mean K approximately 366-370 by episode 500. Its dual decreased from 0.05 to zero by episode 3,000 for all seeds and stayed zero through episode 8,000, yet the learned greedy policy remained at K=370. The slow update arithmetic is correct and independently verified, but the frozen DQN did not realize the intended cost-minimizing behavior when the multiplier reached zero. The exact optimization failure mechanism is not identified by these bytes, so this audit does not claim a general impossibility result for coverage-constrained chance exposure.

The ratio ablation also showed large oscillations and ended with mean K from 225.12 to 364.10 across seeds. This supports an instability concern for these slow-objective DQNs on the fixed state/data, but it is an ablation observation, not the primary rejection reason.

## Main-Codex judgment

v019 fails its preregistered scientific purpose. It raises coverage only by exposing the complete 370-tool registry and is dramatically worse than the target on depth and defined BoR. No threshold may be lowered, no positive claim may be narrowed around the 1.0 coverage result, and no Confirmation bytes may be acquired. No Reviewer is authorized.

v019 is frozen as a failed Candidate within the same Run. A later version must not retune the same dual step, initialization, episode count, or gate to repair this outcome. It needs a scientifically changed optimization computation or a different research problem, with a new Candidate, Evidence Packet, implementation, and one-shot Plan. The prospective Confirmation source remains untouched.
