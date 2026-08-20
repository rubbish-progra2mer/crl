# P084 independent second-read report

## 1. 读取身份与总裁决

- Attempt ID：`r2-20260720-p084-a1`
- Task ID：`/root/plan05_p084_second_read`
- 角色：fresh independent source reader
- 目标 PDF：`knowledge_base/staging/plan05_v004_gap/P084_function_calling_robustness.pdf`
- 实测 PDF SHA-256：`8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7`（与 invocation 一致）

**AUDIT_JUDGMENT — 总裁决：** 该文直接支持：在固定原始查询、把平均工具数从 2.7 扩至 5.6 且新增工具语义相关的条件下，所测 9 个模型的 AST function-call construction 分数均下降；扩展条件的失败中明确包含 wrong function、wrong number of functions、wrong parameter assignment，以及少量 wrong syntax。该文不直接支持：（a）wrong-function 或 wrong/invalid-argument 错误相对原始工具集的类别级“上升量”，因为没有报告原始条件的同口径错误类型分布；（b）运行时工具执行失败、异常或端到端任务成功率，因为实验仅采用 AST 阶段；（c）任何已经验证成功的在线 routing/filtering Operator。用于剔除等价生成工具的 cosine filter 是离线 benchmark 构造清洗，不是被测 agent 的在线路由器。

## 2. Canonical metadata

- **AUTHOR_FACT：** 标题：*On the Robustness of Agentic Function Calling*。（物理页 1，标题）
- **AUTHOR_FACT：** 作者：Ella Rabinovich；Ateret Anaby-Tavor；作者单位均为 IBM Research。（物理页 1，作者栏）
- **AUTHOR_FACT：** 载于 *Proceedings of the 5th Workshop on Trustworthy NLP (TrustNLP 2025)*，论文集页 298–304，日期 2025-05-03，Association for Computational Linguistics。（物理页 1，页脚）
- **AUTHOR_FACT：** PDF 共 7 个物理页；物理页 1–7 对应论文集印刷页 298–304。
- **AUDIT_JUDGMENT：** PDF 页面和 PDF metadata 均未给出 DOI、ACL Anthology ID 或 arXiv ID；在禁止联网条件下不补猜标识符。PDF metadata 的 title/author 字段为空，故以上 canonical metadata 来自论文首页正文。

## 3. Toolkit-expansion intervention 与变量边界

### 3.1 精确 intervention

1. **AUTHOR_FACT：** 起点是一个具有挑战性的、single-turn BFCL test set 子集；作者使用 200 个 dataset examples。（物理页 2，Contribution，短定位语句 “one of the (single-turn) challenging BFCL test sets”；物理页 4，§3.2，短定位语句 “averaged over the 200 dataset examples”）
2. **AUTHOR_FACT：** 对每个原始请求，用 Llama3.1-70B 生成“related yet different”请求变体。附录 prompt 要求：同一企业项目中的相似但不同需求；引入一到两个额外、不同的 parameter types；原始查询的函数不能完全适用于新查询，反之亦然；新查询必须自包含调用及参数所需信息。（物理页 3，§2.2 步骤 (1)；物理页 7，§7.2）
3. **AUTHOR_FACT：** 对每个相关请求变体，用 CodeLlama-13B 生成可满足它的 JSON tool definition；作者称其 prompt 和 few-shot examples 约束 JSON 格式、命名惯例、风格以及函数/参数描述的细节程度。（物理页 3，§2.2 步骤 (2)，短定位语句 “For each request variant, a tool definition is generated”）
4. **AUTHOR_FACT：** 作者构造 tool “signature”：拼接函数名与函数描述、参数名与参数描述；用 sentence-transformers embedding 的 cosine similarity 与原始工具比较，过滤相似度高于预定义阈值的生成工具。附录给出阈值 0.8。（物理页 3，§2.2 步骤 (3)；物理页 7，§7.3，短定位语句 “similarity threshold was set to 0.8”）
5. **AUTHOR_FACT：** 完成扩展后，测试的是**原始查询**；图 2 明说 “expanded toolkit is created for testing the original query”。平均工具数从原 BFCL 的 2.7 个（作者称 seemingly unrelated）变为 5.6 个，亦即每个 200-case test case 平均增加约 3 个 semantically related functions。（物理页 3，Figure 2；物理页 4，§2.2 首段）

### 3.2 固定与变化变量

- **AUTHOR_FACT：** 作者报告三个版本：（a）original query + original toolkit；（b）rephrased query + original toolkit；（c）original query + expanded toolkit。（物理页 4，§3.2，短定位语句 “including three variants”）
- **AUDIT_JUDGMENT：** 对隔离 toolkit-expansion 效应，应比较 (a) 与 (c)：200 个原始任务/原始查询保持不变，所评 9 个模型保持不变，AST 评价框架保持不变；变化的是 prompt 中 toolkit 的内容与大小，从原始工具集改为保留原工具并加入相关生成工具的扩展集。
- **AUDIT_JUDGMENT：** (b) 是另一项 query-rephrasing intervention，不能与 toolkit-expansion 混为一个干预。其查询变化、toolkit 固定。
- **AUDIT_JUDGMENT：** 论文未在正文或附录报告 decoding 参数、随机种子、重复运行次数、tool ordering 是否固定、API 模型 snapshot、每个样本精确新增工具数分布，亦未证明除了 toolkit 文本外 prompt tokenization/context length 完全相同。因而这些变量只能记为“未报告”，不能宣称已控制。

## 4. 报告的性能变化与错误类别

### 4.1 Table 2 全量 AST 结果

下表逐行转录物理页 5 Table 2。`Δabs` 为本审计由展示分数相减所得；括号内相对降幅是论文印刷值，不是本审计重算值。

| Model | Original AST | Orig toolkit + rephrased query | Δabs | Expanded toolkit + original query | Δabs | 扩展失败分布：syntax / function / #functions / parameter |
|---|---:|---:|---:|---:|---:|---:|
| Llama3.1-70B | 0.965 | 0.825 (−15%) | −0.140 | 0.925 (−4%) | −0.040 | 0.00 / 0.45 / 0.10 / 0.45 |
| Llama3.3-70B | 0.945 | 0.785 (−17%) | −0.160 | 0.905 (−4%) | −0.040 | 0.00 / 0.23 / 0.46 / 0.31 |
| DeepSeek-V2.5 | 0.965 | 0.835 (−14%) | −0.130 | 0.950 (−2%) | −0.015 | 0.00 / 0.56 / 0.00 / 0.44 |
| Qwen2.5-72B | 0.975 | 0.850 (−13%) | −0.125 | 0.965 (−1%) | −0.010 | 0.00 / 0.29 / 0.00 / 0.71 |
| Granite3.1-8B-instruct | 0.945 | 0.770 (−19%) | −0.175 | 0.870 (−8%) | −0.075 | 0.09 / 0.50 / 0.18 / 0.23 |
| Claude-3.5-Haiku | 0.925 | 0.765 (−11% as printed) | −0.160 | 0.870 (−2% as printed) | −0.055 | 0.00 / 0.44 / 0.00 / 0.56 |
| Claude-3.5-Sonnet | 0.915 | 0.845 (−8%) | −0.070 | 0.890 (−3%) | −0.025 | 0.00 / 0.29 / 0.00 / 0.71 |
| gpt4o-mini | 0.925 | 0.765 (−17%) | −0.160 | 0.870 (−6%) | −0.055 | 0.26 / 0.42 / 0.00 / 0.32 |
| o1-mini | 0.905 | 0.770 (−15%) | −0.135 | 0.885 (−2%) | −0.020 | 0.33 / 0.27 / 0.00 / 0.43 |

- **AUTHOR_FACT：** Table 2 把扩展条件失败分为 `wrong syntax`、`wrong function`、`wrong num of functions`、`wrong param. assignment`；正文补充说明 wrong number 通常是生成两个函数而不是一个，并提到 parameter hallucinations。（物理页 4，§3.2 “Agents’ Sensitivity to Toolkit Expansion”）
- **AUTHOR_FACT：** 右侧数值是“within the set of failures stemming from toolkit expansion”的类别比例；表头标 `%`，正文称 proportion。故 `0.45` 应读作比例 0.45（45%），而不是 0.45%。（物理页 4–5，Table 2 及紧邻正文）
- **AUTHOR_FACT：** 论文给出一个 wrong-function 实例：扩展 toolkit 下，对 Manchester United 排名查询生成 `football_league.ranking("premier league")`（返回整个联赛表），而非更合适的 `sports_ranking("Manchester United", "premier league")`。（物理页 4，§3.2，短定位语句 “instead of the more appropriate”）
- **AUTHOR_FACT：** 作者还观察到，加入函数偶尔会“repair”少量原始 baseline failures，并解释为模型生成的随机性；论文没有给出这类 repair 的数量或模型分项。（物理页 5，Table 2 后首段）

### 4.2 数值与解释审计

- **AUDIT_JUDGMENT：** 9 个模型在 expanded-toolkit + original-query 条件的展示 AST 分数均低于各自 original baseline，绝对下降范围为 0.010–0.075；论文的“performance degradation across the board”得到 Table 2 直接支持。
- **AUDIT_JUDGMENT：** Claude-3.5-Haiku 行的两个印刷相对降幅与展示分数不相容：`0.925→0.765` 对应约 −17.3%，不是印刷的 −11%；`0.925→0.870` 对应约 −5.9%，不是印刷的 −2%。绝对分数和本审计 Δabs 没有歧义，但不得复用这两个印刷百分比作为精确降幅。
- **AUTHOR_FACT：** 对 rephrased-query 条件，正文另称 70–90% errors 来自 parameter value assignment mismatch，并将多数失败归因于 exact-match evaluation 缺陷；例子是 `Miami,FL` 被模型赋为 `Miami, FL`，但 gold 允许值只列 `Miami`、`Miami, Florida`、`FL`。（物理页 4，§3.2 “FC Evaluation Approach Weakness(es)”）
- **AUDIT_JUDGMENT：** 上述 70–90% 是**查询改写条件**的分析，不是 expanded-toolkit 条件；不能用它证明相关工具扩展造成 70–90% argument errors。

## 5. AST 与 execution 边界

- **AUTHOR_FACT：** BFCL 评价分两阶段：（1）tree-matching AST 检查生成调用；（2）在模拟环境中评价工具执行。本文明确只采用第一阶段 AST，因为研究焦点是输入 intervention 下的 FC construction。（物理页 4，§3.1 “Evaluation Approach”）
- **AUDIT_JUDGMENT：** 因此，分数只衡量构造出的调用是否按 BFCL AST 判定正确；它不证明工具真正运行成功，不覆盖执行异常、外部状态变化、返回值正确性、端到端 goal completion，也不能把语义等价但 AST/exact-match 不同的调用自动视为成功。
- **AUTHOR_INTERPRETATION：** 作者认为 query-rephrasing 的许多失败来自评价方式缺陷，并提出 semantic similarity、多维匹配或 LLM-as-a-Judge 可能缓解，但明确把在 BFCL 中探索该缓解留给 future work。（物理页 4，§3.2）

## 6. Generated tools 与 equivalence filter 的局限

- **AUTHOR_FACT：** 作者称经 manual inspection，生成工具定义的 style 与原工具不可区分；但没有报告检查样本数、检查协议或功能执行验证。（物理页 3，§2.2 步骤 (2)）
- **AUTHOR_FACT：** 作者承认不同名称、描述或参数顺序的工具仍可能 functionally equivalent；附录例子是 `sentence.translate(...)` 与 `translate_sent(...)`。（物理页 7，§7.3）
- **AUTHOR_INTERPRETATION：** 作者说这类情况 rare，并用 signature embedding cosine threshold 0.8 过滤，目标是得到 distinct functions。（物理页 3、7）
- **AUDIT_JUDGMENT：** filter 仅比较文本 signature 的 embedding 相似度，不执行函数、也不做形式语义等价证明；阈值 0.8 可能漏掉低文本相似但功能等价的工具，也可能剔除文本相似但功能确实不同的工具。signature 描述只明确包含名称与描述，没有报告把参数类型、约束、返回语义或副作用纳入判定。
- **AUDIT_JUDGMENT：** 论文没有报告过滤前后候选数、被过滤数、false-positive/false-negative 审计或独立人工复核。因此 5.6 个工具应理解为该生成与启发式过滤流程的产物，不能强解释为已验证互斥的真实 API 集合。
- **AUDIT_JUDGMENT：** 物理页 3 的“manual review of 50 examples ... no semantic drift”针对的是 §2.1 的 meaning-preserving query rephrases，不是扩展工具的功能正确性验证。

## 7. 对指定主张的直接支持度

### 7.1 related-tool expansion 下 wrong-function

- **AUTHOR_FACT：** Table 2 对每个模型都报告了 expanded-toolkit failures 中的 wrong-function 比例，为 0.23–0.56；正文给出 Manchester United 的具体 wrong-function 例子。
- **AUDIT_JUDGMENT：** **直接支持“相关工具扩展条件中存在、且常占显著比例的 wrong-function failures”。**
- **AUDIT_JUDGMENT：** **不直接支持“wrong-function 错误率相对原工具集上升了多少”或“上升具有统计显著性”。** 原因是右表分母仅为 expansion failures，论文未给出 baseline 的同类错误分布、paired transition counts、置信区间或显著性检验。

### 7.2 related-tool expansion 下 wrong/invalid arguments

- **AUTHOR_FACT：** Table 2 直接报告 expanded-toolkit failures 中 wrong parameter assignment 比例 0.23–0.71；正文还提到 parameter hallucinations，并把该类别限定为 correctly selected function 上的错误参数赋值。（物理页 4–5）
- **AUDIT_JUDGMENT：** **直接支持“相关工具扩展条件中存在 wrong parameter assignment”。**
- **AUDIT_JUDGMENT：** **不直接支持“该类错误相对 baseline 上升”**，因为同样缺少 baseline 类别分布；也**不直接支持 runtime invalid-argument exception**，因为没有执行阶段。“wrong syntax”是独立类别，不应与 malformed/incorrect argument 合并；论文亦未提供名为 `invalid argument` 的独立类别。

### 7.3 成功 routing/filtering Operator

- **AUTHOR_FACT：** 作者用 shortlisting module 描述现实动机，并说相关工具“likely to be shortlisted by a selection module”；实验模拟的是 shortlist 后扩展 toolkit 的输入。（物理页 2，Contribution；物理页 3，§2.2）
- **AUTHOR_FACT：** 论文没有实现或比较任何在线 router/shortlister，也没有报告 routing recall、top-K、latency 或成功率。它只报告 agents 在给定 thin/expanded toolkit 后的 AST 表现。
- **AUDIT_JUDGMENT：** **不支持任何已经成功的 routing/filtering Operator。** 0.8 cosine equivalence filter 是离线数据生成清洗，目标是删除与原函数近似等价的 synthetic tools；它既不按用户查询筛选可调用工具，也没有作为 agent-time Operator 被测。作者建议的 semantic-similarity evaluation mitigation 也明确属于 future work。

## 8. 证据定位索引

| 物理页（印刷页） | 章节/对象 | 短 locator | 用途 |
|---|---|---|---|
| 1（298） | 标题、Abstract、§1 | “stability in function calling when the toolkit expands” | metadata 与问题定义 |
| 2（299） | Contribution、§2 | “semantically related tools that are likely to be shortlisted” | 场景与 single-turn BFCL 起点 |
| 3（300） | Figure 2、Table 1、§2.2 | “expanded toolkit is created for testing the original query” | 三步生成/过滤 intervention |
| 4（301） | §3.1–3.2 | “we, therefore, adhere to ... AST” | 200 examples、2.7→5.6、AST 边界、错误解释 |
| 5（302） | Table 2、§4–5 | “Failures stemming from toolkit expansion” | 全模型分数和错误分布、repair、limitations |
| 7（304） | §7.2–7.3 | “similarity threshold was set to 0.8” | related-query prompt 与 equivalence-filter 细节 |

## 9. 实际读取范围与 observable trace

- 完整读取的工作区治理/调用文件：`D:\Desktop\crl_judge\AGENTS.md`、`D:\Desktop\crl_judge\crl_agent_v3\AGENTS.md`、`D:\Desktop\crl_judge\crl_agent_v3\CRL.md`、`D:\Desktop\crl_judge\crl_agent_v3\CRL_ENVIRONMENT.md`、本 attempt 的 `invocation.md`。
- 操作所需技能说明读取：`C:\Users\g\.codex\skills\pdf\SKILL.md`；另读取 `C:\Users\g\.codex\plugins\cache\openai-curated-remote\superpowers\6.1.1\skills\using-superpowers\SKILL.md` 后，按其中 `SUBAGENT-STOP` 忽略该技能。曾尝试读取不存在的 `C:\Users\g\.codex\skills\.system\pdf\SKILL.md`，命令报 path not found，未取得文件内容。
- PDF 读取：仅目标 `P084_function_calling_robustness.pdf`；先以 `Get-FileHash` 核对 SHA-256，再以项目 `.venv` 中 PyMuPDF 1.28.0 读取 metadata、全部物理页 1–7 文本；对物理页 3、4、5、7 单独复核，并用物理页 5 的 word coordinates 校验 Table 2 列对齐。`find_tables()` 对无线框表只识别出不完整表头，未作为数值依据。
- 视觉核验边界：尝试对物理页 5 表格区域作纯内存 PNG/JPEG 渲染，但当前图像显示通道返回 “image content omitted because it could not be processed”；未声称完成成功的图像视觉核验。表 2 数值由页面文本与每词 x/y 坐标交叉核对。
- 首次全页文本输出因终端 GBK 无法编码版权符号而在物理页 1 中止；显式设置 `PYTHONIOENCODING=utf-8` 后重新读取全部 7 页成功。
- 未联网，未运行任何检索，未读取或枚举 `read_1.md`、Cards、其他 reads/reconciliation、Corpus Report、saturation audit、production retrieval calibration/blind/revealed regression、Candidate、Commissioning 或科研 Reviewer 文件。
- 写入范围：仅本 `report.md`；未修改其他文件。
- 模型身份：Codex（基于 GPT-5；当前子任务接口未暴露更细的内部 model/version 标识）。

