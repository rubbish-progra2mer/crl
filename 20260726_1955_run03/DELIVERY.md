# Delivery Record

```json
{
  "review_id": "v001",
  "decision_sha256": "8aa4267b29f781f1435d2c532c975193633603a1c969cefbbe429bbd3c28a51e"
}
```

## Codex Delivery Text

# Candidate Implement Seed Delivery

RUN_ID: 20260726_1955_run03；获批版本 v001；交付日期 2026-07-26（Asia/Shanghai）。
本交付按 decision_v001.md（SHA 8aa4267b29f781f1435d2c532c975193633603a1c969cefbbe429bbd3c28a51e）
的绑定勘误 E1–E17 逐项执行；勘误全文以 decision 为准，本文标注 [E#] 指向对应勘误。

## Carrier-independent mechanism statement

在任何"自然语言约束规格 → LLM 生成可执行约束模型 → solver 求解 → 只检查返回解的认证 →
只由显式错误信号触发修复"的管线中，每个参考条件的 enforcement 可由模型可行集内的定向对抗
搜索度量：找到被模型接受、被参考条件拒绝的解，即为该条件未被 enforce 的构造性证书。全部
故障质量由此分解为三格——错误信号可见、解级检查捕获、对两类信号均不可见的静默掩盖格；
掩盖格的质量及其与可行集内"碰巧合规"频率（luck 指数 λ）的关系是经验量，其对错误触发修复
的不可见性是构造性质。**适用条件 [E16]**：参考条件须可在生成模型的决策词汇上机械表达
（本 harness 经接口合同保证）；对模型自建变量的野生管线需先构造解到参考 schema 的解码器，
此时 enforced 方向证书退化为单向（仅 SAT 方向经检查器复核成立）。"UNSAT ⇒ enforced" 只在
可行集级成立，不等于约束被忠实编码（钉子案例 idx127：未编码的 house_rule 被预算约束偶然
强制）[E11]。

## Implement path/SHA and exact command

冻结实现与输入（experiment_v001/artifacts/，完整 SHA-256 清单按 [E3] 绑定交接）：
- tp_lib.py = 74c21af7280c41def9e1a0fab75e81517c9f70e1168d601d9aff79064ea364d1（实例规范化 + 参考检查器，语义对官方评测器逐条保真，偏离已在头注释披露）
- tp_prompt.py = 6e89a8ac82ea41958c2c8b38097a105df681349a26612465ee225a94d2f1f5c8（F1 自由形式 / F2 一行清单 / A3 自查三个冻结模板）
- tp_api.py = 05388a7bbcf987d5524be2c95b6ecc557b613710a2ac7bb41d3c97679f2f73ac（DeepSeek 调用、退避、逐行 raw、脱敏）
- tp_solve_probe.py = 1757291f21a7cb3c4986fa5281affeac2081cc7e2a0092dc6baa6e2f3ee38224（域构建、生成代码执行、A5 探针、A4 行为测试、λ 采样、selftest）
- run_promotion.py = fdfbbc5316f5f949c4c2135fa9d059fdbd2bba231dbef14e133d2b103d215d95（逐实例交错编排 + 逐行 checkpoint）
- analysis.py = 6ab2b874b95bd9b7d4f55d62b378996fde4f7822f023a175a1870ce77ebe17fa（从 raw 独立重算全部指标）
- config.json = 71657f079c6fdf81ef08286079cbc1584fa7117176eb998369a534e358a1df1d；config_readiness.json = a68fa89cf00400f1619604691b487316773aee7835d8d80bce08d0b1fac9bbde
- input_bucket_D.csv = 3298b92ae09e44d79f09bd75f199fac7d896356db109be25140f89553c7b3b33；input_bucket_D_ref_info.jsonl = 24eb1337bb47ebcbf17f47fab6c01628673287474e0bcbab1be8f0facf790198；input_split_manifest.json = dfeaf9fe4688f9388576c6fbd36960eb095d1262bd8e2cf7e4c078551776dc7e

精确命令链：experiment_v001/captures/dev_001/execution.json（SHA 5191ec68…）记录完整
argv/cwd/inputs/outputs 哈希；metric_audit_001_execution.json（2141d28c…）记录指标重算捕获。
capture 目录三文件名保持 runner 原名。已知勘误：dev_001 wall = 577.1 s（result.md 的
"≈11.5 分钟"为误记）[E14]。

## Environment and raw experiments

编排：共享 .venv python 3.11.15；solver 载荷：run 根例外环境 .venv_z3（python 3.11.15 +
z3-solver 4.15.4，建立依据见 plan.md）；被试：deepseek-chat（84/84 响应 model 字段 =
deepseek-v4-flash，逐行记录），温度 0，max_tokens 4000，F1→F2→A3 逐实例交错。
原始数据：output_deepseek_raw.jsonl（aa6ebf9d…，84 调用逐行 provenance）、
output_results.jsonl（c63d084b…）、output_instance_files.zip（42d5b343…，224 成员内部 SHA
清单）、output_analysis_out.json（168235fc…）。全部指标已由三位 Reviewer 中的两位从 raw
独立重算、关键案例由两位独立重执行复现。API 用量：84 调用，78,282 prompt + 46,484
completion tokens（≈0.03–0.06 USD）；Workbench 另有 24 调用 38,436 tokens [E8]。
已知混杂 [E8]：温度 0 下 provider 端输出非确定性（同 prompt 两次 completion 不同）已实证；
dev_001 的具体故障集合含 provider 随机成分。

## Mechanism signature observed in Promotion Development

D 桶（fresh，instance-disjoint 预承诺）28 个 TP-SC3 实例，F1 自由形式条件：
- 状态：23 ok / 1 formalization_error / 3 default_unsat / 1 default_unknown。
- 解级认证 PASS 21/23；证书背书 enforcement 故障 3 例（witness 全部经独立检查器复核）：
  idx120 cuisine **masked**（量词结构误译：四菜系覆盖被编码为逐餐厅成员归属；λ=1.0，
  50/50 采样碰巧合规）；idx132、idx134 house_rule **caught**（λ=0.0）。
- **SIG-1 成立**：M2 掩盖率 = 1/21 = 4.8%，Wilson 95% CI [0.85%, 22.7%]。按 [E10] 明示：
  SIG-1 等价于 n_masked≥1，是存在性证书门，不是统计强度门。
- **SIG-2 primary 成立（λ 版，[E15]）**：masked λ 中位数 = 1.0 > 0.5（n_masked=1，单点中位数，
  如实声明）；λ 排序 masked(1.0) > caught(0.0) 成立；λ 对采样器选择稳健（Reviewer 2 双采样器
  1.0/0.92）。**一等负向结果 [E15]**：candidate 原 Claim 2 的域级违规选项密度方向预测失败
  （masked 0.784 > caught 0.325）；有效预注册为 plan.md 的 λ 版（先于 D 揭示冻结）；
  candidate→plan 的签名修订在此显式披露。λ 语义限定 [E17]：λ 为 blocking 枚举频率而非均匀
  测度概率。
- 掩盖质量成分披露 [E12]：M2 相对基准钦定语义定义；idx120 的成员归属读法有 NL 辩护余地
  （idx132 为无争议客观错误）；M2 不是客观编码 bug 率。
- 检测器比较（限"所比较的三个家族" [E6]）：同模型清单辅助自查 A3 对 3 例证书故障 0/3
  自信漏检（0/91 虚警；口径 = stated∧¬enforced，字面口径 3/91，见 [E9]）；行为测试 A4 3/3
  覆盖（0/68 虚警）——与探针持平，探针差异仅在证书性；错误信号 A2 对掩盖格覆盖为 0 系
  构造性质。未比较"结构化 LLM 裁决探针"家族（VeriSimpl/OptArgus 型），列入路线图 [E6]。
- F2 一行类别清单 scaffold：26 ok / 26 PASS / 0 证书故障——最便宜 scaffold 本批关闭静默通道
  （bundle 级；清单同时具语义消歧作用，见 [E12] 关联）。
- 跨桶形态重现：同型量词误译亦见于 W 桶 idx064/124/135；W→D 掩盖率 29%→4.8% 衰减
  （W 为 local 约束优先的有偏选择：W SC3 全集 26，falsifier 取 19 local + 3 easy [E8]）。
- harness 保真证据：probe–checker selftest 覆盖全部四类 local 类别（idx001 600 比较 +
  裁决前置补跑 idx064/122/135 共 600 赋值双向一致，0 不符 [E7]）；witness 复核
  all-confirmed；Workbench 曾有一次 2 实例中断试跑后完整重启（raw 日志自证；被弃响应经
  Reviewer 2 亲测同型结论，非择优 [E8]）。

## Closest-composition comparator evidence

外部未检得对认证掩盖分解的可运行竞争实现；存在探针参与但裁决者/用途/载体不同的组合
（VeriSimpl、Constraint Injection），均不计算认证 PASS 内的掩盖质量分解 [E1]。因此
comparator 采用内部臂矩阵（A1 解级认证 / A2 错误信号 / A3 同模型自查有利变体 / A4
ReLoop-CPT 载体内改编），在同一批冻结 F1 产物上实测；探针 delta 归因由设计保证（不改
生成侧、全臂共享产物）。具名最近邻与显式差异见下节。

## Narrow supported Claim and explicit non-claims

**Claim 上限** = decision_v001 "Supported claims" 节（三位 Reviewer 一致的最多支持清单），
全部限定于：TP-SC3 载体（官方验证集受控衍生：单城 3 日全槽位、硬约束+去重、本 harness
接口合同）、deepseek-v4-flash、温度 0、自由形式单次形式化；全部为 Development 级。

**禁止主张（FORBIDDEN）**：掩盖率数值外推；跨模型/载体/scaffold 泛化；官方 TravelPlanner
榜单、P051（其自报 val 93.3% / test 93.9%，公开页面另见 ~97%，口径差异未解析 [E5]）或
P055 结果重估；"探针覆盖优于行为测试"；slack/密度机制存活主张（密度方向已否证）；λ 的
概率解释；K2 探针触发修复有效性；无参考检查器场景可用性；A3 不可靠性普遍化；"首次发现
掩盖现象"或把探针算法（标准蕴含检查）当新方法 [E2]；C 桶执行前任何 confirmed 级语言。
**本交付的一切经验结论均未经 untouched 数据检验。**

## Reserved untouched Confirmation

- 载体：data_split_commitment_v001/bucket_C.csv（SHA 记录于 MANIFEST.json，dfeaf9fe…）与
  bucket_C_ref_info.jsonl 的全部 SC3 实例（tp_lib.normalize_sc3 非 None；预期 ≈11–12，
  实际由接收方执行时确定）。
- 未触碰证明：确定性 commit-reveal 分桶（规则 + salt 在读取任何实例内容前冻结并写入
  MANIFEST；三位 Reviewer 各自独立重算 180 行分配，逐索引一致）；物理分桶独立文件；
  冻结 config 只引用 bucket "D"；两个 capture 的 inputs 只含 D/W 路径；C 文件哈希未变。
  过程性成分（承诺时点先于读取）经 Reviewer 2 标注为不可哈希证明项，但未发现任何矛盾痕迹。
- 预注册计划（plan.md e53f6475…，冻结后未改）：同一冻结 artifacts 仅改 bucket 与 out_dir；
  执行前核对响应 model 字段与 dev_001（deepseek-v4-flash）一致性，不一致即为已知混杂如实
  披露；C-GATE-1 = C 桶 F1 认证 PASS 中证书背书掩盖实例 ≥2 且 Wilson 95% CI 下界 > 0；
  C-GATE-2 = C 桶 masked λ 中位数 > 0.5；两门独立报告；全部指标由 analysis.py 从 raw 重算。
- **功效警告 [E13]**：按 D 点估计 p̂=1/21，预期 C PASS n≈9–10 时 P(masked≥2)≈6.5–7.9%、
  P(masked=0)≈61%——C-GATE-1 是严酷 stability gate：失败不能区分现象不稳定与功效不足，
  通过则是强证据。接收方不得在看到 C 结果后回改门槛。更高功效否证路径按成本序：跨模型
  复跑（<1 USD）→ 180 全量复算 → C 桶。

## Nearest prior and unresolved collisions

截至 2026-07-26 无未解决碰撞；日期限定。具名最近邻与显式差异 [E1][E2][E4]：
- **VeriSimpl**（arXiv 2607.20474，v1 2026-05-24）：逐约束 solver 三型变异赋值探针，LLM 推理
  裁决可行性（其 Algorithm 2），best-of-n 选择用途，OR 载体——无参考检查器证书、无掩盖率/
  λ/三格分解、非认证审计。
- **ReLoop**（2602.15983）：OR 载体 feasibility–correctness gap 量化；引语 "Solver feedback
  catches syntax errors, not missing constraints"（§1 Introduction，逐字核验）。
- **Constraint Injection**（2606.04816）：训练用途探针；"Developing decoupled evaluation
  metrics that reflect independent constraint-violation profiles at finer granularity remains
  an open problem"（Limitations，逐字核验）；非 binding 掩盖概念句在其 Introduction。
- **Zhong–Yu–Klein 2020**（distilled test suites，NL→SQL）：认识论最近祖先。
- **Verus-SpecGym / Alloy LLM test cases / OptArgus / ConstraintBench**：相邻载体的规格
  验证/审计组合，差异见 reviewer_1.md §3.2 表。
- **概念谱系承认 [E2]**：软件测试 coincidental correctness / fault masking / survived mutants
  谱系（masked 格的概念祖先）；模型检测 vacuity/coverage 经典线（Kupferman–Vardi 系）；
  探针组件 = 标准约束蕴含/冗余检查。本 delta 的空缺只在测量分解与载体。
- 私有 prior 承诺：nearest_prior_v001.md SHA bf323e29b576e3ed3f75697cae8eab647912579a9dcaf9f6814acb389b165394
  在 Packet 冻结前预提交，正文未进入 Packet。

## Three independent reviews and Main Codex Decision

一轮三位 fresh 叶子 Reviewer（同一 Packet 741ea353…；互不可见；私有 prior 隔离）：
- reviewer_1.md（Prior and Lineage Attacker）= ef5297f359b84da5eca397ca3c78ea45c332059976fda33200e5e62d1aa2a21b：
  30 项哈希全验 + 13 条开放网络检索 + 6 次全文取回；无致命；发现 VeriSimpl；建议修订后交付。
- reviewer_2.md（Scientific Skeptic）= 6cafe0c2ed266671ca6e4f9db8c027ea468a47030d9be7341b3635530bff8552：
  全指标 raw 重算、idx120 自写代码重执行复现、分桶 180 行重算、被弃响应亲测、provenance
  逐条闭合；无致命；9 项可修复；建议修复后交付。
- reviewer_3.md（Implement Potential Reviewer）= 86f16f7f106ceb3de7453d908739b2068925d52bfd6cf50467802748d1487814：
  analysis 重算 JSON 全等、selftest 复跑、idx120 证书离线全重现；无致命；8 项修复；建议
  作为种子继续。
- decision_v001.md = 8aa4267b29f781f1435d2c532c975193633603a1c969cefbbe429bbd3c28a51e：
  DELIVER_IMPLEMENT，绑定勘误 E1–E17（全部 17 项异议 ACCEPTED/RESOLVED-BINDING，本文
  逐项执行）。

## Scale-up roadmap

成本序，每步都可杀死种子：
1. **跨模型复跑**（config 换 model 参数，<1 USD，小时级）——最大已知风险：更强模型故障率
   趋零则掩盖格空置，种子收窄为审计协议本身；F2 一行清单即 0/26 的提示敏感性加重此风险。
2. **180 全量验证集复算**（~$0.3，把 M2 CI 收紧到有决断力）。
3. **C 桶预注册 Confirmation**（≈36 调用；按上节功效警告解读）。
4. **λ 采样效度升级 [E17]**：近均匀采样（XOR-hash/随机化变量序）替代 blocking 枚举频率。
5. **补缺臂 [E6]**：结构化 LLM 裁决探针家族（VeriSimpl 型）加入检测器矩阵。
6. **野生管线扩展 [E16]**（第一个会碎的台阶）：模型自建变量管线需要解码器，enforced 证书
   退化为单向；先在 P052-LLMFP 式管线上做 SAT 方向审计。
7. **多城/全 TravelPlanner schema、第二载体（NL→调度）**：检查器重写工程量数天/载体。

## Known risks and falsification conditions

n_masked=1（单实例撑起机制信号）；M2 CI 宽 [0.85%, 22.7%]；W→D 衰减 29%→4.8%（构成敏感）；
密度代理方向已被否证；provider 端温度 0 非确定性（故障集合含随机成分）[E8]；C 门低功效
[E13]；单模型单载体单 scaffold；enforced 证书的可行集级语义与 applicable=false 的分母移出
[E11]；掩盖质量含 NL 歧义成分 [E12]；TP-SC3 为受控衍生载体非官方复算。每一条否证路径
（跨模型、全量、C 桶、近均匀 λ、缺臂补比）都便宜且已预注册或可预注册。

## Why further investment is justified

接收方拿到的不是想法而是可机械审计的工作系统：核心证书（可行集 SAT witness + 独立检查器
复核）被两位独立 Reviewer 用自写代码离线重现，全部发表数字被从 raw 独立重算，分桶承诺被
三方逐索引重验；认证侧测量空缺被占用者自认（P055 "no feasible alternative"）与两个最近邻
的逐字引语（ReLoop §1、Constraint Injection Limitations）从两侧夹证；harness 附带产出两个
立即可用的结论——同模型自查在证书对照下自信漏检 0/3、一行类别清单在本批关闭静默通道；
诚实的 Claim 天花板意味着交付内容无一需要在扩大前收回。扩大的第一笔支出（跨模型，<1 USD）
即是最强否证测试。

Delivery 是一颗**待扩大的研究种子**与投资建议，不是论文稿，也不是 harness 质量认证。
其全部经验结论明确未经 untouched 数据检验；该检验（C 桶按预注册门槛执行）与跨模型否证
是接收方扩大实验的第一步。
