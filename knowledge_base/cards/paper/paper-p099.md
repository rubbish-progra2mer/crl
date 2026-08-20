<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p099","card_kind":"paper","paper_id":"P099","evidence_ids":["ev-p099-judge-miss","ev-p099-two-stage-check","ev-p099-soundness-necessity"],"source_refs":[{"path":"papers/P099_verus_specgym.pdf","sha256":"4865494ceedf3da946cc5970d1815b5b534ac0f6793a50dfdf196dca6ec4560d"}]} -->
# Verus-SpecGym: Evaluating Specification Autoformalization

## Role in the knowledge base
[CODEX_SYNTHESIS] LLM 判官漏检 26% 可执行测试可捕获规格错误的大规模外部证据，并提供四桶可执行测试这一评测方法学算子。

## Problem and setting
[CODEX_SYNTHESIS] informal→formal 规格的忠实性无参考评测：581 个 Codeforces 衍生任务、Verus/Rust 生态、agent 交互式填 pre/post 谓词。

## Changed computation
[AUTHOR_FACT] 评测端判定函数：exec_spec 扩展 + 符号优先/执行回退两级流水 + {pre,post}×{completeness,soundness} 四桶（官方测试+人写 hacks）。[[evidence:ev-p099-two-stage-check]]

## Evidence-backed findings
[AUTHOR_FACT] 判官对照：49/191（25.7%）假接受；soundness 桶消融 77→58/82→78/59→51。[[evidence:ev-p099-judge-miss]] [[evidence:ev-p099-soundness-necessity]]
[CODEX_SYNTHESIS] gemini-3.1pro 0.778 最强、开源 0.215-0.255；pass@3=0.756 但 pass3 仅 34.8%（跨尝试脆弱）；过度规格化是独立失败模式；"代码易规格难"对照任务不对等（作者措辞已自限）。

## Limitations and failure signals
[CODEX_SYNTHESIS] 预算型评测混杂（$2.5+75min+延迟/缓存；400 步上限两处表述不一致）——模型排名不作能力结论；判官仅测自评无工具配置；四桶标签为平台产物近似；单文件竞赛域；内部小不一致（均值 21 vs 20；completeness 桶 Max:100 无解释）。

## Lineage and baselines
[CODEX_SYNTHESIS] verified codegen 线之外的第三评测路径；与 P101 同族，均以测试集合逼近语义判定；四桶命名法可迁移到其他可执行规格评测。

## Evidence ledger
[CODEX_SYNTHESIS] 判官漏检、两级判定、soundness 必要性绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] Verus-SpecGym; specification autoformalization; agentic environment; exec_spec; four-bucket faithfulness; LLM judge miss; Codeforces hacks; SWE-agent; evaluating specification autoformalization; executable faithfulness testing; agentic formalization environment
