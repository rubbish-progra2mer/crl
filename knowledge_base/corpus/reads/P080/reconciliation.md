# P080 Reconciliation

- Disposition: `LIMITED_ADMISSION_GOLD_SUPERVISED_SEARCH_DEPTH`
- Read 1 SHA-256: `e8a01968fbd69dd4c671b511ad47fdfabf6b4088012540fe150742d7ecff8c34`
- Accepted read-2: `read_2_attempts/r2-20260720-p080-a1/`
- Read-2 invocation SHA-256: `0982cd9a0e65d835c4fdd85a66ae1ed55c11c663c3e8d3c0f05fbfb1d0d68487`
- Read-2 report SHA-256: `cf9e958714a417fa24f4825ef5b4271ce246a4f2f07e90b48e4fbb22b9fe09ef`
- Accepted read-3: `read_3_attempts/r3-20260720-p080-a1/`
- Read-3 invocation SHA-256: `85c9e862fcb4f9e23e5736e9b4c4a1b34bb6a27aa41e879986dabd85fec1c54a`
- Read-3 report SHA-256: `537da8c7dc48edab010a02953b36795617160aa2ecd13c6afd2c41984efaafb8`
- Other attempts: none.

## Source reconciliation

- `AGREE`: each retrieval step generates an intermediate answer; training uses the first gold-exact-match step as a hindsight target and combines base, depth-efficiency and F1-improvement rewards.
- `NAME_NARROWED`: “self-answering” refers to answer generation, not correctness judgment. Minimal sufficient depth is identified by gold EM/F1 during training; deployment only executes a policy trained from this privileged signal.
- `FORMALISM_WARNING`: the paper sets unsuccessful trajectories to `t_c=-1` but elsewhere describes under-search as `t_c>T`; PDF-only evidence does not fully resolve the implementation branch.
- `CAUSAL_BOUNDARY`: early correctness may come from parametric memory, benchmark familiarity or question cues. No contamination audit or evidence-support test proves that retrieved evidence caused the intermediate answer.
- `DEPTH_BOUNDARY`: all diagnostic/prompt depths are zero through four searches. This does not validate long-horizon, branching or open-web Deep Research stopping.
- `COST_BOUNDARY`: average search depth and EM/search-step ratio omit eight-H20 PPO training, per-step intermediate answers, generated tokens, retrieval latency and amortization. Only proxy inference efficiency is supported.
- `BASELINE_BOUNDARY`: Search-R1, StepSearch and HiPRAG are compared, but matched training compute, tuning budget, repeated seeds, variance and several related efficiency methods are absent. Small per-dataset differences are not stable superiority evidence.
- `MEASUREMENT_WARNING`: the appendix table labelled OSR appears to repeat search-depth values; it is not used as Evidence.

## Frozen source role

Limited Operator source for gold-supervised hindsight search-depth shaping and Failure source for fixed-depth over/under-search. It must never be retrieved as an oracle-free stopping detector or proof of net deployment cost reduction.
