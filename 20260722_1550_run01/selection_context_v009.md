# Neutral Selection Context

## Development Source

Development is the fixed 200-row P084 expanded-toolkit artifact and its matching BFCL v3 question and answer files:

- `BFCL_v3_multiple_tool_enrichment.json`: 582,498 bytes; SHA-256 `1be15f014a2d04af06fec2797e4e53f7a335ce46e6bdc2ec0ef3cabd6074a7b`.
- `BFCL_v3_multiple.json`: 316,583 bytes; SHA-256 `aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a`.
- `BFCL_v3_multiple_possible_answer.json`: 32,254 bytes; SHA-256 `244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047`.

The three files contain 200 aligned IDs. The expanded menu provides the evaluated functions; the original BFCL file is used only to verify the unchanged question; the answer file is used only for evaluation and Development parameter selection. `perturbed_question` and original-menu membership are not inputs to any scoring method.

## Untouched Confirmation

Confirmation was fixed before Development as `BFCL_v4_live_multiple.json` and `possible_answer/BFCL_v4_live_multiple.json` from `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`. Neither file has been downloaded or read. They may be acquired only after the Main Codex verifies every Development output and writes the Promotion Audit.

Exact normalized query SHA-256 values must be disjoint across phases. A nonempty overlap ends v009 without replacement data. The Development-selected tuple is applied unchanged to Confirmation.

## Outcome And Comparators

For each row, top-1 is correct when the top-ranked function belongs to the row's ground-truth function set. On a multi-gold row this is top-1 membership, not complete call-set recall. MRR uses the rank of the highest-ranked ground-truth function.

All methods receive the same query, menu, and full-schema bytes. The primary cross-encoder, MiniLM cosine, and BM25 receive no TPPA score. The relaxed comparator receives the exact TPPA spans, edge features, Development-selected tuple, and fusion weight, changing only capacity reuse. No inference method receives gold functions, original-menu membership, perturbed requests, or Confirmation labels.

## Version Boundary

v008 was the first frozen TPPA implementation. Its Plan SHA-256 is `9c9c2046c345e433857fc74f03f9d7e47a25f73ebee7afec942a493c736f8815`; its single Development capture exited 1 before metrics because the parser did not expand one observed embedded-required BFCL schema; its Result SHA-256 is `20f1320719c83929a63b58dad866dcd9da9a616703d88ea5e78f200e383a4cc0`. Development bytes are therefore touched, but Confirmation remains unacquired.

v009 is an execution-only successor with strict expansion of that observed layout. It retains v008's scientific design, data, models, grid, metrics, gates, and Confirmation boundary. At this point no v009 Experiment Plan, frozen Experiment Artifact, Development capture, Confirmation byte, Review Packet, Reviewer report, Decision, or Delivery exists.
