# CRL Contract v3 本机环境事实

## 1. 文档职责

本文只记录当前宿主可用的路径、密钥注入、硬件、运行时和工具事实。科研流程、Reviewer 语义、实验充分性、资源决策和付费询问边界分别见 `CRL.md` 与 `CRL_REVIEWER_PROTOCOL.md`。

这些事实不是启动检查清单，不要求每轮复验。实际实验遇到差异时，以该次命令真实输出为准。

## 2. 固定位置

- 产品根：`D:\Desktop\crl`
- 机器根：`D:\Desktop\crl\crl_agent_v3`
- 共享知识库：`D:\Desktop\crl\knowledge_base`
- 默认 Python：`D:\Desktop\crl\env\crl_agent_v3\python.exe`
- 依赖快照：`CRL_ENVIRONMENT_LOCK.txt`
- GGUF 模型：`D:\Desktop\crl\models\gguf`
- llama.cpp：`D:\Desktop\crl\runtimes\llama.cpp\b10107`
- 固定 Reviewer CLI：`D:\Desktop\crl\runtimes\codex-cli\0.147.0\codex.cmd`

## 3. 当前硬件与 Python

- 操作系统：Microsoft Windows 11 IoT 企业版 LTSC，64 位。
- CPU：13th Gen Intel Core i5-13490F，10 核、16 逻辑处理器。
- 内存：约 31.84 GiB。
- GPU：NVIDIA GeForce RTX 5060 Ti，约 16 GiB 显存，计算能力 12.0。
- NVIDIA 驱动：591.86；驱动报告 CUDA 13.1。
- Python：3.11.15。

机器工具默认使用外置共享环境，不调用来源不明的裸 Python。研究需要新增或冲突依赖时，使用当前 Run 或用户指定的外部隔离环境；不静默升级 Python、PyTorch、sentence-transformers、transformers、tokenizers 或向量编码语义。

## 4. Codex App Goal 与固定 Reviewer CLI

Codex App 的 Goal runtime 是本次长时实现宿主；Reviewer 使用的 `codex exec` 是另一项本机运行事实，两者不能用版本号或能力结论互相替代。

实施 preflight 发现系统 PATH 上的 `codex-cli 0.111.0` 虽暴露 `--sandbox read-only`、`--json`、`--output-schema`、`--ephemeral` 等参数，但真实调用 `gpt-5.6-sol` 返回“requires newer Codex”，因此未被用作 Reviewer 后端。

机器在外置 `runtimes\codex-cli\0.147.0` 安装精确版本，不修改全局 CLI。真实 canary 已验证：

- `gpt-5.6-sol` 与 `model_reasoning_effort=xhigh` 可用；
- read-only、ephemeral、JSONL 事件和角色输出 schema 同时工作；
- fresh 临时 Codex Home 只复制保存的 `auth.json`，默认复用现有 CLI 登录，不引入独立 API 服务；
- 空工作目录、空 MCP 配置和最小环境下进程成功；
- canary 返回有效结构化 SCI 输出，事件中没有工具调用。

固定后端仍逐次保存 JSONL 事件并执行越界判废，不能把一次 canary 外推成永久平台保证。若精确 CLI 缺失、模型不可用、身份变化或事件审计不足，Reviewer 测量无效；不得静默回退到另一个 backend。

## 5. 本地模型与通用工具

当前可用资源包括 Ollama 模型 `bge-m3:latest`、`qwen3:4b`、`qwen2.5:7b`、`qwen3:8b`，GGUF `Qwen3-8B-Q4_K_M.gguf`，llama.cpp CUDA 运行时、Git、GPU、CPU 和开放网络。它们可按 Claim 需要自主使用，不因存在而必须调用。

网络、登录状态和速率限制以使用时事实为准。Reviewer 是明确例外：协议禁止网络和所有工具，后端以行为边界和事件审计实施该要求。

Windows PowerShell 5.1 读取 Markdown 时必须显式使用 `Get-Content -Encoding UTF8`；可用 `tools/run_python_utf8.ps1` 执行已保存 Python 脚本。

## 6. 外部 API 与密钥

产品根 `.env` 当前保存变量名 `DEEPSEEK_API_KEY`。密钥只能临时注入需要它的当前进程，不得回显，不得进入命令行参数、Markdown、源码、Run 文件、Recall、日志、Reviewer 材料或知识库。

外部 API 实验应保存脱敏请求配置、原始响应、provider、请求模型、可取得的响应模型身份、时间、调用次数、Token、费用和错误事实。无法取得的字段如实说明不可见。

## 7. Run 局部依赖与数据

优先复用兼容共享环境；需要安装新包或改变版本时，在当前 Run 或用户指定位置建立隔离环境，并记录路径、Python、关键依赖和创建方式。不要把完整虚拟环境作为 Reviewer 材料，也不要把例外环境升级成全局默认。

实验所需公开代码、数据和模型可下载到当前 Run 明确目录或用户指定外部缓存。不得覆盖未知数据，不得把跨 Run 科研材料放入共享缓存，不得把下载行为扩张为知识库维护。明显大容量、明显高费用、新账号/密钥/权限或危险环境修改按 `CRL.md` 先询问用户。
