# h-008 第一动作 2×2 杀手试验判定

## 证据身份

- 试验脚本：`positive_ack_factorial_pilot.py`。
- 有效 4B 结果：`positive_ack_qwen3_4b_first_v3.jsonl` 与同名 `summary.json`。
- 有效 8B 结果：`positive_ack_qwen3_8b_first.jsonl` 与同名 `summary.json`。
- `positive_ack_qwen3_4b_first.jsonl` 是服务超时诊断日志；只完成 3 格，不进入统计。
- `positive_ack_qwen3_4b_first_v2.jsonl` 的输出模式要求冗长 `report/rationale`，部分 JSON 被 128 词元上限截断并被旧解析器误记为 `finish`；该文件无效，不进入科学结论。原始截断文本被保留以解释修正。

## 设计

- 4 个写入域，每域 3 个任务，共 12 个配对任务。
- 独立因子为回执标签 `SUCCESS/AMBIGUOUS` 与隐藏效果 `applied/no_op`，每个模型 48 格。
- 同一任务四格共享系统提示、用户任务、工具表面、合成写调用、操作标识、最大步数和随机种子；效果在首次读状态前不可见。
- 只评价回执后的第一动作，允许 `read_state`、`retry_write`、`commit_downstream` 或 `finish`；隐藏状态机械判定 no-op 后的下游提交是否危险。
- 两模型均为本地 Ollama、`temperature=0`、`think=false`、最多生成 128 词元；有效运行无超时与解析错误。

## 有效结果

| 模型 | 回执 | 首次读回 | 首次盲重试 | 首次下游提交 | no-op 危险提交 |
|---|---:|---:|---:|---:|---:|
| qwen3:4b | SUCCESS | 0/12 | 0/12 | 12/12 | 12/12 |
| qwen3:4b | AMBIGUOUS | 0/12 | 11/12 | 1/12 | 1/12 |
| qwen3:8b | SUCCESS | 0/12 | 0/12 | 12/12 | 12/12 |
| qwen3:8b | AMBIGUOUS | 0/12 | 12/12 | 0/12 | 0/12 |

- `SUCCESS-AMBIGUOUS` 的 no-op 危险提交差：4B 为 `+0.9167`，8B 为 `+1.0`。
- `SUCCESS-AMBIGUOUS` 的首次读回差：两个模型、两个效果格均为 `0`。
- 隐藏效果不可能影响首次动作；同一标签下 applied/no-op 的配对一致性符合操纵设计。

## 解释与替代解释

- 标签确实因果改变了动作：肯定回执触发依赖提交，模糊回执主要触发盲重试。
- 但数据不支持 h-008 的强机制，即“AMBIGUOUS 相比 SUCCESS 会促使代理独立取证”。两个模型根本不读状态；差异是提交与重试之间的路由。
- 这个分叉几乎逐字复现 `Verified Tool Calls` 所讨论的两个既有风险：SUCCESS 被直接接受；AMBIGUOUS 下不经验证的重试可能重复效果。其包装器方法正是 verify-before-retry，而 ToolGate 又占据更一般的后置条件提交门。
- `Failing Tools` 已把 success-response trust、silent no-op、未读回和危险后续动作作为 FM1 与评价条件；本试验没有发现新的失败类型。
- 因而 2×2 只提高因果归因精度，不能单独形成足够的方法、现象或系统贡献；在 `AgentCheck` 的单响应受控复放与 `AgentAbstain` 的配对提交框架上，这也是直接可构造的配置。

## 决策

- h-008 不进入 Formal，不扩大模型和措辞样本。
- 状态转为 `prior_collision`：一般现象和方法被直接先行占据，唯一评价差分经实验后仍是明显消融/构造性组合。
- 可复用负面边界：未来候选不得只把工具响应与效果解耦、加入后置条件读回、或做成功/模糊标签消融；必须改变更深的验证选择计算或发现不能由现有配对故障框架直接配置的现象。
