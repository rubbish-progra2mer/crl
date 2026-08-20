<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-joint-nonnegative-residual-retrieval","card_kind":"operator","paper_id":"P088","evidence_ids":["ev-p088-joint-nonnegative-objective","ev-p088-relevant-set-size-signature","ev-p088-theory-deployment-scale-boundary"],"source_refs":[{"path":"papers/P088_nnn_retrieval.pdf","sha256":"adb67ce1c663402dc988cd9de4df891a1e6f540cf41011cd21e406da32ce636e"}]} -->
# Joint Non-Negative Residual Retrieval

## Intervention target
[CODEX_SYNTHESIS] 多工具/多文档 retrieval 的 set decoder：独立 top-k 会让相关近重复项共同占位，挤掉互补 target。

## Before and after computation
[CODEX_SYNTHESIS] 每个 item 只按 query similarity 独立排名 → 以完整 corpus matrix 对 query 做 sparse non-negative elastic-net reconstruction，并按非零系数联合选择 support。[[evidence:ev-p088-joint-nonnegative-objective]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入是预计算 corpus embeddings 与 query embedding；输出是共同求解的 support/ranking。每个 query 的解码在完整 corpus 上迭代，不是 ANN top-k 后的免费去重。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 一个已选 item 解释 query 的一部分后，与其相关的候选面对剩余 residual，因而互补项更可能进入有限 top-k。

## Predicted observable signature
[AUTHOR_FACT] 作者报告差距随 relevant-set size 增大。[[evidence:ev-p088-relevant-set-size-signature]]
[CODEX_HYPOTHESIS] 更严格验证应直接测量 redundant displacement、residual change 与 complete-set recovery，并和 dense/MMR/COLT 在相同 embeddings、k 与 compute 下比较。

## Preconditions and transfer risks
[AUTHOR_FACT] per-query theory 与 global deployment 参数不一致；full-corpus passes 和 unrolled training 限制规模。[[evidence:ev-p088-theory-deployment-scale-boundary]]
[CODEX_SYNTHESIS] 标签 completeness 不等于通用 diversity 或可执行性；NNN-FIX 并非每个数据集/指标都占优，NNN-TR 又加入训练变化。

## Source lineage
[CODEX_SYNTHESIS] 从 P088 抽象；是任何 residualized sparse decoding、joint set selection、diversity retrieval Candidate 的 mandatory closest-composition comparator。

## Evidence ledger
[CODEX_SYNTHESIS] exact objective、set-size signature 与 theory/deployment/scale boundary 均绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] joint set retrieval; non-negative elastic net; residualized decoding; complementary tool recovery; redundant top-k; sparse support; FISTA; completeness; MMR comparator; full-corpus compute
