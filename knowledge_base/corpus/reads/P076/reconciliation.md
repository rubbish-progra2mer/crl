# P076 Reconciliation

- Disposition: `ACCEPTED_AS_BOUNDED_SYSTEM_FAILURE_KNOWLEDGE`
- Read 1 SHA-256: `e430bb62a3f94f4900dc6482ab98e84783ae385a55807cb679cccb6eaf7a3d0a`
- Accepted read-2: `read_2_attempts/r2-20260720-p076-a1/`
- Final invocation SHA-256: `a2fb34ae84f1baeb5a3373d22fe1a03b09b282680cc37b8d71d7e2e11cf7441d`
- Read-2 report SHA-256: `eef106c8bea8cd6a714717acf9621845cd7433a2f5c058ee7adcdabf4166454c`
- Other attempts: none; no read-3 required.

## Provenance note

The independent reader consumed the pre-completion invocation whose SHA is recorded inside its report. After completion, Codex corrected an accidentally future-dated snapshot field and filled reader/report metadata. The exact request and Frozen prompt bytes were not changed; the final invocation SHA above is the post-completion record.

## Source reconciliation

- `AGREE`: the changed computation is a system-level path from untrusted external content to front-line Agent metadata, then to orchestrator next-agent/capability selection. Per-Agent refusal does not compose into safety when a later Agent can still act on the laundered status.
- `NARROWED`: this is a form of indirect prompt injection specialized to inter-Agent metadata and control flow. The evidence shows a material distinction from the tested IPI templates, not independence from natural-language instruction following.
- `NARROWED`: severe outcomes require reachable code/data/network capabilities. The paper demonstrates controlled code-execution and one CrewAI exfiltration setting; it does not demonstrate sandbox escape, host privilege escalation, every MAS or every malicious-code class.
- `CONTROL_BOUNDARY`: templates vary with orchestrator, each tuple has ten trials, precise API/framework snapshots and budget controls are incomplete, and important matched controls for metadata format, role instruction and capability isolation are absent.
- `CONFLICT_RETAINED`: the direct-hijack sentence reports both 80% and 28/40, which is arithmetically inconsistent. No Card may select either value as settled evidence.
- `NO_DEFENSE_OPERATOR_ADMISSION`: the source evaluates no patched framework, typed provenance, least-privilege or sandbox/egress intervention. It freezes the failure mechanism only; operational attack templates and payloads remain excluded from CRL Cards.

## Frozen source role

Failure: Untrusted Agent Metadata Can Launder Privileged Control Flow. Future multi-Agent implements must treat metadata provenance, orchestration authority and reachable capability as one experimental unit, and instrument actual execution rather than infer harm from generated text alone.
