# v071 失败归因

## 失败标签

`FALSIFIED_BY_ZERO_EXECUTOR_COMPENSATION_GAP`

## 证据

- Recorded 记录：`executor-compensation-qwen2-5-7b-001`；
- 20/20 输出为有效 JSON；
- 严格执行器与宽容执行器均成功 20/20；
- 补偿差 0/20，补偿修复族 0/5；
- 结果文件 SHA-256：`bce90ceecfbcc256fdf2feaec7ecdf9006ff0858c20918e7e9cb0de720c5867e`。

## 杀伤范围

明确工具契约、单步动作、五类机械修复的本地条件下，没有证据表明宽容执行器系统性替 `qwen2.5:7b` 完成动作构造。不得删除契约信息、故意增加歧义或注入错误动作来恢复该现象。

## 非归因

- 不是运行失败：Recorded 状态为 `SUCCESS`，stderr 为空；
- 不是结构化输出失败：20/20 JSON 有效；
- 不是宿主安全控制：只调用本地模型并离线校验良性合成动作；
- 不是 Run 终局：只关闭当前执行器补偿假设。

## 决策

H-v071-1 判为 `falsified`，按预注册规则早停第二模型。Run 保持 `ACTIVE`，转向结构不同的前沿。
