<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-semantically-related-toolkit-expansion","card_kind":"failure","paper_id":"P084","evidence_ids":["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p084-expanded-toolkit-table","ev-p084-generated-tool-single-dataset-boundary"],"source_refs":[{"path":"papers/P084_function_calling_robustness.pdf","sha256":"8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7"}]} -->
# Semantically Related Toolkit Expansion Destabilizes Function Calling

## Observed failure
[AUTHOR_FACT] 在 expanded related-function toolkit 下，表 2 中九个模型的 AST 分数均低于各自 original-toolkit 分数。[[evidence:ev-p084-expanded-toolkit-table]]
[AUTHOR_FACT] 扩展条件的失败包含 wrong function、wrong function count、wrong parameter assignment 与 parameter hallucination。[[evidence:ev-p084-related-toolkit-error-types]]

## Conditions and scope
[AUTHOR_FACT] 200 个原始 BFCL request 不变，平均可见工具由 2.7 增至 5.6，新增约三个语义相关但预期功能不同的函数；只评价 AST construction。[[evidence:ev-p084-expanded-toolkit-controlled-setting]]
[CODEX_SYNTHESIS] 该结果证明当前 intervention 下的 function-menu interference，不证明函数数越多错误必然单调上升，也不证明 runtime malformed-argument exception 或端到端失败。

## Failed intervention
[CODEX_SYNTHESIS] 把更多“语义相关”函数全部暴露给 Agent 并非无害扩展；relevance 不能代替可执行必要性或功能区分。

## Evidence and alternative explanations
[AUTHOR_FACT] 论文只用一个数据集，related requests/tools 由多个 LLM 离线生成。[[evidence:ev-p084-generated-tool-single-dataset-boundary]]
[CODEX_SYNTHESIS] 新工具同时增加 prompt 长度；论文未报告 decoding seeds/repeats、tool ordering 或 baseline 类别级错误分布。0.8 cosine signature filter 也不是功能等价证明。因此不能把全部下降唯一归因于“语义重叠”，更不能声称 wrong-function/argument 类别各自相对 baseline 的精确增量。

## Warning for future candidates
[CODEX_SYNTHESIS] 工具路由/检索 Candidate 必须分开报告 correct-tool recall、visible menu size、actual selection、argument correctness 与 task success，并在同模型、同 request/instance、同 demonstrations、同允许 calls 下核算 prompt tokens；不能只用较小菜单的准确率宣称新决策机制有效。

## Possible repair boundary
[CODEX_HYPOTHESIS] state-或contract-aware minimal tool exposure 值得作为 Operator 假设，但 P084 没有实现或验证在线 router，故此处不登记成功修复。

## Evidence ledger
[CODEX_SYNTHESIS] controlled setting、全部模型总体方向、错误类别与生成数据/AST 边界均有独立 Evidence；相对类别增量和单调性明确不在 claim 内。

## Retrieval vocabulary
[CODEX_SYNTHESIS] many semantically overlapping functions; related tool distractors; toolkit expansion failure; wrong tool call; wrong function selection; malformed or incorrect arguments; parameter hallucination; fixed model request demonstrations calls; tool menu interference; prompt length confound
