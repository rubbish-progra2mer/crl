# P045 Codex 首读：ChromaFlow

- 状态：`REJECT_AFTER_FIRST_READ`
- PDF：`knowledge_base/staging/papers/P045_chromaflow.pdf`
- PDF SHA-256：`9e929a4268f747761edea43e1eeb3373150c687e3deadde59e30de8a21000756`
- 读取范围：全文（12 页）。

## 可用事实

- 单一系统在 GAIA Level-1 53 tasks 上，expanded orchestration 从 29/53 降至 27/53，同时 tracebacks、timeouts、tool-failure mentions 和估计成本上升；后续 strict-provider 为 30/53，但 token-log 成本较高。
- 两个 20-task smoke 为 12/20 与 11/20，作者正确地未把小样本正向信号当 full-set 成功。
- [CODEX_SYNTHESIS] 这可以弱支持“更多编排不等于更强 Agent、负向 ablation 应保留”，但无法支撑通用机制结论。

## 拒绝理由

- 仅一个 proprietary orchestration system、一个 53-task validation split；代码/关键组件未完整公开。
- baseline/recovery/strict-provider 不仅改 orchestration，也改变 provider/policy controls；一任务差异没有统计把握，无法识别具体 causal operator。
- GAIA 含图像/附件任务，超出 CRL 纯文本核心范围；作者自己的 error clusters 也含 document-and-image。
- telemetry 是日志关键词计数，受 logging verbosity 影响；成本不是 provider bill 且漏 VM/search side cost。
- 作为单作者 arXiv case report，其证据强度明显低于 P031/P035/P042 的多系统、受控或同行评审结果。

## 可保留的 Failure note（不建正式 Card）

`Unbounded Orchestration Can Add Execution Entropy`：只作为候选检索时的弱补充来源，不进入二读、正式 Evidence 或独立 Operator。

## 首读裁决

`REJECT_AFTER_FIRST_READ`。不进入 production corpus；拒绝的是证据强度与范围，不是否定负向结果本身。
