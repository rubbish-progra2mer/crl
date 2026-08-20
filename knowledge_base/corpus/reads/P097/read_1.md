# P097 first read (W06) — P097 ReLoop：feasibility–correctness gap 量化 + 行为扰动验证

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization
- Authors: Junbo Jacob Lian; Yujun Sun; Huiling Chen; Chaoyu Zhang; Hanzhang Qin; Chung-Piaw Teo（Northwestern/NUS/CityU HK 等，共同一作，Preprint 自标）
- Identity: arXiv 2602.15983v2 (2026-04-29)，cs.SE；代码与基准 `github.com/junbolian/ReLoop`
- PDF: `knowledge_base/staging/w06_targeted/P097_reloop.pdf`
- PDF SHA-256: `8563653b872e78822f024b4d2f11532f75354e98c729ed26ac5bbf9675724c66`
- Parse check: 39 physical pages

## Canonical contribution

定义并量化 **silent failure**（执行无错+solver 可行+语义错误）与 **feasibility–correctness gap**：RetailOpt-190 组合型问题上 DeepSeek-V3.2 solver-feasibility 91.1% 而严格正确率仅 0.5%（Table 5）。两机制：**结构化生成**（understand→formalize→synthesize→verify 四阶段单调用 CoT，含显式变量类型推理）与**行为验证**（Property 1 扰动敏感性：对应约束/目标项的参数被极端扰动后目标必须显著变化；CPT 约束在场测试 + OPT 目标项在场测试，r<5% 报 WARNING 修复、5-30% 仅记录、>30% PASS）；L1 执行层（语法/不可行 IIS/无界 ray 诊断再生成）阻断，L2 非阻断+回归回滚守卫。发布 RetailOpt-190（38 原型×5 数值变体，8 族组合约束，Gurobi 手工形式化作 gold）。


## Evidence and closest lineage

- 主结果（Table 5，RetailOpt-190，pass@1 温度 0）：Claude Opus 4.6 Base 72.1% Exec/22.6% Acc → ReLoop 100%/31.1%——**三分之二仍是 silent failure**；DeepSeek 91.1%/0.5% → 97.4%/5.8%；三个 32B 模型（Qwen3-32B、OptMATH-SFT、SIRL-RL）接近全零（组合结构超出其推理容量）。
- 跨基准（Table 6）：MAMO-ComplexLP 上 Claude 70.4→79.8（L2 是最大单项贡献 +4.4pp）；IndustryOR 上 DeepSeek 50.0→62.0（主要 L1 恢复）。
- 消融（Table 7）：机制按错误结构互补——组合问题上结构化生成主导（+8.5pp）；局部缺陷上 L2 主导；**L2 对 RetailOpt 严格正确率零贡献**（错误主要是结构性重分解，扰动响应看似合理）。CoT 使 DeepSeek 执行崩塌（91.1→53.2，中间数学记号破坏语法）、使 SFT 模型灾难（OptMATH 84 崩+65 回归）。
- IndustryOR 偏差双峰：34% 偏差 <1%（系数级，扰动测不到）+47% >10%（结构性，3 轮修不动）——**可修复带几乎为空**。
- 谱系（Table 1）：与 Self-Refine/Reflexion/LEVER/OptiChat 的四范式对照；敏感性分析被改用途为"测敏感性是否存在"。

## Measurement and fairness boundaries

- 正确性判据是**解级**的：可行状态匹配 + 目标值相对误差 <ε（严格 1e-4/实用 1e-2）——不做逐约束 enforcement 判定；"结构性 silent failure 扰动测不出"是作者自认的检测边界（Limitations：系数量级错、形式化等价错、未表示结构三类超出范围；L2 与生成共享 LLM 有失败相关性）。
- RetailOpt gold 为作者手工形式化（Appendix A），5 变体共享原型（聚类单位=原型 38 非 190）；ReLoop 增 ~3× token 成本（自报）；greedy pass@1。

## Draft knowledge objects

### Failure draft: `Solver Feasibility Is a Near-Zero-Information Proxy for Formulation Correctness`

组合型问题上 91.1% 可行 vs 0.5% 正确；最强模型经全套验证修复后仍 2/3 silent failure；系数级与结构级错误双双落在行为扰动的检测范围外（偏差双峰、可修复带为空）。

### Operator draft: `Behavioral Perturbation Testing (CPT/OPT) with Graduated Non-Blocking Repair`

对候选形式化的每个声称组件做极端参数扰动、以目标响应缺失判定组件缺席；WARNING 才修、回归即回滚。Intervention target = 生成后验证步；前提 = 缺陷是局部的（缺约束/漏目标项）；结构性重分解与系数错不可测。

## Draft Evidence locators

- Physical p.1-2: 摘要、90 点 gap、逐字引语句、贡献清单。
- Physical p.3: Table 1 验证范式对照、Def.1/2、Property 1。
- Physical pp.4-6: 四阶段生成、L1/L2 机制、Table 2 严重度矩阵、阈值。
- Physical pp.7-9: RetailOpt-190 构成（Table 4）、Table 5/6/7 主结果与消融、IndustryOR 双峰、Limitations。

All claims remain draft until independent read and reconciliation.
