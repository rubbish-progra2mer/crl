# Neutral Selection Context

## Version scope

This is the first Candidate version in `20260722_1550_run01`. No earlier version, experiment result, Reviewer report, or Decision exists in this Run.

## Kernels considered

- Local contrastive residual reranking: killed before Candidate because direct recent reranking and neighborhood/set-decoding priors occupy the computation.
- Schema-derived clarification before retrieval: killed before Candidate because SAGE-Agent and ToolDial directly cover structured clarification.
- Provenance-aware target-instruction negative control: selected for v001 as an evaluation implement.

## Data touched before freeze

- The Main Codex read P085 and visually inspected PDF pages 4-5 describing target-aware instruction generation, human review, and the `w/ inst.`/`w/o inst.` protocol.
- Five `rotbench` query rows and five public ToolRet web-corpus/qrel rows were viewed only to verify schema. `rotbench` is therefore assigned to Development and cannot be untouched Confirmation.
- Public dataset metadata and Parquet bytes were downloaded in the development evidence workspace, but no retrieval metrics were computed and no confirmation rows were semantically inspected.
- ArXiv abstracts and titles were inspected for nearest-prior routing. No paid API was called.

## Frozen source identities

- P085 PDF: `D:/Desktop/crl/crl_agent_v3/knowledge_base/papers/P085_toolret.pdf`, SHA-256 `26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a`.
- Official query dataset expected revision: `mangopy/ToolRet-Queries@b8c76ad3349ff17497b6bdb28bb5b8f61a0f6445`.
- Official tool dataset expected revision: `mangopy/ToolRet-Tools@e06c38c75612b6536bd959e08cdd345894aba6a7`.

## Optional-stopping disclosure

No scientific outcome has been observed. Candidate v001 and its falsification conditions are frozen before acquisition and Development metrics. Confirmation configs are named in the Candidate and config before Development.
