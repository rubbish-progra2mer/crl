# Experiment Plan

```json
{
  "experiment_id": "v005",
  "candidate_sha256": "aa99d8c63cc631ca3ce8057408c7f7edea060820098a3d50ac9c6b9a28e22da0",
  "evidence_packet_sha256": "ea26ece96884819b6a633d903f3c3a3f219376abb93331eb2b7080f03b9343dd"
}
```

## Codex Plan

## Frozen before results

Frozen 2026-07-26 after synthetic-smoke readiness, before any D-bucket
byte is read by analysis code.

## Data roles, acquisition and sampling contract

WORKBENCH: LongMemEval-s W bucket (exposed; formed K12; not used here).
PROMOTION_DEVELOPMENT: data_split_commitment_v002/longmemeval_s_
PROMOTION_DEVELOPMENT.json (222 questions, SHA 25cc9c2b6be241fb0caa2689
bf621bf9111c1a9d297f516d1c382a48022d8112), loaded for the FIRST time by
the frozen harness below; all update-pair items (expected ~37) and all
non-update items with evidence are scored; no sampling, no exclusions
beyond evidence-in-haystack presence.
CONFIRMATION: longmemeval_s_CONFIRMATION_RESERVED.json (185 q, SHA
28a5710998a999bf464fa7c97585740af3a89b7816c3292e3c5c93d08a50b2ba) stays
unread; the receiver reruns this identical plan on it.

Reserved-confirmation proof: deterministic split rule committed before
any content read (manifest SHA 00A30A73B532E1334EC4AA23976C53381DDB359E
2BE995B72D83FBC30849F4E3) plus physical file separation; verification =
re-running the rule.

## Primary metric and mechanism signature

Update items: inversion rate turn/direct; margin; per-arm deltas.
Signature: sentence-level reduces inversions and lifts margin (dilution
share); ppr ~= direct (propagation ~0); recency fixes inversions but
harms non-update hits (bluntness); residual inversions carry high
query-stale lexical overlap (isomorphism share). Reader arms: accuracy
oracle_current > sentence_topk > turn_topk on update items at equal
context budget converts inversion into answer errors.

## Closest-composition, neutral comparators and delta ablation

Internal arm matrix is the comparator set (ARM-T/S/P/R; READER-T/S/O);
no external runnable decomposition exists (nearest_prior_v005.md).

## Same-model/data/tool-budget controls

One encoder (all-MiniLM-L6-v2), one reader (deepseek-v4-flash; the
preauthorized provider's current API name for its light model),
temperature 0, equal context char cap 6000, equal K=10, identical
prompts across arms, arms interleaved per item for drift control.

## Capture and Artifact bindings

Frozen inputs: implementation_v005/measure_decomposition.py,
reader_arm.py, config.json (saved as experiment artifacts pre-run).
Captures: experiment_v005/captures/dev_local_001/ (measure) and
dev_reader_001/ (reader), runner-generated execution.json / stdout.bin /
stderr.bin unchanged. Declared outputs: work/dev_local_001/
{development_raw.jsonl, development_summary.json}; work/dev_reader_001/
reader_raw.jsonl (line-checkpointed; per-row model version, usage,
UTC timestamp; interrupted segments disclosed per attempt discipline).

## Exact execution readiness

Interpreter resolved .venv\python.exe; cwd = implementation_v005;
imports verified (httpx, numpy, sentence_transformers); synthetic smoke
passed for both programs (no scientific outcome read; reader smoke 3
calls status 200, model field deepseek-v4-flash, answers correct on
synthetic update); DEEPSEEK_API_KEY only in process env, absent from
argv; exception redaction verified in code path; capture dirs do not
exist yet; declared outputs do not exist; no unresolved placeholders;
foreground array invocation; Candidate SHA aa99d8c63cc631ca3ce8057408c7
f7edea060820098a3d50ac9c6b9a28e22da0 and Evidence Packet bound by this
plan's JSON header.

## Preregistered confirmation isolation and cluster-aware analysis

Isolation unit: question_id hash bucket. Cluster unit: question (each
question's haystack independently sampled by the benchmark). W exposure
disclosed: hypotheses derive from W; D verifies; C reserved.

## Cost and bundle-level attribution

Local GPU minutes (encoder); reader: <=37 items x 3 arms x (~1.6k in /
<=100 out tokens) + retries; expected well under 1 USD; actual usage
reported in result from per-row usage fields. Claims bundle-scoped to
the frozen harness.

## Leakage, oracle and fixture checks

No gold enters retrieval or prompts beyond the question itself;
oracle_current arm is an explicit upper-bound control, labeled as such;
judge = exact/substring match + Main Codex manual review of mismatches
(no LLM judge). Synthetic smoke data cannot enter results (separate
files, scratchpad only).

## Direct falsification conditions

Kill 1: D-bucket turn/direct inversion rate < 40 percent.
Kill 2: sentence-level fails to reduce inversions AND fails to improve
mean margin vs turn-level.
Kill 3: reader accuracy shows no deficit for turn_topk vs
oracle_current on update items (no consequence).
Any kill -> candidate records failure; no claim survives it.
