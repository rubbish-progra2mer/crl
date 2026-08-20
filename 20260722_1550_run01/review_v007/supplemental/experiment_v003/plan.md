# Experiment Plan

```json
{
  "experiment_id": "v003",
  "candidate_sha256": "a9a4aa8c82e95c55007eca51402413b8b676e1467c9687bd8ffd8863e136bb03",
  "evidence_packet_sha256": "cc27bd0faddc5ccef653055695be85b14a33a4d6ddff4b87f0b745a5809677ae"
}
```

## Codex Plan

# ToolRet target-instruction negative-control experiment

## Frozen before results

This plan is frozen before any retrieval metric has been computed. v001 and v002 each persisted identical Development query bytes but ended with HTTP 429 before corpus completion; neither produced an acquisition manifest or metric. Those Development bytes are therefore touched. No Confirmation query bytes have been acquired or semantically read. Candidate SHA-256 is `a9a4aa8c82e95c55007eca51402413b8b676e1467c9687bd8ffd8863e136bb03`; Evidence Packet SHA-256 is `cc27bd0faddc5ccef653055695be85b14a33a4d6ddff4b87f0b745a5809677ae`.

## Data acquisition and sampling contract

- Query dataset: `mangopy/ToolRet-Queries@b8c76ad3349ff17497b6bdb28bb5b8f61a0f6445`, split `queries`.
- Tool dataset: `mangopy/ToolRet-Tools@e06c38c75612b6536bd959e08cdd345894aba6a7`, split `tools`, configs `web`, `code`, and `customized`.
- Development is a census of every served row in `apibank`, `restgpt-tmdb`, `rotbench`, and `taskbench-daily`; there is no row sampling and therefore no sampling seed. The exact per-source N is whatever the pinned public revision serves and must be written to the acquisition manifest.
- Confirmation is a later, untouched census of `craft-math-algebra`, `craft-tabmwp`, `gorilla-pytorch`, `gorilla-tensor`, `metatool`, `t-eval-dialog`, `t-eval-step`, and `toolace`. Its bytes may be acquired only after the Main Codex reads Development output and writes the Promotion Audit.
- Development acquisition also obtains the full pinned public corpus. The paper's 43,215-tool snapshot and the served row count must be reported separately.
- Acquisition uses one HTTP worker and a fixed one-second wait before every rows request. The wait is added because both the recorded 16-worker v001 attempt and one-worker v002 attempt received HTTP 429; it does not alter dataset bytes or sampling. No missing or malformed row is silently removed. A nonzero acquisition/evaluation attempt is preserved and reviewed by the Main Codex; any later attempt receives a new attempt ID.

## Primary metric and mechanism signature

The primary effect is per-query `aligned_full - mismatched_full` NDCG@10. It is summarized per source config, then equally across source configs with a source-cluster bootstrap using seed `20260722` and 20,000 replicates. The mechanism signature is the aligned instruction's target-document IDF lexical support minus the matched wrong-target instruction's support. Recall@10 and Completeness@10 are secondary.

## Closest-composition, neutral comparators and delta ablation

The mandatory closest composition is ToolRet's original `query_only` versus `aligned_full` comparison. The unique delta is `mismatched_full`, chosen from the same source by minimum regex-token length difference with no target-ID overlap and deterministic SHA-256 tie breaking. `generic_full` controls for a generic retrieval instruction. BM25 (`k1=1.5`, `b=0.75`) and `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41` are neutral sparse and dense retrievers.

## Same-model/data/tool-budget controls

All four views use identical corpus bytes, qrels, top-k 10, retriever configuration, and local permissions. The dense model uses normalized embeddings on CUDA with batch size 256. The wrong-target donor identity, donor target IDs, length difference, and zero-overlap count are retained in every raw row. No LLM, paid API, tool execution, tuning, or outcome-selected hyperparameter is used.

## Capture and Artifact bindings

Frozen executable artifacts:

- `experiment_v003/artifacts/audit.py`, expected SHA-256 `d97903a938096dcbee197a8af41617c1c1e2e4226438868c157ff1156c6231f4`.
- `experiment_v003/artifacts/config.json`, expected SHA-256 `7b6e8fd6df080671be6c90769f0ffee1927737d915764018e4d412093e80e07f`.

Every capture is launched by `D:/Desktop/crl/crl_agent_v3/.venv/python.exe` through `D:/Desktop/crl/crl_agent_v3/tools/run_local_experiment.py`, with cwd `D:/Desktop/crl/20260722_1550_run01/implementation_v003`. Scientific argv references the frozen `experiment_v003/artifacts/audit.py` and `config.json`, never an editable machine source.

Development acquisition attempt `dev_acquire_001` declares three outputs: `development_corpus.jsonl`, `development_queries.jsonl`, and `development_acquisition_manifest.json`. After a zero exit, those exact bytes and the capture's `execution.json`, `stdout.bin`, and `stderr.bin` are saved as Experiment Artifacts with the attempt prefix.

Development evaluation attempt `dev_eval_001` takes the frozen corpus, queries, executable, and config as runner inputs. It declares `development_raw.jsonl`, `development_summary.json`, `development_environment.json`, and `corpus_embeddings.npy`. Those outputs and all three capture files are saved as Experiment Artifacts. An `attempts_manifest.json` binds both stages. Because the scientific result has deliberate acquisition and evaluation stages, neither stage is relabelled as a fabricated single canonical capture.

If authorized, Confirmation follows the same pattern with `confirmation_acquire_001` and `confirmation_eval_001`; it reuses the frozen full corpus and corpus embeddings and adds frozen Confirmation query, manifest, raw, summary, environment, capture, and updated attempts-manifest bytes.

## Confirmation isolation and cluster-aware analysis

Isolation and analysis units are source dataset configs. The four Development configs and eight Confirmation configs are disjoint. This supports a narrow source-disjoint replication claim only; it does not establish task-, template-, endpoint-, entity-, or open-world generalization. Query rows within a source share generation provenance and are not treated as independent clusters.

## Cost and bundle-level attribution

LLM tokens and paid calls: zero. External permission: public read-only Hugging Face HTTPS only. Fixed local compute: one corpus encoding, four views per query, BM25 on CPU, MiniLM on the single RTX 5060 Ti. Wall-time budgets are 30 minutes for each acquisition stage and 90 minutes for each evaluation stage. The result identifies the complete view-construction delta, not one lexical or semantic subcomponent.

## Leakage, oracle and fixture checks

Target IDs are used only to choose a non-overlapping offline negative-control donor and to score unchanged official qrels. They are never appended to retrieval text. The aligned instruction is explicitly target-aware and is not described as inference-time query-only information. All retrievals search the full pinned corpus, not an oracle menu or fixture. Non-exhaustive qrels limit every score interpretation.

## Direct falsification conditions

- Do not open Confirmation if either retriever has a non-positive Development effect in any source config, or if either source-cluster bootstrap lower bound is not above zero.
- Do not open Confirmation if the Development mechanism signature is non-positive or any matched pair has target overlap.
- Kill or reframe if matching cannot be constructed for more than 1% of rows; any smaller unmatched fraction must be disclosed rather than silently removed.
- After Confirmation, support the Claim only if both retrievers are positive in every included source, both Confirmation cluster-bootstrap lower bounds exceed zero, and the mechanism signature remains positive.
- Reframe if the effect is only exact-name support or one source family. Kill as a research contribution if formal review identifies the same ToolRet matched negative control in prior work.
