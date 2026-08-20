# v114 研究图谱

## 不可行约束的最小放宽

- [Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools](https://arxiv.org/abs/2404.11891) 已把复杂自然语言规划编译成约束满足；对不可行请求直接提取不可满足核心、解释原因并提出个性化修改。
- [Learn to Relax with Large Language Models](https://aclanthology.org/2026.acl-long.48/) 直接把约束放宽策略、算法原理和可执行代码联合表示，并学习自适应放宽。
- [Trajectory2Task](https://aclanthology.org/2026.acl-long.2037/) 已把不可行原因、必须动作和禁止动作纳入可核验工具智能体任务。
- Run v056 已关闭工具缺口与任务不可达，v061 已关闭不可逆动作下的可选性保存。

因此“提取最小冲突集—按优先级放宽—重新规划”不是新的智能体计算。

## 数字与动作边界的结构弃答

- [Never the Number](https://arxiv.org/abs/2608.13926) 已明确提出“生成壳只能决定回答哪个问题，不能决定返回值”的可信核架构；不可表达的问题在结构上拒绝，并把同一不变量扩展到智能体动作。
- [SteerBench-Work](https://arxiv.org/abs/2608.12654) 已用证据反转镜像评价动作边界的继续/暂停双向门控，并发现主要错误是已消除风险后仍过度暂停。
- Run v047、v057、v076 与 v105 已分别覆盖信息来源、可证实动作、交付承诺和描述—行动断裂。

结构弃答和动作门控均已有问题、架构与评价，不能从“错误严重度”重新包装。

## 语言条件资源不平等

- [Measuring the Tokenization Premium](https://arxiv.org/abs/2608.09046) 在技术辅导语料上量化多语言分词溢价、有效上下文缩短与成本差异。
- [MAPS](https://aclanthology.org/2026.findings-eacl.42/) 已在 11 种语言、9,660 个智能体实例上评价多语言性能与稳健性，并报告退化随翻译输入量变化。
- [Cross-Lingual Token Arbitrage](https://arxiv.org/abs/2606.03618) 已为多语言代码智能体提供本地翻译与结构化重写中间件，在多个后端上降低 34%--47% 的提示词元并保持或提高任务准确率。
- [TokLens](https://aclanthology.org/2026.acl-srw.18/) 与 [TokCollate](https://aclanthology.org/2026.acl-demo.41/) 已提供跨语言分词质量、压缩率和公平性测量。

本机只具备少量开放模型；把任务翻译到低资源语言后，语言理解、预训练数据、翻译质量和分词效率同时变化。没有有效工具变量或同能力配对，无法把智能体结果差异归因于分词。现有工作又已提供直接智能体评价和中间件，因此不实验。

## 自然语言契约与可执行承诺

- [Evaluating Rational Contracting in Natural Language](https://arxiv.org/abs/2608.10475) 已评价长时、条件化、不完全供应契约的协商、可满足性、效率、互利性与履约。
- [PolicyKG](https://arxiv.org/abs/2608.09028) 已把自然语言政策中的义务、许可和禁止编译为道义逻辑与 SHACL 约束，并逐阶段验证。
- [IF:CARGO](https://arxiv.org/abs/2608.12195) 已采用“语言模型做受限语义编译、确定性引擎验证和执行”的分工。
- Run v076 已处理自然语言交付承诺与真实完成的边界。

“承诺编译器”只会组合直接契约评价、政策形式化与确定性执行。

## 决定

四条候选均在模型实验前被直接方法、Run 内负记忆或不可识别载体关闭。
