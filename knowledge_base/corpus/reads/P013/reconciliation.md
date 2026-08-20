# P013 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P013_intrinsic_self_correction_limits.pdf`；SHA-256：`d172f0b3e933544f5165250338e3e989036e8d826fea34093e6aed4adb5b042a`
- 主 Codex 首读：`knowledge_base/pilot/reads/P013/read_1.md`；SHA-256：`adc07b8f34f873dfb58e00b7ef6d2c9d6a90eb4c039c358b8c57f8d5b1993f2a`
- 二读 `r2-20260719-p013-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P013/read_2_attempts/r2-20260719-p013-a1/invocation.md`；SHA-256：`788ae7ba336cd952d962191e7f038e11d9c86c4bafe9e6f64c23c4e7ff74dce5`。Report：`knowledge_base/pilot/reads/P013/read_2_attempts/r2-20260719-p013-a1/report.md`；SHA-256：`795d43a5f4a1807111d755cb5e3330712c51e6ac748ede2b219804315b250ca9`。
- 其他二读 attempts：无。第三读 attempts：无；本文是 reflection/evaluation 的负向诊断材料，不是唯一直接祖先或强方法 baseline；计划不超过两个 Operator/Failure Cards。两读对核心结果无冲突，视觉核查无实质解析冲突。
- 独立性：`procedural_blinding`；二读者声明未读取首读、Cards、其他报告或 blind query。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：论文不是提出新的 self-correction 方法，而是分离三类归因——gold correctness oracle 门控 retry、同模型 intrinsic critique/revise、以及多响应 sampling/selection；还检查 feedback 是否迟到地加入初始 prompt 缺失的任务约束。核点：PDF pp.2–4 §§2–3、Table 1–3。

### Baseline — `AGREE`

Intrinsic correction 的直接 baseline 是同模型单次 Standard Prompting，但不是等成本；debate 的最近公平 baseline 是相同 3/6/9 responses 的 self-consistency；constrained generation 的最近 baseline 是把 `ALL concepts` 前置的强 initial prompt。核点：PDF pp.4–8 Tables 3–8。

### 公平性与预算 — `AGREE`

Oracle setting 机械保护正确初答不再被修改；intrinsic 两轮使调用数 1→3→5，Section 3 未与等 token/call independent sampling 全面对齐；debate 仅按 response 数对齐，未给 token；模型 temperature、sample sizes 和 GPT-3.5 snapshot 跨节不同。核点：PDF pp.3–7。

### 主要结果 — `AGREE`

Tables 3–6 中所测 intrinsic correction 均未超过各自 standard；Figure 1 显示 correct→incorrect 可抵消/超过修正。Table 7 在 6/9 responses 下 self-consistency 85.3/88.2 高于 debate 83.2/83.0。强 initial prompt 81.8，再 self-correct 降至 75.1。核点：PDF pp.4–8。

### Limitation — `AGREE`

结论仅覆盖 2023-era models、所测 reasoning tasks、最多两轮且无外部反馈；不否定 tool/executor/human/训练 verifier，也不覆盖 style/safety。GPT-4 等仅随机 200 题、Hotpot 100，无 CI/seed/显著性。Table 8 两组原结果/复现数的行级映射不够清楚，作为 source ambiguity 保留。核点：PDF pp.3、5、7–9。

### Operator — `RESOLVED_BY_SOURCE`

Pilot 只抽取评测 Operator `Feedback-Provenance and Budget Separation`：分别报告 intrinsic、oracle/tool/human/other-model feedback，并以 equal-response/token baseline 与 strong initial prompt 防止把额外信息/计算错归于 reflection。Oracle-gated correction 本身作为被审计条件，不作为推荐方法。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Intrinsic Critique Flips Correct Reasoning`：无新外部信息时，problem-seeking review prompt 可使正确初答变错，尤其在表面相关 distractors 下；适用范围严格限于本文所测模型/任务/提示。Oracle masking 与 debate sampling confound 放入 Paper Card。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：当前更强模型复现、开放 agent trajectory 的等预算 baseline、独立 calibrated verifier 的反馈层级、更多轮 retain/abstain gate 均未由本文解决。
- CORE disposition：`ACCEPT`。它是 Pilot 的关键负向知识来源，且通过窄化 Claim 可避免“reflection 普遍无效”的错误外推。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先创建 Evidence。
