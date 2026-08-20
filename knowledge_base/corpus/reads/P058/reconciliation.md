# P058 Reconciliation

- Disposition: `ACCEPTED_WITH_NARROWING_MCTS_WORKFLOW_AND_ORACLE_SELECTION_BOUNDARY`
- Read 1 SHA-256: `8bc85d4fa6b07851dffa6f536d01fe927edb078f19da0e6fea2cb01e7cb7dedb`
- Accepted read-2: `read_2_attempts/r2-20260720-p058-a1/`
- Read-2 invocation SHA-256: `7d65996783c835c121b91e0e481be86fdb821d98fdc3e5b97d2a43c2296544e8`
- Read-2 report SHA-256: `cb1f4fc49ab7eb1b629bb6281243bf780f2ee549dff41d625cb6c9b22ddea587`
- Other attempts: none; source conflicts are retained as boundaries rather than resolved by invented settings.

## Source reconciliation

- `AGREE`: AFlow 用 MCTS variant 生成、执行、选择并回传完整 workflow programs。
- `AGREE`: optimizer 反复接触 validation prediction/expected output/error feedback；这是比 aggregate score 更强的信息边界。
- `SOURCE_CONFLICT_RETAINED`: α/λ、early stop、W0 candidate/split 在正文与附录不一致，无法从 PDF 唯一复现；Cards 不固定这些数值。
- `NARROWED`: 不把 AFlow–ADAS 总分差异纯归因于 MCTS；候选次数、tools/oracle access 与预算均需 matched。

## Frozen source role

Executable-workflow MCTS refinement Operator；与 P057 合并形成 reusable-selection-feedback Failure，不单独夸大搜索证据数。
