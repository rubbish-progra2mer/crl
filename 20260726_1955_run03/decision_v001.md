# Main Codex Decision

```json
{
  "review_id": "v001",
  "packet_sha256": "741ea35369def8513d7e6a3622c3498313012ff43f17d921f4eba7c26726362c",
  "reviewer_1_sha256": "ef5297f359b84da5eca397ca3c78ea45c332059976fda33200e5e62d1aa2a21b",
  "reviewer_2_sha256": "6cafe0c2ed266671ca6e4f9db8c027ea468a47030d9be7341b3635530bff8552",
  "reviewer_3_sha256": "86f16f7f106ceb3de7453d908739b2068925d52bfd6cf50467802748d1487814"
}
```

## Main Codex Decision Text

# Main Codex Decision

## Bound materials

- Packet：review_v001/packet.md = 741ea35369def8513d7e6a3622c3498313012ff43f17d921f4eba7c26726362c
- Reviewer 1（Prior and Lineage Attacker）：review_v001/reviewer_1.md = ef5297f359b84da5eca397ca3c78ea45c332059976fda33200e5e62d1aa2a21b
- Reviewer 2（Scientific Skeptic）：review_v001/reviewer_2.md = 6cafe0c2ed266671ca6e4f9db8c027ea468a47030d9be7341b3635530bff8552
- Reviewer 3（Implement Potential Reviewer）：review_v001/reviewer_3.md = 86f16f7f106ceb3de7453d908739b2068925d52bfd6cf50467802748d1487814
- 裁决前置核验：decision_support_v001/（扩展 selftest ×3、引语 locator 核验、C 门功效重算），不作 Promotion 证据。

主 Codex 在裁决前完整阅读了同一 Packet 全部冻结 bytes（本人冻结并在 run 中逐一生成/核验）、三份完整报告及其引用依据；对报告中的关键事实主张做了独立复核：三位 Reviewer 的逐项哈希回读一致（3×30 项交叉覆盖）；R2/R3 的独立重算与重探针结论与我方产物一致；R1 发现的 VeriSimpl（arXiv 2607.20474）已由我读其 abstract/HTML 确认身份与差异；两条近邻引语已由我取回原文逐字定位（见 E4）。三位 Reviewer 均确认 fresh 上下文、无委派、未读私有 prior 与 peer 报告；三份报告均满足统一报告合同（逐项读取回报、九项结构完整），全部计入三审。

## Objection-by-objection disposition

三份报告合计 0 条未解决致命异议、23 条可修复/条件性异议（去重后 17 项）。逐项处置如下；每一项 "ACCEPTED-BINDING" 都构成对交付文本的绑定勘误（errata），DELIVERY.md 必须按其执行。

**E1（R1-6.1，条件致命）VeriSimpl 补披露与新颖性限定。** ACCEPTED-BINDING。最近先行清单必须加入 VeriSimpl（arXiv 2607.20474，v1 2026-05-24）：逐约束 solver 生成三型变异赋值（含违反型）做诊断查询、由 LLM 推理裁决可行性（其 Algorithm 2）、用于 best-of-n 候选选择、OR 载体（NL4Opt/NLP4LP/CompOR/IndOR）。与本 delta 的差异如 R1 所述：无参考检查器证书（soundness 依赖 LLM）、非认证审计对象、无掩盖率/λ/三格分解、非 agent 规划载体。"外部无可运行竞争分解" 一律改写为："外部未检得对认证掩盖分解的可运行竞争实现；存在探针参与但裁决者/用途/载体不同的组合（VeriSimpl、Constraint Injection），均不计算认证 PASS 内的掩盖质量分解。"

**E2（R1-6.2）概念谱系承认。** ACCEPTED-BINDING。交付文本承认三条祖先线：(a) 软件测试 coincidental correctness / fault masking / survived mutants 谱系是 "masked 格" 的概念祖先，λ 对应其通过概率思想；(b) 模型检测 vacuity/coverage 经典线（Kupferman–Vardi 系）是 "检查通过≠约束起作用" 的组件级祖先；(c) 探针组件本身 = 标准约束蕴含/冗余检查。本 delta 的空缺只在测量分解与载体（认证时点、掩盖率、三格、λ、检测器矩阵、agent 规划载体）。

**E3（R1-6.3 / R2-5-1 / R3-5.5，三方一致）Packet manifest 缺实现字节；plan 截断哈希。** ACCEPTED-BINDING + 机器改进项。事实成立：11 项冻结实现/配置/输入不在 review_v001 manifest；其中 tp_lib/tp_prompt/tp_api 在冻结 bytes 内只有 8-hex 前缀。补救（本版本）：完整 SHA-256 清单在此绑定，随 DELIVERY 交接——tp_lib.py=74c21af7280c41def9e1a0fab75e81517c9f70e1168d601d9aff79064ea364d1；tp_prompt.py=6e89a8ac82ea41958c2c8b38097a105df681349a26612465ee225a94d2f1f5c8；tp_api.py=05388a7bbcf987d5524be2c95b6ecc557b613710a2ac7bb41d3c97679f2f73ac；tp_solve_probe.py=1757291f21a7cb3c4986fa5281affeac2081cc7e2a0092dc6baa6e2f3ee38224；run_promotion.py=fdfbbc5316f5f949c4c2135fa9d059fdbd2bba231dbef14e133d2b103d215d95；analysis.py=6ab2b874b95bd9b7d4f55d62b378996fde4f7822f023a175a1870ce77ebe17fa；config.json=71657f079c6fdf81ef08286079cbc1584fa7117176eb998369a534e358a1df1d；config_readiness.json=a68fa89cf00400f1619604691b487316773aee7835d8d80bce08d0b1fac9bbde；input_bucket_D.csv=3298b92ae09e44d79f09bd75f199fac7d896356db109be25140f89553c7b3b33；input_bucket_D_ref_info.jsonl=24eb1337bb47ebcbf17f47fab6c01628673287474e0bcbab1be8f0facf790198；input_split_manifest.json=dfeaf9fe4688f9388576c6fbd36960eb095d1262bd8e2cf7e4c078551776dc7e。三位 Reviewer 已经由该清单（capture/plan 记载）在场外核验实际字节一致。机器改进（不追溯改判）：后续版本 Packet manifest 必须包含实现/配置/输入 bytes；plan 模板停用截断哈希。

**E4（R1-6.4）近邻自认引语核验。** RESOLVED-BINDING（核验完成，无需降级）。ReLoop："Solver feedback catches syntax errors, not missing constraints; …"，逐字，locator = arXiv 2602.15983 HTML §1 Introduction；91.1%/0.5% gap 句同节，另见其 Table 5。Constraint Injection："Developing decoupled evaluation metrics that reflect independent constraint-violation profiles at finer granularity remains an open problem"，逐字，locator = arXiv 2606.04816 HTML Limitations；非 binding 掩盖句 "a candidate may introduce a spurious constraint or omit a required one while still matching the reference optimum, whenever the affected constraint is non-binding"，locator = Introduction。交付文本引用时附上述 locator。

**E5（R1-6.5）P051 数字口径。** ACCEPTED-BINDING。凡引用 P051 成功率一律写明 "其论文自报 validation 93.3% / test 93.9%（Claude 3 Opus）；公开页面另见 ~97% 表述，口径差异未解析"，并重申不重估其数字。

**E6（R1-6.6 / R3-5.6）检测器家族措辞限定与缺臂披露。** ACCEPTED-BINDING。M4 结论一律限定为 "所比较的三个家族（错误信号、同模型清单自查、选项消融行为测试）"；明示未含 "结构化 LLM 裁决探针" 家族（VeriSimpl/OptArgus 型），该缺臂列入扩大路线图。任何 "探针覆盖优于 A4" 的经验语言禁止（本批 A4 3/3 与探针持平；探针差异仅证书性）。

**E7（R2-5-2）selftest 覆盖夸大。** ACCEPTED-BINDING，且已机械补齐。事实成立：冻结 readiness selftest 只在无 local 约束的 idx001 上覆盖 3 类（600 比较），plan.md "全类别" 表述错误。补救：裁决前置核验中用冻结 tp_solve_probe.py selftest 模式对 W 桶 idx064（cuisine×2）、idx122（house_rule+room_type+transportation）、idx135（cuisine×4+room_type+transportation）补跑，合计 600 赋值、全部四类 local 类别双向（probe-true⟺checker-violated）覆盖，0 不一致（decision_support_v001/selftest_result_idx{064,122,135}.json）。plan 的该句在交付文本中按此更正；R2 指出的方向性（若有 bug 只会压低 M2，对 SIG-1 保守）一并记载。

**E8（R2-5-3 / R3-5.7）Workbench 双启动与分母披露。** ACCEPTED-BINDING。更正三处：(a) selection_context "Workbench 探针一次通过（无多次探针择优）" 更正为 "一次 2 实例试跑在中断后被完整重启（wb raw 日志 24 行/22 唯一 request_id 自证；被弃首跑响应经 Reviewer 2 亲自探针，结论同型，不构成择优）"；(b) falsifier_report 用量更正为 24 调用、38,436 tokens；(c) W 桶 SC3 全集 = 26（19 含 local + 7 easy），falsifier 的 22 = 全部 19 local + 3 easy，为有偏截断，W→D 衰减解释须含此选择细节。temperature 0 下 provider 端非确定性（同 prompt 两次 completion 不同）记为已知混杂——它同时意味着 dev_001 的具体故障集合含 provider 随机成分，是 C 桶复验必要性的又一依据。

**E9（R2-5-4）A3 虚警口径。** ACCEPTED-BINDING。文档化：A3 虚警 = stated=true ∧ enforced=false 且探针 enforced（0/91）；按字面 enforced=false 口径为 3/91（idx123/127/133，其 house_rule 未被代码编码、A3 语法层判断正确）；现行口径对 A3 有利、不夸大 delta。

**E10（R2-5-5）SIG-1 语义。** ACCEPTED-BINDING。交付文本明示：SIG-1（Wilson CI 下界>0）数学上等价于 n_masked≥1，是存在性证书门而非统计强度门；有实质功效内容的是 C-GATE-1。

**E11（R2-5-6）enforced 证书语义限定。** ACCEPTED-BINDING。"UNSAT ⇒ enforced" 只在可行集级成立（"可行集内不可违反"），不等于 "约束被忠实编码"：idx127 为钉子案例（代码明确未编码 house_rule，但违规酒店全部超预算 ⇒ 探针 UNSAT）。enforcement 剖面不得读作代码忠实度剖面。probe applicable=false（域内无违规选项）意味着该约束在该实例上不可检验并移出分母，一并文档化。

**E12（R2-5-7）掩盖质量的 NL 歧义成分。** ACCEPTED-BINDING。披露：M2 相对基准钦定语义（官方检查器的覆盖读法）定义；idx120 的成员归属读法有自然语言辩护余地，idx132 则是无争议客观错误；掩盖质量混有 "合理替代读法" 成分，不得读作客观编码 bug 率。

**E13（R2-5-8 / R3-5.8）C 门功效警告。** ACCEPTED-BINDING。随交付移交：按 D 点估计 p̂=1/21，C 桶预期 PASS n≈9–10 时 P(masked≥2)≈6.5–7.9%（n∈[8,12] 时 5.2–10.9%），P(masked=0)≈61%——C-GATE-1 失败无法区分现象不稳定与功效不足，通过则是强证据；接收方不得在看到 C 结果后回改门槛；更高功效的否证路径按成本序为跨模型复跑（<1 USD）与 180 全量复算。

**E14（R2-5-9）小误差更正。** ACCEPTED-BINDING。dev_001 wall = 577.1 s（≈9.6 分钟，非 result.md 的 ≈11.5 分钟）；wb 用量见 E8。

**E15（R3-5.1，条件致命）Claim 2 裁决：λ 版替换密度版。** ACCEPTED-BINDING（本裁决的核心勘误）。candidate_v001 Minimal Claim Contract 之 Claim 2 原文（掩盖故障违规选项密度低于捕获故障 + 预算收紧翻转）被 D 桶证据触及：密度方向实测相反（masked 0.784 > caught 0.325），预算翻转子句空集不可测。有效的预注册以 plan.md（先于 D outcome 揭示冻结）的 SIG-2 为准：primary = masked λ 中位数 > 0.5（成立，λ=1.0，n=1）；secondary = λ 排序（成立）。裁决：交付 Claim 2 改写为 λ 版；域级密度代理的方向预测失败作为一等负向结果交付；candidate→plan 的签名修订是合法的揭示前修订，此事在交付文本显式陈述，不留隐式。

**E16（R3-5.4）carrier-independent statement 前置条件。** ACCEPTED-BINDING。机制陈述追加适用条件："参考条件须可在生成模型的决策词汇上机械表达（本 harness 通过接口合同保证）；对模型自建变量的野生管线，需解到参考 schema 的解码器，此时 enforced 证书退化为单向（仅 SAT 方向经检查器复核成立）"。这是接收方扩大到审计既有管线时最先碎掉的台阶，列入扩大路线图首位风险组。

**E17（R3-5.3）λ 测量效度。** ACCEPTED-BINDING。λ 定义为 z3 blocking-clause 枚举频率，非均匀测度概率；R2 的双采样器稳健性（1.0/0.92）记载；接收方扩大前应改用近均匀采样（XOR-hash/随机化变量序）或报告多策略稳健性；C-GATE-2 按原预注册执行但其解释受此限定。

## Supported and unsupported claims

支持（全部限定于 TP-SC3 + deepseek-v4-flash + 温度 0 + 自由形式单次 + 本 harness 接口合同；Development 级、未经 untouched 数据）：三位 Reviewer §7/§6 的"最多支持 Claim"清单在实质内容上一致，采纳为交付 Claim 上限——掩盖格非空的存在性（1/21，Wilson CI [0.85%, 22.7%]，构造性证书经两位 Reviewer 独立重执行复现）；λ 机制方向的单案例信号（含 E17 限定）；三个被比较检测家族的覆盖事实（A3 0/3 自信漏检、A4 3/3、A2 构造性 0）；F2 一行清单本批关闭静默通道（bundle 级）；量词误译形态跨桶重现。

不支持（三份报告 §7/§8 并集，全部采纳为禁止清单）：掩盖率数值外推；跨模型/载体/scaffold 泛化；官方榜单/P051/P055 重估；"探针覆盖优于 A4"；slack/密度机制存活主张（密度方向已否证）；λ 的概率解释；K2 修复有效性；无检查器场景可用性；A3 不可靠性的普遍化；"首次发现掩盖现象"或将探针算法当新方法；C 桶执行前任何 confirmed 级语言。

## Decision and evidence reason

**DELIVER_IMPLEMENT**（绑定勘误 E1–E17，DELIVERY.md 必须逐项执行）。

理由：(1) 本版本真实完成了 Promotion Development（含内部臂矩阵 comparator 实测）、Seed Readiness Audit、三位 fresh 叶子 Reviewer 对全部冻结 bytes 的实际读取审查；三份报告零未解决致命异议，两条条件致命（E1、E15）已在本裁决中以绑定勘误解决。(2) 核心科学主张（掩盖格非空）由构造性证书支撑，被两位 Reviewer 用独立实现/自写代码重执行复现，被第三位 Reviewer 哈希级审计——这是本机器所能达到的最强内部验证。(3) 全部 17 项异议均为披露/措辞/机械层，无一触及数据角色、预注册或计算有效性；其中两项（E4、E7）已在裁决前置核验中用真实执行闭合。(4) 交付判据是"该机制值得投入扩大"：证书级测量分解 + 可复现 harness + 两个立即可用的负向/实践结论 + 明确的低成本否证路径（跨模型 <1 USD、180 全量、C 桶）满足该判据；n_masked=1、宽 CI、C 门低功效等薄弱面全部随勘误如实移交。DELIVER_IMPLEMENT 表示"值得投入扩大"，不表示"该方法已证实成立"；一切经验结论保持 Development 级，untouched Confirmation 随 DELIVERY 移交接收方执行。
