# v055 研究地图

## 现象与直接先行工作

- *Agentic Auto-Research is Fuzz Testing* 已把自动科研形式化为反馈引导搜索，明确要求廉价密集信号只负责导航，最终发现必须由免受自适应复用影响的受保护证据裁决，并提出检验受保护验证能否减少错误发现。
  - https://arxiv.org/abs/2608.09855
- *The More You Automate, the Less You See* 对 Agent Laboratory 与 AI Scientist v2 的候选选择做操纵实验，报告奖励函数接触测试表现会引入事后选择偏差。
  - https://openreview.net/pdf/2cdf4ddde7951396651a1b688f5eb1201cd09746.pdf
- *Adaptive Learn-then-Test* 已用 e-过程实现顺序、数据依赖的多重假设检验与提前停止，并明确在自动提示工程中验证其效率和有限样本有效性。
  - https://openreview.net/forum?id=JxnOZwFNcU
- *Preserving Statistical Validity in Adaptive Data Analysis* 已建立反复、自适应查询同一数据时维持统计有效性的通用理论。
  - https://arxiv.org/abs/1411.2664

## 候选计算

草案把每次实验拆成两个通道：公开给智能体的密集进展信号用于候选变异和预算路由；隐藏验证流只在候选提交后产生顺序 e-值，并按候选谱系分配检验财富。最终交付必须跨过验证流，而不能用搜索分数替代。

## 差分审计

双通道“导航而非裁决”和受保护验证已由最新自动科研工作直接提出；顺序 e-值、数据依赖多重检验、提前停止及其在提示工程中的使用又由 aLTT 直接实现。按候选谱系记账只是把现有在线多重检验的索引换成变异树，没有改变统计保证或智能体搜索计算。

## 结论

问题重要，但没有剩余论文级方法内核；v055 不注册假设、不重复已有统计模拟。
