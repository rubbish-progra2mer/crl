# P068 first read — evidence-backed audit before scoring

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality
- Authors: Yukun Huang et al.
- Venue: ACL 2026 long paper
- PDF: `knowledge_base/staging/plan05_sat_a1/P068_deepfact.pdf`
- PDF SHA-256: `a26aeaefd0f1c763a40c1383c3a18ac723629519f6089abcdfe85ad74057f079`
- Parse check: 31 physical pages

## Changed computation

Audit-then-Score treats expert benchmark labels and rationales as revisable. A verifier that disagrees must submit a stronger evidence-backed verdict; an independent auditor compares it with the incumbent rationale; only accepted challenges update a versioned benchmark before the challenger is scored. DeepFact-Eval complements this with breadth-first source search followed by targeted document-level questioning for claim-critical details.

## Evidence and closest lineage

PhD specialists achieve only 60.8% on hidden known-answer micro-golds when labeling alone. Across three evidence-backed audit rounds, benchmark micro-gold accuracy rises to 90.9%; harmful human flips are rare. On the frozen v4 snapshot, DeepFact-Eval reaches 83.4%, above traditional snippet checkers and general deep-research agents, while grouped verification trades some accuracy for much lower cost.

## Measurement and fairness boundaries

- Micro-golds are 25% of annotation items with a 1:4 supported-to-unsupported ratio and many manually injected errors; they measure particular factual blind spots, not all scientific truth.
- DeepFact-Eval uses costly iterative retrieval (about 516.9K input tokens and $1.16 per claim under the reported GPT-4.1 setup).
- Auditing consolidates evidence already found; the paper notes that stronger verifiers are still needed to expand the evidence frontier.
- Literature verification cannot resolve claims requiring new experiments or simulations.
- The benchmark's versioning machinery is an evaluation method, not a template for turning CRL into a workflow engine.

## Draft knowledge objects

### Operator draft: `Evidence-Backed Audit-then-Score`

When a verifier conflicts with a difficult gold label, require a sourced competing rationale and let an independent auditor adjudicate the two before scoring, preserving the original unless the challenge is stronger.

### Failure draft: `One-Shot Expert Gold Is Brittle for Deep Research Claims`

Domain expertise alone does not prevent missed qualifiers, source conflation or overlooked counter-evidence in long claim verification; agreement or authority is not a substitute for an auditable rationale.

## Draft Evidence locators

- pp.1–5: expert micro-gold study, AtS protocol and versioned benchmark.
- pp.6–9: audit trajectories, cost, verifier comparison and external-benchmark disagreement audits.
- p.10: experiment/literature boundary and expense limitation.
- pp.27–31: observed deep-research error cases and taxonomy.

All claims remain draft until independent read and reconciliation.
