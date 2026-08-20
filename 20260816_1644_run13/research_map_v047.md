# v047 研究地图

## Run 内事实诊断

- 按 `crl-active-diagnosis` 收集 `v047-frontier-reset-002`；诊断权威性为 `ADVISORY_NON_AUTHORITATIVE`。
- 当前版本没有实验尝试、比较文件或检索快照；Run-wide 已识别 46 个科学版本。
- 全文索引为 `READY`，含 55,372 个分块；语义索引因未请求而单独为 `DEGRADED`，不影响全文索引可用性。
- 诊断没有选择或杀死候选；主研究者将其解释为近期主要问题是先行工作碰撞，而非连续实验反证。
- 事实路径：`workbench_v047/diagnosis/v047-frontier-reset-002/`。

## 用户在环任务现象

- AppWorld-UL 从有状态 AppWorld 任务构造 516 个用户在环任务，覆盖目标欠明确、目标不可行、执行前确认及其组合；每项任务把只由用户掌握的信息表示为知识集合。
  - https://arxiv.org/abs/2607.20536
  - https://appworld.dev/appworld-ul/
- 论文公开例子显示，智能体通常必须先搜索邮件、订单、库存、价格或文件，才能知道应问什么；这些共享步骤主要是只读检查。发送、购买、退货或设置闹钟等有副作用动作则位于用户意图分叉之后。
- 因而“在澄清前执行最长共同前缀”在现有公开例子上主要退化为正常的环境探索，尚未建立非平凡、可安全写入的共同动作前缀现象。

## 直接先行覆盖

- Uncertainty-Aware Clarification in LLM Agents with Information Gain 采用“执行后澄清”：澄清器只在工具调用及其观察之后运行，使问题绑定实际环境反馈；其公开提示还明确要求不得询问可从工具取得的数据。
  - https://arxiv.org/abs/2606.03135
- Structured Uncertainty guided Clarification 已把工具参数上的规格不确定性与模型不确定性分开，并以期望完美信息价值和提问成本决定何时问、问什么以及何时停止。
  - https://aclanthology.org/2026.findings-acl.2028/
- AppWorld-UL 本身用知识边界约束模拟用户：知识集合外的问题会被转回智能体自行通过工具处理，并单独报告提问精度和召回。

## 结论

候选的两个核心步骤——先从环境取得可观测事实，以及不向用户询问工具可取得的信息——已经被执行后澄清框架直接实现；“共同前缀”在公开任务例子中又没有展示独立的有副作用计算。v047 不注册正式假设。
