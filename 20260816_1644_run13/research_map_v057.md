# v057 研究图谱

## 最近工作

- [ToolGate](https://arxiv.org/abs/2601.04688) 用霍尔式前置条件与后置条件约束已选工具的执行和状态提交。
- [Verified Tool Calls](https://arxiv.org/abs/2608.02645) 在调用后加入后置条件核验、重试前核验和幂等键。
- [Verification-Aware Planning for Multi-Agent Systems](https://arxiv.org/abs/2510.17109) 为分解后的子任务生成验证函数并据此迭代修订。
- [Tool Preferences in Agentic LLMs are Unreliable](https://aclanthology.org/2025.emnlp-main.1060/) 证明工具描述的表面编辑可大幅改变选择。
- [Diagnosing Tool-Selection Reasoning with Canary Tools](https://arxiv.org/abs/2608.04719) 给出语义诱饵、参数陷阱、能力幻象、先决条件盲区、时间诱饵和粒度陷阱，但摘要未把“效果证据不可达”单列为类型。

## 暂存差分

既有核验工作主要问“已选工具执行后能否验证或提交”，本版本问“在功能等价的动作工具之间，未来能否形成证据闭包是否应进入选择函数”。候选计算是把目标效果、动作输出和读回工具连接为可达图，在执行前排除没有目标证据路径的动作。

## 高碰撞风险

这一差分可能只是 ToolGate/VeriMAP 的显然前移，或被一句通用提示完全吸收。只有在同信息强提示仍失败、而编译闭包卡跨模型稳定改善时，才值得继续最近先行工作映射。

## 最小实验结果

- `qwen2.5:7b`：原始 12/12，强通用提示 12/12，闭包卡 12/12。
- `qwen3:8b`：原始 12/12，强通用提示 12/12，闭包卡 12/12。
- 六个模型×条件单元均无漏调用、无先调用状态工具；动作身份和列表顺序交替后结果不变。
- 两次运行都由记录器成功捕获，层级为 `RECORDED_NON_SUPPORTING`；它们支持淘汰判断，不作为交付级实验依据。

原始条件已经远超预注册的 90% 杀死阈值，闭包卡没有任何可测增益。
