<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-retrieved-memory-laundered-through-actions","card_kind":"failure","paper_id":"P075","evidence_ids":["ev-p075-retrieve-to-action-leakage","ev-p075-measured-memory-extraction","ev-p075-session-isolation-boundary"],"source_refs":[{"path":"papers/P075_memory_privacy.pdf","sha256":"8c2cfcee69d60f4c20a959cd6b1a6a14d5f6e8d732792cf2a2b4864ac38a88cb"}]} -->
# Retrieved Long-Term Memory Can Be Laundered Through Allowed Actions

## Observed failure
[AUTHOR_FACT] query 可诱导 Agent 把 retrieved history 作为任务对象，并经其正常 code/web 输出格式暴露。[[evidence:ev-p075-retrieve-to-action-leakage]]

## Conditions and scope
[AUTHOR_FACT] 主证据来自两个 GPT-4o single-agent 的静态 200-record memories；30 prompts 报告提取 50/26 条 queries。[[evidence:ev-p075-measured-memory-extraction]]

## Failed intervention
[CODEX_SYNTHESIS] 把其他用户历史无所有权隔离地放入当前模型 context，并假设“无直接 memory API”就足够安全。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 泄露依赖 retrieval exposure、模型服从与合法 action channel；较弱模型提取更少也可能只是正常任务能力更低。

## Warning for future candidates
[CODEX_SYNTHESIS] memory implement 必须测跨用户 retrieval exposure、最终 action leakage、真实调用预算和正常任务能力，不能只评 retrieval accuracy。

## Possible repair boundary
[AUTHOR_FACT] 来源明确缺少 session control，并把 user/session isolation 留作未来研究。[[evidence:ev-p075-session-isolation-boundary]] [CODEX_SYNTHESIS] 因未实验，不把 isolation、sanitization 或 output filter登记为已验证 Operator。

## Evidence ledger
[CODEX_SYNTHESIS] Failure mechanism、observed leakage 与威胁前提均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] retrieved memory leakage; allowed action channel; cross session memory; demonstration exfiltration; ownership isolation
