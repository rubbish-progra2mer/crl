# P072 first read — structured uncertainty for clarification

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Structured Uncertainty guided Clarification for LLM Agents
- Authors: Manan Suri, Puneet Mathur, Nedim Lipka, Franck Dernoncourt, Ryan A. Rossi, Dinesh Manocha
- Venue: Findings of ACL 2026
- PDF: `knowledge_base/staging/plan05_sat_a2/P072_structured_clarification.pdf`
- PDF SHA-256: `def959b625902e0381ddbac6f25e042c8670f07435248e50a075fe8ef3945598`
- Parse check: 28 physical pages

## Changed computation

SAGE-Agent maps uncertain tool arguments to explicit parameter domains, maintains a belief over candidate calls, generates questions tied to unresolved tool-argument aspects, and chooses between asking and executing with cost-penalized Expected Value of Perfect Information. A response constrains the relevant parameter domains before the next decision. This changes the Agent's decision computation from free-form “ask if uncertain” prompting to a schema-grounded ask/act gate.

The paper also uses the same structured certainty signal as an action-dependent GRPO reward for choosing among tool call, clarification, decline, and direct answer. The inference operator and training signal must remain separate knowledge objects because their information and cost assumptions differ.

## Evidence and closest lineage

- On ClarifyBench, SAGE-Agent is compared on a common ReAct scaffold with ReAct+ask, ProCOT, Active Task Disambiguation, and Domain-aware ReAct across ambiguous, explicit, and infeasible requests.
- The reported GPT-4o ambiguous coverage is 59.73% versus 55.70% for the strongest listed baseline, with fewer questions; the same ordering is weaker but generally retained on Qwen2.5-14B.
- A heuristic `<UNK>` trigger is 1–3 points below the full EVPI version and asks 0.2–0.4 more questions, providing a narrow mechanism ablation.
- Uncertainty-weighted GRPO improves When2Call action classification for Qwen2.5 3B and 7B over the base and standard reward variants.

## Measurement and fairness boundaries

- ClarifyBench relies on a stateful LLM user simulator; a 600-trajectory post-hoc check reports 98.8% valid responses, but this is not real-user validation.
- Tool domains are partly produced by Qwen2.5-7B analysis, and continuous/unbounded domains are approximated with epsilon. EVPI quality therefore inherits schema/domain quality.
- The paper reports the best of three reward-training runs rather than the mean, so training gains are selection-sensitive.
- The full inference method uses more tokens than simple prompting baselines, although fewer calls than Active Task Disambiguation; question count alone is not total cost.
- The benchmark covers five simulated API families and scoped models. High-stakes or open-world tool domains are not established.
- The paper contains a nominal error-recovery path, but this project excludes environment-feedback learning and execution-recovery as research directions; that branch is not admitted as an Operator.

## Draft knowledge objects

### Operator draft: `Cost-Penalized Structured Clarification Gate`

Before committing a tool call, expose unresolved schema arguments as domains, score candidate questions by their expected reduction in call uncertainty minus repeated-aspect cost, and ask only when the best net information gain exceeds the execution threshold.

### Failure draft: `Free-Form Clarification Lacks a Stop and Value Criterion`

An Agent can ask redundant questions, choose an uninformative aspect, or execute an assumed default when clarification is driven only by token-level language confidence or a generic ask tool rather than by the unresolved tool-argument space.

## Draft Evidence locators

- pp.1–6: structured parameter domains, viability beliefs, EVPI, redundancy cost, stopping rule, and SAGE-Agent algorithm.
- pp.6–9: uncertainty-weighted reward, ClarifyBench/When2Call setup, main results, ablation, resource use, and limitations.
- pp.11–17: proofs, prompts, domain-analysis procedure, reward details, and training configuration.
- pp.17–28: simulator formalization/validation, API domains, corruption construction, and complete algorithms.

All claims remain draft until independent read and reconciliation.
