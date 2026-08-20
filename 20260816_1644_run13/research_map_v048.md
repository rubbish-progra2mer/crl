# v048 研究地图

## 近期直接证据

- *Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents* 把外部执行框架自演化拆成两种能力：更新者能否从执行证据产出有用的持久化更新，以及求解器能否从更新后的执行框架获益。论文进一步把弱求解器的低收益归因为相关工件的激活失败和激活后的遵循失败。
  - https://arxiv.org/abs/2605.30621
  - https://github.com/A-EVO-Lab/a-evolve/tree/release/harness-evolution
- *Position: Agentic Evolution is the Path to Evolving LLMs* 已把知识、工具和验证资产建模为可版本化、可编辑的持久状态，并用诊断、规划、更新、验证和条件提交组成求解—演化循环；文中还明确举出生成版本化适配器和修正接口模式的例子。
  - https://openreview.net/forum?id=9ypfISYVNZ
- *Living-Harness Is an Interactive-Agent Evolver* 把轨迹与评价信号编译为受限的程序性记忆和状态图，继续覆盖“从失败写入可调用持久工件”的主路径。
  - https://arxiv.org/abs/2607.26598
- *Self-Evolving Agent Harnesses via Gated Semantic Quality-Diversity* 把更新提议与确定性归因、显著性检验及密封测试分开，覆盖“可靠地决定何种更新应被保留”的评测与提交路径。
  - https://arxiv.org/abs/2607.13683

## 与 Run 内历史的关系

- v018/v019 已关闭一般性的经验抽取、迁移与复用。
- v020 已关闭把实现差异和自适应比较包装成核心方法的候选。
- v021 已关闭执行框架投影与变形审计。
- v042 已关闭技能注入、失败经验编译以及影子失败分支。

## 结论

激活与遵循的能力分解是有价值的现象和评测结论，但从它直接导出的干预仍是检索/注入技能、编译失败经验、修改执行框架或加强验证。这些计算同时被近期先行工作和 Run 内负面记忆覆盖。v048 不注册正式假设，也不把能力分解本身误报为新方法。
