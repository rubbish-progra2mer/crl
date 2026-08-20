# P099 reconciliation — Verus-SpecGym

Disposition: `EVALUATOR_AND_FAILURE_ADMISSION_WITH_BUDGET_CONFOUND_AND_JUDGE_CONFIG_BOUNDARIES`
Read 1: `corpus/reads/P099/read_1.md`
Accepted read-2: `corpus/reads/P099/read_2_attempts/r2-20260727-p099-a1/`
  - report SHA-256: `e9e6cdea52c964202226ba838b81c07994c0bd45f9c22f9c07c0f89ffc4e64ea`（17,742 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**（无事实冲突；read-2 对 read_1 一处措辞作了收紧，见第 4 条，属细化非矛盾）。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜身份与机制**：58 页 preprint（CMU+Amazon）；不提规格生成新方法，改变的是**评测端判定函数**——exec_spec 扩展把规格谓词编译为可执行 Rust + 符号检查优先/执行回退两级流水（六类 resolution）+ {pre,post}×{completeness,soundness} 四桶测例（官方测试 + 人写 hacks 经平台裁决路由）；exec_spec_unverified 砍对应性证明以消评测器伪失败；字节级 round-trip P(R(t))==t 验收转换。
3. **ACCEPT-BOUNDARY（read-2 新增，重要）｜预算型评测的跨模型混杂**：$2.5/题 + 75 分钟墙钟下，API 延迟决定交互轮数、prompt-cache 定价决定实际 token 量（作者自认）；且 400 API 调用上限在 App F（未限定范围）与 Table 1（仅标开源组）两处表述不一致（OPEN）——**模型间量的排名部分含非能力因素**，"任务对所有模型都难"的定性结论不受影响。弱开源模型的低分部分是"停不进 exec_spec 语言片段"（多桶被编译错误主导），维度上是能力但与规格化能力不同层。
4. **ACCEPT-NUANCE（read-2 细化）｜测试规模消融的实际形状**：read_1 的"测试数量增加使成功率稳定下降"须收紧——量化支撑主要是 **soundness 桶有无**的消融与判官对照；数量维度上 F.8 是均匀子抽样下的回溯计算（桶间独立假设、非重跑），结论反而是**小预算已近饱和**（post-completeness 桶饱和最慢 m≈50–75）。"稀疏测试高估忠实性"成立的主轴是**方向缺失**（漏 soundness 桶）而非测例条数。
5. **ACCEPT-BOUNDARY（read-2 新增）｜判官配置与代码-规格对照的限定**：判官仅测自评、静态一次性、无执行工具——不排除更强判官配置（跨模型/带工具/投票）缩小 26% 差距，该 26% 证明的是"无执行的 LLM 判断漏掉可执行测试能抓的错"；F.6 的"代码易规格难"（81.8% vs 57.8%）任务不对等（Python vs Verus、官方测例 vs 四桶含 hacks），不是同一把尺子，作者措辞已自限。
6. **ACCEPT-NOTE（read-2）**：四桶标签本身是平台产物近似（Table 4 自注 "as approximated by benchmark testcases"）；构建期过滤链（无浮点、hack 时代题、每桶≥5、>200 抽 200）；内部小不一致——p.8 均值 "21 pre-sound" vs Figure 5 "Mean: 20"；completeness 桶 Max:100 堆积无正文解释（OPEN）；摘要区间表述粒度；覆盖性佐证 ≥86% 是单向的。
7. **AGREE｜负向结果（read-2 补强）**：pass@3=0.756 但 pass3 仅 34.8%（202/581）——规格生成跨尝试脆弱；难度单调衰减（最易档最好模型也只 0.90）；过度规格化是独立于欠规格化的失败模式（2074D：更复杂规格自身导致 post-completeness 失败）；符号可证但语义错的失败带。

## Frozen source role

- **不是什么证据**：模型间 Pass@1 排名不作能力结论（预算/延迟/缓存/步数上限混杂）；26% 不外推到带工具或跨模型判官配置；"测例条数越多越暴露"不成立（饱和快，方向缺失才是主轴）；四桶判定是有限测例上界近似，"全通过"≠忠实；代码-规格差距非同尺读数。
- 状态：preprint（v1）；GitHub 仓库未访问核验。
