<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-llmcompiler","card_kind":"paper","paper_id":"P006","evidence_ids":["ev-p006-dependency-dag-dispatch","ev-p006-token-cost-accounting","ev-p006-shared-prompt-comparison-boundary"],"source_refs":[{"path":"papers/P006_llmcompiler.pdf","sha256":"36dde899ed8abe0df728215e054aab21d1699add719afeb0ddadbb4e4eb23263"}]} -->
# An LLM Compiler for Parallel Function Calling

## Role in the knowledge base
[CODEX_SYNTHESIS] 文本工具 Agent 的并行控制流来源，同时是检查 method gain、latency、token cost、prompt 和 tool-coverage 混杂的重要 Paper Card。

## Problem and setting
[CODEX_SYNTHESIS] 在 search、math、WebShop 和 Tree-of-Thoughts 等任务中比较串行 ReAct、并行函数调用与依赖图调度，报告 accuracy、latency 和 token-dependent cost。

## Changed computation
[AUTHOR_FACT] Planner 生成任务依赖 DAG，Task Fetching Unit 按依赖就绪替换中间结果并把独立任务并行派发给 Executor。[[evidence:ev-p006-dependency-dag-dispatch]]

## Evidence-backed findings
[AUTHOR_FACT] 成本按 input/output token 使用计算；作者把部分成本差异归因于更少 LLM invocation 和只含 plans、不含 observations 的较短 Planner examples。[[evidence:ev-p006-token-cost-accounting]]

[AUTHOR_FACT] 同 benchmark 对照共享 few-shot examples 并通常共享 instruction prompt，但 ReAct-dagger 明确加入额外专用 prompt。[[evidence:ev-p006-shared-prompt-comparison-boundary]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 同模型或同示例不等于完全等预算：并行方法会改变调用数量、观察覆盖和上下文结构；因此 accuracy、latency 与 cost 必须分开归因，不能把全部差异都归给 DAG dispatch。

## Lineage and baselines
[CODEX_SYNTHESIS] ReAct 是串行直接 baseline，OpenAI parallel function calling 是并行 baseline；最关键的缺失对照是固定 Planner、DAG、tool calls 和 observations，仅切换 serial/parallel Executor。

## Evidence ledger
[AUTHOR_FACT] p.4 支持 dependency DAG dispatch；p.7 支持 token/cost accounting；p.16 支持共享示例、共享 instruction 与 ReAct-dagger 例外。[[evidence:ev-p006-dependency-dag-dispatch]] [[evidence:ev-p006-token-cost-accounting]] [[evidence:ev-p006-shared-prompt-comparison-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] method-effect attribution；model and prompt matched comparison；token cost accounting；tool-call and observation budget；parallel function calling；ReAct baseline；LLMCompiler。
