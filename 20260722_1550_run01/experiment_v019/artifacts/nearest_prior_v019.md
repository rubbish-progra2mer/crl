# Main Codex Nearest Prior Record v019

## Pre-Development commitment

This record was written before any v019 model training or metric output. It may be extended with source-hash readback before Review, but its comparator identities and collision judgments may not be changed after Development to rescue an outcome.

## Search views

1. **Changed computation:** optimize expected success relative to expected retrieval exposure, and enforce a coverage requirement, without using the Candidate's name.
2. **Key components:** ratio maximization, two-timescale reward-minus-cost learning, constrained accuracy/cost control, and adaptive stopping.
3. **Full pipeline:** query -> fixed tool ranking -> sequential STOP/CONTINUE policy -> shortlist -> presented-gold coverage and exposure.
4. **Composition and runnable baseline:** target official repository/notebook, fixed target DQN artifacts, generic cost-aware RL, and recent offline adaptive-retrieval implementations.

## Exact bounded searches

Executed on 2026-07-24 against primary paper or official proceedings sources:

- `Dinkelbach adaptive retrieval policy reward ratio tool selection`
- `fractional programming adaptive retrieval depth LLM tools`
- `chance-corrected tool retrieval policy Dinkelbach`
- `adaptive top-k retrieval policy success cost objective`
- `CARVI Q-learning`
- `Cost-Aware Actor-Critic Suttle`
- `conformal adaptive retrieval top k coverage guarantee`

The search found generic ratio RL, fixed-penalty cost-aware retrieval, conformal coverage methods, heuristic adaptive-k, AutoSearch, and the exact target BoR-DQN. No source found in this bounded audit reports the exact fixed target pipeline with a 0.90 coverage dual over terminal chance exposure. This is not proof of universal novelty.

## Component collisions

| Source | Existing component | Collision status |
|---|---|---|
| Suttle et al., ICML 2021 | Two-timescale ratio RL using an auxiliary `reward - rho*cost` MDP | Complete collision with claiming ratio optimization or the slow reward/cost transform as new |
| Generic constrained MDP/RL | Lagrange dual control of a reward/cost constraint | Complete collision with claiming coverage-dual mathematics as new |
| Conformal prediction sets | Coverage-controlled variable-size sets | Component collision with broad coverage-guaranteed set-size claims; v019 supplies no distribution-free guarantee |
| Adaptive-k / AutoSearch | Query-dependent depth from score patterns or supervised earliest success | Collision with claiming the first adaptive depth policy |

## Composition collisions

- The target paper combines BM25 rankings, a seven-feature sequential state, a small binary DQN, fixed-K baselines, and success-dependent chance reward. It does not optimize the aggregate ratio or impose explicit coverage control.
- Offline RL for Adaptive Policy Retrieval combines learned stopping with explicit correctness and step cost, and reports a Pareto frontier. It uses a different medical evidence simulator, fixed scalar penalties, and CQL/IQL/DPO rather than chance exposure with a target-coverage dual.
- Cost-aware ratio RL supplies the mathematical inner computation but not the BFCL tool-depth data flow, target state, coverage demand, or frozen target comparator.

## Full-pipeline collision judgment

No complete collision was found for the narrow empirical pipeline. The remaining difference is not a new neural architecture: it is replacing the target's non-equivalent per-query reward by terminal chance exposure under explicit training coverage control, while holding ranking, state, action, network, split, and seeds fixed.

## Comparator roles and relative differences

- **Official target BoR-DQN reproduction:** closest runnable full-pipeline comparator; it must use the score-only official state and be trained once inside v019 because v013's learned-policy reproduction leaked gold state and used a different split/protocol.
- **Official target F1-DQN reproduction:** same official architecture, state, budget, split, and target continuation cost with the paper's `2/(K+1)` success reward.
- **Fixed-K policies:** analytic coverage/exposure controls on the identical official test split.
- **Unconstrained ratio DQN:** mechanism ablation showing what happens when the coverage constraint is removed.
- **Offline PA retrieval RL:** adjacent pipeline evidence, not a byte-compatible comparator on BFCL.

## Source bindings

| Source | Path | SHA-256 |
|---|---|---|
| How Many Tools Should an LLM Agent See? | `sources_v013/how_many_tools_2605.24660.pdf` | `4DB89BFAC79BC90DD5B532D04AC1012ED1691657A45379BBBB2312682847164C` |
| The 99% Success Paradox | `sources_v013/bits_over_random_2605.18857.pdf` | `8587A2502CF4F5FA371A04EACA3EEC4D782AD52D0A12F346606EE2FFD4B3EC02` |
| Reinforcement Learning for Cost-Aware MDPs | `sources_v019/ratio_rl_icml2021.pdf` | `949FE7D0D8137A6EF1190BFCA17F258603602AC881D8F99F04D1B720C71DA877` |
| Offline RL for Adaptive Policy Retrieval | `sources_v019/offline_adaptive_retrieval_2604.05125.pdf` | `357EC6826E8C4032D9F807CC31440E5BFE47F4B4003C22EF698A4EB85469122F` |
| Target official repository | `sources_v013/chance-corrected-tool-selection/` | commit `9759eb9f0e7ed90ff289d34300acc15453f7851a` |

## Closest-composition conclusion

The closest composition is the fixed target DQN plus the generic two-timescale constrained reward/cost transform. Both must be visible to Review. v019 may support only a narrow empirical claim on the two fixed BFCL protocols; it may not claim new constrained-RL theory, a general optimal tool policy, or downstream execution gains.
