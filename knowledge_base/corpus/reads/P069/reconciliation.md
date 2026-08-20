# P069 Reconciliation

- Disposition: `ACCEPTED_AS_TOOL_SELECTION_BIAS_NEGATIVE_SOURCE`
- Read 1 SHA-256: `9725bbeb4f25337b446e7d44ebdca2fb8e360b6d82b5c98f93a005884ff39dbf`
- Accepted read-2: `read_2_attempts/r2-20260720-p069-a1/`
- Read-2 invocation SHA-256: `a3bab4b0c8cca3d46fef6fbd5caf342edafe9f2291d9ff7dcfa7ec71df70a591`
- Read-2 report SHA-256: `014d2a0c4ec3c89d68c8ebdc1111c7900678aff336ab7247bcdc96785e5811de`
- Other attempts: none; no read-3 required.

## Source reconciliation

- `AGREE`: 只改 tool description 可造成巨大 usage difference；functionally identical tools 仍有 order bias。
- `NARROWED`: 直接结论是 selection/provider fairness 不稳定，不是任务 correctness、execution result、cost 或 side-effect 的下降。
- `CONFOUND_RETAINED`: combined edit 同时改变长度、cue、示例和信誉；顺序实验未完全排除 name suffix，跨模型均值还受 Qwen family 权重影响。
- `SOURCE_QUALITY_WARNING`: `over 10×`、12.19×/11.22× 与结论 `up to 10×` 措辞不一致；Card 不依赖精确最大倍数。

## Frozen source role

Tool-description/order-bias Failure；不生成未经验证的 mitigation Operator。
