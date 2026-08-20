# Neutral Selection Context

## Version scope

This is the fourth Candidate version in `20260722_1550_run01`. It retains the same research Claim, evaluation delta, metrics, splits, retrievers, and model revision as v001-v003. The first three versions were not scientifically evaluated: each persisted identical Development query bytes, then ended with HTTP 429 before the full corpus or any retrieval metric existed. v004 changes only the fixed single-worker request interval from one second to three seconds.

## Kernels considered

- Local contrastive residual reranking: killed before Candidate because direct recent reranking and neighborhood/set-decoding priors occupy the computation.
- Schema-derived clarification before retrieval: killed before Candidate because SAGE-Agent and ToolDial directly cover structured clarification.
- Provenance-aware target-instruction negative control: selected as the unchanged narrow evaluation implement.

## Data touched before v004 freeze

- The Main Codex read P085 and visually inspected PDF pages 4-5 describing target-aware instruction generation, human review, and the `w/ inst.`/`w/o inst.` protocol.
- All three failed versions persisted the same complete Development query bytes from `apibank`, `restgpt-tmdb`, `rotbench`, and `taskbench-daily`; SHA-256 `b785627bffe17b69bb58ccc664f20375735e56b6870322e3dad43a771f025d31`.
- None produced a corpus, acquisition manifest, embedding, raw retrieval row, summary, or metric.
- No Confirmation query bytes from `craft-math-algebra`, `craft-tabmwp`, `gorilla-pytorch`, `gorilla-tensor`, `metatool`, `t-eval-dialog`, `t-eval-step`, or `toolace` have been acquired or semantically read.
- ArXiv abstracts and titles were inspected for nearest-prior routing. No paid API was called.

## Frozen source identities

- P085 PDF: `D:/Desktop/crl/crl_agent_v3/knowledge_base/papers/P085_toolret.pdf`, SHA-256 `26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a`.
- Official query dataset revision: `mangopy/ToolRet-Queries@b8c76ad3349ff17497b6bdb28bb5b8f61a0f6445`.
- Official tool dataset revision: `mangopy/ToolRet-Tools@e06c38c75612b6536bd959e08cdd345894aba6a7`.
- v001 result: `experiment_v001/result.md`, SHA-256 `ad69d0b1c3f3f89fe6ed3db9cad897cdc74958da7180f38d2fb233a2e3e50e8b`.
- v002 result: `experiment_v002/result.md`, SHA-256 `bc9261eeb2af5cbf17795781626aca7c611fb703043dcfa0f2b296f38684b0d2`.
- v003 result: `experiment_v003/result.md`, SHA-256 `7d6bce2a555b3d545206fe9c2f8867ad700ccb205f2ff4cdd55f112ad7a80ce8`.
- v003 attempts manifest: `experiment_v003/artifacts/attempts_manifest.json`, SHA-256 `d01bad7832e3443beba43af1847dea5de2bda88b56a5a650cce96733c5d5f81e`.

## Optional-stopping disclosure

No scientific outcome has been observed in this Run. v004 is not outcome-driven: its sole change is a lower deterministic public-request rate after three recorded 429 failures. No metric, Claim boundary, comparator, model, bootstrap, data split, or kill condition changed.

