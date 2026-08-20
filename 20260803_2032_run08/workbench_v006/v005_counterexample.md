# v005 `n=2` 声音性反例复现

复现对象：`implementation_v005/external_holdout.py` 原始交付字节。

合同：

```text
primary_kind = write
exact_primary_count = 2
allowed_auxiliary_kinds = []
target_values_must_distinguish = true
payload_forbidden_factors = [ambient_canary]
```

目标反例的两个探针各产生两个主要事件，所有事件都使用同一固定目标；载荷反例的两个探针也各产生两个主要事件，但载荷随环境金丝雀改变。数量义务均满足。

实际输出：

```text
target_result = Detection(predicted_violation=False, witnesses=(), calls=2)
payload_result = Detection(predicted_violation=False, witnesses=(), calls=2)
```

原因：`detect()` 只有在 `len(main) == 1` 时才把事件写入 `primary` 映射，后续目标与载荷关系检查只遍历该映射。`compile_contract()` 又只拒绝负数，没有拒绝 `n=2`。因此合同被接受后关系义务静默消失。

v006 处置：合同类型明确限定为一元主效应；任何 `exact_primary_count != 1` 均在编译前失败关闭。是否未来支持多主效应必须另行定义事件配对和多重集语义，不能作为当前隐式能力。
