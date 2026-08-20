<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-large-corpus-tool-retrieval-breaks-oracle-menu","card_kind":"failure","paper_id":"P085","evidence_ids":["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"],"source_refs":[{"path":"papers/P085_toolret.pdf","sha256":"26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a"}]} -->
# Large-Corpus Tool Retrieval Breaks the Oracle-Menu Assumption

## Observed failure
[AUTHOR_FACT] 在 43,215-tool merged corpus 上，作者报告所有 query-only retrievers 的 Completeness@10 低于 35%、Recall@10 低于 52%。[[evidence:ev-p085-large-corpus-scale]] [[evidence:ev-p085-retrieval-completeness-failure]]

## Conditions and scope
[CODEX_SYNTHESIS] 该 Failure 针对英语、文本、one-shot retrieval 与继承的 target-tool labels；它不意味着每个 production registry 都有相同绝对分数。

## Failed intervention
[CODEX_SYNTHESIS] 在 oracle 或 tiny preselected menu 上改进 function-call syntax/validity，然后把结果外推成 open-world tool selection 能力。

## Evidence and alternative explanations
[AUTHOR_FACT] 合并来源造成 one-to-many label 问题：其他数据集里的相似工具可能也是有效解。[[evidence:ev-p085-non-exhaustive-label]]
[CODEX_SYNTHESIS] 因而低 retrieval score 同时包含真实 selection failure 与 metric false negative；target-aware instructions 又包含标签侧信息。不能把单一指标差异直接解释成 semantic correctness。

## Warning for future candidates
[CODEX_SYNTHESIS] 工具路由 Candidate 必须明确 candidate universe，纳入 full-corpus/strong learned retriever，报告 target-set completeness、实际 selection、argument、execution 与 task success；oracle-menu 正向不能作为 Delivery 证据。

## Possible repair boundary
[CODEX_HYPOTHESIS] learned tool-specific retrieval、parameter-aware matching、document enrichment 或 joint-set decoding均可作为 comparator/repair family，但任何一个都必须单独证明其 changed computation 与 end-to-end failure 对齐。

## Evidence ledger
[CODEX_SYNTHESIS] corpus scale、complete-set failure 与 non-exhaustive-label boundary 分别绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] oracle tool menu failure; large tool registry; open-world tool retrieval; incomplete target set; missing required tool; TOOLRET; full corpus comparator; non-exhaustive relevance labels
