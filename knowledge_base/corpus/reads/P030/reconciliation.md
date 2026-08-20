# P030 Reconciliation

- Disposition：`ACCEPT_WITH_NARROWING`
- Read 1 SHA-256：`735e9bf1c05f476808f8bf9190186b0ac89a34cc3e8b1ca652b396d55cf7a4b3`
- Accepted read-2：`read_2_attempts/r2-20260719-p030-a1/`
- Invocation SHA-256：`93ca7b02e4c7a01543a0d23a1d7cf6095be30e1f7dd57f39a47a088eac46d1c2`
- Report SHA-256：`1dd116f74179d0bd99597368396d9a8326523323a35873491acd0a735a1eff62`
- 其他 attempts：无。

## Source reconciliation

- `AGREE`：STALE 用 recognition、premise resistance、policy adaptation 三 probes 区分“知道更新”与“让更新支配决策”；LightMem 新证据已召回仍大量失败是核心负向证据。
- `AGREE`：CUPMEM 将 state adjudication 前移到写入时，并以 typed schema、传播搜索与 constrained readout 约束当前状态；68.0 由复合机制和额外 LLM/cost共同产生。
- `RESOLVED_BY_SOURCE`：正式 Operator 同时保留 evaluation 与 write-side adjudication 两种角色；Failure 为 `Retrieved Update Without Decision Authority`。attention 仅为诊断，不作因果 Evidence。

## Frozen source role

以高优先 Failure/evaluation 及有边界的 memory Operator 准入；必须绑定一次性合成 conflict、固定 schema、约 `$0.37`/instance、judge false negative 和错误 retirement 风险。

## PLAN_05 Card source-audit disposition

- Audits: A `64f4c12681fc74c47cbae98e24f2501c92e3e8f1bb978edcfafc20dbd2f247e9`（task `/root/plan05_card_source_audit_a`）；C `e086a8f797068fcaf3ca2f44227eddb8c289f980f63e1784da0acb832b6a6aa2`（task `/root/plan05_card_source_audit_c`）
- Operator Card SHA-256: pre `13ee316cd43a0939623c8c71c84a3d74e1f1f7467e13d02b8793d853bf4b434b` → post `6762b232c292d40e9296adda607c90906751b25b3ee0ffd2903abe67ecef8f01`
- Failure Card SHA-256: pre `e4aae555e5a7e7a3fd37cca1d0920e9f36e0169ad0459a962208e75e8c22498d` → post `1a663588481e6a0cd9b8d12fbf31b19f23e667d4fc081c2011458fc4a4ff4212`
- Disposition: `RESOLVED_BY_SOURCE`

Operator 补入 write-side adjudication 与 authorized-state readout 的直接 Evidence；Failure 补入 SR 76% 对 IPA 39% 等实测差距，不再由定义性片段单独支撑结果主张。
