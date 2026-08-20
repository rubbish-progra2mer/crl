<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-paired-single-factor-bias-decomposition","card_kind":"operator","paper_id":"P093","evidence_ids":["ev-p093-paired-protocol","ev-p093-foil-collapse"],"source_refs":[{"path":"papers/P093_dense_retriever_collapse.pdf","sha256":"e62a61bf3e0bfbfcbd08f9fe09cdb29079f9e87035c32b3ee7eee89df1630fb1"}]} -->
# Paired Single-Factor Document Construction for Retriever Bias Decomposition

## Intervention target
[CODEX_SYNTHESIS] 检索器行为的归因测量：把"检索分数为何偏离事实相关性"分解为可分别操纵的偏差因素。

## Before and after computation
[AUTHOR_FACT] 关系抽取数据（Re-DocRED）映射为查询模板；每查询构造 D1/D2 文档对，只在一个因素上差异（答案在场/字面重合/长度/位置/重复），其余句子受控填充；每设定 250 查询做配对差分与 t 检验。[[evidence:ev-p093-paired-protocol]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：带证据句标注的关系数据集 + 因素定义。输出：每偏差的配对 t 统计与偏好率；组合电池（foil/poison）测叠加效应。时点：离线评测，任何打分器可插入。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 单因素对照使每个偏差的因果贡献可辩护（配对消除查询间方差）；这是把"检索器有偏"从轶事变成统计测量的最小协议。

## Predicted observable signature
[AUTHOR_FACT] 协议产出清晰分离：brevity/literal/position 最有害（Fig.1）；foil 叠加时 8 模型选含答案文档 <10%（配对 t −20.96~−42.25，Table 4）。[[evidence:ev-p093-foil-collapse]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 前提：证据句可自包含（head+tail 同句）且中性填充句可过滤。转移风险：成对打分不等于全库检索行为；合成模板查询与自然查询分布有距离；结论限被测打分器世代。

## Source lineage
[CODEX_SYNTHESIS] IR 探针/行为测试传统 → 本文单因素配对协议（正式发表锚），可作为时序检索残差分解的方法学模板。

## Evidence ledger
[AUTHOR_FACT] 协议构造与主测量绑定 exact Passage。[[evidence:ev-p093-paired-protocol]] [[evidence:ev-p093-foil-collapse]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] paired document construction; single-factor control; bias battery; foil composition; paired t-statistic; relation-to-query template; controlled retrieval evaluation; controlled document pairs; isolating one retrieval bias factor; paired significance testing; attributing retriever bias; constructing biased and answer-bearing pairs
