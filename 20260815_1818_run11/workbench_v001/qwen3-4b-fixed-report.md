# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：5
- 关系评估行数：10
- 墙钟时间：43.460 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 三元精确 | 相关应变 | 无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen3:4b::strict | 5 | 0.000 | 0.000 | 0.200 | 0.800 | 1.000 | 0.200 | 0.000 |
| ollama::qwen3:4b::weak | 5 | 0.000 | 0.000 | 0.200 | 0.600 | 1.000 | 0.200 | 0.000 |

## 机械诊断

### deterministic_signal_discrimination

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `dual_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### ollama_signal_agreement_with_exact_triple

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/10/0
- `relevant_changed`：balanced_accuracy=None，precision=0.0，recall=None，TP/FP/TN/FN=0/2/8/0
- `selective_change`：balanced_accuracy=None，precision=0.0，recall=None，TP/FP/TN/FN=0/2/8/0
- `dual_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/10/0

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。
