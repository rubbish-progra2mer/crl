# P090 first read (W06) — MemGAS occupies read-side multi-granularity allocation, not temporal validity

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents (MemGAS)
- Authors: Derong Xu; Yi Wen; Pengyue Jia; Yingyi Zhang; Wenlin Zhang; Yichao Wang; Huifeng Guo; Ruiming Tang; Xiangyu Zhao; Enhong Chen; Tong Xu
- Identity: arXiv 2505.19549v2 (2025-09-29); no venue note on abs page (ICLR-style template; treat as preprint); code `github.com/quqxui/MemGAS`
- PDF: `knowledge_base/staging/w06_targeted/P090_memgas.pdf`
- Parse check: 33 physical pages

## Canonical operator contribution


## Evidence and closest lineage

- 载体与基线：LoCoMo、Long-MT-Bench+、LongMemEval-s/m；基线 Full History、MPNet、Contriever、MPC、RecurSum、SeCom、HippoRAG 2、RAPTOR、A-Mem（p.5-6）。
- 主结果（Table 1，GPT4o-mini 生成、Contriever 检索底座）：LongMemEval-s 4o-J 60.20 vs Contriever 55.40 / HippoRAG2 57.60；F1 20.38 vs 13.78/14.73。Table 2 检索：LongMemEval-s R@10 94.47 vs HippoRAG2 91.28。
- 消融（Table 3，LongMemEval-s）：w/o All 使 F1 20.38→13.78、R@3 78.51→71.06；单组件移除各降 ~1-3 点 4o-J——各组件贡献小而叠加。
- 粒度×查询类型（Table 7，LongMemEval-m R@3）：**knowledge-update 最优单粒度是 turn 41.67，router 51.39，oracle 选择 72.22**——路由距 oracle 有 ~21 点缺口；不同查询类型偏好不同粒度是其核心经验事实。
- 构建成本（Table 8-9）：LongMemEval-s（语料 ~51.6M tokens）构建耗 52.9M 输入/5.2M 输出 tokens；额外存储 ~27MB（原始 266MB 的 10%）。等 token 对照（D.2）：8k/16k 截断下 4o-J 仍最高（59.8/60.3）。
- 误差分析（Fig.7）：LongMemEval-m 40.6% 属"检索错+生成错"；方法对无相关信息倾向回答"未提及"。

## Measurement and fairness boundaries

- 评判以 GPT4o-as-Judge 为主指标，无显著性/误差棒/多 seed；temperature 0 单跑。
- 统一 top-3 session 设置对部分基线（RAPTOR/A-Mem 检索不可评、LongMemEval-m 上多基线因运行时长缺席）造成覆盖不齐。
- write 侧多粒度元数据由 LLM 生成——方法收益与 write-time LLM 计算捆绑（Table 8 已计量，但 QA 对比不按等构建预算配平）。
- 熵路由的前提是"低熵=该粒度可信"；理论节（App.H）给的是条件性保证。

## Draft knowledge objects

### Operator draft: `Entropy-Routed Multi-Granularity Retrieval over GMM Association Graph`

对同一底层记忆维护四粒度视图；查询时按各粒度相似度分布熵的倒数加权融合，再在 accept-集关联图上 PPR 传播。Intervention target = 检索时粒度权重分配；predicted signature = 不同查询类型的最优粒度不同、路由接近但不达 oracle。

### Failure draft: `Fixed Single-Granularity Segmentation Loses Cross-Session Links`

单粒度切分导致多 session 查询部分检索（Fig.1 实例）；且即便自适应路由，与 oracle 粒度选择仍差 ~21 点（knowledge-update，Table 7）——粒度自适应本身仍是开放缺口。

## Draft Evidence locators

- Physical pp.1-3: 问题设定、两个 limit 主张、Fig.1 多 session 实例。
- Physical pp.3-5: 四粒度构建、GMM accept/reject、熵路由公式、PPR+过滤。
- Physical pp.5-8: Table 1/2 主结果、Table 3 消融。
- Physical p.19: Table 7 粒度×查询类型（knowledge-update 行）。
- Physical p.20: Table 8/9 构建 token 与存储成本。

All claims remain draft until independent read and reconciliation.
