# P070 first read — stage-wise MCP cost attribution

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol-Based LLM Agents
- Authors: Sumera Anjum et al.
- Venue: Findings of ACL 2026
- PDF: `knowledge_base/staging/plan05_sat_a1/P070_promcp.pdf`
- PDF SHA-256: `d67090fae5dd6eef7edb633ad9e3b7f4b3873b48fea8276aecb5d5877377f777`
- Parse check: 12 physical pages

## Changed computation

ProMCP decomposes an MCP run into user prompting, LLM planning, client tool call, server result, context update and final synthesis, while separately recording initialization/tool-discovery schema cost. It attributes both token footprint and latency to each stage across local/custom, cloud/custom and cloud/off-the-shelf topologies.

## Evidence and closest lineage

Across 20 servers and 169 tools from MCP-Bench and MCP-Universe, custom clients spend most tokens/latency on planning plus schema injection, whereas an off-the-shelf desktop client spends over 75–85% of latency in final synthesis. Actual lightweight tool execution is negligible in all reported configurations. Raw JSON result retention can repeatedly re-inject large web outputs.

## Measurement and fairness boundaries

- Off-the-shelf measurements use post-hoc conversation-log reconstruction and cannot expose hidden internal retries or fine jitter.
- Hardware and OS are fixed to one Windows workstation.
- The conclusion that tool runtime is negligible applies to lightweight/moderate benchmark tools, not heavy production I/O or long jobs.
- Model/tokenizer/topology differ; per-topology bottleneck comparisons are more defensible than absolute cross-model token equality.
- This source motivates cost-aware experiment controls, not a new CRL profiling platform.

## Draft knowledge objects

### Operator draft: `Stage-Wise Agent Protocol Cost Attribution`

Separate schema discovery, planning, tool transport/execution, context reinjection and final synthesis before claiming an efficiency gain, rather than reporting only total tokens or tool runtime.

### Failure draft: `Tool Runtime Optimization Can Miss the Dominant Agent Cost`

For common MCP workloads, planning, schema injection, retained tool outputs or final synthesis dominate; speeding up the called function alone may leave end-to-end cost unchanged.

## Draft Evidence locators

- pp.1–5: six stages, hidden initialization costs and instrumentation.
- pp.6–9: topology-specific token/latency results and implementation-caused result retention.
- p.9: limits of post-hoc OTS logging, one-hardware setup and lightweight tools.

All claims remain draft until independent read and reconciliation.
