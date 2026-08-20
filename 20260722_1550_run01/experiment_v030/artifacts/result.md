# Experiment Result v030

Disposition: `NO_GO_FOR_CONFIRMATION`.

## Frozen execution evidence

- Plan SHA-256: `3dc859f38bff818c03314d825368e55e6ef95836924924e3a870caf1a02e7cdb`
- Development execution SHA-256: `3b2480e97187ac2f397c6f802b868dc30945c440e90c2369388fefd39a991c31`
- Development raw SHA-256: `add9d1d946809a991adfb8b64c4d3db9191c700e6d9f0746e9b45be95ba868e5`
- Development summary SHA-256: `ef938cacb741a0ece165a4ee7d91381c7469bdd962fb11b815d08d62857a3683`
- Audit execution SHA-256: `20589e61e6bc71adc73902188f2d6e387ae96d1d06a4f555bad79cfb4086f96e`
- Audit report SHA-256: `c61b7f553f12e3089cf49cadeabe7be6da55b1e7f66f0562d1f08995cb6c1b54`
- Main raw analysis SHA-256: `7782a9e9a903b7c23373b1786f389798715bdc5e18c0fc6dc65af412a0118109`
- Main Promotion Audit SHA-256: `e48896a5fdd7288dcc4b8d3ca512a41b3902f3ddb86411713be5f10ec64f26dc`
- Attempts Manifest SHA-256: `6ac19d63d2e0d9ffb1b4e1175b5c77f2eec6b784f6a4dc2c4f23e7033a5b4253`

Before this Result was copied, `experiment_v030/artifacts/` contained 68 frozen files totaling 11,299,656 bytes. It includes all 55 preexecution files, Development output/capture bytes, independent-audit output/capture bytes, the Main raw analysis, Promotion Audit and Attempts Manifest.

## Result

- Development and independent audit both exited `0`; `AUDIT_OK`.
- Auditor verified 31 sources and 1,506 source-feature rows with maximum channel, score, rank and metric errors all zero.
- RTCA MRR: `0.31369047619047624`.
- RTCA MAP: `0.3211309523809524`.
- RTCA Recall@10: `1.0`.
- RTCA top-10 PR coverage: `8/8`.
- Strongest comparator: `schema_only`, MRR `0.2428575796222855`.
- MRR delta: `+0.07083289656819075`.
- MRR-delta bootstrap 95% interval: `[-0.09111721611721614, 0.21369003942533354]`.
- Program gates: `5/8`.
- Failed gates: `candidate_mrr`, `mrr_delta`, `bootstrap_lower`.

Every changed entry activated exactly one channel; the result did not demonstrate the claimed typed cross-layer combination. Recall@10 and pool coverage cannot override the preregistered MRR, comparative-gain and uncertainty failures.

## Boundary and next action

- Confirmation acquired: `false`.
- Reviewers started: `false`.
- Review Packet created: `false`.
- Delivery created: `false`.
- Same-version retry permitted: `false`.
- Next version: `v031`, requiring a scientifically distinct computation.
- Run status remains `ACTIVE`.
- System status remains `DEVELOPMENT_NOT_COMMISSIONED`.
