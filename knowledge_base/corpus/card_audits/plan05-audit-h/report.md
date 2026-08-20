# PLAN_05 A3 Card 独立来源审计报告

## 总结

审计范围严格限于指定的 13 张 Card；未读取既往 source-audit、Candidate、Commissioning 或 Reviewer 文件，未启动科研三审，未评价 Candidate，未修改任何文件。

实际核对：13 张 Card 全文；scratch SQLite 中对应 21 条 Evidence 与 passage；正式 `evidence.json`；P077–P083 七份 PDF 的相关物理页与邻接上下文；七份 reconciliation/read reports。21/21 Evidence quote 与 passage 字符切片精确一致，21/21 passage hash 有效，7/7 PDF SHA 与 Card/SQLite 一致，13/13 Card 机械 validate 通过。共核对 31 处 `[AUTHOR_FACT]`，全部有 Evidence 与原文支持；没有 `[AUTHOR_INTERPRETATION]`。

问题主要是部分 `[CODEX_SYNTHESIS]` 把未隔离因果写成 failure，或没有显式保留 oracle、成本、baseline 公平性及适用范围。结论：`PASS 4 / REVISE 9`。

## 逐卡结论

### 1. `operator-hierarchical-utterance-critic-token-actor` — PASS

物理页 5 支持 utterance-level TD critic 与 token-level policy-gradient actor；页 12 支持 Twenty Questions 的条件性 trajectory 比较；页 23 支持 simulated oracle 与 reward-hacking patch。Card 没有偷换成 token、wall-clock 或通用效率，且保留项目排除边界。

### 2. `operator-validated-specialized-tool-creation-retrieval` — REVISE

机制事实与页 4 一致。风险段需保留：GPT-4 借助已知 source answers 构建/裁决工具库；离线创建约 USD 2,500；TabMWP 上 BM25 89.2 高于 CRAFT 88.4；CREATOR checking/rectifying loop 被移除；没有 equal-total-token/API/cost 比较。`validated toolset` 必须明确只证明 originating-instance preservation。

### 3. `operator-action-preserving-observation-contextualization` — REVISE

ground-truth action retry 与 Filter-List unseen-category 零提升均有原文支持。标题 `Action-Preserving` 暗示未被 fidelity metric 证明的保真；contextualizer 明确同时生成 reasoning 与 next-step rationale；每动作增加一次调用，训练依赖强 teacher/judge，且没有 matched-token/latency/teacher-supervision baseline。建议标题改为 `Next-Action-Supervised Observation Contextualization`。

### 4. `operator-gold-supervised-hindsight-search-depth` — REVISE

gold-supervised/hindsight 命名正确。需补：失败轨迹 `t_c=-1` 与 prose `t_c>T` 的形式化歧义；诊断/提示范围实际为 0–4 searches；average search depth 只是代理成本，每步 intermediate answer、PPO training 与 retrieval latency 未计入，未证明 net deployment cost reduction。

### 5. `operator-fixed-budget-independent-path-aggregation` — PASS

独立路径、40 samples vs greedy 与 fixed-answer boundary 均有原文支持。Card 已明确 equal candidates 不等于 equal tokens、latency 或 tool calls。

### 6. `operator-future-token-loss-filtered-tool-learning` — REVISE

训练计算与 limitation 均准确。`top-10` 应精确为 `<API>` token 进入 top-10 候选时允许触发；需保留 GPT-J-6.7B 外还调用 Atlas-xxl QA、Wikipedia BM25、NLLB 等外部系统的总系统规模/成本，以及部分任务接近 98% 调用率并非自然 top-1 calibration；“直接祖先”需改为“早期代表性方法”。

### 7. `failure-token-local-credit-misses-turn-level-delayed-value` — REVISE

事实准确，但标题和 failed intervention 把 PPO–ArCHer 差异主要归因于 token-local credit；比较同时改变 on/off-policy replay、critic 粒度、actor-critic computation 与 sample reuse，原文只把高 variance 写成 likely。建议标题改为 `Token-Level On-Policy PPO Can Be Sample-Inefficient under Turn-Level Delayed Rewards`，并明确没有隔离唯一原因。

### 8. `failure-generic-or-unvalidated-tool-libraries-add-distractors` — REVISE

基线事实准确，但来源没有直接测 `distractor-induced error`，也未隔离“扩大错误选择面”的因果。建议标题改为 `Generic or Unvalidated Tool Libraries Can Fail to Improve and May Hurt`，把 distractor 机制降为 hypothesis，并补 GPT-4/答案、约 USD 2,500、BM25 与被删 CREATOR correction 等公平性边界。

### 9. `failure-raw-observation-overload-hides-action-relevant-ui` — REVISE

直接观察到的是 contextualizer 在未见 Filter-List affordance 上漏必要元素并保持 0% success；不能反向证明 raw observation 隐藏元素。建议标题软化为 `Lengthy Raw Observations May Obscure Action-Relevant UI`，把 overload 写为 hypothesis/author motivation，并补 planning、fidelity 与每步调用成本边界。

### 10. `failure-fixed-search-depth-causes-under-and-over-search` — PASS

NQ/Bamboogle 与不同模型曲线直接支持任务/模型依赖深度、过搜与性能下降；Card 已保留 gold、低最大步数与同成本对照。

### 11. `failure-interactive-gains-collapse-against-independent-sampling` — REVISE

P081 没有实验 reflection、debate、tree search 或 multi-Agent；`Observed failure` 应降为 `[CODEX_HYPOTHESIS]`。等候选独立采样只是必要对照，残余增益还可能来自 prompt、aggregator、parser、token/tool budget，不能视为充分因果证明。

### 12. `failure-likelihood-utility-does-not-guarantee-agent-utility` — PASS

Card 使用“does not guarantee”是恰当 proxy boundary，并明确 task success、wrong-call harm、call count/latency 与 chaining 的下游检查。

### 13. `failure-multi-agent-adversarial-coordination-spans-trust-surfaces` — PASS

三类攻击面、轻量防御失败与 simulated-tool 边界均准确；没有把防御写成成功 Operator。

## 必须优先修正的未验证假设

1. P077：把 PPO–ArCHer 差异唯一归因于 token-local credit。
2. P078：把基线退化因果归因于 distractors。
3. P079：把作者 raw-observation overload 动机写成已观察机制。
4. P081：把等预算独立采样后的残余增益视为 interaction 的充分因果证明。

这些内容应降级为 `[CODEX_HYPOTHESIS]` 或增加隔离实验，不能以确定性综合承担来源事实。
