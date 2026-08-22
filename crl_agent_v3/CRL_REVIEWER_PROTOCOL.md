# CRL Contract v3 固定 Reviewer 协议

## 1. 定位

固定 Reviewer 是 implementation 比较仪器，不是论文质量 oracle、投票器或 Delivery 分数 Gate。主 AI 研究者可以在不同 implementation revision 上多次送审；一次 materially changed implementation 对应一次正式 Review。Reviewer 只提供独立测量和意见，最终科研裁决始终属于主研究者。

本协议中的 `implementation` 是当前 Review 所绑定的可执行或可机械核验研究 artifact，不专指新算法。它可以承载方法、系统、基准/评价、可复现现象或具有机械核验载体的理论/分析贡献；固定评估器只评价 packet 中实际呈现且有 Formal / Review-support 依据的内容。没有相应载体和证据的纯概念主张不在当前正式 Delivery 的测量覆盖内。

`DIRECTED` Run 的 No-Go 与用户终止不要求 Reviewer。准备最终交付时，必须有一次绑定最终 implementation、最终 Seed 和有效 Formal / Review-support 实验的 final-delivery Review。

## 2. 冻结评估器

当前评估器位于 `evaluation/reviewer/CRL-EVAL-1.0/`，其定义由下列精确字节共同组成：

- `evaluator.json`
- `common.md`
- `SCI.md`、`EMP.md`、`ADV.md`
- `SCI.schema.json`、`EMP.schema.json`、`ADV.schema.json`

固定运行身份是 `gpt-5.6-sol`、`xhigh`、`codex-cli 0.147.0`、`codex_exec_jsonl_v1`。角色与总体权重为：

- SCI 35%：问题价值、最近工作分离、机制、科学具体性、Claim 校准；
- EMP 40%：实验有效性、基线公平、测量可靠性、稳健性/反证、结果强度；
- ADV 25%：复现追踪、混杂/泄漏控制、边界外推、对抗存活、证据可审计性。

每个维度取 0—4 整数，先按角色维度权重聚合，再按 35/40/25 聚合总体百分比。算法只做确定性算术，不设合格阈值。Prompt、结构化模式、权重、模型、推理强度、后端或隔离政策任一实质变化都必须升级 `evaluator_version`，不同版本不能无说明横向比较。

## 3. 固定输入包

每次 `review create` 生成不可覆盖的 `review_vNNN/evaluations/eval-NNNN/`，核心文件为：

```text
request.json
implementation_manifest.json
evidence_inventory.json
packet.md
```

`packet.md` 固定包含七个逻辑区域：

1. Implementation / Seed Overview
2. Closest Prior Evidence
3. Core Experimental Evidence
4. Baseline & Budget Facts
5. Ablation / Robustness / Falsification Evidence
6. Reproducibility Facts
7. Known Limitations

主研究者按 Run 相对路径选择各区材料；同一源文件不能重复进入多个区域。没有材料的区域明确渲染 `NOT PROVIDED`。所有源文件保存路径、大小和 SHA-256，packet 形成后不可修改。final-delivery packet 必须包含当前 `seed_vNNN.md` 和至少一个与当前实现匹配、有效且进入核心材料的 Formal attempt。

机器在 packet 尾部自动附加 Evidence Inventory。它列出当前版本全部 Formal attempt，标明与当前 implementation 的 `MATCH`、`MISMATCH` 或未知关系、有效性、状态和是否进入核心材料；列出与匹配 attempt 相关的全部 comparison；并列出当前版本全部 Recorded attempt 的身份、状态、关联关系和是否进入材料。清单只陈述事实，不判断实验好坏；其目的在于让 Reviewer 看见被选择和未被选择的证据，防止只挑漂亮结果。

final-delivery packet 另自动附加机器生成、确定性且限长的 Core Evidence Closure。它陈列所选 Formal attempt 的关键 Spec/Claim 身份、真实指标值及资源事实，并显示 Seed 显式 metric mapping 的解析结果和未映射数字 advisory；每个 attempt 最多展开 64 条指标记录，长文本和列表按公开上限截断并披露遗漏数量或内容哈希。代码、stdout/stderr 和大体量 raw JSON 不自动复制。已显式声明但机械错误的 mapping 会拒绝 final Review；没有 mapping 或仍有未映射数字不会仅因此被拒绝。

## 4. 三类身份键

```text
implementation_key = SHA-256(规范化 implementation manifest)
packet_key = SHA-256(packet.md 精确字节)
measurement_key = SHA-256(implementation_key + packet_key + evaluator_definition_sha256)
```

同一实现换了评审材料时，`implementation_key` 相同而 `packet_key`、`measurement_key` 改变；它是同一实现的另一项测量，不能伪装成完全无关的历史。实现目录任何受清单覆盖的字节变化都会产生新 `implementation_key`。

## 5. Fresh、输入与行为隔离

SCI、EMP、ADV 必须是三个 fresh、互不可见的调用，读取相同 `packet.md` 字节。固定后端为每个角色创建独立临时 Codex Home，只复制保存的 CLI 登录凭据；不复制配置、缓存、Skills 或 MCP。Reviewer 在空工作目录中以 read-only、ephemeral、结构化输出模式执行，中介服务器配置为空，环境变量为最小白名单。

Reviewer 协议明确禁止：

- 任何工具、Shell、文件读取/写入、浏览器、网络搜索或外部访问；
- 主动获取 packet 外科研材料；
- 看见其他 Reviewer 输出；
- 继续委派或修改 Run。

后端必须保存完整 `events.jsonl`、`stderr.bin`、`raw_output.json` 和结构化 `report.json`。每个角色保存实际 `codex --version` 原始输出，并与 frozen evaluator manifest 的 `codex_cli_version` 做规范化精确匹配；不可解析或不一致时该角色及整组 measurement 无效，不能占用 canonical 或 stability 身份。JSONL 出现工具或外部访问事件时，不论调用是否成功，整组三审都作废并保留原始证据；必须用新的 evaluation 重新运行。不能把“继承来的工具可见”或 Reviewer 自述“未使用工具”当成隔离证明。

## 6. 结构化输出与聚合

每个角色输出固定包含协议、角色、评估器、模型、推理强度、五维分数与逐维理由、角色诊断、关键风险、置信度和自由评审。字段、角色、模型、分数范围或诊断键不匹配均判无效。

三个角色都有效且没有越界事件时生成 `aggregate.json` 与 `aggregate.md`。原始角色意见不被聚合器改写；总体分只是精确权重算术，并明确 `score_is_gate: false`。

## 7. Canonical 与稳定性

每个 `measurement_key` 的第一次有效三 Reviewer 测量固定为 `CANONICAL_IMPLEMENTATION_SCORE`。后续完全相同 packet 的有效重复只记为 `STABILITY_MEASUREMENT`，报告全部总体分、均值、范围和总体方差，永远不替换 canonical。无效测量保留但不占 canonical。

这条规则禁止 optional stopping：不能无限复测后在均值有利时停下并改写正式成绩。也禁止只选择最高一次。相同 implementation 的所有不同 packet 测量按 `implementation_key` 关联展示；主研究者可以解释材料修订，但不能隐藏旧测量。

## 8. Decision 与最终交付绑定

`decision_vNNN.md` 的机器元数据绑定：

- implementation、packet、measurement 三类键；
- canonical evaluation ID 与 aggregate SHA-256；
- implementation manifest 与 Evidence Inventory SHA-256；
- SCI、EMP、ADV 三份 `report.json` SHA-256；
- 相同 implementation 的已知 Review 历史；
- 该 packet 是否为 final-delivery Review。

Reviewer 执行起点一次读取 `request.json` 和 `packet.md`，三份角色 `report.json` 同时记录该 request 精确字节 SHA-256、`packet_key` 与 `measurement_key`。finalize 只有在三角色身份全部与当前 request/packet 相同时才能产生 aggregate；执行后、汇总前的 request 或 packet 换绑不能成为有效 canonical 测量。canonical aggregate 记录已经过这一致性核验的 `request.json` 精确字节 SHA-256，并已通过自身 SHA-256 被 Decision 绑定；`packet_key` 则继续绑定 Reviewer 实际读取的 `packet.md` 精确字节。Delivery 前分别核验当前 request 与 packet 是否仍匹配这两个 canonical 身份，再重新计算当前 implementation manifest、Seed 和 Evidence Inventory。任何实现变化、Seed 字节变化、Formal/Recorded 证据增删改、角色报告变化、request 或 packet 变化都会使旧最终绑定失效。交付明确列出的 Formal attempt 必须在最终 packet 中与当前实现匹配、有效并被选择；旧实现的高分不能覆盖后来修改的实现。

对新的 final-delivery Review，Delivery 还会由当前 Seed、所选 Formal 和已验证 comparison 重建同一 Core Evidence Closure，复核其哈希及所有显式 metric mapping。该检查只认证研究者已声明引用的机械真实性，不要求为 Seed 中每个数字建立 mapping，也不判断指标是否足以支持科学主张。

上述绑定只证明 Reviewer 测量的是被冻结的 artifact 与材料。Seed 的核心贡献、artifact 实际承载的对象、Formal 的独立评价依据和 packet 中的主张必须科学对应；这种对应关系由主研究者诚实裁决，不由 implementation key、聚合分数或脚本自动认证。

## 9. 冻结校准

`evaluation/reviewer_calibration/` 中的 Weak、Medium、Strong、Unfair Baseline Trap 四包来自已批准 Proposal，fixture SHA-256 固定。首次 `CRL-EVAL-1.0` 校准每包运行一组三个 fresh Reviewer，不根据得分修改 Prompt 或 fixture。

接受语义是：

- `Strong > Medium > Weak`；
- Unfair Baseline Trap 不高于 Medium；
- Unfair 的 EMP `baseline_fairness` 与 ADV `confound_leakage_control` 明确重罚；
- 三角色分别聚焦科学、实验和对抗复现。

校准不是 Delivery Gate。它验证相对测量尺度和关键方向敏感性。

## 10. 操作入口

```powershell
python tools\crl.py review canary
python tools\crl.py review create --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --section 1=<RUN_RELATIVE_PATH> --section 3=<RUN_RELATIVE_PATH> [--final-delivery]
python tools\crl.py review run --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --evaluation-id <eval-NNNN>
python tools\crl.py review status --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --implementation-key <KEY>
python tools\crl.py review decide --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --body-file <RUN_LOCAL_FILE> [--measurement-key <KEY>]
python tools\crl.py review deliver --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --supporting-attempt <ATTEMPT_ID>
```

`review decide` 的正文文件必须是 Run 内安全 UTF-8、LF 文件。工具管理身份和真实性，不判断 Decision 的科研质量。
