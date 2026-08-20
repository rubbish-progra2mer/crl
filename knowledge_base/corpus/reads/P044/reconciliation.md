# P044 Reconciliation

- Disposition：`ACCEPTED_AS_EVALUATION_CARRIER`
- Read 1 SHA-256：`8e18dcb71036cd9e1574274d62aa6993a8c52ceedcfb5577220a99080981da85`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p044-a1/`
- Invocation SHA-256：`1c4cf86910f86771f7a932affcde5aa6eef96a9343964bf18593879aa2feb590`
- Report SHA-256：`e0b18f15c4c8a3a1505f26361b1125cbd05abda2933c7708043acda127b8f10f`

## Source reconciliation

- `AGREE`：changed evaluation 是固定 taxonomy 加任务专属 Expert Guidance，以及 A–F claim 类型化、引用语义回溯与 A–C 网页支撑核验。
- `AGREE`：F 类来源未知主张不被直接事实验证；约 91% evidence coverage 不等于 91% 事实正确。
- `AGREE`：claim gold set 很小且类别不平衡；固定细粒度 rubric 单独使用反而降低人评一致，加入 EG 后才改善；任务预筛排除难由 LLM 评价的题目。

## Admission boundary

作为 rubric/EG 与 claim-level evidence tracing 的评测算子准入。不得把小规模验证升级为完整自动事实裁判，也不以异质系统总分推断单一架构优劣。

