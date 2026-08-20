<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p086","card_kind":"paper","paper_id":"P086","evidence_ids":["ev-p086-hypothesize-retrieve-invoke","ev-p086-required-parameter-score","ev-p086-near-identical-distribution"],"source_refs":[{"path":"papers/P086_meta_tool.pdf","sha256":"02064499a8345eb333e4fdd71abaa5ee69133af5be7b81626ba09816f48d194b"}]} -->
# Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models

## Role in the knowledge base
[CODEX_SYNTHESIS] required-parameter-description-aware retrieval 的直接先行；是任何“利用 schema/参数语义改进工具路由”Candidate 的 mandatory closest-composition comparator。

## Problem and setting
[AUTHOR_FACT] Meta-Tool 让 LLM 先描述所需工具及参数，再检索真实工具并调用。[[evidence:ev-p086-hypothesize-retrieve-invoke]]

## Changed computation
[AUTHOR_FACT] 检索分数结合 tool-description similarity 与每个 hypothesized required parameter 对候选 required parameters 的 best-match similarity 均值。[[evidence:ev-p086-required-parameter-score]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 方法在 invocation 之前改变 candidate tool ranking，因此不是 output validation，也不能被“先做 JSON 合法性检查”视为同一比较。

## Limitations and failure signals
[AUTHOR_FACT] Meta-Bench 与训练集对话不重叠，但分布近乎相同，且相同/相似功能工具可能同时出现。[[evidence:ev-p086-near-identical-distribution]]
[CODEX_SYNTHESIS] 参数计算只使用 required-parameter 的自然语言描述和独立 max pooling；不处理类型、枚举、默认值、nested schema、具体用户值、跨参数约束或真实执行结果。

## Lineage and baselines
[CODEX_SYNTHESIS] 比 dialogue-history/keyword retrieval 更接近 schema-aware routing；未来 delta 必须相对 tool-only Meta-Tool full computation 明确，而不能只换 prompt 或字段名称。

## Evidence ledger
[CODEX_SYNTHESIS] framework、精确 score computation 与同分布边界均绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] Meta-Tool; hypothesize retrieve invoke; required parameter descriptions; parameter-aware tool retrieval; open-world function calling; best-match parameter similarity; schema-aware retrieval closest prior
