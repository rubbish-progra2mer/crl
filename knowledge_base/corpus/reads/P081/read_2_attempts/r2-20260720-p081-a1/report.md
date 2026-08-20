# P081 独立二读报告：Self-Consistency

## 阅读与来源状态

- 已逐页阅读指定 PDF 的全部 24 个物理页，包括正文、参考文献、资源说明、消融、样例和完整 prompts。
- 源 PDF SHA-256：`1A49CE0373AFC89D2D6E97FB1AA8230F6B818C70590D732A3187F753F4DF6ABA`。
- 本报告页码均为 PDF 物理页。

## Changed computation

Self-consistency 只改变测试时解码与聚合，不训练或微调模型。给定与普通 chain-of-thought 相同的 few-shot prompt 和问题，它不取单条 greedy reasoning path，而是从同一模型独立采样多条 `(reasoning path, final answer)`；随后把 reasoning path 当潜变量边缘化，对解析出的 final answer 做无权多数票，返回最一致答案。（物理页 1–3）

作者同时比较了按整段生成概率加权的聚合。长度归一化 weighted sum 与多数票接近，但未归一化权重明显较差；按每个答案的平均生成概率排序更差。最终采用多数票的理由不是它能判断推理正确性，而是多个多样路径对同一最终答案的重复支持提供了统计冗余。（物理页 3）

## 输入、输出、信息与时点

- 输入：人工编写的 CoT exemplars、当前问题以及标准语言模型上下文；所有模型均在 few-shot、无任务微调设置运行。（物理页 3–5）
- 中间输出：同一个模型在温度/top-k/nucleus sampling 下生成的多条完整 reasoning paths 和格式化 final answers。实验主设置每题采样 40 条，重复 10 runs 统计均值。（物理页 3–6）
- 聚合信息：只看可解析的最终答案是否相同；不读取 ground truth，不调用 verifier，不根据 reasoning 的事实性或逻辑正确性打分。任务相关 parser 从固定短语后的首个数字或完整字符串抽取答案。（物理页 3）
- 时点：全部额外计算发生在推理期。答案投票完成后才输出；训练权重、预训练数据和 exemplars 不因当前题更新。（物理页 1–4）
- oracle 边界：ground truth 只用于离线评测，不参与投票；没有外部搜索、计算器或人工评审 oracle。人工 CoT exemplars 是提示监督，固定答案集合与 parser 是可用的任务结构。（物理页 3–5）

## 实验与强基线

模型覆盖 UL2-20B、LaMDA-137B、PaLM-540B，以及 GPT-3/Codex `code-davinci-001`、`code-davinci-002` 175B。任务覆盖 6 个算术、3 个 commonsense、2 个 OOD symbolic reasoning benchmark，另测 ANLI、e-SNLI、RTE、BoolQ、HotpotQA。（物理页 4–6）

主结果以 CoT greedy decode 为直接基线。代表性结果包括：PaLM-540B 在 GSM8K 56.5→74.4、AQuA 35.8→48.3、SVAMP 79.0→86.6；`code-davinci-002` 在 GSM8K 60.1→78.0、AQuA 39.8→52.0、SVAMP 75.8→86.8。commonsense/symbolic 上 `code-davinci-002` 的 StrategyQA 73.4→79.8、ARC-c 83.6→87.5、Letter(4) 70.4→73.4。（物理页 5）

强比较不止 greedy：

- Sample-and-rank 使用相同样本数并按 sequence log-probability 选一条，收益显著小于答案投票。（物理页 7）
- Beam search 在相同 beams/paths 下更差；即使把 beam outputs 再做 self-consistency，也因路径多样性不足而弱于 sampling。（物理页 7）
- 40 次 prompt-order permutation、3 套 prompt ensemble、多个模型 ensemble 均弱于单模型 40-path self-consistency；与不同 prompt/排列组合仅有小额附加收益。（物理页 7、16–18）
- 标准 prompting（无 rationale）用于检验 CoT 有害情形。ANLI-R1、e-SNLI、RTE 上 CoT 确有退化，而 self-consistency 超过无 rationale 基线；例如 e-SNLI 85.8/81.0/88.4 对应 standard/CoT/self-consistency。（物理页 6）
- 论文还列既有 task-specific SoTA，包括 GSM8K 的 GPT-3 175B 微调和额外 175B verifier；这些并非相同无训练预算，只适合背景比较。（物理页 5）

采样数消融表明 1、5、10、20、40 paths 通常随样本增加而提升并逐渐饱和；采样温度、top-k 与 nucleus 参数变化下趋势较稳健。增益随模型规模增强，小模型因为基础推理能力不足而收益有限。（物理页 6、8、16–17）

## 预算、模型与 oracle 边界

- 主结果每题 40 次完整生成，并平均 10 runs；因此报告准确率所对应的推理调用量远高于单次 CoT greedy。作者建议成本敏感时从 5 或 10 paths 起步，因为许多任务早期已获得多数增益。（物理页 5–6、9）
- UL2-20B：TPU v3 2x2（4 chips/8 cores）；LaMDA-137B：TPU v3 8x8（64 chips/128 cores）；PaLM-540B：TPU v4 4x4x12（192 chips/384 cores）；GPT-3 通过公开 API。约 1,000 examples 的单任务推理通常为 1–4 小时（UL2/LaMDA）或 2–12 小时（PaLM），部分 commonsense 任务更久但不超过 2 天。（物理页 18）
- GPT-3 各方法最大生成 128 tokens，不设 frequency/presence penalty；输出在下一段 `Q:` 开始处截断。采样参数主设为 UL2/LaMDA `T=0.5,k=40`，PaLM `T=0.7,k=40`，GPT-3 `T=0.7` 无 top-k。（物理页 4、18）
- 该方法没有 verifier 或 correctness oracle。多数票只能利用答案频率；当错误路径高度相关地聚到同一答案时，它会自信地错。所谓“consistency 可作 uncertainty estimate”来自 GSM8K 上一致率与准确率的经验相关，而不是校准保证。（物理页 8–9）

## Failure、限制与可迁移风险

1. 适用前提是最终答案可映射到固定/可规范化的答案集合。开放文本只有在另有可靠“两个回答是否一致”的度量时才可能扩展，而论文没有解决该度量。（物理页 4）
2. 成本按 paths 近似成倍增长；40-path、10-run 的论文设置不应与单次 greedy 在 latency、energy 或 API 费用上视作等预算。（物理页 5–6、9、18）
3. 多数票不验证 rationale。论文样例中正确答案可能伴随错误事实（例如 StrategyQA 人口数字不准），结论也明确承认会产生错误、荒谬或非事实 reasoning paths。（物理页 6、9、19）
4. 路径错误若相关而非独立，多采样只会放大错误共识；论文展示的是平均准确率收益，没有给出对系统性偏见、同一 prompt 诱发的共享错误或 tie-breaking 的完整机制保证。
5. 小模型或缺乏基础能力时收益弱；短 equation path 的可多样化空间小，增益也小。方法依赖“可产生多样且部分正确路径”的模型能力，而非普遍适用的错误修复器。（物理页 8、16）
6. exact parser 是隐藏的任务依赖：数值题从固定短语后取首个数字，commonsense 取完整字符串。格式漂移、单位等价、自由文本同义答案都可能改变投票桶。（物理页 3）
7. 论文使用的若干模型/engine 和当时 API 条件并非完全开放；LaMDA、PaLM 不公开，复现实验只能在 UL2/GPT-3 等部分边界进行。（物理页 10、18）

## 页码定位索引

- 方法图、latent path 与聚合公式：物理页 1–3。
- 任务、模型、prompt、采样参数：物理页 4–5。
- 主结果与 sampled-path 曲线：物理页 5–6。
- sample-and-rank、beam、prompt/model ensemble：物理页 7、16–18。
- robustness、imperfect prompt、consistency/accuracy：物理页 8、16–17。
- 限制、伦理与可复现性：物理页 9–10。
- 精确硬件、运行时间和解码长度：物理页 18。
- 生成样例与完整 prompts：物理页 18–24。

## 准入与第三读建议

- 准入判定：**准入**。changed computation 极其清楚，且同预算样本数下与 sample-and-rank/beam 的对照支持“答案层聚合而非只多采样”的贡献；成本、固定答案集、rationale 不可靠等边界也在原文中明确。准入仅表示可作为知识来源，不构成 Candidate 或 Reviewer 裁决。
- 第三读：**原则上不建议**。二读已能稳定界定其机制和主要边界；若后续要实际复现或用于开放文本，则再做定向第三读，重点只需核对 parser、无效输出、平票处理和等预算 latency/accuracy 曲线。

