# v006 观察闭包效应证书参考实现

本目录实现一个严格限域的一元工具副作用合同编译器。它把 `EffectContract` 与 `ProjectionSpec` 编译为探针、关系、可辨识主张和不可辨识隐藏世界见证；执行后签发绑定工具、合同、投影、探针、计划与证据的覆盖记录，并由最小消费者失败关闭地作出接入决定。

## 主要文件

- `observation_closed_effects.py`：合同/投影数据模型、编译器、观察评价、证书签发和消费端。
- `independent_semantic_oracle.py`：不导入候选编译器的有限隐藏世界穷举判定器及见证验证器。
- `run_contract_panel.py`：契约敏感性、历史故障、基线和消费差分面板。
- `run_exhaustive_audit.py`：864 种支持组合、1,440 个语义判断和 6,048 个绑定变化的穷举审计。
- `toolsandbox_adapter.py`：锁定 ToolSandbox 工具的真实状态差分适配器。
- `run_toolsandbox_panel.py`：四种结构不同合同、23 个实现变体、同信息手写基线和 16 个证书消费场景。
- `run_full_evidence.py`：统一运行测试和三层证据，并生成 `evidence_summary.json`。
- `upstream_lock.json`、`upstream_evidence/`、`vendor/`：固定提交的文件锁、原始测试/许可证和最小本地依赖副本。

## 运行

从本目录调用：

```powershell
D:\Desktop\crl\.crl_external_cache\run08_v005\external_eval_venv\Scripts\python.exe -B run_full_evidence.py --output-dir <输出目录>
```

运行器使用 `-B` 禁止生成字节码，并以 `pytest -p no:cacheprovider` 禁止测试缓存。输出包括测试日志、契约面板、可辨识性矩阵、故障回归、消费场景、穷举审计、ToolSandbox 结果/计划/证书场景和总证据摘要。

## 语义边界

支持域只含一次调用、恰一个主效应、最多两类载荷因素和三类有限投影。编译器对非一元合同、未知因素、重复声明或无版本投影直接抛出 `UnsupportedContract`。序列、共享状态第二次调用、复合触发、异步、重试和多主效应没有被计划覆盖；消费者中的域外主张回归保证它们不能借已有证书被接纳。

明文可见投影保留身份；跨克隆稳定匿名投影只保留相等关系；克隆局部匿名投影不允许跨探针对齐。候选只为在相应观察等价类上真值恒定的主张生成关系，否则生成同观察、异真值见证。

## 安全声明

`record_digest` 与各 SHA-256 字段只提供字节绑定和意外篡改检测，不提供恶意签发者认证、密钥信任、生产环境授权或远程证明。生产系统若采用该协议，仍需数字签名、签发者信任根、重放防护和证据存储验证。

## 公平基线解释

同信息手写变形计划在 23 个 ToolSandbox 变体上与候选完全一致。本实现不主张新的变形关系或更高检出率；被检验的窄增量是自动计算投影闭包、输出不可辨识见证，并将结果绑定到失败关闭的接入消费者。
