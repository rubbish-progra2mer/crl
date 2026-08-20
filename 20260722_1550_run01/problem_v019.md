# Research Problem v019

## User intent

Produce one real, reviewable research implement inside the commissioning Run. The implement must change a material decision computation, execute on real frozen bytes, survive untouched Confirmation and three independent Reviews, and remain narrow enough for a small experiment.

## Text/tool LLM Agent scope

The scope is the retrieval stage immediately before an LLM receives a shortlist of candidate tools. For each real BFCL request, a fixed BM25 scorer ranks a fixed registry and a small policy decides when to stop exposing additional tools. The measured outcome is whether the gold tool is presented, together with the number of tools exposed. Argument generation, execution correctness, stateful task success, and open-world tool discovery are outside the claim.

## Research question

Can an unchanged small STOP/CONTINUE DQN reduce random shortlist exposure `K/N` while preserving a fixed coverage demand, when its terminal utility is controlled by a slow coverage dual rather than the published success-weighted per-query BoR surrogate?

## Soft constraints

- Reproduce the official target BFCL parser, BM25 ranking, score-only seven-state features, `train_test_split` split, network architecture, and seeds.
- Use the shared Python 3.11.15 environment and no paid API.
- Rerun the target baseline exactly once because source review found that v013's local learned-policy state leaked the gold-found flag and did not match the official split or training protocol.
- Keep the experiment CPU-sized and use only the minimum mechanism ablation needed to test the coverage constraint.

## Hard exclusions

- Do not claim new ratio-RL, constrained-RL, DQN, BM25, or adaptive-retrieval mathematics.
- Do not optimize, inspect, download, or tune on Confirmation before Development promotion.
- Do not use aggregate BoR alone as a utility claim; fixed `K=1` already demonstrates that high selectivity can coexist with inadequate coverage.
- Do not change v013 gates, reuse its failed disposition as positive evidence, or claim the target paper's downstream tool-choice result is disproved.
- Do not add a framework, environment router, state machine, defensive compatibility layer, or non-Reviewer subagent.

## Cost authorization

No paid API or external credential is authorized or needed. Development is limited to local CPU/PyTorch execution in `D:\Desktop\crl\crl_agent_v3\.venv\python.exe`.
