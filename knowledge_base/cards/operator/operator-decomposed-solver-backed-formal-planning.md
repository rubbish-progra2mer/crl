<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-decomposed-solver-backed-formal-planning","card_kind":"operator","paper_id":null,"evidence_ids":["ev-p051-formalization-pipeline","ev-p051-solver-guarantee-boundary","ev-p051-cost-boundary","ev-p052-decomposed-formalization","ev-p052-result-self-assessment","ev-p052-self-assessment-loop-limit","ev-p052-fixed-cross-task-examples","ev-p052-direct-code-smt-baselines"],"source_refs":[{"path":"papers/P051_formal_verification_planning.pdf","sha256":"ba9261d6d8fbf2b43817e57c29aa6ffacc0b14ef038e6c86a33f8780490bd365"},{"path":"papers/P052_llmfp.pdf","sha256":"e59c5c55b3befeeb4774a20990b8629f487e9fb1520cc2a953f041b7bb6fdaec"}]} -->
# Decomposed Solver-Backed Formal Planning

## Intervention target
[CODEX_SYNTHESIS] 在计划交付前，把组合约束推理从自由语言生成迁移到显式形式模型与 solver 搜索。

## Before and after computation
[CODEX_SYNTHESIS] 基线由 LLM 直接写计划，或按 P052 的 `Code SMT` 基线直接生成使用 Z3 的 Python 代码。改变后的计算先定义目标、变量与显隐约束，再生成可执行模型并调用 solver；P052 进一步把定义、表示和代码生成分开，并加入固定格式结果转换及最多五轮的同模型自评与修改。[[evidence:ev-p051-formalization-pipeline]] [[evidence:ev-p052-decomposed-formalization]] [[evidence:ev-p052-result-self-assessment]] [[evidence:ev-p052-self-assessment-loop-limit]] [[evidence:ev-p052-direct-code-smt-baselines]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入是自然语言请求、任务说明、可信数据或 API 与形式求解接口；输出是 solver 对已编码模型求得的计划，发生在最终计划交付前。P052 的跨任务性仍依赖固定结构示例。[[evidence:ev-p052-fixed-cross-task-examples]]

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 显式分解约束翻译并把组合搜索交给形式 solver，可减少语言空间中遗漏全局可行性的失败；收益应集中在可形式化的组合约束，而不是开放式偏好判断。

## Predicted observable signature
[CODEX_HYPOTHESIS] 在相同基础模型、任务信息和明确计算预算下，相比 Direct 与 `Code SMT`，结构化可行率应提高；剩余错误应更多集中于约束遗漏、误译、接口破坏或超时。P052 只证明这些基线共享输入信息，并未匹配调用、token 或时延预算。[[evidence:ev-p052-direct-code-smt-baselines]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] solver 的保证只覆盖实际编码的模型。该机制要求可形式化领域、可信接口和可接受的调用/solver 成本；P051 报告的多调用成本与时延说明比较必须公开预算。[[evidence:ev-p051-solver-guarantee-boundary]] [[evidence:ev-p051-cost-boundary]]

## Source lineage
[CODEX_SYNTHESIS] P051 专用自然语言到 solver 形式化 → P052 跨任务分解形式化。未来 Candidate 必须超越“再接一个 solver”或简单串联自评的 composition-only 变化。

## Evidence ledger
[CODEX_SYNTHESIS] 本卡把 P051 与 P052 视为方法谱系；下列全文 Evidence 分别支持流程、形式保证边界、成本、分解、五轮自评边界、固定跨任务示例和 Direct/Code SMT 基线定义。[[evidence:ev-p051-formalization-pipeline]] [[evidence:ev-p051-solver-guarantee-boundary]] [[evidence:ev-p051-cost-boundary]] [[evidence:ev-p052-decomposed-formalization]] [[evidence:ev-p052-result-self-assessment]] [[evidence:ev-p052-self-assessment-loop-limit]] [[evidence:ev-p052-fixed-cross-task-examples]] [[evidence:ev-p052-direct-code-smt-baselines]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] formalized planning; SMT; constraint decomposition; solver-backed search; Code-SMT; formalization pipeline; plan feasibility
