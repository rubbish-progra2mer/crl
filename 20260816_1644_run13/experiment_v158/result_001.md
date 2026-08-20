# v158 Recorded 结果 001

## 记录

- 记录标识：`e2-full-graph-marginal-counterexample-001`
- 状态：`SUCCESS`
- 层级：`RECORDED_NON_SUPPORTING`
- 运行时长：5.516 秒
- 标准错误：0 字节
- 记录文件：`experiment_v158/recorded/e2-full-graph-marginal-counterexample-001/record.json`
- 程序：`workbench_v158/e2_full_graph_marginal_counterexample.py`
- 输出：`workbench_v158/e2_full_graph_marginal_metrics.json`
- 程序 SHA-256：`86bce9a5ea21077a560a394724a55a618947dbe9fab8977345d650d5c1e50b3e`
- 输出 SHA-256：`987f19d7d9745c986570c09d51abcf235a7f124bafa3a4ac6b1c7b3c6a2a718a`
- 记录 SHA-256：`a6288c105dfc2577898c283240cc870555d82106f44e6f7296eb476c90509861`

## 预注册结果

全部判据通过：

- `m=6` 全枚举的单调性违例为 0、次模性违例为 0；
- 五个规模中 `bundle` 的完整图删边效应均为 0，碎片边效应均严格为正；
- 全部 119 个 `m,k` 条件中，一阶前 `k` 名均排除 `bundle`，被选效用精确为 `k/m`；
- 同预算最优解均包含 `bundle` 且严格优于一阶选择；
- 从空集重算条件边际的贪心在全部条件中达到最优；
- `m=64,k=1` 的一阶选择效用为 `1/64`，最优值为 `4096/4097`，近似比为 `4097/262144`。

## 解释

该构造证明：即使通信子图效用是良性的单调次模覆盖，完整图中的冗余也能把“单独覆盖全部核心需求”的边压成零边际，同时让各碎片边因独占微小附加信息而获得正边际。先固定完整图算分、再按预算截断可以随规模任意接近零近似比。

结果不证明 E2-Explainer 在 MMLU、HumanEval 等真实基准上的报告错误，不评价其语义熵辅助项或摊销预测器，也不把条件边际贪心、最大覆盖或联盟归因视为新方法。
