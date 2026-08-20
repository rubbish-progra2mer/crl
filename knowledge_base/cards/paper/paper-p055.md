<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p055","card_kind":"paper","paper_id":"P055","evidence_ids":["ev-p055-constraint-formalism-taxonomy","ev-p055-representative-subset-boundary","ev-p055-three-revision-budget","ev-p055-constraint-performance-drop","ev-p055-plan-correctness-false-positive-boundary"],"source_refs":[{"path":"papers/P055_planner_formalizer_constraints.pdf","sha256":"0d21a03ded6ae892d0818ec8e0f453b3ca0fc1c4cb3e30ae2c3b182c40868207"}]} -->
# Language Model as Planner and Formalizer under Constraints

## Role in the knowledge base
[CODEX_SYNTHESIS] P054 formalizer 谱系的 2026 constraint-shift 负向锚点：检查一个短约束能否被 direct Planner 与多种 formalizer 忠实吸收。

## Problem and setting
[AUTHOR_FACT] CoPE 按 initial、goal、action、state 四类组织约束；不同类别在 PDDL、PDDL3、LTL 与 SMT 中需要不同修改，没有一种 formalism 平凡覆盖全部类别。[[evidence:ev-p055-constraint-formalism-taxonomy]]

## Changed computation
[CODEX_SYNTHESIS] 同一个 constraint-conditioned planning problem 被分别映射为直接 plan 或不同 formal language，再由各自 solver/toolchain 产生可验证 plan；这里主要是压力测试与测量比较，不是单一新 Operator。

## Evidence-backed findings
[AUTHOR_FACT] 论文报告一行约束在该设置中显著降低 planning 与 formalization 表现，且 direct Planner 在总体上仍高于 formalizer。[[evidence:ev-p055-constraint-performance-drop]]

## Limitations and failure signals
[AUTHOR_FACT] 完整数据可形成 10,000 个 constraint/problem 配对，但主评测每域只运行 100 个手工代表配对。[[evidence:ev-p055-representative-subset-boundary]] [AUTHOR_FACT] formalizer 最多获得三次基于工具错误的代码修订，因此不同路径不是 matched single-call budget。[[evidence:ev-p055-three-revision-budget]] [AUTHOR_FACT] plan correctness 可能接受不忠实的 formalization，而作者只对合并的 20 个样本检查了这一假阳性。[[evidence:ev-p055-plan-correctness-false-positive-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] P054 complete PDDL formalizer → P055 constraint shift；P053 随后改变 grounded representation scaling。未来机制必须区分 constraint semantics、formalism/toolchain 与额外 revision budget。

## Evidence ledger
[CODEX_SYNTHESIS] 本卡只记录“该 benchmark 上广泛且显著的下降”，不把摘要中的 `consistently halves` 当成有统计保证的普遍定律。[[evidence:ev-p055-constraint-performance-drop]] [[evidence:ev-p055-representative-subset-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] constrained planning; CoPE; initial goal action state constraint; PDDL3; SMT; LTL; constraint shift; formalizer robustness; faithfulness false positive
