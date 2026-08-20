# Experiment Plan

```json
{
  "experiment_id": "v006",
  "candidate_sha256": "bee9c37465b9f4dfa6cb1f0522569eed80fa4ca079332f2c84996c5708384e09",
  "evidence_packet_sha256": "32780d598e779fa25e5c8f4e65ecc2db07805ce8217e33b4be039b6562f4cee8"
}
```

## Codex Plan

# ToolRet training-prompt three-donor audit

Frozen before any row from `mangopy/ToolRet-Training-20w@fdf5a317455b1e60785de7ba587496aa6cc878e4` was fetched. Metadata and README only were read.

Development is the exact half-open row range `[0,1000)`; Confirmation is `[207826,208826)`. Each is split into ten contiguous 100-row analysis blocks. Confirmation acquisition is forbidden until Main Codex Development Promotion Audit.

Acquisition normalizes each row into query, target-aware prompt, and positive-document qrels. It hashes and deduplicates every positive and negative tool string into one complete phase-wide corpus. Every view searches this corpus; the row's supplied negative list is never an oracle menu. Three non-self, positive-label-disjoint donor prompts are selected from the full 1,000-row phase by `[a-z0-9_]+` token-length difference and SHA-256 tie break.

Frozen implementation expected SHA-256: `ba44d7893e239983affffa2e20653ce4370b46a1eff60b38de2ffb41ae5efe74`. Frozen config expected SHA-256: `b9ebb6f4e695772533b81e50d667dae92312fe8ecf3fcd6c9da4f1643d45e64b`.

Six views, BM25, fixed `all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, top-k 10, three-donor mean effect, lexical-support mechanism, seed 20260722 and 20,000 block bootstraps are fixed. Development and Confirmation gates require both retrievers' equal-block mean, bootstrap lower bound, block median, and mechanism mean above zero; exactly three distinct zero-overlap donors per row; complete unique `rows x 6 x 2` cells; ten unique ranked IDs; and exact independent qrel metric recomputation.

Acquisition attempts output queries, phase corpus, and manifest. Evaluation attempts output raw, summary, and environment. All run through the shared Python 3.11.15 capture runner with frozen artifact argv. Failed attempts are retained and IDs increment, never overwritten.

Success supports only target-linked information in generated training prompts on the two fixed ranges. It does not support deployable improvement, causal identification, label exhaustiveness, benchmark invalidity, optimal donor count, or universal generalization. Formal novelty, rigor, and evidence Review remain mandatory after a fully frozen successful Confirmation Packet.
