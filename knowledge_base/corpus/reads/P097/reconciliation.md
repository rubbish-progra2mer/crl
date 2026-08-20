# P097 reconciliation — ReLoop

Disposition: `FAILURE_QUANTIFICATION_AND_OPERATOR_ADMISSION_WITH_RETRY_BUDGET_AND_CITED_BASELINE_BOUNDARIES`
Read 1: `corpus/reads/P097/read_1.md`
Accepted read-2: `corpus/reads/P097/read_2_attempts/r2-20260727-p097-a1/`
  - report SHA-256: `78fd45c9bae3552d632ce2a7a529e51d3e841f228561bf712207bce8a31791d6`（21,405 B，已对盘复核）
Other attempts: none
Reconciler: main Codex, 2026-07-27

## Source reconciliation

2. **AGREE｜消融与互补性**：+CoT 是 Claude 组合问题主驱动（+8.5pp）；L2 在 MAMO 局部缺陷上最大单项（+4.4pp）但对 RetailOpt 严格精度零贡献（结构性错误扰动测不到）；CoT 使 DeepSeek 执行崩塌、毁 SFT 模型（84 崩+65 回归）；IndustryOR 偏差双峰（34%<1% + 47%>10%，可修复带为空）；修复 LLM 会伪造数据（safety check 动因）。
3. **ACCEPT-BOUNDARY（read-2 新增，重要）｜重试预算混杂**：ReLoop ~3× token 成本、L1/L2 各 ≤3 次再生成/修复，而 Base 单次调用；**无等预算盲重试对照**——Exec% 增益（如 OptMATH 2.6→17.9）中"诊断质量"与"重试次数"贡献不可分。Acc 侧 +CoT（同为单次）与 L2 增量（回滚保护）部分免疫。
4. **ACCEPT-BOUNDARY（read-2 新增）｜引用基线**：MAMO/IndustryOR 上 4/5 模型的 Base 数字**引自 SIRL 论文**而非复跑，harness 对齐未描述——Base→ReLoop 跨基准增量含此不确定性；OptMATH 的 MAMO 高 Base 有训练-评测重叠疑虑（作者自曝脚注）。
5. **ACCEPT-BOUNDARY（read-2 新增）｜RetailOpt 自建自评与脚手架**：prompt 自带与参考 MILP 同源的结构线索（无脚手架时全模型近零）——绝对准确率部分测"遵循给定约定"，跨配置比较仍公平但不外推；gold 为作者手工形式化；全部结果 single-run pass@1 无误差条（checklist 自认）；阈值敏感性只有一句话无表格。
6. **ACCEPT-NOTE（read-2）**：L2 与生成共享 LLM（失败相关，作者自认，cross-model verification 留未来）；仅 Gurobi；checklist 与正文 Limitations 清单轻微不一致；IndustryOR "longer" 与其 token 统计（267<459）表观矛盾（或指推理链）；GitHub 声明与 checklist "upon acceptance" 措辞不一致；A.7 替代方向 35% 错误率是 pilot 级。
7. **AGREE｜内部一致性正面项**：Table 23 每族汇总与 Table 5 总量可复算吻合（43/190、59/190）；+8.5/+4.4 可复算。

## Frozen source role

- **不是什么证据**：不证 L1 诊断相对等预算盲重试的净价值（无对照）；跨基准 Base→ReLoop 增量点值不引用（引用基线+harness 未对齐）；RetailOpt 绝对准确率不外推到无脚手架场景；无统计区间——一切幅度按方向引用。
- 状态：preprint（NeurIPS 格式投稿态）；代码仓库可用性未核验。
