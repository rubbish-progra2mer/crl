<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-external-instructor-attribution","card_kind":"failure","paper_id":"P014","evidence_ids":["ev-p014-external-instructor-confound"],"source_refs":[{"path":"papers/P014_instruct_of_reflection.pdf","sha256":"57a01e87496308e3345839c48f085516dd2824ec5aaacf51b71f127c12f42bb7"}]} -->
# External Instructor Confounds Base-Model Self-Improvement Attribution

## Observed failure
[AUTHOR_FACT] IoRT 的所有 backbone 实验都由 GPT-3.5-Turbo-0613 同时担任 meta-thinker 与 instructor。[[evidence:ev-p014-external-instructor-confound]]

## Conditions and scope
[CODEX_SYNTHESIS] 这是归因失败而非“方法无效”：尤其影响弱/开源 backbone 的 intrinsic improvement Claim。

## Failed intervention
[CODEX_SYNTHESIS] 外部异构 GPT-3.5 模型选择和指导候选，changed computation 同时改变模型角色与控制流程。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 提升可能来自动态 gate、meta criteria、更多 calls 或更强 instructor；现有设置不能完全分离。

## Warning for future candidates
[CODEX_SYNTHESIS] 必须报告 selector-only、同模型 instructor 和等调用 baselines，并公开模型身份。

## Possible repair boundary
[CODEX_HYPOTHESIS] 冻结同一 backbone 作生成与判断，或用可验证规则替代强 instructor，可缩窄归因。

## Evidence ledger
[AUTHOR_FACT] `ev-p014-external-instructor-confound` 定位到 PDF p.6 的模型角色。[[evidence:ev-p014-external-instructor-confound]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] stronger-critic confound；external instructor；heterogeneous ensemble；self-improvement attribution；强模型裁判混杂。
