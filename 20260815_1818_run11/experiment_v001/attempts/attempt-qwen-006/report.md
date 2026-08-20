# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：20
- 关系评估行数：360
- 墙钟时间：1142.227 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen2.5:7b::strict::seed-123 | 20 | 0.300 | 0.150 | 1.000 | 0.350 | 0.250 | 0.850 | 0.150 | 0.150 |
| ollama::qwen2.5:7b::strict::seed-456 | 20 | 0.300 | 0.100 | 1.000 | 0.450 | 0.250 | 1.000 | 0.250 | 0.100 |
| ollama::qwen2.5:7b::strict::seed-789 | 20 | 0.300 | 0.100 | 1.000 | 0.350 | 0.250 | 0.850 | 0.250 | 0.100 |
| ollama::qwen2.5:7b::weak::seed-123 | 20 | 0.250 | 0.100 | 1.000 | 0.350 | 0.150 | 0.650 | 0.100 | 0.100 |
| ollama::qwen2.5:7b::weak::seed-456 | 20 | 0.250 | 0.050 | 1.000 | 0.550 | 0.250 | 0.900 | 0.200 | 0.050 |
| ollama::qwen2.5:7b::weak::seed-789 | 20 | 0.250 | 0.050 | 1.000 | 0.600 | 0.250 | 0.850 | 0.200 | 0.050 |
| ollama::qwen3:4b::strict::seed-123 | 20 | 0.600 | 0.150 | 0.650 | 0.650 | 0.450 | 1.000 | 0.150 | 0.150 |
| ollama::qwen3:4b::strict::seed-456 | 20 | 0.600 | 0.150 | 0.650 | 0.650 | 0.450 | 1.000 | 0.150 | 0.150 |
| ollama::qwen3:4b::strict::seed-789 | 20 | 0.600 | 0.150 | 0.650 | 0.650 | 0.450 | 1.000 | 0.150 | 0.150 |
| ollama::qwen3:4b::weak::seed-123 | 20 | 0.650 | 0.200 | 0.700 | 0.750 | 0.450 | 1.000 | 0.250 | 0.250 |
| ollama::qwen3:4b::weak::seed-456 | 20 | 0.650 | 0.200 | 0.700 | 0.750 | 0.450 | 1.000 | 0.250 | 0.250 |
| ollama::qwen3:4b::weak::seed-789 | 20 | 0.650 | 0.200 | 0.700 | 0.750 | 0.500 | 1.000 | 0.250 | 0.250 |
| ollama::qwen3:8b::strict::seed-123 | 20 | 0.600 | 0.500 | 0.950 | 0.900 | 0.500 | 1.000 | 0.500 | 0.500 |
| ollama::qwen3:8b::strict::seed-456 | 20 | 0.600 | 0.500 | 0.950 | 0.900 | 0.500 | 1.000 | 0.500 | 0.500 |
| ollama::qwen3:8b::strict::seed-789 | 20 | 0.600 | 0.500 | 0.950 | 0.900 | 0.550 | 1.000 | 0.550 | 0.500 |
| ollama::qwen3:8b::weak::seed-123 | 20 | 0.700 | 0.700 | 0.950 | 0.900 | 0.700 | 1.000 | 0.700 | 0.700 |
| ollama::qwen3:8b::weak::seed-456 | 20 | 0.750 | 0.700 | 0.950 | 0.850 | 0.750 | 0.950 | 0.700 | 0.700 |
| ollama::qwen3:8b::weak::seed-789 | 20 | 0.700 | 0.700 | 0.950 | 0.850 | 0.700 | 0.950 | 0.700 | 0.700 |

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

- `tool_value_overlap`：balanced_accuracy=0.552734375，precision=0.3282828282828283，recall=0.625，TP/FP/TN/FN=65/133/123/39
- `relevant_changed`：balanced_accuracy=0.587890625，precision=0.33015873015873015，recall=1.0，TP/FP/TN/FN=104/211/45/0
- `selective_change`：balanced_accuracy=0.96875，precision=0.8666666666666667，recall=1.0，TP/FP/TN/FN=104/16/240/0
- `relevant_relation`：balanced_accuracy=0.841796875，precision=0.5621621621621622，recall=1.0，TP/FP/TN/FN=104/81/175/0
- `bidirectional_relation`：balanced_accuracy=0.994140625，precision=0.9719626168224299，recall=1.0，TP/FP/TN/FN=104/3/253/0

### diagnostic_quadrants

- `single_correct_relation_pass`：104
- `single_correct_relation_fail`：83
- `single_wrong_relation_pass`：3
- `single_wrong_relation_fail`：170
- `one_shot_success_brittleness_rate`：0.44385026737967914
- `systematic_wrong_uptake_rate`：0.017341040462427744

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。
