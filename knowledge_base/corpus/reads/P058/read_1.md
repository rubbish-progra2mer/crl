# P058 first read — execution-feedback workflow tree search

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: AFlow: Automating Agentic Workflow Generation
- Authors: Jiayi Zhang et al.
- Venue: ICLR 2025
- Canonical ID: ICLR paper hash `5492ecbce4439401798dcd2c90be94cd`; arXiv:2410.10762 v4
- PDF: `knowledge_base/staging/plan05_sat_a1/P058_aflow.pdf`
- PDF SHA-256: `9be15f695f11dd5bc634c1c026bd2270eff3d3c4a53c4d9b51c012b7bd03d521`
- Parse check: 38 pages, 116,645 extracted characters, zero empty pages

## Changed computation

AFlow treats each MCTS node as a complete executable workflow. A stronger optimizer LLM selects a parent among top workflows, makes one code/prompt modification using predefined operators and stored parent experience, runs the child five times on a validation subset, and backpropagates its score plus modification outcome. Code edges allow loops/conditions; operators (generate, review/revise, ensemble, test, programmer) inject human priors. A blank-root selection probability preserves exploration.

## Evidence and closest lineage

The closest direct line is P056 GPTSwarm (probabilistic DAG edge search) → P057 ADAS (linear archive-conditioned code generation) → AFlow (tree-structured code-workflow search with execution feedback). On six split benchmarks, workflows searched with Claude-3.5-Sonnet and executed by GPT-4o-mini are compared to manual methods and ADAS, with AFlow reporting 80.3 average versus 67.2 for its ADAS implementation. Transfer across executor models is positive but model-specific workflows are often best. Removing predefined operators still yields an ensemble-like structure on GSM8K, but operators improve search efficiency.

## Measurement and fairness boundaries

- Search fixes model/temperature/format and primarily changes prompt plus code edges, so it is not unconstrained “all agent design.”
- Twenty iterations × five validation executions plus a separate optimizer model create material discovery cost; the headline Pareto plot reports selected-workflow test execution cost, not full search amortization.
- Validation data is first filtered for high-variance examples after five blank-workflow runs, changing the optimization distribution. Figure 5 plots both validation and test curves across iterations; the algorithm says selection uses validation, but repeated test visibility is a reporting/selection risk.
- Code tasks expose public example tests to the `Test` operator; gains support test-time verification with those cases, not hidden-test oracle access.
- Several best workflows mainly add multiple samples, ensembles, programmer execution or review. Their effect must be separated from extra calls/tokens in downstream claims.
- Open-ended idea-generation appendix uses GPT-4o scoring and eight iterations; it is not evidence that automated idea generation is scientifically valid and is outside CRL's use of AFlow as a nearest-prior baseline.

## Draft knowledge objects

### Operator draft: `Execution-Feedback Tree Search over Agent Programs`

Store complete executable workflows as tree nodes; propose local code/prompt modifications; evaluate each child repeatedly; propagate modification outcome and score to guide later parent selection while retaining blank-root exploration.

### Failure draft: `Final-Workflow Pareto Can Omit Discovery Cost`

A cheaper selected workflow can require an expensive optimizer plus repeated validation executions to discover. Claims must report search cost, amortization horizon and selected-workflow inference cost separately.

## Draft Evidence locators

- pp.4–7 and p.19: search space, MCTS cycle and pseudocode.
- pp.8–10: six-dataset results, model transfer, cost framing and ablation.
- p.18: public-test operator boundary; p.30: inference-only cost table.
- pp.35–37: open-ended evaluator appendix and its narrow evidence status.

All claims remain draft until independent read and reconciliation.
