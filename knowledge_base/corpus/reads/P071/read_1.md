# P071 first read — reusable plan-template memory

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents
- Authors: Qizheng Zhang et al.
- Venue: NeurIPS 2025; arXiv:2506.14852 v2
- PDF: `knowledge_base/staging/plan05_sat_a1/P071_agentic_plan_caching.pdf`
- PDF SHA-256: `af2ec5f2b4431048ef71d4e090a43a6e9ed9104bcba6dd6d0826c8e26cbc3c8a`
- Parse check: 27 physical pages

## Changed computation

APC extracts a context-independent structured plan template and high-level keyword from a successful Plan-Act trace. Exact keyword matches retrieve a template; a smaller planner adapts it to the current external context, while misses use the large planner and add a filtered template afterward. It caches the transformation pattern, not the final answer or raw history.

## Evidence and closest lineage

Across FinanceBench, TabMWP, QASPER, AIME and GAIA/Open Deep Research, APC reports 50.31% average cost and 27.28% latency reduction while retaining 96.61% of the accuracy-optimal baseline. It beats semantic and full-history caching on accuracy/cost; cache-hit accuracy remains stable in the reported primary tasks. On GAIA it reduces cost 76.42% with a 0.61-point accuracy drop.

## Measurement and fairness boundaries

- Template generation is admitted only after an execution is judged correct; the judge or reference answer is therefore an important quality dependency.
- Exact keyword matching protects precision but misses semantically related formulations; fuzzy matching improves hit rate while reducing accuracy.
- Benefits depend on repeated task structure. GAIA's heterogeneous requests produce fewer initial hits, and dynamic workloads weaken the mechanism.
- The evaluation uses paid API models and GPT-4o judging; reported dollar savings depend on those prices and model assignments.
- The primary architecture is sequential two-stage Plan-Act; multi-agent cache consistency is untested.

## Draft knowledge objects

### Operator draft: `Context-Independent Plan Template Reuse`

Extract the invariant plan skeleton from a successful trace, index it by task intent, and adapt it with a cheaper model to new context instead of reusing a data-dependent answer or replaying the whole history.

### Failure draft: `Aggressive Plan Matching Trades Cost for Semantic Drift`

Looser cache matching creates more hits and lower cost but can apply a superficially similar plan to a materially different task, reducing accuracy; heterogeneous tasks also leave the cache cold.

## Draft Evidence locators

- pp.1–6: plan-template extraction, keyword matching, adaptation and raw-history boundary.
- pp.6–10: five-workload results, cache-hit accuracy, overhead, fuzzy-match trade-off and cold start.
- pp.23–27: API/model setup, sensitivity and explicit dynamic/multi-agent limits.

All claims remain draft until independent read and reconciliation.
