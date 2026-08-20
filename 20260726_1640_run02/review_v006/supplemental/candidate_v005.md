<!-- crl-v3-evidence-ids
["ev-p010-index-retrieve-read","ev-p030-failure-core","ev-p011-failure-core","ev-p064-experience-following-error"]
-->
# Candidate Implement

## One-sentence method kernel

A preregistered measurement harness that causally decomposes stale bias
in schema-free conversational-memory retrieval (phrasing isomorphism vs
chunk dilution vs graph propagation) and quantifies its answer-level
consequences with a fixed reader at equal budget.

## Carrier-independent statement

Paired stale/current best-unit analysis under unit-granularity ablation
and scoring-arm ablation, plus a fixed-reader consequence arm, applies
to any timestamped memory store with annotated update queries. Channel:
first-hand workbench failure (v002-v004 chain).

## Use Thesis, decision interface and Value Bridge

Consumers: memory-system builders (where to place staleness defenses)
and long-memory benchmark maintainers (update-question design).
Decision changed: stop investing in retrieval-layer staleness patches
for schema-free memory; prioritize representation/write-side. Bridge:
reader arm converts retrieval inversion to answer errors.

## Failure/Evidence -> Operator -> Gap lineage

P010 oracle gap + stage decomposition [[evidence:ev-p010-index-retrieve-read]];
P030 stale application failure [[evidence:ev-p030-failure-core]];
P011 granularity failures [[evidence:ev-p011-failure-core]];
P064 error-following [[evidence:ev-p064-experience-following-error]];
first-hand v002-v004 falsifier chain (workbench_v003/, workbench_v004/).
Gap: no causal decomposition of stale bias with consequence arm exists.

## Baseline computation

Turn-level MiniLM cosine retrieval over haystack units; top-k context to
reader. Inputs: query, units, timestamps. No outcome signal at run time.

## Changed computation

None in the production path (attribution candidate). The measurement
harness computes: (a) per-item stale/current best-unit ranks and margins
at turn and sentence granularity; (b) direct vs PPR vs global-recency
scoring arms; (c) reader answer correctness under three context arms
(natural turn-level top-k; sentence-level top-k; oracle-current) at
equal returned-token budget.

## Closest-composition difference

P010 stage decomposition diagnoses retrieval-vs-reading; it never splits
stale-vs-current inside retrieval. MemStrata's AUROC study covers
synthetic triples without granularity/propagation axes or reader
consequences. Neither is runnable as a competing decomposition; both are
components. No fair runnable closest-composition exists for the full
decomposition; the Claim stays measurement-scoped accordingly.

## Minimal Claim Contract

If kill conditions fail to trigger, the maximal claim is: on
LongMemEval-s knowledge-update questions (fresh D bucket), turn-level
schema-free retrieval exhibits stale-over-current inversion at a rate
materially above chance; sentence-level indexing removes a quantified
minority share (dilution); the dominant residual is phrasing
isomorphism; and inversion converts to a quantified answer-error
increase with a fixed reader at equal budget. FORBIDDEN extensions: any
repair-effectiveness claim; any cross-dataset or cross-encoder
generalization; any claim about write-side/LLM-gating alternatives.

## Causal chain and one major scientific risk

Failure phenomenon (inversion) -> decomposition (isomorphism/dilution/
propagation) -> consequence (answer errors). Established: W-bucket
pattern (workbench-grade). THE single unverified leap: replication on
untouched data with consequence conversion. Falsifiers: preregistered
kill conditions 1-3 in problem_v005.

## Workbench decisive falsifier

Already executed across v002-v004 (five experiments); they formed this
candidate rather than merely authorizing it. No further workbench
probing before Promotion; any additional W-bucket tuning would be
optional-stopping surface.

## Implement contract

implementation_v005/: measure_decomposition.py (local; loads ONLY the
physically-separated D-bucket file; computes (a)+(b) and writes raw
per-item jsonl); reader_arm.py (deepseek-chat; three context arms
interleaved per item; raw API jsonl with per-row model version and
timestamps; secret-redacted; segment checkpoints); config.json (frozen
parameters: K=10, granularity defs, arm order, prompts, seeds, budget
caps); judge = exact-match+substring against gold answer with manual
review of mismatches by Main Codex (no LLM judge, avoiding judge
circularity). Exact argv/cwd fixed in experiment plan.

## Neutral comparators

ARM-T (turn-level direct), ARM-S (sentence-level direct), ARM-P (PPR),
ARM-R (global recency), READER-T/READER-S/READER-O (oracle-current).
Identities and configs frozen; no ranking labels.

## Experiment contract

Primary metrics: inversion rate (T), inversion reduction (S vs T),
margin shift, per-arm stale@k/current@k; reader accuracy per context
arm. Mechanism signature: dilution share = inversions removed by S;
isomorphism share = residual inversions with high query-stale lexical
overlap; propagation share = P vs T delta (predicted ~0). Artifacts:
execution.json, stdout.bin, stderr.bin, development_raw.jsonl,
reader_raw.jsonl, summary.json.

## Data roles and freshness

WORKBENCH: LongMemEval-s W bucket (exposed; formed this candidate).
PROMOTION_DEVELOPMENT: D bucket file (untouched; physically separated;
loaded for the first time by the frozen harness).
CONFIRMATION: C bucket file (reserved untouched; commit SHA 28a5710998
a999bf464fa7c97585740af3a89b7816c3292e3c5c93d08a50b2ba; delivery hands
it over with the preregistered plan).
Freshness: candidate formed exclusively from W; D outcomes never read;
split rule is deterministic and re-runnable by the receiver.

## Model coverage

Retrieval stages: single encoder (all-MiniLM-L6-v2). Reader: single
model (deepseek-chat). Why acceptable now: the candidate's claim is
explicitly scoped to this encoder family and reader; cross-model
verification is the FIRST scale-up step and the known largest risk;
the decomposition harness runs unchanged on any encoder. Reviewers
should challenge if the claim text drifts wider.

## Reserved confirmation isolation and analysis unit

C bucket: 185 questions incl. 27 knowledge-update; isolation unit =
question_id (deterministic hash split); analysis clusters = question
level (each question's haystack is independently sampled by the
benchmark). Preregistered plan: rerun the identical frozen harness on C.

## Cost and bundle attribution

Local GPU minutes for retrieval arms; deepseek-chat for reader arm
(~250 calls, ~0.6M tokens in, ~30k out; expected < 1 USD; exact usage
reported in result). All arms share retrieval budget K and token caps;
reader arms share prompts and generation params. Claims are
bundle-scoped to the frozen harness.

## Risks and kill conditions

Kill conditions 1-3 (problem_v005). Additional risks: D-bucket update
count (37) limits CI width - claims will carry intervals, not point
brags; judge simplicity may misgrade paraphrases - manual review of all
mismatches; v007-precedent boundary - the Decision must explicitly
weigh whether attribution-with-consequences meets the delivery bar.
