# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：20
- 关系评估行数：360
- 墙钟时间：1106.899 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 顺序不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen2.5:7b::strict::seed-123 | 20 | 0.250 | 0.100 | 0.850 | 0.600 | 0.300 | 0.500 | 0.700 | 0.150 | 0.100 |
| ollama::qwen2.5:7b::strict::seed-456 | 20 | 0.250 | 0.100 | 0.850 | 0.600 | 0.350 | 0.700 | 0.800 | 0.250 | 0.100 |
| ollama::qwen2.5:7b::strict::seed-789 | 20 | 0.300 | 0.100 | 0.850 | 0.650 | 0.450 | 0.700 | 0.800 | 0.250 | 0.100 |
| ollama::qwen2.5:7b::weak::seed-123 | 20 | 0.350 | 0.150 | 0.900 | 0.600 | 0.400 | 0.600 | 0.850 | 0.300 | 0.150 |
| ollama::qwen2.5:7b::weak::seed-456 | 20 | 0.400 | 0.150 | 0.850 | 0.650 | 0.450 | 0.500 | 0.800 | 0.350 | 0.150 |
| ollama::qwen2.5:7b::weak::seed-789 | 20 | 0.350 | 0.150 | 0.900 | 0.550 | 0.500 | 0.500 | 0.850 | 0.400 | 0.150 |
| ollama::qwen3:4b::strict::seed-123 | 20 | 0.600 | 0.200 | 0.750 | 0.900 | 0.500 | 0.700 | 0.950 | 0.200 | 0.200 |
| ollama::qwen3:4b::strict::seed-456 | 20 | 0.600 | 0.200 | 0.750 | 0.900 | 0.500 | 0.700 | 1.000 | 0.200 | 0.200 |
| ollama::qwen3:4b::strict::seed-789 | 20 | 0.600 | 0.200 | 0.750 | 0.900 | 0.500 | 0.700 | 1.000 | 0.200 | 0.200 |
| ollama::qwen3:4b::weak::seed-123 | 20 | 0.700 | 0.200 | 0.650 | 0.800 | 0.550 | 0.750 | 1.000 | 0.200 | 0.200 |
| ollama::qwen3:4b::weak::seed-456 | 20 | 0.650 | 0.250 | 0.650 | 0.850 | 0.550 | 0.850 | 0.950 | 0.250 | 0.250 |
| ollama::qwen3:4b::weak::seed-789 | 20 | 0.700 | 0.250 | 0.650 | 0.900 | 0.600 | 0.800 | 0.950 | 0.250 | 0.250 |
| ollama::qwen3:8b::strict::seed-123 | 20 | 0.450 | 0.400 | 0.800 | 0.750 | 0.550 | 0.550 | 0.950 | 0.400 | 0.400 |
| ollama::qwen3:8b::strict::seed-456 | 20 | 0.450 | 0.400 | 0.800 | 0.700 | 0.600 | 0.550 | 0.900 | 0.400 | 0.400 |
| ollama::qwen3:8b::strict::seed-789 | 20 | 0.450 | 0.400 | 0.800 | 0.700 | 0.650 | 0.500 | 0.900 | 0.400 | 0.400 |
| ollama::qwen3:8b::weak::seed-123 | 20 | 0.750 | 0.600 | 0.950 | 0.850 | 0.750 | 0.800 | 1.000 | 0.600 | 0.600 |
| ollama::qwen3:8b::weak::seed-456 | 20 | 0.750 | 0.600 | 0.950 | 0.850 | 0.700 | 0.800 | 1.000 | 0.600 | 0.600 |
| ollama::qwen3:8b::weak::seed-789 | 20 | 0.750 | 0.600 | 0.950 | 0.850 | 0.700 | 0.800 | 1.000 | 0.600 | 0.600 |

## 机械诊断

### deterministic_uptake_discrimination

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_plain_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `order_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### deterministic_correctness_agreement

- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### ollama_signal_agreement_with_exact_counterfactual_set

- `tool_value_overlap`：balanced_accuracy=0.5314614473030315，precision=0.30412371134020616，recall=0.5841584158415841，TP/FP/TN/FN=59/135/124/42
- `relevant_changed`：balanced_accuracy=0.6293436293436293，precision=0.3447098976109215，recall=1.0，TP/FP/TN/FN=101/192/67/0
- `selective_change`：balanced_accuracy=0.9633204633204633，precision=0.8416666666666667，recall=1.0，TP/FP/TN/FN=101/19/240/0
- `relevant_relation`：balanced_accuracy=0.8841698841698842，precision=0.6273291925465838，recall=1.0，TP/FP/TN/FN=101/60/199/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=101/0/259/0

### diagnostic_quadrants

- `single_correct_relation_pass`：101
- `single_correct_relation_fail`：86
- `single_wrong_relation_pass`：0
- `single_wrong_relation_fail`：173
- `one_shot_success_brittleness_rate`：0.45989304812834225
- `systematic_wrong_uptake_rate`：0.0

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。
