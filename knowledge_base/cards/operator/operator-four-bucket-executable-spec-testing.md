<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-four-bucket-executable-spec-testing","card_kind":"operator","paper_id":"P099","evidence_ids":["ev-p099-two-stage-check","ev-p099-soundness-necessity","ev-p099-judge-miss"],"source_refs":[{"path":"papers/P099_verus_specgym.pdf","sha256":"4865494ceedf3da946cc5970d1815b5b534ac0f6793a50dfdf196dca6ec4560d"}]} -->
# Four-Bucket Executable Specification Testing with Symbolic-then-Runtime Checks

## Intervention target
[CODEX_SYNTHESIS] 规格忠实性的评测计算：从参考比对/LLM 判断改为具体测例上的确定性接受/拒绝判定。

## Before and after computation
[AUTHOR_FACT] 每测例先符号检查（测例作 Verus 断言插入跑验证器；completeness 用 assert(spec)、soundness 用取反断言），失败或超时回退运行时检查（exec_spec 编译为可执行 Rust 比对布尔输出）；全部四桶（{pre,post}×{completeness,soundness}）所有测例通过才判对。[[evidence:ev-p099-two-stage-check]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：候选规格 + 四桶测例（官方测试 + 人写 hacks 经平台裁决路由；字节级 round-trip P(R(t))==t 验收转换）。输出：六类 resolution → 按桶极性映射对/错。时点：评测时，agent 可在可见样例上迭代、隐藏套件终评。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 忠实性拆成四个方向可分别测量的失败面；人类对抗产物（hacks）提供 LLM 难自产的贴身反例；按用途裁剪保证强度（exec_spec_unverified 砍对应性证明）消评测器伪失败。

## Predicted observable signature
[AUTHOR_FACT] soundness 桶加入使 pass@1 大幅下降（77→58 等）；判官对照量化可执行化的净价值（26% 漏检差）。[[evidence:ev-p099-soundness-necessity]] [[evidence:ev-p099-judge-miss]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 前提：规格可编译执行（exec_spec 片段内）、测例可得且有极性标签（平台裁决产物）。四桶判定是有限测例上界近似——全通过≠忠实；模型间 Pass@1 排名含预算/延迟/缓存混杂（$2.5/75min 预算型评测，作者自认）不作能力结论。

## Source lineage
[CODEX_SYNTHESIS] 参考规格线（贵）与 LLM-judge 线（近似）→ 可执行四桶第三路径；与 P101 的蒸馏测试套件同属“用测试逼近语义判定”的方法族。

## Evidence ledger
[AUTHOR_FACT] 两级判定、soundness 必要性、判官对照绑定 exact Passage。[[evidence:ev-p099-two-stage-check]] [[evidence:ev-p099-soundness-necessity]] [[evidence:ev-p099-judge-miss]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] exec_spec; four buckets; pre-condition post-condition; soundness completeness; symbolic check runtime check; Codeforces hacks; round-trip verification; Verus SpecGym; compiling specifications into executable checks; soundness and completeness test buckets; precondition and postcondition testing; adversarial test cases from human hacks; evaluating specs on concrete test cases
