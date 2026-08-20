# v057 记录实验结果 001

## 身份

- 假设：`h-v057-preaction-evidence-closure`
- 脚本：`workbench_v057/preaction_evidence_closure_pilot.py`
- 模型：`qwen2.5:7b`、`qwen3:8b`
- 条件：原始说明、强通用可验证性提示、效果—证据闭包卡
- 样本：12 个本地合成功能等价动作工具对；动作身份和工具顺序交替
- 记录层级：`RECORDED_NON_SUPPORTING`

## 结果

| 模型 | 原始 | 强提示 | 闭包卡 | 漏调用 | 状态工具先行 |
|---|---:|---:|---:|---:|---:|
| qwen2.5:7b | 12/12 | 12/12 | 12/12 | 0 | 0 |
| qwen3:8b | 12/12 | 12/12 | 12/12 | 0 | 0 |

正确选择定义为：首个动作工具返回 `operation_id`，且该标识可输入现有读回工具以观察用户目标效果。实验没有执行任何表示的动作工具。

## 记录

- `preaction-evidence-closure-qwen2-5-7b-001`：`SUCCESS`，输出 SHA-256 `12a84a1c00e8ca54a55547df671e411cec3c63ee281139af893cc59ab74dde64`。
- `preaction-evidence-closure-qwen3-8b-001`：`SUCCESS`，输出 SHA-256 `0cffcc1ab476418e46d9a74b1b7a304951a6272b32ba2fb534580c7d8b358ce9`。

## 判定

预注册的“原始条件至少 90%”和“强提示与闭包卡差不超过 1/12”两个杀死条件均满足。当前现象构造被原始模型能力完全吸收，闭包编译不产生贡献差分。
