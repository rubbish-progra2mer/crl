# P082 独立定向三读报告

## 读取与来源

- 论文：*Toolformer: Language Models Can Teach Themselves to Use Tools*。
- 来源：`knowledge_base/staging/plan05_sat_a3/P082_toolformer.pdf`。
- SHA-256：`6d7483d94653008e40c2058a1c22441c92e3713dae278b6361e8efc447c99522`（读取前本地复核一致）。
- 阅读范围：物理页 1–17，逐页阅读全文；未联网，遵守 `procedural_blinding`。

## Changed computation 与 future-token hindsight

Toolformer 的核心不是在线 RL，而是离线自举造数后做标准 LM fine-tuning。给定原始文本 `x` 和少量人工 API 示范，基础 LM 先在候选位置生成 API call；工具执行得到结果；随后比较加入“call+result”与“不调用/只给 call 无 result”时，模型对位置 `i` 之后原始 token `x_i…x_n` 的加权交叉熵，只保留 future-token loss 至少下降 `τ_f` 的调用，再把保留调用插回文本形成 `C*` 并训练 LM（物理页 2–4）。

这是一种明确的 hindsight 标签：筛选器在造数时使用调用之后已经存在的真实 future tokens 来判断该调用是否“有用”。调用候选生成流程也并非完全等同推理期因果信息；附录对 MT 明说“during data generation the model can look ahead”，并专门删除把调用后才出现的文本作为 MT 输入的样本，因为推理时做不到（物理页 15）。该防护只对 MT 的一种泄漏模式有明文说明，本文没有证明其他 API 的候选/参数生成完全不利用原文后缀。故可接受的机制表述是“用离线 future-token predictability 产生工具调用监督，再期望其泛化到因果推理时”，不能表述为模型在无 hindsight 条件下自行发现真实任务效用。

筛选目标也不是答案正确性、事实性或任务回报，而只是后续 token NLL。无关但能降低 perplexity 的调用可以保留；正文给出 “Fast train success” 搜索结果无关却仍降低损失的例子，并认为噪声有时会迫使模型不要盲从工具（物理页 9–10）。因此 changed computation 优化的是“帮助复现语料后缀”，不等同于“调用真实有用/正确的工具”。

## top-k 强制触发与单 call 边界

训练造数时，默认只保留 `p(<API>) > 0.05` 的候选位置，至多 top-5，每个位置至多采 5 个调用；calculator/MT 为补偿稀疏性改为阈值 0、top-20、每位置 10 个调用，并用更宽松的 `τ_f=0.5`（物理页 3、15）。这是候选造数参数，不应与推理参数混淆。

推理时采用 greedy decoding，但并非只有 `<API>` 为 top-1 才调用：只要它进入 top-10 就强制开始调用；并硬性限制每个输入最多一次 API call，以防循环（物理页 5–6）。消融显示 top-1 时 T-REx/WebQS 调用率仅 40.3%/8.5%，top-10 时升至 98.1%/100%；作者还指出较大 k 会丢失“不确定时才调用”的校准性（物理页 9）。因此主结果高度依赖人工提高调用倾向，不能称为纯 greedy 下模型自然决定“何时调用”。

“最多一次调用”意味着不能链式使用工具，也不能根据第一次结果改写搜索或浏览多个结果；训练中各工具调用又独立生成。论文将这些列为明确限制（物理页 7–8、11）。所以本文准入的是单步 tool augmentation，不是一般多步 agentic tool use。

## Atlas size、系统预算与公平性

Toolformer 主 LM 是 6.7B GPT-J，但 QA 工具是另一个 retrieval-augmented LM：造数时用 `Atlas-large`，推理时改用更大的 `Atlas-xxl`（物理页 4、15）。本文没有报告这两个 Atlas 变体的参数量，也没有把 Atlas、Wikipedia BM25 索引、600M NLLB、工具执行和检索成本计入“6.7B”或推理预算。因而本文内无法建立 Toolformer 总系统与 OPT-66B/GPT-3-175B 的等参数、等 FLOP、等 latency 或等外部知识预算比较。

这一边界不是次要细节：LAMA 上 98.1% 样本主要调用 QA 工具，math 上 97.9% 调 calculator，QA benchmarks 上 99.3% 主要调用 Wikipedia search（物理页 6–7）。在 Natural Questions 等 QA 测试中，作者关闭 QA 工具，因为 Atlas 本身就在 Natural Questions 上 fine-tuned，启用会使任务过于简单（物理页 6–7）。所以“6.7B 模型击败 175B”应改写为“6.7B 控制器接入特定外部工具的系统，在本文协议下超过无工具大模型”；不能作为 standalone model-size scaling 结论。

训练本身使用每 API 最多 25k 样本、最长 1024 token、有效 batch 128、8 张 A100 40GB、最多 2k steps，并按 1k CCNet dev 样本选 checkpoint（物理页 17）。但论文未量化从上百万文档生成/执行/筛选 API calls 的总 token、工具调用、wall-clock 或能耗；作者也承认某些工具样本效率很低且没有把工具调用成本纳入决策（物理页 11）。

## 宽松 parser 与评测边界

多个任务采用明显宽松的非标准匹配：LAMA 只检查正确词是否出现在预测前 5 个词；数学题取模型预测的第一个数字，若有等式则取等号后第一个数字；QA 检查前 20 个词是否包含答案；MLQA 检查最多 10 个词内是否包含正确答案（物理页 6–8）。这些规则对同一任务内各 baseline 一致，故相对比较并非完全无效；但它们不是严格 exact match，并可能对包含工具返回文本、较冗长输出或偶然字符串命中的系统产生差异性优势。结果应称为“在本文宽松 containment parser 下的分数”，不能直接等同标准 benchmark accuracy。

另外，LAMA 过滤到 mask 位于句尾的子集，且禁用 Wikipedia Search 以避免直接泄漏（物理页 6）；QA 工具在 NQ 相关评测被禁用（物理页 6–7）。这些是必要但任务特定的防泄漏措施，进一步限制跨基准泛化解释。

## 争议结论

1. “self-supervised”可接受为“不需要大规模人工标注 API calls”，但并非无人工/外部监督：需要少量人工 demonstrations、API 专用 heuristic、已监督训练的 Atlas/NLLB，以及 future-token hindsight 筛选。
2. “decide when to call”在 top-1 消融下部分成立；主结果用 top-10 强制触发且调用率接近 100%，不能支持强自主选择解释。
3. “6.7B competitive with/outperforms 175B”不是系统资源公平结论；Atlas-xxl 等辅助组件大小与成本未在本文量化。
4. “learns useful calls”只能理解为降低语料 future-token NLL；表 10 明示有语义无关但通过过滤的调用。
5. “general tool use”应限定为每输入最多一次、不可链式、不可交互改写查询的工具调用。

## 准入裁决

**有限准入。** 准入：（a）few-shot 生成候选调用、future-token-loss 筛选、插入语料并 LM fine-tune 的 changed computation；（b）在本文 top-k/单-call 推理协议和宽松 parser 下，接入工具能提升若干零样本任务；（c）工具使用能力随控制器规模出现的经验趋势。拒绝准入：（a）无 hindsight 的自主工具学习；（b）自然 greedy 下可靠决定何时调用；（c）多步、链式或交互式 agent tool use；（d）与 66B/175B 的等总参数/计算/延迟公平结论；（e）严格标准 parser 下同等幅度的 benchmark 改善。后续引用必须同时标注 top-10 强制触发、最多一次调用、Atlas-xxl 未计入 6.7B、future-token hindsight 和宽松 parser。

