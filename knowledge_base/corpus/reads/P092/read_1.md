# P092 first read (W06) — MemConflict：冲突分型 + 白盒检索/排序指标（SEH@K/SRS）与利用缺口诊断

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: MemConflict: Evaluating Long-Term Memory Systems Under Memory Conflicts
- Authors: Zhen Tao; Jinxiang Zhao; Peng Liu; Dinghao Xi; Yanfang Chen; Wei Xu; Zhiyu Li（人大 + 上财 + MemTensor）
- Identity: arXiv 2605.20926v1 (2026-05-20)，cs.IR；ACM 期刊模板（J.ACM 占位页脚，未见正式接收标注）；代码 `github.com/TaoZhen1110/MemConflict`
- PDF: `knowledge_base/staging/w06_targeted/P092_memconflict.pdf`；SHA-256 `1918dd32c20affd501ac314ab4f1c5b67ab71dc2178784d31b6596030abbebce`
- Parse check: 33 physical pages

## Canonical contribution

以 fitness-for-use 视角把记忆有效性形式化为查询条件化问题，分三种冲突：**dynamic**（真更新取代旧状态，考时序有效性）、**static**（后来的错误矛盾不应覆盖稳定事实，考事实保持）、**conditional**（多值各自条件下有效，考条件-值绑定）；再注入相关实体的语义相似干扰项。评测协议双层：黑盒 AA（+动态 UOCS、静态 CRS 诊断）与**白盒 SEH@K（gold 记忆项进 top-K 命中率）与 SRS（对数折扣排名分）**；并定义 Evidence Utilization Gap = SEH@3 − AA 区分"检索到但没用上"。基准由结构化用户画像（Persona Hub 种子）经 LLM（gpt-5.0-mini）流水线生成：时间线模拟（2022-01–2025-12 月粒度）、冲突构造、synopsis→对话两阶段生成、人工检查。

## Evidence and closest lineage

- 数据规模（Table 2）：**12 个实例**（虚拟用户），均值 52.3 sessions / 2349 turns / 204k tokens / 124.3 查询；查询分布 dynamic 90.8 / static 16.7 / conditional 16.9（宏平均聚合防 dynamic 主导）。冲突距离 5–49 sessions；干扰项均值 32.8/实例。
- 被测六系统：A-Mem、LangMem、Letta、MemOS、Mem0、Memobase。黑盒（Table 3）：MemOS 平均 AA 最高 0.554；static 最难（最好 0.4375）；conditional 极化（MemOS/Letta/Mem0/A-Mem 0.71-0.84 vs LangMem 0.16/Memobase 0.24）；**CRS 全员 ≤0.2501**——答对稳定值≠识别出矛盾存在。
- 白盒（Table 4）：MemOS 平均 SEH@3 0.671/SRS 0.588 最高；LangMem 专精 dynamic（SEH@3 0.784）但 static/conditional 崩；SEH@3 普遍高于 SRS——gold 项常在集合内但排名低，冲突下易被无效项盖过。
- 敏感性：更深检索 K=2→5 提升不均（Letta 受益最大）；**冲突距离增大（5-10→20-25 sessions）全系统三指标齐降**（Fig.7）；implicit 查询普遍降（Table 5）；干扰项注入降性能。
- 诊断（Table 7, Fig.8）：EUG 最大 LangMem（dynamic 0.288——检索到更新记忆却不产出时序有效答案）；失败分解中 retrieval failure 占多数（46-91%），但 utilization failure 在 conditional 达 9-36%。
- 效率（Table 6）：加库成本差异巨大（Mem0 40216s vs MemOS 473s）。

## Measurement and fairness boundaries

- **基准全 LLM 生成**（画像/时间线/对话/查询均 gpt-5.0-mini），人工验证覆盖度未量化到条目级；12 实例的用户级 N 很小（查询级 N 依赖同实例内相关样本）。
- 判分为 LLM 辅助匹配 + 人工复核；无显著性区间；六系统各按默认用法接入，公平性受各系统默认配置影响（作者自认按"intended design"保留差异）。
- 白盒接口要求系统暴露 top-K 记忆——对无自然检索列表的系统需适配。
- ACM 模板占位（"J. ACM 2018"样板页脚、DOI XXXXXXX）：投稿态，未见接收记录。

## Draft knowledge objects

### Failure draft: `Conflict-Type Unevenness and Low Conflict Recognition in Memory Systems`

六个代表性记忆系统在 dynamic/static/conditional 三型冲突上强弱严重不均；矛盾识别（CRS）全员 ≤0.25，答案正确常与冲突意识脱钩；冲突候选间隔越远性能越差。

### Operator draft: `White-Box Support-Evidence Metrics for Memory Evaluation (SEH@K/SRS/EUG)`

把评测从答案级拆到"gold 记忆项是否被检回、排多高、检回后是否被用上"三层；changed computation = 评测计算从终态判分改为检索证据链判分。可迁移为任何记忆/检索系统的诊断层。

## Draft Evidence locators

- Physical pp.2-3: 三冲突类型定义与 Fig.1 实例。
- Physical pp.8-13: 构造流水线（画像/时间线/冲突/对话/查询）。
- Physical pp.13-15: 指标定义（AA/SEH@K/SRS/UOCS/CRS）；p.16 Table 2 数据统计。
- Physical pp.18-20: Table 3/4 主结果；p.24-25 implicit 与距离敏感性；pp.26-27 效率与 EUG/失败分解。

All claims remain draft until independent read and reconciliation.
