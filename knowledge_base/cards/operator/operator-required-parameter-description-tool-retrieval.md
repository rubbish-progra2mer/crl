<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-required-parameter-description-tool-retrieval","card_kind":"operator","paper_id":"P086","evidence_ids":["ev-p086-hypothesize-retrieve-invoke","ev-p086-required-parameter-score","ev-p086-near-identical-distribution"],"source_refs":[{"path":"papers/P086_meta_tool.pdf","sha256":"02064499a8345eb333e4fdd71abaa5ee69133af5be7b81626ba09816f48d194b"}]} -->
# Hypothesize–Retrieve–Invoke with Required-Parameter Description Matching

## Intervention target
[CODEX_SYNTHESIS] open-world Agent 在 invocation 前的 tool retrieval decision，特别是功能描述相近但 required parameter semantics 不同的候选。

## Before and after computation
[CODEX_SYNTHESIS] dialogue/query 直接对 tool name/description 独立打分 → LLM 先生成 desired tool 与 required-parameter descriptions，再组合 tool-level 与 parameter-level similarity 排名。[[evidence:ev-p086-hypothesize-retrieve-invoke]] [[evidence:ev-p086-required-parameter-score]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为对话上下文和静态 tool definitions；中间表示是 hypothesized interface；输出是 invocation 前的 top-k real tools。该 Operator 不读取真实执行结果。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 当 query 没直接说出接口词、而相近工具在 required parameter semantics 上可区分时，参数描述匹配提供 tool-description-only score 缺失的 discriminative signal。

## Predicted observable signature
[CODEX_HYPOTHESIS] 在保持 model、candidate pool、top-k 与 token/call budget 可比时，hard function-missing retrieval hit 应提高；提升应集中在 parameter-description 可区分的 pairs，而非只提高 JSON validity。

## Preconditions and transfer risks
[AUTHOR_FACT] Meta-Bench 与训练数据分布近乎相同，且相似工具可跨 split。[[evidence:ev-p086-near-identical-distribution]]
[CODEX_SYNTHESIS] 独立 max-match 允许一个 candidate parameter 重复解释多个 query parameters；Operator 不编码类型、枚举、值、nested schema 或 cross-parameter constraint，也不证明调用后的 semantic correctness。

## Source lineage
[CODEX_SYNTHESIS] 从 P086 Meta-Tool 抽象；它是参数/契约感知 router 的 nearest component，而非普通 keyword、schema validation 或 output repair。

## Evidence ledger
[CODEX_SYNTHESIS] framework、精确 combined score 与 distribution boundary 均绑定当前 Passage SHA。

## Retrieval vocabulary
[CODEX_SYNTHESIS] required parameter matching; parameter description retrieval; hypothesized interface; open-world tool routing; Meta-Tool; schema-aware closest comparator; pre-invocation tool selection
