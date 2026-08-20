# Nearest Prior Work v013

## Search question

What is the nearest prior definition and implementation for Bits-over-Random under variable per-query shortlist depth, and has the difference between the aggregate definition and a mean success-weighted ceiling already been disclosed?

## Direct comparison

| Source | Core definition or computation | Exact overlap | Remaining v013 contribution |
|---|---|---|---|
| How Many Tools Should an LLM Agent See? A Chance-Corrected Answer, arXiv:2605.24660 | Defines `log2(P_obs/P_rand)`; trains adaptive-depth agents with zero-on-failure, ceiling-on-success reward; notebooks report the mean reward as “BoR bits” | Exact target data, policy family, reward, and reported statistic | Byte-level consistency audit, dual recomputation on identical rows, pairwise ordinal-reversal analysis, and untouched version confirmation |
| The 99% Success Paradox: When Near-Perfect Retrieval Equals Random Selection, arXiv:2605.18857 | Defines aggregate observed success over aggregate chance probability | Exact aggregate metric definition | Does not audit the adaptive-tool-selection notebook or its policy rankings |
| Official `bits-over-random` package, commit `746ef2466c24e0f810d2dde1b35db5c481949db6` | Computes `p_obs`, mean query-level `p_rand`, then `bits_over_random(p_obs, p_rand_mean)` and bootstraps the aggregate ratio | Exact reference implementation for the defined metric | Does not compare against the target notebook's success-weighted reward aggregation |
| AutoSearch (formal P080) | Learns task/model-dependent search depth from the earliest gold-correct intermediate answer | Adaptive-depth motivation and learned stopping | Different task, objective, and evaluation metric; no BoR consistency audit |
| ToolRerank and adjacent adaptive tool retrieval | Reorders or truncates visible tool menus | Same broad tool-selection setting | No identified audit of the target paper's two BoR computations |

## Collision judgment

- **Exact audit collision:** not found in the directly read fixed sources, exact-title searches, or official repository issue/PR records as of 2026-07-23.
- **Definition collision:** complete. Both the aggregate BoR definition and its correct implementation are prior work by the same author group.
- **Adaptive-policy collision:** complete. v013 cannot claim a new adaptive-K policy, a new BoR metric, or the first chance-corrected tool selector.
- **Surviving contribution:** a narrow reproducibility and measurement finding: the official adaptive-tool-selection notebook aggregates a different quantity under the BoR label, and the substitution can reverse policy rankings on fixed official protocols.
- **Novelty ceiling:** a focused metric-audit/technical-note claim, not a new learning algorithm.

## Fixed source bytes

| Path | SHA-256 |
|---|---|
| `sources_v013/how_many_tools_2605.24660.pdf` | `4DB89BFAC79BC90DD5B532D04AC1012ED1691657A45379BBBB2312682847164C` |
| `sources_v013/chance-corrected-tool-selection/notebooks/01_tool_selection_downstream_validation.ipynb` | `61DA53127597D7A90A440A87FF2EFCEA77665454852D50552DF9BB2972A6FF81` |
| `sources_v013/chance-corrected-tool-selection/results/downstream_results_bm25.json` | `8872DB7F8528560419AB74AAE8D1F268C193AECE3E670CC11F96B15C336EFB93` |
| `sources_v013/bits_over_random_2605.18857.pdf` | `8587A2502CF4F5FA371A04EACA3EEC4D782AD52D0A12F346606EE2FFD4B3EC02` |
| `sources_v013/bits-over-random/src/bor/audit.py` | `3DA2D063CCD78242686F54D3FDCD2E89A1E318BA20C6DAD4261F64552A8645C8` |
| `sources_v013/bits-over-random/src/bor/metrics.py` | `5D1E282B72B267314C8DA83B3FBA192D40FDD97A7FDB8D9D69943EAC34F6724D` |

## Forbidden novelty statements

v013 must not claim:

- invention of Bits-over-Random;
- invention of adaptive K or learned stopping;
- invalidity of the target paper's raw coverage, average K, or downstream LLM choice observations;
- superiority of aggregate BoR as a universal utility;
- absence of all prior private or unpublished critiques.
