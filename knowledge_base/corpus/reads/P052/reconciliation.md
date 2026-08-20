# P052 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_DIRECT_REFINEMENT`
- Read 1 SHA-256: `0233da043a2acef93dfe3f618f7c614ccd6fbd99790f84dd610594fb13800f36`
- Accepted read-2: `read_2_attempts/r2-20260719-p052-a1/`
- Read-2 invocation SHA-256: `7b640e7660f519821046c7076159cd44426d4656eb1f4007dad9867816ac31d2`
- Read-2 report SHA-256: `1cde5290a17ddd4985f4226d3d1bfbb66114a890461658a77c2345ba4eb3b1e0`
- Accepted read-3: `read_3_attempts/r3-20260720-p052-a1/`
- Read-3 invocation SHA-256: `054ffc41e9b36026b488fa00c9134cafd87823ec3638a8a4711ff59000418441`
- Read-3 report SHA-256: `2d1c48a2996ad1bbe7c956ea1a6aaf6ac056ec9ff27473cfbe1076751a0330bd`
- Other attempts: none.

## Source reconciliation

- `AGREE`: P052 保留 P051 的“LLM formalization + external solver”核心，把 task-specific query/code demonstrations 改成 Definer、两类 Formulator schema、固定跨任务 examples、zero-example Code Generator 与 bounded Self Assess/Modification。
- `AGREE`: `zero-shot/task-agnostic` 只表示九个测试任务没有 task-specific examples；系统仍需要详细 task description、背景/API、output format、single-step/multi-step 路由、固定结构相近 examples 与少量 model-specific prompt editing。
- `AGREE`: No-Self-Assessment ablation 支持完整“自评+最多五轮重建/求解预算”的净效果，不隔离 same-model diagnosis 本身。Gripper 非终止循环与 Coffee formatter 矛盾后仍全通过直接反驳“自评即独立验证”。
- `AGREE`: 主表匹配了输入和基础模型，但没有匹配 call/token/dollar/wall-time/solver budget。GPT-4o LLMFP 相对 Direct/Code-SMT 有显著额外成本与时延，因此只能视为系统级效果—成本点。
- `AGREE`: solver guarantee 仍只覆盖正确编码；implicit constraint omission、API overwrite、closed-world false 初始化遗漏、ambiguous-query inversion 与 timeout 是真实 Failure。
- `RESOLVED_BY_SOURCE`: 正式机制抽取为“decomposed formalized planning”，Self Assess 只作为 bounded supporting component，不升级为独立 verifier 或自动正确性证明；不把任务载体中的执行恢复扩展成用户排除的研究方向。
- `UNRESOLVED_NONBLOCKING`: 没有 zero-example removal、matched-call resampling、independent critic、self-assessor confusion matrix 或未整理真实用户任务实验；这些限制其泛化 Claim，但不阻断其作为 P051 的直接 refinement 准入。

## Frozen source role

P051 的直接泛化后继：把专用 formalization demonstrations 抽象成跨任务 schema，并同时暴露通用化的真实剩余成本。与 P051 共同定义 planning 簇的强 baseline、closest composition 和 formalization-fidelity Failure；不是“planning anything without domain engineering”的证明。

## PLAN_05 Card source audit D disposition

- Auditor task: `/root/plan05_card_source_audit_d`
- Raw report: `knowledge_base/corpus/card_audits/plan05-audit-d/report.md`
- Raw report SHA-256: `b3bbb7f8815886416d0a48979e29028f4c2070070843ad7411bad2a881e5d657`
- Pre-revision Operator Card SHA-256: `124b3a6745a6ee2400cfe48e89e4b97831e7871f4819c4bd3ad889fc763b1b82`
- Pre-revision Failure Card SHA-256: `8462a8670d338ab1c4e2e1a1e48ff4651063d5b416e0ed27e9bd947ffb545692`
- Post-revision Operator Card SHA-256: `50b53481b4bc4561b457d70b6bb8016c2ba0b63b3ecf36980bb25da36018fe48`
- Post-revision Failure Card SHA-256: `5fc66a92cf67a2fb314c19a596e1c04d0a582de5a0b488ba3d4ff3dbb89f1709`
- Disposition: `RESOLVED_BY_MAIN_CODEX_WITH_ONE_METADATA_LIMITATION`

处置：新增 `ev-p052-self-assessment-loop-limit` 与 `ev-p052-direct-code-smt-baselines`，把同模型修改明确限制为最多五轮，并以论文原名 `Direct`、`Code SMT` 表述；没有把相同输入偷换成 matched call/token/time budget。跨论文 ledger 改标 `[CODEX_SYNTHESIS]`。两条附录 Failure Evidence 的 `section` 已改成 PDF 可见 A.6.1/A.6.9；派生 Passage section 仍保留当前 parser 的过粗标题，未直接编辑可重建 SQLite，也未为了导航标签扩张 PDF parser。精确 PDF 页、locator、quote、Passage SHA 与字符区间均通过。
