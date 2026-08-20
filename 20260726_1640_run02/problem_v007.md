# Research Problem

## User intent

v007 is the record-and-claim repair version mandated by decision_v006
(SHA 3442b769f615d85c85e218e128634cda6d3cc0755b66ca59354f59904eccf43b).
No kernel change; no new experiment. The scientific problem, Use
Thesis, occupancy scan and Mechanism Demand of problem_v005 (SHA
3ffc013a...) remain incorporated by reference; the v005 kill-condition
framing is superseded by the corrected claim ceiling below.

## What v007 repairs (all six decision points)

1. Scoring record: turn arm 29/37 (not 30/37); 11 manual verdicts (not
   12); 031748ae_abs/turn answered substantively about a never-held
   role and is INCORRECT. Judge frozen at implementation_v007/judge.py;
   full 111-row verdict table at workbench_v007/verdict_table_v006_
   reader.jsonl; both reproduce 29/34/32 deterministically.
2. Claim contract rewritten to the supported ceiling (below).
3. Date-tie disclosure: item 618f13b2's two evidence sessions share
   2023-05-30; stale/current is timestamp-undecidable there and the
   two frozen v005/v006 programs tie-break oppositely, so the v006
   oracle arm read the other session on that item. It is EXCLUDED from
   per-item causal narratives and flagged in the verdict table context;
   aggregate numbers are reported both as frozen (37-item) and
   tie-excluded (36-item) where material. Future harness versions must
   unify tie-breaking; the frozen v005/v006 bytes stay as they are.
4. Band-size narrative corrected: K11 rows show band_size==1 in 9/14
   (band_sessions==1 in 11/14); the "10/14" in research_map_v004 was a
   transcription error (frozen, superseded here).
5. Oracle arm relabeled: "current-session control" (it restricts
   context to the current evidence session and loses cross-session
   context on 3 items; it is not an upper bound; sentence_topk exceeded
   it 34 vs 32).
6. Named nearest neighbors added (see research_map_v007) and severe
   C-bucket gates preregistered (see below).

## Corrected claim ceiling (Minimal Claim Contract, v007)

On LongMemEval-s knowledge-update questions (D bucket, 37 items; one
encoder all-MiniLM-L6-v2; one reader deepseek-v4-flash at temperature
0; equal 6000-char context CAP with realized mean prompt tokens
1399/466/1478 across arms):

(a) TEMPORAL BLINDNESS: turn-level direct retrieval shows no
    current-over-stale preference where the task requires a strong
    one - the stale evidence unit outranks the current one in 22/37
    items (59.5%, Wilson 95% CI 43.5-73.7%; not distinguishable from
    the 50% exchangeability null, p=0.162; far above the ~0% a
    currency-aware retriever should exhibit).
(b) GRANULARITY SHARE: sentence-level indexing shifts inversions
    22->16 net (12 fixed, 6 newly created; McNemar p~0.24) and the
    mean current-minus-stale margin from -0.049 to -0.020, while
    raising non-update evidence hits 6.52->8.06.
(c) PROPAGATION: PPR-style diffusion leaves inversion essentially
    unchanged (23/37 vs 22/37).
(d) RECENCY TRADE-OFF: a global recency prior removes most inversions
    (6/37) but harms non-update evidence hits (6.52->5.91).
(e) READER OBSERVATION (directional only): final accuracies 29/37
    (turn) vs 34/37 (sentence) vs 32/37 (current-session control);
    all pairwise deltas inside wide 95% CIs (e.g. sentence-turn
    +13.5pp, CI includes zero at n=37); the turn arm produced five
    verbatim superseded-value answers, absent under sentence-level
    retrieval; two of those five occurred despite current-first
    retrieval, so stale answers arise from stale-dominated CONTEXT
    COMPOSITION, not from best-unit inversion per se.
(f) RESIDUAL: inversions surviving granularity ablation are consistent
    with query-initial-statement phrasing overlap (unregistered proxy:
    mean q_overlap 0.696 vs 0.501); this is residual attribution, NOT
    a measured mechanism; the direct falsifier (paraphrase ablation)
    is registered for scale-up.

FORBIDDEN claims (unchanged plus reinforced): any quantified
answer-error increase; any item-level inversion-to-error conversion;
inversion above 50% chance; isomorphism as measured dominant
mechanism; equal budget (only equal cap); any cross-encoder/reader/
dataset generalization; any repair effectiveness; any Confirmation-
grade status for any conclusion (D was partially exposed between v005
and v006; C is the only clean set and is handed over unread).

## Preregistered severe C-bucket gates (receiver-executed)

Gate C1: turn-level inversion rate on C's 27 update items with Wilson
95% CI excluding 0.50 from above would establish inversion-above-
chance; CI containing 0.50 leaves only temporal blindness.
Gate C2: paired reader delta (sentence minus turn) with 95% CI
excluding 0 would establish the consequence claim; C's n=27 is likely
underpowered - the receiver should treat a second dataset replication
as the real consequence gate and C as a replication-of-direction
check. These gates are preregistered here, before any C byte is read;
the machine does not run C.

## Cost authorization

Unchanged. No new API usage in v007.
