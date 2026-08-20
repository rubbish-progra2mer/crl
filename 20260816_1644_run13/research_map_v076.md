# v076 研究图谱

## 较弱目标通过导致的自我终止

- *DeployBench* 在 51 个研究制品部署任务上使用隐藏流水线执行论文指定实验并检查输出。其失败由完成判断主导：154 个失败中 97 个是智能体自行停止，结束前检查验证的是与论文任务不同或更弱的目标。
  - https://arxiv.org/abs/2606.05238

该发现精确覆盖“检查通过但检查对象弱于真实交付要求”的核心现象。

## 部分交付物的错误批准

- *AgentHire-Bench* 直接包含最终 PNG/PDF 看似完整、但缺少必需可编辑源文件的交付审查；低分智能体反复宣称完整并批准，高分智能体阻止批准并要求补齐核心文件。
  - https://openreview.net/pdf?id=GrMXHoBp3h
- *Plan-RewardBench* 将部分完成、缺失子任务、工具根据伪造和完整失败作为轨迹级评分标签，并逐子任务给出状态与证据位置。
  - https://aclanthology.org/2026.acl-long.1062/

## 部分证据下的完整性过度声明

- *Partial Evidence Bench* 提供完整答案、授权视图答案、完整性判断和结构化缺口报告，直接评价答案正确性、完整性意识、缺口报告质量及不安全的完整性声明。
  - https://arxiv.org/abs/2605.05379
- *Do Search Agents Verify Before They Search?* 直接评价轨迹证据完整性，并发现只部分验证当前实体就向下游扩展的现象。
  - https://openreview.net/pdf?id=nkHa4MbPG6

## 程序与制品完整性

- *StructureClaw* 要求解释需求、可计算模型、验证记录、求解器输出、规范检查和最终报告形成完整制品链，避免只奖励流畅但不完整或不可执行的输出。
  - https://arxiv.org/abs/2607.14896

## 结论

较弱检查目标、自我提前终止、部分交付错误批准、有限证据下过度声明和制品链完整性均有直接工作。增加 `complete/partial/blocked` 字段或列交付清单不构成新计算，不注册实验。
