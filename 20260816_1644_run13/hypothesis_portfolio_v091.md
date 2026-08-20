# v091 假设组合

本版本没有注册实验假设。

- “成本变化后智能体仍沿用旧计划”：`EXACT_DYNAMIC_COST_REPLANNING_COLLISION`。
- “工具失败和成本变化应触发剩余路径重算”：`DIRECT_COSTBENCH_COLLISION`。
- “已知图与成本下选择新的最便宜可行路径”：`CLASSICAL_DYNAMIC_SHORTEST_PATH_COLLISION`。

本地修改工具价格并比较是否重规划，只会复现 CostBench 的任务生成与经典图求解器优势。
