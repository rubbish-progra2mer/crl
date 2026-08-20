# P101 reconciliation — Distilled Test Suites (limited admission)

Disposition: `LIMITED_ANCESTOR_ADMISSION_WITH_ONE_SIDED_AUDIT_AND_ADAPTED_METRIC_BOUNDARIES`
Read 1: `corpus/reads/P101/read_1.md`
Accepted read-2: `corpus/reads/P101/read_2_attempts/r2-20260727-p101-a1/`
  - report SHA-256: `d946bdb3c757a58f31eb9a4c9c31e59437dbc09e14a02be9be55e26eb18051be`（15,721 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**（无事实冲突；read-2 的数字校正与方向性限定均为增量）。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜机制与蕴含链**：改变的仅是判分函数——从字符串/子句匹配（ESM）或单库 denotation 改为"邻居查询覆盖判据下蒸馏的多库测试套件"逐库 denotation 比对；蕴含链 exact match ⇒ semantic ⇒ test suite ⇒ single denotation；语义等价一般不可判定（Chu 2017）、形式化方法排除理由（sort/float 不可表达）逐字属实；1000 随机库区分 >99% 邻居；套件先于取得模型预测生成（防过拟合设计，作者书面声明）。
2. **CORRECT（read-2 数字校正）｜2.5% vs 2.6%**：read_1 引摘要的 "2.5%" 均值——正文 §6.2 与 Table 1 实为 **2.6%**（摘要疑为旧稿舍入，文内不一致，OPEN）；最坏 8.1% 两处一致。建卡引用以 Table 1 的 0.5/2.6（FP/FN all-data）为准并注明摘要差异。
3. **ACCEPT-BOUNDARY（read-2 新增，重要）｜人工核验是单向的**：100 例人工核验全部抽自"ESM 判错但套件判对"的分歧侧——只验证了套件不产假阳性的一个方向；**套件产假阴性方向未做对称抽验**，依赖"严格 PL 意义下 provably no false negatives"论断，而作者自己给出 broader-sense 反例（随机库违反常识约束致 unnatural 判定）。且已实证 oracle 缺口：WikiSQL 200K 预测中 1 条套件判对但语义不等价（多出的 WHERE 未被覆盖）。
4. **ACCEPT-BOUNDARY（read-2 新增）｜适配后的较松判定**：为与 Spider 官方口径公平比较，常数替换枚举（任一替换通过即判对）会意外放松语义判定（LIKE vs = 案例，作者自认）；官方脚本忽略 join predicate 的 bug 被作者修复后才比较——**文中 FP/FN 率全部是"适配后 ESM vs 套件"的相对量**，且以套件为 ground-truth proxy 的自举结构（read-2 明确点出）。
5. **ACCEPT-NOTE（read-2）**：单库加速消融——从 Ig 采样的**单个**高覆盖随机库在 21 提交上复现全套件结论（高覆盖生成 > 多库集合的贡献分解线索）；数据集级可靠性边界（Advising 63.2%、ATIS 76.3%——多 WHERE 叠加与精确基数谓词是 fuzzing 盲区）；WikiSQL 上作者明确**不推荐**用套件准确率；浮点精度邻居区分困难；成本（16 CPU 一周蒸馏、3.27GB、75.3 分钟）；贪心蒸馏远非最优且无算法对照；EMNLP 2020 归属 PDF 内无自证（波次身份核验时以外部 venue 记录确认，引用沿用，注明来源为外部元数据）；Spider 原始标注错误一处（BETWEEN 区间颠倒）与官方 metric τ=40%（extra 20%）的量化。
6. **AGREE｜核心榜单扭曲证据**："undervalues a high-score submission with 61% semantic accuracy by 8%, but instead favors five other submissions" 逐字核实；偏差随复杂度增大（hard FN 均值 4.4/max 12.1；τ hard 74.1%）。

## Frozen source role

- **准入形态**：**有限准入**（CORPUS_SCOPE 早期论文/定义性祖先条款，2020 年，transfer boundary 显式）。
- **不是什么证据**：不证套件自身两侧误判率——拒绝侧（广义假阴，"非自然库"类）无对称人工审计，误接受（假阳）侧有 1/200K 实证反例；FP/FN 数字是适配后相对量非绝对语义错误率；不外推到 denotation 不可机械判定的载体（solver/优化）；2.5% 摘要数字不引用（用 2.6%）；Advising/ATIS 级数据集不引其可靠性；WikiSQL 场景作者自己弃用。
- 状态：published（EMNLP 2020，归属据外部元数据；PDF 为 arXiv v1）；代码仓库明文在 PDF 内、未访问核验。
- 2026-07-27 追记：按 `w06-audit-c` 处置修正误判方向标签——1/200K WikiSQL 反例属套件**误接受（假阳）**侧（论文自身约定），真正无对称审计的是套件拒绝侧（广义假阴）；严格 PL 意义假阴被 §8 证明不可能。
