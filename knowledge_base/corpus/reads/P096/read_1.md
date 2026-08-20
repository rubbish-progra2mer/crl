# P096 first read (W06) — P096 VeriSimpl：solver 生成简化诊断查询 + LLM 裁决的形式化验证

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: VeriSimpl: Robust Optimization Modeling from Natural Language using Simplification-based Verification
- Authors: Sumaya Abdul Rahman; Seckhen Ariel Andrade Cuellar; Ghani Raissov; Mohammad Raza（Texas A&M Qatar / CMU Qatar / QCRI）
- Identity: arXiv 2607.20474v1（abs 页提交日 2026-05-24；**ICML 2026 正式发表**——正文页脚 "Proceedings of the 43rd ICML, Seoul, PMLR 306, 2026"；编号 2607 与 5 月提交日的表观异常此前已核验页面自洽）
- PDF: `knowledge_base/staging/w06_targeted/P096_verisimpl.pdf`
- PDF SHA-256: `81b34a7084aa5552ef9a1491ec5e5f9da5c149e80beb06fe81fc163ae4d595b3`
- Parse check: 33 physical pages

## Canonical contribution

**Simplification-based verification**：倒转"LLM 出测试、solver 执行"的常规——由 solver 从候选程序生成降维诊断查询、LLM 只在具体数值上做局部推理，二者一致性作为验证信号，用于 best-of-K（K≤10）候选选择。三路信号：(1) **约束变异可行性查询**（每约束按 <
/=/> 三型变异，solver 造 witness 赋值，LLM 判断该赋值在 NL 描述下是否可行，Algorithm 2）；(2) **变量掩蔽估值查询**（solver 先解出最优赋值，固定其余变量、让 LLM 推被掩蔽变量，单变量掩蔽 + 全变量掩蔽两档，Algorithm 3）；(3) 类型一致性检查。词典序聚合选最高分候选执行。

## Evidence and closest lineage

- 主结果（Table 1/2）：四基准（NL4Opt 269 / NLP4LP 67 / CompOR / IndOR 100）上，GPT-4o 底座平均 65.5 vs SelfDebug 59.1 / OptiMUS 48.4 / 直接 56.8；R1 底座平均 72.8。增益跨两家底座一致（+Mistral 附录 C）。
- **自验证信号**（Table 3）：全部检查通过的子集 precision GPT-4o 平均 91.5%（CompOR 100%），coverage 仅 34.2%（R1 78.5/23.0）——高精度低覆盖的置信指示器。
- 消融（Table 4）：无单一信号足够；A-CONS（仅约束）precision 掉到 75.7；A-FULLVAR 覆盖最低（端到端目标推理对 LLM 太难）。
- 谱系：OptiMUS/CoE agentic 线、LLMOpt 微调线、mutation testing（DeMillo 1978 被引）、property-based testing。

## Measurement and fairness boundaries

- 验证裁决者是 **LLM 推理**（对 solver witness 的可行性/估值判断）——无参考检查器基准真值；"验证通过"=LLM 与 solver 输出一致，非与规格真值一致（共享误解案例正是此软肋的实证）。
- 准确率的评判口径（与 gold 解比对方式）在正文未详述（附录）；无显著性区间；K=10 采样与验证查询数的计算成本未与基线配平（best-of-K 本身含采样预算优势）。

## Draft knowledge objects

### Operator draft: `Solver-Generated Simplification Queries with LLM Adjudication`

对候选形式化做约束三型变异与变量掩蔽，由 solver 构造具体 witness/最优赋值，LLM 在降维具体值上做局部一致性推理；聚合为 best-of-K 选择信号 + 高精度自验证标志。前提 = LLM 对 NL 的解读独立于生成侧错误（共享误解时失效）；无外部真值时 soundness 不封闭。

### Failure draft: `Verification by Generator-Aligned Reasoning Passes Shared Misinterpretations`

当形式化误差源于对 NL 的系统性误读（变量语义、漏计成本项）时，LLM 裁决与 solver 输出一致地错，验证信号满分通过；完全遗漏的 NL 方面不产生任何查询。自验证 precision 91.5% 的补集里藏着这类结构性假阴影响。

## Draft Evidence locators

- Physical pp.1-3: 问题设定、Fig.1 正误对照实例、simplification 流程与两维简化。
- Physical pp.4-5: Algorithm 1/2/3 与查询定义。
- Physical p.6: Table 1/2/3 主结果与自验证 precision/coverage。
- Physical p.7: Table 4 消融。
- Physical p.8: §4.4 共享误解失败案例与两点未覆盖自认。

All claims remain draft until independent read and reconciliation.
