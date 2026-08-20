# P008 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P008_agent_security_bench.pdf`
- PDF SHA-256：`e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9`
- 读取时间：`2026-07-19T17:25:00+08:00`
- 读取范围：逐页检查 1–36 页；正文 1–10 页，参考文献 11–15 页，攻击/防御形式化与实例 16–21 页，场景/工具/实验实现/metrics/prompts 22–29 页，补充攻击与防御结果 29–35 页，复现说明 36 页。

## Changed computation / evaluation object

- [AUTHOR_FACT] ASB 不是一个防御方法，而是把 Agent 的 system prompt、user prompt、tool observation、retrieved memory 四个信息入口分别对应 PoT backdoor、DPI、IPI、memory poisoning，并以 mixed attacks 组合测试。
- [AUTHOR_FACT] 攻击目标机械定义为 agent 是否调用指定 malicious tool；clean utility/PNA 定义为是否调用任务全部 labeled normal tools。工具是 JSONL 定义的 simulated objects，每次返回预设 output，而非真实外部系统。
- [READER_INTERPRETATION] 可迁移资产是“按信息进入时点分层的攻击面”与“攻击下行为/无攻击效用同时报告”；ASR/NRP 数值只对其工具调用代理指标成立，不应成为 CRL 的自动安全分数或现实伤害概率。

## 威胁模型、数据与基线

- attacker 不知道 backbone 内部，只经 API 使用；但可把攻击工具加入可用 tool list，并按攻击类型修改 user input/tool response、黑盒写入共享 memory，或作为第三方 prompt engineer 把后门 demonstrations 放进 system prompt。这是能力很强且各类攻击权限不同的 threat model。
- Benchmark 有 10 scenarios/agents、50 normal agent tasks、20 normal tools、400 attack tools/tasks；包含 aggressive 与 non-aggressive requests。每个 normal task 期望固定两步 tool workflow，降低了 task completion 判定难度。
- 13 个 backbone 运行于 AIOS Agent；memory 用 Chroma，memory poisoning 由 GPT-4o-mini 生成 DPI 内容；PoT 只选择 5 个 agent，每个用 2 个 demonstration tasks 与 2 个不同 testing tasks，证据样本结构远小于主攻击表的表面规模。
- Refusal 由另一个 LLM 按 prompt 自动判断；PNA/ASR 只看所需或攻击工具是否被调用，不检查 tool arguments、最终输出正确性或实际副作用。PNA 不是一般 task accuracy。
- 论文没有设置独立于现有 defenses 的强训练式安全 baseline；防御主要是 delimiter、paraphrase、instruction/sandwich prompts、dynamic rewriting、shuffle、PPL/LLM detector。

## 主要结果与定位

- Table 5 跨模型平均 ASR：DPI 72.68%、IPI 27.55%、memory poisoning 7.92%、mixed(DPI+IPI+MP) 84.30%、PoT 42.12%。最高的 84.30% 指攻击者同时控制多个入口且可加入攻击工具，不是单一远程 injection 成功率。
- 同一模型差异大：GPT-4o DPI/IPI/MP/mixed/PoT 为 60.35/62.45/10.00/89.25/100%；GPT-3.5 为 98.40/55.10/9.30/99.75/8.25。能力与 ASR 非单调，弱模型低 ASR 可能只是无法完成任何 tool task。
- NRP=`PNA*(1-ASR)` 把 clean labeled-tool completion 与平均攻击 tool-call 乘在一起；Table 6 中 Claude 43.56、LLaMA3-70B 30.03、GPT-4o 28.12。该排序依赖攻击混合权重与两个粗代理指标，只能作为本文汇总，不作为自动选模型依据。
- DPI defenses（Table 7）：delimiter 平均 ASR 78.38→79.08（变差），instruction prevention 76.77，paraphrase 56.87，dynamic rewriting 44.45；GPT-4o 上多种防御反而高于原 DPI 55.50。
- IPI defenses（Table 8）：delimiter 27.98→24.96、instruction 26.31、sandwich 28.04，平均改善很小且 sandwich 略变差。
- Table 19 无攻击效用：平均 PNA 29.46，delimiter/paraphrase/instruction/sandwich/DPR 为 22.52/27.69/26.63/28.29/26.38；多数防御有 utility cost，但模型级有正负变化。
- memory detector：LLM-based 平均 FNR/FPR 0.660/0.200；PPL threshold 无法同时压低两者。PoT paraphrase 将平均 ASR 42.12→29.06，shuffle 却升到 44.37。

## 失败边界与限制

- [AUTHOR_FACT] memory poisoning 是五类中最低 ASR（7.92%）；不能因论文同时研究 memory 就断言普通 RAG memory 广泛易被其攻击成功。
- [AUTHOR_FACT] 防御不具单调性：delimiter 对 DPI、sandwich 对 IPI、shuffle 对 PoT 的平均 ASR 可升高；简单 prompt 包裹不能隔离语义指令。
- [AUTHOR_FACT] aggressive tasks 的 DPI/IPI/MP average ASR 33.12，低于 non-aggressive 38.98，同时 refuse 8.31 vs 4.87；拒绝安全机制会改变攻击测量，低 ASR 不全是精确区分攻击。
- [AUTHOR_FACT] PoT trigger 的接近 100% 补充结果（Table 15）只针对 GPT-4o 与所选 PoT 设置；主 Table 5 跨 13 模型平均仅 42.12%。两者不可互相替代。
- [READER_INTERPRETATION] “成功调用 malicious tool”不验证实际数据擦除/泄漏，工具输出固定；ASR 是控制流劫持 proxy。相反，正常 PNA 只调用全部 labeled tools也可能参数错误或输出错误。
- [READER_INTERPRETATION] DPI 等设置同时把 malicious instruction 与 malicious tool 加入可用列表；现实可行性取决于平台是否允许第三方注册/注入工具。若 tool allowlist 受信，结果不会原样迁移。
- [READER_INTERPRETATION] system prompt backdoor 攻击假设第三方 prompt engineer 能修改部署 prompt；这是供应链/配置威胁，不是外部用户仅靠 trigger 可先植入后门。
- [READER_INTERPRETATION] 10 场景含超出本 CRL 范围的 autonomous driving 等载体；Pilot 只抽取文本 Agent 跨入口安全机制与测量边界，不把载体本身计入覆盖。

## 可抽取候选（尚非正式 Card）

- Evaluation Operator：`Information-Entry-Point Threat Decomposition`——分别在 system/user/tool-observation/retrieved-memory 时点注入，并保留攻击者权限与可用工具条件。
- Evaluation Operator：`Joint Clean-Utility and Attack-Action Reporting`——攻击结果与无攻击任务完成并列，避免把不会用工具的弱模型误判为安全；不采用本文 NRP 自动总分。
- Failure：`Prompt-Only Defense Non-Monotonicity`——delimiter/sandwich/shuffle 等可不降反升 ASR，且常损害 clean PNA。
- Failure：`Tool-Invocation Proxy Overstates End-to-End Harm/Utility`——恶意/正常工具被调用不等于参数正确、输出正确或真实副作用发生。
- Failure：`Cross-Run Memory Poisoning under Shared Writable Retrieval`——只有在攻击者能借 DPI/IPI 将恶意计划写入共享 Chroma 且后续相似检索命中时才成立；本文平均 ASR 较低。

## 未解决问题

- `[OPEN_QUESTION]` 每项主 ASR 的重复次数、置信区间和随机种子未在正文表中完整披露。
- `[OPEN_QUESTION]` proprietary model 参数规模来自外部估计且不可核验；本文安全结论不应依赖 Table 13 的规模数。
- `[OPEN_QUESTION]` LLM refusal judge 与人工标注的一致率未报告。
- `[OPEN_QUESTION]` 若移除 attack tool 注入权限、验证真实 tool arguments/side effects，攻击排序是否保持，本文未测。
