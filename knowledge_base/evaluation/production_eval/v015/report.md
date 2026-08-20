# Retrieval Lock 有界收尾接受报告

本记录只接受当前机器与外置知识库之间的检索维护身份，不是新的盲测体系、科研质量评分或 CRL 启动/交付门。

- 重建前只读审计：99 Paper、3995 Passage、224 Evidence、228 Card；唯一 ERROR 是 `research_retrieval.py` 从锁定的 `09caf4...` 漂移到当前 `8662e98...`。其余锁定源码、Card source signature、Evidence、数据库和索引身份均匹配。
- 冻结回放：复用 v012 的 20 条 calibration 与 18 条 blind 查询及既有直接阅读判断，不改 query、label 或参数。关键查询 13/13 通过，相关 top-5 Card 到当前 Evidence/Passage 的链路失败为 0。
- 普通查询边界：calibration 为 20/20，blind 为 16/18；相对 v012 新增普通 miss `v012-blind-q02`，相关 Operator 当前位于第 13、19、55 名。38 条 top-10 排序均不与 v012 完全相同。当前 Card 代码和 Card FTS 索引与已接受 v014 锁完全一致，因此这是 v012→v014 已存在的排序差异，不是本次 `research_retrieval.py` 漂移引入的新 ranking 变化；本记录不声称 exact replay equivalence。
- 当前五用途真实知识库冒烟：problem/failure/operator/prior/measurement 共 20 条路线全部非空；物化 `result.json` 保留 60 条原始 route hits、rank、score 与来源定位，紧凑地图可从原始路线精确重算，且不产生自动科研判断。同进程两次接受复跑均为 0 条降级路线。
- 一次更早的独立进程首条 Passage route 因 Hugging Face 客户端 RuntimeError 明确降级，但 FTS fallback 仍返回 3 条命中；后续与两次接受复跑恢复正常。该事实作为可选向量能力限制保留。
- Python 3.11 全量真实回归：`465 passed, 6 skipped, 0 failed`，命令包含 `--run-real-kb --run-real-pdf`。
- 排除 `evaluation/` 与未触碰的非科学打包文件 `evaluation.zip` 后，科学内容平面仍为 821 文件、326477929 字节；关键 Evidence、manifest、数据库、Passage vector、Card FTS 与 Card source signature 均与 v014 一致。没有重建或修改任何论文、PDF、Card、Evidence、Passage、数据库或索引。
- 不重新设计 blind query/judgment：当前漂移只涉及已知的 purpose-aware 导航/呈现源身份，底层检索、Card 与索引身份未变，冻结关键查询没有新增阻断失败。

上述证据允许使用现有维护工具把 `PRODUCTION_RETRIEVAL_LOCK.json` 显式更新到 v015。锁仍只是可审计维护元数据。
