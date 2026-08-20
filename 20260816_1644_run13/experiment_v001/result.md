# v001 实验结果

## 记录

- `outcome-semantics-probe-001`：`SUCCESS`，记录型非支持实验，103.172 秒。该试运行错误地把合法空结果与普通完成拆成两个不同标签，不用于候选判断。
- `outcome-semantics-probe-002`：`SUCCESS`，记录型非支持实验，136.671 秒。修正为 `FINISH / RETRY / VERIFY / REVISE` 四动作空间，覆盖五种结果状态、每类两个表面模板、三个本地模型与四种输入条件。

## 主要结果

| 模型 | 原始响应 | 通用策略提示 | 自解析 | 显式分面契约 |
|---|---:|---:|---:|---:|
| `qwen2.5:7b` | 9/10 | 10/10 | 9/10 | 10/10 |
| `qwen3:8b` | 9/10 | 10/10 | 10/10 | 10/10 |
| `qwen3:4b` | 6/8 | 4/6 | 6/8 | 5/6 |

分母只计可解析输出。`qwen3:4b` 在各条件均发生结构化输出截断，因此不用于方法比较。

两个稳定模型在原始响应条件下都把一个“连接在提交后丢失、服务端结果未知、不得假设回滚”的案例从 `VERIFY` 错判为 `RETRY`。这支持状态语义混叠现象存在，但不支持显式契约作为独立方法：通用策略提示在两个模型上与显式契约同为 10/10，自解析在 `qwen3:8b` 上也达到 10/10。

## 判定

H1 的方法贡献被强基线吸收，停止扩展。现象作为负结果保留，不构造缩窄交付主张。

## 可审计材料

- 修正实验输出：`workbench_v001/outcome_semantics_probe_results_002.json`
- 修正实验记录：`experiment_v001/recorded/outcome-semantics-probe-002/record.json`
- 首次试运行记录：`experiment_v001/recorded/outcome-semantics-probe-001/record.json`
