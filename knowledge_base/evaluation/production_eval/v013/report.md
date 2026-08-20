# CRL Contract v3 机器耦合检索维护接受报告

本记录属于机器维护元数据，不是知识库扩建、科研交付或机器 Ready 状态。

- 知识库在维护写入前与实施前冻结基线完全一致：857 个文件、331008320 字节、聚合 SHA-256 `a9c283b71e6b88a549e8cc4ff40bf6a038d9049ed79e833be11cc0f1bea883c8`。
- `pytest -q --run-real-kb --run-real-pdf`：422 passed、6 skipped、0 failed。
- 中央 PDF 解析：99/99 唯一解析并通过论文记录 SHA-256；99 条历史绝对路径均由中央 `papers/` 文件名回退修复，没有改写 KB 记录。
- 五种用途检索均按不同 route plan 返回 Paper、Failure、Operator、Passage 事实并保留来源；检索器不宣称研究空白或自动作科研裁决。
- Recall、Diagnosis、Recorded 与 Tool Forge 的最小机械边界由默认回归覆盖；semantic Recall 仍是 best-effort，不作为发布阻塞。
- `CRL-EVAL-1.0` 首次冻结校准的 12 个 fresh 角色调用全部有效：Weak 10.5000、Medium 52.8750、Strong 96.5000、Unfair 27.1875；Unfair 的 EMP 基线公平与 ADV 泄漏控制均为 0。未根据结果修改 Prompt 或 fixture。

本次接受允许显式重建 `PRODUCTION_RETRIEVAL_LOCK.json`，使其记录当前 retrieval、purpose-aware research retrieval、Cards、Knowledge 和 Vector 代码身份。它不修改论文、PDF、Evidence、Cards、`knowledge.sqlite`、Passage 或 vector index，也不构成正式 Run 启动或科研质量 Gate。
