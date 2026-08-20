# P094 reconciliation — MemoryAgentBench

Disposition: `EVALUATION_CARRIER_ADMISSION_WITH_BACKBONE_AND_CHUNKSIZE_CONFOUND_BOUNDARIES`
Read 1: `corpus/reads/P094/read_1.md`
Accepted read-2: `corpus/reads/P094/read_2_attempts/r2-20260727-p094-a1/`
  - report SHA-256: `a14978b3bb731c253cc19ac3fb631fcde9928e03c13ccadb8a162903dbde1b8f`（17,229 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜身份与框架**：ICLR 2026 正式发表（页眉自证）；四能力（AR/TTL/LRU/SF）；两阶段增量注入协议；EventQA/FactConsolidation 两个新数据集；2071 问、103K–1.44M 上下文；SF 序号护栏 prompt。
2. **AGREE｜主结果**：GPT-5-mini Overall 60.6 最强；FC-MH 全线 ≤28%；o4-mini 6K→32K 从 80.0 崩至 14.0（任务可解、长程失败）；商业记忆代理 Overall 低于裸 GPT-4o-mini 参照（42.3）。
3. **ACCEPT-BOUNDARY（read-2 新增，重要）｜两个主表混杂**：(a) **骨干不齐**——长上下文代理各用自家模型而 RAG/商业代理固定 4o-mini，主表跨行非同骨干比较；公平对照是附录 J 的算力配平三档（预算拉平后 LC/BM25 近乎打平，"success is determined by meeting the full information threshold, not by the architecture itself"）。(b) **chunk size 配置不齐**——商业代理被统一 4096 而 BM25/embedding RAG 在 AR/SF 用 512，512 对 AR 显著更优（HippoRAG SH-QA 76.0 vs 49.0）——商业代理 AR/SF 劣势部分是配置伪影，正文未明示。**引用系统排名必须连同这两个混杂。**
4. **ACCEPT（read-2 新增）｜有利证据**：TTL 零样本地板 <4%（排除预训练先验解释）；SF 提示工程消融（激进/保守覆写策略都救不了，Table 19）——加固"长程更新一致性是机制级失败"的读法。
5. **ACCEPT-NOTE（read-2）**：GPT-4o 既当 judge 又是被测代理（轻度自评亲和，作者未讨论）；MIRIX 部分延迟为估计值（带 * ）；FC 答案 SubEM 硬匹配（10 token 上限）受 judge 影响小；小型内部瑕疵（42.2/42.3、"five dimensions" 实列四、"Abstractive Retrieval" 笔误、Overall 聚合公式未明示但可反推为四类均分）。
6. **AGREE｜作者自认限制**：预算限制只测代表性代理；SF 合成设置自认并辩护；TTL 为在线学习简化；离散 chunk 非真流式；未测 top-k=20。

## Frozen source role

- **不是什么证据**：主表跨行排名不作同骨干/同配置结论引用（两混杂）；不证 SF 失败不可被"chunk=512+强骨干+更深检索"组合缓解（该组合单元未测全）；FC 序号护栏使其结果不可直接与 marker-free 口径（P091）比较。
- 状态：published（ICLR 2026）；arXiv v4 与 OpenReview 录用版逐字一致性未核（OPEN，引用以 v4 bytes 为准）。
