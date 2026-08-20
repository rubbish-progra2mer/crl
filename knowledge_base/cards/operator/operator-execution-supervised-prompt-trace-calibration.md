<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-execution-supervised-prompt-trace-calibration","card_kind":"operator","paper_id":"P073","evidence_ids":["ev-p073-execution-supervised-probe","ev-p073-internal-confidence-misalignment"],"source_refs":[{"path":"papers/P073_probecal.pdf","sha256":"2c56eb776ba9caf9dbe0663fdabbafc2941c10c08394494df158c5980090cc53"}]} -->
# Execution-Supervised Prompt-and-Trace Calibration

## Intervention target
[CODEX_SYNTHESIS] 干预 Agent 在多个 prompt 或 tool execution traces 之间的选择概率。

## Before and after computation
[AUTHOR_FACT] Before：未校准模型会给形式相近、正确性不同的 traces 相似 uncertainty。[[evidence:ev-p073-internal-confidence-misalignment]] After：训练 MLP 将 LLM embedding 映射到执行监督下的 calibrated probability。[[evidence:ev-p073-execution-supervised-probe]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 训练输入是候选 prompt/trace 的 embedding 与 ground-truth execution outcome；推理输入是不带标签的候选 embedding，输出为候选成功概率。prompt calibration 可影响生成前的 prompt allocation；trace rerank 发生在候选已生成和执行之后，因此不能减少这些候选的 tool calls。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 若内部表示包含“将来执行是否成功”的可分信息，监督 probe 能纠正 token-confidence 与任务结果的错位。

## Predicted observable signature
[CODEX_HYPOTHESIS] matched candidates 下 calibration error 与 task success 同时改善；换任务/模型后若只剩 calibration 数字改善而 task success 不变，则迁移失败。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 需要可获得的隐藏表示和可信执行标签；离线训练还需承担候选生成与执行预算。标签域、模型和工具分布变化会破坏 probe，不能把训练 oracle 隐藏为测试时能力。

## Source lineage
[CODEX_SYNTHESIS] 来源 P073；最近对照应含相同候选数的 self-consistency、logit confidence 与 temperature scaling。

## Evidence ledger
[CODEX_SYNTHESIS] 监督计算和未校准反例各一条 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] supervised calibration; execution reward probe; trace confidence; prompt allocator; hidden state success prediction
