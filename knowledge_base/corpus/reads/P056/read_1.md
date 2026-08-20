# P056 first read — optimizable agent graphs

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: GPTSwarm: Language Agents as Optimizable Graphs
- Authors: Mingchen Zhuge, Wenyi Wang, Louis Kirsch, Francesco Faccio, Dmitrii Khizbullin, Jürgen Schmidhuber
- Venue: ICML 2024, PMLR 235
- Canonical ID: PMLR:v235/zhuge24a
- PDF: `knowledge_base/staging/plan05_sat_a1/P056_gptswarm.pdf`
- PDF SHA-256: `63aab69835f124fd1bee714a21433a696c4d8d36da9f7883e0b5b01b836fd6ed`
- Parse check: 25 pages, 78,594 extracted characters, zero empty pages

## Changed computation

GPTSwarm encodes LLM/tool operations as nodes in a directed acyclic computation graph, composes agents by cross-agent edges, and exposes two optimization levels. Edge optimization assigns Bernoulli probabilities to feasible cross-agent edges and uses REINFORCE on task utility; node optimization updates each node prompt using its local input/output history while holding other prompts fixed. The meaningful Operator is not merely “use a graph,” but `execute candidate graph → measure task utility → update edge distribution/node prompts`.

## Closest baselines and evidence

- MMLU adversarial swarms test whether edge optimization suppresses deliberately harmful agents; the optimized 3T3A system scores 0.8301 versus DyLAN 0.8366, while using materially lower reported optimization/inference cost.
- Mini Crosswords combines fixed ToT, Reflexion and CoT agents. Ten REINFORCE steps improve mean best-state word accuracy from 0.465 to 0.575; a matched expected-edge-count random distribution reaches 0.510, so density alone does not explain the full gain. Applying node optimization later reaches 0.668.
- HumanEval node optimization raises reported online accuracy from 0.76 to 0.88, but uses problem-statement unit tests to label demonstrations.
- GAIA is a framework/application demonstration without graph optimization: seven ToT agents plus self-consistency improve accuracy but take about 415 seconds versus about 71 seconds for one ToT agent.

## Cost, oracle and generalization boundaries

- Mini Crosswords edge optimization with GPT-3.5 uses roughly 50.4M prompt and 13.5M completion tokens; the improvement is search-budget intensive even when inference edge count is controlled.
- The crossword utility chooses the best returned solution by word accuracy, and HumanEval uses included tests; these are task-specific evaluation signals, not generally available self-improvement feedback.
- Graphs are restricted to DAGs and optimize only potential cross-agent connections; internal topology changes, conditional/cyclic control and >100-agent robustness remain future work.
- GAIA gains largely track more agents/tools and are explicitly not evidence for node/edge optimization.

## Draft knowledge objects

### Operator draft: `Utility-Trained Agent Communication Graph`

Represent fixed operations/agents as a DAG, sample cross-agent connectivity from trainable edge probabilities, execute candidates on an explicit utility set, and update probabilities with REINFORCE. Node prompt updates are a separable secondary mechanism.

### Failure draft: `Workflow Search Can Hide a Large Evaluation Budget`

Reporting the final graph's edge count or inference cost does not account for millions of search-time tokens and repeated task scoring. Any workflow-optimization claim must separate discovery cost, selected-workflow inference cost and utility-oracle access.

## Draft Evidence locators

- pp.2–4: graph/edge/node definitions and algorithms.
- pp.5–8: MMLU, Mini Crosswords, HumanEval and GAIA results/boundaries.
- p.17: DyLAN/MAD comparison and cost; p.22: limitations; p.25: full resource table.

All claims remain draft until independent read and reconciliation.
