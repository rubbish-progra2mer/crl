# P101 first read (W06) — P101 Distilled Test Suites：单执行判分掩盖语义错误的定义性祖先（有限准入）

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)
准入形态：**有限准入**（CORPUS_SCOPE §2 早期论文条款：定义性祖先）；transfer boundary 在卡中显式。

## Canonical source and bytes

- Title: Semantic Evaluation for Text-to-SQL with Distilled Test Suites
- Authors: Ruiqi Zhong; Tao Yu; Dan Klein（Berkeley/Yale）
- Identity: arXiv 2010.02840v1 (2020-10-06)；**EMNLP 2020 长文**；代码/测试套件 `github.com/ruiqi-zhong/TestSuiteEval`（11 个 Text-to-SQL 数据集）
- PDF: `knowledge_base/staging/w06_targeted/P101_distilled_test_suites.pdf`
- PDF SHA-256: `50aa8da6bf61c37f4819f45a5db19cafba4721540d14bf97b4ab29a196265d1a`
- Parse check: 16 physical pages

## Canonical contribution

**test suite accuracy**：从大量随机数据库中蒸馏出小型高覆盖测试套件——目标是区分 gold 查询的全部 **neighbor queries**（对 gold 单点修改：换列名/比较符/数值/字符串/删片段），能区分所有邻居的数据库集合即达成对修改点的全覆盖；评测时只在蒸馏套件上比对预测查询与 gold 的 denotation，得到语义准确率的紧上界。蕴含链：exact match ⇒ semantic ⇒ **test suite** ⇒ single denotation。语义等价判定一般不可判定（Chu 2017），形式化方法覆盖不了 sort/float——蒸馏 fuzzing 是无操作约束的可靠近似。

## Evidence and closest lineage

- Spider 套件从 1000 随机库蒸馏，区分 >99% 邻居查询；评测 21 个榜单提交；100 例与官方 ESM 分歧样本人工核验**全部我方正确**。
- 官方 ESM 假阴性率均值 2.5%、最坏 8.1%；ESM 低估一个 61% 语义准确率的高分提交 8%，反而偏好五个更低语义准确率的提交——**榜单排序被判分度量扭曲**；查询越复杂 ESM 偏差越大。
- 单库 denotation 的假阳性 = Fig.1 案例：漏 WHERE 的错误查询在特定库上恰好同 denotation——**"执行通过掩盖语义错误"的教科书定义**。
- 谱系：fuzzing/测试覆盖（Miller 1963、AFL）、K-relations/U-semiring 形式等价线。

## Measurement and fairness boundaries

- test suite accuracy 是**上界**：套件区分不了的错误仍会漏（作者明示 tight upper-bound 而非等价判定）。

## Draft knowledge objects

### Failure draft: `Single-Execution Denotation Check Passes Semantically Wrong Programs`

单库执行比对产生假阳性（漏约束的查询碰巧同 denotation）；字符串匹配产生假阴性（2.5-8.1%）；判分度量的偏差随查询复杂度增大并已实际扭曲榜单排序。

### Operator draft: `Neighbor-Distinguishing Distilled Test Suites`

以"区分 gold 的全部单点变异邻居"为覆盖判据，从随机实例蒸馏紧凑测试套件；changed computation = 判分从单实例 denotation 改为蒸馏套件 denotation 集合。前提 = 语义由程序+输入完全决定、邻居可枚举、实例可自由生成。

## Draft Evidence locators

- Physical pp.1-2: Fig.1 假阳/假阴对照、蕴含链、贡献清单。
- Physical pp.2-3: 问题形式化（式 1-3）与不可判定性引用。
- Physical p.3: 邻居查询五类变异实例。
- Physical §6: 21 提交评测、100 例人工核验、ESM 偏差三发现。

All claims remain draft until independent read and reconciliation.
