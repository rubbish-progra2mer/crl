# P069 first read — description-induced tool preference

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Tool Preferences in Agentic LLMs are Unreliable
- Authors: Kazem Faghih et al.
- Venue: EMNLP 2025
- PDF: `knowledge_base/staging/plan05_sat_a1/P069_tool_preferences.pdf`
- PDF SHA-256: `bf2fb1bba7d9d028348bc9d8991d3ed01f78437c834fa4106d3abae048cbbac5`
- Parse check: 16 physical pages

## Changed computation studied

The study presents functionally identical tools that differ only in name suffix and description, counterbalances their order, and measures correct selection across BFCL cases. Assertive, maintenance, example, reputation, length and tone edits are tested singly and against each other across 17 models.

## Evidence and closest lineage

An assertive description can receive more than seven times the usage of the identical original tool for GPT-4.1 and Qwen2.5-7B; stacked edits exceed eleven times in the primary setup. Susceptibility persists across model sizes and both instruction- and reasoning-trained families. Identical-description controls also reveal strong position bias.

## Measurement and fairness boundaries

- The primary tasks are single-turn simple-function BFCL cases with duplicated functionality; effects in large heterogeneous tool ecosystems remain unmeasured.
- The tested edits are not exhaustive and model-specific preference patterns vary.
- “Correct usage rate” permits at least one correct call and excludes incorrect calls to that same tool; it does not measure downstream multi-turn task success.
- The paper suggests behavior-grounded selection channels but does not establish a validated mitigation.

## Draft knowledge object

### Failure draft: `Tool Descriptions Can Dominate Functionally Equivalent Selection`

When agents select tools only from unverified natural-language descriptions, assertive marketing language or ordering can outweigh actual functionality; model scale and reasoning training do not reliably remove the bias.

No mitigation Operator is promoted because the paper does not experimentally validate one.

## Draft Evidence locators

- pp.1–3: controlled duplicate-tool setup, metrics and ordering calibration.
- pp.3–6: individual and combined edit effects.
- pp.7–9: 17-model comparison, protocol implication and limitations.

All claims remain draft until independent read and reconciliation.
