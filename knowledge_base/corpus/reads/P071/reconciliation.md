# P071 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_PLAN_TEMPLATE_REUSE_AND_FALSE_POSITIVES`
- Read 1 SHA-256: `55b3635d5bf2d59c7ee73972ae9bbff046b734da8ce43d061c39ae8f69b2ef9a`
- Accepted read-2: `read_2_attempts/r2-20260720-p071-a1/`
- Read-2 invocation SHA-256: `4e341ebd217d8d340d6177261e8679a7c0c38008436982c5d1df063f19a374f5`
- Read-2 report SHA-256: `4d7b63f9dc73f2dd251282cff3bad8f99bffb9da47f5ff3369b5c25d3bf04429`
- Other attempts: none; no read-3 required.

## Source reconciliation

- `AGREE`: 从成功 plan 抽取 abstract template，按目标检索并用较小模型适配；changed computation 不等于 answer cache。
- `AGREE`: query semantic cache 出现 false positives，full-history reuse 也较弱，构成真实负向基线。
- `SOURCE_CONFLICT_RETAINED`: 正文称成功/正确轨迹才入库，Algorithm 3 却无条件 cache；正式 Operator 不冻结未解决门控。
- `NARROWED`: 27.28% latency 只来自 FinanceBench 100-query microbenchmark，Table 3 components 与 Total 不闭合；不外推为普遍效率定律。

## Frozen source role

Adaptive plan-template reuse Operator + semantic false-positive Failure；要求后续实验同时报 wrong-hit 和真实 planning cost。
