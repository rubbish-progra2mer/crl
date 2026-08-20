# P029 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`1020c39441b50043cb19e670d920746b538906dee8f405dc62b584aa5279e13c`
- Accepted read-2：`read_2_attempts/r2-20260719-p029-a1/`
- Invocation SHA-256：`be82064b4923ace3727ac381eb244032f57799e6230cc09d62d7edf7ebde49cb`
- Report SHA-256：`d75b09a32d66e959f1d6c8a9017b26d3e4e602dc113917b2cd08e59b089b2e18`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：MemFail 通过 source/store/retrieval/answer 全局视图将错误按 summarization、storage、retrieval、reasoning 生命周期定位；不是新 memory architecture。
- `AGREE`：合成五任务/四显式系统显示 architecture-specific failure profile；增大 k 或换更强模型不是统一修复。
- `RESOLVED_BY_SOURCE`：judge 的 oracle view 只允许离线诊断；“忠实保存用户断言”不等于现实事实正确，相关 storage label 必须携带语义边界。

## Frozen source role

以 Failure taxonomy 和条件归因 Operator 准入，优先于 Paper summary；不得外推真实部署发生率、参数化记忆或在线 detector 能力。
