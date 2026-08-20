# v041 研究地图

## 主动诊断事实

- `workbench_v041/diagnosis/v041-frontier-reset-001/report.md` 标记为 `ADVISORY_NON_AUTHORITATIVE`，仅提供机械事实。
- Run 已有 40 个科学版本；v041 收集时尚无 Recorded/Formal 尝试、检索快照或评审产物。
- 全 Run 有 16 个检索快照；原始检索数据约 29.7 MB，紧凑检索报告约 135.7 KB。
- 词法召回可用；语义召回因未建立语义索引而降级。诊断没有给出科研裁决。

## 路线 A：委派后的全局约束保持

- Zhang et al., *Planning with Multi-Constraints via Collaborative Language Agents*, COLING 2025：PMC 已把多约束规划分解成层级子任务，并在 TravelPlanner 与 API-Bank 上评估。
  - https://aclanthology.org/2025.coling-main.672/
- Chang, *SagaLLM: Context Management, Validation, and Transaction Guarantees for Multi-Agent LLM Planning*, 2025：直接研究多智能体规划中的全局约束意识、上下文收窄、验证与事务保证。
  - https://arxiv.org/abs/2503.11951

判定：候选问题和干预位置均已有直接覆盖；“把全局约束分配给子任务并在合并时验证”不足以形成新方法差分。

## 路线 B：异构工具结果的实体身份绑定

- Babu and Indukuri, *Entity Binding Failures in Tool-Augmented Agents*, 2026：明确区分工具正确与实体正确，并评估实体解析前置条件、置信门控绑定、歧义澄清和来源追踪；其受控评测中动作型基线仍有 24%--26% 的错误实体动作。
  - https://arxiv.org/abs/2606.30531
- 传统实体链接与记录匹配已为异构记录别名、歧义和候选选择提供成熟方法背景；把这些算子置于工具调用之前本身不是新计算。

判定：该路线与 v004/v013 的字面量与句柄问题不同，但被更近期、题目级同构的智能体工作直接覆盖。

## 安全边界

本版本未访问、设计或测试任何安全过滤绕过机制；所有候选均为非操作性的可靠性问题。
