# P014 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P014_instruct_of_reflection.pdf`
- PDF SHA-256：`57a01e87496308e3345839c48f085516dd2824ec5aaacf51b71f127c12f42bb7`
- 读取时间：`2026-07-19T15:46:00+08:00`
- 读取范围：逐页检查 1–23 页；正文 1–9 页，参考文献 9–12 页，datasets/transition tables/prompts 12–14 页，stop/select/refresh case studies 15–23 页。

## Changed computation / 方法对象

- [AUTHOR_FACT] IoRT 在 static reflection 的“basic→critique→revision”后加入 instructor。若 basic/reflected exact answers 不同，instructor 基于 meta-thought 选较好 response；若相同，判断 stop 或 refresh；最多 4 iterations。
- [AUTHOR_FACT] Meta-thinker 先从人工定义的 dataset-specific meta examples 中按 embedding similarity 取 top-k，生成当前问题 meta-thought，并把 `(question, meta-thought)` 追加到持续增长的 meta-memory，后续 instructor 用它作评判准则。
- [AUTHOR_FACT] Self-consistency classifier 只是字符串/结果 equality，不调用 LLM；真正 select、stop、refresh 的正确性判断由固定 GPT-3.5-Turbo-0613 instructor 完成。GPT-3.5 同时是 meta-thinker；reflector/black-box 可以是 GPT-3.5、GPT-4 或 Llama2 7B/13B/70B。
- [READER_INTERPRETATION] 核心 changed computation 是“对两个 test-time trajectories 做动态保留/重启 gate”，而不是 self-consistency 本身。它用一个独立 GPT-3.5 critic 选择答案，因此不属于单模型 intrinsic self-correction。

## 设置、信息与公平边界

- 数据：GSM8K 1319、SVAMP 1000、StrategyQA 2290；math 用 PoT 生成 Python 并执行得到 answer，commonsense 用 CoT+regex。代码执行只提供程序输出/错误，不直接提供 gold。
- Few-shot resources 每 dataset 人工准备 meta 6–8、refresh 5–8、reflect 3–4 examples；meta examples 含手工定义 meta-thought。IoRT 相比 plain PoT/CoT 多了 dataset-specific instruction assets。
- 所有方法 temperature .3，IoRT 最多 4 iterations；每 dataset 做 5 runs 报 average。论文给平均 calls，StrategyQA 给 tokens，但 math 未给总 tokens，且表中若干 baseline 数字来自 Zhang et al. 而非同一实现重新运行。
- 最接近 compute baselines：PoT-SC(8)/CoT-SC(8)（8 calls）、Self-Contrast（约 7.8）、Multi-Agent（9）、Self-Reflection/CRITIC（9）。IoRT math 7.3 average calls、StrategyQA 3877 tokens。

## 主要结果与窄归因

- Math Table 1：IoRT 相对 PoT 在 10 个 model×dataset cells 全部更高，例如 GPT-3.5 GSM8K 78.3→84.6、SVAMP 82.9→88.1；GPT-4 94.0→95.4、93.4→95.3。它与 PoT-SC(8)、Self-Contrast 各有胜负，不是所有 cell 最优。
- StrategyQA Table 2：IoRT 在五 backbone 为 71.9/78.8/53.1/60.1/67.9，高于 CoT 与 listed baselines；但所有 Llama 输出都由 GPT-3.5 instructor/meta-thinker辅助，不能归因于 Llama 自身 reflection capability。
- Ablation Table 3：不做 select、直接采用 reflected output 的 IoRT* 平均低约 4.4%；无 meta-thought 低约 2.1%；无 equality gate accuracy 约只低 .51%，但必须跑满 4 iterations。主要 accuracy gain 来自 independent selection 与 meta guidance，equality gate主要节省 calls。
- Transition Table 4 对 GPT-3.5 GSM8K：0→1 correct→wrong 1.7%、wrong→correct 5.9%；后续均保持净正，但第 3→4 仅 +.2。仍存在 drift，只是 select gate降低。
- 作者 exploration 中 CRITIC/self-correct 无 oracle 最高下降约 3.0/2.4%；oracle curves 上升。IoRT 未达到 oracle final，limitations 称 GPT-3.5 math 最终低 oracle 1.6%，仍会误判。

## 失败边界与限制

- [AUTHOR_FACT] Static reflection 可产生 redundant（correct→correct 的无效重复）、drift（correct→wrong）与 stubborn（wrong→wrong）；三者比例强依赖 backbone，Llama2-7B unstable iterations 达 89%，GPT-4 stable 达 94.3%。
- [AUTHOR_FACT] Instructor 并非完美；select/stop/refresh 会误判，IoRT 仍有 correct→wrong transitions。作者未使用 open-source meta-thinker/instructor，因为其 abstract reasoning/guidance 能力不足。
- [AUTHOR_FACT] 小模型更常产生多样但无效 iterations，也消耗更多 calls；若模型无法生成候选正确解，selector 无法创造正确答案。
- [READER_INTERPRETATION] 对 Llama 的提升混合了“候选由 Llama 生成”与“GPT-3.5 辅助判断/生成 meta-thought”；这是一种 heterogeneous ensemble，不是 Llama 内在自改进。
- [READER_INTERPRETATION] Meta-memory 在 evaluation 中持续追加 test questions/meta-thoughts，可能产生顺序依赖与 transductive test-time adaptation；论文未说明每个 question/run 是否 reset、是否跨 test items 复用。没有 gold label 不等于没有 evaluation-set adaptation。
- [READER_INTERPRETATION] IoRT select 在答案不一致时等价于 learned/model-based best-of-two；应与同 calls 的 independent verifier/reranker、SC 或 self-contrast比较。表含部分等 calls baselines，但没有单独隔离“GPT-3.5 selector without reflection”。
- [READER_INTERPRETATION] Math 的 code execution提供语法/运行信息，却不验证数值正确；StrategyQA 无 tool。两任务都是短答案，answer equality 易定义，开放式 Agent trajectories 无直接 equality gate。

## 可抽取候选（尚非正式 Card）

- Operator：`Dynamic Stop–Select–Refresh Reflection Control`——一致时判断 stop/refresh，不一致时保留更可信 trajectory；显式把候选生成与选择分开。
- Operator：`Meta-Criterion-Augmented Candidate Selection`——用任务级抽象方法作为 verifier criterion，而不是只比较表面 rationale；需标注 meta source 与模型能力。
- Failure：`Static Reflection Redundant–Drift–Stubborn Trilemma`——固定迭代会无效重复、破坏正确答案或困在错误吸引子，且比例随模型/任务变化。
- Failure：`Strong External Instructor Masquerades as Base-Model Self-Improvement`——弱模型候选由更强独立模型筛选，gain 不能归因于 base model intrinsic reflection。
- Failure：`Test-Time Meta-Memory Creates Order-Dependent Evaluation`——测试问题生成的 meta-thought若跨样本累积，结果依赖顺序/是否 reset。

## 未解决问题

- `[OPEN_QUESTION]` Meta-memory 是否在每个 dataset/run/question 重置，论文公式与文字未给清晰 protocol。
- `[OPEN_QUESTION]` 人工 meta/refresh/reflect few-shot examples 是否从 train split选取、是否与 test patterns重叠，PDF未列所有来源。
- `[OPEN_QUESTION]` 仅 GPT-3.5 selector、无 reflection 或无累积 meta-memory 的完整消融缺失，无法分离 selector 与迭代机制。
- `[OPEN_QUESTION]` 开放文本、tool trajectories、多步 Agent task 如何定义 answer consistency 与 stop，没有实验。
