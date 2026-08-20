# P005 主 Codex 首读

- PDF：`knowledge_base/staging/papers/P005_toolllm.pdf`
- PDF SHA-256：`76f7d1a6acd0c8d86d0bd41340dd12976643b9bbcaed3008a2357ef2d492ff8a`
- 读取时间：`2026-07-19T16:37:00+08:00`
- 读取范围：逐页检查 1–23 页；正文 1–10 页，参考文献 10–12 页，过滤/压缩/训练/DFSDT/ToolEval 细节 13–16 页，生成与推理 prompts/样例 16–23 页。

## Changed computation

- [AUTHOR_FACT] ToolLLM 是数据、训练、检索、推理、自动评测的组合框架：从 RapidAPI 筛出 16,464 APIs，ChatGPT 生成 instruction 与相关 API，再用真实 API response 标注成功路径，SFT LLaMA-2-7B，并在推理时用 dense retriever 选 API。
- [AUTHOR_FACT] DFSDT 把单路径 ReAct 改为可撤回的深搜：模型可调用 `Finish by Giving Up` 放弃当前分支；回溯后把已生成节点放进 prompt，明确要求新 action 与旧节点不同。为节省评估调用，它不对子节点打分排序，而采用 pre-order DFS，首个可行路径即停止。
- [READER_INTERPRETATION] DFSDT 的最小 changed computation 是“失败分支可显式终止、历史兄弟分支作为去重约束参与下一次采样”，不是通用 learned planner；整个 ToolLLaMA 增益则同时含成功路径筛选、SFT、上下文扩展、API retrieval 与推理搜索。

## 数据、基线与预算

- 第 3–6 页：初始 10,853 tools/53,190 APIs 经可用性、响应时间/质量过滤后剩 3,451/16,464；ChatGPT 用每次 3 个由人工写的 seed 生成 I1 单工具、I2 同类别多工具、I3 同集合多工具 instruction，共约 200k qualified pairs。
- DFSDT 对所有生成 instruction 标注，只保留 ToolEval 判定通过的路径，最终 126,486 对、469,585 次真实 API calls。训练分布因此是 teacher+search+evaluator 条件下的成功样本，不能代表原始用户请求分布，也缺少失败路径监督。
- 第 7 页 Table 3 以 ChatGPT 比较 ReAct 35.3、按 DFSDT 总成本重复的 ReAct@N 44.5、DFSDT 63.8 average pass。论文称预算对齐，但没有逐类 token、function-call、延迟和回溯深度分解。
- 主实验除 `ToolLLaMA-DFSDT-Retriever` 外都直接提供 generator 标注的 ground-truth/oracle API 集；因此表 4 主要测试在给定相关 API 条件下的执行/搜索，不是从 16k API 端到端选择。
- ToolLLaMA 是 LLaMA-2-7B，context 从 4096 插值到 8192，2 epochs，按 dev 最佳 checkpoint；与 ChatGPT/GPT-4/Claude/Text-Davinci 的预训练规模和接口不同，不能仅由表 4 分离“ToolBench 数据”的因果贡献。

## 主要结果与定位

- API retriever Table 2：相对 BM25/Ada，平均 NDCG@1 为 78.0 vs 18.5/49.6，NDCG@5 为 84.9 vs 17.0/45.4。但 positive API 标签由 ChatGPT 生成 instruction 时同步给出，且作者后续发现其他替代 API 可能更好，标签并非完备语义真值。
- Table 4：ChatGPT ReAct/DFSDT average pass 40.2/64.8；GPT-4 为 57.2/71.1；ToolLLaMA ReAct/DFSDT 为 29.0/66.7，带 top-5 retriever 67.3。Vicuna/Alpaca 为 0，说明普通 dialogue tuning 未满足其特定 function-call protocol，不足以推出“无工具能力”。
- ToolLLaMA DFSDT 的 average win 60.0（与 ChatGPT-ReAct 比），Retriever 63.1；完整 tie 表在附录 Table 6 中分别为 raw win/tie 55.2/9.8 与 59.2/7.8，主表把一半 tie 加入 win/lose。
- APIBench OOD：带 oracle API 时 ToolLLaMA AST 85.88–88.80，但带自身 retriever 只有 16.77/51.16/40.59；Gorilla-RS+BM25 在三域分别 15.71/50.00/41.90，ToolLLaMA 并非全面更强。retrieval 明显是端到端瓶颈。
- ToolEval 与 human agreement：300 test instructions/方法的子集上 pass 87.1%、win 80.3%；作者明确承认人类对探索充分性与调用成本偏好也常不一致，自动评测仍未解决公平性。

## 失败边界与限制

- [AUTHOR_FACT] ToolEval 的“Pass”并不总是完成任务：对 unsolvable instruction，拒绝或 `Give Up` 可算 Pass；对 solvable instruction，若充分尝试所有 API 仍无有效信息，拒绝也可算 Pass。故 pass rate 衡量的是其 rubric 下的适当终止，不等于任务成功率。
- [AUTHOR_FACT] 第 13 页 response compression：超过 1024 tokens 时按 ChatGPT 选的 schema 删除字段，仍长则只保留前 1024 tokens。作者称人评保留重要信息，但未给定量误删率；这可能改变工具 observation。
- [AUTHOR_FACT] DFSDT 在无撤回时退化为 ReAct；论文关于 pre-order 与经典 DFS “explored nodes almost the same”的说法是经验陈述，未给排序版 DFS 的准确率/成本表。
- [AUTHOR_FACT] 主实验的 pass/win 都由 ChatGPT 至少 4 次投票；同一模型参与 instruction 生成、solution annotation 与 evaluation，存在 teacher-style 与自偏好闭环。有限人评一致率不能排除各模型间系统偏差。
- [READER_INTERPRETATION] top-5 retriever 高于“ground truth APIs”说明所谓 oracle 集不是真正覆盖所有有效 API；既影响 retrieval NDCG 的解释，也影响用 oracle API 比较模型的难度。
- [READER_INTERPRETATION] 只保留 passed DFSDT 路径把搜索时的负向经验丢弃；SFT 学到的是成功轨迹模仿，不能据论文证明模型获得了运行时自我纠错或失败学习能力。
- [READER_INTERPRETATION] RapidAPI 动态、可用性与返回内容变化使复现依赖当时 API 状态；作者使用自动过滤和压缩缓解，但未提供稳定 snapshot 的端到端响应集合。

## 可抽取候选（尚非正式 Card）

- Operator：`Explicit Give-Up Backtracking with Sibling-Aware Resampling`——当前 action path 失败时终止分支，把旧兄弟节点作为差异约束重新采样，pre-order 深搜直到可接受终点。
- Operator：`Instruction-Conditioned API Retrieval before Tool Execution`——先从超大 API 文档库检索小候选集，再把文档注入 Agent function/action space。
- Failure：`Success-Only Tool Trace Distillation`——只用 evaluator 通过轨迹训练，丢失失败与回退信息，且模型/搜索/评测贡献无法分离。
- Failure：`Evaluator-Defined Refusal as Apparent Success`——rubric 把某些 give-up/refusal 计为 pass，使 headline pass rate 不等于实际完成请求。
- Failure：`Oracle API and Incomplete Relevance-Label Confound`——绝大多数主表使用不完备的 generator API 集，真实检索性能显著改变端到端结果。

## 未解决问题

- `[OPEN_QUESTION]` ReAct@N 与 DFSDT 的精确平均 token/API-call/latency 及失败预算未公开，无法复核“相同成本”。
- `[OPEN_QUESTION]` ToolEval 人评是否盲于模型身份、annotator 数和 inter-annotator agreement 未在本文给全。
- `[OPEN_QUESTION]` API response compression 的字段误删对多步任务成功率没有消融。
- `[OPEN_QUESTION]` 训练集中同源 ChatGPT 生成/筛选是否造成对 ChatGPT rubric 的过拟合，缺少独立 evaluator 的主结果。
