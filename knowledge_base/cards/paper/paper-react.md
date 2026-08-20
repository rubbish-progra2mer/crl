<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-react","card_kind":"paper","paper_id":"P001","evidence_ids":["ev-p001-react-interleaved","ev-p001-search-hallucination-boundary"],"source_refs":[{"path":"papers/P001_react.pdf","sha256":"f285b0971ae4a790e402fb93966bed3adde2cf0a04977d08b2b40d6ab0cace69"}]} -->
# ReAct

## Role in the knowledge base
[CODEX_SYNTHESIS] Planning/tool-use 直接祖先与强 baseline，解释 reasoning–acting 交错而不是泛称“会用工具”。

## Problem and setting
[CODEX_SYNTHESIS] 文本 QA 与交互式环境中的语言 Agent；模型通过语言动作访问环境反馈。

## Changed computation
[AUTHOR_FACT] 同一轨迹中交错生成 reasoning traces 与 task actions。[[evidence:ev-p001-react-interleaved]]

## Evidence-backed findings
[AUTHOR_FACT] 人工错误分析将 search-result error 与 hallucinated reasoning 分开记录。[[evidence:ev-p001-search-hallucination-boundary]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 非信息性搜索会使后续推理难以恢复；当前 Evidence 不支持把所有结果差异纯归因于 Thought。

## Lineage and baselines
[CODEX_SYNTHESIS] Reason-only CoT 与 Act-only 是本文展示的直接组件对照；ReAct 是后续部分 tool-use Agent 的常用基线或执行底座。

## Evidence ledger
[AUTHOR_FACT] p.2 支持 changed computation；p.6 Table 2 支持错误类型边界。[[evidence:ev-p001-react-interleaved]] [[evidence:ev-p001-search-hallucination-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] ReAct；reasoning acting；Thought Action Observation；tool-use ancestor；推理行动交错。
