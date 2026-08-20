# P093 reconciliation — Collapse of Dense Retrievers

Disposition: `FAILURE_AND_OPERATOR_ADMISSION_WITH_PAIRWISE_SCOPE_AND_JUDGE_SELF_LOOP_BOUNDARIES`
Read 1: `corpus/reads/P093/read_1.md`
Accepted read-2: `corpus/reads/P093/read_2_attempts/r2-20260727-p093-a1/`
  - report SHA-256: `77a958f4bfb16831fc57ff387868709b446d2c10f8939f6f41873b35d2ed130a`（16,763 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜构造与统计框架**：Re-DocRED 改造、单因素文档对、配对 t（n=250/df=249）、五偏差电池、foil/poison 组合、DecompX 仅可视化。
2. **AGREE｜主结果**：foil 下 8 模型 accuracy 0.4–8.0%（t −21~−42）；poison 使 gpt-4o 64.8→30.8（"34% drop"=34.0pp 核实）；无监督 Contriever answer-importance t=−5.92；ColBERT v2/ReasonIR-8B 也 <9%。
3. **ACCEPT-BOUNDARY（read-2 新增）｜成对比较非真实检索**：Table 4/A.9 是 D1-vs-D2 打分比较，非全库 top-k 检索；"可使 top-k 全为偏置文档"是作者的 potentially 级推断未实测。攻击叙事 = 成对偏好证明 + 单独的 RAG 喂入实验拼接。
4. **ACCEPT-BOUNDARY（read-2 新增）｜judge 自环**：poison 句由 GPT-4o 生成、RAG 答案由 GPT-4o 生成、判分也是 GPT-4o——绝对数字有 judge 偏置风险，四条件相对排序稳健；模型版本已钉死（gpt-4o-2024-08-06 等）。
5. **ACCEPT-DEFECT（read-2 新增）**：(a) Table 3 与 Table A.8/Fig A.1 同设定数值有 ≤0.05 漂移（来源不明，不影响方向）；(b) "poison 100% 被偏好"对 Contriever 实为 98.8%（微调五模型确为 100%）；(c) PDF 本体无 "ACL 2025" 字样——会议归属以外部 abs 页 venue 注记为准（首读已核）。
6. **AGREE｜范围边界**：单向量稠密检索器为对象（ColBERT/ReasonIR 只测 foil）；无 BM25/重排器同电池对照；合成模板查询、仅英文单跳；无缓解实验。brevity 与池化稀释在解释层不可分（作者自给 pollution effect）。

## Frozen source role

- 状态：published（ACL 2025 主会，venue 依 abs 页）；数据集 ColDeR 公开。
