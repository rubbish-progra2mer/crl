# P100 reconciliation — Tool Shortlist Size (BoR)

Disposition: `OPERATOR_AND_FAILURE_ADMISSION_WITH_ATTRIBUTION_AND_CONDITIONING_BOUNDARIES`
Read 1: `corpus/reads/P100/read_1.md`
Accepted read-2: `corpus/reads/P100/read_2_attempts/r2-20260727-p100-a1/`
  - report SHA-256: `a40d2783a3e4bfec44dfb75835c95dab8917c3af64f2e94eb51268fed859b62b`（16,881 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**（无事实冲突；read-2 提供归属澄清与两处残余混杂，均为增量）。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜机制与定位**：改变的是"scorer 排序后、prompt 构建前"的截断步骤——展示深度 K 从固定超参变为评测对象（BoR = log2(Pobs/Prand)，超几何 Prand）与学习对象（STOP/CONTINUE MDP，STOP 命中奖励 −log2(Prand(kstop))，深度惩罚内生）；策略只看分数形状特征不看文本；RL agent 自我定位为度量探针非生产架构。
2. **ACCEPT-ATTRIBUTION（read-2 新增，建卡必须）｜BoR 指标归属**：BoR 本身出自引文 [30]（Repantis et al., ICLR Blogposts 2026，作者高度重叠），本文首句自认——**本文新贡献是把它用于工具选择评估并 RL 化**。Operator 卡中 chance-corrected 指标/BoRopt ceiling/doubling rule 的原始出处应指 [30]，本文提供的是奖励化 + 难度分桶 + 下游验证。
3. **AGREE｜主证据**：BFCL+BM25 90.3%@K=7.4 ≈ FK=50 的 90.8%（1/7 深度）；ToolBench 难度分桶分离（hard 桶 FK=5/FK=1/F1 全 0% vs BoR 16.7%；聚合 FK=5 64.7 反而 > BoR 61.9——聚合指标掩盖分布性失败）；F1 型固定深度惩罚无自适应（各桶 K≈1.5，SciFact K std=0.00）；弱 scorer 负结果（found@1=33% 时膨胀至 K=80.7/1.04 bits，换强 scorer 得 K≈2.3）；下游验证 over-presentation 有害（93.1 vs 87.1；medium 桶 76.8 vs 60.9；embed 复现更宽 96.1 vs 84.6）。
4. **ACCEPT-BOUNDARY（read-2 新增）｜下游验证的条件化选择偏差**：Choice Acc% 以"gold 被呈现"为条件，而各方法条件集不同——BoR 只在 76.9%（偏易）查询上呈现 gold，FK=5 在 84.2%（含更难）上呈现，93.1 vs 87.1 部分被此放大；方向性结论存活（FK=5 在 medium 桶内 100% 呈现仍只 60.9% 选对），但表面差距点值不引用。
5. **ACCEPT-BOUNDARY（read-2 新增）｜超参敏感与消融不齐**：下游 RL agent 用 step_cost=0.01 重训得 K=2.2，主表同条件 step_cost=0.005 得 K=7.4——同一奖励对 step_cost 敏感 3 倍以上，下游结论绑定特定超参；BFCL+BM25 条件的 F1 消融用简化变体（常数终端奖励），九条件中该条 F1 对比不同公式（作者自称偏保守）；MetaTool 六个条件为单 seed。
6. **ACCEPT-BOUNDARY（read-2 新增）｜构造性与量纲**：MetaTool/ToolBench 候选集为人工构造（gold 恒在内），Found% 绝对值依赖构造方式，不作对原基准的检索性能引用；MS MARCO 本地索引 ~51K 而 Prand 按全库 8.8M 计算——**奖励位数跨语料不可比**（20.28 bits 偏大）。工具域全部 Rq=1、最大真实 N=370、单 LLM（Claude Sonnet 4.6）下游、执行正确性超范围。
7. **ACCEPT-NOTE（read-2）**：found@1 两处口径不一致（p.5 60.0/73.2 vs p.8 65/77，OPEN）；下游 prompt 模板与强制单选实现未给出；基准均非为深度评估设计（作者自认并呼吁专用基准）。

## Frozen source role

- **不是什么证据**：下游 93.1 vs 87.1 点值不引用（条件化偏差+单 LLM+超参绑定）；奖励 bits 跨语料不比较；构造候选集数字不代表原基准检索性能；MetaTool 各条件单 seed 无区间；不证 Rq>1 或多轮执行场景。
- 状态：preprint（v2，Meta Platforms）；BoR 原始出处 [30] 未入库（引用时注明二手归属）。
