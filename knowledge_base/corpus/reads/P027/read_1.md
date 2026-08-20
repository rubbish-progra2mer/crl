# P027 Codex 首读：Verified Critical Step Optimization

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P027_critical_step_optimization.pdf`
- PDF SHA-256：`2278960362823372029670a209ba7f9ce969485cd47f831c0406bb6016c1f288`
- 读取范围：动机与 prior（pp.1–3）、分支验证与 DPO（pp.3–5）、设置/基线/主结果/消融（pp.5–9）、PRM prompt 与 teacher 鲁棒性（pp.12–13）。

## Changed computation

- [AUTHOR_FACT] 从当前 policy 的失败轨迹出发，强 expert 为各步提出替代 action；PRM 仅筛出“原 action 低分、替代高分”的候选点（pp.3–4）。
- [AUTHOR_FACT] 对候选点替换一个 expert action 后，其余步骤仍由当前 policy 继续执行；只有最终任务从失败翻为成功的分支才生成 `(same state, successful alternative, original failure)` DPO pair（pp.4–5）。
- [CODEX_SYNTHESIS] 这是 Knowledge→Implement 很重要的 Operator：启发式/LLM 判断只负责缩小搜索，真正准入由非 Oracle 的终局执行结果决定；它避免把 Reviewer/PRM 分数当真值。

## Baseline、公平性与结果

- Policy 为 CK-Pro-8B；训练起点含 47K SFT task-trajectory；Claude-3.7-Sonnet 同时作为 action proposer 与 PRM，K=5，最多两轮更新，三次独立运行（p.5）。
- GAIA-Text-103/XBench-DeepSearch 对比 ETO、RFT、dense Step-DPO、IPR，均在同一 Agent 框架实现；终局仍由带 gold answer 的 LLM judge 判断（pp.5–7）。
- CSO 在 GAIA overall 49.5%，SFT 35.9%，IPR 44.6%；XBench 为 29、23、24（p.7 Table 1）。L3 仅 12 个左右样本量级且 CSO/IPR 都为 16.7，整体增益主要不来自最难层。
- 去 PRM、全步做验证为 48.5% 但需 1967 pairs；PRM+验证 49.5%/671；只有 PRM 无验证 43.6%/4126（p.7 Table 3）。这直接支持“选择器可近似，准入必须验证”。
- K=5→7 无增益且验证成本增加；CSO 额外 token 约为 Step-DPO 的 1.19×（pp.7–8）。成本表不含共同的 123K 任务全轨迹采样，不能把 1.19×当总系统成本。

## 失败边界与未否定项

- “替换一步后成功”证明该替代在该状态与一次后续 rollout 下充分，不证明原 action 是唯一原因，也不证明新 action 在不同随机后续中稳健。
- Expert 与 PRM 同源会使筛选与提案错误相关；附录更换 GPT-4.1/Qwen3-235B 仍有增益，但绝对效果明显依赖 teacher（pp.12–13）。
- outcome verification 依赖任务可判分、完整继续执行与 gold answer；开放 research implement 不能直接复制这一 gate。
- 论文把 PRM 噪声称为被“消除”过强：PRM 不决定最终 label，但决定哪些分支有机会被验证，仍会造成 selection blind spot。
- 未否定：低 PRM 分但可成功的替代会被漏掉；多个动作共同修复的 failure 也可能无法通过单点替换发现。

## Evidence 草案

| Evidence ID | kind | section / page | locator | source range（短引） | Codex note |
|---|---|---|---|---|---|
| P027-E01 | mechanism | §3.2, pp.4–5 | Figure 2, branch rollout | “continuing rollout with the policy model” | [AUTHOR_FACT] 可达性由当前 policy 后续执行验证。 |
| P027-E02 | mechanism | §3.2, p.5 | preference construction | “shared state context” | [AUTHOR_FACT] DPO pair 只改变关键 action。 |
| P027-E03 | result | §5.1, p.7 | Table 3 | “w/o Verification 43.6” | [AUTHOR_FACT] PRM-only 明显弱于终局验证。 |
| P027-E04 | saturation | §5.1, p.7 | Table 4 | “k = 7 ... limited practical benefit” | [AUTHOR_FACT] 分支数存在成本饱和。 |
| P027-E05 | failure | §5.4, p.8 | Figure 3 | “ETO ... falling below the SFT baseline” | [AUTHOR_EXPLANATION] 轨迹级负样本可能 unlearn 正确步骤。 |

## Card 草案（不进入正式 Cards）

### Paper source role — `DRAFT_BEFORE_SECOND_READ`

Agent learning 与“选择器—验证器分工”的高价值 Operator；同时提供 trajectory-level negative contamination 的负向证据。

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Verified Single-Branch Counterfactual Repair`
- Baseline：整条成功/失败轨迹做偏好学习，或用 PRM 直接给每步打分。
- Changed computation：PRM 仅定位候选分支；替换一个 action 后由原 policy 续跑，只有真实终局翻转才形成局部偏好对。
- 前提：终局可可靠判分；state 可精确复现；替代 action 不含隐藏 oracle；续跑预算与基线一致。
- retrieval vocabulary：critical step, branch rollout, outcome verification, reachability, local preference pair。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Whole-Trajectory Negative Contamination`
- 条件：一条失败轨迹的所有 action 被同等当成 negative。
- 现象：原本正确的检索、工具与推理步骤被一并压低；多轮迭代可能跌回 SFT 以下。
- 替代解释：ETO 的 expert/policy 分布差异、数据量或 DPO 超参也可能导致退化。
- 未否定：能局部对齐且保持 state 的轨迹方法可能避免污染。

## 首读裁决

`KEEP_FOR_SECOND_READ`。二读需重点攻击单点因果、同源 teacher/PRM、oracle 与总成本口径。
