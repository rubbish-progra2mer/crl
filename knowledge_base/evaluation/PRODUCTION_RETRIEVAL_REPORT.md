# 当前论文知识检索维护报告

当前身份：`v015_retrieval_lock_bounded_closeout_acceptance`

本报告只说明当前真实知识库与机器耦合检索身份已经完成有界维护收口；它不是新盲测体系、科研质量评分、CRL 启动门或 Delivery Gate。

- 重建前唯一锁 ERROR 是 `research_retrieval.py` 源身份从 `09caf4...` 漂移到 `8662e98...`；底层 retrieval、Cards、Knowledge、Vector 源码以及全部锁定科学资产与索引身份仍匹配 v014。
- 复用 v012 冻结材料回放 38 条查询：关键查询 13/13 通过，Card→Evidence→Passage 链路失败为 0。普通 blind 为 16/18，相对 v012 新增 `v012-blind-q02` miss；38 条 top-10 不完全等价。该差异已明确保留，不冒充 exact replay equivalence，也不机械升级为新 Gate。
- 当前真实 KB 五用途冒烟覆盖 problem、failure、operator、prior、measurement 共 20 条路线；全部非空，原始 route hits、rank、score 与来源保持在完整 `result.json`，紧凑地图只是可重算的导航派生层。两次接受复跑均为 0 条降级路线。
- 一次更早的独立进程首条向量路线曾因 Hugging Face 客户端 RuntimeError 显式降级到 FTS，仍返回完整限额命中；该瞬时环境限制没有被隐藏。
- Python 3.11 全量回归：465 passed、6 skipped、0 failed，包含真实 KB 与真实 PDF 标记。
- 排除 `evaluation/` 和未触碰的非科学打包文件 `evaluation.zip` 后，科学内容平面仍为 821 文件、326477929 字节；Evidence、manifest、数据库、Passage vector、Card FTS 和 Card source signature 均与 v014 一致。
- 本轮只新增或替换 `evaluation/` 内 v015 接受记录、维护审计、本报告与 `PRODUCTION_RETRIEVAL_LOCK.json`。没有修改或重建论文、PDF、Evidence、Cards、Passage、数据库、向量或 Card 索引。
- Retrieval lock：旧 SHA-256 `a901ead6ac4cffb5264a170a636003ab39e8814ebba71aff001613398e19a5dc`，新 SHA-256 `713ef58de7c3793777d504cfc29f0ad083d84f9d903abd2c744dae8c2e99c26e`。完整证据见 `production_eval/v015/`。

Post-audit 为 0 ERROR；当前状态：**FROZEN — Retrieval Lock / KB Maintenance Coupling**。
