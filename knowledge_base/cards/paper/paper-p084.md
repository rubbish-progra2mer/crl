<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p084","card_kind":"paper","paper_id":"P084","evidence_ids":["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p084-expanded-toolkit-table","ev-p084-generated-tool-single-dataset-boundary"],"source_refs":[{"path":"papers/P084_function_calling_robustness.pdf","sha256":"8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7"}]} -->
# On the Robustness of Agentic Function Calling

## Role in the knowledge base
[CODEX_SYNTHESIS] 语义相关 toolkit expansion 的直接负向来源；把“工具描述偏置”推进到固定原始 request/model 下的 function-set interference 测量。

## Problem and setting
[AUTHOR_FACT] 论文在 200 个 single-turn BFCL 样例上比较原始 thin toolkit 与加入语义相关函数后的 expanded toolkit。[[evidence:ev-p084-expanded-toolkit-controlled-setting]]

## Changed computation
[CODEX_SYNTHESIS] 本文改变的是 Agent 每步可见的 function menu，不提出在线 router；原始 query 不变，平均工具数从 2.7 增至 5.6。[[evidence:ev-p084-expanded-toolkit-controlled-setting]]

## Evidence-backed findings
[AUTHOR_FACT] 表 2 中九个模型的 expanded-toolkit AST 分数均低于各自 original 分数。[[evidence:ev-p084-expanded-toolkit-table]]
[AUTHOR_FACT] 扩展条件的失败包括 wrong function、wrong number of functions、wrong parameter assignment 与 parameter hallucination。[[evidence:ev-p084-related-toolkit-error-types]]

## Limitations and failure signals
[AUTHOR_FACT] 研究只使用一个数据集，related requests/tools 由多个 LLM 离线生成。[[evidence:ev-p084-generated-tool-single-dataset-boundary]]
[CODEX_SYNTHESIS] AST 评价不等于真实工具执行；论文未报告 baseline 同口径错误类型分布，也未配平新增工具文本造成的 prompt-token 增量。Claude-3.5-Haiku 行印刷相对百分比与绝对分数不一致，因此 CRL 不复用该百分比。

## Lineage and baselines
[CODEX_SYNTHESIS] P084 补足 P078 通用/未验证工具库退化的直接 interference Evidence；它不验证 tool filtering repair，也不把 offline cosine equivalence filter 登记为 Operator。

## Evidence ledger
[CODEX_SYNTHESIS] intervention、error taxonomy、完整表格与单数据集/生成工具边界分别绑定当前 Passage SHA。

## Retrieval vocabulary
[CODEX_SYNTHESIS] semantically related tools; overlapping functions; toolkit expansion; tool menu interference; wrong function selection; wrong parameter assignment; parameter hallucination; BFCL AST robustness; fixed original query; visible function count
