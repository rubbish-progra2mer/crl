# v059 研究图谱

## 现象证据

- [TRACES](https://arxiv.org/abs/2608.11415) 用 42 篇撤稿、欺诈和伪科学论文构造研究设计探针；30 个模型的结果显示，模型经常在不可靠前提上继续深入设计，且匹配结构对照指向话题关键词而非稳健认识判断。
- [Don't Take the Premise for Granted](https://aclanthology.org/2025.findings-emnlp.44/) 已专门评价前提批判能力，发现多数模型依赖显式提示才检测错误，复杂和程序性前提更难。

## 直接方法与部件

- [SciFact](https://aclanthology.org/2020.emnlp-main.609/) 与 [SciFact-Open](https://aclanthology.org/2022.findings-emnlp.347/) 已实现开放科学文献中的主张检索、支持/反驳判定和证据理由。
- [CLAIMCHECK](https://aclanthology.org/2025.findings-emnlp.1185/) 已把论文主张、审稿弱点和有依据的核验绑定。
- [Web Search Is Not Enough](https://openreview.net/forum?id=yvivK8FdVI) 直接研究撤稿状态：网页结果能大幅提高状态回答，但模型仍可能不把该状态用于引用决策，说明检索与决策绑定是已知问题。
- [Pre-Generative Epistemic Gating](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6363538) 已在生成前推导最小认识模式、审计所需元素并产生绑定门记录。
- [HCRC](https://arxiv.org/abs/2607.04562) 又将推理写成由独立验证信号控制的谓词门状态转换。

## 差分审计

候选“前提审计器输出可信/不可信/未知，再硬门控下游研究设计”由科学主张核验、撤稿状态更新和生成前准入门直接组合得到。其变化只是域适配和系统连接；没有新的学习目标、推断结构或可证明性质。

显式“先质疑前提”提示已被前提批判基准证明是强吸收条件。即使本地实验重现 TRACES 失败，也不能恢复相对上述组件的贡献差分，因此不运行。
