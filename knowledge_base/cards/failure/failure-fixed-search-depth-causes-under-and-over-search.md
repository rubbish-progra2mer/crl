<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-fixed-search-depth-causes-under-and-over-search","card_kind":"failure","paper_id":"P080","evidence_ids":["ev-p080-gold-supervised-minimal-depth","ev-p080-fixed-depth-under-over-search","ev-p080-shallow-depth-boundary"],"source_refs":[{"path":"papers/P080_autosearch.pdf","sha256":"ab078ee4e0221166d92ea3856d028f92a9348899f8fa9d63ec8841764edd8a86"}]} -->
# Fixed Search Depth Causes Both Under- and Over-Search

## Observed failure
[AUTHOR_FACT] 不同任务和模型在不同搜索深度达到峰值；超过近优深度可能增加 over-search ratio 并降低准确率。[[evidence:ev-p080-fixed-depth-under-over-search]]

## Conditions and scope
[CODEX_SYNTHESIS] 适用于 retrieval step 有成本且新增观察可能干扰答案的 Agentic RAG；不代表所有多步工具调用都应尽早停止。

## Failed intervention
[CODEX_SYNTHESIS] 对所有问题施加同一 search steps，会在简单问题浪费/干扰，在复杂问题提前终止。

## Evidence and alternative explanations
[AUTHOR_FACT] AutoSearch 用 gold 对每步 intermediate answer 进行 hindsight 标注，得到最早正确深度。[[evidence:ev-p080-gold-supervised-minimal-depth]]

## Warning for future candidates
[AUTHOR_FACT] 论文只研究较低最大步数。[[evidence:ev-p080-shallow-depth-boundary]] [CODEX_SYNTHESIS] 在线 Candidate 不能偷看 gold，且需对照同模型、同检索器、同总成本的 fixed/adaptive baselines。

## Possible repair boundary
[CODEX_HYPOTHESIS] 从部署时可观察的 sufficiency signal 选择 continue/stop；P080 只验证 gold-hindsight training，不证明该 oracle-free 方案。

## Evidence ledger
[CODEX_SYNTHESIS] failure、hindsight repair 与 depth range 均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] fixed search depth failure; over-searching; under-searching; adaptive retrieval stopping; gold hindsight oracle
