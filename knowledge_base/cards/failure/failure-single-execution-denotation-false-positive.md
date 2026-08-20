<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-single-execution-denotation-false-positive","card_kind":"failure","paper_id":"P101","evidence_ids":["ev-p101-metric-distortion","ev-p101-esm-fn-rate"],"source_refs":[{"path":"papers/P101_distilled_test_suites.pdf","sha256":"50aa8da6bf61c37f4819f45a5db19cafba4721540d14bf97b4ab29a196265d1a"}]} -->
# Single-Execution Denotation Checks Pass Semantically Wrong Programs

## Observed failure
[AUTHOR_FACT] 判分度量双向失真并已实际扭曲榜单：ESM 低估一个 61% 语义准确率的高分提交 8%、反而偏好五个更低语义准确率的提交；复杂查询上偏差更大。[[evidence:ev-p101-metric-distortion]]
[AUTHOR_FACT] ESM 假阴性率均值 2.6%、最坏 8.1%（hard 段 4%/12.1%）；单库 denotation 侧的假阳性是 Fig.1 教科书案例——漏 WHERE 的错误查询在特定库上恰好同 denotation。[[evidence:ev-p101-esm-fn-rate]]

## Conditions and scope
[CODEX_SYNTHESIS] Text-to-SQL（Spider 21 榜单提交 + 11 数据集）；EMNLP 2020（有限准入：定义性祖先，2020 年，transfer boundary 显式）。注意摘要写 2.5% 而 Table 1/正文为 2.6%（文内不一致，引用用 2.6%）。

## Failed intervention
[CODEX_SYNTHESIS] 以单一数据库执行结果比对（或字符串/子句匹配）作为程序语义正确性的判分函数。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 审计单向性（reconciliation）：100 例人工核验全部抽自 ESM-套件分歧侧，只验证套件不产假阳性的一个方向；套件拒绝侧（广义假阴，"非自然库"类）无对称抽验；套件误接受（假阳）侧在 WikiSQL 约 200K 预测中有 1 例实证反例（多余 WHERE 未被覆盖）；FP/FN 数字是"适配后 ESM vs 套件"的相对量（常数替换枚举放松了判定）。

## Warning for future candidates
[CODEX_SYNTHESIS] “执行通过=语义正确”在任何单点执行检查上均不可辩护；多 WHERE 叠加与精确基数谓词是随机 fuzzing 盲区（Advising 可靠比例仅 63.2%）。

## Possible repair boundary
[CODEX_HYPOTHESIS] 邻居覆盖蒸馏套件的前提是 denotation 可机械判定、邻居可枚举且实例可自由生成；solver/优化载体只部分满足这三项前提，独立参考检查器可能补充“套件自身无对称审计”的结构弱点。

## Evidence ledger
[CODEX_SYNTHESIS] 榜单扭曲与 FN 量化绑定 exact Passage；单向审计边界记录于 reconciliation。

## Retrieval vocabulary
[CODEX_SYNTHESIS] single denotation; exact set match; false positive execution; test suite accuracy; leaderboard distortion; masked by execution; semantic accuracy; Spider; execution passes a semantically wrong program; coincidentally equal outputs; single test database false positives; string match false negatives; scoring metric distorts the leaderboard
