# Neutral Selection Context v019

## Recovery and version boundary

- Run: `20260722_1550_run01`.
- System state: `DEVELOPMENT_NOT_COMMISSIONED`.
- Run state: `ACTIVE`.
- Current version began from the durable v018 no-candidate disposition.
- v019 has not started a model-training run, created a Development capture, acquired Confirmation, frozen a Review Packet, started a Reviewer, or created Delivery.

v017 closed pairwise/listwise tool discrimination and hidden-state tool-necessity control because direct 2026 priors occupied those computations. v018 closed argument provenance, multilingual schema projection, constrained-planning revision, incomplete-contract gating, and memory-poisoning screening because the proposed deltas either collided with direct priors or lacked a real runnable carrier. v019 does not reopen those routes, TPPA, P084 reranking, Required-Grounding Precedence, or Run011-style fixtures.

## Route screened and rejected in v019

The first v019 route was inference-time counterbalancing of tool-list order. The formal Cards recovered P069's identical-tool order bias. Direct primary-source search then found that the relevant computation is already occupied by permutation self-consistency, CalibraEval, RoToR, CapCal, DGAO, and permutation-aware GRPO. Repeating tool permutations and voting, averaging, or calibrating logits would therefore be a domain application of established position-debiasing computations, not the unique narrow gap selected below.

## Selected route and its relation to v013

v013 established from fixed source bytes that the target adaptive-depth paper defines an aggregate metric

```text
BoR = log2(mean(hit) / mean(K/N))
```

but trains its DQN with a success-weighted per-query surrogate

```text
hit * -log2(K/N).
```

v013 was an evaluation audit. It did not propose a replacement policy objective and explicitly forbade claiming a new adaptive-K algorithm. Its Development failed preregistered audit gates and remains frozen.

v019 is scientifically different: it tests an explicit coverage-constrained decision objective on the unchanged target STOP/CONTINUE state and network. It does not change, lower, or rerun v013's audit gates. The proposed computation uses `K/N` as chance exposure and a slow dual variable to maintain a prospectively fixed coverage demand.

## Data exposure and optional-stopping record

The following v013 Development bytes and results have already been read in this Run:

- `sources_v013/bfcl_development/BFCL_v3_simple.json`, 400 lines, SHA-256 `FBC37B2AD252BF9AF985582E0E07B456173FE627D957491472EA9CEF5FB83158`.
- `experiment_v013/artifacts/dev_eval_001_raw_rows.jsonl`, 1,440 rows, SHA-256 `64046FE59AE1706975830585D48896D689C31807D6139D153F7F18F91C598A68`.
- The v013 local rows report target-labelled BoR-DQN mean coverage `0.925`, mean K `9.7388888889`, and mean defined BoR approximately `5.1585` across seeds 42, 123, and 456.
- Fixed-K Development results, including `K=1` coverage `0.60` and defined BoR `7.7944`.

These facts make BFCL v3 simple an exposed Development carrier, not untouched evidence. The v019 computation was selected after these results were known, so its thresholds and interpretation must remain narrow and Confirmation must be prospective. No v019 training output is currently known.

## v013 comparator defect discovered before v019 implementation

Direct source-code comparison found that `implementation_v013/audit.py` did not reproduce the target BFCL policy state or split:

- v013 state exposed `float(found)` as feature 7, which leaks whether the gold tool is already present at decision time;
- the target BFCL notebook state contains only K and score-distribution features and no gold-dependent feature;
- v013 used Python shuffle plus a 70/30 prefix split, while the target notebook uses `train_test_split(..., random_state=42)`;
- v013 also differs from the target BFCL replay size, batch size, epsilon schedule, F1 reward, continuation cost, and target-copy timing.

Therefore the v013 learned rows and weights are frozen historical evidence but are not a fair v019 target comparator and will not be used to claim a Candidate improvement. This does not overwrite or reopen v013. v019 must reproduce the actual target BFCL code once, inside the same frozen Development execution as the Candidate. Fixed-K arithmetic remains usable because it does not depend on the leaked state or training split, but v019 will recompute it on its own official split.

The fixed prospective Confirmation is `berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_live_simple.json` at Gorilla commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`. Its file bytes have not been downloaded or read in this Run. Acquisition remains forbidden until v019 Development and the main-Codex Promotion Audit authorize it.

## Fixed primary sources

- `sources_v013/how_many_tools_2605.24660.pdf`, SHA-256 `4DB89BFAC79BC90DD5B532D04AC1012ED1691657A45379BBBB2312682847164C`.
- `sources_v013/bits_over_random_2605.18857.pdf`, SHA-256 `8587A2502CF4F5FA371A04EACA3EEC4D782AD52D0A12F346606EE2FFD4B3EC02`.
- `sources_v019/ratio_rl_icml2021.pdf`, SHA-256 `949FE7D0D8137A6EF1190BFCA17F258603602AC881D8F99F04D1B720C71DA877`.
- `sources_v019/offline_adaptive_retrieval_2604.05125.pdf`, SHA-256 `357EC6826E8C4032D9F807CC31440E5BFE47F4B4003C22EF698A4EB85469122F`.

The main Codex parsed 45 physical pages and directly read the metric, reward, two-timescale ratio-RL, cost-aware stopping, Pareto, and limitations sections. This is a bounded primary-source record, not proof that no unindexed implementation exists.

## Current disposition

One candidate is promoted to implementation design: coverage-constrained chance-exposure depth control on the target DQN. Its unique empirical question is whether explicit coverage control can reduce chance exposure relative to the frozen target surrogate without sacrificing the target's presented-gold coverage. Generic constrained RL and ratio optimization are borrowed components and are not claimed as new mathematics.
