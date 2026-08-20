# v077 研究图谱

## 直接检索结果

围绕 `tool call argument copying`、`copy demonstration values`、`demonstration literal leakage` 和 `in-context examples identifiers` 做精确检索，没有找到直接评价“演示工具调用中的实例字面量被复制到当前显式参数”的公开论文，也没有找到以逐演示 α 改名和局部绑定表作为干预的直接工作。

## 最邻近工作

- *Z-ICL* 明确观察到模型会从伪演示直接复制文本，并通过改写邻居文本和使用与标签无关的短语降低复制；任务是零样本文本分类，不是工具调用参数绑定。
  - https://arxiv.org/abs/2212.09865
- *Rethinking the Role of Demonstrations* 表明，演示的标签空间、输入分布和整体格式可以比真实输入标签映射更重要；覆盖一般上下文学习机制，不含工具参数串值或作用域隔离。
  - https://arxiv.org/abs/2202.12837
- *Where to show Demos in Your Prompt* 系统评价演示位置偏差：改变演示、系统提示和用户消息的位置可显著改变预测，小模型更敏感；它研究位置，不研究实例字面量绑定。
  - https://aclanthology.org/2025.emnlp-main.1503/
- *Tool Learning in the Wild* 研究真实工具文档、上下文演示以及不完整示例对工具学习的影响；它提供工具域邻近性，但未把显式当前参数被演示值覆盖作为独立现象。
  - https://openreview.net/forum?id=T4wMdeFEjX

## 差分判断

一般复制偏差构成现象级近邻，演示选择和位置构成替代解释。当前剩余问题仅是：在单步工具调用、当前值完全显式、无信息缺口时，是否仍存在稳定的实例字面量串值；若存在，局部变量作用域表示是否比同信息的普通警告更有效。该问题先接受强现象杀伤，不能靠隐藏当前值、增加歧义或移动演示到异常位置来挽救。
