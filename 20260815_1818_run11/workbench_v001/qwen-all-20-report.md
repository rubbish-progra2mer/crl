# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：20
- 关系评估行数：120
- 墙钟时间：303.071 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen2.5:7b::strict | 20 | 0.400 | 0.400 | 1.000 | 0.800 | 0.800 | 0.950 | 0.700 | 0.400 |
| ollama::qwen2.5:7b::weak | 20 | 0.250 | 0.050 | 0.900 | 0.600 | 0.700 | 0.900 | 0.400 | 0.050 |
| ollama::qwen3:4b::strict | 20 | 0.450 | 0.200 | 0.600 | 0.750 | 0.600 | 1.000 | 0.250 | 0.200 |
| ollama::qwen3:4b::weak | 20 | 0.550 | 0.250 | 0.750 | 0.650 | 0.650 | 0.950 | 0.350 | 0.250 |
| ollama::qwen3:8b::strict | 20 | 0.450 | 0.400 | 0.700 | 0.900 | 0.700 | 1.000 | 0.500 | 0.400 |
| ollama::qwen3:8b::weak | 20 | 0.550 | 0.450 | 0.650 | 0.900 | 0.700 | 0.900 | 0.550 | 0.450 |

## 机械诊断

### deterministic_signal_discrimination

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_plain_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### ollama_signal_agreement_with_exact_counterfactual_set

- `tool_value_overlap`：balanced_accuracy=0.45210084033613446，precision=0.25396825396825395，recall=0.45714285714285713，TP/FP/TN/FN=16/47/38/19
- `relevant_changed`：balanced_accuracy=0.6647058823529411，precision=0.3804347826086957，recall=1.0，TP/FP/TN/FN=35/57/28/0
- `selective_change`：balanced_accuracy=0.8823529411764706，precision=0.6363636363636364，recall=1.0，TP/FP/TN/FN=35/20/65/0
- `relevant_relation`：balanced_accuracy=0.9117647058823529，precision=0.7，recall=1.0，TP/FP/TN/FN=35/15/70/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=35/0/85/0

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。
