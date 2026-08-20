<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-evidence-audit-before-score","card_kind":"operator","paper_id":"P068","evidence_ids":["ev-p068-audit-then-score","ev-p068-one-shot-gold-brittle"],"source_refs":[{"path":"papers/P068_deepfact.pdf","sha256":"a26aeaefd0f1c763a40c1383c3a18ac723629519f6089abcdfe85ad74057f079"}]} -->
# Evidence Audit Before Benchmark Scoring

## Intervention target
[CODEX_SYNTHESIS] Deep Research factual claim 的 gold adjudication 与评分顺序。

## Before and after computation
[CODEX_SYNTHESIS] fixed gold direct score → evidence-backed challenger disagreement, auditor revision, then score。[[evidence:ev-p068-audit-then-score]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] challenger 读取 current benchmark state，仅在 disagreement 时提交 verdict、rationale 与 evidence；auditor 比较该 proposal 和 incumbent rationale，接受的修订形成新版本后再评分。评分前增加审计模型与 token 成本。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 先修正错误或不完整 gold，可避免把 benchmark defect 记成 Agent factuality error。

## Predicted observable signature
[CODEX_HYPOTHESIS] 提升应来自 disagreement-gated、可审计的 label revision，且在固定 incumbent label 与近成本对照中分别报告。

## Preconditions and transfer risks
[AUTHOR_FACT] 人类对 hidden micro-gold 的准确率随审计轮次显著变化。[[evidence:ev-p068-one-shot-gold-brittle]] [CODEX_SYNTHESIS] verifier/benchmark 共演化和更高 token 成本需单独控制。

## Source lineage
[CODEX_SYNTHESIS] fixed expert gold → co-evolving evidence adjudication；不等同于普通 LLM-as-judge 投票。

## Evidence ledger
[CODEX_SYNTHESIS] audit pipeline 与 gold brittleness 有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] audit then score; benchmark adjudication; versioned evidence; brittle gold; deep research factuality
