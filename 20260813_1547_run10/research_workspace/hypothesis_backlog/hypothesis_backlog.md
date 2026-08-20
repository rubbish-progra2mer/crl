# Hypothesis Backlog — v001

## HB-001

- `hypothesis_id`: h-v001-002-proxy
- `linked_evidence`: `ev-p073-internal-confidence-misalignment`, `ev-p025-grouped-step-influence`
- `evidence_level`: C
- `linked_route_ids`: NONE
- `why_not_gap_matrix`: 证据只分别否定局部置信度并展示一般步骤影响估计，未证明“传播风险×可逆性”预测验证价值。
- `promotion_blocker`: 等预算故障对实验中，对真实边际验证价值的排序相关与终局改善。
- `validation_need`: 先做无需训练的合成可控故障对 Scratch，再在独立程序化终局环境做 Recorded/Formal。
- `owner_status`: 主研究者 draft h-v001-002

## HB-002

- `hypothesis_id`: h-v001-003-transfer
- `linked_evidence`: `ev-p030-recognition-application-gap`, `ev-p064-experience-following-error`
- `evidence_level`: C（迁移主张）
- `linked_route_ids`: NONE
- `why_not_gap_matrix`: 原始现象在智能体记忆中直接成立，但迁移到在线工具状态及局部后代回滚仍是推断。
- `promotion_blocker`: 工具轨迹分叉任务上，局部回滚相对全轨重试的独立终局收益与成本。
- `validation_need`: 依赖抽取误差压力测试、冲突信号非真值泄漏审计。
- `owner_status`: 主研究者 draft h-v001-003

## HB-003

- `hypothesis_id`: h-v001-001-non-isomorphic-check
- `linked_evidence`: `ev-p074-missing-schema-true-postcondition`, `ev-p097-behavioral-perturbation`, `ev-p096-shared-misinterpretation`
- `evidence_level`: C（方法有效性）
- `linked_route_ids`: NONE
- `why_not_gap_matrix`: 已有证据支持验证缺口及相邻行为检查，但没有证明由任务轨迹自动产生的非同构关系能可靠检测工具语义错误。
- `promotion_blocker`: 与 ToolGate、统一重试、同模型反思在等预算下的直接对照；共享误读失败率。
- `validation_need`: 可执行关系来源、关系正确率、误拒绝率与真实故障检出率。
- `owner_status`: 主研究者 draft h-v001-001
