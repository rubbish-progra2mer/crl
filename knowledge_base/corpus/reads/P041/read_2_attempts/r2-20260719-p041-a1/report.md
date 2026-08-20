# P041 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P041/read_2_attempts/r2-20260719-p041-a1/invocation.md`
- 论文：*LLM Agents Already Know When to Call Tools -- Even Without Reasoning*
- PDF SHA-256：`a05f71b904209ea49cbc9cd13434255aab4037f96640477810fb78a61b701ba0`
- [AUTHOR_FACT] 已逐页读取全部 34 个物理页；页码均为 PDF 物理页。

## 1. 改变的计算与 I/O

- [AUTHOR_FACT] WHEN2TOOL 从基础模型最后一个输入 token 的所有层隐藏状态拼接向量训练 L2 正则逻辑回归，输出“需要工具”的概率；阈值决定在生成前加入 soft prefill（“可直接作答”或“需要工具”）。hard prefill 则直接约束输出为答案或工具 JSON。（物理页 3–5，Method；短定位：“last input token”“all layers”“soft prefill”）
- [AUTHOR_FACT] 输入是问题、模型隐藏状态及模型/任务专属的 probe；输出是工具必要性概率及一个生成前控制提示。干预发生在主模型生成之前，不要求模型显式写 reasoning。（物理页 4–5，图 2/方法流程）
- [READER_INTERPRETATION] 方法改变的是**工具调用门控**而不是工具选择或参数生成；其部署前提是可访问中间隐藏状态，闭源 API 通常不满足。

## 2. 标签、基线与结果

- [AUTHOR_FACT] 必要性标签来自反事实的强制无工具运行：无工具仍成功标记“不必要”，失败标记“必要”。WHEN2TOOL 含 18 个环境、1,080 个训练与 2,700 个测试样本，覆盖 scale/knowledge/execution 三类。（物理页 5–6，Data construction；短定位：“forced no-tool”）
- [READER_INTERPRETATION] 该标签本身需要离线执行与任务正确性 oracle，因此“推理时低成本”不等于整个系统无 oracle 成本；标签还绑定特定基础模型能力。
- [AUTHOR_FACT] 对比包括五类 prompt（F/D/N/S/X）、Reason-then-Act 对应版本，以及后续的全参数 SFT。probe AUROC 约 0.894–0.957；阈值 0.5 平均减少约 48% 工具调用、准确率下降约 1.7 个点。（物理页 6–8，主表/图；短定位：“48%”“1.7”）
- [AUTHOR_FACT] 结果并非所有模型稳定：Llama-3.1 的 soft prefill 经常不被遵守，hard prefill 恢复门控但可能明显伤害准确率；例如阈值 0.5 时约 69.7，对应 Default 约 79.5。（物理页 8–9，trade-off 图表）
- [AUTHOR_FACT] 多跳任务上 Qwen 可减少调用，但部分 Llama 配置反而增加约 35%/82% 的工具调用，同时准确率提高，说明“省调用”与“做对任务”并非同一目标。（物理页 9–10，Multi-hop results）

## 3. 公平性、预算与迁移

- [READER_INTERPRETATION] Prompt-only/Reason-then-Act 是训练免费基线，而 WHEN2TOOL 获得了 900 个模型专属反事实标签和隐藏状态；比较支持“监督 probe 可形成更优 trade-off”，不能支持“同预算零监督优于提示”。
- [AUTHOR_FACT] OOD 设置仅在同一类别五环境中取三环境训练并作定性曲线比较；Search-o1 迁移只取 50/50 样本训练/测试。（物理页 9–11 与附录实验）
- [AUTHOR_FACT] 六个 Search-o1 任务中有四个表现较好，但 NQ 从约 44.8 降至 42，MuSiQue 的调用缩减也不优于基线；WHEN2TOOL 跨任务 probe AUROC 约 0.675–0.803，通常低于 in-domain。（物理页 10–11，transfer table）
- [OPEN_QUESTION] 原文没有证明不同模型、模型升级或不同工具成本下可共用一个 probe，也没有报告生产重标注频率。

## 4. 限制、Failure 与 Operator 候选

- [READER_INTERPRETATION] 明确 Failure：soft prefill 可被模型忽略；硬控制可节省调用却显著降低正确率；多跳中调用数甚至上升；迁移 AUROC 有明显衰减。
- [READER_INTERPRETATION] Operator 候选：在可访问隐藏状态且可获得反事实正确性标签时，以模型专属 probe 作为前生成工具门控，并把阈值作为成本—准确率控制旋钮。
- [READER_INTERPRETATION] 建议保留 changed-computation 证据，但必须同时记录隐藏状态权限、反事实 oracle、模型专属训练成本和 Llama 负结果；不能外推到闭源 API 或“所有模型已内生知道何时调用工具”。

## 5. 可视核验

- [AUTHOR_FACT] 已核对物理页 8 的主 trade-off 曲线/表格，模型间差异与解析文本一致；未见可视 PDF 与文本抽取冲突。

