# v036 Result

Disposition: `NO_GO_FOR_CONFIRMATION`.

## Execution

- Development exit `0`, duration `210.43340929999977` seconds;
- Development execution:
  `186461108638723f5e4566c91688c3b380a4997cea33f7582bd2ec3c01b0caac`;
- raw predictions:
  `3ded63023a116f31d3ace2c5ba4b39f06e5a7b3214dd8cea7d51b7022856fe4d`;
- Summary:
  `0f8f595dc2a09f6f7845650d84c80dd8859cca1ced58a2edd26741276e108f23`;
- environment:
  `34ca95bece8684a69e1a0833a5ca341a228e6736f5c0f3a2cf8564a92ca24317`;
- frozen state:
  `56f5a3956f654636a322e20d3d4b2e112618c7f50cb94d5f64e05f969045f084`.

Independent audit exit `0`, duration `210.7018065000011` seconds:

- execution:
  `4632481733151012b1dfc9898a991659173a4652027c3f9ef79f79b85b2d6b26`;
- report:
  `e7310b6c71ea592c66f8e78ee447f2dab326d8d4683a2919a17e046eac228cca`;
- 315 rows, 2,520 prompts, 19,570 numeric values and 10,580 exact
  values reproduced;
- mismatch count `0`, maximum numeric error `0.0`.

## Development result

| Method | Accuracy |
|---|---:|
| SDEJ | 0.507937 |
| full pair | 0.519048 |
| full pointwise | 0.561905 |
| difference without evidence | 0.674603 |
| forward-only difference | 1.000000 |

Formal Candidate delta against the preregistered strongest control is
`-0.492063`, bootstrap
`[-0.553799, -0.426512]`. Source accuracies are BFCL `0.536036`, GTA
`0.521186` and ToolTalk `0.453488`; all source deltas are negative.

The forward-only value is a fixed label-order shortcut, not valid capability:
chosen is always A, and the frozen judge selects displayed A on 315/315
forward prompts and 313/315 reverse prompts. Bidirectional SDEJ order
consistency is `0.006349`.

Development gates: `1/8`. Only independent reproduction passes.

## Main-Codex decision

Raw Analysis SHA-256:
`0cdebde60ccdcfb1ed98d24bb02dfff2f520f4047189f4234c489815ed7f3e25`.
Promotion Audit SHA-256:
`1d08934e61ec67fea33d11827ecae2a69033af31fbd49e87318379efd28feae2`.

SDEJ is falsified on Development. ToolSandbox remains unacquired and unread.
No Review Packet, Reviewer, Decision or Delivery exists.

Future work may not retune v036 SDEJ or exploit fixed label order. A new
version must use a scientifically different computation.

System state remains `DEVELOPMENT_NOT_COMMISSIONED`.

