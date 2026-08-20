# v100 研究地图

## 主动诊断事实

- facts-only 诊断 `v100_century_convergence_20260817` 确认当前为 Contract v3、`v100`、`ACTIVE`。
- Run-wide 机械计数为 99 个既有科学版本、13 次记录级尝试、3 次正式/评审支持尝试和 16 份搜索快照；当前 v100 在诊断时尚无实验、比较或搜索快照。
- 全文召回索引为 `READY`，共 56,782 个检索块；语义索引未请求且单独为 `DEGRADED`。这些状态不影响 Run 权威状态，也不自动证明候选收敛。

## 结构残余一：不确定副作用与重复执行

- Run 内 v008 已定义“未执行、部分执行、全部执行、延迟可见”并审计先验证再重试、后置条件核验和幂等键；v034、v075 又关闭事务提交、补偿和完成后清理。
- 该路径与当前负记忆直接同构，不重开实验。

## 结构残余二：局部观察与完备性

- Run 内 v010 已把分页、分区、筛选域和快照覆盖写成否定结论的覆盖义务，并与自动分页和查询完备性工作对照。
- 把目标记录放到隐藏后页只能复现自动分页优势，不产生新的在线计算。

## 结构残余三：含噪选择与赢家高估

- [Towards Reliable LLM Evaluation: Correcting the Winner's Curse in Adaptive Benchmarking](https://arxiv.org/abs/2605.05973) 已直接研究自适应提示/程序搜索中的选择敏感评测，并以冻结候选短名单、重复数据划分和选择后不确定性量化处理赢家乐观偏差。
- [Valuing Winners](https://arxiv.org/abs/2605.18887) 区分全局与选择性赢家诅咒，并比较交叉拟合、重采样和经验似然等校正目标。
- Run 内 v020 已测量构想的独立实现方差与胜者翻转，v055 已关闭自适应搜索复用验证信号的统计有效性缺口。将赢家校正实例化到自动科研智能体不留下独立方法核。

## 结构残余四：证据顺序、利用与停止

- Run 内 v005 固定调用、结果、模型和解码，只排列三条工具结果；两个模型各 8/8 个任务、48/48 个排列保持正确，未观察到翻转。
- [Diagnosing Search Behavior and Failure Modes in Long-Horizon Search Agents](https://arxiv.org/abs/2608.01913) 已把长搜索失败分成检索缺口与利用缺口，并指出搜索量与答案质量仅弱相关，停止应依据证据充分性而不是调用数量。
- [Belief Revision: The Adaptability of Large Language Models Reasoning](https://aclanthology.org/2024.emnlp-main.586/) 已用顺序前提评测新证据到达后的信念修订，并发现更新与不应更新之间存在权衡。
- [Chow-Liu Ordering for Long-Context Reasoning in Chain-of-Agents](https://arxiv.org/abs/2603.09835) 已明确研究有损有界记忆导致的顺序依赖，并按学习到的依赖结构优化块顺序。
- 把上述工作组合为“随机置换证据并延迟停止”的本地实验，若短上下文无效只复现 v005；若有损压缩或顺序停止有效，则分别落入既有顺序优化、信念修订和证据充分性停止。

## 边界结论

四条路线均未通过“Run 内非同构 + 公开计算未覆盖 + 最小实验高信息量”三条件。本版本不注册实验，但只关闭这些明确路线，不外推到宽 Charter 的全部 frontier。
