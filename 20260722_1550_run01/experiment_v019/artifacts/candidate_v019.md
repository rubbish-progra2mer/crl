<!-- crl-v3-evidence-ids
["ev-p039-aggregate-score-masking","ev-p080-fixed-depth-under-over-search","ev-p080-gold-supervised-minimal-depth"]
-->
# Candidate Implement v019 — Coverage-Constrained Chance-Exposure Depth

## One-sentence method kernel

On the target paper's unchanged BM25 ranking, score-only seven-feature state, binary STOP/CONTINUE action, and `7 -> 64 -> 64 -> 2` DQN, train terminal utility `lambda*hit - K/N` and update `lambda` slowly from a fixed 0.90 training-coverage residual, so the policy reduces chance exposure without hiding coverage inside a non-equivalent per-query BoR surrogate.

## Failure/Evidence -> Operator -> Gap lineage

P080 establishes query-dependent under/over-search and supervised earliest-sufficient depth; P039 establishes the diagnostic risk of collapsed aggregate tool scores. The fixed target source supplies the exact surrogate mismatch. Generic constrained RL supplies the slow dual operator. The narrow gap is the fixed-pipeline empirical effect of using explicit coverage control and chance exposure instead of the target reward.

## Baseline computation

For a query with a fixed BM25 ranking over N tools, the official target DQN starts at `K=1` and observes `[K/N, log2(K+1)/log2(N+1), current score, next score, their gap, standardized current score, current/top-score ratio]`. It contains no gold-dependent state. At STOP, target BoR-DQN receives `hit * -log2(K/N)` and otherwise receives zero, with continuation cost `0.01` and discount `0.95`. It never observes an explicit batch coverage requirement.

Pre-implementation source review proved that v013's local learned-policy rows cannot serve as this comparator: v013 exposed `found` in the state, used a different split, and differed on several training details. v019 therefore reproduces the target BFCL baseline in the same program, split, environment, seeds, and official 8,000-episode budget as the Candidate. This is the sole necessary baseline rerun.

## Changed computation

The Candidate keeps the official BFCL parser, ranking, `train_test_split(..., test_size=0.30, random_state=42)` split, score-only state, action, architecture, Adam learning rate `0.001`, replay size `50,000`, batch size `128`, episode count `8,000`, linear epsilon schedule `1.0 -> 0.05`, seeds, and maximum K fixed. It changes the training computation as follows:

1. At STOP, record success `h in {0,1}` and chance exposure `p=K/N` separately.
2. Recompute sampled terminal utility with the current slow variable: `u=lambda*h-p`; intermediate utility is zero and `gamma=1`.
3. Every 500 episodes, evaluate the greedy policy on the fixed training queries only; target-network copies remain every 500 environment steps as in the official code.
4. Update `lambda <- clip(lambda + 0.10*(0.90 - training_coverage), 0, 1)`.
5. Initialize `lambda=0.05`; never inspect Development-test outcomes during updates.
6. Freeze final network weights, `lambda`, every dual update, and all Development rows.

Recomputing utility from stored `(h,p)` avoids mixing rewards created under stale dual values. This is a direct implementation choice, not a general replay theorem.

## Closest-composition difference

The closest full pipeline is target BoR-DQN; the closest component is generic two-timescale constrained reward/cost learning. The Candidate's entire supported difference is their fixed composition on this tool-depth problem:

| Property | Target BoR-DQN | Candidate |
|---|---|---|
| Ranking/score-only state/action/network/data/seeds | official target components | identical |
| Terminal success term | `h * -log2(p)` | `lambda*h` |
| Exposure term | implicit inside success reward plus continuation cost | explicit `-p` for every terminal outcome |
| Coverage demand | none | fixed 0.90 training demand |
| Slow control | none | one scalar dual updated from training coverage |
| Test information | none | none |

The experiment identifies this objective bundle. It cannot attribute any gain separately to `gamma=1`, removing the continuation cost, or the slow dual.

## Minimal Claim Contract

If Development, untouched Confirmation, three independent Reviews, and the main-Codex decision all support it, the maximum claim is:

> On the two fixed BFCL simple protocols and the target paper's frozen BM25/DQN setup, explicit 0.90 training-coverage control over terminal chance exposure reduces mean shortlist size relative to the published success-weighted chance surrogate without a material loss in presented-gold coverage.

The claim does not cover argument accuracy, downstream LLM choice, tool execution, open-world retrieval, other retrievers, theoretical convergence, distribution-free coverage, or a first adaptive-depth/constrained-RL method.

## Implement contract

Files to create and freeze:

- `implementation_v019/program.py`
- `implementation_v019/audit.py`
- `implementation_v019/config.json`
- `implementation_v019/test_objective.py`

The Development command will use only the authoritative interpreter and frozen artifacts:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe program.py --phase development --config config.json --input BFCL_v3_simple.json --rank-bm25-wheel rank_bm25-0.2.2-py3-none-any.whl --output-dir <new output dir>
```

The independent audit is a separate entry point over raw outputs. Neither program may open the Confirmation URL or path during Development.

## Neutral comparators

- `target_bor_dqn`: same-run reproduction of the official BFCL target reward and training code.
- `target_f1_dqn`: same-run reproduction of the official BFCL `2/(K+1)` success reward and training code.
- `fixed_k`: `K in {1,3,5,10,20,50}` on the same official test split.
- `unconstrained_ratio_dqn`: same v019 code and budget, but slow ratio control without the 0.90 coverage residual; mechanism ablation only.
- `coverage_constrained_chance_dqn`: Candidate.

## Experiment contract

Development uses the exposed 400-line BFCL v3 simple file and the official deterministic 70/30 `train_test_split` from the target notebook. Primary paired outputs per seed are coverage, mean K, mean `K/N`, and defined aggregate BoR. The program also records per-query K/hit transitions, all dual histories, wall time, model weights, environment capture, and training-only coverage probes.

Development support requires all of the following as evidence for main-Codex judgment, not automatic promotion:

1. exact row, split, ranking, and comparator-hash integrity;
2. Candidate mean coverage no more than 0.01 below target BoR-DQN mean coverage;
3. Candidate mean K at least 1.0 lower than target BoR-DQN mean K;
4. Candidate mean defined BoR at least 0.25 bits higher than target BoR-DQN;
5. in at least two of three matched seeds, coverage loss is at most 0.025 and K is lower;
6. Candidate is not dominated in the `(coverage, mean K)` plane by a fixed-K or target comparator;
7. the unconstrained ratio ablation is reported even if it collapses to low coverage;
8. an independent audit recomputes every raw-row metric and slow update with maximum error `<=1e-12`.

No failed condition may be lowered or replaced after execution. Raw-case inspection must distinguish whether reduced K comes from preserving easy cases, abandoning hard cases, or a broad shift.

## Confirmation isolation and analysis unit

Only after a positive main-Codex Promotion Audit may the fixed Gorilla v4 live-simple file be acquired. Candidate, target, F1, fixed-K, and ratio-ablation weights/controls are applied without refitting. Confirmation is benchmark-version and live/non-live source separated but not a proof of task-family, template, or endpoint generalization. The paired analysis unit is one query; three seeds are repeated training realizations, not 360 independent tasks.

## Cost and bundle attribution

No LLM generation, token fee, external tool execution, or GPU training is used. The Candidate, ratio ablation, target BoR-DQN, and target F1-DQN each train three small CPU DQNs for the same official 8,000-episode budget. The two target comparators are rerun exactly once because the frozen v013 learned policies are invalid comparators. The output must report actual wall time and CPU/GPU environment. Any positive result is bundle-level.

## Risks and kill conditions

- The slow dual may oscillate or meet training coverage without transferring to Development.
- Defined BoR alone rewards low coverage; the Candidate is killed if it improves BoR by abandoning the coverage boundary.
- Reusing exposed v013 Development increases optional-stopping risk; only the fixed unread v4 file can confirm the claim.
- Three seeds and one BFCL category support only a narrow fixed-protocol claim.
- Failure of coverage preservation, chance-exposure reduction, independent recomputation, or comparator fairness freezes v019 and forbids Confirmation.
