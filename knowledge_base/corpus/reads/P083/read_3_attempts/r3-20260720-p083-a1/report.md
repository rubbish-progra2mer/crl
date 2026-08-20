# P083 独立定向第三读报告

## 读取边界与来源

- 论文：*TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems*。
- 原始文件：`knowledge_base/staging/plan05_sat_a3/P083_tamas.pdf`。
- SHA-256：`4ad6d486003dc7268c80cdc2f49224a955792843d57155915d5f77889f7f7bdd`。
- 已逐页读取 PDF 物理页 1–31，包括正文、威胁形式化、数据集设计、指标、人工复核、置信区间、完整防御表、案例和 judge/monitor prompts。
- 本报告是 fresh third reader 在 procedural blinding 下的独立判断；未联网，未读取任何既有读审、调和、Cards、Evidence、审计、Candidate、calibration 或 blind 材料。

## 结论先行

TAMAS 对多代理系统的攻击面和失败现象提供了有用的结构化覆盖，尤其适合作为 Failure 证据：轻量 prompt/environment 注入会沿代理通信传播，单个被破坏代理可成为 weakest link，colluding/contradicting/Byzantine 行为会破坏协调。但它不是对真实工具部署风险的充分测量，也没有证明任何轻量防御是可靠的正向 Operator。

本篇建议：Failure/威胁覆盖 `准入`；防御 Operator `不准入`。分隔符、paraphrase、sandwich 和 monitor 可以作为“被测试但不稳定/破坏任务的失败基线”记录，不能作为已证实有效的防御机制向下游迁移。

## 三层 threat taxonomy 核对

### 高层三攻击面

- Prompt level（PDF 物理页 3–4）：DPI 直接把恶意指令拼入用户请求；Impersonation 在用户请求中添加虚假的权威身份。
- Environment level（PDF 物理页 4）：IPI 把恶意指令注入工具/外部来源返回的 observation。
- Agent level（PDF 物理页 4–5）：通过修改一个或多个代理的 system prompt，构造 Byzantine、Colluding、Contradicting 行为。

这一三面划分可作为实用的攻击入口索引，但不是严格互斥、同粒度的 taxonomy：

- PDF 物理页 16 的 Table 5 又把 Byzantine 标为 “Agent-level”，把 Colluding 与 Contradicting 标为独立的 “Multi-agent level”，实际形成四级标签，而非始终一致的三层。
- DPI/IPI 的成功条件主要是恶意工具调用；Byzantine/Contradicting 可用 misleading output、harmful output 或 task failure；Colluding 要求协调恶意结果。不同类别混合了注入位置、攻击者控制面和结果类型，难以把跨类 ARIA 差异直接解释为“哪一层更危险”。
- DPI 与 IPI 在构造中还会把 attack-specific tool 追加到工具集（PDF 物理页 4）；因此测到的是“恶意指令 + 可直接调用的模拟恶意工具”的联合脆弱性，不只是纯文本隔离失败。

故 taxonomy 可准入为覆盖框架，不应被当作完备、互斥或强因果的安全分层。

## 模拟工具与样本规模边界

### 数据与工具事实

- PDF 物理页 1、5、14：五个场景，每个场景 4 个代理；每种攻击在每场景 10 个样本，共 6×5×10=300 个 adversarial instances；每场景 20 个 harmless tasks，共 100 个。
- PDF 物理页 13–15：所有工具都是 simulated tools，返回受控字符串，不调用真实 API；数据/攻击工具由 ChatGPT 辅助生成，再由人工检查与修改。
- PDF 物理页 15：每个攻击类型实际只有 50 个实例。作者称这样兼顾变化与评测成本。

### 外推限制

- 模拟工具可以测试“代理是否选择调用恶意工具”及消息传播，却不覆盖真实 API 的鉴权、权限边界、确认流程、状态依赖、失败恢复、速率限制、网络内容、持久副作用和审计机制。
- 恶意工具通常直接返回“成功”字符串；ARIA-4 对 DPI/IPI/Impersonation 很大程度由工具调用日志判定（PDF 物理页 16）。这证明模型会选择危险动作，不等价于真实系统中攻击已成功造成损害。
- 50 个样本/攻击由五个手工场景和高度结构化模板组成，模型与配置复用同一小套任务。10,000 次 Dirichlet-smoothed bootstrap（PDF 物理页 17、20–22）只能描述这套样本上的不确定性，不能创造新的攻击多样性或真实部署覆盖。
- 没有给出多次独立 LLM rollout、API snapshot 版本、随机种子或跨时复验。温度 0 也不能保证闭源 API 的严格确定性。

因此可接受的证据边界是“在受控模拟环境中，当前多代理框架经常选择危险工具或被恶意代理扰乱”；不可外推为真实部署攻击成功率。

## LLM judge 与指标边界

- PDF 物理页 6、16：DPI、IPI、Impersonation 等攻击的 ARIA-4 可由工具调用解析；需要语义判断的轨迹使用 GPT-4o、temperature 0.0 作为 LLM judge。
- PDF 物理页 16：人工验证只覆盖 120 条“representative logs”。两名标注者独立标注、第三人裁决；Cohen’s kappa=0.77。LLM judge 平均 macro-F1=89.13%，但 Byzantine 仅 79.17%，Contradicting 仅 74.85%。这两个恰是多代理交互特有、也是论文核心主张最依赖的类别。
- PDF 物理页 28–30：judge prompt 对不同攻击使用不同标签和归因条件；Byzantine/Contradicting 要求判断失败是否由指定恶意代理引起。这是高难度因果归因，现有 74.85%–79.17% F1 留下实质测量误差。
- 人工样本如何在模型、框架、攻击、领域间分层抽取没有充分说明，120 条也只覆盖全部轨迹的一小部分；不能把 89.13% 平均值视为无误差 oracle。
- PDF 物理页 16：PNA 只计算 benign task 中“required tools 被正确调用的比例”，不检查最终语义质量、参数正确性、真实副作用或用户目标是否真正完成。
- PDF 物理页 17：Safety Score 使用自定义 A1/A2/A3/A4 权重，再按每个攻击 min-max 到 [0,100]；ERS 再与 PNA 作 harmonic mean。min-max 使安全分数依赖当前被比较系统集合，ERS 不是稳定的绝对安全量尺。

因此 ARIA/ERS 适合 benchmark 内部诊断，不应作为精确、跨研究可直接比较的绝对安全率。

## 轻量防御是否有效

防御只在最脆弱的 AutoGen RoundRobin 配置、五个代表性开源模型上测试（PDF 物理页 7–8），没有覆盖闭源模型、其他 AutoGen 配置或 CrewAI。结果不支持“有效且稳定”的正向结论。

### DPI 与 impersonation

- PDF 物理页 18，Table 8：DPI delimiter 的平均 ASR 仅从 88.4 降至 83.2，即 -5.2 点；Llama-3.1-8B 反而由 88 升至 92。
- PDF 物理页 17–18：paraphrasing 虽在 94% 样本中移除了 injected instruction，却在 48% 样本中也删掉至少一个原始子任务或信息。因此看似防御成功的一大部分是 task destruction，不是既安全又保用的净改进。
- PDF 物理页 18：Impersonation 的 apparent success 同样常因恶意指令被整个移除、查询变成另一个 benign task；论文自己承认这不等于 robust mitigation。

### IPI

- PDF 物理页 19，Table 9：tool-output delimiter 的平均 ASR 从 75.2 降至 64.0，sandwich 降至 65.2。
- 但 DeepSeek-R1-32B 从 74 恶化为 92/80，Mixtral 从 74 恶化为 88/82；平均收益主要来自 Qwen/Llama，跨模型方向不一致。

### 交互攻击 monitor

- PDF 物理页 8、18–19：Gemma3-12B monitor 周期检查 trace，但经常误报终止 benign/可继续执行，并出现同一轨迹前一时刻判“停”、下一时刻又判“继续”的时序摇摆。
- Table 10 主要报告 stop/检测结果，没有把 attack residual、benign false-positive、PNA 损失、额外 token/延迟和监控成本统一成可比较的防御效用。

论文 Limitations 也明确说研究主要 benchmark attacks，防御评估有限且非全面（PDF 物理页 9）。因此轻量防御应被解读为负面/混合结果，而不是可复用的成功 Operator。

## 预算、oracle 与公平性

- 论文横跨 10 个 backbone、5 个配置和 400 个任务，但没有给出总 API 调用数、token、费用、wall-clock、硬件、重复次数或完整运行预算。
- PDF 物理页 7–8：CrewAI 因兼容性不含 Gemini，因 API credits 不含 GPT-4；因此模型×框架矩阵不完整，框架安全均值并非完全同配比较。
- 防御实验只挑 RoundRobin 和五个开源模型，且额外使用 Gemma3-12B 做 paraphrase/monitor；没有报告该额外模型的 runtime/cost，也没有把它对 benign utility 的损失完整计入。
- 攻击成功既有 tool-log 规则，也有 GPT-4o judge；这是可扩展评估方案，不是 gold oracle。尤其交互攻击 judge 的有限 F1 应随结论一起传播。
- 防御表未报告置信区间、显著性或多次 rollout；原始 attack 结果虽给 bootstrap CI，但小样本和重复模板仍限制其解释。

## 争议结论与可接受表述

| 论文式结论 | 第三读裁决 |
|---|---|
| 三层 taxonomy 系统覆盖多代理攻击 | 可作高层索引；实际 Table 5 使用四级标签且成功条件异质，不是严格互斥 taxonomy。 |
| 多代理系统高度易受攻击 | 在 300 个受控模拟实例上有强 Failure 证据；真实工具成功率与部署外推未被建立。 |
| 跨模型/框架比较揭示架构影响 | 有诊断价值，但存在缺失模型×框架单元、小样本、单次 rollout 和相对归一化边界。 |
| lightweight defenses 能降低攻击 | 只能说某些模型/攻击上平均 ASR 下降；效果小、方向不一致，且 paraphrase 严重损害任务。 |
| monitor 是交互攻击防御 | 不支持为有效 Operator；误报和时序不稳定，缺少安全—效用—成本的闭环评估。 |

## 准入建议

- Failure 证据：`准入`。可提取 prompt/environment/compromised-agent 三类入口，以及消息传播、weakest-link、collusion/contradiction/Byzantine 协调失败；必须附 simulated tools、每攻击 50 样本和 judge 误差边界。
- 防御 Operator：`不准入`。delimiter、sandwich、paraphrase、monitor 只可记录为失败或不稳定 comparator，不得写成“有效防御”。
- 指标 Operator：`不建议正向准入`。ARIA 可作局部标注框架；ERS 因 attack-specific success、judge 误差、PNA 代理和 cohort-relative min-max，不宜作为跨系统绝对鲁棒性 operator。
- 总体裁决：`FAILURE_ONLY_ADMISSION`。论文适合沉淀威胁/失败知识，不足以提供经验证的轻量防御 Operator。

