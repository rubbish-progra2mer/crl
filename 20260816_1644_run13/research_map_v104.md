# v104 研究地图

## 最新直接工作

- [Diagnosing Search Behavior and Failure Modes in Long-Horizon Search Agents](https://arxiv.org/abs/2608.01913) 已分离检索缺口与利用缺口，并以累计召回、冗余查询和证据充分性分析长搜索。
- [When Should Multi-Round RAG Stop?](https://arxiv.org/abs/2608.13237) 已直接研究结构化停止判断与检索轮次缩减。
- [Not Worth Another Token](https://arxiv.org/abs/2608.08389) 已以边际价值估计决定深度研究是否继续消耗检索与生成预算。
- [Exact Adaptive Hybrid Retrieval Without Fixed Top-L Cutoffs](https://arxiv.org/abs/2608.07152) 已直接去除固定 Top-L 截断并提供精确自适应混合检索。
- [What Would Fix This RAG Failure?](https://arxiv.org/abs/2608.08944) 已用配对证据干预审计回答是否对关键证据变化作出反事实响应。
- [Search, Inspect, Fetch](https://arxiv.org/abs/2608.02751) 与 [Fetch-then-Explore](https://arxiv.org/abs/2608.02097) 已把选择、结构检查、内容提取和持久工作区探索解耦。
- [Position Bias Undermines Preference Consistency in Listwise LLM-Based Reranking](https://arxiv.org/abs/2608.03091) 已直接处理列表排序中的位置偏差。

## Run 内边界

- v002 关闭描述扩展、候选截断和检索—选择错位；
- v006 关闭工具结果取得但不影响最终动作的反事实利用问题；
- v010 关闭分页/分区/筛选/快照覆盖义务；
- v050 关闭随计划展开的依赖闭合检索与自适应 Top-K；
- v081 关闭深度研究证据充分性停止；
- v095 关闭不可回答问题上的过度搜索。

## 归约

隐藏低排名关键证据的实验测量召回或固定截断；置换候选顺序测量位置偏差；替换关键片段测量反事实利用；追加检索轮次测量边际价值与停止。四种实验均有直接工作和 Run 内边界，不能产生新计算。
