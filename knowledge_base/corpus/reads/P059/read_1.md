# P059 first read — state-conditioned within-run orchestration

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Multi-Agent Collaboration via Evolving Orchestration
- Authors: anonymous/author list as printed in the source PDF
- Venue: arXiv preprint, 2025
- PDF: `knowledge_base/staging/plan05_sat_a1/P059_evolving_orchestration.pdf`
- PDF SHA-256: `244c86ebd95a9fa7ca06539854186ea3dcdbf794ceb6e7827fff6e642e647bf6`
- Parse check: 28 physical pages

## Changed computation

The method learns a central orchestration policy that selects one member from a fixed heterogeneous agent pool at each within-run step, conditioned on the current global state and task. Repeated selections allow cycles, so the serial policy induces a task-dependent dynamic collaboration graph rather than executing one frozen workflow. REINFORCE optimizes a terminal objective combining task quality with token/FLOP cost.

## Evidence and closest lineage

The closest line is static/manual multi-agent workflows → search-time workflow synthesis (P056–P058) → a learned within-run routing policy. Experiments use GSM-Hard, MMLU-Pro, SRDD and CommonGen-Hard with heterogeneous and homogeneous pools, and rerun AFlow/MacNet/EvoAgent baselines. The reported heterogeneous Titan system improves average quality, but the smaller Mimas configuration loses on some individual tasks despite a slight average gain.

## Measurement and fairness boundaries

- The policy chooses only among a fixed agent/tool pool; it does not discover new agent capabilities.
- Terminal reward is shared over a multi-step collaboration trace, so causal attribution to an individual activation remains coarse.
- The policy is initialized from a large reward-model checkpoint and trained on eight A800 GPUs; this training cost is not directly comparable to inference-search baselines.
- Default episode length four and the selected task suite leave longer or more asynchronous collaboration untested.
- Heterogeneity is not uniformly beneficial: the smaller configuration degrades on some reported tasks.

## Draft knowledge objects

### Operator draft: `State-Conditioned Within-Run Agent Orchestration`

At each collaboration step, condition a shared router on task plus accumulated global state and choose the next specialist, allowing revisits and task-dependent execution graphs while charging task utility and resource cost in one objective.

### Failure draft: `Terminal Collaboration Reward Blurs Useful Agent Activations`

A final team reward can distinguish successful trajectories but does not identify which specialist call caused the gain; with a fixed pool, the router may also learn benchmark-specific routing rather than a transferable collaboration rule.

## Draft Evidence locators

- Introduction and method overview: central policy, global state and evolving graph.
- Method/reward section: serial selection, terminal task-plus-cost reward and REINFORCE.
- Main result tables: heterogeneous versus homogeneous Titan/Mimas results and per-task regressions.
- Implementation/limitations: fixed pool, length, initialization and eight-A800 training budget.

All claims remain draft until independent read and reconciliation.
