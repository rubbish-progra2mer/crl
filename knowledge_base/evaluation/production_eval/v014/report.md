# CRL v3 最小充分收尾维护接受报告

本记录属于机器维护元数据，不是知识库扩建、科研交付、机器 Ready 状态或新检索框架验收。

- 全量真实回归：`426 passed, 6 skipped, 0 failed`，包含真实知识库与真实 PDF 标记。
- Recall resume 已能从当前版本最近关键研究文件形成恢复查询，复用现有 semantic 索引；无 semantic 时明确降级并继续 FTS。敏感文件排除和输出脱敏不变。
- purpose-aware retrieval 保留原始路线、命中和既有分数，只增加透明噪声标记、机械注意力降权以及按 `paper_id` 去重的紧凑研究地图；没有引入 reranker、模型或科研裁决。
- 真实知识库只读冒烟使用 3 个用途查询，12 条路线均各返回 2 个命中，紧凑地图得到 18 个去重 Paper。
- `crl` CLI 已验证从 Run 的嵌套当前目录发现产品根、Run 根和 `CURRENT_VERSION`；显式参数仍优先。
- 独立知识库审计确认 99 Paper、3995 Passage、224 Evidence、228 Card，SQLite 完整、Card 与向量索引 ready。更新前唯一 ERROR 是本次 `research_retrieval.py` 改动造成的 v013 检索锁身份漂移。
- 知识科学内容平面保持 821 个文件、326477929 字节；关键 Evidence、manifest、数据库、Passage 向量和 Card 索引 SHA-256 与 v013 一致。
- Recorded 沿用现有轻量超时记录，不重构 Formal runner；它不保证清理被测命令自行派生的整个进程树，需要该保证时使用 Formal。

本次接受只允许更新 `knowledge_base/evaluation/` 内 v014 记录、维护审计、当前报告和 `PRODUCTION_RETRIEVAL_LOCK.json`。papers、PDF、Evidence、Cards、`knowledge.sqlite`、Passage、`passages.npz`、`cards_fts.sqlite` 均不得修改。
