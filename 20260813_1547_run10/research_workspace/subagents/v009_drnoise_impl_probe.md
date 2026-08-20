# v009 DRNOISE 实现可行性核查（Research Subagent 草案）

> 身份与权限：本文件只做 DRNOISE 官方资产核查和最小实现设计，是非权威 Research Subagent 草案；没有运行昂贵实验，没有安装依赖，没有修改 CRL 机器、`hypotheses`、`portfolio` 或 `Decision`。网络和本机核查时间为 2026-08-13。

## 1. 结论先行

1. **当前无法核验到可访问的 DRNOISE 官方代码、100 题数据、grader 或许可证。** arXiv v1 论文说“released benchmark comprises 1,750 documents”和“grader ships with regression tests”，但论文页、TeX 源包、GitHub/Hugging Face 精确检索均没有给出资产 URL。论文的 CC BY 4.0 只可确认论文/源稿许可，不能外推到未取得的数据或代码。
2. **能固定的官方对象只有论文 v1。** `arXiv:2607.17291v1` 提交于 2026-07-19；PDF 和源包已在临时目录只读下载并计算 SHA-256，源包只含论文 TeX、参考文献、样式和两张图，不含 benchmark 文档、grader 或运行脚本。
3. **精确复现 DRNOISE 论文结果目前被官方资产缺失阻塞。** 无法复现其 100 题、共享背景语料、Qwen3-Embedding-8B dense index、Lucene snippets、模型轨迹和回归测试，也不能把 Run-local 合成结果写成“DRNOISE 复现”。
4. **20–30 题的 Run-local 谱系扩增探针可低成本落地。** 最小方案用 20 题覆盖论文全部 10 个任务家族，每家族 2 题；SQLite FTS5 提供固定语料搜索，答案采用隐藏结构世界的确定性 exact-match 终局。先做 copy-invariance property test，再做少量真实搜索智能体运行。
5. **oracle lineage 与 estimated lineage 必须物理和语义隔离。** oracle 运行时只能看到“文档→匿名记录根”的盲映射，不能看到 gold、false、route 或 document role；estimated 运行时只能从公开文本、URL、时间和公开引用推断谱系。独立 evaluator 在运行结束后才读取私有 gold、路线和角色。
6. **最强基线必须是 `Argus-style evidence graph + near-duplicate clustering`，而不是弱提示。** Argus 当前也没有检索到官方可运行代码，因此只能明确标为“按论文语义重实现的 Argus-style baseline”，不能声称复现官方 Argus。

## 2. DRNOISE 官方资产核查

### 2.1 固定论文版本

一级来源：

- 摘要页：<https://arxiv.org/abs/2607.17291>
- HTML：<https://arxiv.org/html/2607.17291>
- 固定版本：<https://arxiv.org/abs/2607.17291v1>
- PDF：<https://arxiv.org/pdf/2607.17291v1>
- TeX 源包：<https://arxiv.org/src/2607.17291v1>

已核验事实：

| 对象 | 固定值 |
|---|---|
| arXiv 版本 | `2607.17291v1` |
| 提交时间 | 2026-07-19 15:20:40 UTC |
| 论文页许可 | CC BY 4.0 |
| PDF 大小 | 3,302,885 bytes |
| PDF SHA-256 | `29D45DBE0DD62D74EF42244A6C7032961C445E914E0F072CDDC86BC510002590` |
| TeX 源包 SHA-256 | `985587560076F23F10360D5794C3C054DF987D339529504AE5625C6B1AA21EBE` |

TeX 源包清单只有：

```text
00README.json
figures/main_results.pdf
figures/drnoise.pdf
main.bbl
main.tex
math_commands.tex
paper.bst
paper.sty
references_correct.bib
```

源包中对 `github`、`huggingface`、`code availability`、`data availability`、`repository` 的检索没有得到资产地址。`main.tex` 的确写出：

- benchmark 含 100 题、10 家族、1,750 个任务文档；
- 每题有两个独立间接记录组和一个直接错误总结；
- 文档标识在索引前被中性化；
- agent 使用 BrowseComp-Plus-compatible search-only harness；
- dense retrieval 为 Qwen3-Embedding-8B，Lucene 提供文本片段；
- grader “ships with regression tests”。

但上述描述没有随源包交付任何数据或代码。

### 2.2 代码、数据和许可证搜索结果

执行了只读 GitHub Repository Search API：

- 查询 `DRNOISE in:name,description,readme` 返回 4 个 repository，均是综述/论文列表，没有 DRNOISE 官方实现；其中 `Awesome-Deep-Research` 对 DRNOISE 只标 `[Paper]`，邻近基准会明确标 `[Code]`。
- 查询 `2607.17291 in:name,description,readme` 返回大量无关数字碰撞；没有可验证为作者官方仓库的结果。
- GitHub/通用搜索对完整论文标题没有命中官方代码。

执行 Hugging Face datasets API `search=DRNOISE`，返回 0 个数据集。通用搜索对完整标题也没有命中官方数据卡。

因此截至核查时的严谨状态是：

| 资产 | 状态 | 可否固定版本 | 许可证 |
|---|---|---|---|
| 论文 PDF/TeX | 可访问 | 是，arXiv v1 + SHA-256 | CC BY 4.0（论文） |
| DRNOISE 100 题与 1,750 文档 | 未找到可访问官方资产 | 否 | 未知 |
| DRNOISE grader / regression tests | 未找到 | 否 | 未知 |
| DRNOISE agent harness / traces | 未找到 | 否 | 未知 |
| 背景语料和索引 | 未找到 | 否 | 未知 |

“论文声称 released”与“当前找不到公开入口”之间存在不一致；不能据此断言作者从未发布，只能断言本次一级来源和主流代码/数据入口未能定位。

### 2.3 BrowseComp-Plus 可用但不是 DRNOISE 资产

DRNOISE 说明使用 BrowseComp-Plus-compatible harness。BrowseComp-Plus 官方资产可访问：

- 官方仓库：<https://github.com/texttron/BrowseComp-Plus>
- 本次核查固定提交：`046949032b0328319cc9a02663a759ec601d9402`
- 该提交时间：2026-05-28 19:01:25 UTC
- repository license：MIT
- 官方语料数据卡：<https://huggingface.co/datasets/Tevatron/browsecomp-plus-corpus>，数据卡标 MIT，约 1.76 GB、100,195 文档。

它提供搜索 agent、BM25/Qwen3-Embedding 索引入口和自定义 retriever 接口，但不能恢复 DRNOISE 的 100 题或 1,750 个任务文档。其完整依赖包括 Python 3.10/uv、Java 21、Pyserini、FAISS、Qwen Agent 等；直接并入当前 Windows 共享环境会引入不必要的依赖和版本风险。本次仅在系统临时目录浅克隆、检视固定提交，未写入 Run，也未安装依赖。

## 3. 复现层级与允许的科学表述

### 3.1 当前不可做

- 不可声称“在 DRNOISE 上复现/提升”；
- 不可引用未取得 grader 的回归测试结果；
- 不可把论文 CC BY 4.0 当作数据/代码许可证；
- 不可用 Appendix E 的一个公开例子扩写后冒充官方 20–30 题子集；
- 不可把 BrowseComp-Plus 原语料当成 DRNOISE 背景语料；
- 不可把 Argus-style 自行实现写成官方 Argus 复现。

### 3.2 当前可做

可以明确标为：

> **Run-local DRNOISE-inspired lineage stress test**：基于 DRNOISE 论文公开任务结构、但由本 Run 独立生成的合成谱系压力测试，用于杀掉/支持复制不变停止机制的实现可行性，不用于声称外部 benchmark SOTA。

这个探针只应作为 Scratch/Recorded 阶段的高信息量证据。即使结果正向，也不能单独满足正式 Seed 所需的独立 Formal / Review-support 真实实验。

## 4. Run-local 20–30 题合成设计

### 4.1 任务数量与覆盖

建议最小版为 **20 题，固定 seed，每个 DRNOISE 家族 2 题**：

1. 实体选择；
2. 日期选择；
3. 布尔核验；
4. 有序 Top-3；
5. 多跳连接；
6. 全条件选择；
7. 文本属性查找；
8. 集合选择；
9. 冲突归因；
10. 分布式总成本聚合。

如果 20 题机制探针存活，再固定扩至 30 题（每家族 3 题）。不要根据 20 题测试结果重新挑任务或 seed；扩展规则需先写入配置。

### 4.2 每题的隐藏结构世界

每题先生成一个私有、结构化 `world`：

- 4–8 个匿名实体；
- 题目需要的属性、时间、集合或交易关系；
- 唯一 gold answer；
- 一个明确错误但有竞争性的 designated false answer；
- 两条使用不同 ID 空间和不同记录类型的独立真实路线 `E_A`、`E_B`；
- 每条路线 3–6 个必要叶和 1–3 个连接键；
- 10–30 个与实体/日期重叠但不闭合答案的背景干扰文档。

由隐藏结构世界渲染公开文档。任何单一真实文档都不得直接说出 gold；只有连接一条完整路线或交叉两条路线才可确定答案。错误总结直接说出 designated false，但不能包含 gold。

文档文件名、URL slug、标题和 public metadata 均使用中性 UUID/随机 outlet，不允许出现 `gold`、`false`、`route_A`、`route_B`、`primary`、`copy` 等角色词。

### 4.3 复制谱系条件

同一题至少生成以下配对条件；除新增谱系文档外，其余 corpus bitwise-identical：

| 条件 | 新增内容 | 目的 |
|---|---|---|
| `clean` | 无错误总结 | 基础能力与 conditional deference 分母 |
| `F1` | 一个直接错误总结根，一个文档 | 重现直接答案捷径 |
| `F1_copy3` | 同根 3 个后裔；含转载和轻改写 | 低强度复制放大 |
| `F1_copy8_crossdomain` | 同根 8 个跨域改写后裔 | 测 URL/域名多样性失效和复制不变量 |
| `F2_independent` | 两个独立撰写、结论相同的错误根 | 测方法边界，防止把抗复制夸成普遍抗误导 |

最省 API 的第一轮可以只跑 `clean`、`F1`、`F1_copy8_crossdomain`、`F2_independent`，20 题共 80 cells/方法；`F1_copy3` 用于 property test 和第二轮曲线。若成本仍过高，先在所有 20 题上运行非 LLM 检索/证书测试，再只选择预先固定的 10 题做 agent smoke；但这 10 题结果不能当作 20 题正式效应估计。

### 4.4 复制生成不能给 estimator 送答案

至少准备三类同根后裔：

1. 带显式“据 X 报告”引用的转载；
2. 不带显式引用、保留稀有实体—数值—日期组合的编辑性改写；
3. 跨域、改标题、改段序、局部同义替换的洗稿。

estimated lineage 的阈值不能在测试 20 题上看 gold 调参。可用 4 个不进入评价的 dev-sanity world 固定阈值，或在运行前登记无监督阈值。若 paraphrase 由与 estimator 同源的模型生成，会产生隐藏偏置；最低限度应使用确定性模板 + 手写变体，后续 Formal 则需异源模型/人工生成并冻结。

## 5. Gold、oracle lineage、estimated lineage 的隔离

### 5.1 建议目录边界

以下是待实施的目录契约，不表示这些脚本现已存在：

```text
workbench_v009/drnoise_lineage_probe/
  config/
    spec_v1.json
  src/
    generate_worlds.py
    seal_bundle.py
    audit_bundle.py
    build_fts5.py
    estimate_lineage.py
    run_agent.py
    evaluate_private.py
  methods/
    react_baseline.py
    argus_cluster.py
    root_certificate.py
  tests/
    test_pair_identity.py
    test_no_role_leak.py
    test_copy_invariance.py
    test_grader.py
  data_v1/
    private_authoring/
      worlds.jsonl
      gold.jsonl
      route_membership.jsonl
      document_roles.jsonl
      lineage_full.jsonl
    public_runtime/
      questions.jsonl
      documents.jsonl
      condition_manifests/
      corpus.sqlite
    oracle_runtime_blinded/
      doc_to_opaque_root.jsonl
    estimated_runtime/
      lineage_edges.jsonl
      lineage_clusters.jsonl
  runs/
  evaluation/
```

`run_agent.py` 只能接受 `public_runtime` 及可选的盲 oracle/estimated 文件，命令行和配置中不得出现 `private_authoring` 路径。`evaluate_private.py` 是唯一读取 `private_authoring` 的入口。

### 5.2 oracle lineage：只暴露盲谱系，不暴露角色

oracle 机制上界文件只能包含：

```json
{"doc_id":"d-uuid","root_id":"r-random-uuid"}
```

要求：

- `root_id` 随机且不可从前缀区分真假/路线；
- 不含 `role`、`truth`、`route`、`gold`、`false`、`is_summary`；
- 一个错误总结及其复制后裔共享一 root，两个独立错误作者为两个 root；
- 每个真实底层记录按实际记录生成事件分配 root，而不是把整条真路线人为合并成一个 root；
- oracle controller 可以知道两文档同根，但不能知道该根是否可靠。

oracle 的用途只是回答：“如果复制谱系完美可知，证书机制是否能起作用？”它不能作为可部署主结果。

### 5.3 estimated lineage：只用公开可观察量

最小 estimator 不依赖新包，当前共享 Python 3.11.15 已有 `scikit-learn`、`numpy`、`scipy`、`networkx`，SQLite 3.53.2 含 FTS5。建议特征：

- URL canonicalization 和显式出链/引用；
- 发布时间方向（早→晚）；
- char 3–5 gram TF-IDF cosine；
- 稀有实体、数值、日期和短语的加权重合；
- 标题—正文交叉相似；
- 文档级引用声明。

先生成有向复制候选边，再以阈值图的弱连通分量或最早高置信祖先作为 estimated root。边/簇质量由 private evaluator 离线计算；estimator 自身看不到真根。

近重复基线应使用与 candidate **相同文本相似特征**，但只聚类去重，不利用时间/引用方向和根不相交路径。这样能防止 candidate 的收益仅来自更强文本编码器。

### 5.4 进程隔离与泄漏审计

1. `seal_bundle.py` 先从 private authoring 导出 public runtime，再把运行包复制到一个不含 private 文件的工作目录。
2. `audit_bundle.py --assert-no-role-leak` 扫描 public JSON keys、值、路径、文件名和 document IDs；出现角色词立即失败。
3. agent backend 只获得问题文本和 `search(query)` 结果，没有 filesystem 工具。
4. agent 原始输出只写 `runs/<method>/<condition>/<task>.json`，包括 final exact answer、citations、search calls、stop reason 和证书状态。
5. 所有方法完成后，独立运行 `evaluate_private.py` 合并 gold/route/lineage；方法不能收到任何在线 reward 或正确性反馈。
6. clean/noisy corpus 差异用文件哈希断言：`noisy = clean ∪ added_condition_docs`，共同文档内容逐字节相同。

## 6. 独立终局与指标

### 6.1 不需要同源 LLM judge

DRNOISE 的答案类型都可以确定性判分：实体/文本做规范化 exact match，日期转 ISO，布尔接受固定同义词，集合要求 exact membership，有序列表要求 exact order，金额解析为 Decimal。Run-local 探针应使用隐藏 world 直接生成 gold，再由独立 grader 计算；不要让 method 自己判断“我是否正确”。

路线闭合也离线判分：grader 将 agent citations 的 `doc_id` 与私有 `route_membership` 比对，报告完整 A 路线、完整 B 路线、仅部分路线、完全未取真路线。方法自己的“certificate closed”只能作为预测，不能当终局事实。

### 6.2 必报指标

- clean accuracy、各 noisy accuracy；
- conditional deference；
- complete route A/B acquisition；
- 在路线闭合前的 false stop rate；
- search calls、retrieved docs、tokens/费用（如可见）、latency；
- abstention / coverage；
- `duplication_sensitivity = P(decision(F1) != decision(F1_copyK))`；
- oracle-to-estimated performance gap；
- estimated lineage edge precision/recall/F1、pairwise cluster F1；
- `F2_independent` 的边界表现。

最核心的机制检查不是总准确率，而是：只添加同根后裔时，A 的准停决策是否保持不变；若 estimated lineage 下不变性消失，则 oracle 正向结果没有部署意义。

## 7. Argus + 近重复聚类强基线

Argus（arXiv:2605.16217）目前没有检索到官方代码，综述索引也没有 Code 链接。因此基线必须命名为 `argus_cluster_reimplementation`，并把与论文的差异写入实验元数据。

最低实现应与 candidate 共享：

- 同一 search backend、top-k、snippet 长度、LLM、系统提示、最大迭代和 token 预算；
- 同一 candidate-answer 原子主张抽取器；
- 同一 support / contradict / unverified 判定器；
- 同一 evidence/claim graph 和缺口驱动查询模板。

基线特有计算：

1. URL canonicalization；
2. 用与 estimated lineage 相同的 char-ngram/entity-value 特征做 near-duplicate clustering；
3. cluster 内只保留一个 source vote；
4. 对未验证主张找另一 cluster 的支持，对冲突找消歧证据；
5. 所有必要主张达到 `supported` 且没有未解冲突时停止。

candidate 唯一额外能力应是：方向化根推断、记录根折叠、根不相交支持证书，以及未闭合时的“寻找新根/反例根”动作。若 candidate 仅用不同聚类阈值或更多 prompt，不构成公平比较。

还应保留两个廉价基线：

- `url_two_source`：URL/domain 去重后两来源规则；
- `cluster_two_source`：near-duplicate cluster 后两簇规则。

如果 candidate 不能超过 `argus_cluster_reimplementation`，不应再扩大。

## 8. 命令级实施入口

下面是**待实现的可执行 CLI 契约**，本次没有创建这些脚本、也没有运行这些命令。路径和参数固定后，主线程可直接按此实现；命令中只有 evaluator 接触 private 目录。

### 8.1 生成、封装与审计

```powershell
$py = 'D:\Desktop\crl\env\crl_agent_v3\python.exe'
$probe = 'D:\Desktop\crl\20260813_1547_run10\workbench_v009\drnoise_lineage_probe'

& $py "$probe\src\generate_worlds.py" `
  --spec "$probe\config\spec_v1.json" `
  --seed 20260813 `
  --tasks 20 `
  --families all-10 `
  --out "$probe\data_v1\private_authoring"

& $py "$probe\src\seal_bundle.py" `
  --private "$probe\data_v1\private_authoring" `
  --public-out "$probe\data_v1\public_runtime" `
  --oracle-blinded-out "$probe\data_v1\oracle_runtime_blinded"

& $py "$probe\src\audit_bundle.py" `
  --public "$probe\data_v1\public_runtime" `
  --private "$probe\data_v1\private_authoring" `
  --assert-unique-gold `
  --assert-two-complete-routes `
  --assert-paired-identity `
  --assert-neutral-docids `
  --assert-no-role-leak
```

### 8.2 索引、谱系估计和不变量测试

```powershell
& $py "$probe\src\build_fts5.py" `
  --documents "$probe\data_v1\public_runtime\documents.jsonl" `
  --out "$probe\data_v1\public_runtime\corpus.sqlite" `
  --tokenizer unicode61

& $py "$probe\src\estimate_lineage.py" `
  --documents "$probe\data_v1\public_runtime\documents.jsonl" `
  --config "$probe\config\estimated_lineage_v1.json" `
  --out "$probe\data_v1\estimated_runtime"

& $py -m pytest `
  "$probe\tests\test_pair_identity.py" `
  "$probe\tests\test_no_role_leak.py" `
  "$probe\tests\test_copy_invariance.py" `
  "$probe\tests\test_grader.py" `
  -q
```

`test_copy_invariance.py` 必须构造同一支持根的 1、3、8 个后裔，并断言 oracle root-certificate 的 stop decision 完全一致；这个测试不调用 LLM。

### 8.3 方法运行

```powershell
$conds = 'clean,F1,F1_copy8_crossdomain,F2_independent'

& $py "$probe\src\run_agent.py" `
  --public "$probe\data_v1\public_runtime" `
  --method argus_cluster `
  --conditions $conds `
  --top-k 5 `
  --max-searches 20 `
  --output "$probe\runs\argus_cluster"

& $py "$probe\src\run_agent.py" `
  --public "$probe\data_v1\public_runtime" `
  --method root_certificate `
  --lineage estimated `
  --lineage-file "$probe\data_v1\estimated_runtime\lineage_edges.jsonl" `
  --conditions $conds `
  --top-k 5 `
  --max-searches 20 `
  --output "$probe\runs\root_certificate_estimated"

& $py "$probe\src\run_agent.py" `
  --public "$probe\data_v1\public_runtime" `
  --method root_certificate `
  --lineage oracle-blinded `
  --lineage-file "$probe\data_v1\oracle_runtime_blinded\doc_to_opaque_root.jsonl" `
  --conditions $conds `
  --top-k 5 `
  --max-searches 20 `
  --output "$probe\runs\root_certificate_oracle"
```

`run_agent.py` 还应要求显式 `--provider`、`--model`、`--temperature`、`--seed`，并在输出保存真实请求/响应模型身份、token、调用次数、错误和费用可见性。本报告不替主线程选择或调用付费后端。

### 8.4 独立终局

```powershell
& $py "$probe\src\evaluate_private.py" `
  --predictions "$probe\runs" `
  --private "$probe\data_v1\private_authoring" `
  --estimated-lineage "$probe\data_v1\estimated_runtime" `
  --out "$probe\evaluation\summary.json"
```

只有该命令读取 gold、designated false、route membership 和真 lineage。运行方法的进程不得导入 `evaluate_private.py`。

## 9. 已执行的轻量探针与未执行项

已执行：

- 打开 arXiv v1 摘要/HTML；
- 下载 v1 PDF 和 TeX 源包到系统临时目录并计算 SHA-256；
- 列出源包并检索代码/数据链接；
- GitHub Repository Search API、Hugging Face datasets API 和通用搜索；
- 在系统临时目录浅克隆 BrowseComp-Plus，固定到提交 `0469490...`，只读检查 README、docs、`pyproject.toml` 和 MIT LICENSE；
- 只读检查本机共享 Python 的 SQLite FTS5、scikit-learn、numpy、scipy、networkx 可用性。

未执行：

- 未下载 1.76 GB BrowseComp-Plus corpus 或任何大型模型/索引；
- 未安装 Java、Pyserini、FAISS、Qwen Agent 或其他包；
- 未创建 Run-local 合成数据或方法代码；
- 未调用任何 LLM/API；
- 未得到任何准确率、deference、lineage F1 或 cost 结果。

## 10. Blocker 与停止条件

### 10.1 当前硬 blocker

1. **DRNOISE 官方资产入口缺失**：阻止精确 benchmark 复现和外部有效性结论。
2. **DRNOISE 数据/代码许可证未知**：即使通过非官方镜像找到，也不能直接复用或再分发，需确认作者许可/官方来源。
3. **Argus 官方实现未定位**：强基线只能按论文重实现，必须披露 fidelity gap。

### 10.2 工程 blocker / 风险

1. BrowseComp-Plus 官方栈偏 Linux、Python 3.10、Java 21/Pyserini/FAISS；不应污染共享环境。需要时应建 Run-local 隔离环境，但当前最小探针可用 SQLite FTS5 避开。
2. SQLite FTS5 与论文的 Qwen3-Embedding-8B + Lucene 不同；正向结果不能外推到官方 retrieval setting。
3. 20 题模板合成可能过于规则，estimated lineage 可能因生成器指纹虚高。必须报告 oracle→estimated gap，并加入未用于调参的跨域改写。
4. `F2_independent` 会暴露 A 只防复制依赖的边界；若两个独立错误根通过证书，不能改口称“普遍抗错误总结”。
5. 如果 agent backend 具有 filesystem/tool 访问，private 隔离会失效；本设计要求 agent 只获得单一 search 工具。

### 10.3 实施 kill 条件

- property test 都无法保证添加同根副本不改变 stop decision；
- public bundle 泄漏角色/gold/route；
- estimated lineage 只能依赖合成器私有字段或 gold 调参；
- `argus_cluster` 和 candidate 的搜索/LLM 预算不能匹配；
- candidate 只在 oracle lineage 下有效；
- candidate 不优于 `Argus-style + near-duplicate clustering`；
- 改善完全来自更高弃答或更多搜索，在匹配 coverage/cost 后消失；
- 20 题正向但换一组冻结 seed/改写模板即消失。

## 11. 给主线程的非权威建议

先不要投入 BrowseComp-Plus 的大型索引或训练。按以下次序最省成本：

1. 实现 sealed 20-task synthetic bundle 与四个无 LLM tests；
2. 运行纯检索的 estimated-lineage 质量和复制不变量检查；
3. 只在预注册的 10 题 smoke 上比较 `cluster_two_source`、`argus_cluster`、candidate estimated、candidate oracle；
4. smoke 只有在 estimated candidate 超过 Argus+cluster 且 oracle→estimated gap 可接受时，才扩到完整 20 题；
5. 若路线存活，再联系作者/持续查找官方 DRNOISE 资产，或寻找另一个许可证明确的自然 misleading-evidence benchmark 做 Formal 外部验证。

当前实现判定：**机制探针可落地；官方 DRNOISE 复现不可落地；最关键的不可替代实验是 estimated lineage 对 Argus+近重复聚类的同预算优势，而不是 oracle 上界。**
