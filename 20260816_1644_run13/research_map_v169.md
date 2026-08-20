# v169 研究图谱

## 目标现象

- 研究偏好模型每轮从 15 个候选中选一个执行；仅看计划、代码与历史树的推断型版本把 AIRS-Bench 平均归一化分数从 0.684 提高到 0.711，允许五分钟小试验的智能体版本进一步提高到 0.729。
- 小试验常用单折验证、数据子采样、减少轮数、移除集成或其他训练组件。论文发现全量数据通常比子采样更可靠，移除学习率调度器或数据增强会造成严重下降。
- 因而“更便宜”不是一条统一保真度轴：同一代理干预对不同候选可能保留、削弱或翻转全规模排序。

## 自然候选：候选条件化试验代理

- 把候选表示、试验代理和历史全规模结果共同输入保真度模型，估计每个低成本观测对目标全规模分数的偏差与不确定性。
- 在固定预算下选择单位成本预期信息增益最高的“候选 × 代理”，不再对所有候选使用同一种五分钟缩减方案。
- 高信息量判定本应是：相同成本下，它是否比固定小试验、纯语言排序和普通逐级加预算更少发生最终赢家错选。

## 直接先行

- [FABOLAS](https://proceedings.mlr.press/v54/klein17a.html) 已把训练集大小作为保真度变量，联合建模损失与时间，并按关于全量最优点的信息增益／成本选择评估。
- [Freeze-Thaw Bayesian Optimization](https://arxiv.org/abs/1406.3896) 已从部分学习曲线决定暂停、启动或恢复候选，并用信息论规则分配预算。
- [Adaptive multi-fidelity optimization](https://proceedings.mlr.press/v108/fiegel20a.html) 已在未知偏差函数下自适应权衡成本与近似偏差。
- [Multi-Fidelity Bayesian Optimization with Unreliable Information Sources](https://proceedings.mlr.press/v206/mikkola23a.html) 已处理低保真信息源可能比单保真优化更差的情况，并给出稳健界。
- [Input-dependent Fidelity MFBO](https://proceedings.mlr.press/v244/fan24a.html) 更直接地允许同一近似源在输入空间不同区域具有不同保真度，学习输入依赖噪声并据此选择查询。

## 结论

“候选 × 试验代理”的可靠性正是输入依赖多保真优化的既有问题；加入大语言模型候选文本只改变输入表征，不改变查询、偏差建模或信息价值计算。当前没有独立方法差分。
