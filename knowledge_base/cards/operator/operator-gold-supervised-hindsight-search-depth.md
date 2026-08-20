<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-gold-supervised-hindsight-search-depth","card_kind":"operator","paper_id":"P080","evidence_ids":["ev-p080-gold-supervised-minimal-depth","ev-p080-fixed-depth-under-over-search","ev-p080-shallow-depth-boundary"],"source_refs":[{"path":"papers/P080_autosearch.pdf","sha256":"ab078ee4e0221166d92ea3856d028f92a9348899f8fa9d63ec8841764edd8a86"}]} -->
# Gold-Supervised Hindsight Search-Depth Shaping

## Intervention target
[CODEX_SYNTHESIS] Agentic RAG policy 的 continue-search/answer computation。

## Before and after computation
[CODEX_SYNTHESIS] 固定搜索深度或仅按最终正确性训练 → 每步生成 intermediate answer，以 gold 判断最早正确深度，再分别塑形有效、过度与不足搜索。[[evidence:ev-p080-gold-supervised-minimal-depth]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 训练输入含逐步 trajectory、intermediate answers 与 gold；输出是对 continue/stop search policy 的 stepwise rewards。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 策略应随问题与模型能力选择不同深度，同时降低 over-search ratio；固定深度的任务/模型异质性提供机制动机。[[evidence:ev-p080-fixed-depth-under-over-search]]

## Predicted observable signature
[CODEX_HYPOTHESIS] 在保持 answer quality 时平均 depth 与 OSR 下降，且不同难度问题获得不同深度。

## Preconditions and transfer risks
[AUTHOR_FACT] 研究只覆盖较低最大步数。[[evidence:ev-p080-shallow-depth-boundary]] [CODEX_SYNTHESIS] 诊断与训练提示覆盖 0–4 searches，不能外推到 long-horizon、branching 或 open-web stopping；失败轨迹的 `t_c=-1` 与 prose 中 `t_c>T` 还存在形式化歧义。名称必须保留 gold-supervised/hindsight，不能把训练标签误写成部署时可见信号。平均 search depth 只是代理成本，每步 intermediate answer、PPO 训练与 retrieval latency 未计入，论文没有证明 net deployment cost reduction。

## Source lineage
[CODEX_SYNTHESIS] 从 P080 抽象；属于 adaptive Agentic RAG 与 test-time compute allocation。

## Evidence ledger
[CODEX_SYNTHESIS] training label、failure motivation 与 range boundary 均绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] hindsight search depth; gold-supervised stopping; intermediate answer reward; over-search penalty; adaptive agentic RAG
