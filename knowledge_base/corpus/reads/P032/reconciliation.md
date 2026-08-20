# P032 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`ddb24ef66434ff69e66a493aef9cce24f9bf51c6a90371d514fb74b5b3312529`
- Accepted read-2：`read_2_attempts/r2-20260719-p032-a1/`
- Invocation SHA-256：`a8c3a21d83c05252e2b37b5401e01ef0060b04fc6ae7db9b5e7c13fefe88cf9d`
- Report SHA-256：`606e408a63e3f5b90236a32fa14479d812a70f78dfcb98ec833ecb4f14ce3327`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：CRITIC 的关键变化是生成后调用任务匹配外部工具，再用工具反馈条件化有限次修正；不是内在自省。
- `AGREE`：无工具变体、自校验与错误分析显示修正非单调，GSM8K 可修复 32.2% 初始错误，也会破坏 4.3% 原正确答案。
- `RESOLVED_BY_SOURCE`：毒性实验 feedback/evaluator 共源，只作测量混杂；QA/数学作为主要机制 Evidence。CRITIC* 依赖正确性 oracle，不进入 deployable Claim。

## Frozen source role

作为 `Externally Grounded Critique-and-Correction` 直接祖先和 `Ungrounded/Wrong Feedback Can Break Correct Output` Failure 准入；所有 Claim 携带任务工具、few-shot prompt、最多 7 工具交互/3 修正及未等预算边界。
