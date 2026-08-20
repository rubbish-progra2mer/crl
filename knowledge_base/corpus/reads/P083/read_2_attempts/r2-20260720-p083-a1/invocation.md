# P083 independent read_2 invocation

## Identity

- paper_id: `P083`
- attempt_id: `r2-20260720-p083-a1`
- task: PLAN_05 独立二读；逐页阅读全文，形成仅面向本轮饱和阅读决策的 `report.md`。
- source_pdf: `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/plan05_sat_a3/P083_tamas.pdf`
- source_pdf_sha256: `4AD6D486003DC7268C80CDC2F49224A955792843D57155915D5F77889F7F7BDD`
- source_pdf_bytes: `3628351`

## Allowed inputs

- 唯一允许的科研内容输入：上述 P083 原始 PDF。
- 允许的程序性输入：任务调用消息；工作区根目录 `AGENTS.md`；`crl_agent_v3/AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`；本地 `pdf` 技能说明。
- 允许的机械工具：本地文件哈希、PDF 页数/文本抽取/页面渲染与视觉核验、UTF-8/LF 校验；这些工具只辅助逐页定位，不替代原文阅读。

## Procedural blinding

- 本 attempt 在科研内容上仅接触 P083 PDF；不接触其他论文或任何既有综合结论。
- 禁止读取 P083 的 `read_1`、任何旧读稿或其他 read attempt。
- 禁止读取任何其他 Paper/Failure/Operator Card、Evidence、饱和审计、Candidate、calibration/blind 材料。
- 禁止联网、搜索网页、调用外部 API 或使用外部论文内容补充判断。
- 不生成 Candidate，不进行或模拟科研 Reviewer 三审，不执行 novelty/prior-work 审查。
- 除本 attempt 的 `invocation.md` 与 `report.md` 外，不写其他文件。

## Required report scope

- changed computation，但以 Failure、threat model 与 measurement 为优先。
- 输入、输出、信息可见性与时点。
- 实验设置与强基线。
- 预算、模型与 oracle 边界。
- Failure、限制与威胁。
- 可复核的物理 PDF 页码定位。
- 是否准入与是否建议第三读。
- 不从有限 defense 结果外推或生成“已验证 Operator”。

## Model and run provenance

- executor: OpenAI Codex agent，系统仅暴露其“based on GPT-5”；精确部署模型版本/权重标识未暴露，故不作推断。
- agent_task: `/root/plan05_a3_second_read_search_safety`
- parent_task: `/root`
- execution_date: `2026-07-20`
- timezone: `Asia/Shanghai`
- cwd: `D:/Desktop/crl_judge/crl_agent_v3`
- network: 禁止且未使用。
- paid_or_external_api: 未使用。
- random_seed: 未设置；本任务不是随机实验。
- fixed_compute_or_token_budget: 未提供；不捏造。

