# P039 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING_SECONDARY_DIAGNOSTIC`
- Read 1 SHA-256：`c6fc2bbd54af18c7d18d46052a0cc0bda782651f6ebbe1b0c06a3d3691a3cbd4`
- Accepted read-2：`read_2_attempts/r2-20260719-p039-a1/`
- Invocation SHA-256：`e7b7d4dbcb415221e9be507849590e64581be4df942c8c74768dfd9c2d1085bf`
- Report SHA-256：`9f0ebcc0fdf98359d37a64b0a944a5dd9fe9b68a45c46b2207a06427cd7e4e9e`
- 其他 attempts：无；不触发三读，因为本库只将其作为次级新近诊断，不承担核心 Claim/强 baseline。

## Source reconciliation

- `AGREE`：paired tool-required traps/no-tool controls 将 Tool-Skip、Result-Ignore、Fabrication 与 Unnecessary Use 分开；单轮强提示协议不等同开放工具信任。
- `AGREE`：两 judge+规则多数票仍有共模/低流行率问题；parser/chat-template failures 必须与模型行为分开。
- `RESOLVED_BY_SOURCE`：不能声称冲突值来自参数记忆；只记录“成功调用后未服从受控结果”的可观察 Failure。

## Frozen source role

以 `Post-Call Evidence-Faithfulness Decomposition` 与 `Tool Called but Evidence Not Used` 准入；限制为单轮、mock return、强 source-of-truth prompt 与薄弱人工数据验证。

## PLAN_05 Card source-audit disposition

- Audit: `plan05-audit-c/report.md`；SHA-256 `e086a8f797068fcaf3ca2f44227eddb8c289f980f63e1784da0acb832b6a6aa2`；task `/root/plan05_card_source_audit_c`
- Card SHA-256: pre `d4374a67cda9f7969afacfbe64eae7291613e5f63efc53c89f613bac446e0555` → post `ab819f606c8353b8c8f4d6c2fa9fb91a31a9c4339f7aedb01af218de7bb2a606`
- Disposition: `RESOLVED_BY_SOURCE`

补入摘要中 aggregate task accuracy 混淆 tool-skip 与 result-ignore 的直接 Evidence；原 taxonomy Evidence 继续负责四类诊断标签。
