# v038 Evidence Packet

Packet status: `PREFREEZE_CURRENT`.

v038 is an execution-only successor. v037 produced no Development subprocess or
metric. ToolSandbox remains absent, unacquired and unread. This is not a Review
Packet or Delivery evidence.

## v038 identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `selection_context_v038.md` | 832 | `3d4393407d969444a0162b267147cb8c529141c6635de14e9638659f19d75c45` |
| `problem_v038.md` | 482 | `40a326adea32827319b910da21f40e53b89595567fa44686e164ee7b17a82fa7` |
| `research_map_v038.md` | 677 | `05ed442ac4e5bc32e0e291f25f078c47f909376075c1192a28b8dcf07b279baa` |
| `nearest_prior_v038.md` | 582 | `225e2cfe7ac49b798f1f1da936645f280fe60772296499ee14953560778fb01e` |
| `candidate_v038.md` | 1,514 | `19b7ac97c4b1e3845410ff67101aa254436d526bd8d8c77817d0e2d176f6d2ef` |
| `implementation_audit_v038.md` | 2,698 | `b3e8178e6c736f63f2a3729a37bdef3465f6a2ff48261c3ba72409f172f0d195` |

## Executable identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `program.py` | 27,605 | `c29395c7072b177b64b833aed0c8e253d6d71ff70aa4cc564cb656a94081ef17` |
| `audit.py` | 29,749 | `abfcb551889d3e0051feee788be45192b80bbfd4bc344159ddc97e62d2dcb0a6` |
| `config.json` | 1,664 | `86186d37f1fcfce3b9f1656555a416f2abe2ec4796bf88d2bbc9381f97092726` |
| `test_program.py` | 2,969 | `f98af7ecd9424b5c60b3372e528a96bfd6a7d6941b150c84cc10970c11d29d45` |
| `run_local_experiment.py` | 4,350 | `2a888a00cd9845f848fa2da8f572c105a55b5dbf7ca518dac8cd9988131abb37` |
| `acquire_confirmation.py` | 2,009 | `1848dbcc808ce2f2def9b6a945d9b3a264bbf626392840acf8e037791a2cf4ae` |
| `freeze_artifacts.py` | 4,933 | `8248a29682c37b107cd93cdc829f45c9d13b850e12e413f27ed4f9e9db2ebe97` |

`program.py`, `audit.py` and `test_program.py` are byte-identical to v037. The
runner has exactly one execution hunk: `capture_dir.mkdir(parents=True)`.

## Scientific bytes inherited from v037

- v037 scientific Candidate:
  `85a6636225de3465641c185db4725781731fc3d1bc7cc4413c2df63507a4096e`;
- v037 Evidence Packet:
  `c12fba01f2b7d739d92d6df6bd208deee9570e4af2d7c03bc453e268c3101b19`;
- v037 Artifact Manifest:
  `d434f3bcc36593ab9b94a1c4d8470dd56c6e9ef2c76ed0ec188e3c88c566a18c`;
- v037 failure record:
  `985cc8f328dd52aa4da182aa3ac8b930cdd8dc988698fdf435ddcde098c8d98d`;
- v037 Result:
  `bc210c972fed6b6cca5f071718a124d867a577d48d8a7d59f46d7acd0ce7a5b9`.

The v037 failure happened before scientific subprocess launch. It supplies no
result about ECDS and no optional metric feedback.

## Frozen carrier and model

Development remains exactly:

- GTA 118 rows / 92 clusters,
  `dc4cfb906dd2b20ad9452b3afdca5346a4a6a3378e15667fd47fa1c21a54a23c`;
- BFCL 111 rows / 52 clusters,
  `3c13646f14abaaeba619d5ba91d6cc64bcd4223472eea62ab91ca94f588f14a8`;
- ToolTalk 86 rows / 51 clusters,
  `e5327446f854fae9d9ed5319bd5a418168626aa6327853d145e35cf87f2027a1`.

Total: 315 rows, 195 source-qualified clusters and 1,260 sequences.

The Qwen3-0.6B model revision is
`c1899de289a04d12100db370d81485cdf75e47ca`, model manifest
`9518287b603d6bc25ef7cd3f98764db94a633f360faa68f57ee80ceb8cf72034`
and weight
`f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b`.
The shared environment was not changed.

Prior PDFs and the v037 collision ceiling remain unchanged. The inherited prior
source manifest SHA-256 is
`d1c01b550e61dd34e7be8eb25115325fa8ea0bc89fd44ce382b687017f7ea1a1`.

## Gates and execution boundary

All eight v037 Development gates remain conjunctive. Only all gates plus a
positive main-Codex Promotion Audit permits acquiring the fixed 130-row
ToolSandbox. The claim ceiling remains limited to exact-split next-action
ranking for the frozen small model.

Six unit tests, six-file AST parsing and the missing-parent runner smoke all
exited `0`. v038 permits exactly one Development capture and then, only after
exit `0`, one independent replay. No Reviewer may be created before a positive
Development, positive untouched Confirmation and complete frozen Review Packet.
