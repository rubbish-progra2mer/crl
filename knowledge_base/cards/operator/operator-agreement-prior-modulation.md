<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-agreement-prior-modulation","card_kind":"operator","paper_id":"P015","evidence_ids":["ev-p015-agreement-prior"],"source_refs":[{"path":"papers/P015_should_we_be_going_mad.pdf","sha256":"8d0330933f495a3804842e8c8b0f778d8529fefeaf8d2a2dbf89d94f97bd0e70"}]} -->
# Agreement-Prior Modulation

## Intervention target
[AUTHOR_FACT] 在多代理 debate 开始时，用 prompt 指定角色应同意其他代理的比例。[[evidence:ev-p015-agreement-prior]]

## Before and after computation
[CODEX_SYNTHESIS] Baseline 是固定 contrarian persona；changed computation 是给 devil role 加入可调 agreement intensity。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为问题、角色 system prompt 与目标 agreement，输出为多轮立场及 judge 答案；干预发生在首次交互前。相对原始 Multi-Persona，该操作可保持 agents、rounds 与调用数不变，但增加少量 system-prompt tokens；跨协议比较仍需另行对齐总 calls/tokens。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 调节社会性先验可减少无条件反驳对正确初答的破坏，同时保留必要异议。

## Predicted observable signature
[CODEX_HYPOTHESIS] 机制有效时，实际首轮 agreement 与最终准确率应随强度呈任务相关而非普遍单调关系。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Prompt 百分比不是校准概率；方向依赖 task、backbone 与 protocol，不能当通用控制旋钮。

## Source lineage
[CODEX_SYNTHESIS] MAD study 是直接来源；self-consistency 与 independent ensemble 是结构不同的强对照。

## Evidence ledger
[AUTHOR_FACT] `ev-p015-agreement-prior` 定位到 PDF p.6 的精确 prompt。[[evidence:ev-p015-agreement-prior]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] multi-agent debate；agreement intensity；contrarian agent；devil prompt；多代理一致性调节。
