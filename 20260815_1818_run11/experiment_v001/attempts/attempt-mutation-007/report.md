# 双向反事实工具证据测试结果

- 后端：`deterministic`
- 案例数：20
- 关系评估行数：180
- 墙钟时间：0.003 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 顺序不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deterministic::distractor | 20 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| deterministic::faithful | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| deterministic::ignore | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| deterministic::misdirected_selective | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| deterministic::position_first | 20 | 0.000 | 0.000 | 0.100 | 1.000 | 1.000 | 0.400 | 1.000 | 0.000 | 0.000 |
| deterministic::position_third | 20 | 0.100 | 0.000 | 0.250 | 1.000 | 1.000 | 0.400 | 1.000 | 0.000 | 0.000 |
| deterministic::repeat_only_unstable | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| deterministic::unstable | 20 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| deterministic::wrong_equivariant | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## 机械诊断

### deterministic_uptake_discrimination

- `tool_value_overlap`：balanced_accuracy=0.4857142857142857，precision=0.21052631578947367，recall=0.4，TP/FP/TN/FN=16/60/80/24
- `relevant_changed`：balanced_accuracy=0.7607142857142857，precision=0.37383177570093457，recall=1.0，TP/FP/TN/FN=40/67/73/0
- `irrelevant_plain_invariant`：balanced_accuracy=0.5714285714285714，precision=0.25，recall=1.0，TP/FP/TN/FN=40/120/20/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=0.6428571428571428，precision=0.2857142857142857，recall=1.0，TP/FP/TN/FN=40/100/40/0
- `irrelevant_invariant`：balanced_accuracy=0.6428571428571428，precision=0.2857142857142857，recall=1.0，TP/FP/TN/FN=40/100/40/0
- `order_invariant`：balanced_accuracy=0.6571428571428571，precision=0.29411764705882354，recall=1.0，TP/FP/TN/FN=40/96/44/0
- `selective_change`：balanced_accuracy=0.8571428571428572，precision=0.5，recall=1.0，TP/FP/TN/FN=40/40/100/0
- `relevant_relation`：balanced_accuracy=0.9035714285714286，precision=0.5970149253731343，recall=1.0，TP/FP/TN/FN=40/27/113/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=40/0/140/0

### deterministic_correctness_agreement

- `relevant_changed`：balanced_accuracy=0.728125，precision=0.18691588785046728，recall=1.0，TP/FP/TN/FN=20/87/73/0
- `selective_change`：balanced_accuracy=0.8125，precision=0.25，recall=1.0，TP/FP/TN/FN=20/60/100/0
- `relevant_relation`：balanced_accuracy=0.853125，precision=0.29850746268656714，recall=1.0，TP/FP/TN/FN=20/47/113/0
- `bidirectional_relation`：balanced_accuracy=0.9375，precision=0.5，recall=1.0，TP/FP/TN/FN=20/20/140/0

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
