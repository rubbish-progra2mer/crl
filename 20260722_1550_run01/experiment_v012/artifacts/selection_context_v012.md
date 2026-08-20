# v012 Selection Context

## Recovery boundary

- Run: `20260722_1550_run01`
- System state at recovery: `DEVELOPMENT_NOT_COMMISSIONED`
- Run state at recovery: `ACTIVE`
- Previous durable result: `experiment_v011/result.md`
- Previous result SHA-256: `2C7663E3154C28D1074776B84A8C51B55E797228C71EC2EECF8444D360AF45FB`
- v012 began with no Candidate, implementation, Experiment Plan, Development capture, Confirmation data, Review Packet, Reviewer report, Decision, or Delivery.
- v009 and v011 already exposed the P084 Development bundle. v012 does not use that bundle, does not retune TPPA, and does not retune residual or anchor features.

## Knowledge-base entry search

The main Codex executed the required Failure, Operator, and Paper Card queries before choosing a candidate. The relevant formal Cards were:

- `failure-confident-completion-without-state-success`
- `failure-incomplete-tool-contracts-false-verified-state`
- `operator-terminal-state-reliability-evaluation`
- `operator-contract-gated-tool-state-commit`
- `operator-evidence-audit-before-score`
- `paper-tau-bench`
- `paper-p037` (ToolSandbox)
- `paper-p085` (ToolRet)
- `paper-p088` (joint neural nearest-neighbour retrieval)

These Cards motivate the distinction between a successful verifier/reward and a real task-state transition. They do not establish the v012 method or its empirical performance.

## Open-network nearest-prior audit

The main Codex directly read the following fixed PDFs:

| Source | Local path | SHA-256 | Directly relevant finding |
|---|---|---|---|
| Cheap Reward Hacking Detection | `sources_v012/cheap_reward_hacking_2606.08893.pdf` | `C5FD945125B1B6CD4739B2AACF150156BBFC8E47AFF2D7240EA05ED697075CE0` | Terminal Wrench uses task-disjoint evaluation. A separately trained stripped-trajectory encoder retains action-surface signal but is substantially weaker than the full sanitized encoder: reported AUC `0.7631`, TPR@5%FPR `0.2275`. |
| Praetor: Enforcing Benign Trajectories | `sources_v012/praetor_2604.26274.pdf` | `842D593F53486481D384C8407D2FD688BBFBF90B69E505DB54BC31008A15AA98` | Learns pDFA-style guards from verified benign structured tool-call telemetry, including sequence and parameter constraints; the paper states limitations for open/unstructured workflows and synonymous actions. |
| Terminal Wrench | `sources_v012/terminal_wrench_2604.17596.pdf` | `140DF68E633BCB5544E37B67A6F362A917F7A38B566B25E1B42FE86BEB619E8A` | Provides real terminal-agent tasks and paired successful baseline/reward-hacking trajectories, including reasoning-stripped variants. |
| TRACE | `sources_v012/trace_2601.20103.pdf` | `98A3121DE46018F08F47A8DB18B4ED55C9D117BEB5E984EAA9F3C2A47F3A5649` | Uses contrastive LLM analysis on a curated synthetic trajectory benchmark; it does not evaluate the proposed deterministic reference-conditioned shell-effect representation. |

Repository identity was checked with:

```text
git ls-remote https://github.com/few-sh/terminal-wrench.git HEAD
```

Observed HEAD: `d8a29613235a0ef56a8b70b3142626a533da28c2`.

## Rejected v012 routes

1. **Weakest-positive retrieval loss** was rejected before implementation. P088 already applies a soft-min over positives and a softmax over negatives to optimize the weakest positive coefficient. JointLH/SumMargLH/LSEPair and differentiable SoftTop-k provide further direct collisions.
2. **Query decomposition or dynamic top-k for ToolRet** was rejected before implementation because ToolQP, LANCER, and MagicSelector already cover the relevant computation family, while v009/v011 had already exhausted nearby P084 retrieval adaptations.
3. **A fixed-workflow state machine** was rejected because it would reproduce Praetor's structured-workflow premise and would not address open shell trajectories.
4. **A terminal-state verifier trained without real trajectories** was rejected because no untouched real trajectory bytes were then available; fixture sanity is forbidden as research or Delivery evidence.

## Selection-only exposure and untouched boundary

- During selection, the main Codex read only task `1012` metadata plus one stripped hack (`claude-opus-4.6/v5`) and one successful baseline (`claude-opus-4.6/1`).
- `SHA256("1012")[0] mod 4 = 2`; therefore task `1012` is assigned to Development.
- Its second SHA-256 byte modulo five equals `4`, which would otherwise place it in the held-out Development test. Because its bytes were inspected during selection, every ID in `selection_exposed_task_ids` is prospectively forced into the training partition before any metric is produced.
- Development uses bucket `2`.
- Confirmation is prospectively fixed to bucket `3`.
- No bucket-3 task metadata or trajectory content was read during selection.
- Confirmation acquisition is forbidden until Development passes every preregistered gate and the main Codex records a Promotion Audit.

## Selected computation

The selected candidate is **Reference-Conditioned Effect Delta (RCED)**: for each task, reserve one deterministic successful trajectory as a non-evaluated reference, then add ordered executable/effect/path/dataflow deltas from the evaluated trajectory to that reference. The primary comparison holds labels, task split, action-only text, learner family, and threshold protocol fixed; only the reference-conditioned structured computation is added.
