# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：20
- 关系评估行数：120
- 墙钟时间：348.453 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen2.5:7b::strict | 20 | 0.400 | 0.400 | 1.000 | 0.800 | 0.700 | 0.900 | 0.700 | 0.400 |
| ollama::qwen2.5:7b::weak | 20 | 0.250 | 0.050 | 0.900 | 0.600 | 0.700 | 0.900 | 0.400 | 0.050 |
| ollama::qwen3:4b::strict | 20 | 0.400 | 0.200 | 0.600 | 0.750 | 0.650 | 0.950 | 0.250 | 0.200 |
| ollama::qwen3:4b::weak | 20 | 0.600 | 0.250 | 0.800 | 0.600 | 0.650 | 0.900 | 0.350 | 0.250 |
| ollama::qwen3:8b::strict | 20 | 0.450 | 0.400 | 0.750 | 0.900 | 0.600 | 0.900 | 0.500 | 0.400 |
| ollama::qwen3:8b::weak | 20 | 0.600 | 0.500 | 0.650 | 1.000 | 0.700 | 1.000 | 0.600 | 0.500 |

## 机械诊断

### deterministic_uptake_discrimination

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_plain_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### deterministic_correctness_agreement

- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### ollama_signal_agreement_with_exact_counterfactual_set

- `tool_value_overlap`：balanced_accuracy=0.4484126984126984，precision=0.25806451612903225，recall=0.4444444444444444，TP/FP/TN/FN=16/46/38/20
- `relevant_changed`：balanced_accuracy=0.6547619047619048，precision=0.3829787234042553，recall=1.0，TP/FP/TN/FN=36/58/26/0
- `selective_change`：balanced_accuracy=0.8809523809523809，precision=0.6428571428571429，recall=1.0，TP/FP/TN/FN=36/20/64/0
- `relevant_relation`：balanced_accuracy=0.9107142857142857，precision=0.7058823529411765，recall=1.0，TP/FP/TN/FN=36/15/69/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=36/0/84/0

### diagnostic_quadrants

- `single_correct_relation_pass`：36
- `single_correct_relation_fail`：18
- `single_wrong_relation_pass`：0
- `single_wrong_relation_fail`：66
- `one_shot_success_brittleness_rate`：0.3333333333333333
- `systematic_wrong_uptake_rate`：0.0

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。
