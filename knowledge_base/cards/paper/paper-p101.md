<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p101","card_kind":"paper","paper_id":"P101","evidence_ids":["ev-p101-metric-distortion","ev-p101-neighbor-distillation","ev-p101-esm-fn-rate"],"source_refs":[{"path":"papers/P101_distilled_test_suites.pdf","sha256":"50aa8da6bf61c37f4819f45a5db19cafba4721540d14bf97b4ab29a196265d1a"}]} -->
# Semantic Evaluation for Text-to-SQL with Distilled Test Suites

## Role in the knowledge base
[CODEX_SYNTHESIS] **有限准入**（CORPUS_SCOPE 早期论文/定义性祖先条款）：“执行通过掩盖语义错误”这一失败类型的认识论祖先；迁移边界显式记录于卡内。

## Problem and setting
[CODEX_SYNTHESIS] Text-to-SQL 判分：语义等价一般不可判定（Chu 2017），字符串匹配假阴、单库执行假阳；形式化方法覆盖不了 sort/float。

## Changed computation
[AUTHOR_FACT] 判分函数改为蒸馏测试套件上的逐库 denotation 比对；蕴含链 exact match ⇒ semantic ⇒ test suite ⇒ single denotation。[[evidence:ev-p101-neighbor-distillation]]

## Evidence-backed findings
[AUTHOR_FACT] ESM FN 2.6%均值/8.1%最坏且随复杂度增大；榜单排序被实际扭曲（61% 提交被低估 8%）。[[evidence:ev-p101-esm-fn-rate]] [[evidence:ev-p101-metric-distortion]]
[CODEX_SYNTHESIS] 1000 随机库区分 >99% 邻居；单个高覆盖随机库在 21 提交上复现全套件结论（高覆盖生成>多库集合的贡献线索）。

## Limitations and failure signals
[CODEX_SYNTHESIS] 人工审计单向（只验分歧侧假阳方向）；套件误接受（假阳）方向在 WikiSQL 约 200K 预测中有 1 例实证反例；FP/FN 是适配后相对量（常数替换枚举放松判定）；数据集级可靠边界（Advising 63.2%/ATIS 76.3%）；WikiSQL 作者自己不推荐；摘要 2.5% vs 正文 2.6% 不一致（引用用 2.6%）。

## Lineage and baselines
[CODEX_SYNTHESIS] fuzzing 传统→本文→P098（探针注入训练信号）/P099（四桶可执行测试）的共同上游；三项前提在 solver 载体上只部分成立。

## Evidence ledger
[CODEX_SYNTHESIS] 蒸馏定义、FN 量化、榜单扭曲绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] distilled test suites; test suite accuracy; neighbor queries; Spider evaluation; exact set match; single denotation; EMNLP 2020; semantic evaluation ancestor; semantic evaluation with test suites; test suite accuracy; neighbor-query coverage
