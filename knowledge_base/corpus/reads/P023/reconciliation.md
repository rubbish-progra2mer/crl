# P023 Reconciliation

- Disposition：`ACCEPTED_WITH_NARROWING`
- Read 1 SHA-256：`7abf6ae09aa3ae0e112bea90a171892a141e9cd3ca55b911182e7714030058c5`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p023-a1/`
- Read-2 invocation SHA-256：`794f461432f9d825f6c8622a8692065aafb44dac824552d6493c16afb97928b9`
- Read-2 report SHA-256：`634164383b27e048d501fdc12f9b3a58924d6529a454efc9eb8071ca52341a84`
- Accepted read-3 attempt：`read_3_attempts/r3-20260719-p023-a1/`
- Read-3 invocation SHA-256：`984bf12525fdc755a3263900f9a5060864392db0832cf4341a89cba443ef5d04`
- Read-3 report SHA-256：`843f452bd0abd8aad61487ccfdf9f1c0ce8a94249391729dcfadbcfe959ed09d`

## Source reconciliation

- `AGREE`：方法按 query 级联选择协作模式/规模、角色与异构模型，训练 reward 使用 benchmark oracle answer。
- `AGREE`：方法结构可定义为 meta-control Operator，但组件随机化消融、不同模型池与价格不足以单独证明各级路由的独立因果贡献。
- `RESOLVED_BY_SOURCE`：论文 PDF 没有交代五个 benchmark 的完整切分。作者官方代码仓库 `yanweiyue/masrouter` 在 main commit `e005f7696fe0c0412563f6cd67f4cd3712fa2822` 中，对 MATH/MBPP/MMLU 分别使用 train/test、train/test、dev/test；GSM8K/HumanEval 使用 `split_list(dataset, 0.2)` 将打乱后的 20% 用作训练、其余用作测试。
- `UNRESOLVED_NONBLOCKING`：代码的 `fix_random_seed(1234)` 只设置 PyTorch/CUDA，而 `split_list` 使用 Python `random.shuffle`，因此 GSM8K/HumanEval 的实际划分未被该函数固定；代码也没有给出验证集、重复训练次数或方差。官方代码补足“存在 held-out test”但没有补足完全可复现性。
- `UNRESOLVED_NONBLOCKING`：PDF 与代码仍不足以严密界定 oracle reward 在超参数选择、验证和最终报告中的全部使用范围。

## Admission boundary

准入仅支持“联合路由改变了 multi-agent meta-control computation”及其成本/信息边界，不把论文主表视为各级路由的无混杂因果证明，也不把单次结果外推为稳定泛化。正式 Evidence 不写未被固定的随机 split、重复方差或 oracle 使用范围；Card 必须保留异构模型选择、预算和 oracle reward 三项替代解释。

## External source record

- Official repository：`https://github.com/yanweiyue/masrouter`
- Frozen commit identity：`e005f7696fe0c0412563f6cd67f4cd3712fa2822`
- Checked files：`Experiments/run_gsm8k.py`、`run_humaneval.py`、`run_math.py`、`run_mbpp.py`、`run_mmlu.py`、`MAR/Utils/utils.py`

## PLAN_05 Card source-audit disposition

- Audit: `plan05-audit-a/report.md`；SHA-256 `64f4c12681fc74c47cbae98e24f2501c92e3e8f1bb978edcfafc20dbd2f247e9`；task `/root/plan05_card_source_audit_a`
- Card SHA-256: pre `17af3add59018dcf8f92cf249901c8d8561dca78699b94f74d257094dae820e2` → post `e2dc9760d5ab6a6420bb8ca4ca042d274f5f99ec8a0dc28726fc5a0ec723044c`
- Disposition: `RESOLVED_BY_SOURCE`

补入 Algorithm 1 的 cascade/agent-count/role/per-agent-LLM Evidence。正式 Card 未绑定官方代码版本，因而删除 split 可复现性短语；该代码级边界仍保留在本 reconciliation 中。
