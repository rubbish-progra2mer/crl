# v051 研究地图

## 基准与公开代码事实

- MCPWorld 提供 201 个跨 10 个应用的程序接口、图形界面和混合任务，并用应用内部挂钩、代码注入或接口状态查询进行与智能体实现无关的自动验证。
  - https://arxiv.org/abs/2506.07672
  - https://github.com/SAAgent/MCPWorld
- v051 固定查看公开仓库提交 `12396eb911c8ed9cf78fde72c15fe7b8a947f6de`。其混合模式只是把图形界面工具与模型上下文协议工具的并集交给模型；代码没有独立路由器或跨表面提交门。
- MCPWorld 论文明确说明混合基线无启发式偏置，由模型逐步选择工具。混合任务成功率为 75.12%，高于图形界面单独的 70.65% 和程序接口单独的 53.23%；但中等难度任务增益很小，作者怀疑过长工具提示会引入干扰。

## 步骤路由的直接碰撞

- *ToolCUA: Towards Optimal GUI-Tool Path Orchestration for Computer Use Agents* 直接把图形界面—工具切换建模为轨迹级策略学习，以关键切换点强化学习和工具效率路径奖励学习何时继续图形界面、何时切换工具。
  - https://arxiv.org/abs/2605.12481
- *EE-MCP: Self-Evolving MCP-GUI Agents via Automated Environment Generation and Experience Learning* 也把两种模态何时产生互补优势建模为统一混合策略学习，并按应用构成选择蒸馏或经验库机制。
  - https://arxiv.org/abs/2604.09815

## 跨表面核验的差分审计

- ToolCUA 的训练数据生成已经对工具步骤做“下一状态落地”：将预测工具效应锚定到原轨迹中真实后续截图，核对预测效果与可见状态；其推理状态同时含当前截图和此前工具结果。
- 若进一步把不一致转为显式拒绝继续，该计算等价于工具后置条件验证。ToolGate 已用工具契约的后置条件决定结果能否提交到可信状态。
  - https://aclanthology.org/2026.findings-acl/
- Run 内 v012 已关闭一般状态新鲜度失配，v034 已关闭事务式状态提交并检查过假成功，v040/v044 又覆盖最终状态与工件核验。

## 结论

v051 的两个草案分别被 ToolCUA/EE-MCP 的混合路径学习与 ToolCUA/ToolGate 的状态落地和提交验证覆盖。双表面只是观测来源特化，不改变验证计算，因此不注册正式假设。
