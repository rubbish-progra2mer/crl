# P026 first read — transition-level agent RL interface

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Agent Lightning: Train ANY AI Agents with Reinforcement Learning
- Authors: Xufang Luo, Yuge Zhang, Zhiyuan He, Zilong Wang, Siyun Zhao, Dongsheng Li, Luna K. Qiu, Yuqing Yang
- Venue/status: Microsoft Research technical report, arXiv:2508.03680 v1 (2025)
- PDF: `knowledge_base/staging/plan05_sat_a1/P026_agent_lightning.pdf`
- PDF SHA-256: `e223648a09b021785a46f60dd5ce13301622eca930ff91a5b45e971b53422561`
- Parse check: 20 pages, 77,051 extracted characters, zero empty pages

## Scope and admission boundary

The source is admitted for the agent-learning mechanism, not for its training platform breadth. The in-scope change is to observe arbitrary agent runs as component calls, extract only trainable LLM call transitions, assign episode return to those transitions, and train them with an existing single-turn RL objective. Server/client disaggregation and observability are implementation support, not a research Operator for CRL.

## Changed computation and information boundary

An agent execution is represented by states over semantic variables and ordered component calls. For a selected policy LLM, Agent Lightning extracts `(current rendered input, generated output, assigned reward)` for each invocation instead of concatenating the whole multi-turn trace with masks. LightningRL then performs hierarchical assignment: episode return to call-level transitions, followed by the ordinary token-level advantage/loss inside each response. In the published implementation every selected action receives the same final return; more discriminative credit assignment is future work. Optional AIR can add intermediate rewards from monitoring signals such as tool-call status, but these are developer-defined signals rather than learned causal credit.

## Evidence and results

- Text-to-SQL uses one Llama-3.2-3B model under three roles, jointly tuning SQL writing and rewriting, with final-answer correctness as reward.
- MuSiQue RAG uses gold-answer word F1 (0.9) plus a required-format reward (0.1).
- Calc-X tool use uses final answer correctness.
- Figures 5–7 report improving training and test reward curves, but the paper does not provide matched masking-vs-transition endpoint tables, statistical tests, token/rollout budgets, or an ablation of equal-return assignment versus alternative credit.

## Failure and fairness boundaries

- The title's “ANY” is an interface claim, not evidence that the same RL algorithm solves arbitrary long-horizon credit assignment.
- Equal episode return assigned to every LLM call can reinforce irrelevant or harmful intermediate decisions; AIR may reduce sparsity but can also encode hand-written proxies.
- RAG reward directly uses a gold answer; training success therefore does not establish reward-free self-improvement.
- Multi-LLM joint optimization is explicitly unresolved; independent per-model MDPs ignore coordination dependencies.
- Experiments use three application examples and one base model, without a matched multi-turn RL baseline or training-cost accounting.

## Draft knowledge objects

### Operator draft: `Agent-Trace Transition Decomposition`

Convert heterogeneous agent execution into per-LLM-call transitions with locally rendered context, then apply an existing single-turn RL optimizer after explicit call-level reward assignment. Predicted benefit is training compatibility and shorter samples, not inherently better causal credit.

### Failure draft: `Uniform Episode Return Does Not Identify Critical Agent Steps`

If every call receives the same terminal return, successful episodes reinforce all calls equally and failed episodes penalize all calls equally. This is a concrete limitation stated by the implementation and a strong baseline for P019/P027/P065-style step-credit methods.

## Draft Evidence locators

- pp.2, 4–9: state/call interface, MDP extraction and transition-level training.
- p.9: current identical final-return assignment and future high-level value function.
- pp.11–14: AIR and the three experiments/rewards.
- p.15: future work on long-horizon credit assignment.

All claims remain draft until independent read and reconciliation.
