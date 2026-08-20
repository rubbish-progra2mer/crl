# v002 研究图

## 直接问题证据

- P087，*Tools Are Under-Documented*：查询无关地扩展功能、适用场景、限制与标签；只评测检索与重排指标，并明确发现字段扩展并非普遍有益。
- P084，*On the Robustness of Agentic Function Calling*：在固定请求下加入语义相关工具会使九个模型的抽象语法树准确率全部下降，支持近邻干扰问题存在。
- P069，*Tool Preferences in Agentic LLMs are Unreliable*：仅修改描述即可造成超过十倍的使用差异，且相同工具仍有顺序偏置；任何比较必须抵消描述与位置混杂。
- P100，*How Many Tools Should an LLM Agent See?*：候选集过宽会损害下游选择，说明检索覆盖与最终选择不是同一目标。

## 致命先行工作

- Zhang 等，*ToolExpNet: Optimizing Multi-Tool Selection in LLMs with Similarity and Dependency-Aware Experience Networks*，ACL Findings 2025：直接用语义相似与依赖关系组织工具，进行适应性试验，分析相似工具细微差异，并重写工具描述以区分易混工具。官方论文页：https://aclanthology.org/2025.findings-acl.811/
- Hallinan 等，*OpaqueToolsBench: Learning Nuances of Tool Behavior Through Interaction*，arXiv:2602.15197：ToolObserver 从多工具执行轨迹更新文档；提示明确要求比较工具、给出区别特征与相对适用场景。官方页面：https://arxiv.org/abs/2602.15197
- Chen 等，*MagicSelector*，arXiv:2607.17751：用高分错误工具进行困难负例挖掘，训练重排器区分高度相似工具。它不直接重写描述，但进一步压缩了“近邻辨析”作为独立方法的空间。官方页面：https://arxiv.org/abs/2607.17751

## 仍可保留的经验问题

Tool-DE 的独立扩展是否会在最终选择层造成碰撞仍值得测量，但它更像分析或评测消融；在 ToolExpNet 与 ToolObserver 之后，不能把“比较近邻并写入边界”提升为新方法贡献。

## 检索审计

Run 内快照：`hypotheses_v002/searches/tool-doc-collision-001/`。该快照只作导航；上述结论分别回到论文卡、原始论文页面与方法文本核对。
