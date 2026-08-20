# P038 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`8b918cc4a6fd8ebf11ebb8341f29de37458f54ee3eeadc53735d60f267dcf3b9`
- Accepted read-2：`read_2_attempts/r2-20260719-p038-a1/`
- Invocation SHA-256：`2dd0c3d0b5467d2527d52e479255825ee447240404424337da9c0cd1578899e9`
- Report SHA-256：`ec70b0f19b1b76f5db46f952ea2ae6e834acb22d930d9fb457cb1deabcb9dabe`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：AgentDojo 用确定性 state functions 联合测 benign utility、utility-under-attack 与 targeted ASR；攻击位于真实 tool-returned untrusted data。
- `AGREE`：tool filter 在接触不可信内容前缩小 action set；GPT-4o 主表下 ASR 显著下降且 utility 保持，但约 17% shared-tool cases 与动态工具选择构成硬边界。
- `RESOLVED_BY_SOURCE`：正式数值采用二读核对的表 5（无防御 69.0/50.01/57.69，filter 73.13/56.28/6.84）；跨模型 prompt/interface 不作纯安全能力排名。

## Frozen source role

以 `Pre-Exposure Tool-Authority Minimization` 与 `Security Gain by Utility Collapse` 准入；只支持指定 2024 默认攻击，不支持自适应攻击通用安全。
