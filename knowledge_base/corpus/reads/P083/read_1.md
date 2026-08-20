# P083 first read — three-layer adversarial failures in multi-Agent systems

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems
- Authors: Ishan Kavathekar, Hemang Jain, Ameya Rathod, Ponnurangam Kumaraguru, Tanuja Ganu
- Venue: ACL 2026
- PDF: `knowledge_base/staging/plan05_sat_a3/P083_tamas.pdf`
- PDF SHA-256: `4ad6d486003dc7268c80cdc2f49224a955792843d57155915d5f77889f7f7bdd`
- Parse check: 31 physical pages

## Canonical failure contribution

TAMAS separates attacks across prompt, environment/tool-output, and compromised-agent interaction layers, then evaluates them under centralized, fixed sequential, and dynamic handoff configurations. Its scientific value for CRL is negative knowledge: multi-agent coordination creates propagation and weak-link failures that single-agent prompt-injection tests do not cover.

## Evidence and closest lineage

- The benchmark contains 300 adversarial instances, 100 benign tasks, five domains, six attack types, 211 simulated tools, ten backbone models, and AutoGen/CrewAI configurations.
- Prompt-level attacks include direct injection and impersonation; environment-level attack is indirect prompt injection; agent-level attacks include Byzantine, colluding, and contradicting agents.
- Findings report high vulnerability across layers and architectures. Central orchestrators can improve aggregate utility/robustness while also creating a single point of failure.
- Human verification covers 120 logs with two annotators and third-party adjudication; agreement is κ=0.77, while GPT-4o judge macro-F1 averages 89.13% but is lower for Byzantine and contradicting cases.

## Measurement and fairness boundaries

- Tools and side effects are simulated for determinism. This supports controlled coordination analysis but does not reproduce all real-world permissions or consequences.
- The study covers two frameworks, three configurations, four agents per scenario, five application domains, and ten examples per attack/scenario combination; generality beyond them remains open.
- Several results use an LLM judge plus tool-invocation checks. Judge quality varies substantially by attack type.
- Lightweight defenses are not robust Operators: paraphrasing can delete benign subtasks, delimiters provide modest/inconsistent gains, and monitor agents produce frequent false positives and unstable decisions.
- A persuasion-only compromised-agent attack failed entirely in this setting; the paper does not establish that all adversarial interaction styles succeed.

## Draft knowledge objects

### Failure draft: `Multi-Agent Adversarial Coordination Spans Three Trust Layers`

Safety can fail at the user prompt, untrusted tool/environment output, or internal agent communication. A system can inherit model-level compliance failures while also adding framework-level propagation, privileged orchestration, collusion, contradiction, and weakest-link risks.

### Operator disposition

No positive defense Operator is extracted. The tested lightweight defenses are inconsistent and sometimes reduce benign task fidelity; they remain negative evidence and evaluation warnings.

## Draft Evidence locators

- pp.1–6: threat model, attack taxonomy, benchmark design, configurations and metrics.
- pp.7–9: vulnerability results, framework/model distinctions and limitations.
- pp.13–16: simulated-tool boundary, dataset construction, attack table and judge validation.
- pp.17–19 and pp.23–27: defense failures, confidence analyses and concrete propagation traces.

All claims remain draft until independent read and reconciliation.
