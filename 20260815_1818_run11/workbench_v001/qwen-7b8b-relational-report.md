# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：5
- 关系评估行数：20
- 墙钟时间：47.908 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 三元精确 | 相关应变 | 无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen2.5:7b::strict | 5 | 0.400 | 0.400 | 0.600 | 1.000 | 1.000 | 0.600 | 0.400 |
| ollama::qwen2.5:7b::weak | 5 | 0.400 | 0.200 | 0.600 | 0.800 | 1.000 | 0.400 | 0.200 |
| ollama::qwen3:8b::strict | 5 | 0.600 | 0.600 | 0.800 | 0.800 | 0.800 | 0.800 | 0.800 |
| ollama::qwen3:8b::weak | 5 | 0.800 | 0.800 | 0.800 | 1.000 | 1.000 | 0.800 | 0.800 |

## 机械诊断

### deterministic_signal_discrimination

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### ollama_signal_agreement_with_exact_triple

- `tool_value_overlap`：balanced_accuracy=0.6000000000000001，precision=0.5714285714285714，recall=0.8，TP/FP/TN/FN=8/6/4/2
- `relevant_changed`：balanced_accuracy=0.8，precision=0.7142857142857143，recall=1.0，TP/FP/TN/FN=10/4/6/0
- `selective_change`：balanced_accuracy=0.85，precision=0.7692307692307693，recall=1.0，TP/FP/TN/FN=10/3/7/0
- `relevant_relation`：balanced_accuracy=0.95，precision=0.9090909090909091，recall=1.0，TP/FP/TN/FN=10/1/9/0
- `bidirectional_relation`：balanced_accuracy=0.95，precision=0.9090909090909091，recall=1.0，TP/FP/TN/FN=10/1/9/0

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。
