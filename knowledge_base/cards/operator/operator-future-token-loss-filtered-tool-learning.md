<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-future-token-loss-filtered-tool-learning","card_kind":"operator","paper_id":"P082","evidence_ids":["ev-p082-future-token-loss-filtered-calls","ev-p082-top-k-single-call-boundary","ev-p082-chaining-cost-sparsity-boundary"],"source_refs":[{"path":"papers/P082_toolformer.pdf","sha256":"6d7483d94653008e40c2058a1c22441c92e3713dae278b6361e8efc447c99522"}]} -->
# Future-Token-Loss-Filtered Tool Learning

## Intervention target
[CODEX_SYNTHESIS] 训练语料中的 tool-call placement、arguments 与 retained supervision。

## Before and after computation
[CODEX_SYNTHESIS] 少量 API demonstrations → 模型生成并执行候选 calls → 仅保留降低后续 token loss 的 calls → 在插入结果的语料上微调。[[evidence:ev-p082-future-token-loss-filtered-calls]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入是预训练文本、少量 API 示例及执行结果；输出是带调用监督的增强文本与微调后 LM，调用筛选发生在训练前处理。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 模型自身 future-token loss 可作为无需任务标签的 call placement 与 argument utility proxy。

## Predicted observable signature
[CODEX_HYPOTHESIS] 在无需任务级标签时学出稀疏 call preference；但 downstream Agent success 未必随 language-model likelihood 同步。

## Preconditions and transfer risks
[AUTHOR_FACT] 推理在 `<API>` token 进入 top-10 候选时允许触发，且每输入最多一次调用。[[evidence:ev-p082-top-k-single-call-boundary]] [AUTHOR_FACT] 不支持 chaining/interactive refinement，样本可极稀疏且不计调用成本。[[evidence:ev-p082-chaining-cost-sparsity-boundary]] [CODEX_SYNTHESIS] controller 是 GPT-J-6.7B，但完整系统还调用 Atlas QA、Wikipedia BM25、NLLB 等外部工具；部分任务调用率接近 98%，不能把 controller 参数量或自然 top-1 calibration 当作完整系统预算。

## Source lineage
[CODEX_SYNTHESIS] 从 P082 Toolformer 原样抽象，是 self-supervised tool-learning 的早期代表性方法；“直接祖先”关系需在具体 Candidate 的 nearest-prior 谱系中另行核验。

## Evidence ledger
[CODEX_SYNTHESIS] data construction、inference 与 limitation 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] Toolformer operator; future token likelihood utility; self-supervised API calls; single-call limitation; tool cost mismatch
