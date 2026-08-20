# v001 研究地图

## 已核对的强先行与杀伤范围

- `P040`，*From Confident Closing to Silent Failure*（2026）：在 tau2-bench 与 AppWorld 上证明代理会在环境状态未完成时声称成功；直接轨迹—环境一致性检查被作者明确列为高风险部署方向。杀死“首次发现假成功”主张，但没有直接比较合法空结果、明确失败与未知副作用的控制决策。
- `P074`，*ToolGate*（ACL Findings 2026）：用 Hoare 风格前置/后置条件约束工具调用和可信状态提交；原文说明 ToolBench 约四分之一缺少结构化响应模式的工具把后置条件退化为恒真，且空值是否非法取决于模式。杀死通用“后置条件核验”方法主张。
- `P039`，*ToolFailBench*（2026）：区分工具跳过、结果忽略、捏造和不必要调用。杀死“最终准确率首次掩盖结果处理错误”主张。
- SABER（arXiv:2512.07850）：在可变更动作前做用户核验与定向反思。杀死一般的“可变更动作门控”主张。
- *FAILING TOOLS*（ACL ARR 2026 May）：覆盖静默无操作、陈旧数据、损坏状态、模式不匹配及恢复证据义务。杀死一般的“运行时工具失败恢复基准”主张。
- *Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures*（arXiv:2608.02645）：组合后置条件核验、重试前核验与幂等键。杀死非原子写入恢复包装器主张。
- OpenAgent（ICML 2026，arXiv:2607.01084）：系统测试查询、工具、观测与领域漂移，包括 JSON 到 Markdown/原始日志的返回格式变化。杀死一般的“工具结果格式不变性”主张。
- *Adjudicating Artifact-Faithfulness Claims in Tool-Using LLM Agents*（ACL ARR 2026 May）：区分调用核验器后产物仍违背核验结果的失败。杀死一般的“工具调用但未采纳结果”主张。

## 当前可能剩余的贡献差分

现有工作分别处理失败恢复、后置条件、格式漂移和结果忠实性，但尚未从已核对材料中看到一个把“合法空、明确失败、未知副作用、语义无操作、已确认成功”作为同形工具观测的控制语义进行配对测量，并比较原始响应、通用策略提示、模型自解析和显式分面契约的工作。

该差分很脆弱：它可能只是结构化接口的工程常识，也可能被强提示完全吸收。首轮实验专门用于杀死这种伪贡献。

## 可审计来源

- 知识库搜索：`hypotheses_v001/searches/broad-frontier-001/`
- 知识库定向搜索：`hypotheses_v001/searches/outcome-semantics-001/`
- 知识库论文：`P039`、`P040`、`P074`、`P073`、`P084`。
- 最新先行网址：
  - https://arxiv.org/abs/2512.07850
  - https://arxiv.org/abs/2608.02645
  - https://arxiv.org/abs/2607.01084
  - https://openreview.net/pdf?id=j7YsSnA64D
  - https://openreview.net/pdf?id=40wuXQMQRU

