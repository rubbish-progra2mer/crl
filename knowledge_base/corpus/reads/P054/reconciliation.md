# P054 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_DIRECT_FORMALIZER_ANCESTOR`
- Read 1 SHA-256: `dbafca2ee3f9a86c06ee6a1cac2d48451b6f2df28ec61be4dbd641fc1a1a7d31`
- Accepted read-2: `read_2_attempts/r2-20260720-p054-a1/`
- Read-2 invocation SHA-256: `5cff215a24333fb6fbf4befe4d639c412b151fe15ecafd676cfdb011ad45abc5`
- Read-2 report SHA-256: `3328f13bab77aeea049f00d36f06272b66840c69422a024d2d2eea0cfacf18a7`
- Other attempts: none; read-2 did not create a source conflict requiring read-3.

## Source reconciliation

- `AGREE`: 方法把 domain/problem 的自然语言描述转成完整 PDDL domain/problem，再交给 dual-bfws 与 VAL；输入仍提供动作标识和参数，且任务 fully observed。它测试的是 formalization，不是从零发现 action schema。
- `AGREE`: 对若干强模型和较简单域，formalizer 可明显优于直接输出 plan；但优势不跨模型、naturalness 和复杂域稳定成立，DeepSeek/o3 及 Logistics/Barman 等存在反例。
- `AGREE`: naturalness 操作同时改变措辞多样性、显式信息量和常识补全需求，不能把下降单独解释为“语言不自然”。模板化描述也可能接近 PDDL action semantics。
- `AGREE`: baseline 主要是 direct Planner；论文没有 matched-budget iterative/validated planner、独立语义校验器或统一 token/call/time 控制。附录也不足以完整复现实验 formalizer prompt。
- `RESOLVED_BY_SOURCE`: 本文作为完整 PDDL formalizer 的直接祖先、强 baseline 与自然语言显式性边界准入；不另建与 P051/P052 solver-boundary 高度重复的 Operator/Failure Card。
- `UNRESOLVED_NONBLOCKING`: 模型差异、prompt 细节和预算未充分控制，限制“formalizer 普遍优于 planner”的 Claim，但不影响其作为 P053/P055 lineage anchor。

## Frozen source role

P053 higher-order formalizer 与 P055 constraint formalizer 的直接机制祖先。它证明 formalization route 在限定模型与域上可以改变成功率，同时提供重要反证：即使外接 planner+validator，语言显式性、复杂域和模型差异仍决定 formalization 是否可用。

## PLAN_05 Card source audit E disposition

- Auditor task: `/root/plan05_card_source_audit_e`
- Raw report: `knowledge_base/corpus/card_audits/plan05-audit-e/report.md`
- Raw report SHA-256: `82e6b1f26842f02b00c03af621141791b513a82d930b2c3fa01a48086be5b1a2`
- Pre-revision constraint-shift Failure Card SHA-256: `45ebf8d2dc5597a994110169fa59c73578cc345f5781993466b593f658765db1`
- Post-revision constraint-shift Failure Card SHA-256: `c3f80b652ebe2234255041bfe1d6c1dea08511e3ab3aa74a4b55ab80b47c6b37`
- Disposition: `RESOLVED_BY_MAIN_CODEX_ONE_PASS`

处置：P054 的 implicit-`clear` Failure 被独立核源为直接、准确且可定位，保持不变；跨 P054/P055 Failure 的首段和测量 warning 按 auditor 意见收窄，不新增自动判定或审查层。
