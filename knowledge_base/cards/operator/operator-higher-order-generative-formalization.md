<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-higher-order-generative-formalization","card_kind":"operator","paper_id":null,"evidence_ids":["ev-p053-higher-order-generator","ev-p053-python-to-pddl-pipeline","ev-p053-pattern-review-confound","ev-p053-parser-evaluation-boundary"],"source_refs":[{"path":"papers/P053_higher_order_planning_formalizers.pdf","sha256":"224970784bd45edc3191b71c2aadd81e01f5869fcd004c4fa10bac4ed1217b19"}]} -->
# Higher-Order Generative Formalization

## Intervention target
[CODEX_SYNTHESIS] 当自然语言规格很短、但其 grounded formal representation 随对象或关系规模迅速扩张时，避免让 LLM 逐项枚举全部 facts。

## Before and after computation
[AUTHOR_FACT] 普通 Formalizer 直接输出完整 grounded instance；改变后由 LLM 输出紧凑 generator program，再执行程序生成 PDDL problem file。[[evidence:ev-p053-higher-order-generator]] [[evidence:ev-p053-python-to-pddl-pipeline]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入是自然语言 domain/problem、可信的 domain file 与 generator 运行接口；中间输出是可执行规则程序，最终输出仍是外部 planner 所需的 grounded formal instance。干预发生在 formal solver/search 之前。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 若错误主要来自长输出中的重复枚举、漏项和索引漂移，把模型的任务改成生成短的结构化规则，可使模型侧输出复杂度更接近描述规则数而不是 grounded fact 数。

## Predicted observable signature
[CODEX_HYPOTHESIS] 随 instance expansion ratio 增大，generator 方案相对普通 Formalizer 的精确 formalization 保持率应更稳定；优势应在去除额外 pattern review、匹配模型调用/token 和使用同一 planner/parser 后仍存在。论文主 H-O/普通 Formalizer 对比没有匹配 review；另有 Q25 pattern-review 消融，但没有形成四臂 matched-budget 分解。[[evidence:ev-p053-pattern-review-confound]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 重复关系必须能被短程序表达，运行环境必须受控，且生成程序的语义仍需核查。planner timeout 后的 parser exact match 只能证明 formal instance 一致，不能替代端到端 solver scalability。[[evidence:ev-p053-parser-evaluation-boundary]]

## Source lineage
[CODEX_SYNTHESIS] P054 complete PDDL Formalizer → P053 generator representation。changed computation 位于表示展开层，而不是再加一个 self-review。

## Evidence ledger
[CODEX_SYNTHESIS] Operator 只吸收 representation change；two-stage pattern review 作为混杂记录，不升级为第二个 Operator。[[evidence:ev-p053-higher-order-generator]] [[evidence:ev-p053-python-to-pddl-pipeline]] [[evidence:ev-p053-pattern-review-confound]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] output expansion; compact generator; higher-order representation; grounded formalization; compiler intermediate representation; symbolic instance generation
