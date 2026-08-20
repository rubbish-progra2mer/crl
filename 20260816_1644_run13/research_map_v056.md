# v056 研究图谱

## 运行内诊断事实

- `workbench_v056/diagnosis/v056-frontier-reset-004/report.md` 的权限为 `ADVISORY_NON_AUTHORITATIVE`；全文检索就绪，语义检索因本次未请求而降级。
- 诊断时当前版本没有实验、比较或评审记录；Run 已有 55 个科学版本，后段多为文献级关闭。因此本版本优先做现象级去重，不先构造方法。
- `v029` 的宿主安全控制仍被视为外部执行边界；本版本没有尝试规避控制，也没有研究可操作的过滤绕过。

## 候选 A：批量调用的部分成功

- [Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures](https://arxiv.org/abs/2608.02645) 已明确研究非原子工具故障，包括部分状态更新，并用后置条件核验、重试前核验和幂等键处理。
- 本 Run `v001` 已把合法空、明确失败、未知副作用、语义无操作与确认成功分开，并因通用策略提示和模型自解析吸收显式契约而终止。
- 结论：批量部分成功只是 `v001` 状态语义与公开非原子故障工作的交集，不构成新前沿。

## 候选 B：因工具缺口而不可达的任务

- [Do Agents Know What They Can't Do?](https://arxiv.org/abs/2605.28532) 以遮蔽关键工具构造不可行任务并评估智能体是否错误继续。
- [Agent Planning Benchmark](https://arxiv.org/abs/2606.04874) 已包含不可解任务；[HyperAgent](https://arxiv.org/abs/2608.02650) 又以工具模式超图识别能力缺口并扩展工具集。
- 结论：任务可行性判断、不可达证明和缺失能力定位均已有直接问题或方法覆盖。

## 候选 C：请求值—实际应用值偏差

- 候选例包括页长被封顶、时间被吸附到离散槽、质量等级被降级、退款额度被限制；响应仍呈成功形状，但同时给出请求值和实际值。
- [Failing Tools: Benchmarking LLM Agent Recovery Under Runtime Tool Failures](https://openreview.net/pdf?id=j7YsSnA64D) 已把“成功响应信任”与缺失一致性检查列为故障模式，并明确包括小数位移、总额与明细不一致、时间戳越界等值级偏差；其修复要求追踪预期后置条件并将工具输出视为可错证据。
- 本 Run `v001` 已覆盖成功外观与任务效果的分离，`v028` 已覆盖依赖真值维护，`v038` 已关闭数值/单位/尺度传递，`v044` 又说明执行差分见证的语义绑定不可靠。
- 结论：把响应字段命名为 `requested/applied/delta` 只是类型化后置条件与数值规范化的实例化，不改变计算结构。

## 研究决定

三条草案均在方法注册与本地实验前被直接工作或 Run 内负面记忆吸收。没有可支持论文级主张的剩余贡献差分，因此不运行重复性合成实验。
