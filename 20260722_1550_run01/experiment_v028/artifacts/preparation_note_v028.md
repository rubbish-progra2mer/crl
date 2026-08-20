# v028 Preparation Note

At `2026-07-25T19:59:37.7513471+08:00`, the corrected post-Plan preparation command created `captures/` and `model_cross/` and copied all six frozen model files. Its trailing verifier exited `1` because the command-local expected value for `vocab.txt` omitted one hexadecimal `B`.

No copy failed and no scientific program or capture runner started. A subsequent read-only verification exited `0` and proved:

- exactly six regular model files;
- total model bytes `91,815,758`;
- every file SHA-256 exactly equals the frozen Plan and artifact SHA;
- `captures/` has zero children;
- `dev_output_001` and `dev_audit_output_001` are absent.

The actual `vocab.txt` SHA-256 is `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3`. No file was recopied or changed during the read-only verification.

This is a transparent preparation-verifier correction, not a Development retry. The v028 Plan’s failure rule applies to nonzero scientific/capture execution; neither has occurred.

