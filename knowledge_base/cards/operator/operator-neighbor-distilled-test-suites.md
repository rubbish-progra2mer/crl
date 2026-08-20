<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-neighbor-distilled-test-suites","card_kind":"operator","paper_id":"P101","evidence_ids":["ev-p101-neighbor-distillation","ev-p101-esm-fn-rate"],"source_refs":[{"path":"papers/P101_distilled_test_suites.pdf","sha256":"50aa8da6bf61c37f4819f45a5db19cafba4721540d14bf97b4ab29a196265d1a"}]} -->
# Neighbor-Distinguishing Distilled Test Suites

## Intervention target
[CODEX_SYNTHESIS] 可执行程序输出的判分函数：从单实例执行比对改为"能区分参考程序全部单点变异邻居"的蒸馏输入集合上的逐输入比对。

## Before and after computation
[AUTHOR_FACT] 对 gold 查询做单点修改生成邻居查询集（换常数/字符串/运算符/列名、删 span）；区分全部邻居要求执行覆盖 gold 的每个被修改部分——即可计算的代码覆盖代理；从大量随机数据库中贪心保留能区分未区分邻居者，得蒸馏测试套件。[[evidence:ev-p101-neighbor-distillation]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：gold 程序 + schema/类型约束的随机实例生成器（混入 gold 中常数及近变体）。输出：小型高覆盖输入集合（Spider：1000 随机库蒸馏、区分 >99% 邻居）。时点：一次性离线预处理；oracle 先于取得模型预测生成（防评测器对被评对象过拟合）。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 邻居 = 最可能的错误程序形态；能区分全部邻居的输入集合以高概率区分其他错误程序——测试充分性从不可判定的语义等价降为可计算的覆盖判据。

## Predicted observable signature
[AUTHOR_FACT] 相对单库/字符串匹配，套件暴露系统性判分误差（ESM FN 2.6%/8.1%，随复杂度增大）。[[evidence:ev-p101-esm-fn-rate]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 三项前提：语义由程序与输入完全决定（denotation 机械可判定）、邻居可机械枚举、实例可自由生成；优化/solver 载体只部分满足。已知盲区包括浮点精度邻居、多 WHERE 叠加和精确基数谓词；套件是紧上界而非等价判定，作者也承认 Goodhart 风险。

## Source lineage
[CODEX_SYNTHESIS] fuzzing/测试覆盖传统（Miller 1963）→ 邻居覆盖蒸馏（本文，EMNLP 2020 定义性祖先）→ P098 探针注入与 P099 四桶测试的共同认识论上游。

## Evidence ledger
[AUTHOR_FACT] 蒸馏目标定义与判分误差量化绑定 exact Passage。[[evidence:ev-p101-neighbor-distillation]] [[evidence:ev-p101-esm-fn-rate]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] neighbor queries; distilled test suite; code coverage proxy; random database fuzzing; greedy distillation; tight upper bound; semantic evaluation; test suite accuracy; distilling a small test suite; distinguishing neighbor programs; single-modification neighbors; random inputs exercising every modified part; approximating semantic equivalence with tests
