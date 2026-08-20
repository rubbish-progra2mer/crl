<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-fixed-budget-independent-path-aggregation","card_kind":"operator","paper_id":"P081","evidence_ids":["ev-p081-independent-path-majority-aggregation","ev-p081-forty-sample-baseline","ev-p081-fixed-answer-space-boundary"],"source_refs":[{"path":"papers/P081_self_consistency.pdf","sha256":"1a49ce0373afc89d2d6e97fb1aa8230f6b818c70590d732a3187f753f4df6aba"}]} -->
# Fixed-Budget Independent-Path Aggregation

## Intervention target
[CODEX_SYNTHESIS] test-time answer selection，作为 interactive reflection/search/multi-Agent 方法必须击败的 compute baseline。

## Before and after computation
[AUTHOR_FACT] greedy single path → 独立采样多条 reasoning paths，丢弃路径身份并按最终答案一致性聚合。[[evidence:ev-p081-independent-path-majority-aggregation]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为同一 prompt 与固定样本预算；输出为各路径最终答案及其聚合结果，整个过程无路径间通信。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 独立 path diversity 能平均掉单次 reasoning error，构成“更多候选”解释的最小充分基线。

## Predicted observable signature
[CODEX_HYPOTHESIS] 若所谓 Agent 机制只增加候选数，其收益会在相同模型、prompt、总候选与近似 token budget 的独立采样基线下消失。

## Preconditions and transfer risks
[AUTHOR_FACT] 主结果使用 40 个样本对 greedy baseline。[[evidence:ev-p081-forty-sample-baseline]] [AUTHOR_FACT] 直接形式需要固定答案集。[[evidence:ev-p081-fixed-answer-space-boundary]] [CODEX_SYNTHESIS] equal candidates 不自动等于 equal tokens、latency 或 tool calls。

## Source lineage
[CODEX_SYNTHESIS] P081 的经典 self-consistency 原样机制化，作为复杂 Agent test-time computation 的 comparator。

## Evidence ledger
[CODEX_SYNTHESIS] aggregation、sample count 与 answer-space boundary 分别绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] independent sampling baseline; self consistency; equal candidate budget; majority vote; test-time compute control
