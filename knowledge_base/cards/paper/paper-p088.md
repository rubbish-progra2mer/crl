<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p088","card_kind":"paper","paper_id":"P088","evidence_ids":["ev-p088-joint-nonnegative-objective","ev-p088-relevant-set-size-signature","ev-p088-theory-deployment-scale-boundary"],"source_refs":[{"path":"papers/P088_nnn_retrieval.pdf","sha256":"adb67ce1c663402dc988cd9de4df891a1e6f540cf41011cd21e406da32ce636e"}]} -->
# Non-negative Elastic Net Decoding for Information Retrieval

## Role in the knowledge base
[CODEX_SYNTHESIS] joint-set/diversity retrieval 的最近直接先行；专门阻止 CRL 把“对独立 top-k 加一个去重项”误判为新的 changed computation。

## Problem and setting
[CODEX_SYNTHESIS] 独立 query-item score 不利用 corpus items 之间的相关性，可能让近重复工具挤掉完成多工具任务所需的互补项。

## Changed computation
[AUTHOR_FACT] NNN 用 non-negative elastic-net reconstruction 联合决定 support；某项系数依赖完整 corpus matrix，而非独立相似度。[[evidence:ev-p088-joint-nonnegative-objective]]

## Evidence-backed findings
[AUTHOR_FACT] 作者报告相关集合越大，NNN 与 dense retrieval 的差距越大。[[evidence:ev-p088-relevant-set-size-signature]]
[CODEX_SYNTHESIS] 这是与 residual mechanism 一致的 signature，不是直接测得的 causal mediation，也不支持所有数据集/指标的统一优势。

## Limitations and failure signals
[AUTHOR_FACT] 理论是 per-query hyperparameter existence，部署却在验证集选全局参数；全语料求解与 unrolled training 存在 scale/memory 限制。[[evidence:ev-p088-theory-deployment-scale-boundary]]
[CODEX_SYNTHESIS] 主实验 corpus 最大 1,651 项；Completeness 只验证标注集合，不等价于通用 diversity、可执行性或答案正确性。

## Lineage and baselines
[CODEX_SYNTHESIS] 后续 diversity reranker、set retrieval 或 residual decoding Candidate 必须纳入 dense、MMR、COLT 与 NNN closest composition，并核算全语料 compute。

## Evidence ledger
[CODEX_SYNTHESIS] 精确 objective、relevant-set-size signature、理论/部署/规模边界均绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] NNN retrieval; non-negative elastic net; joint sparse reconstruction; residual decoding; complementary tool set; redundant near neighbours; support recovery; per-query hyperparameters; full-corpus FISTA; completeness
