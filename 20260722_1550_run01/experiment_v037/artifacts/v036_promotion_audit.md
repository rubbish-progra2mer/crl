# v036 Promotion Audit

Decision: `NO_GO_FOR_CONFIRMATION`.

The current main Codex personally read the frozen Plan, Summary, raw
predictions, source actions, both captures and the independent audit report.
No subagent or automated vote made this decision.

SDEJ accuracy is `0.507937`, below the `0.70` gate and below both full-pair and
full-pointwise controls. It loses to evidence-free differences by `0.166667`
and to the preregistered forward-only control by `0.492063`. The bootstrap
interval against the strongest control is entirely negative. Every source
accuracy and source-delta condition fails.

The forward-only control's `1.0` accuracy is a fixed-label-order artifact:
chosen is always displayed as A, and the judge selects A on all forward prompts
and 313 of 315 reverse prompts. This cannot be promoted as a result. The
bidirectional Candidate exposes rather than solves the bias; its order
consistency is `0.006349` and its final accuracy is near chance.

The independent audit confirms that these findings are not capture or
aggregation errors: 2,520 prompts and 30,150 checked values reproduce with
maximum error `0.0`.

Only the reproduction gate passes (`1/8`). ToolSandbox must remain unacquired
and unread. No Review Packet or Reviewer is permitted.

Future versions may not retune SDEJ wording, field projection, evidence
selection, A/B tokens, bidirectional aggregation, Qwen3-0.6B, controls or
gates. A new version must use a scientifically different computation, not
exploit fixed label order and not reinterpret `delta_forward` as a valid
capability.

