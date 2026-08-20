# v019 研究图谱

- Toward a Gricean Retreat（arXiv:2608.13484）在 T-REx 派生基准上正交操纵实体熟悉度与指称具体度，发现模型激活可分别预测知识边界和即将生成的具体度，但生成仍系统偏好具体指称；论文明确把耦合两种信号的训练或转向目标列为后续方向。
- Hierarchical Selective Classification（arXiv:2405.11533）已经形式化分层选择性分类，使模型在不确定时降低预测具体度，并提出分层风险—覆盖曲线及满足目标准确率的高概率算法。
- Conformal Prediction in Hierarchical Classification（arXiv:2501.19038）允许以层级内部节点作为保形预测集；后续分层保形分类继续在覆盖保证下优化表示复杂度。
- Geometry-Calibrated Conformal Abstention（arXiv:2604.27914）已经利用模型内部表示几何校准知识参与度并提供选择性回答保证。

结论：现象真实且最新，但方法方向已被源论文明确提出，核心“按不确定性上退到更粗标签”又有成熟统计方法；当前组合没有新的计算原语。
