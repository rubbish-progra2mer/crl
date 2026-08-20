# 双向反事实工具证据测试结果

- 后端：`deterministic`
- 案例数：5
- 关系评估行数：20
- 墙钟时间：0.000 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 三元精确 | 相关应变 | 无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deterministic::distractor | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 |
| deterministic::faithful | 5 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| deterministic::ignore | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| deterministic::unstable | 5 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## 机械诊断

### deterministic_signal_discrimination

- `tool_value_overlap`：balanced_accuracy=0.5333333333333333，precision=0.2727272727272727，recall=0.6，TP/FP/TN/FN=3/8/7/2
- `relevant_changed`：balanced_accuracy=0.8333333333333333，precision=0.5，recall=1.0，TP/FP/TN/FN=5/5/10/0
- `irrelevant_invariant`：balanced_accuracy=0.8333333333333333，precision=0.5，recall=1.0，TP/FP/TN/FN=5/5/10/0
- `selective_change`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=5/0/15/0
- `dual_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=5/0/15/0

### ollama_signal_agreement_with_exact_triple

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `dual_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。
