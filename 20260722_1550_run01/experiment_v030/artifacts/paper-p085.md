<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p085","card_kind":"paper","paper_id":"P085","evidence_ids":["ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"],"source_refs":[{"path":"papers/P085_toolret.pdf","sha256":"26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a"}]} -->
# Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models

## Role in the knowledge base
[CODEX_SYNTHESIS] 大规模开放工具检索的直接 Failure 与 baseline 来源；它阻止 CRL 用 oracle/tiny menu 的 function-calling 结果替代真实 retrieval stage。

## Problem and setting
[AUTHOR_FACT] TOOLRET 含 7,615 个 retrieval tasks 与 43,215 个合并工具，覆盖 Web API、Code Function 与 Customized App。[[evidence:ev-p085-large-corpus-scale]]

## Changed computation
[CODEX_SYNTHESIS] 论文主要改变 evaluation candidate universe，并比较通用、重排和 tool-specific learned retrieval；CRL 不从内部冲突的 hard-negative 数量/矿工细节抽取可复现 Operator。

## Evidence-backed findings
[AUTHOR_FACT] query-only 主结果中，作者报告全部检索器的 Completeness@10 低于 35%，Recall@10 低于 52%。[[evidence:ev-p085-retrieval-completeness-failure]]
[CODEX_SYNTHESIS] 这证明 complete target-set recovery 是独立瓶颈，不证明检索指标提高后参数、执行或最终答案必然正确。

## Limitations and failure signals
[AUTHOR_FACT] 合并多个来源后，其他数据集里的相似工具可能是有效替代，却不在当前 query 的原始标签内。[[evidence:ev-p085-non-exhaustive-label]]
[CODEX_SYNTHESIS] target-aware instruction 使用标签侧工具描述；hard-negative miner/count 在 PDF 内冲突；ToolBench pass rate 也没有分解 retrieval、planning、argument、execution 与 answer synthesis。

## Lineage and baselines
[CODEX_SYNTHESIS] P085 把 P084 的小菜单 interference 推进到 43k 规模 retrieval；未来工具选择 Candidate 至少需要 full-corpus retriever、complete-set metric 与 closest learned-retriever baseline。

## Evidence ledger
[CODEX_SYNTHESIS] 规模、query-only complete-set failure 与非穷尽标签风险分别绑定 exact Passage；争议训练配方未进入正式 claim。

## Retrieval vocabulary
[CODEX_SYNTHESIS] TOOLRET; large tool corpus retrieval; oracle menu assumption; complete target tool set; Completeness@10; retrieval bottleneck; non-exhaustive labels; alternative valid tools; learned tool retriever baseline
