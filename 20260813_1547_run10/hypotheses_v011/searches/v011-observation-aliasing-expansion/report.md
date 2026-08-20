<!-- CRL_RESEARCH_SEARCH_META {"created_at_utc":"2026-08-13T11:34:49.317566Z","request_fingerprint_sha256":"3d73ee127a327cbf91cafea085d855ce66cb232da221a65222b434ee8498c24f","result_json_sha256":"f165426af2ed918c626ac2b25ed7ca1dce07df4a1e9614f73003dbbb06aec69e","search_id":"v011-observation-aliasing-expansion"} -->
# 研究检索导航

> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。

- 搜索标识：`v011-observation-aliasing-expansion`
- 生成时间（协调世界时）：`2026-08-13T11:34:49.317566Z`

## 紧凑研究地图

> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。

- Paper `P055` · Language Model as Planner and Formalizer under Constraints；用途 `problem`；路线 `q001:passage_hybrid` #1；Passage `P055:p0010:s0002`
- Paper `P027` · Verified Critical Step Optimization for LLM Agents；用途 `failure`；路线 `q002:passage_hybrid` #1；Passage `P027:p0011:s0001`
- Paper `P074` · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs；用途 `operator`；路线 `q003:passage_hybrid` #1；Passage `P074:p0012:s0001`
- Paper `P047` · tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment；用途 `prior`；路线 `q004:paper_card_fts` #1；Card `paper-p047`（paper）；Evidence `ev-p047-evaluation-core`
- Paper `P041` · LLM Agents Already Know When to Call Tools - Even Without Reasoning；用途 `prior`；路线 `q004:operator_card_fts` #1；Card `operator-hidden-state-tool-necessity-prefill`（operator）；Evidence `ev-p041-operator-core`, `ev-p041-probe-prefill-steering`
- Paper `P036` · tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge；用途 `prior`；路线 `q004:failure_card_fts` #1；Card `failure-gold-context-does-not-solve-knowledge-use`（failure）；Evidence `ev-p036-failure-core`
- Paper `P007` · tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains；用途 `prior`；路线 `q004:passage_hybrid` #2；Passage `P007:p0003:s0002`
- Paper `P042` · LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild；用途 `measurement`；路线 `q005:passage_hybrid` #3；Passage `P042:p0030:s0001`

- 代表项：8 / 去重 Paper：63

## 查询与路线覆盖

### q001 · problem

- 原始查询：`工具型大语言模型智能体在不同隐藏外部状态下收到相同或近似观察，却需要采取不同的安全后续动作；观察别名导致错误提交`
- 规范化查询：`"工具型大语言模型智能体在不同隐藏外部状态下收到相同或近似观察" OR "却需要采取不同的安全后续动作" OR "观察别名导致错误提交"`
- 路线 `paper_card_fts`：0 条；降级 false（无）
- 路线 `failure_card_fts`：0 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：0 条；降级 false（无）

### q002 · failure

- 原始查询：`部分可观测、分页或权限隐藏、陈旧响应与摘要压缩使状态不可区分，智能体在不可辨识状态下过早执行不可逆动作`
- 规范化查询：`"部分可观测" OR "分页或权限隐藏" OR "陈旧响应与摘要压缩使状态不可区分" OR "智能体在不可辨识状态下过早执行不可逆动作"`
- 路线 `failure_card_fts`：0 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `operator_card_fts`：0 条；降级 false（无）
- 路线 `paper_card_fts`：0 条；降级 false（无）

### q003 · operator

- 原始查询：`主动选择最小区分性只读查询，基于反例分裂观察等价类；无法区分时机械拒绝或澄清`
- 规范化查询：`"主动选择最小区分性只读查询" OR "基于反例分裂观察等价类" OR "无法区分时机械拒绝或澄清"`
- 路线 `operator_card_fts`：0 条；降级 false（无）
- 路线 `paper_card_fts`：0 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：0 条；降级 false（无）

### q004 · prior

- 原始查询：`LLM agent active sensing hidden state POMDP observation aliasing distinguishing query bisimulation tool use`
- 规范化查询：`"LLM" OR "agent" OR "active" OR "sensing" OR "hidden" OR "state" OR "POMDP" OR "observation" OR "aliasing" OR "distinguishing" OR "query" OR "bisimulation" OR "tool" OR "use"`
- 路线 `paper_card_fts`：20 条；降级 false（无）
- 路线 `operator_card_fts`：20 条；降级 false（无）
- 路线 `failure_card_fts`：20 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）

### q005 · measurement

- 原始查询：`构造观测相同但正确动作相反的成对隐藏状态，独立终局评价区分查询是否降低错误且报告额外调用与弃权`
- 规范化查询：`"构造观测相同但正确动作相反的成对隐藏状态" OR "独立终局评价区分查询是否降低错误且报告额外调用与弃权"`
- 路线 `paper_card_fts`：0 条；降级 false（无）
- 路线 `passage_hybrid`：24 条；降级 false（无）
- 路线 `failure_card_fts`：0 条；降级 false（无）
- 路线 `operator_card_fts`：0 条；降级 false（无）

## 覆盖诊断

- 去重 Card：60
- 去重 Evidence：90
- 去重 Passage：73
- 命中 Paper：63
- 原始观测：180
- 带机械噪声标记的观测：96
