<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p097","card_kind":"paper","paper_id":"P097","evidence_ids":["ev-p097-feasibility-gap","ev-p097-behavioral-perturbation"],"source_refs":[{"path":"papers/P097_reloop.pdf","sha256":"8563653b872e78822f024b4d2f11532f75354e98c729ed26ac5bbf9675724c66"}]} -->
# ReLoop: Structured Modeling and Behavioral Verification

## Role in the knowledge base
[CODEX_SYNTHESIS] solver 反馈验证路线的重要最近工作，提供“solver feedback catches syntax errors, not missing constraints”的引语锚和 90 个百分点 gap 的定义性量化。

## Problem and setting
[AUTHOR_FACT] silent failures：执行成功且 solver-feasible 的代码编码语义错误形式化——91.1% Exec vs 0.5% Acc。[[evidence:ev-p097-feasibility-gap]]

## Changed computation
[AUTHOR_FACT] 无训练干预两件套：四阶段结构化生成（单次调用内 understand/formalize/synthesize/verify）+ L1 执行验证（IIS/unbounded ray 诊断再生成 ≤3）+ L2 行为扰动测试（非阻断、分级阈值、保守修复+回滚）。[[evidence:ev-p097-behavioral-perturbation]]（L1/L2 参数细节出自 §3.2–3.4/App.E，PDF 直核；所绑引文锚定核心机制）

## Evidence-backed findings
[CODEX_SYNTHESIS] 消融链一致：+CoT 是组合问题主驱动（Claude +8.5pp）；L2 局部缺陷域最大单项（MAMO +4.4pp）、结构域零贡献；CoT 使 DeepSeek 执行崩塌 91.1→53.2、毁 SFT 模型（84 崩+65 回归）；IndustryOR 可修复带空洞双峰（34%<1% + 47%>10%）；修复 LLM 伪造数据实录。

## Limitations and failure signals
[CODEX_SYNTHESIS] 三重证据软肋（reconciliation）：重试预算混杂（~3× token 无等预算对照）、跨基准 Base 引用自 SIRL（harness 对齐未描述）、single-run 无误差条——增益按方向引用；RetailOpt prompt 自带与参考 MILP 同源脚手架（绝对值不外推无脚手架场景）；L2 与生成共享 LLM。

## Lineage and baselines
[CODEX_SYNTHESIS] 与 P096（LLM 裁决探针）、P098（探针作训练信号）共同构成认证侧三类近邻。

## Evidence ledger
[CODEX_SYNTHESIS] gap 量化与扰动机制绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] ReLoop; structured generation; four-stage reasoning chain; behavioral verification; silent failure; feasibility correctness gap; diagnostic execution recovery; RetailOpt-190; structured generation with behavioral verification; silent failures in optimization code; perturbation testing of formulations
