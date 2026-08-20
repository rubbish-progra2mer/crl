# P095 reconciliation — Don't Ask the LLM to Track Freshness

Disposition: `OPERATOR_AND_FAILURE_ADMISSION_WITH_PIPELINE_LEVEL_ATTRIBUTION_BOUNDARY`
Read 1: `corpus/reads/P095/read_1.md`
Accepted read-2: `corpus/reads/P095/read_2_attempts/r2-20260727-p095-a1/`
  - report SHA-256: `5ae9f7bcbf566155f28ebb38ea5381143f1e3cca7184e22f185ca1ea2fdcf001`（18,536 B，已对盘复核）
Other attempts: none
Read 3: **not triggered**。
Reconciler: main Codex, 2026-07-27

## Source reconciliation

1. **AGREE｜机制与主数字**：extract-then-max 管线（三步，≈50 行）；matched 对照 67.2→78.0（+10.8pp，262K +21）；chunk-4096 匹配格 61.0→80.8（+19.8pp）；CAR 逐 hop 确定性解析 FC-MH 30.2/51.5；262K apples-to-apples +28/+33/+20pp；LongMemEval 移植仅打平（57.8 vs 64.4，n=45）。
2. **AGREE｜混杂自认**：+10.8pp 是管线级效应（resolver+prompt 格式+温度联动），作者四处重复声明；限制披露密度高，摘要主张未超出表格。
3. **ACCEPT-BOUNDARY（read-2 新增）｜实际有两个干预点**：除检索后聚合外，fact-level 切分把版本元数据保留前移到**索引期**——matched 对照只对齐了后段；与 MAB Table 3 发表值的跨系统对比在 chunking 上不对齐（+28pp 混合切分/抽取/resolver 三重差异；chunk-4096 消融 80.8% 仍超全部发表系统，说明不全由切分造成）。
4. **ACCEPT-BOUNDARY（read-2 新增）｜缺关键对照**："共享同一候选抽取、让 LLM 挑最新"（LLM-picks-newest）未跑（作者自列 future work）——resolver 单独贡献文内无对照可证。hybrid 回退实测无效（+0.2pp wash）。
5. **ACCEPT-NOTE（read-2）**：SubEM 口径作者自注（利短实体输出的一面已披露）；CAR 每题多次调用（Finding 3 含更多计算成分，单跳无此问题）；未重跑发表系统（避免实现差异，自认）；6K 行不进 apples-to-apples；~30 例失败抽查是定性 pilot；主表 ⋆ 标记与脚注轻微不符；作者-邮箱疑似互换（仅记录）；方法前提=显式全序版本标记，恰为该基准构造性质（跨系统读法：其余系统未利用该显式结构，非在无结构任务上也差）。
6. **AGREE｜方法学正面项（read-2 补强）**：union-accuracy 88.5% 下界检索天花板 + McNemar 配对（85 vs 42, p<0.001）；互补性 21.3% vs 10.5%；条件化于"事实确已检回"把退化定位到判断层。这些是可复用的评测算子。

## Frozen source role

- **不是什么证据**：不证 resolver 的单独贡献（管线级归因，缺共享抽取对照）；不证对已发表系统的同切分优势；不证无显式版本标记场景可用性；LongMemEval 上不证优于 LLM judgment（平局且点值更低）；OP5 问题类型路由是 proposed-untested。三骨干全 OpenAI 系——**无跨家族**。
- 状态：双作者 preprint；外部资源（GitHub/Langfuse traces）未访问核验。
