# v073 研究图谱

## 直接诊断

- *Lost in Execution: On the Multilingual Robustness of Tool Calling in Large Language Models*（ACL 2026）提出 MLCL，系统评价中文、印地语和低资源伊博语工具调用。它直接发现：许多失败发生在意图理解和工具选择正确之后，主导模式是参数值语言不匹配——模型生成用户语言中的语义正确值，却违反语言无关的执行约定；论文还评价了多种推理期系统策略。
  - https://aclanthology.org/2026.acl-long.2039/

该工作精确覆盖本版最有可能形成的现象与“推理期语言规范化”方法。

## 多语言与地域化基准

- *International Tool Calling* 包含 3,571 个真实 API、17,540 个任务、20 个类别和 40 个国家，并以多语言微调改善跨语言泛化。
  - https://arxiv.org/abs/2603.05515
- *Ticket-Bench* 在六种语言中使用地域化球队、城市与用户画像，测函数调用准确率和跨语言一致性。
  - https://arxiv.org/abs/2509.14477
- *X-WebAgentBench* 在交互式网页环境中评价多语言规划和交互，并比较跨语言对齐方法。
  - https://arxiv.org/abs/2505.15372
- *FahMai-TeleBench* 为泰语/英语企业目录提供四种工具制度，并报告低资源语言与工具模式宽度的交互影响。
  - https://openreview.net/pdf?id=ZdatfV6rxt

## 邻近方法

- *MPR-GUI* 构造六种语言严格对齐的界面环境，定位语言敏感层并用跨语言干预缩小差距。
  - https://openreview.net/forum?id=OY4AkzNLt4

## 结论

跨语言工具调用的现象、参数值语言错配、对齐环境、推理期策略和多语言训练数据均已有直接工作。把参数值先翻译成英语、增加语言标签或加入本地化词典只会复现 MLCL/ITC，不注册实验。
