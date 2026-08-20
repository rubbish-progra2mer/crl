# Research Problem

## User intent

Controlled Commissioning run02, v004. User directive: continue
autonomously until the machine genuinely delivers; review every failure
round for machine defects.

## PROCESS DEVIATION DISCLOSURE

The v004 K11 falsifier was executed BEFORE this problem document was
frozen (Main Codex ordering violation under momentum; W bucket was
already exposed workbench so no data-role contamination occurred, but
the Knowledge-to-Implement ordering was violated). Recorded as machine
observation MD-10: the machine has no mechanical checkpoint preventing
experiment-before-problem ordering; discipline rests on Main Codex
self-control. This document was written after K11's kill and after two
mechanism-attribution checks; it records the resulting state honestly
rather than pretending prospective framing.

## Occupancy scan before problem commitment

Inherited from v003 (all staleness-repair nodes occupied or dead) plus
v004 probes: learned relevance/recency balancing (Re3 2509.01306),
query-intent temporal overlays (LongEval 2607.04088), LLM temporal
extraction (Chronos 2603.16862, Mem0 temporal reasoning), trained memory
rerankers (MemReranker 2605.06132). The zero-training, zero-extraction,
retrieval-set-conditioned node was open; K11 tested it and killed it.

## Use Thesis and real consumer

Memory-system builders deciding WHERE to spend staleness defenses:
retrieval-layer heuristics vs write-side structure vs LLM gating. The
v002-v004 chain now shows cheap retrieval-layer fixes are systematically
ineffective, and localizes why. The consumer decision this changes:
stop investing in retrieval-layer staleness patches for schema-free
conversational memory; the binding constraint is representation-level
(query-initial-statement phrasing isomorphism), with chunk dilution a
secondary, granularity-addressable factor.

## Decision interface (v004 outcome shape)

v004 closes kernel-wise (K11 dead) but converts the accumulated evidence
into a candidate MEASUREMENT/ATTRIBUTION contribution for v005:
a causal decomposition of stale bias in schema-free memory retrieval,
with preregistered D-bucket verification and an end-task reader arm.

## Mechanism Demand / carrier-independent statement

Established first-hand (W bucket, five experiments): in conversational
memory with updated facts, retrieval-layer stale bias decomposes into
(1) phrasing isomorphism between queries and initial statements
(dominant; survives sentence-level indexing), (2) chunk dilution of
update statements embedded in long multi-topic turns (secondary;
removed by sentence-level units: inversions 9->7, margin -0.064->+0.011),
(3) graph propagation (no contribution). Carrier-independent: the
decomposition method (paired stale/current best-unit analysis under
unit-granularity and scoring-arm ablations) applies to any timestamped
memory store with update annotations.

## Cost authorization

Unchanged (deepseek preauthorized; local otherwise).
