# 证据清单

## 文献与边界证据

- ToolGate，Findings of ACL 2026：固定霍尔式前置/后置契约与验证提交。https://aclanthology.org/2026.findings-acl.470/
- VERIMAP，2026：规划时为子任务生成验证函数。https://arxiv.org/abs/2510.17109
- Failing Tools，2026：把轨迹约束解释为证据义务和安全不变量。https://openreview.net/forum?id=j7YsSnA64D
- Verified Tool Calls，2026：固定写后验证、重试前验证与幂等键。https://arxiv.org/abs/2608.02645
- ETAS，2026：类型/效果语义、轨迹监控与动态资源残余义务。https://arxiv.org/abs/2607.17780
- AgentCheck，2026：模型上下文协议工具的系统故障注入工作台。https://arxiv.org/abs/2607.11098

以上来源只支持最近边界和问题存在性；它们不自动证明 PDEO 新颖。

## Run 内检索快照

- `hypotheses_v001/searches/initial-scope-001/`
- `hypotheses_v001/searches/orthogonal-tool-retrieval-001/`

## 负结果

- `workbench_v001/scratch_metrics.json`
- `workbench_v001/scratch_details.json`
- `failure_attribution_v001.md`

这些材料只支持 H1 淘汰，不支持 H4 交付。

## H4 Scratch

- `workbench_v001/pdeo_scratch_metrics.json`
- `workbench_v001/pdeo_scratch_details.json`

这些材料用于预检和实现修正，不是交付支撑。

## H4 Formal / Review-support

- `experiment_v001/specs/pdeo-plan-heldout-rules-v2.json`
- `experiment_v001/specs/pdeo-plan-variation-suite-v2.json`
- `experiment_v001/attempts/attempt-pdeo-plan-formal-002/execution.json`
- `experiment_v001/attempts/attempt-pdeo-plan-formal-002/metrics.json`
- `experiment_v001/attempts/attempt-pdeo-plan-formal-002/plan-variation-details.json`
- `experiment_v001/plan_variation_plan.md`
- `experiment_v001/plan_variation_result.md`

最终支撑是 `attempt-pdeo-plan-formal-002`。它在四个域、16 个计划变体和 178 个计划—状态案例上评价逐计划义务与探针编译，并以独立冻结输入提供评价规则。候选实现不读取该规则文件；但规则、计划与实现仍由同一主研究者在同一 Run 内设计，不能等价为外部独立基准。

关键源码随最终 Reviewer packet 直接提供正文：

- `implementation_v001/obligation_core.py`
- `implementation_v001/plan_variation_bench.py`
- `implementation_v001/formal_plan_variation_experiment.py`
- `implementation_v001/test_plan_variation.py`

## 较早 H4 证据与三审历史

- `experiment_v001/specs/pdeo-systematic-fault-suite-v1.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/execution.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/metrics.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/formal-details.json`
- `experiment_v001/plan.md`
- `experiment_v001/result.md`
- `review_v001/evaluations/eval-0001/aggregate.json`
- `review_response_v001.md`

第一套系统性状态变异实验用于证明闭集提交性质，但计划没有变化。评价规则与 PDEO 编译器在同一实验程序中以独立常量和函数实现；标签函数不调用编译器。首次固定三审有效，却指出它不能识别“计划派生”而非“每域固定契约”。因此它保留为较早支持，不替代最终的计划变化 Formal。

`attempt-pdeo-formal-001` 是同规格的早期有效运行，但其实现文件身份清单不完整，与最终实现 manifest 不匹配；它保留在 Run 中，不作为交付支撑。001 与 002 的数值指标除墙钟时间外完全相同。
