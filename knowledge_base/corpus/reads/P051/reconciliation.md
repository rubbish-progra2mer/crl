# P051 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_STRONG_BASELINE`
- Read 1 SHA-256: `8a8586debeff52660e652c9be82c97b0248ea89c1a9a79b81c251cc544d3c5cc`
- Accepted read-2: `read_2_attempts/r2-20260719-p051-a1/`
- Read-2 invocation SHA-256: `b4aa11e66172afb469463384bdea5e306a0d9394fa71f22e032ae428a3bffc9b`
- Read-2 report SHA-256: `04b8a313ddb3e525abb2806efd143137e7519c7df44ac91eab66a7c9e2a47836`
- Accepted read-3: `read_3_attempts/r3-20260720-p051-a1/`
- Read-3 invocation SHA-256: `edb4b1b37657f7884df3c8338bf9ace7f88ce9ac3649272d18644740d8398fa3`
- Read-3 report SHA-256: `2f42c42ce0ae3ffa0c3df424751c3f3eacf8c3220637729f9bcd23bea8df094f`
- Other attempts: none.

## Source reconciliation

- `AGREE`: changed computation 是 `natural-language query → constraint steps → Python/Z3 model → solver search → rendered plan`；三位读者均把核心增量定位于可执行 formalization 与 solver-backed combinatorial search，而不是“solver 直接理解自然语言”。
- `AGREE`: solver soundness/completeness 只覆盖实际编码出的 constraint system；遗漏约束、语义反转、API/索引错误、错误数据库和超时均切断端到端保证。论文没有独立 semantic-equivalence audit。
- `AGREE`: TravelPlanner 同模型结果支持整个 formalization+solver 系统优于 direct planning，但比较没有匹配 LLM calls、tokens、API/tool calls、solver time、prompt length 或人工 task engineering；LLM-Modulo 也没有在同表同预算重跑。
- `AGREE`: `$0.74/query`、约 `245.66s/query` 以及长篇 task-specific examples/prompt tuning 是方法边界，不得把终端用户只给自然语言改写成“无域工程成本”。
- `RESOLVED_BY_SOURCE`: 正式准入只吸收 satisfiable-plan formalization、solver boundary、cost 与 encoding-fidelity Failure。unsat-core/user-feedback interactive repair 属于用户排除的环境反馈/执行恢复方向，只作为论文组成与成本背景，不形成 Operator 或 Gap。
- `UNRESOLVED_NONBLOCKING`: 论文没有逐样本 formalization omission 率、统一 delivery-failure 分解、matched-budget curve 或 Optimize/timeout 的完整语义说明；这些成为 future-use warning，不阻断其作为强 baseline 准入。

## Frozen source role

P004 TravelPlanner 的直接机制后继与 solver-backed formal planning 强基线。它证明“把组合搜索移交形式 solver”可显著改变可行性结果，也同时提供最重要的负向边界：形式保证终止于 LLM 生成的形式化模型。

## PLAN_05 Card source audit D disposition

- Auditor task: `/root/plan05_card_source_audit_d`
- Raw report: `knowledge_base/corpus/card_audits/plan05-audit-d/report.md`
- Raw report SHA-256: `b3bbb7f8815886416d0a48979e29028f4c2070070843ad7411bad2a881e5d657`
- Pre-revision Operator Card SHA-256: `124b3a6745a6ee2400cfe48e89e4b97831e7871f4819c4bd3ad889fc763b1b82`
- Pre-revision Failure Card SHA-256: `8462a8670d338ab1c4e2e1a1e48ff4651063d5b416e0ed27e9bd947ffb545692`
- Post-revision Operator Card SHA-256: `50b53481b4bc4561b457d70b6bb8016c2ba0b63b3ecf36980bb25da36018fe48`
- Post-revision Failure Card SHA-256: `5fc66a92cf67a2fb314c19a596e1c04d0a582de5a0b488ba3d4ff3dbb89f1709`
- Disposition: `RESOLVED_BY_MAIN_CODEX_WITH_ONE_METADATA_LIMITATION`

处置：接受并修正“solver 重复选择”的错误主体归因；从两来源 Operator Card 删除未绑定的 P004 节点；删除 `one-shot` 扩写；把跨论文结论改标 `[CODEX_SYNTHESIS]`；为 P052 五轮上限和 Direct/Code SMT 定义新增全文 Evidence。P051 的三条 Evidence `section` 已改成 PDF 可见小节。派生 Passage 的 section 仍由现有 PDF heading parser 产生，未手工修改 SQLite，也未为这一导航标签重写解析器；PDF 页码、locator、quote、Passage SHA 和正文切片均保持精确。该限制不影响 Card 的事实支撑，但在最终 Corpus Report 披露。
