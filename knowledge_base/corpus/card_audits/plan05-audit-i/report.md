# PLAN_05 Card source audit I report

- Audit ID: `plan05-audit-i`
- Role: fresh independent Card source auditor；不是 Candidate、Commissioning 或科研 Reviewer
- 总结论：两张 Card 均为 `PASS`

## 逐卡结论

| Card | 结论 | 最小修正 |
|---|---|---|
| `paper/paper-p084.md` | `PASS` | 无 |
| `failure/failure-semantically-related-toolkit-expansion.md` | `PASS` | 无 |

## 来源链核对

- 官方 PDF 实际 SHA-256 为 `8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7`，与 P084 manifest、SQLite paper record 及两卡 `source_refs` 完全一致。
- 两卡 `paper_id` 均为 `P084`，Card meta 均准确列出同一组四个 Evidence ID；所有行内 Evidence 引用均存在于该组中。
- `manifest.json` 中有且仅核对了 1 条 P084 record；`evidence.json` 与 scratch SQLite 中均有 4 条 P084 Evidence，逐字段一致。
- 四条 Evidence 的 `source_content` 均与 SQLite passage 的 `[quote_start:quote_end]` 精确逐字符相等；保存的 passage SHA 与对 passage 文本重新计算的 SHA 一致；SQLite 保存的 source-content SHA 与重新计算值一致：

| Evidence | Passage | Passage SHA-256 | Source-content SHA-256 |
|---|---|---|---|
| `ev-p084-expanded-toolkit-controlled-setting` | `P084:p0004:s0001` | `24569f556e418bb8f8655f657948e872f459ea3236a2e128704a8d14b86b74c2` | `ef529a2bfa93c286fc5c553150583882ca1fa7cc2bbc472e1817c5d2c9a22142` |
| `ev-p084-related-toolkit-error-types` | `P084:p0004:s0001` | `24569f556e418bb8f8655f657948e872f459ea3236a2e128704a8d14b86b74c2` | `a5b7de37609c028ac0d2e1f2316980cf05086d3dc5af1de8621cd33d618c07ab` |
| `ev-p084-expanded-toolkit-table` | `P084:p0005:s0001` | `da954c2860d69d3bed6d881a22c1eaf1de96e557f6c4b745c6e90503d5f2934a` | `e886e48120b57b38b6e5d21305d2d4d385decfe2ac21665c50418489549fc016` |
| `ev-p084-generated-tool-single-dataset-boundary` | `P084:p0005:s0002` | `5a7059bdb5f577af55b4630c10b74164811c095a5f86f1bd9912decf1705185d` | `c1610cde7ddaeb2976b5e8e591700a2b3c6fd1db4b519a760ec14731aeea07aa` |

## 主张核对

### `paper/paper-p084.md` — PASS

- AUTHOR_FACT 均受来源支持：数据为 200 个 single-turn BFCL test cases；expanded 条件保留 original query；平均工具数由 2.7 增至 5.6，即平均约加入 3 个 semantically related functions；评测只采用 BFCL 第一阶段的 AST construction，不包含 simulated execution。
- Table 2 的九组 expanded/original AST 绝对分数分别为：`0.925/0.965`、`0.905/0.945`、`0.950/0.965`、`0.965/0.975`、`0.870/0.945`、`0.870/0.925`、`0.890/0.915`、`0.870/0.925`、`0.885/0.905`。九个 expanded 分数均低于各自 original，Card 只主张该无歧义方向，没有夸大效应量。
- 错误类别文字准确回述作者原文：wrong function、wrong number of functions、wrong parameter assignment、parameter hallucination。Card 没有把 expanded-condition failures 内的类别占比误写成相对 baseline 的类别级增量。
- 单数据集及 related requests/tools 由多个 LLM 离线生成的限制准确；Card 未把离线生成流程或 cosine signature filter 写成在线 router 或已验证的成功修复。
- CODEX_SYNTHESIS 正确保留边界：没有声称 tool count 与错误单调因果；明确指出没有 equal-token 控制、没有 baseline 同口径类别分布、AST 不等于真实执行。
- Claude-3.5-Haiku 行确有印刷矛盾：`0.925 -> 0.765` 与 `(-11%)` 不符，`0.925 -> 0.870` 与 `(-2%)` 不符；按绝对分数计算约为 `-17.3%` 和 `-5.95%`。Card 明确拒绝复用该行印刷百分比，处理安全。
- Card 中涉及 P078 的 lineage 句未跨读 P078（invocation 禁止读取其他 Card/read）；本审计仅确认其对 P084 的窄表述——P084 提供了直接 toolkit-expansion interference Evidence——由 P084 来源支持。

### `failure/failure-semantically-related-toolkit-expansion.md` — PASS

- AUTHOR_FACT 的 200 cases、original request、2.7/5.6、平均约 3 个 related functions、九模型总体方向、AST-only、错误类别、单数据集和离线 LLM 生成边界均与 PDF、Evidence 和 exact passage 一致。
- “预期功能不同”没有被写成已证明的全量功能不等价：论文先生成 related-yet-different requests/tools，再以 signature embedding cosine similarity `> 0.8` 过滤；Card 进一步明确 `0.8` cosine filter 不是功能等价证明，边界恰当。
- Card 明确否定从单一 2.7→5.6 对照推出 function count 越多、错误必然单调上升；也明确否定 runtime malformed-argument exception 与端到端失败。错误事实始终停留在 AST construction 边界。
- Card 明确披露 prompt-length confound、未报告 decoding seeds/repeats、tool ordering、equal-token isolation 与 baseline 类别分布，因此没有把全部下降唯一归因于语义重叠，也没有声称各错误类别相对 baseline 的精确增量。
- possible repair 被标成 `CODEX_HYPOTHESIS`；Card 明说 P084 没有实现或验证在线 router，未登记成功 routing/filtering Operator。
- Warning for future candidates 是审计约束建议，不是被伪装成 P084 AUTHOR_FACT 的实验结论。

## 重点攻击项结论

| 攻击项 | 结果 |
|---|---|
| 类别级 baseline 增量 | 安全；两卡均明确未报告，未由 expanded-condition 类别占比反推增量 |
| 单调 tool-count 因果 | 安全；failure Card 显式否定，paper Card 仅报告单一受控对照 |
| equal-token isolation | 安全；两卡均未声称，且明确暴露 prompt-token/length confound |
| runtime malformed-argument exception | 安全；明确限定 AST，failure Card 显式否定 runtime/端到端外推 |
| 成功 router/filtering Operator | 安全；明确说明无在线 router，0.8 离线 filter 不是等价证明或成功修复 |
| Claude-Haiku 百分比矛盾 | 安全；保留绝对分数方向，明确不复用矛盾百分比 |

## 实际读取范围与 provenance

- 实际读取的任务资产：两张指定 P084 Card；P084 官方 PDF（重点直接核对物理页 3、4、5、7）；`manifest.json` 中仅 P084 record；`evidence.json` 中仅四条 P084 records；`knowledge.plan05_84_scratch.sqlite` 的 schema 及仅 P084 paper/evidence/passages；冻结的 `plan05-audit-i/invocation.md`。
- 治理/操作文件：工作区根 `AGENTS.md`、`crl_agent_v3/AGENTS.md`、`CRL.md`、`CRL_ENVIRONMENT.md`；本任务触发的本地 `evidence-quality-gate` 与 `pdf` 技能说明。
- 未读取 P084 read-2 report：官方 PDF 已消除来源歧义。
- 未读取任何旧 Card audit/disposition、production calibration/blind/retrieval 产物、其他 Card/read、Candidate、Commissioning、科研 Reviewer 或 saturation audit；未运行 retrieval；未修改任何 source asset。
- Model/version：invocation 时未提供可独立验证的运行时 model/version，本审计不作猜测。
- Procedural blinding：实际操作遵守 file-level allowlist；invocation 已说明完整 trace 不可用，因此不声称可由系统证明 complete blinding。
- Thread/task ID：`/root/plan05_p084_card_source_audit`。
