# P034 Reconciliation

- Disposition：`ACCEPTED_AS_NARROW_NEGATIVE_EVIDENCE`
- Read 1 SHA-256：`abfc3636c5fb8b8e654c481b1c8cb5d7f09a3dce552ae447f771a94a3c403681`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p034-a1/`
- Read-2 invocation SHA-256：`c01937df0a86cd992c86e5b05c265b4f6ccf34bd674d8ef703e33932875dfd4b`
- Read-2 report SHA-256：`52b9216d17b217c0f7a8ca6685047a57b19c6cf704a541312c73fef725fd8513`
- Accepted read-3 attempt：`read_3_attempts/r3-20260719-p034-a1/`
- Read-3 invocation SHA-256：`ad1041b98a926512e44944834a5e45c857ec2fa555f391c3b02630bafb4842e4`
- Read-3 report SHA-256：`6d742e848290d5775d32e68b2e4cb9c08f7978974a8465d1f7d880848081f524`

## Source reconciliation

- `AGREE`：self 条件只给极简“继续改写/无改进则停止”提示，不给 checklist 或缺陷定位；guided 条件把 GPT-4.1 判定失败的、参考答案派生 checklist 项回注，额外信息不同。
- `AGREE`：严格 Pass 变化很小，但细粒度 Acc 显示多模型退化；DeepSeek-R1 的 correct→incorrect 转移直接说明修订可破坏正确内容。
- `AGREE`：guided refinement 接近高 Pass 证明模型能遵循非常具体的失败项反馈，不等价于能自行发现缺陷，也不覆盖模糊/错误/冲突反馈。
- `RESOLVED_BY_SOURCE`：作者限制明确说明结果依赖领域、难度、prompt scaffold 与推理配置，不能解释为一般 self-refinement 不成立。
- `UNRESOLVED_NONBLOCKING`：`R^2=-0.477` 记号异常、提前 TERMINATE 后逐轮计分细节未明；不作为正式核心数值。

## Admission boundary

正式 Failure 只反证 RefineBench 的 checklist、极简无反馈提示、最多五轮和 GPT-4.1 evaluator 设置。它与 P033 共同支持“缺陷定位、修复执行、停止/选择必须分开”，不外推带 critic、工具反馈、搜索或训练后模型的一般 self-refinement。

