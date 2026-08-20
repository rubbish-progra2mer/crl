<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-answer-accuracy-without-conflict-recognition","card_kind":"failure","paper_id":"P092","evidence_ids":["ev-p092-crs-low","ev-p092-whitebox-metrics"],"source_refs":[{"path":"papers/P092_memconflict.pdf","sha256":"1918dd32c20affd501ac314ab4f1c5b67ab71dc2178784d31b6596030abbebce"}]} -->
# Memory Systems Answer Correctly Without Recognizing the Underlying Conflict

## Observed failure
[AUTHOR_FACT] 六个记忆系统上 Conflict Recognition Score 全线低迷（最好仅 0.2501）；Memobase 静态 AA 相对高但 CRS 最低——最终答案正确与冲突觉察不等价，系统可能返回正确稳定值却从未识别矛盾存在。[[evidence:ev-p092-crs-low]]

## Conditions and scope
[CODEX_SYNTHESIS] MemConflict 基准：dynamic（真更新）/static（假矛盾）/conditional（条件偏好）三型冲突注入长期交互；被评为 Letta/Mem0/LangMem/A-Mem/MemOS/Memobase 六系统。preprint（ACM 模板），judge 为 LLM 辅助匹配＋人工校验（§3.6）。

## Failed intervention
[CODEX_SYNTHESIS] 以最终答案准确率作为记忆冲突处理能力的度量；黑盒 AA 无法区分"裁决了冲突"与"碰巧检回正确值"。

## Evidence and alternative explanations
[AUTHOR_FACT] 白盒侧 SEH@K/SRS 直接检查 gold 一致记忆项是否被检回及其排名，把"支持证据在场"与"答案正确"解耦。[[evidence:ev-p092-whitebox-metrics]]
[CODEX_SYNTHESIS] CRS 低也可能部分反映评分 prompt 对"显式承认矛盾"的苛刻口径；但跨系统一致的低值与 AA-CRS 解耦模式使定性结论稳健。

## Warning for future candidates
[CODEX_SYNTHESIS] 答案级指标应与支持证据级指标（SEH@K/SRS 同族）及冲突觉察指标分层报告；只报答案准确率不足以支撑冲突处理主张。

## Possible repair boundary
[CODEX_HYPOTHESIS] 把冲突识别做成可测中间产物（显式裁决记录）而非答案副产品；与 P091 写侧 supersession 的可审计 ledger 同向。

## Evidence ledger
[CODEX_SYNTHESIS] CRS 解耦发现与白盒指标定义分别绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] conflict recognition score; answer accuracy decoupling; memory conflict; support evidence hit; SEH@K; SRS; dynamic static conditional conflicts; MemConflict; answering correctly without recognizing the conflict; low conflict recognition; conflict awareness decoupled from accuracy; evaluating memory under conflicts
