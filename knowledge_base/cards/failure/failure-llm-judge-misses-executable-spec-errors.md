<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-llm-judge-misses-executable-spec-errors","card_kind":"failure","paper_id":"P099","evidence_ids":["ev-p099-judge-miss","ev-p099-soundness-necessity"],"source_refs":[{"path":"papers/P099_verus_specgym.pdf","sha256":"4865494ceedf3da946cc5970d1815b5b534ac0f6793a50dfdf196dca6ec4560d"}]} -->
# LLM Judge Misses a Quarter of Executable-Testcase-Caught Specification Errors

## Observed failure
[AUTHOR_FACT] gpt5.3-codex 判官评审自己生成的规格时，把 191 个"可执行测例有具体反例"的错误规格中的 49 个（25.7%）判为正确——无执行的 LLM 判断漏掉可执行测试能抓的错。[[evidence:ev-p099-judge-miss]]
[AUTHOR_FACT] 方向缺失同病：只用 completeness 测例评测时 pass@1 系统性虚高（77→58 / 82→78 / 59→51 当加入 soundness 测例）——规格可以接受全部合法样例同时也接受非法输入。[[evidence:ev-p099-soundness-necessity]]

## Conditions and scope
[CODEX_SYNTHESIS] Verus-SpecGym：581 个 Codeforces 衍生规格自动形式化任务；判官为静态一次性自评、无执行工具（不排除跨模型/带工具/投票判官缩小差距——这些配置未测）；四桶标签是平台产物近似。

## Failed intervention
[CODEX_SYNTHESIS] 以 LLM 判断替代可执行测试作为规格忠实性度量；以稀疏（completeness-only）测试套件近似语义判定。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] "测例条数越多越暴露"不成立——F.8 回溯子抽样显示小预算已近饱和；高估的主轴是方向缺失（漏 soundness 桶）而非条数。26% 的分母是 compile-clean 错误规格（54 个不编译者被排除）。

## Warning for future candidates
[CODEX_SYNTHESIS] LLM 判官漏检规格级错误的大规模外部证据；任何以 LLM 审读替代执行验证的候选方法都必须面对该测量。评测协议应同时覆盖 completeness 与 soundness。

## Possible repair boundary
[CODEX_HYPOTHESIS] 可执行化（exec_spec 类编译）与人类对抗测例（hacks）是已有修复路线；四桶命名法（pre/post × sound/complete）可迁移到野生管线评测。

## Evidence ledger
[CODEX_SYNTHESIS] 判官漏检与 soundness 消融绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] LLM-as-judge miss rate; 49 of 191; specification faithfulness; soundness testcases; completeness-only overestimate; executable evaluation; self-judge blind spot; LLM judge marks incorrect specifications correct; judges missing concrete counterexamples; executable tests beat LLM judgment; misjudging specification faithfulness
