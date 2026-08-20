# P050 Reconciliation

- Disposition：`ACCEPTED_WITH_NARROWING`
- Read 1 SHA-256：`ef578f66b62042536e2913b1429c8297995c99c71ce949c6db5e826804eb362c`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p050-a1/`
- Invocation SHA-256：`4e878ffdcd389cdd193fd11d6dfb8d065f99709a0a69fdf210571df5a5bd623e`
- Report SHA-256：`8915b18c10c5f4a492c44f65c57a789764e129f4d7ed0a57ffacaab0b24b6d57`

## Source reconciliation

- `AGREE`：changed computation 是对候选程序成对、多轮执行并主动寻找能造成输出分歧的输入，再把这些输入加入一致性投票。
- `AGREE`：分歧证明程序不等价但不标识哪一个正确；LLM 生成 validator 不是形式证明，多数输出也不是真值。
- `AGREE`：512 只匹配测试输入数量，不匹配 token、sandbox calls、wall-clock 或训练预算；训练—测试去重与污染审计未报告。

## Admission boundary

代码/SWE 只作为主动 discriminative counterexample search 的机制载体准入。不得把行为分歧升级为正确性证明，也不得把数量相等称为等计算预算。

