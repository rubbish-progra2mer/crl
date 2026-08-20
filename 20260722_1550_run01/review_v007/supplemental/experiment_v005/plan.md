# Experiment Plan

```json
{
  "experiment_id": "v005",
  "candidate_sha256": "c36b4847029ea234c8db9b574a128b1d9ca01dc6d425e9fddd099ba141ad8291",
  "evidence_packet_sha256": "a54b710aed7ce35f44a25943d4f4e46826e7ffdc34c628f53ce9d180f9882d6b"
}
```

## Codex Plan

# ToolRet three-donor target-instruction audit

## Frozen before v005 Development bytes

This plan is frozen before acquiring or reading any v005 query row. v004 is a disclosed negative predecessor, not part of v005 statistics. v004's one-donor universal Claim failed because MiniLM was exactly neutral on `gorilla-pytorch`; its frozen Result SHA-256 is `33c0e0865849ae131740584fe9b3103cb3f0cbb9029251b6a951b33e69ada961`.

Before this freeze, the Main Codex read only the pinned dataset's config names and size metadata for the remaining pool. A new arXiv exact search was rate-limited and is not treated as a zero-result search. No v005 Development or Confirmation query bytes have been acquired.

## Frozen executable and reused inputs

- `experiment_v005/artifacts/audit.py`, expected SHA-256 `2bd37ea6cc21e1ff3ef46e76d86322dc33f2b56fe8dd7dce12fdc9aca6c6ea02`.
- `experiment_v005/artifacts/config.json`, expected SHA-256 `6bf119f6f18432008ca0ba5fda743323ac4f1a0707b87eb72a581c0d001e3436`.
- Reused full pinned corpus, expected SHA-256 `1bff924c03fe4b48e8d902045d68eb7fad3c2decd569fb52566ea0aec4a056f0`, 44,453 rows.
- Reused fixed MiniLM corpus embeddings, expected SHA-256 `1892ff350f336b5e0ace8882fb300cce4b10ab6333cf2905b852b1243322f5f7`.

The corpus and embeddings are touched infrastructure, not outcome partitions. v005 query acquisition still verifies that the currently served query and tool dataset SHAs equal the frozen revisions.

## Prospective phase split

Development configs, 2,600 advertised rows: `apigen`, `craft-vqa`, `gorilla-huggingface`, `reversechain`, `toolalpaca`, `toolbench-sam`, `tooleyes`, `toollens`.

Confirmation configs, 2,764 advertised rows: `appbench`, `autotools-food`, `autotools-music`, `autotools-weather`, `gpt4tools`, `gta`, `mnms`, `restgpt-spotify`, `taskbench-huggingface`, `taskbench-multimedia`, `tool-be-honest`, `toolbench`, `toolemu`, `toolink`, `ultratool`.

All 23 configs were absent from v001-v004 acquisition. Confirmation query bytes may be acquired only after the Main Codex reads Development artifacts, independently verifies raw integrity and metrics, and writes a Promotion Audit.

## Donor and view construction

For each query, eligible donors must share the source config, differ in query ID, and have no target-label overlap. Candidates are ordered by absolute `[a-z0-9_]+` instruction-token length difference, then SHA-256 of `(recipient_id, donor_id)`. The first three are retained without outcome selection.

The six views are `query_only`, `aligned_full`, `mismatched_full_1`, `mismatched_full_2`, `mismatched_full_3`, and `generic_full`. All views append the unchanged user query and search the identical full corpus with top-k 10.

## Primary computation and diagnostics

For each retriever and query, the primary effect is aligned NDCG@10 minus the arithmetic mean of the three mismatched-view NDCG@10 values. Query effects are averaged within source configs; source effects are then equally averaged. A source-cluster bootstrap uses NumPy seed `20260722` and 20,000 replicates. The median source effect is a second primary robustness condition.

The mechanism signature is aligned instruction IDF lexical support for official target documents minus mean donor instruction support. Mean within-query standard deviation across donor NDCG values is a secondary control-stability diagnostic. Recall@10, Completeness@10, query-only, generic, each donor view, every source effect, and every non-positive source remain descriptive outputs.

## Development promotion gate

The Main Codex may open Confirmation only if, for both BM25 and MiniLM:

- equal-source mean effect is positive and the source-cluster bootstrap 95% lower bound is strictly above zero;
- median source effect is strictly above zero;
- mean aligned-minus-mean-donor lexical support is strictly above zero;
- every Development query has exactly three distinct same-source non-self donors, all recorded target overlaps are zero, and no query is removed; and
- the expected `queries x 6 views x 2 retrievers` raw cells are complete and unique, every ranking has ten unique IDs, and independent official-qrel metric recomputation matches exactly.

Any non-positive source is disclosed but does not independently fail the aggregate Claim. The Main Codex must record the Promotion Audit before any Confirmation acquisition.

## Confirmation gate

The same conditions apply unchanged on the fifteen untouched Confirmation sources. Failure kills v005 and forbids Review. Success permits freezing a Review Packet but does not itself authorize Delivery.

## Capture contract

Every attempt is run from `implementation_v005/` by `D:/Desktop/crl/crl_agent_v3/.venv/python.exe` through `tools/run_local_experiment.py`, with argv pointing only to current `experiment_v005/artifacts/` bytes. Acquisition uses one HTTP worker and a fixed three-second delay, outputs only phase queries and an acquisition manifest, and reuses the frozen corpus. Evaluation outputs raw JSONL, summary JSON, environment JSON, and reuses the fixed corpus embeddings.

Attempt IDs are `dev_acquire_001`, `dev_eval_001`, `confirmation_acquire_001`, and `confirmation_eval_001`, incremented rather than overwritten after any failure or interruption. Every capture preserves `execution.json`, `stdout.bin`, and `stderr.bin`. All outputs and attempts are frozen as Experiment Artifacts before Result or Review Packet construction.

## Claim boundary and direct falsification

If both phases pass, v005 may claim only a positive average target-conditioning signal across the frozen source clusters relative to this deterministic three-donor control. It cannot claim universal per-source positivity, a deployable retrieval gain, causal identification, benchmark invalidity, exhaustive labels, optimal donor count, or end-to-end Agent improvement.

Formal review still kills Delivery if the same ToolRet donor-ensemble audit exists in prior work, the increment is judged insufficiently substantive, the baseline is unfair, or the evidence cannot support the bounded Claim.
