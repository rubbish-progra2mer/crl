<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-generator-aligned-verification-passes-shared-misreads","card_kind":"failure","paper_id":"P096","evidence_ids":["ev-p096-shared-misinterpretation","ev-p096-simplification-inversion"],"source_refs":[{"path":"papers/P096_verisimpl.pdf","sha256":"81b34a7084aa5552ef9a1491ec5e5f9da5c149e80beb06fe81fc163ae4d595b3"}]} -->
# Generator-Aligned Verification Passes Shared Misinterpretations

## Observed failure
[AUTHOR_FACT] VeriSimpl 自报失败案例：自然语言规格的同一误读使符号形式化与 LLM 具体推理一致同意同一个错误模型（如班车 "start time" 变量语义、profit 目标漏成本项）——模型内部自洽，验证因 LLM 推理与 solver 输出一致而通过；决策变量被假定为给定共享，完全被遗漏的 NL 方面不产生任何简化查询。[[evidence:ev-p096-shared-misinterpretation]]

## Conditions and scope
[CODEX_SYNTHESIS] ICML 2026 正式发表；NL→优化建模，solver 构造降维简化查询、LLM 裁决，三路信号（约束突变/变量掩码/类型检查）字典序聚合的 best-of-K 选择器；裁决者与生成者同为 LLM（生成对齐裁决）。[[evidence:ev-p096-simplification-inversion]]

## Failed intervention
[CODEX_SYNTHESIS] 用"生成侧 LLM 对 solver 降维查询的裁决"作为正确性验证——共享误解时裁决与形式化同错，all-pass 反而给出高置信信号。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] reconciliation 记录的发表版自带缺陷连带引用：best-of-K 混杂（任一单信号 10 候选选择器已达 62.2-64.8 vs BASELLM 56.8，验证信号叠加边际仅 ~0.7-3.3 点，无算力配平对照）；CompOR 列仅 n=17；A.2/A.3 案例 transcript 与题目数值不符（不作机制证据）。

## Warning for future candidates
[CODEX_SYNTHESIS] 任何“LLM 裁决探针”路线都必须回答共享误解假阳性；采用独立参考检查器时，裁决者独立性是关键区分。补充对照应以本文 Algorithm 2 为实现依据并做算力配平。

## Possible repair boundary
[CODEX_HYPOTHESIS] 裁决者与生成者解耦（独立参考实现、跨模型裁决、人类锚点）是未被本文占据的修复方向；仅换更强同侧 LLM 不改变失败结构。

## Evidence ledger
[CODEX_SYNTHESIS] 共享误解失败自认与机制定义绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] shared misinterpretation; generator-aligned adjudication; verification false positive; simplification query; best-of-K confound; self-verification precision; VeriSimpl; verification passes a wrong formulation; shared misinterpretation of the specification; self-verification false positives; generator and verifier agreeing on the same wrong model
