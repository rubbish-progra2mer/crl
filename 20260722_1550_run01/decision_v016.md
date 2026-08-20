# Main Codex Decision

```json
{
  "review_id": "v016",
  "packet_sha256": "2a98c56d0c7787806d3f219afbff972708a77f8569c23ff5777e24e0669c12c9",
  "reviewer_1_sha256": "5330053d5c3d8a8b967120a10fa8eaabfcde9269cfae083df2815dab033ed87b",
  "reviewer_2_sha256": "9d6ec0a3c4b3ebc48b71a768d6f57eb75a9b941f22aa214d4112845438c01f65",
  "reviewer_3_sha256": "a6d5086ef9baba1fd4457e3cb3919dc04309e7d84897dbfb163b40b82e625d33"
}
```

## Main Codex Decision Text

# v016 Main Codex Decision

## Disposition

`NO_GO_FOR_DELIVERY`

这是主 Codex在重新读取冻结 Packet、全部 frozen bytes、三份独立原始报告、私有 prior commitment 与影响裁决的一手来源后作出的科研裁决，不是评分、投票、gate 自动结果或多数意见。

v016 的执行、数据绑定和配对统计真实且可复现；它发现了 ToolFailBench 官方 coarse fabrication heuristic 与 required-answer substring contract 在固定 released traces 上的大量冲突。但是 v016 的实际 computation 是在 `G=true` 时完全忽略 `F`，现有证据不能把这一 override 交付为合理的完整 classifier、grounding method 或足够新颖的研究 implement。不得从 v016 创建 `DELIVERY.md`。

Run 保持 `ACTIVE`，系统保持 `DEVELOPMENT_NOT_COMMISSIONED`。下一版本必须改变科研内核；不得继续 RGP retuning、降低 gate、只改 Claim 文案或追加同构模型样本。

## Bound evidence re-read by the Main Codex

- Packet：`review_v016/packet.md`，80,939 bytes，SHA-256 `2a98c56d0c7787806d3f219afbff972708a77f8569c23ff5777e24e0669c12c9`。
- v016 Result：SHA-256 `50577be4959112f22c98224900419018105f075e87f708fa3ecdc2c308b1f547`。
- Reviewer 1 / Prior：SHA-256 `5330053d5c3d8a8b967120a10fa8eaabfcde9269cfae083df2815dab033ed87b`。
- Reviewer 2 / Scientific：SHA-256 `9d6ec0a3c4b3ebc48b71a768d6f57eb75a9b941f22aa214d4112845438c01f65`。
- Reviewer 3 / Potential：SHA-256 `a6d5086ef9baba1fd4457e3cb3919dc04309e7d84897dbfb163b40b82e625d33`。
- 私有 `nearest_prior_v016.md`：3,405 bytes，SHA-256 `e22e9e5d7d34c01d2fa9d8c802727f06470039287910c3833c593610d37fdfb7`，与 Packet commitment 相同。

主 Codex的 post-review readback 命令在第一次执行中已经读取并解释全部 179 项，但汇总阶段因 Development raw 文件实际带 `v015__development__` 前缀而 KeyError、退出 1。仅修正两个只读选择键后，同一审计退出 0；没有修改 Packet 或科研字节。最终 readback：

- 179/179 frozen supplementals，累计 `659,636,407` bytes；missing、byte-count、SHA、decode、parse error 均为 0。
- 108 JSON，累计遍历 10,316,330 个节点。
- 2 JSONL，共 22,000 行。
- 16 Python，全部 AST parse 成功。
- 34 Markdown，全文读取 368,710 characters。
- 16 capture BIN，全部读取；非空项 UTF-8 可解释。
- 3 PDF，共 49 页、190,336 extracted text characters，逐页读取。
- 三份 formal report 的内部 `reviewer_report` 均与各自 Reviewer session 首次完整 final 逐字符相等，且均绑定当前 Packet。

## What the evidence genuinely establishes

令 `G` 为官方 `answer_must_contain` / `match_mode` 子串合同满足，`F` 为官方 coarse output-fabrication predicate 为真。在 expected tool 已调用的 tool-required 行：

- 官方 `correct` 等价于 `G ∧ ¬F`；
- RGP `correct` 等价于 `G`；
- 唯一 changed quadrant 是 `F ∧ G`，官方输出 `output_fabrication`，RGP 无条件输出 `correct`。

所有 changed rows 均精确落在该象限，没有实现身份漂移。固定实验的 judge-relative 总体 accuracy 结果也真实：

- Development：10,000 rows，9,345 unanimous；187 changed；157 corrections / 1 regression；paired delta `+0.016693418940609953`。
- Confirmation：12,000 rows，10,792 unanimous；271 changed；195 corrections / 1 regression；paired delta `+0.01797627872498147`；model-cluster bootstrap 95% `[0.011547301103986307, 0.024226015729936882]`。
- Confirmation 的 generator models 与 Development 不重合；正向出现在 10/12 Confirmation models 与 5/5 固定 domains。
- v015 在任何 trace/judge JSON 解析前因 manifest SHA 字符错误退出；v016 只修正该绑定，program bytes 与科学函数未变。

因此当前证据最多支持：在固定 dataset revision、固定 1,000 tasks 和固定两条 released judge streams 上，用 G-only override 会提高规则分类器与两条 unanimous judge labels 的逐行一致率。这是 benchmark-specific measurement finding，不是答案真实正确性的证明。

## Fatal objections and Main-Codex resolution

### 1. G-only override is not a sound fabrication or correctness rule

Confirmation 的 271 changed rows 中只有 229 行有 unanimous reference；其分布是：

- 195 `correct`；
- 14 `tool_skip`；
- 19 `result_ignore`；
- 1 `output_fabrication`。

RGP 把 229 行全部输出为 `correct`。除 sole regression 外，还有 33 行是 official 与 RGP 都不匹配 unanimous label、只是错误类型发生变化。Development 也有 6 个此类 both-wrong changed rows。

唯一 Confirmation regression `qwen3.5-9b / RI-MED-014` 是机制反例：答案包含 required warfarin values，但增加了工具返回未支持的孕期时间窗、颅内出血、肝素替代、避孕、超声和 INR 管理建议；两条 judges 均判 `output_fabrication`，RGP 仅因 `G=true` 改成 `correct`。

Potential Reviewer 进一步复算：在 unanimous `output_fabrication` 类上，官方仅有 1 个 TP，而 RGP 把它也消除，RGP 的该类 recall/F1 为 0。总体 accuracy 提升与完整 taxonomy quality 不是同一结论。此异议阻止 classifier/method Delivery。

### 2. The allowed Candidate Claim still overstates semantic truth

Candidate 写“reduces deterministic false fabrication labels relative to two unanimous independent judges”。两条 judge outputs 来自不同模型与 overlay，但共享同一 base rubric、标签定义和数据构造；ToolFailBench 论文自己承认 judges 可能共享 blind spots。它们是两个分别运行的 released LLM judge streams，不是统计独立的人类 gold。

在 changed-unanimous 行中 34/229 明确不是 `correct`，因此不能把 195 个有利翻转整体解释为真实的 “false fabrication”。最多只能说 G-only override 减少 rule–judge disagreement。仅改写 Claim 会改变冻结 Candidate，而且即便完成也不会解决方法合理性或新颖性。

### 3. Closest-composition comparator was missing before Confirmation

CRL.md 要求：若存在直接且可运行的 closest-composition，必须在打开 Confirmation 前进入实验，不能用弱 baseline 或简单 ablation 代替。

主 Codex的前置 prior 已把 novelty ceiling 限定为 benchmark correction，但没有把 `required coverage + answer-wide claim support` 落实为 closest-composition comparator。Prior Reviewer 的独立开放检索与主 Codex复核确认：

- Bulian et al. 的 Answer Equivalence 要求候选既覆盖参考重要信息，也不加入 misleading / excessive information；
- RAGAS、RAGChecker、RAGVUE 已将 answer coverage/correctness 与 claim-level faithfulness 分解；
- RAGChecker 显式区分正确但无 context support 的 self-knowledge、hallucination 与 faithfulness；
- RAGVUE 的公开实现把答案拆为 atomic claims，并要求每个 material detail 都受 context 支持；
- EigenData 已公开更完整的 function-calling benchmark audit/repair pipeline，以 schema/implementation/reference 修复、outcome-aware state correctness 与 human functional-correctness judgments 验证。

v016 只比较官方 coarse `G∧¬F` 与 G-only，没有比较 `G + answer-wide support`、修正后的 F、atomic unsupported-claim detection 或 human adjudication。这个遗漏使“precedence 是合理修复”的识别不成立，并构成流程与科研上的致命异议。

### 4. Method novelty and contribution are insufficient

当前 upstream 中没有找到完全相同的 RGP patch，所以具体 bug 发现可能是独立的；但 RGP 没有新 predicate、表示、学习器或 inference mechanism，只把官方已有 `_answer_correct` 提前，并在 `F∧G` 象限删除 F。

这可作为 ToolFailBench erratum / benchmark maintenance finding，却不足以成为 CRL 目标下值得交付的优质 research implement。BFCL changelog 已将 possible-answer、normalization 和 evaluator 修订作为 benchmark maintenance；EigenData 已覆盖更强的 audit/repair pipeline。一个独立发现的具体 bug 不自动等于新方法贡献。

### 5. Confirmation supports model-disjoint fixed-task replication only

Development 与 Confirmation 的 generator models 完全不重合，但 1,000/1,000 task IDs 和 task JSON SHA 全部相同；111 个 unique Confirmation correction tasks 中有大量固定任务重复。它不能支持 task、template、endpoint、judge-family 或 benchmark generalization。此点不是单独的算术失败，但进一步限制交付价值。

## Reviewer objections handled without voting

- Prior Reviewer 的四项致命异议（方法新颖性、nearest fair baseline、人类真值/系统过接受、grounding 术语）全部由主 Codex接受，并由 frozen raw rows、官方代码及一手先行复核。
- Scientific Reviewer 认为最窄 fixed-data judge-agreement Claim 的执行/算术可成立，同时要求披露 task-identical、34 个 unanimous non-correct changed rows、sole regression 和非 human gold。主 Codex接受其证据边界；该边界不足以解决 research-implement 新颖性和缺失 comparator，因此不授权 Delivery。
- Potential Reviewer 认为可把 v016 作为 scoped ablation/measurement correction 交付，但明确阻止把它当默认 classifier、完整 taxonomy 或 production evaluator。主 Codex接受其可复现性判断，不接受“measurement correction 即满足本 Run Delivery”的推论，因为 CRL 要求 Candidate Implement + Minimal Claim Contract 经最近公平 comparator 后形成值得交付的研究 implement。

没有任何报告被票数覆盖；一个可信且经复核成立的致命异议已足以阻止 Delivery。

## Public primary bases rechecked by the Main Codex

- ToolFailBench paper v1: `https://arxiv.org/abs/2607.04686`；frozen PDF SHA `6588af66fd477d9764c20c52c2adb7d92fcbf6a788fe09713bc71916862d3009`；pp.3–7 的 rule/two-judge labeling、surface brittleness 与 shared-blind-spot limitation。
- Official detector at commit `c8be7fb0...`: `https://raw.githubusercontent.com/SoHarshh/ToolFailBench/c8be7fb0f1d295b1e116d7bd0e01d4c5e91f1653/evaluation/detect.py`；公开 LF source 与 frozen CRLF source 在换行归一后正文/AST 一致。
- Bulian et al. 2022: `https://aclanthology.org/2022.emnlp-main.20/`；frozen arXiv-layout PDF SHA `bd320a5183a6fb507f4e3ebfbff27eb76af647e68f55980ea4c6762907f62b40`；Definition 3.1, PDF p.4。
- Kamalloo et al. 2023: `https://aclanthology.org/2023.acl-long.307/`；frozen PDF SHA `61676b02aa277893a9ad9a4c9cf691a29ace32a47e6fe3b024d598632d318bd2`；pp.1–2, 5–6 的 long-answer hallucination/unattributable-information limitation。
- RAGChecker: `https://arxiv.org/abs/2408.08067` and official `computation.py` at commit `6091f08...`。
- RAGVUE: `https://aclanthology.org/2026.eacl-demo.35/` and official `strict_faithfulness.py` at commit `a370a6c...`。
- EigenData: `https://arxiv.org/abs/2603.05553`；benchmark auditing/repair 与 human-correlated outcome-aware evaluation。
- BFCL changelog: Gorilla commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`。

## Version closure and next boundary

v016 冻结为真实 negative Review Decision。不得覆盖 Candidate、Plan、implementation、captures、Packet、reports 或本 Decision。

下一版本 v017 必须满足：

1. 科学 computation 与 G-only precedence 不同；
2. 不再把 substring presence 称为 grounding；
3. 若继续 tool-output evaluation，必须同时处理 required coverage、answer-wide unsupported additions 与 tool-call correctness，并正面比较最近公平 baselines；
4. v016 Confirmation 已暴露，不能作为 v017 untouched Confirmation；
5. 若无法取得新的 prospective Confirmation 或可靠 truth construction，应转向另一个有可执行 Development/Confirmation 边界的研究问题，而不是停在本 Run。

`DELIVERY.md`: forbidden for v016.

System: `DEVELOPMENT_NOT_COMMISSIONED`.

Run status after Decision: `ACTIVE`.
