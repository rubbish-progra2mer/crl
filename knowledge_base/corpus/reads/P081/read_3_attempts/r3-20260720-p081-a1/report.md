# P081 独立定向三读报告

## 读取与来源

- 论文：*Self-Consistency Improves Chain of Thought Reasoning in Language Models*。
- 来源：`knowledge_base/staging/plan05_sat_a3/P081_self_consistency.pdf`。
- SHA-256：`1a49ce0373afc89d2d6e97fb1aa8230f6b818c70590d732a3187f753f4df6aba`（读取前本地复核一致）。
- 阅读范围：物理页 1–24，逐页阅读全文；未联网，遵守 `procedural_blinding`。

## Changed computation 核对

方法没有训练、微调或辅助 verifier。对同一 few-shot CoT prompt，从同一个 LM 独立采样 `m` 条 `(reasoning path, final answer)`，用任务相关 parser 抽取 final answer，再对答案做不加权多数投票；reasoning path 被边缘化（物理页 2–3）。主实验每个 run 采 40 个输出，并对 10 个 run 取结果统计（物理页 5）。因此 changed computation 是“单路径 greedy decode”变成“多路径随机采样 + 离散答案聚合”，而不是提高单条 reasoning path 的生成概率或验证其推理正确性。

加权聚合消融显示，长度归一化概率加权与多数投票接近，而未归一化权重明显较差；作者自己指出不同路径的归一化概率很接近，模型不能良好区分正确与错误解（物理页 3）。所以收益证据支持的是 answer-frequency aggregation，不支持模型概率已校准或多数路径各自逻辑可靠。

## 等样本 baseline 与预算公平性

主表的 CoT baseline 是一次 greedy decode，而 self-consistency 使用 40 条路径（物理页 5）。其大幅准确率增益证明“用更多独立推理样本并投票能提高准确率”，但不是等推理样本、等 token、等 FLOP 或等 wall-clock 的 decoding 优势。论文在结论中也承认额外计算成本，并建议 5 或 10 条路径作为折中（物理页 9）。

论文确实提供三类更公平的样本数对照：

- sample-and-rank 与 self-consistency 使用相同数量的采样序列，self-consistency 更强（物理页 7，图 3）；
- beam search 与 self-consistency 对齐 beam/path 数，sampling self-consistency 更强（物理页 7，表 6）；
- 40 次 prompt permutation、40 组 prompt 与 40-path self-consistency 对齐输出次数，后者更强（物理页 17–18，表 11）。

这些对照能支持“在相同输出条数下，按答案频次聚合优于所列排序/ensemble 方案”，但仍未严格对齐生成 token 数：不同策略、不同 reasoning path 的长度可变，beam search 与独立 sampling 的 KV/cache 和搜索成本也不同。资源报告只给出硬件和每任务约 1–12 小时、部分任务不超过两天的粗粒度范围，没有逐方法 wall-clock、token 或能耗分解（物理页 18）。因此公平预算的最强可接受口径是“相同候选条数”，不能再升级为“相同计算”。

## Parser 与开放答案边界

形式化假设答案来自固定集合 `A`（物理页 3）。算术任务的 parser 抽取模型生成 “The answer is ” 后的第一个数；commonsense 任务抽取该短语后的完整字符串（物理页 3 脚注）。生成输出在下一个 `Q:` 前截断；GPT-3 统一设 128 max tokens（物理页 18）。这些格式化 prompt 与 task-dependent parser 是方法的实际组成部分。

论文明确限定 self-consistency 只能直接用于最终答案属于固定集合的问题；开放文本只有在另行定义良好的一致性度量（例如语义同意/矛盾）后才“原则上可扩展”（物理页 4）。本文没有实现语义聚类、同义归并或开放答案一致性判定。虽然物理页 6 报告了 HotpotQA EM/F1，附录给出自由字符串式 HotpotQA exemplars（物理页 20），但论文没有说明多数投票时如何合并拼写差异、别名、同义答案或部分重叠答案。因此这些开放答案结果不足以确立一般开放文本 self-consistency。

“entirely unsupervised”也需按窄义理解：它不训练额外模型、不新增标注数据，但仍使用人工撰写的 CoT exemplars、任务相关输出格式和 parser（物理页 2–4）。这不是无需人工规格的通用聚合器。

## 争议结论

1. “self-consistency 优于 greedy CoT”作为准确率事实成立，但主结果同时增加约 40 倍候选路径预算，不能解释为等预算算法优势。
2. “self-consistency 优于 sample-and-rank/beam/prompt ensemble”在相同候选数对照下有直接证据；未对齐 token 与 wall-clock，故只能接受候选数公平。
3. “可用于开放文本生成”在本文中只是未来扩展设想；固定答案集合和 parser 是当前方法边界。
4. consistency 与 accuracy 的相关性（物理页 8）不等于校准保证；正文同时承认模型会生成错误、荒谬或事实不准的 reasoning path（物理页 9–10）。

## 准入裁决

**有限准入。** 准入：（a）固定答案任务上的多路径采样与多数投票 changed computation；（b）40-path 相对单次 greedy 的准确率增益，但必须标注额外推理预算；（c）与 sample-and-rank、beam、40-output prompt ensemble 的等候选数优势。拒绝准入：（a）等 token/FLOP/wall-clock 优势；（b）无需 parser 的通用方法；（c）一般开放答案或开放文本生成已被验证；（d）把“无额外训练”表述为“无需人工 prompt/parser 规格”。

