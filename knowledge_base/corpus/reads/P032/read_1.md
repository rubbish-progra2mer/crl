# P032 Codex 首读：CRITIC

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P032_critic.pdf`
- PDF SHA-256：`30a3161dbbb9531528bf410bd1df84eeb9ada8151f614789ae80ca86b7b32c7e`
- 读取范围：方法与主实验（pp.1–9）、限制（p.21）、self-verification、error/cost analysis（pp.24–28）。

## Changed computation

- [AUTHOR_FACT] 初始回答后，模型调用任务相关外部工具生成 critique，再把初始输出与 critique 共同用于修正；可迭代并在 critique 判断正确时停止。
- [CODEX_SYNTHESIS] 核心不是“多想一轮”，而是让可执行外部观测进入 correction computation；纯 self-critique 是关键对照。

## 结果、基线与公平性

- QA、数学程序合成、toxicity reduction 分别使用 web、Python interpreter、Perspective API；工具在任务前预指定。
- 在数学程序合成中，ChatGPT+CRITIC 相对 PoT 在 GSM8K / SVAMP / TabMWP 为 +5.7 / +1.3 / +14.0；移除 interpreter 后分别为 +4.5 / +0.0 / +12.0。text-davinci-003 的无工具版本在 GSM8K 和 SVAMP 可下降 1.8 与 3.3。
- 自校验 AUROC/accuracy 低于带工具 critique；HotpotQA 100 例中 hallucination 从 CoT 36% 降至 7%，但仍有 incorrect correction、refusal 与 reasoning error。
- GSM8K 中，初始错误样本可修正 32.2%；原本正确样本仍有约 4.3% 被改坏。收益不能写成单调或无风险。
- 多轮推理时延随迭代近似线性增加；论文没有 token/cost-matched 单次生成对照，且不同任务的 feedback oracle 强度差异大。

## 失败边界

- 工具必须对目标 claim 提供可靠且相关的观测；工具错误、偏置或评价代理偏离会把 correction 导向错误方向。
- 手工 demonstrations、任务预设工具与停止规则带来 scaffold 优势；外推到开放 Agent 需要先证明 feedback availability。
- oracle 版本只在已知错误时修正，不能作为可部署主结果。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P032-E01 | mechanism | §2, pp.3–5 | Algorithm 1 | [AUTHOR_FACT] 工具观测驱动 critique/correction。 |
| P032-E02 | negative_result | §4.2, pp.7–8 | Table 2 | [AUTHOR_FACT] 无工具自修正不稳定。 |
| P032-E03 | failure | App. D.2, pp.25–26 | error analysis | [AUTHOR_FACT] 正确答案也会被改坏。 |
| P032-E04 | limitation | App. A, p.21 | latency/prompt | [AUTHOR_FACT] 迭代时延与 prompt dependency。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Externally Grounded Critique-and-Correction`
- Baseline：同一模型依据自身已有输出继续反思或直接重采样。
- Changed computation：把可执行工具返回的任务相关观测显式写入 critique，并用 critique 条件化下一次生成。
- 前提：工具独立于被评输出；反馈能定位错误；额外调用与 token 被公平计价；修正可回归验证。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Ungrounded Self-Critique Amplifies Wrong Feedback`
- 现象：模型无法可靠识别细微错误，生成貌似具体但错误的 feedback，随后忠实地把正确输出改坏。
- 未否定：强 verifier、可执行测试或独立证据可让同一 refinement loop 有效。

## 首读裁决

`KEEP_FOR_SECOND_READ`。作为 grounded reflection 的祖先 Operator 与 ungrounded refinement Failure 的共同来源。
