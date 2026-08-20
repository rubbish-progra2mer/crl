# v070 研究图谱

## 多条有效路径的表示与评价

- *CORE: Full-Path Evaluation of LLM Agents Beyond Final State* 使用确定有限自动机把任务编码为有效工具路径集合，并以路径正确性、前缀关键度、危害调用率与效率等指标评价完整轨迹。
  - https://arxiv.org/abs/2509.20998
- *WebGraphEval* 把多个智能体的网页交互轨迹抽象为统一加权动作图，直接面向多路径、跨智能体和效率感知评价。
  - https://openreview.net/forum?id=IPpOtWGmdf

## 替代路径发现与阻断

- *PlanBench-XL* 在 1,665 个工具的生态中加入工具缺失、失败或干扰的阻断机制，迫使智能体在运行时发现受阻路径并改走更长的替代工具路径。
  - https://arxiv.org/abs/2606.22388
- *ToolChain\** 把工具调用空间表示为决策树，并用 A* 搜索低成本有效路径，直接属于多路径规划。
  - https://arxiv.org/abs/2310.13227
- *ToolBench-X* 要求故障实例至少保留一条重试、回退、验证或交叉检查路径，已覆盖工具路径受阻后的恢复。
  - https://arxiv.org/abs/2606.25819

## 邻近覆盖

- *RealFin* 明确包含同一任务多条可行解法，并分析规范工具失败后的替代路径。
  - https://openreview.net/forum?id=0ni0z8Ttg6
- 当前 Run v003、v006 与 v067 已分别关闭功能等价工具、反事实轨迹重放和等价接口扰动。

## 结论

“表示所有有效路径—阻断常用路径—观察替代路径恢复—按路径结构评分”的完整计算链已有直接工作。再造合成本地工具图只会复现 CORE、WebGraphEval 或 PlanBench-XL，不注册实验。
