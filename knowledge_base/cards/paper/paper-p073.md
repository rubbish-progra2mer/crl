<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p073","card_kind":"paper","paper_id":"P073","evidence_ids":["ev-p073-execution-supervised-probe","ev-p073-internal-confidence-misalignment"],"source_refs":[{"path":"papers/P073_probecal.pdf","sha256":"2c56eb776ba9caf9dbe0663fdabbafc2941c10c08394494df158c5980090cc53"}]} -->
# Uncertainty Calibration for Tool-Using Language Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] 提供“用真实执行结果监督一个轻量 probe，再选择 prompt 与 trace”的正向 Operator，以及“内部置信度不等于执行成功率”的 Failure。

## Problem and setting
[AUTHOR_FACT] 文本形式相近但执行正确性不同的 traces，可能得到相近的未校准 uncertainty。[[evidence:ev-p073-internal-confidence-misalignment]]

## Changed computation
[AUTHOR_FACT] ProbeCal 以 LLM embeddings 为输入、执行结果为监督训练 MLP，并用校准概率选择 prompt 与 execution trace。[[evidence:ev-p073-execution-supervised-probe]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 证据支持 supervised outcome probe 改变候选选择，不支持把模型自报 confidence 直接当作成功概率。

## Limitations and failure signals
[CODEX_SYNTHESIS] 训练需要带答案的执行结果，主要证据来自数学/表格代码工具任务；它不是 oracle-free、online 或零样本校准。

## Lineage and baselines
[CODEX_SYNTHESIS] 最近基线是 token logit aggregation、temperature scaling、uniform trace selection 与 self-consistency；核心差异是额外 outcome-supervised probe。

## Evidence ledger
[CODEX_SYNTHESIS] 一条 Evidence 固定监督计算，一条固定未校准 Failure。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool calibration; execution supervised probe; prompt selection; trace selection; hidden embedding confidence; outcome probability
