# P099 first read (W06) — P099 Verus-SpecGym：规格忠实性的可执行四桶评测 + LLM-judge 漏检 26%

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization
- Authors: Anmol Agarwal; Natalie Neamtu; Pranjal Aggarwal; Seungone Kim; Jannis Limperg; Cedric Flamant; Kanna Shimizu; Bryan Parno; Sean Welleck（CMU + Amazon，Preprint 自标）
- Identity: arXiv 2605.26457v1 (2026-05-26)，cs.SE；代码 `github.com/formal-verif-is-cool/verus-spec-gym`
- PDF: `knowledge_base/staging/w06_targeted/P099_verus_specgym.pdf`
- PDF SHA-256: `4865494ceedf3da946cc5970d1815b5b534ac0f6793a50dfdf196dca6ec4560d`
- Parse check: 58 physical pages

## Canonical contribution

**规格自动形式化**（informal→formal spec）忠实性的可扩展评测：581 个 Codeforces 衍生任务、目标 Verus（Rust 验证器，Z3 后端）；agent 在含 Verus/bash/文件系统的环境中填 pre_spec/post_spec 谓词并迭代。核心评测创新：(a) 扩展 Verus `exec_spec` 把规格谓词编译为可执行 Rust 检查——**无需专家参考规格也无需 LLM judge**；(b) 四桶测试：pre-completeness（合法输入被接受）/pre-soundness（非法输入被拒）/post-completeness（正确输出被接受）/post-soundness（错误输出被拒）；(c) 测试源 = 官方测例 + **Codeforces "hacks"**（人类竞赛者为击破错误解写的对抗边角例）。

## Evidence and closest lineage

- 主结果：gemini-3.1pro 77.8%；其他前沿 51.1–57.8%；开源仅 21.5–25.5%——**能写对代码的模型常写不出忠实规格**。
- 失败三型：漏输入假设（Spec1 实例：排序数组规格误写严格递增、拒绝含重复的合法输入）、接受错误输出、拒绝正确输出。
- 消融：测试数量/多样性增加使测得成功率稳定下降（**稀疏测试套件系统性高估规格忠实性**）；hacks 暴露官方测例完全漏掉的规格失败（人类对抗输入非冗余）。
- 谱系：verified codegen（Sun/Misu/Aggarwal）、参考规格线（贵）与 LLM-judge 线（近似）之外的第三路径；与 P101 的 distilled test suite 同族（用测试集合逼近语义判定）。

## Measurement and fairness boundaries

- 载体为竞赛题（Codeforces）+ Verus/Rust 单生态；"忠实"由测试桶近似（仍是上界逻辑：测试区分不了的不忠实会漏）；hacks 覆盖依赖题目有 hack 历史；固定算力/时间预算下六模型对比（agent 脚手架同一）。
- exec_spec 扩展本身是工程贡献，其类型/算子覆盖边界（Codeforces 风格约束）划定适用域。

## Draft knowledge objects

### Failure draft: `LLM Judges Miss a Quarter of Specification Faithfulness Failures`

LLM-as-judge 相对可执行评测器漏检 26% 失败；稀疏测试高估忠实性；官方测例漏掉的失败需人类对抗 hacks 才暴露。判官与被评者同为 LLM 时，规格级细错正是共同盲区所在。

### Operator draft: `Executable Specification Testing via exec_spec + Four-Bucket Faithfulness`

把规格谓词编译为可执行检查，在 {pre,post}×{completeness,soundness} 四桶上用官方+对抗测例判忠实性；changed computation = 规格评测从参考比对/LLM 判断改为编译执行。前提 = 规格可编译执行、测例可得；上界语义保留。

## Draft Evidence locators

- Physical pp.1-3: 摘要、Fig.1 环境总览与四桶、贡献清单（26% 数字在摘要与 §1 双现）。
- Physical p.4: Fig.2 四桶测例实例与两种缺陷规格反例。
- 主结果/消融节：模型对比、测试规模消融、hacks 价值、LLM-judge 对照。

All claims remain draft until independent read and reconciliation.
