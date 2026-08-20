# 文献与方法谱系图

## 已核对的直接依据

1. **ToolGate（Liu 等，Findings of ACL 2026；共享知识库 P074）**：把候选调用生成与可信状态提交分开，前置条件决定可否调用，后置条件决定返回值能否进入符号状态。原文明确说明约四分之一 ToolBench 工具没有结构化返回模式，此时采用恒真后置条件。共享知识库双读进一步确认：保证相对于契约成立，调用后的门不能撤销外部副作用。
2. **tau-bench（Yao 等，ICLR 2025；P007）与 tau2-Bench（Bhardwaj 等，ICML 2026；P047）**：以隐藏终态或环境断言评价完整工具交互，说明表面回答或聚合工具正确率不能替代独立终态判定；它们是评价载体，不是遗漏效应发现方法。
3. **Towards Practically-Secure Tools for AI Agents（Adam 等，EuroMLSys 2026）**：用静态代码分析发现效应、用开发者植入的细粒度沙箱执行上下文策略；论文明确指出源码不可得和远程基础设施是困难，并要求工具开发者使用可信沙箱库与远程证明。这是本候选最接近的系统基线。
4. **Governed Individuation（Qin 等，arXiv:2607.04613）**：把动作映射为语义效应并在权限格上门控；原文明确把“为任意开放动作构造可靠、保守的效应抽象”列为未解决的系统问题，最强动态监视器是在已截获的原子效应上逐项检查。
5. **Cordon（Chen 等，arXiv:2606.17573）**：以任务级语义事务暂存可逆状态和外发效应，再统一验证和提交；其贡献是事务边界与组合验证，不是不透明工具的效应发现。
6. **AgentTrust（Yang，arXiv:2605.04785）与 ToolSafe（Mou 等，Findings of ACL 2026）**：在执行前根据命令、历史或模型判断危险调用，主要观察拟执行动作，不直接观察工具实现遗漏的真实效应。
7. **ARMeta（Khan 等，arXiv:2605.28321 / COMPSAC 2026）**：从 OpenAPI 说明生成 Given–When–Then 变形关系与可执行测试，比较种子和后续调用的 HTTP 响应；它直接否定“把变形测试用于接口”本身的新颖性。
8. **SGVEF-LOOP（Liu 与 Zhang，ACL 2026）**：以事实支撑的语义等价任务对检查 MCP 智能体的轨迹与回答稳定性，并用覆盖反馈探索工具转移图；其干预对象是任务语言表面，CEP 的干预对象是工具参数和影子后端状态。

## 候选位置

本候选不替代事务、效应门或沙箱，而是尝试生成一个受限的、经验性的行为证书：在可复制影子环境中，对同一调用做单因素成对干预，读取独立审计面上的效应轨迹，把“工具说明”升级为“在已覆盖干预域中观察到的效应包络”。

最近工作的贡献上界因此是：

- 相对 ToolGate：补的是契约之前的经验效应发现，不是更强的返回值后置条件；
- 相对静态分析与细粒度沙箱：补的是源码不可见但后端可复制、效应可审计的远程工具，不提供静态完备性；
- 相对 Cordon：提供待暂存/待门控效应的经验发现线索，不解决任意跨步骤事务；
- 相对语义效应门：尝试降低效应抽象的人工声明依赖，最终保证仍受观测覆盖限制。

## 当前最大相撞风险

软件测试中的差分测试、变形测试、污点追踪和组合测试都是直接祖先；如果最终方法只是把这些术语换到工具智能体场景，没有参数关系、影子凭证和运行时证书之间的新计算链，则方法潜力不足。实验必须证明“成对干预产生的关系型效应原子”比同预算普通复测或随机模糊测试提供独立增益。

## 主要公开来源

- ToolGate: https://aclanthology.org/2026.findings-acl.470/
- tau-bench: https://openreview.net/forum?id=roNSXZpUDN
- Cordon: https://arxiv.org/abs/2606.17573
- Governed Individuation: https://arxiv.org/abs/2607.04613
- Towards Practically-Secure Tools for AI Agents: https://doi.org/10.1145/3805621.3807645
- AgentTrust: https://arxiv.org/abs/2605.04785
- ToolSafe: https://aclanthology.org/2026.findings-acl.1850/
- ARMeta: https://arxiv.org/abs/2605.28321
- SGVEF-LOOP: https://aclanthology.org/2026.acl-long.1224/
