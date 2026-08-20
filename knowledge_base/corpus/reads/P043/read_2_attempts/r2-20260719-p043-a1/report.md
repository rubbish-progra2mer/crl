# P043 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P043/read_2_attempts/r2-20260719-p043-a1/invocation.md`
- 论文：*DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents*
- PDF SHA-256：`8fbf30398f5e62f8839f0c9c8609bbb9e3cd0b57ae27d4bf33cb5db2007d1118`
- [AUTHOR_FACT] 已读取全部 31 个物理页。

## 1. 评测计算与 I/O

- [AUTHOR_FACT] 数据集为 100 个中英文任务（50/50）、22 个领域；任务分布参考 96,147 条匿名查询日志，其中筛得 44,019 条 deep-research 查询，再由专家构造高难任务。（物理页 3–5，Dataset construction）
- [AUTHOR_FACT] RACE 先由 LLM 为任务生成 completeness、depth、instruction-following、readability 四维的任务专属准则与权重，再让 Gemini 2.5 Pro judge 将目标报告与 Gemini 2.5 Pro Deep Research 参考报告做 pairwise 比较；目标中间分再按 target/(target+reference) 归一化。（物理页 4–6，RACE）
- [AUTHOR_FACT] FACT 抽取并去重 statement–URL 对，通过 Jina Reader 获取网页，再由 Gemini 2.5 Flash 判断支撑；输出 citation accuracy 与每任务有效引用数。（物理页 5–6，FACT）
- [READER_INTERPRETATION] RACE 输出是“相对指定参考报告”的得分，不是绝对正确性；FACT 对可访问网页的陈述支撑更直接，但仍依赖抽取、抓取和 judge。

## 2. 基线与主要结果

- [AUTHOR_FACT] 为可比性，普通搜索模型最多 5 次搜索、可配置 reasoning 约 16k，报告输出最高约 36k；专有 deep-research 产品的真实内部预算并不透明。（物理页 5–6，Experimental setup）
- [AUTHOR_FACT] 表 1 中 Gemini Deep Research 的 RACE 约 48.88，OpenAI Deep Research 约 46.98，Perplexity 约 42.25，Grok 约 40.24。FACT 呈不同排序：Gemini 有效引用约 111.21、citation accuracy 约 81.44%，Perplexity citation accuracy 约 90.24%。（物理页 6，表 1）
- [AUTHOR_FACT] 报告在送入 RACE 前会用 LLM 清理引用格式；搜索模型还会被统一插入 citation markers/references。（物理页 5 与附录预处理说明）
- [READER_INTERPRETATION] 清理可减少格式噪声，但属于评测前变换；不同系统接受的修复形式不同，应被视为潜在差异化后处理，而不是原始端到端输出。

## 3. judge、oracle 与人类验证边界

- [AUTHOR_FACT] 参考报告由 Gemini 2.5 Pro Deep Research 在 2025 年 4 月生成，作者无法确认其内部迭代次数；RACE judge 也是 Gemini 2.5 Pro。（物理页 4–6）
- [READER_INTERPRETATION] 同族参考与 judge 存在模型耦合/风格偏好风险；Gemini DR 的最高 RACE 不能单独证明绝对最优。
- [AUTHOR_FACT] 人类验证只覆盖 50 个中文任务和四个 agents；每题三份报告、三位专家，约 70 名标注者、225 小时。RACE pairwise agreement 约 71.33%，人类互相 agreement 约 68.44%。（物理页 7–9，Human alignment）
- [AUTHOR_FACT] 报告的 OPC 约 99.54% 是在四个模型级平均点上计算；去除 ICC<0 的任务后仅保留约 37 题，RACE overall agreement 约 72.56%。（物理页 8–9）
- [READER_INTERPRETATION] 四点相关系数极不稳定，不能作为强系统级校准证据；只验证中文任务也不能直接支持英文等价性。

## 4. 限制、Operator 与 Failure

- [AUTHOR_FACT] 作者明示限制包括仅 100 题、策划偏差、人评吞吐有限（每题三专家、样本较小），以及误导信息与过度依赖自动评测风险。（物理页 17，Limitations）
- [READER_INTERPRETATION] Operator 候选：任务自适应 rubric/权重的参考相对 pairwise 评分；statement–URL 去重、网页抓取与支撑判定的 FACT 管线。二者应分开记录。
- [READER_INTERPRETATION] Failure 候选：reference-relative 分数被误当绝对分；同模型参考/judge 耦合；四个系统均值点产生近 1 的相关；引用格式修复改变待评对象。
- [OPEN_QUESTION] 专有系统搜索、token 与迭代预算未知，且 Gemini 参考生成次数未知，无法排除算力差异。
- [READER_INTERPRETATION] 建议保留，优先复用 FACT 的可核验流程；RACE 总排名必须注明 reference-relative、模型耦合和仅中文的人类验证范围。

## 5. 可视核验

- [AUTHOR_FACT] 已核对物理页 6 表 1，RACE/FACT 排名差异与抽取文本一致；未见实质冲突。

