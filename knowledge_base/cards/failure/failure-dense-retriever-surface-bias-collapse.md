<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-dense-retriever-surface-bias-collapse","card_kind":"failure","paper_id":"P093","evidence_ids":["ev-p093-foil-collapse","ev-p093-poison-rag","ev-p093-paired-protocol"],"source_refs":[{"path":"papers/P093_dense_retriever_collapse.pdf","sha256":"e62a61bf3e0bfbfcbd08f9fe09cdb29079f9e87035c32b3ee7eee89df1630fb1"}]} -->
# Surface Biases Outrank Answer-Bearing Evidence in Dense Retrievers

## Observed failure
[AUTHOR_FACT] 偏差叠加时顶级稠密检索器崩塌：在 foil（含 brevity/literal/position 等偏差但无答案）与含答案文档的成对比较中，8 模型选中含答案文档的比例 <10%（最低 0.4%）。[[evidence:ev-p093-foil-collapse]]
[AUTHOR_FACT] 该偏好可被利用：检索器偏好的 poisoned 文档使 RAG 表现劣于不给文档，注入假事实。[[evidence:ev-p093-poison-rag]]

## Conditions and scope
[AUTHOR_FACT] 受控构造：Re-DocRED 关系抽取改造为单因素文档对，每设定 250 查询、配对 t 检验。[[evidence:ev-p093-paired-protocol]]
[CODEX_SYNTHESIS] ACL 2025 正式发表。范围：单向量稠密检索器（微调五模型+Contriever 为主电池；ColBERT v2 另见 Fig.1 五设定与 foil；ReasonIR-8B 仅 foil 电池）；合成模板查询、英文单跳。

## Failed intervention
[CODEX_SYNTHESIS] 假设"嵌入相似度=事实相关性"，直接在含对抗/偏差文本的库上用 dense top-k 供给下游。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 成对打分比较非全库 top-k 检索——端到端攻击成功率未实测（作者推断级）；poison 实验 GPT-4o 自产自评有 judge 自环，四条件相对排序稳健、绝对值连同条件引用；无 BM25/重排器同电池对照，不证偏差为 dense 特有。

## Warning for future candidates
[CODEX_SYNTHESIS] literal/brevity/position 检索残差的方法学最近邻；本文未测试 2025–2026 世代强嵌入器，因此其结论不可直接外推到这些模型。

## Possible repair boundary
[CODEX_HYPOTHESIS] 缓解未在本文测试（无缓解实验）；paraphrase 消融（literal-bias 检验）可迁移到时序检索载体。

## Evidence ledger
[CODEX_SYNTHESIS] foil 崩塌、poison RAG、配对协议三条绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] dense retriever bias; brevity bias; literal bias; position bias; foil document; poisoning; paired t-test; Re-DocRED; answer presence; dense retriever prefers distractors; biased document outranks the answer; retrieval bias collapse; poisoned documents preferred; misleading retrieved evidence; ranking short early literal documents
