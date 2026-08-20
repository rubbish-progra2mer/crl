# 最近先行科研解释

> 本文件属于主研究者解释，可在阅读候选、PDF、Evidence 和实验后继续修订；它不进入机器事实快照哈希。

- 审计标识：`h004_behavior_probe`
- 碰撞类型：`DIRECT_EXACT + EMPIRICAL_ABSORPTION`

## 真正的 nearest prior

- ToolExpNet（Findings of ACL 2025）是直接精确先行：它对工具迭代执行模拟实验，以自适应采样探索相似工具的细微差异与依赖，并把试错经验汇总进网络以指导多工具选择。
- ToolScope（ACL 2026）用工具合并、自校正和上下文过滤解决重叠名称/描述导致的歧义。
- Diagnosing Tool-Selection Reasoning with Canary Tools（arXiv:2608.04719）已系统评价语义诱饵、能力幻象等六类工具选择弱点，并含真实沙箱执行。

## 实质组件重合

候选的关键变化“通过真实试验而非只读描述来学习工具差异并据此选择”已被 ToolExpNet 直接实现；将经验网络压缩成行为指纹或能力等价类不足以形成新的论文级计算差分。

## 仍存贡献增量

仅可能剩余对描述扰动不变性的专门评价与副作用指纹，但 P069、Canary Tools 和一般黑盒 API 测试共同使其很容易退化为已知评价切片。

## 最危险替代解释

- ToolExpNet 的试错经验可能已经隐式编码全部行为指纹信息。
- 行为指纹的优势可能来自手工探针泄漏或确定性解析器知道能力类。
- 保留输入上若不能泛化，只是离线记忆探针输出。

## 最小区分实验

不再运行本地实验：直接先行已经命中候选的 changed computation，符合先行优先的死亡条件。若未来重启，必须先证明相对 ToolExpNet 的非措辞、非数据结构差分。

## 方法死亡后仍存现象

描述偏置与行为不一致现象仍真实，但不足以支持本候选；不把“副作用也应探查”缩窄成贡献。

## 背景与身份未解决项

机器 Prior Audit 的通用来源有降级，但 ToolExpNet、ToolScope 与 Canary Tools 均通过 ACL Anthology 或 arXiv 原文人工核对，因此碰撞判断不依赖降级源。
