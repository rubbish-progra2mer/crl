<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-interactive-gains-collapse-against-independent-sampling","card_kind":"failure","paper_id":"P081","evidence_ids":["ev-p081-independent-path-majority-aggregation","ev-p081-forty-sample-baseline","ev-p081-fixed-answer-space-boundary"],"source_refs":[{"path":"papers/P081_self_consistency.pdf","sha256":"1a49ce0373afc89d2d6e97fb1aa8230f6b818c70590d732a3187f753f4df6aba"}]} -->
# Interactive Gains Can Collapse Against Independent Sampling

## Observed failure
[CODEX_HYPOTHESIS] reflection、debate、tree search 或 multi-Agent 方法若只与 greedy 单路径比较，正向可能来自更多 samples 而非交互计算；P081 本身没有实验这些 interactive methods。

## Conditions and scope
[CODEX_SYNTHESIS] 当复杂方法使用相同模型但获得更多 generations、tokens 或 tool calls，且 comparator 仍为 greedy 时风险最高。

## Failed intervention
[CODEX_SYNTHESIS] 仅与 greedy single path 比较不能识别交互机制贡献。

## Evidence and alternative explanations
[AUTHOR_FACT] Self-consistency 以独立路径最终答案聚合改变单路径 decoding。[[evidence:ev-p081-independent-path-majority-aggregation]] [AUTHOR_FACT] 其主结果每 run 用 40 samples 对 greedy CoT。[[evidence:ev-p081-forty-sample-baseline]]

## Warning for future candidates
[AUTHOR_FACT] 原始聚合需要 fixed answer set 或额外一致性度量。[[evidence:ev-p081-fixed-answer-space-boundary]] [CODEX_SYNTHESIS] 对开放文本还需冻结 judge/parser，避免 hidden oracle。
[CODEX_SYNTHESIS] 至少加入相同模型、prompt、candidate count 与近似 token/tool-call budget 的 independent sampling；equal candidates 不应偷换成 equal compute。

## Possible repair boundary
[CODEX_HYPOTHESIS] 在 frozen aggregator 且严格匹配 candidate/token/tool-call budget 后仍存在的残余增益，可作为 interaction contribution 的证据，但不是唯一因果归因证明；prompt、parser 与其他组件差异仍需隔离。

## Evidence ledger
[CODEX_SYNTHESIS] independent aggregation、sample budget 与 applicability boundary 均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] independent sampling comparator; interaction ablation; self consistency baseline; more tokens confound; equal compute Agent evaluation
