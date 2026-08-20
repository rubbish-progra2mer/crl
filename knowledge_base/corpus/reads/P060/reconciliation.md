# P060 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_FORMAL_IR_AND_NL_IR_FAILURE`
- Read 1 SHA-256: `de495280695d4103c222e7771cea3ff64fd7c8e633aeae75fb88b51d88bf0e79`
- Accepted read-2: `read_2_attempts/r2-20260720-p060-a1/`
- Read-2 invocation SHA-256: `08987ec22b047569d62cd54cfe63082154c980e69ea8f768a363e4aad1a210b9`
- Read-2 report SHA-256: `28835e05f6483965d4ee4e0315472f4aa30fda9f463a2e3e8e97f6fccbecdd26`
- Other attempts: none; no read-3 needed.

## Source reconciliation

- `AGREE`: LLM 生成 formal IR，symbolic solver 执行；syntax-aligned second IR 与 natural-language IR 的结果方向相反。
- `NARROWED`: 系统已知 action ontology/interface，属于 Spec-to-Code，而不是从环境发现 world model。
- `NARROWED`: 第二阶段仍可见原始描述且调用预算未 matched，故不声称收益只由 IR 信息或 solver 保证产生。
- `SOURCE_QUALITY_WARNING`: 摘要对 baseline 的概括和附录代码排版存在不一致；不影响窄机制/负向结果准入。

## Frozen source role

Formal-IR planning Operator + natural-language-IR Failure；与 P051/P052 formalization fidelity boundary 联动召回。
