<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-labeled-probe-injection-dual-verifier","card_kind":"operator","paper_id":"P098","evidence_ids":["ev-p098-constraint-injection","ev-p098-nonbinding-blindness","ev-p098-diff-leak-550"],"source_refs":[{"path":"papers/P098_constraint_injection.pdf","sha256":"f73aaa44ab843311d0676030081b8f1b9e18f9e9bb0bb0b9a87c761917b43ab3"}]} -->
# Labeled-Probe Constraint Injection as Dual Verifier

## Intervention target
[CODEX_SYNTHESIS] 训练管线的接受信号：数据合成拒绝采样过滤器与 GRPO 逐 rollout 奖励中，"候选程序约束结构是否正确"如何机器判定。

## Before and after computation
[AUTHOR_FACT] INJ 算子：执行候选得 Gurobi 模型对象，复制后把目标替换为常数可行性目标、追加 probe-encoding 约束把带标签解注入候选变量空间，只解可行性查询（目标值忽略），solver 判定与标签比对。[[evidence:ev-p098-constraint-injection]]
[CODEX_SYNTHESIS] 双探针配对：可行探针 s+ 必须被接受（抓伪过约束）+ 单约束违反探针 s- 必须被拒绝（抓静默缺失）；与 DIFF 组成 dual verifier，同一实现过滤/奖励双用。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：候选代码 + 实例 + 带标签探针集（专家 gold 脚本作 oracle 生成）。输出：0/1 约束级正确性信号。时点：训练期两处（SFT 过滤样本级 + GRPO 奖励 rollout 级）；评测不用 INJ。

## Mechanism hypothesis
[AUTHOR_FACT] 非绑定约束错误在目标值上不可见但在可行性判定上可见——注入恰好激活该约束的解使其绑定。[[evidence:ev-p098-nonbinding-blindness]]

## Predicted observable signature
[AUTHOR_FACT] 信号净贡献被消融隔离：无注入臂（数据更大）SFT -2.86 / GRPO -4.00 平均 Pass@1；550/7347 泄漏被过滤器实际拦截。[[evidence:ev-p098-diff-leak-550]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 前提链（reconciliation 记录）：结构化 gold 参考在场（探针标签 oracle）、输出协议契约（变量命名/arc-first 索引 + node_id_map 回译）、退化修复封堵（同车绑定防拆路掩盖）、人工攻击算子目录。契约失配样本整类弃用（INJ 非全覆盖判定器，规模未报）；实例极小（客户 4-12）；载体 VRP。

## Source lineage
[CODEX_SYNTHESIS] 差分测试/answer-agreement 过滤线 → 带标签探针注入（本文）；认证时点审计与掩盖质量分解未被本文覆盖，且后者被作者列为开放问题。

## Evidence ledger
[AUTHOR_FACT] INJ 实现、失明动机、消融隔离绑定 exact Passage。[[evidence:ev-p098-constraint-injection]] [[evidence:ev-p098-nonbinding-blindness]] [[evidence:ev-p098-diff-leak-550]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] constraint injection; feasibility probe; one-constraint-violating probe; dual verifier; rejection sampling filter; GRPO reward; addConstr encoding; node_id_map; boundary tightening; injecting a labeled solution; constant-objective feasibility query; probe-based constraint verification; feasible and violating probes as filters and rewards; verifying the constraint set of generated code
