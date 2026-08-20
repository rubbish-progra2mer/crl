# Target Problem Card

- `problem_id`: TP-v001-01
- `research_direction`: 文本与工具型大语言模型智能体中的长程执行可靠性
- `target_problem`: 在没有外部真值、没有特权工具状态、且额外工具预算受限时，如何让文本与工具型大语言模型智能体识别并修复“工具调用表面成功但语义结果错误”所造成的长程状态漂移？
- `problem_statement`: 现有工具型智能体通常把可解析、无异常码的工具返回视为可信观测；一旦返回内容在语义上错误、陈旧、不完整或与任务隐含约束冲突，错误会进入后续计划并在多步执行中放大。本版本研究一个可证伪的问题：能否仅依据智能体可见的任务、动作、工具返回与后续轨迹，在相同工具权限和可比预算下，比固定重试、自洽采样和事后反思更有效地定位需要验证或回滚的状态转移，并提高独立终局判定下的任务成功率？
- `task_setting`: 输入为自然语言任务、工具接口及逐步执行轨迹；输出为下一动作，以及可选的验证、回滚或重规划动作。约束为纯文本/结构化工具交互、工具权限对所有方法一致、无测试真值和隐藏模拟器状态、额外工具调用受预算约束。默认评价语境为可注入“表面成功、语义错误”观测的多步工具任务，并由独立于方法规则的任务终局或环境判定给出正确性。
- `assumed_user_goal`: 找到一颗具有 CCF-B 方法论文潜力、真实改变智能体计算过程、可通过独立评价依据反证的研究种子；不是完成整篇论文。
- `explicit_boundary`: 仅研究文本与工具型大语言模型智能体；聚焦多步轨迹中的语义错误观测、状态漂移、预算化验证与恢复；方法不得依赖测试真值、额外工具权限或仅对候选开放的外部信息。
- `excluded_subfields`: 具身机器人控制；纯视觉导航；模型权重训练或大规模预训练；单轮事实核查；仅做越狱/提示注入防御；纯多智能体协商；以提示措辞变化冒充方法贡献。
- `first_pass_search_keywords`: tool-using LLM agent semantic tool error; silent tool failure; observation corruption; long-horizon agent recovery; selective verification; rollback planning; execution trace consistency; agent state drift; tool hallucination detection; budgeted verification.
- `historical_failure_constraints`: 本 Run 新建，尚无版本内负结果；禁止读取其他 Run 的失败记录。
- `consulted_route_registry_ids`: NONE
- `rerun_avoidance_strategy`: 所有检索查询、命中、淘汰原因和实验身份只记录在本 Run；若局部谱系被最近工作或强基线吸收，则推进科学版本并选择结构不同的问题或干预算子。
- `ambiguity_needing_user_confirmation`: NONE。AUTONOMOUS Charter 已授权主研究者在默认硬领域内自主选题和转向。

## 主研究者确认

`KEEP`：目标问题单一、可反证、具备公平基线与独立终局评价路径，可以进入文献入口选择。
