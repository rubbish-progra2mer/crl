# v052 研究地图

## Run 内事实诊断

- 按 `crl-active-diagnosis` 刷新全文索引并收集 `v052-frontier-reset-003`；诊断权威性为 `ADVISORY_NON_AUTHORITATIVE`，不自动选择或杀死候选。
- Contract 版本为 3；当前 v052 没有实验、比较文件、评审文件或正式检索快照。
- Run-wide 已识别 51 个科学版本。全文索引为 `READY`，含 56,019 个分块；语义索引因未请求而单独为 `DEGRADED`。
- 索引组成报告无污染、无陈旧源，正式历史检索快照为 16 个、原始结果约 29.68 MB。
- 事实路径：`workbench_v052/diagnosis/v052-frontier-reset-003/`。

## 异步工具直接先行工作

- *Asynchronous LLM Function Calling* 以中断机制在函数返回时异步通知正在生成的语言模型，并给出上下文协议和适配训练。
  - https://arxiv.org/abs/2412.07017
- *Asynchronous Tool Usage for Real-Time Agents* 直接采用事件驱动有限状态机，使工具、用户输入和模型处理能够异步并发。
  - https://arxiv.org/abs/2410.21620
- *Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs* 以符号化未来值表示未解析工具结果，在依赖允许时并行，并在不修改模型/函数的执行层实现。
  - https://arxiv.org/abs/2605.15077
- ASYNCTOOL 已把任务内步骤依赖和工具响应延迟共同纳入异步多任务评测。
  - https://openreview.net/forum?id=FfedFHs6Tx

## 结论

未来对象、依赖允许的并行、完成中断和事件驱动状态机已逐项覆盖候选计算。v052 不注册正式假设。
