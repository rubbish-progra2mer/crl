# P074 first read — contract-gated tool state commits

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: ToolGate: Contract-Grounded and Verified Tool Execution for LLMs
- Authors: Yanming Liu, Xinyue Peng, Jiannan Cao, Xinyi Wang, Songhang Deng, Jintao Chen, Jianwei Yin, Xuhong Zhang
- Venue: Findings of ACL 2026
- PDF: `knowledge_base/staging/plan05_sat_a2/P074_toolgate.pdf`
- PDF SHA-256: `7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d`
- Parse check: 32 physical pages

## Changed computation

ToolGate separates candidate generation from state admission. It keeps a typed symbolic state, derives a precondition `P` and postcondition `Q` for each tool from interface material, filters calls whose required state is absent, executes a selected tool, and commits the result to trusted state only if the returned structure/types satisfy `Q`. A rejected result leaves the state unchanged and another candidate may be tried. The important Operator is therefore the two-sided gate around a state transition, not the accompanying embedding retrieval/reranking stack.

## Evidence and closest lineage

- The paper evaluates ToolBench G1/G2/G3 and three MCP-Universe tasks across Qwen3-235B, DeepSeek V3.2, GPT-5.2, and Gemini 3 Pro.
- In the reported GPT-5.2 MCP average, full ToolGate reaches 57.0% versus 52.5% without `P`, 46.2% without `Q`, and 37.6% without the Hoare module; the stronger drop without `Q` supports post-execution admission as a distinct mechanism.
- Reported rejection tracing attributes 17.6% of invocations to precondition filtering and 11.8% to postcondition rejection.
- ToolGate uses fewer tool-calling steps than search-heavy baselines in the paper's ToolBench comparison, while running slightly slower than ReAct but faster than DFSDT/ToolChain*/Tool-Planner.

## Measurement and fairness boundaries

- The guarantee is conditional on sound contracts and state updates. It is not a guarantee that a schema expresses task intent or safety.
- Approximately 25% of ToolBench tools lack structured response schemas and receive `Q=True`; ToolBench response shapes are LLM-assisted expected schemas rather than authoritative formal specifications.
- A postcondition can prevent a bad result from entering the Agent's symbolic state but cannot undo an irreversible external side effect that already occurred during the tool call.
- The paper describes semantic constraints and state consistency, but the reproducible derivation examples are primarily required fields, types, and explicit length constraints. How richer semantic predicates and update functions are produced is underspecified.
- ToolBench Win Rate uses LLM judging, variance/significance and matched-call details are limited, and only three of six MCP-Universe domains are reported.
- Formal weakest-precondition notation is stronger than the operational algorithm, which mechanically checks `P` before execution and `Q` after it.

## Draft knowledge objects

### Operator draft: `Contract-Gated Tool State Commit`

Require explicit state predicates before invoking a tool and admit its output into trusted Agent state only after a separately specified return contract passes. Failed verification changes neither trusted state nor downstream evidence.

### Failure draft: `Incomplete Contracts Create False Verified State`

If missing schemas default to `True`, or generated response shapes omit task-semantic and side-effect conditions, the “verified” label can mean only structurally parseable—not correct, safe, or causally harmless.

## Draft Evidence locators

- pp.1–5: typed state, `P/Q` derivation, pre-call filter, post-call admission, and trajectory formulation.
- pp.6–10: datasets, main results, ablations, rejection distribution, efficiency, contract and environment limits.
- pp.13–16: incomplete-contract robustness, benchmark scope, retrieval/reranking setup, and rejection categories.
- pp.18–32: operational algorithm, concrete contract examples, formal conditional guarantees, and policy factorization.

All claims remain draft until independent read and reconciliation.
