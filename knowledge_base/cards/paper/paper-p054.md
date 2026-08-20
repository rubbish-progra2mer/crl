<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p054","card_kind":"paper","paper_id":"P054","evidence_ids":["ev-p054-complete-pddl-formalizer","ev-p054-model-conditional-advantage","ev-p054-natural-language-implicit-predicate-failure","ev-p054-plan-validation-boundary"],"source_refs":[{"path":"papers/P054_planning_formalizer_limits.pdf","sha256":"f1e766c715ddaef8b671a9176c75c65759ddf09316dffd8ea32eab4a2c05a5a1"}]} -->
# On the Limit of Language Models as Planning Formalizers

## Role in the knowledge base
[CODEX_SYNTHESIS] P053 的直接机制祖先和 planning 簇强 baseline：要求 LLM 从自然语言恢复完整 PDDL domain/problem，而不是只补一个 goal 或部分文件。

## Problem and setting
[CODEX_SYNTHESIS] 四个 fully observed classical-planning domains，描述从高度模板化到更自然；外部 planner 负责搜索，VAL 依据 ground-truth dynamics 验证最终 plan。

## Changed computation
[AUTHOR_FACT] 自然语言 domain/problem descriptions 先被转换为 PDDL domain/problem files，再交给 planner 找 plan。[[evidence:ev-p054-complete-pddl-formalizer]]

## Evidence-backed findings
[AUTHOR_FACT] 在 BlocksWorld-100 等部分模型/域上，GPT-4o formalizer 显著超过 direct Planner；但 o3-mini 是反例，不能把优势推广到所有模型。[[evidence:ev-p054-model-conditional-advantage]]

## Limitations and failure signals
[AUTHOR_FACT] 更自然的描述会省略人类可推断的 `clear` 等 predicate，模型遗漏后会产生 unsolvable PDDL 或错误计划。[[evidence:ev-p054-natural-language-implicit-predicate-failure]] [AUTHOR_FACT] 生成 PDDL 不要求与唯一 ground truth 文本相同，而是通过最终 plan 验证，避免错杀等价 formalization。[[evidence:ev-p054-plan-validation-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] direct Planner → complete PDDL Formalizer → P055 constraint stress → P053 higher-order representation。本文只使用 straightforward direct Planner 作为主对照，未来 Candidate 还需面对 iterative/symbolically validated Planner。

## Evidence ledger
[CODEX_SYNTHESIS] 本卡不把“formalizer often wins”扩写为普遍规律；模型、描述自然度、domain complexity 和未匹配预算都是 source-level 边界。[[evidence:ev-p054-model-conditional-advantage]] [[evidence:ev-p054-natural-language-implicit-predicate-failure]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] complete PDDL formalization; domain file; problem file; natural-language planning; implicit predicate omission; planner versus formalizer; VAL validation
