# v043 研究地图

- SAUP（ACL 2025）已经逐步传播智能体不确定性，并按情境权重聚合每一步的不确定性。
  - https://aclanthology.org/2025.acl-long.302/
- SRICE 使用保形预测校准外部视觉工具输出，并据不确定性选择工具。
  - https://arxiv.org/abs/2503.08308
- GLIDE（ACL ARR 2026 May）直接指出异构智能体产生的原始置信分数分布尺度不兼容，因而不能跨智能体直接比较，并提出分布式内部证据。
  - https://openreview.net/pdf?id=QMJhAFQ1SS
- MICE for CATs 使用模型内部层级信号校准工具调用置信度。
  - https://openreview.net/forum?id=22uOLJuRFR
- 置信度校准、分数标准化与排序融合本身已有成熟统计基础。

## 判定

测量对象与 v016 的策略/环境轨迹方差不同，但“逐步传播不确定性”和“跨异构来源校准分数”均已有直接方法。将来源从模型改成外部工具只改变数据出处，不改变校准与传播计算。
