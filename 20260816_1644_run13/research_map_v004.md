# v004 研究图

## 问题证据

- FuncBenchGen，arXiv:2509.26553：受控多步函数依赖图实验观察到强模型会传播错误或过期参数值；简单重述先前变量即可显著改善。
- P066 / BFCL：从单轮函数调用到有状态多轮评测存在明显性能落差。
- P084：加入语义相关工具会产生错误参数分配与参数幻觉。

## 直接先行工作

- LLMCompiler，*An LLM Compiler for Parallel Function Calling*：规划器生成任务及依赖，中间结果先以变量占位；任务取指单元按依赖就绪状态，把占位符替换为前序任务真实输出后执行。官方页面：https://openreview.net/forum?id=uQ2FUoFjnF
- Evoflux，arXiv:2606.12674：通过结构化编辑与执行反馈演化类型化工具工作流图，显式维护中间输出依赖。官方页面：https://arxiv.org/abs/2606.12674
- ToolGate：在显式类型化键值状态上以工具前置条件和后置条件控制状态提交，覆盖可信状态与类型约束的相邻面。

## 边界判断

候选强调的是避免模型复制值，而 LLMCompiler 已经用符号变量与运行时替换完成这一计算。为槽位再加类型、版本或来源标签具有实用价值，但属于对已有执行器的约束增强，当前没有论文级剩余差分。

## 检索审计

Run 内快照：`hypotheses_v004/searches/typed-dataflow-binding-001/`。
