# 双向反事实工具证据测试结果

- 后端：`deterministic`
- 案例数：20
- 关系评估行数：100
- 墙钟时间：0.001 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deterministic::distractor | 20 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |
| deterministic::faithful | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| deterministic::ignore | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| deterministic::unstable | 20 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| deterministic::wrong_equivariant | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## 机械诊断

### deterministic_uptake_discrimination

- `tool_value_overlap`：balanced_accuracy=0.4666666666666667，precision=0.36363636363636365，recall=0.4，TP/FP/TN/FN=16/28/32/24
- `relevant_changed`：balanced_accuracy=0.8333333333333333，precision=0.6666666666666666，recall=1.0，TP/FP/TN/FN=40/20/40/0
- `irrelevant_plain_invariant`：balanced_accuracy=0.6666666666666666，precision=0.5，recall=1.0，TP/FP/TN/FN=40/40/20/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=0.8333333333333333，precision=0.6666666666666666，recall=1.0，TP/FP/TN/FN=40/20/40/0
- `irrelevant_invariant`：balanced_accuracy=0.8333333333333333，precision=0.6666666666666666，recall=1.0，TP/FP/TN/FN=40/20/40/0
- `selective_change`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=40/0/60/0
- `relevant_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=40/0/60/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=40/0/60/0

### deterministic_correctness_agreement

- `relevant_changed`：balanced_accuracy=0.75，precision=0.3333333333333333，recall=1.0，TP/FP/TN/FN=20/40/40/0
- `selective_change`：balanced_accuracy=0.875，precision=0.5，recall=1.0，TP/FP/TN/FN=20/20/60/0
- `relevant_relation`：balanced_accuracy=0.875，precision=0.5，recall=1.0，TP/FP/TN/FN=20/20/60/0
- `bidirectional_relation`：balanced_accuracy=0.875，precision=0.5，recall=1.0，TP/FP/TN/FN=20/20/60/0

### ollama_signal_agreement_with_exact_counterfactual_set

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### diagnostic_quadrants

- `single_correct_relation_pass`：0
- `single_correct_relation_fail`：0
- `single_wrong_relation_pass`：0
- `single_wrong_relation_fail`：0
- `one_shot_success_brittleness_rate`：None
- `systematic_wrong_uptake_rate`：None

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。
