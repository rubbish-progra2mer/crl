# P038 Codex 首读：AgentDojo

- 状态：`DRAFT_BEFORE_SECOND_READ`
- PDF：`knowledge_base/staging/papers/P038_agentdojo.pdf`
- PDF SHA-256：`26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913`
- 读取范围：正文（pp.1–10）及实验置信区间、attack/defense 设置。

## Changed evaluation / mechanism

- [AUTHOR_FACT] 97 个正常任务与 629 个 security cases 在真实可变环境状态上分别计算 utility 与 attacker goal；恶意指令通过 tool-returned untrusted data 注入。
- [AUTHOR_FACT] tool filtering 在读取不可信数据前先限制本任务允许的工具集合，使攻击能看到的数据与可执行副作用分离。
- [CODEX_SYNTHESIS] 安全机制的本质不是提示模型“忽略恶意文本”，而是提前缩小被不可信数据影响后仍能造成的 action authority。

## 关键结果

- benign utility 最高也低于约 66%；攻击可使多数模型 utility 绝对下降 10–25%。
- 更有能力的模型更能完成 attacker goal，形成 utility/targeted-ASR 的逆向关系；低 ASR 不能脱离正常 utility 解读。
- 简单 tool filter 把 GPT-4o targeted ASR 降到 7.5%，但若正常任务与攻击需要同一工具（17% test cases）或工具无法预先规划，就会失败。
- prompt-injection detector false positive 较多并显著伤害 utility；重复用户 prompt 对当前攻击有效，但作者明确预计 adaptive attack 可绕过。

## 边界

- 主要攻击较简单且非完全 adaptive；cross-product cases 不等于真实攻击分布。
- 每个模型使用 provider 推荐 prompt，严格说并非完全相同 scaffold；同时这是必要兼容处理，二读须保留该事实。
- deterministic state checks 比 LLM judge 更适合该攻击场景，但人工定义 utility/security function 限制扩展性。

## Evidence 草案

| Evidence ID | kind | section / page | locator | Codex note |
|---|---|---|---|---|
| P038-E01 | evaluation | §3, pp.3–6 | state utility/security | [AUTHOR_FACT] utility 与 attack goal 双轴。 |
| P038-E02 | mechanism | §4.3, pp.8–9 | tool filtering | [AUTHOR_FACT] 预先限制 action authority。 |
| P038-E03 | limitation | §4.3–5, pp.9–10 | shared-tool/adaptive | [AUTHOR_FACT] tool isolation 的失败边界。 |

## Card 草案（不进入正式 Cards）

### Operator — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Pre-Exposure Tool-Authority Minimization`
- Baseline：把所有读写工具持续暴露给同一受不可信文本影响的 planner。
- Changed computation：在读取 untrusted content 前，依据用户任务确定最小工具权限；后续文本不能扩张该 action set。
- 前提：所需工具可提前确定；utility 与 ASR 联合报告；shared-tool attacks 另行处理。

### Failure — `DRAFT_BEFORE_SECOND_READ`

- 名称：`Security Gain by Utility Collapse`
- 现象：系统因不会完成正常工具链而表现出低攻击成功率，或 detector 通过高误报终止正常任务。
- 约束：安全 Candidate 必须同时比较 benign utility、utility-under-attack 与 targeted ASR。

## 首读裁决

`KEEP_FOR_SECOND_READ`。作为 text/tool Agent safety 的核心机制与公平评价来源。
