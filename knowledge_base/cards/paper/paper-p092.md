<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p092","card_kind":"paper","paper_id":"P092","evidence_ids":["ev-p092-whitebox-metrics","ev-p092-crs-low"],"source_refs":[{"path":"papers/P092_memconflict.pdf","sha256":"1918dd32c20affd501ac314ab4f1c5b67ab71dc2178784d31b6596030abbebce"}]} -->
# MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts

## Role in the knowledge base
[CODEX_SYNTHESIS] 白盒支持证据检索指标（SEH@K/SRS/EUG）与三型冲突分类的组合基线；适合作为长期记忆分层测量主张的口径对照。

## Problem and setting
[CODEX_SYNTHESIS] 长期交互中记忆冲突是常态而非异常：dynamic（真更新取代）、static（假矛盾干扰）、conditional（条件依赖偏好）三型，各要求不同的有效性判断。

## Changed computation
[AUTHOR_FACT] 评测计算从黑盒 AA 扩展为白盒 SEH@K/SRS（支持证据是否检回、排名）+ 冲突觉察指标（CRS/UOCS）。[[evidence:ev-p092-whitebox-metrics]]

## Evidence-backed findings
[AUTHOR_FACT] 无系统全面占优；静态冲突平均最难；CRS 全线低（最好 0.2501），AA 与 CRS 解耦——正确答案不等于识别了冲突。[[evidence:ev-p092-crs-low]]

## Limitations and failure signals
[CODEX_SYNTHESIS] preprint 未过评审；冲突为构造注入（分布与野生冲突有距离）；LLM judge 链的口径影响 CRS 绝对值；六系统各配置差异未完全配平——排名按方向引用。

## Lineage and baselines
[CODEX_SYNTHESIS] RAG 知识冲突线（文档间/参数-上下文）之外的长期记忆条件实例化；与 P094（FactConsolidation）、P091（marker-free）构成三个互补评测口径。

## Evidence ledger
[CODEX_SYNTHESIS] 白盒指标定义与主结果解耦发现绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] MemConflict; memory conflict taxonomy; white-box metrics; conflict recognition; update order consistency; long-term memory evaluation; Letta Mem0 LangMem MemOS; long-term memory conflict benchmark; dynamic static conditional conflicts; evaluating memory systems under conflicting information
