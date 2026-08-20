# Seed Queries

## Keyword Queries

- `"tool-using LLM agent" AND ("silent failure" OR "semantic error" OR "incorrect tool output")`
- `("LLM agent" OR "language agent") AND ("observation corruption" OR "state drift") AND recovery`
- `("tool agent" OR "agentic workflow") AND (verification OR rollback OR retry) AND budget`
- `("LLM agent") AND (execution trace OR trajectory) AND (consistency OR fault localization)`
- `(tau-bench OR BFCL OR ToolBench) AND (reliability OR failure OR recovery OR verification)`

## Semantic Queries

- 智能体在工具返回没有报错、但内容错误时，如何判断哪些中间状态值得重新验证？
- 如何从长程执行轨迹中定位最可能导致终局失败的工具观测，并用有限预算恢复？
- 哪些方法显式改变验证/回滚的计算，而不是只增加反思提示或采样次数？
- 哪些基准具有独立终局、可控语义故障注入和可比较工具预算？

## Citation Expansion Starts

- 工具增强大语言模型综述与工具学习基准的故障/评价章节。
- tau-bench、BFCL、ToolBench 及其直接后继。
- 检索命中的选择性验证、执行校验、回滚或轨迹故障定位论文。

## Venue Filters

- NeurIPS、ICML、ICLR、ACL、EMNLP、NAACL、AAAI、IJCAI、WWW、KDD、ASE、FSE、ICSE；同时保留高相关 arXiv 最近预印本作为碰撞监控对象。

## Recency Filters

- 最近工作主窗口：2023-01-01 至 2026-08-13。
- 基准起源、经典规划/故障定位或软件补偿机制不设年份下限，但必须说明其仅是基础或相邻机制。
