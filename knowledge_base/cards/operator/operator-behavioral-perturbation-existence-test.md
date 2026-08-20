<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-behavioral-perturbation-existence-test","card_kind":"operator","paper_id":"P097","evidence_ids":["ev-p097-behavioral-perturbation","ev-p097-feasibility-gap"],"source_refs":[{"path":"papers/P097_reloop.pdf","sha256":"8563653b872e78822f024b4d2f11532f75354e98c729ed26ac5bbf9675724c66"}]} -->
# Behavioral Perturbation Testing: Test Whether Sensitivity Exists

## Intervention target
[CODEX_SYNTHESIS] 优化代码生成的验证时点：可行解已得、无 ground truth 时，如何获得语义级外部信号。

## Before and after computation
[AUTHOR_FACT] 把敏感性分析反用为验证：不解释敏感度数值，而测试敏感度是否存在——本应影响最优值的参数被极端扰动后目标零响应，指示缺失组件；绕过 LLM 自审、不需 ground truth。[[evidence:ev-p097-behavioral-perturbation]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：候选代码 + LLM 抽取的约束/目标项候选 + 类型化扰动因子（capacity ×0.001 / demand ×100 / cost ×0.001 / revenue ×100）。输出：分级判定（r<5% WARNING、5-30% INFO、>30% 或诱发 infeasible 为 PASS）。时点：L1 执行验证通过后，非阻断 + 保守修复（回归回滚 τr=4%）。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 缺失约束/目标项在参数空间留下"零敏感"指纹；极端扰动放大指纹使其可机器判读，solver 充当行为 oracle。

## Predicted observable signature
[CODEX_SYNTHESIS] MAMO 局部缺陷域 +4.4pp（其最大单项）；RetailOpt 结构性错误域零贡献——增益分布本身即机制签名。引用时连同重试预算混杂（无等预算对照）。

## Preconditions and transfer risks
[AUTHOR_FACT] 前提：缺陷局部可扰动；数据-代码分离（data["key"] 访问模式）使运行时扰动可行，抽取失败回退 AST 源码扰动；修复 LLM 会伪造数据（safety check 动因）。[[evidence:ev-p097-behavioral-perturbation]]（data-code 分离/AST 回退/伪造细节出自 §3.2、App.E.2、§3.4，PDF 直核）
[CODEX_SYNTHESIS] 该方法使用阈值规则裁决扰动响应；共享生成 LLM 的抽取步骤是作者承认的失败相关源。

## Source lineage
[CODEX_SYNTHESIS] 敏感性分析（经典 OR）→ 反用为存在性测试（本文自称 novel），形成认证掩盖测量的一类近邻机制。

## Evidence ledger
[AUTHOR_FACT] 核心思想与 gap 语境绑定 exact Passage。[[evidence:ev-p097-behavioral-perturbation]] [[evidence:ev-p097-feasibility-gap]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] behavioral verification; parameter perturbation; CPT OPT; sensitivity existence test; severity thresholds; conservative repair; regression rollback; IIS diagnostic recovery; perturbing a parameter that should change the optimum; zero objective response flags a missing component; expected sensitivity absent; perturbation-based verification; testing whether sensitivity exists; verifying formulations by perturbation without ground truth
