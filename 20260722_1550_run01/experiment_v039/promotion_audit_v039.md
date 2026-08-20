# Main-Codex Promotion Audit v039

Decision: `NO_GO_FOR_CONFIRMATION`.

The frozen primary execution and independent replay are valid, complete and
identical within tolerance. The Candidate nevertheless passes only four of
eight conjunctive Development gates.

Blocking evidence:

1. ECDS accuracy `0.5396825396825397` is below `0.65`;
2. bootstrap lower delta `-0.0033444816053511683` is not positive;
3. BFCL `0.43243243243243246` and ToolTalk `0.45348837209302323` are below
   the `0.55` source floor;
4. BFCL delta `-0.04504504504504503` violates the nonnegative-source rule.

The positive overall delta, three control-superiority results and perfect audit
cannot override these conjunctive failures. The evidence instead shows a
source-dependent likelihood proxy, strongest on GTA and unreliable on BFCL.

The main Codex rejects:

- lowering or removing gates;
- selecting only GTA after seeing results;
- tuning the differential boundary rule, evidence withholding or source
  composition;
- changing Qwen3-0.6B, prompts or controls within this lineage;
- using the incomplete v038 capture as a second favorable experiment.

ToolSandbox remains absent and unread. No Confirmation, Review Packet, Reviewer
or Delivery is authorized. v039 is frozen as a negative result and the same Run
may advance only to a scientifically different v040, the user's final allowed
version.

System status remains `DEVELOPMENT_NOT_COMMISSIONED`.
