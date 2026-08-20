# Delivery Record

```json
{
  "review_id": "v007",
  "decision_sha256": "e6ec3f718646e8206563093094eb2eee3f445d7034841b7de787b85a017c8cd9"
}
```

## Codex Delivery Text

# Candidate Implement Seed Delivery

## Carrier-independent mechanism statement

A preregistered measurement harness that measures stale-over-current
inversion in schema-free conversational memory retrieval, attributes it
across granularity, propagation and scoring interventions, and observes
its directional answer-level consequences with a fixed reader under an
equal context cap (kernel wording per decision_v007 ERRATUM E9). It
applies to any timestamped memory store with annotated update queries.

## Implement path/SHA and exact command

- Frozen harness: experiment_v005/artifacts/measure_decomposition.py
  (SHA c171a710...f3a108bc), reader_arm.py (dbbd3233...c894a4f0),
  config.json v006 (daf7c2e7..., max_tokens=1000).
- Frozen judge: implementation_v007/judge.py (b14b3841...), full
  verdict table workbench_v007/verdict_table_v006_reader.jsonl
  (425d09d0...), reproduced byte-identically by two independent
  reviewers.
- Exact commands: captures experiment_v005/captures/dev_local_001/
  execution.json and experiment_v006/captures/dev_reader_001/
  execution.json record complete argv/cwd/input-SHA/output-SHA chains.

## Environment and raw experiments

Python 3.11.15 (.venv), all-MiniLM-L6-v2 encoder on RTX 5060 Ti;
reader deepseek-v4-flash (per-row model field), temperature 0.
Raw: development_raw.jsonl (bd7ad4de...), reader_raw.jsonl v006
(e81e79c1...), all summary numbers independently recomputed by three
reviewers across two review rounds. Total API usage across the run:
~371k in / ~25k out tokens (about 1 USD).

## Mechanism signature observed in Promotion Development

Retrieval stage (D bucket, 37 update items): turn-level inversion 22/37
(Wilson CI 43.5-73.7%); sentence granularity 22->16 net (12 fixed / 6
created); propagation ~0 (23/37); recency 6/37 with non-update harm
-0.61 [-0.91,-0.31]; sentence non-update gain +1.55 [+1.27,+1.83].
Answer stage (directional only): 29/34/32 of 37; at least five
turn-arm answers return specific superseded values, the five listed
all correct under sentence retrieval; of the four timestamp-decidable,
two occurred despite current-first retrieval. All intervals include
zero on pairwise reader deltas; nothing here is a quantified
consequence claim.

## Closest-composition comparator evidence

No external runnable competing decomposition exists (two independent
open-web reviewer sweeps, 18 query families total, 2026-07-26,
absence-of-evidence grade). Internal arm matrix is the comparator set.
Named nearest neighbors with explicit differences: LongMemEval (P010,
ancestor), MemStrata, STALE, MemConflict 2605.20926, Collapse of Dense
Retrievers 2503.05037, MemoryAgentBench FactConsolidation, Dense X,
SGMem, and the June-July 2026 items per decision_v007 ERRATUM E8.

## Narrow supported Claim and explicit non-claims

The claim ceiling of problem_v007.md (f52b776e...) AS AMENDED BY the
binding errata E1-E10 in decision_v007.md. Non-claims (FORBIDDEN):
quantified answer-error increase; item-level inversion-to-error
conversion; inversion above 50% chance; isomorphism as measured
mechanism; equal budget; any cross-encoder/reader/dataset
generalization; any repair effectiveness; any Confirmation-grade
status. NOTHING in this delivery has been tested on untouched data.

## Reserved untouched Confirmation

- Carrier: data_split_commitment_v002/longmemeval_s_CONFIRMATION_
  RESERVED.json, SHA 28a5710998a999bf464fa7c97585740af3a89b7816c3292e
  3c5c93d08a50b2ba (185 questions, 27 knowledge-update).
- Untouched proof: deterministic commit-reveal split (rule committed
  before any content read, manifest 00A30A73...; physically separated
  file; re-run the rule to verify; three reviewers re-executed all 500
  assignments with zero mismatches; no C outcome appears in any frozen
  artifact).
- Preregistered plan: run the identical frozen harness on the C file;
  gates C1 (inversion Wilson CI excluding 0.50 requires >=19/27) and
  C2 (paired reader delta CI excluding 0), scoring protocol per
  ERRATUM E10 (frozen auto-scorer primary, blind-to-arm equivalence
  adjudication dual-reported, date-tied items excluded from C1).
  The record itself computes C1 pass probability ~17% at the D point
  estimate: a severe test, expected to be hard.

## Nearest prior and unresolved collisions

None unresolved as of 2026-07-26; date-scoped. Private prior
commitments honored across both rounds (v006 A5419590..., v007
38C0853E...), bodies never entered any packet.

## Three independent reviews and Main Codex Decision

Two full rounds, six fresh leaf reviewers total:
- v006: packet 2fe7fceb...; reports fb4ac733... / b707d54b... /
  8c0e13b9...; decision_v006 3442b769... = REVISE_AS_NEW_VERSION
  (three verified claim-text fatal objections; execution record
  confirmed sound).
- v007: packet cce10f04...; reports c85a1af3... / c26a0454... /
  02b7ec3b...; decision_v007 e6ec3f71... = DELIVER_IMPLEMENT with
  binding errata E1-E10.

## Scale-up roadmap

Cost-ordered, each step can kill the finding: (1) encoder sweep
(config swap, local, hours) - kills residual-attribution generality if
overlap dominance vanishes; (2) stronger readers (<5 USD) - kills the
consequence observation if strong readers self-correct; (3) C bucket
per preregistered gates; (4) second dataset with update annotations
and preregistered paired-delta gate (candidates per ERRATUM E10) -
this step carries the consequence claim; (5) paraphrase ablation -
direct falsifier for the residual component; (6) length-matched
context control - closes the "shorter context is easier" alternative.
Cross-model verification is the first and largest known risk.

## Known risks and falsification conditions

n=37 development data; one encoder, one reader, one dataset; D bucket
partially exposed between v005 and v006 (disclosed everywhere); the
isomorphism residual may be benchmark question-writing artifact; C
likely underpowered for the consequence gate; every falsifier above is
cheap and preregistrable.

## Why further investment is justified

The receiver starts from a working, byte-reproducible implementation
and raw data, not from an idea: every published number was reproduced
independently by multiple reviewers; the harness manipulates the
computation under test rather than observing fixed data; the kill
chain (five workbench falsifiers, two review rounds) already removed
the obvious wrong turns at near-zero cost; and the honest claim
ceiling means nothing delivered here needs to be walked back before
scaling. The deliverable is a measurement-paper skeleton whose
consequence headline is deliberately deferred to the receiver's
severe gates.

Delivery is a research-seed investment recommendation, not a paper
draft and not a harness-quality certification. It is explicitly
untested on untouched data; that test is the receiver's first step.
