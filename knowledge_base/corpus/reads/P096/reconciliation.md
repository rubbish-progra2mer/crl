# P096 reconciliation — VeriSimpl

Disposition: `KEY_ANCHOR_ADMISSION_WITH_BEST_OF_K_CONFOUND_AND_CASE_TRANSCRIPT_DEFECTS`
Read 1: `corpus/reads/P096/read_1.md`
Accepted read-2: `corpus/reads/P096/read_2_attempts/r2-20260727-p096-a1/`
  - report SHA-256: `2bdcd0d9399a6d1b7e357516d944dd235ecb1b8227c39eb640b72cb609cd686c`（20,620 B，已对盘复核）
Other attempts: none
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜身份与机制**：ICML 2026（PMLR 306 页脚自证）；simplification-based verification 反转（solver 出降维查询、LLM 裁决）；三路信号（约束三型突变 / 单变量+全变量掩码 / 类型检查）字典序聚合的 **best-of-K（K≤10）选择器**；主结果 GPT-4o 平均 65.5 / R1 72.8 跨三底座一致；自验证 precision 91.5%（GPT-4o）/低覆盖 23-34%。
3. **ACCEPT-BOUNDARY（read-2 新增，重要）｜best-of-K 混杂**：无任何算力配平对照（多数投票/自一致性/随机选可执行者）；消融显示任何单一验证信号的 10 候选选择器即达 62.2-64.8（vs BASELLM 56.8），采样+任意选择器贡献 ~5.4-8.0 点，验证信号叠加边际仅 ~0.7-3.3 点——**增益的大头可能是 best-of-K 效应而非验证信号本身**；token/调用数/成本全文未报。
4. **ACCEPT-DEFECT（read-2 新增）**：(a) **CompOR 仅 17 题**（公开可用子集）——该列 100% precision 建立在极小 n 上；(b) 有效分母与声明不符（NLP4LP 百分比吻合 /62 或 /61 而非 67；IndOR 吻合 /96 或 /95 而非 100）——疑存在未声明剔除；(c) **A.2/A.3 两个成功案例的 LLM transcript 与其题目数值完全不符**（疑贴入他实例记录），示证价值存疑；(d) R1 存在两套不一致数字（Table 2/3 vs Table 13）；(e) accuracy 判定标准（容差/比对方式）全文未定义；(f) δ、singleton 上界、K 敏感性、tie-breaking 均缺；(g) R1 的验证 precision 反而低于 GPT-4o（78.5 vs 91.5，未解释）；(h) 多处小笔误与 "System-10" 内部代号残留。
5. **AGREE｜oracle 无泄漏**：验证 oracle 由 solver 对候选自身模型算出，数据集真值不进验证环节；LLM 只见 NL+数据+具体 valuation。

## Frozen source role

- **不是什么证据**：不证验证信号相对朴素 best-of-K 选择器的净贡献（无配平对照）；不证 CompOR 级别结论（n=17）；A.2/A.3 案例不作机制证据（transcript 错配）；R1 数字引用需注明表号；accuracy 绝对值不跨文比较（判定标准未定义）。
- 状态：published（ICML 2026）；上述缺陷为发表版自带，引用时逐项连带。
