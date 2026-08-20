# P077 独立二读调用记录

- attempt：`r2-20260720-p077-a1`
- 运行日期与时区：2026-07-20，Asia/Shanghai
- 执行上下文：Codex 子任务 `/root/plan05_a3_second_read_learning`
- 模型 provenance：OpenAI Codex，基础模型系列 GPT-5；当前运行接口未暴露更细的模型快照、构建号或采样参数，因此不作猜测。
- 源 PDF：`knowledge_base/staging/plan05_sat_a3/P077_archer.pdf`
- PDF 字节数：4,197,709
- PDF SHA-256：`9A25030A872732DC5FC544E04E3D20382BE1D512EEEFD97E7E92179DD2C5F8EC`

## 任务

逐页阅读全文，独立完成第二读报告。报告必须分别说明 changed computation、输入输出/信息/时点、实验与强基线、预算/模型/oracle 边界、Failure/限制、物理页码定位、是否准入、是否建议第三读。仅写本 attempt 的 `report.md`，不生成 Candidate，不执行科研 Reviewer 三审。

## 允许输入

1. 上述 SHA-256 对应的 P077 原始 PDF 字节及其逐页视觉/文本内容。
2. 用户在本轮直接给出的 PLAN_05 二读任务、文件路径和盲法边界。
3. 工作区根 `AGENTS.md`、`crl_agent_v3/AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`，以及 PDF/编码技能说明；这些只提供程序性规范，不提供论文结论。
4. 本 attempt 内由本次运行新建的 `invocation.md` 与待写的 `report.md`。

## Procedural blinding 边界

这是内容层独立二读：科研判断只能来自指定原始 PDF，不接受任何既有综合、卡片、证据、候选、审计或他人读稿。项目与技能文档仅用于约束执行、编码和来源追溯，不得作为论文内容证据。允许本地工具对指定 PDF 做逐页文本提取、页面渲染、页数和哈希核对，但工具输出只用于辅助定位，不能替代逐页阅读与视觉核对。

## 明确禁止

- 不联网，不搜索或调用外部 API。
- 不读取 `read_1`、任何其他 read attempt、任何 Card、Evidence、饱和审计、Candidate、calibration/blind 材料或旧读稿。
- 不读取未被列入允许输入的论文或知识库内容。
- 不生成 Candidate，不做 novelty/prior-work 审查，不调用或模拟科研 Reviewer 三审或 Commissioning Cycle。
- 不写入本 attempt 的 `invocation.md`、`report.md` 之外的任何文件。

