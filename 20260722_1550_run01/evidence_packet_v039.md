# v039 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

v039 is an execution-only successor. v038 output bytes are disclosed and bound,
but v038 lacks an execution record and is not accepted as Development.
ToolSandbox remains absent, unacquired and unread. This is not a Review Packet.

## v039 identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v039.md` | 839 | `75e5f509dc23c9000bd8fb09c56367ad14cadd32406e5c0ae1bb9365a76bf2bf` |
| `problem_v039.md` | 433 | `e4c22acf9668c235d2d8ed650383b3921bcc790ddb8f5e6e6f2364ee030be7ff` |
| `research_map_v039.md` | 558 | `dcba609c215b274cfd8c52f1d0551c738868cbad4e5b51642e9c7d4635c1e345` |
| `nearest_prior_v039.md` | 413 | `ae1c029286459b9f8ee0b990c2066c9eb2af421d41da7daa8898e876d94a1b0d` |
| `candidate_v039.md` | 1,121 | `84f515dbc6f2b347aad4078364ac711c03ca6eb2577b0797d9e3636a25058720` |
| `implementation_audit_v039.md` | 2,685 | `7a760a9c267556b744f9e7ef7f698f5c58c27f3048219d5bf0f414549d7d5518` |

## Executables

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 27,605 | `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17` |
| `audit.py` | 29,749 | `abfcb551889d3e0051feee788be45192b80bbfd4bc344159ddc97e62d2dcb0a6` |
| `run_local_experiment.py` | 4,350 | `2a888a00cd9845f848fa2da8f572c105a55b5dbf7ca518dac8cd9988131abb37` |
| `test_program.py` | 2,969 | `f98af7ecd9424b5c60b3372e528a96bfd6a7d6941b150c84cc10970c11d29d45` |
| `config.json` | 1,656 | `19571514487d3a24a8577427886ff8fa0f27080ffb85b6aa0f9c8614ea3157bc` |
| `acquire_confirmation.py` | 2,009 | `0ac0965c72796705b13569dcf2cf440ad03d7b1f8c1bd2a69b39dc4e1fa67df6` |
| `freeze_artifacts.py` | 5,271 | `15b801981aa2a4f01dc8bfa840d61b40b88eeecf21ba5e5d1500c6a71f8c43f4` |

Program, auditor, runner and tests are byte-identical to v038. Only the frozen
runner invocation will list four exact outputs instead of their directory.

## Scientific identity and exposed v038 bytes

The scientific ancestor Candidate remains
`85a6636225de3465641c185db4725781731fc3d1bc7cc4413c2df63507a4096e`.
Its complete computation, controls, eight gates and claim ceiling are unchanged.

v038 disclosed:

- raw predictions:
  `73986d3bdd8449952abd9410aa962b0edf39a2b8a908498108f31e58b7ffe389`;
- summary:
  `7b9189ebe772a13fff24295ff44f972e458beb69c6d4334e3c214c1c334cc647`;
- environment:
  `274b27ca22ac925ef76836f0d5cf21f92f1bb41cd73f1fea0647860c53e2176c`;
- frozen state:
  `dc1fecdce3eba91bc65acfae9bacdc9a55aa827eed4212d3980714272f500fab`.

Those bytes visibly suggest gate failure, but no scientific byte is changed in
response. v039 exists solely to obtain the predeclared complete capture and
audit needed for a durable decision.

## Data, model and prior boundary

Development remains 315 rows / 195 clusters / 1,260 sequences:

- GTA:
  `dc4cfb906dd2b20ad9452b3afdca5346a4a6a3378e15667fd47fa1c21a54a23c`;
- BFCL:
  `3c13646f14abaaeba619d5ba91d6cc64bcd4223472eea62ab91ca94f588f14a8`;
- ToolTalk:
  `e5327446f854fae9d9ed5319bd5a418168626aa6327853d145e35cf87f2027a1`.

Model manifest:
`9518287b603d6bc25ef7cd3f98764db94a633f360faa68f57ee80ceb8cf72034`;
weight:
`f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b`.
The shared environment and v037 prior PDFs are unchanged.

## Boundary

Six unit tests, six-file AST parsing and one no-data exact-output capture smoke
all exited `0`. v039 permits one Development capture and, only after exit `0`,
one independent replay within `1e-6`. Only all eight scientific gates plus a
positive main-Codex Promotion Audit permits acquiring ToolSandbox. No Reviewer
may be created before positive untouched Confirmation and a frozen Review
Packet.
