# P066 Reconciliation

- Disposition: `ACCEPTED_AS_STATEFUL_TOOL_EVALUATION_CARRIER`
- Read 1 SHA-256: `e7cc27c32e497fa81881eadd13c15692a63b53b1fd40d26f07b71e8995152803`
- Accepted read-2: `read_2_attempts/r2-20260720-p066-a1/`
- Read-2 invocation SHA-256: `e8403908480360f391c4c99c9de156b6c280ef871e5873b5b6491b2aa040367b`
- Read-2 report SHA-256: `82f857005efded4a789e8215453a0a816eed4425b804fa8ac4c7e377c7e75aef`
- Other attempts: none; no read-3 required.

## Source reconciliation

- `AGREE`: single-turn function calling 不能代表 memory/stateful/long-horizon competence；multi-turn suite 分解 missing parameter/function 与 long-context state。
- `NARROWED`: BFCL 是 benchmark carrier，不抽成方法 Operator。
- `SOURCE_BOUNDARY`: parallel surplus/duplicate calls、nested value comparison、multi-turn aggregation 和 Web 时间复现未完全规定；正式 claim 必须匹配 evaluator semantics。
- `SOURCE_QUALITY_WARNING`: Figure 10 caption 的 decimal `max` 用词疑似 mean/max 误写，不用于 Card。

## Frozen source role

Stateful tool-use baseline + single-turn-overclaim Failure；为后续 tool Agent implement 提供 claim 边界。
