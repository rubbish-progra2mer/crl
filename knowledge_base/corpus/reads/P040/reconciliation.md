# P040 Reconciliation

- Disposition：`ACCEPTED_WITH_NARROWING`
- Read 1 SHA-256：`d2a92516ad6c78c77dbed386ebff769d9028d4efea974c585fb323b5765d0b97`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p040-a1/`
- Invocation SHA-256：`deb3a068e7b78c6a142c007a4776c26e68dad7c156a30ca1291d7f9f2df2c02d`
- Report SHA-256：`cbb43c50cc39001abf5ceb71d6bffe343651dda579e35017c262587ca41202e7`

## Source reconciliation

- `AGREE`：论文研究执行后的 false-success 检测，而非动作前安全控制；结构化环境状态是 ground truth，轻量文本分类器明显优于多种 LLM judge。
- `AGREE`：AppWorld 结果只覆盖显式自评子集；跨域/跨时间迁移及对抗改写均退化，10% 告警点的 precision 不足以支持自动封禁。
- `UNRESOLVED_NONBLOCKING`：生产先验漂移、跨语言和恶意规避未测。

## Admission boundary

作为 false-success measurement Failure 与低成本域内风险分流证据准入。不得写成通用因果检测器、动作前安全保证或跨域稳定方案。

