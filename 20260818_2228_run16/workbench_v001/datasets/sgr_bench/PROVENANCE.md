# SGR-Bench 数据来源

- 数据集：PKUAIWeb/SGR-BENCH，`constraint_hf.jsonl`
- 来源页面：https://huggingface.co/datasets/PKUAIWeb/SGR-BENCH
- 下载地址：https://huggingface.co/datasets/PKUAIWeb/SGR-BENCH/resolve/main/constraint_hf.jsonl
- 下载时间：2026-08-18 +08:00
- 字节数：310505
- SHA-256：`b3a7200d6181a891c2bd7ab8045d8ef11e6ea837f736ceabff402520a690af34`
- 用途：Run16 内只读实验输入；不写回共享知识库。
- 上游论文：SGR-Bench: Benchmarking Search Agents on State-Gated Retrieval，arXiv:2605.22219v1。

本 Run 不声称重新执行 SGR-Bench 的真实网站交互。实验只复用其公开任务约束和 oracle answer set，构造独立的分页/完整性适配器，检验“局部结果能否支持不存在结论”。
