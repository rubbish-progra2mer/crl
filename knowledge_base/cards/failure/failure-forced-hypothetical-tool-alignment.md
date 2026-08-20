<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-forced-hypothetical-tool-alignment","card_kind":"failure","paper_id":"P089","evidence_ids":["ev-p089-training-gold-count-hypothetical-tools","ev-p089-hungarian-alignment","ev-p089-forced-alignment-proxy","ev-p089-retrieval-only-metrics"],"source_refs":[{"path":"papers/P089_tooldreamer.pdf","sha256":"d13b84ab7c2a66069f8d160ab78dfb3e7efd5dabab06c219995c5f92b2093918"}]} -->
# Forced One-to-One Alignment Can Launder Noisy Hypothetical Tools

## Observed failure
[AUTHOR_FACT] ToolDreamer 的 square similarity matrix 总会产生 match，HT–GT pairing 被明确称为可能不完美的 proxy。[[evidence:ev-p089-forced-alignment-proxy]]

## Conditions and scope
[AUTHOR_FACT] 训练期 generator 被告知 exact gold-tool count，并生成同数量 hypothetical tools。[[evidence:ev-p089-training-gold-count-hypothetical-tools]]
[AUTHOR_FACT] pairing 使用 embedding similarity 与 Hungarian matching。[[evidence:ev-p089-hungarian-alignment]]

## Failed intervention
[CODEX_SYNTHESIS] 把每个生成的 latent/hypothetical tool 强制映射到一个 gold tool，再将该 mapping 当成可靠 supervision；缺少 reject/null/集合级不确定性时，错误 HT 也会获得正标签。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 强 embedding 与 matching 可降低噪声，但不能验证对应关系。训练 gold count 也让方阵构造比实际 inference 更容易；实验只评价 retrieval ranking，无法证明噪声 pairing 不伤害执行。[[evidence:ev-p089-retrieval-only-metrics]]

## Warning for future candidates
[CODEX_SYNTHESIS] 任何 latent-tool alignment Candidate 必须报告 alignment validity 或允许 reject/null；至少比较 forced one-to-one、greedy/random/no-alignment 与不使用 gold count 的集合级方案，不能只凭 retrieval gain 宣称内部工具分解正确。

## Possible repair boundary
[CODEX_HYPOTHESIS] 可拒配、many-to-many/set-level objective 或 execution-grounded alignment 可能改变失败计算，但它们在形成 Candidate 前仍需 nearest-prior 和本机可识别 observable。

## Evidence ledger
[CODEX_SYNTHESIS] gold-count generation、Hungarian computation、forced-proxy warning 与 retrieval-only endpoint 均绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] forced Hungarian alignment; hypothetical tool noise; gold tool count leakage; square assignment; no reject option; noisy positive pairs; latent tool decomposition; alignment validity
