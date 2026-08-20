# P046 Reconciliation

- Disposition：`ACCEPTED_WITH_NARROWING`
- Read 1 SHA-256：`4a1033f446a490b1b84edbf95e7af44d79a3dfcf9b3dadb3d387ee395efa5462`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p046-a1/`
- Invocation SHA-256：`1f89ca300bf8084627e82ae5d173abaf7e595b0ef31955e726547410a8d0876f`
- Report SHA-256：`71761aeb3dab47cf65d036003f68503a0f7968ffa71cc9164fe86c995460ba07`

## Source reconciliation

- `AGREE`：changed computation 是在 planned tool call 与执行之间插入 SMT satisfiability guard，SAT 放行、UNSAT 用最小冲突核驱动有限重规划。
- `AGREE`：保证仅相对于人工审核的 policy encoding 与 LLM 状态抽取；自动自然语言形式化多次产生语法错误、遗漏或欠约束。
- `AGREE`：实验只覆盖 tau2 airline 50 题，增加 GPT-4o、Z3 与最多三次重规划；precision/pass 提升伴随 recall 下降。
- `UNRESOLVED_NONBLOCKING`：最终 policy artifact 经 benchmark-guided 人工调优且无独立 holdout，存在测试适配风险。

## Admission boundary

准入单域、人工形式化条件下的 pre-execution guard Operator；自动政策翻译失败、recall 代价与虚假安全感作为更高优先负向知识。不得称端到端政策安全证明。

