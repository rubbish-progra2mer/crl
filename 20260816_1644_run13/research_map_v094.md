# v094 研究图谱

## 主动诊断事实

- Contract v3，权威当前版本为 v094，Run 状态为 `ACTIVE`。
- FTS Recall 刷新后包含 56,701 个检索块；FTS 为 `READY`，语义检索未请求并单独标为 `DEGRADED`。
- Run-wide 机械统计为 93 个科学版本、13 次 Recorded 实验和 3 次 Formal/Review-support 尝试；v094 当前没有实验、比较文件、检索快照或评审文件。
- 诊断材料是 `ADVISORY_NON_AUTHORITATIVE_FACTS_ONLY`，仅提示连续碰撞后优先验证稳定现象，不作科研选择。
  - workbench_v094/diagnosis/v094_residual_convergence_20260817/

## 报告论证逻辑

- ReportLogic 已把深度研究报告的逻辑质量分成三层：宏观逻辑检查统一分析主线，阐释逻辑检查必要上下文与推进，结构逻辑检查结论是否有明确主张—支持关系。
  - https://aclanthology.org/2026.acl-long.384/
- 该工作构建人类标注、量规引导的数据集并训练开源 LogicJudge；稳健性实验发现通用模型裁判会受冗长等表面线索影响，推理模式可能掩盖断裂支持关系。
- DREAM 已把深度研究评价扩展为能调用工具的自适应评价器，覆盖时间有效性、事实核验和系统推理探针。
  - https://arxiv.org/abs/2602.18940
- EviReport 以证据单元、层级提纲和事实优先循环生成长报告，并同时评价事实准确性与覆盖度。
  - https://aclanthology.org/2026.findings-acl.1397/

## 当前 Run 去重

- v039 已处理多文档综合中的范围丢失和伪因果化解。
- v054 已处理可迁移核验能力而非一次性正确答案。
- v080、v089 已处理引用事实支持、时间有效性和来源链。
- v084 已检查科研分析流程有效性与可复现性。

## 结论

报告级宏观、阐释和结构逻辑已有直接问题定义、人工数据、专门评价模型和裁判稳健性分析。用本地成对报告删除推理桥，只会复现 ReportLogic 的结构逻辑扰动，v094 不注册实验。
