# v007 原型

- `typed_model.py`：封闭类型合同、投影、计划、观察、报告、证明和接入请求；规范 UTF-8 JSON 与 SHA-256。
- `compiler.py`：有限公式/投影族的观察等价类枚举、真值表监控器和不可识别见证合成；计划规范重编译。
- `protocol.py`：从原始观察重算报告、HMAC-SHA256 共享密钥签发、有效期/随机数/重放与失败关闭消费。
- `test_protocol.py`、`attack_audit.py`：协议、计划、见证和旧反例回归。
- `small_model_audit.py`：不调用候选求值器的有限模型预言机。
- `large_pilot.py`：SQLite 强一致与 Git 两轮异步收敛服务的 820 案例持留面板。
- `run_full_evidence.py`：正式证据总入口。

默认运行时：`D:\Desktop\crl\crl_agent_v3\.venv\python.exe`。本原型不需要网络、第三方密码库或真实凭据；测试签名密钥是文件内合成常量，不得用于生产。
