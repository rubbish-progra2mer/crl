# P063 first read — dynamic note linking and evolution

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: A-Mem: Agentic Memory for LLM Agents
- Authors: Wujiang Xu et al.
- Venue: NeurIPS 2025 / arXiv:2502.12110 v11
- PDF: `knowledge_base/staging/plan05_sat_a1/P063_a_mem.pdf`
- PDF SHA-256: `fec32b521c4a1f793442bf1aeb26139c583078350d1cd4ab8f4eccc54a0694f0`
- Parse check: 28 physical pages

## Changed computation

A-MEM converts each interaction into an atomic note with LLM-generated context, keywords and tags plus a dense embedding. It retrieves nearest historical notes, asks an LLM to create semantic links, and may rewrite context/keywords/tags of earlier notes when a new note arrives. Query-time dense retrieval then supplies relevant memories to the agent.

## Evidence and closest lineage

On LoCoMo and DialSim, A-MEM is compared with LoCoMo full context, ReadAgent, MemoryBank and MemGPT across six foundation models. Removing link generation and memory evolution sharply reduces performance; retaining links without evolution is intermediate. Results are strongest on multi-hop and temporal categories, with much shorter answer context than full-context baselines.

## Measurement and fairness boundaries

- Note construction, linking and evolution all depend on the underlying LLM; the authors explicitly identify this as a limitation.
- The main ablation removes link generation and evolution together before adding link generation back, but does not cleanly isolate enriched note construction from all other changes.
- Retrieval parameter k is adjusted by category; larger k often improves performance and therefore changes context budget.
- No error bars are reported because API repetitions were considered costly.
- Method text says old memories are replaced after evolution; provenance and protection against incorrect rewrites are not evaluated.
- The formal retrieval equation lists dense top-k notes, while the architecture description also says linked memories are automatically accessed; exact query-time contribution of links needs implementation-level verification.

## Draft knowledge objects

### Operator draft: `LLM-Constructed Memory Notes with Dynamic Linking and Evolution`

Enrich each atomic experience with generated semantic attributes, retrieve nearby notes, create content-dependent links, and revise older note representations when new evidence changes their context.

### Failure draft: `Dynamic Memory Organization Inherits Generator Error`

When the same LLM creates semantic attributes, links and historical rewrites, incorrect interpretations can alter future retrieval; the paper reports dependence on backbone quality and does not test provenance-preserving rollback.

## Draft Evidence locators

- pp.1–5: note schema, link generation, memory evolution and retrieval equations.
- pp.6–9: main results, ablations, k sensitivity, cost/scaling analysis and stated limitation.
- p.25 checklist: no statistical-significance runs because of API cost.

All claims remain draft until independent read and reconciliation.
