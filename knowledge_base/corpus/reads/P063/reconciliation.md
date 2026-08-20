# P063 Reconciliation

- Disposition: `ACCEPTED_WITH_STRONG_NARROWING_LINK_AND_REWRITE_ONLY`
- Read 1 SHA-256: `c047a8482bf578f2ec462c739096620cc3dff7b0229be0c125a004714a372787`
- Accepted read-2: `read_2_attempts/r2-20260720-p063-a1/`
- Read-2 invocation SHA-256: `032b4442f28a5848c5914bc4cf9e28e423f5f92bbbbd43f2c69b3faa2339b947`
- Read-2 report SHA-256: `650f736eeda6f79fa6b7e0c3dbca6da1257b3a943ac9ea462843949e6fd82b66`
- Other attempts: none; internal omissions are preserved rather than guessed.

## Source reconciliation

- `AGREE`: new note 触发 neighbor retrieval、LLM link decision，并允许更新 neighbor context/tags。
- `SOURCE_CONFLICT_RETAINED`: link schema/direction、Eq. 6 下标、rewrite field preservation、re-embedding/reindex、link traversal 与 action names 均未形成可唯一复现的闭环。
- `NARROWED`: Operator 只冻结“dynamic link generation + authorized neighbor rewrite”这一作者可见计算；不写入未说明 graph runtime。
- `NEGATIVE_PRIORITY`: mutable memory 无 version/source-span/rollback provenance，且 k/cost/storage 口径有不一致；作为 transfer risk，而非捏造已观察的通用 performance failure。

## Frozen source role

Write-time linked-memory evolution 的受限 Operator；重要价值在于提醒 CRL：可变 memory 若无 provenance，后续 evidence 无法审计。
