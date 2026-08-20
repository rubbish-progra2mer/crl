<!-- crl-v3-evidence-ids
["ev-p010-long-history-decline","ev-p011-failure-core","ev-p084-expanded-toolkit-controlled-setting"]
-->
# Research Map

## Observed Failure and boundary

- [AUTHOR_FACT] Reading the full interaction history instead of oracle
  evidence sessions costs 30-60 percent accuracy on long-history memory QA;
  oracle retrieval is the upper-bound control.
  [[evidence:ev-p010-long-history-decline]]
- [AUTHOR_FACT] Turn-, session-, and summary-level memory units exhibit
  distinct retrieval and semantic-quality failures; no single fixed unit is
  adequate. [[evidence:ev-p011-failure-core]]
- [AUTHOR_FACT] Expanding a toolkit with semantically related tools
  degrades function-calling accuracy in a controlled setting; distractor
  proximity is directly harmful. [[evidence:ev-p084-expanded-toolkit-controlled-setting]]
- [CODEX_SYNTHESIS] Both failures share one structure: a retrieval-stage
  decision (unit granularity / menu width) is fixed globally while the
  per-query optimum varies, so any fixed choice is mismatched for part of
  the load.
- [CODEX_HYPOTHESIS] Query-conditioned allocation of the fixed retrieval
  budget could dominate every fixed choice on mixed loads (this hypothesis
  drove kernel formation below; see probe outcomes).

## Intervention stage

Memory read path (unit selection at query arrival) for the memory framing;
tool-menu construction after tool retrieval for the tool framing. Both read
the query plus a pre-built store; both output the unit set handed to the
downstream decision computation.

## Use Thesis, Value Bridge and Mechanism Demand

Bound to problem_v001.md (SHA 2b25b5d22a4bb8176ad6787e1bcc2c2a29c9acd23c
594323262d7b731ed426ff): builders of long-horizon agents with persistent
memory; decision interface at the memory read path; Value Bridge through
the oracle-retrieval evidence; Mechanism Demand fixed carrier-independently
before any Promotion carrier outcome was read. No Promotion carrier outcome
has been read in this version.

## Operator shortlist and source recheck

Three formal card queries were executed on 2026-07-26 (failure / operator /
paper kinds; queries generated from the Problem and Mechanism Demand, no
candidate-invented names). Top hits and readings:

- failure-memory-unit-granularity-mismatch (P011), failure-long-history-
  reading-overload (P010): the target failures.
- operator-subtask-compute-allocation (P020): allocate budget across
  stages by sensitivity; cross-cluster source of the allocation structure.
- operator-gold-supervised-hindsight-search-depth (P080): adaptive depth
  by query; same allocation family, training-side.
- operator-memory-stage-decomposition (P010): index/retrieve/read stage
  separation; justifies retrieval-stage metrics with reading-stage limits.

Lineage-chain position (CORPUS_REPORT section 5, memory cluster): MemGPT
paging -> LongMemEval stage decomposition -> SeCom topical construction ->
ExpeL insight ops -> Memory-R1 learned CRUD -> STALE adjudicated state.
Natural next step along the chain: read-time query-conditioned unit
selection. Why it has not been done inside the formal corpus: no Failure
Card excludes it; the corpus (frozen 2026-07-20) simply predates the
external work that, as the probes below show, has already done it.

Cross-cluster probe (formal): the allocation structure of P020/P080
(efficiency / test-time-search clusters) shares the decision-variable type
"budget split conditioned on input features" with the memory-cluster and
tool-cluster fixed-choice failures. Probe hit accepted as a generation
channel; two kernels below came from it.

## Competing method kernels

K1 - Query-conditioned granularity allocation at memory read time.
  Carrier-independent statement: at read time, allocate a fixed retrieval
  budget across coexisting granularities of the same history, conditioned
  on query features available at query arrival. Generation channel:
  lineage extrapolation + cross-cluster probe (P020 allocation onto
  P010/P011 failures). Cheap novelty probe (2026-07-26, open web):
  DIRECT FULL-PIPELINE COLLISION.
  - MemGAS (arXiv:2505.19549v2, read directly; local PDF SHA-256
    256eba2430611820eb4b18978fdd35f05a3bcf26c7b808b03ef0971ab3bc49c8):
    maintains turn/session/summary/keyword granularities, GMM-based
    cross-granularity association, an entropy-based router that
    adaptively selects granularity per query, plus LLM filtering;
    evaluated on four long-term memory benchmarks including retrieval
    metrics. Same causal node (read-time unit selection), same decision
    variable (per-query granularity), same information timing (query
    arrival). Any budget-split or router-feature variant is the same
    family under CRL's substantive-difference test.
  - Mix-of-Granularity (arXiv:2406.00456, COLING 2025): the same router
    computation for static-document RAG; establishes the pattern is not
    memory-specific either.
  Disposition: KILL.

K2 - Construction-time adaptive segmentation (write-side).
  Generation channel: lineage extrapolation. Probe: SeCom (P011) already
  owns topical construction granularity; RAPTOR / MemTree own hierarchical
  multi-scale construction. Remaining delta would be prompt/feature-level.
  Disposition: KILL (same family as incumbents).

K3 - Post-retrieval unit reshaping (retrieve fine, expand to parent).
  Probe: auto-merging / parent-document retrievers are established
  engineering practice in mainstream RAG frameworks; no substantive
  causal-node difference. Disposition: KILL.

K4 - Query-conditioned tool-menu width (cross-cluster transfer of the
  same allocation structure onto P084/P085 menu failures).
  Carrier-independent statement: after tool retrieval, choose the menu
  size/composition per query from predicted tool-need set size, under an
  equal average-menu-token budget. Cheap novelty probe (2026-07-26):
  DIRECT COLLISION with "How Many Tools Should an LLM Agent See? A
  Chance-Corrected Answer" (arXiv:2605.24660, 2026), which studies
  exactly the per-query tool-list size question and reports downstream
  validation of shorter adaptive lists (93.1 vs 87.1 percent), plus
  Toolshed / MemTool / DTDR occupying adjacent nodes.
  Disposition: KILL.

## Natural-language disposition

All four kernels are killed by pre-freeze probes, not by workbench
experiments: K1 and K4 by direct external collisions read at first hand
(MemGAS PDF; 2605.24660 abstract and results section via web), K2 and K3
by incumbent occupation already documented in the corpus and mainstream
practice. No kernel reached the workbench-falsifier stage, so no data
role was consumed: WORKBENCH, PROMOTION_DEVELOPMENT and CONFIRMATION
remain untouched for every candidate dataset considered (LongMemEval was
never downloaded; no outcome of any carrier was read).

Meta-observation recorded for future versions: the family "query-
conditioned allocation of a fixed retrieval/compute budget" has been
systematically mined across 2024-2026 (granularity: MemGAS/MoG; retrieval
strategy: Adaptive-RAG; menu width: 2605.24660; search depth: P080).
Lineage extrapolation and cross-cluster structure transfer, when the
shared structure is this allocation pattern, should be treated as
high-collision-risk generation channels until the corpus is refreshed
past 2026-07.

## Family Viability

The problem family "fixed retrieval-stage choice vs per-query optimum"
is externally saturated at every causal node reachable with local-only
resources (write-side, read-side, post-retrieval, tool-menu). This is not
an execution failure and no fair comparator absorbed a delta in our own
experiments; the family is closed by prior occupation. Continuing the
family would require either (a) a genuinely different causal node, for
which no evidence-backed route was found in the current corpus, or (b) a
measurement-only critique of the incumbents, which CRL's v007-class
precedent (run01, publicly recorded in decision text as insufficient for
delivery) rules out as a seed. RESET Problem/family.

The binding constraint on the reset is resource-shaped: with no paid API
(RUN_CHARTER preauthorization NONE), viable problems must have public
annotated outcome variables and local-encoder-scale computation. Both
probe-killed kernels had such carriers; the surviving problem space after
their exclusion is narrow. The Main Codex judges the expected value of a
third local-only problem search to be low relative to unblocking the
space that requires real LLM rollouts (agent-behavior mechanisms, fresh
self-generated confirmation data), which requires paid API authorization.

## Candidate Promotion Audit

Not applicable in v001: no kernel survived to Candidate formation; no
Promotion carrier was selected; no outcome was read.

## Seed Readiness Audit

Not applicable in v001: no Candidate exists.

## Unique narrow Gap

None in v001. The version closes with all kernels killed pre-freeze and a
Problem/family reset decision. Next version (v002) must re-open from a
different failure structure; if the Run remains ACTIVE without paid API,
the search is constrained to locally-executable problems with public
outcome annotations, and the realistic kernel space is materially
narrower than the mechanisms the corpus supports.
