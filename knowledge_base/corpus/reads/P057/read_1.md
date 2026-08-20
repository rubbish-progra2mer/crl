# P057 first read — meta-agent code-space search

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Automated Design of Agentic Systems
- Authors: Shengran Hu, Cong Lu, Jeff Clune
- Venue: ICLR 2025
- Canonical ID: ICLR paper hash `36b7acf6f6010652b3f2a433774a66fe`; arXiv:2408.08435 v2
- PDF: `knowledge_base/staging/plan05_sat_a1/P057_adas.pdf`
- PDF SHA-256: `32eb1c1a6888e35fae0f618e33c58698b54d9c49bc063fef91ee591719fca376`
- Parse check: 34 pages, 117,671 extracted characters, zero empty pages

## Changed computation

Meta Agent Search gives a stronger LLM a small code framework and an archive of prior agent programs plus validation scores. Each iteration it proposes a named design and complete `forward()` implementation, performs two self-reflection passes for novelty/correctness, executes it on validation data, repairs runtime errors up to five times, then appends code and score to the archive. The search space includes prompts, loops, conditional control and compositions, rather than only graph edges or a fixed prompt.

## Evidence and closest baselines

The paper compares against CoT, self-consistency, Self-Refine, debate, step-back, role assignment, Quality-Diversity and OPRO under a shared framework. Search uses GPT-4o while candidate agents and baselines use GPT-3.5. On held-out textual DROP/MGSM/MMLU/GPQA subsets, selected searched agents outperform the reported hand-designed baselines, with the largest gaps on DROP and MGSM; top MGSM agents also transfer to GSM8K/GSM-Hard and sometimes textual non-math tasks. ARC is outside CRL's modality scope and is retained only as supporting evidence for code search.

## Fairness and measurement boundaries

- Search uses 25/30 candidate iterations, two mandatory meta-reflections, up to five code repairs, validation execution and a growing archive; one search/evaluation run costs about USD 500 on ARC or USD 300 on the textual domains. Final-agent inference cost is not matched to all baselines.
- Discovered winners frequently use more parallel samples, critics, refinements and ensembles than simple baselines. Performance therefore supports the whole searched program under its budget, not an isolated new primitive.
- The meta prompt explicitly asks for “interesting” and literature-inspired agents; its novelty check is self-judgment against the archive, not nearest-prior verification.
- Search optimizes a small validation subset (128 for most textual domains; 32 GPQA). The paper reports all discovered agents on held-out tests and then discusses top agents; this creates a test-inspection/selection ambiguity even though archive updates use validation metrics.
- Only single-step QA-like tasks are tested; multi-step tool/environment interaction and multi-objective cost/robustness optimization are future work.

## Draft knowledge objects

### Operator draft: `Archive-Conditioned Agent Program Search`

Generate full agent code conditioned on prior programs and measured validation outcomes; repair executable errors; retain each evaluated program as a stepping stone. The changed computation is broader than prompt or edge tuning, but its evidence is inseparable from strong meta-model and repeated evaluation access.

### Failure draft: `Agent Search Selects Token-Heavy Compositions Under Accuracy-Only Utility`

When the objective is only validation accuracy and cost is not constrained, code search tends to retain multi-sample/critic/refinement ensembles. A higher score is not evidence of a more efficient or genuinely novel mechanism without matched inference budget and nearest-prior analysis.

## Draft Evidence locators

- pp.3–5 and p.33: ADAS formulation and Meta Agent Search pseudocode.
- pp.6–11: textual results, transfer, safety and stated future limits.
- pp.21–22: exact meta/reflection/error-repair prompts.
- pp.29–30: textual split and baseline budgets; p.34: API search cost.

All claims remain draft until independent read and reconciliation.
