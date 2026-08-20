# PLAN_05 Card 来源审计 H 调用快照

## 身份与目的

- 审计上下文：fresh subagent `plan05_a3_card_source_audit`。
- 审计类型：新增正式 Card 的独立来源忠实性检查；不是 Candidate 三审 Reviewer，也不作科研 Candidate 裁决。
- 创建时 Evidence snapshot SHA-256：`8e7ac0d963e8144fc5ad1928fe8cb8ecd09591bf17cbbd7fc01fbe851453cf7c`。

## 唯一审计对象

Operator：

- `cards/operator/operator-hierarchical-utterance-critic-token-actor.md`
- `cards/operator/operator-validated-specialized-tool-creation-retrieval.md`
- `cards/operator/operator-action-preserving-observation-contextualization.md`
- `cards/operator/operator-gold-supervised-hindsight-search-depth.md`
- `cards/operator/operator-fixed-budget-independent-path-aggregation.md`
- `cards/operator/operator-future-token-loss-filtered-tool-learning.md`

Failure：

- `cards/failure/failure-token-local-credit-misses-turn-level-delayed-value.md`
- `cards/failure/failure-generic-or-unvalidated-tool-libraries-add-distractors.md`
- `cards/failure/failure-raw-observation-overload-hides-action-relevant-ui.md`
- `cards/failure/failure-fixed-search-depth-causes-under-and-over-search.md`
- `cards/failure/failure-interactive-gains-collapse-against-independent-sampling.md`
- `cards/failure/failure-likelihood-utility-does-not-guarantee-agent-utility.md`
- `cards/failure/failure-multi-agent-adversarial-coordination-spans-trust-surfaces.md`

## 可见与不可见范围

审计员可读取上述 Card 明示 Evidence、对应 SQLite passages、PDF 与 read/reconciliation。不得读取既往 source-audit report、Candidate、Commissioning 或科研 Reviewer 文件。逐项核对 `[AUTHOR_FACT]` / `[AUTHOR_INTERPRETATION]` 的原文支持，并检查 Codex 综合是否夸大 oracle、cost、baseline、scope 或 transfer。

审计员只向主 Codex返回原始报告文本，不直接修改 Card。主 Codex将原文落盘并逐项处置；报告必须先于 disposition 固定。
