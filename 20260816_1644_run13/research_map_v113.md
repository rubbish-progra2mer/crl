# v113 研究图谱

## 查询相对的对象身份与计数单位

候选试图让同一批跨工具记录按用户问题选择“人、账户、订单、运送批次或事件”等不同等价关系，再进行去重和计数。它不是 v010 的分页完备性，也不是 v082 的事件流物化。

- [DocSage](https://arxiv.org/abs/2603.11798) 已直接从问题发现最小可连接模式，把分散信息转成关系表，执行跨文档实体连接和聚合。
- [EA-Agent](https://aclanthology.org/2026.acl-long.1420/) 把跨知识图实体对齐构造成结构化多步推理。
- [GRIT](https://aclanthology.org/2025.emnlp-main.1118/) 显式推断主外键关系，并把问题相关列与连接路径编码给语言模型。

剩余的“按目标实体键分组再计数”是经典关系代数。将 DocSage/实体对齐/关系分组串联，不形成新的智能体方法核。

## 澄清提问与偏好构造

候选现象是：带默认、顺序或不对称措辞的澄清问题不只测量已有偏好，也可能改变后续选择。

- [Asking Clarifying Questions for Preference Elicitation With Large Language Models](https://arxiv.org/abs/2510.12015) 已直接训练序列澄清问题来恢复用户偏好。
- [PEPPER](https://aclanthology.org/2025.findings-emnlp.1067/) 已指出预编码目标的用户模拟器会让系统走偏好获取捷径，并改用无目标模拟器让偏好在互动中逐步显现。
- [A Flash in the Pan](https://aclanthology.org/2025.coling-main.561/) 已实证提问轮数增加反而可能降低推荐质量，并给出偏好获取策略。
- [Toward Natural Language Mitigation Strategies for Cognitive Biases in Recommender Systems](https://aclanthology.org/2020.nl4xai-1.11/) 已把偏好获取中的认知偏差和自然语言缓解列为直接研究对象。

当前本地资源只能让另一个语言模型模拟用户，无法从模型受选项顺序影响推断真实人的偏好被构造。该实验载体不能提供所需外部效度；不能用模拟器行为替代真人证据。

## 跨工具统计粒度

候选试图区分订单级、行项目级、账户级与事件级汇总，阻止不同分组键的表在连接后重复扩张。

- [GRIT](https://aclanthology.org/2025.emnlp-main.1118/) 已提供多表关系模式、主外键与问题相关连接路径表示。
- [UNJOIN](https://aclanthology.org/2026.surgellm-1.pdf) 直接针对多表连接、分组、嵌套查询与聚合生成困难进行模式简化和查询翻译。
- [TAP4LLM](https://aclanthology.org/2024.findings-emnlp.603/) 已把问题相关表采样、增强与序列化作为通用预处理器。
- 文本到结构化查询错误分析已经把错误分组列、错误聚合和多余/缺失连接列为直接错误类型。

把分组粒度写成卡片再交给模型，是现有模式连接和确定性查询计划的界面重述；若由运行时直接计算，则语言模型不再承担核心聚合。两种形式都没有剩余新计算。

## 决定

三条候选在模型调用前均有决定性杀伤：前两条分别被直接方法/经典关系计算和评价载体不可识别性关闭；第三条被多表模式连接、分组聚合与表预处理直接覆盖。不注册假设或实验。
