# P087 Reconciliation

- Disposition: `DIRECT_PRIOR_ADMISSION_WITH_CLAIM_NARROWING`
- Read 1 SHA-256: `2beed96f073015bf6503c3c578aed56706b74c328b780fbbd8c46cae293e3ff0`
- Accepted read-2: `read_2_attempts/r2-20260720-p087-a1/`
- Read-2 invocation SHA-256: `1a1843dcce8b3cad351cd87ce813db8e8e5142b080cc6d0a9b6cef0d64af4802`
- Read-2 report SHA-256: `6529b04b911b1649922d3b65a6f177f9e46a4b4f818e103ae1de70b35e1755b3`
- Other attempts: none
- Read 3: not triggered. The bytes contain several internal reporting conflicts; the formal role relies only on the undisputed document-expansion computation, and disputed magnitudes are excluded rather than resolved by another reread.

## Source reconciliation

- `VERSION_BOUNDARY`: the read bytes are arXiv:2510.22670 v1 and use the name TOOL-DE. ICLR 2026 Poster status and the later TOOL-REX name are provenance metadata, not claims imported from unread final-version pages.
- `AGREE`: the operator is query-independent structured tool-document expansion. It generates function, when-to-use, limitation and tag fields, preserves the original document, and uses the merged text for retrieval/reranking training or evaluation.
- `DIRECT_PRIOR`: this is a direct collision for description-aware document expansion. Changing prompts, field labels or backbone alone does not create a distinct computation.
- `PARTIAL_SCHEMA_PRIOR`: the source analyzes schema-like fields, but the admitted computation remains text enrichment. It does not implement typed parameter/output alignment, field-level constraint matching, graph computation or runtime argument validation.
- `GROUNDING_BOUNDARY`: the generation/judging chain and a small human check reduce risk but do not guarantee fidelity. The PDF examples contain unsupported or altered inferences, so CRL does not treat generated profiles as authoritative schema facts.
- `REPORTING_CONFLICTS_EXCLUDED`: the PDF says 35 source datasets while the appendix enumerates 28; the 41.6%→23.5% documentation audit lacks enough model/count detail to reproduce; several field names, ablation statements and table deltas conflict. None becomes a precise formal claim.
- `NON_UNIVERSAL_GAIN`: expansion helps several retrievers/rerankers but harms or lowers recall/completeness for some evaluated models. More text is not itself a generally successful mechanism.
- `COMPARISON_BOUNDARY`: reported chains jointly change training and evaluation document views and omit the full cross-grid needed to isolate each effect. No cross-registry, live-tool or end-to-end execution success is established.

## Frozen source role

Direct prior and closest document-enrichment comparator for grounded structured tool-description expansion. The source supports a bounded representation operator, not complete schema recovery, universal retrieval improvement or correct tool execution.
