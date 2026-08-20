<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-solver-simplification-query-verification","card_kind":"operator","paper_id":"P096","evidence_ids":["ev-p096-simplification-inversion","ev-p096-shared-misinterpretation"],"source_refs":[{"path":"papers/P096_verisimpl.pdf","sha256":"81b34a7084aa5552ef9a1491ec5e5f9da5c149e80beb06fe81fc163ae4d595b3"}]} -->
# Solver-Generated Simplification Queries with LLM Adjudication

## Intervention target
[CODEX_SYNTHESIS] NL→优化形式化的验证时点：谁出测试、谁裁决。

## Before and after computation
[AUTHOR_FACT] 反转常规验证流：不让 LLM 提出测试场景再交 solver 检查，而是利用 solver 在高维空间构造可行/最优解的可靠性，沿约束与决策变量维度降维，产出保持全局语义结构的简化诊断查询，交给 LLM 推理裁决。[[evidence:ev-p096-simplification-inversion]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：候选形式化 + 原 NL 描述 + solver。输出：feasibility/optimality 探针裁决序列 + all-pass 高置信门控信号。时点：生成后、提交前（选择器/自验证两用）。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 降维查询把"验证整个模型"变成"验证 LLM 可推理的低维性质"；solver 出题避免 LLM 自产测试的覆盖性缺陷。

## Predicted observable signature
[CODEX_SYNTHESIS] 自验证门控的高 precision（91.5% GPT-4o）低覆盖（23-34%）——all-pass 严格性使 2/3 正确解无标记；增益引用必须连同 best-of-K 混杂（无算力配平对照，单信号选择器已捕获大部分增益）。

## Preconditions and transfer risks
[AUTHOR_FACT] 结构性边界（作者自认）：决策变量语义被假定共享，简化查询不覆盖候选完全遗漏的 NL 方面——共享误解穿透验证。[[evidence:ev-p096-shared-misinterpretation]]
[CODEX_SYNTHESIS] 裁决者与生成者同 LLM 是失败相关源；迁移到其他载体需 solver 类可靠 witness 生成器在场。

## Source lineage
[CODEX_SYNTHESIS] LLM 自产测试线 → solver 出题反转（本文）；若采用独立参考检查器，裁决者独立性是相对于生成对齐 LLM 的关键区别。

## Evidence ledger
[AUTHOR_FACT] 反转机制定义与结构性边界绑定 exact Passage。[[evidence:ev-p096-simplification-inversion]] [[evidence:ev-p096-shared-misinterpretation]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] simplification-based verification; solver-generated queries; constraint mutation; variable masking; feasibility probe; optimality probe; all-pass gating; lexicographic selection; solver-generated diagnostic queries; simplified feasibility and optimality probes; LLM-adjudicated verification; verifying by reducing problem complexity
