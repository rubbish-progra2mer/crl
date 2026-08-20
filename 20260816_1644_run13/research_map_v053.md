# v053 研究地图

## 现象与直接先行工作

- *SlotGuard: Stop Oversharing Private Local Context in LLM Agent Transcripts* 直接针对工具输出、终端日志和文件读取进入提供方转录的泄露问题，把结构绑定改写为带类型、后缀感知的槽位，用会话图链接跨轮引用，并只在可信运行时恢复原值。
  - https://arxiv.org/abs/2607.17147
- *Secure Forgetting* 把智能体遗忘分为状态、轨迹和环境级别，并训练转换模型把高层删除请求变成可执行遗忘提示。
  - https://arxiv.org/abs/2604.00430
- FSFM 已系统覆盖被动衰减、主动删除、安全触发和自适应强化式选择性遗忘。
  - https://arxiv.org/abs/2604.20300
- AgentDAM 已在端到端网页任务中把数据最小化定义为只使用完成任务所必需的敏感信息，并提供提示防御。
  - https://openreview.net/forum?id=SP0X5rm6f3
- *Data Flow Control: Data Safety Policies for AI Agents* 已把派生与释放限制建模为来源多项式上的声明式策略，并在数据库基础设施中确定性执行。
  - https://arxiv.org/abs/2606.05679
- AgentSandbox 已采用按任务隔离的短暂智能体、上下文感知数据最小化器和受保护记忆。
  - https://openreview.net/forum?id=XR9UpqWhmT

## 差分审计

按最后一次使用删除属于经典数据流存活性调度；它没有改变 SlotGuard 的受信槽位与跨轮绑定，也没有改变 Secure Forgetting/FSFM 的删除语义或数据流控制的派生策略。把这些组件串联只得到更早的删除时点，而非新的隐私—效用计算。

## 安全边界

本版本只研究防御性数据最小化，未生成攻击步骤、提示注入载荷或安全过滤绕过；v029 的宿主执行边界保持不变。

## 结论

v053 不注册正式假设。
