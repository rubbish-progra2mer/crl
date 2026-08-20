# Neutral Selection Context

## Version scope

This is the second Candidate version in `20260722_1550_run01`. It retains the v001 research Claim and evaluation delta. v001 was not scientifically evaluated: its frozen `dev_acquire_001` attempt ended with HTTP 429 while paging the full tool corpus, before a corpus, acquisition manifest, or any retrieval metric existed. v002 changes only the mechanical acquisition concurrency from 16 workers to one.

## Kernels considered

- Local contrastive residual reranking: killed before Candidate because direct recent reranking and neighborhood/set-decoding priors occupy the computation.
- Schema-derived clarification before retrieval: killed before Candidate because SAGE-Agent and ToolDial directly cover structured clarification.
- Provenance-aware target-instruction negative control: selected as the unchanged narrow evaluation implement.

## Data touched before v002 freeze

- The Main Codex read P085 and visually inspected PDF pages 4-5 describing target-aware instruction generation, human review, and the `w/ inst.`/`w/o inst.` protocol.
- Before v001 freeze, five `rotbench` rows were viewed for schema.
- The frozen v001 acquisition persisted all served Development query rows from `apibank`, `restgpt-tmdb`, `rotbench`, and `taskbench-daily` as a partial output before HTTP 429. No v001 corpus or metric output was produced.
- No Confirmation query bytes from `craft-math-algebra`, `craft-tabmwp`, `gorilla-pytorch`, `gorilla-tensor`, `metatool`, `t-eval-dialog`, `t-eval-step`, or `toolace` have been acquired or semantically read.
- ArXiv abstracts and titles were inspected for nearest-prior routing. No paid API was called.

## Frozen source identities

- P085 PDF: `D:/Desktop/crl/crl_agent_v3/knowledge_base/papers/P085_toolret.pdf`, SHA-256 `26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a`.
- Official query dataset revision: `mangopy/ToolRet-Queries@b8c76ad3349ff17497b6bdb28bb5b8f61a0f6445`.
- Official tool dataset revision: `mangopy/ToolRet-Tools@e06c38c75612b6536bd959e08cdd345894aba6a7`.
- v001 failed result: `experiment_v001/result.md`, SHA-256 `ad69d0b1c3f3f89fe6ed3db9cad897cdc74958da7180f38d2fb233a2e3e50e8b`.
- v001 attempts manifest: `experiment_v001/artifacts/attempts_manifest.json`, SHA-256 `4490f6b1f00a59aceb324f303aadee71164b3048e782ce3f0c81944e394d0d6e`.

## Optional-stopping disclosure

No scientific outcome has been observed in this Run. v002 is not an outcome-driven hyperparameter change: the sole change is reducing public HTTP request concurrency after a recorded 429. Candidate metrics, splits, retrievers, model revision, bootstrap, controls, Claim, and falsification conditions are unchanged.

