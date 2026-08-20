<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p068","card_kind":"paper","paper_id":"P068","evidence_ids":["ev-p068-audit-then-score","ev-p068-one-shot-gold-brittle"],"source_refs":[{"path":"papers/P068_deepfact.pdf","sha256":"a26aeaefd0f1c763a40c1383c3a18ac723629519f6089abcdfe85ad74057f079"}]} -->
# DeepFact

## Role in the knowledge base
[CODEX_SYNTHESIS] Deep Research factuality 的 evidence-backed audit-then-score operator 与 brittle gold 负向来源。

## Problem and setting
[AUTHOR_FACT] challenger 提交带证据的分歧，auditor 先决定是否修订 benchmark，再进行评分。[[evidence:ev-p068-audit-then-score]]

## Changed computation
[CODEX_SYNTHESIS] 把固定 gold 的一次性判分改为 versioned evidence adjudication 后再评分。

## Evidence-backed findings
[AUTHOR_FACT] hidden micro-golds 上的人类 benchmark accuracy 经多轮 audit 从 60.8% 提升到 90.9%。[[evidence:ev-p068-one-shot-gold-brittle]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 审计会增加模型调用与 token 成本；benchmark 与 verifier 的潜在共演化是正式实验必须控制的 confound，收益不能只报总分。

## Lineage and baselines
[CODEX_SYNTHESIS] fixed expert gold → evidence challenger → auditor revision → score。

## Evidence ledger
[CODEX_SYNTHESIS] adjudication pipeline 与 gold brittleness 均有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] audit then score; factuality adjudication; versioned gold; deep research evaluation; benchmark correction
