# Main Codex Implementation Audit v025

Disposition: `APPROVED_FOR_EXECUTION_ONLY_FREEZE`.

v025 is byte-identical to the fully read v024 VIAF implementation except five version-identity string changes: the program import-module label and emitted `experiment_id`, the auditor import-module label and expected `experiment_id`, and `config.json`'s `experiment_id` all change from `v024` to `v025`. `git diff --no-index` showed no other code/config/test difference; `test_viaf.py` is byte-identical. The Candidate and Evidence Packet are also byte-identical and currently bound.

Current bytes:

- program: SHA-256 `e71a820adfe798b0732a07dbfe1e31286cad7eab43c229309a9522e34ea44ab6`, 23,422 bytes;
- auditor: `8eade0d127843da37545327622e7be7627592400ca696c05c63aa1a1dcd66c72`, 21,053 bytes;
- config: `e34c812e78d1476e6a283d89452f3f61b3cd7bb74859d11a29fa2202bacf9983`, 1,200 bytes;
- tests: `1f334f43fb9222ef625f10732b9f17b072c5439cbfef76709ea28bf5b381a3fb`, 1,937 bytes;
- Candidate: `d7af6362080666bdecc927c8f2c65ea0894d2b7e1756d6434b61107ae8156c60`;
- Evidence Packet: `87d886ba29d9096e35537802de1388f48fb2e9ef5f3a87b957044dedab99128f`.

At the correct implementation cwd, shared Python 3.11.15 produced `py_compile` exit 0 and `pytest -q test_viaf.py` exit 0 (`4 passed in 2.15s`). Exact-path cache removal ended with `CACHE_LEFT=0`.

The v024 failure was outside the scientific implementation: the frozen runner requires the capture parent to pre-exist. v025 therefore must create only empty `experiment_v025/captures` and `experiment_v025/work` parents after Plan publication, then verify `captures/dev_acquire_001`, `dev_acquire_output_001`, and `work/dev_acquire_001` remain absent before the unique runner call. No runner rewrite, retry loop, environment router, defensive path handling or scientific change is approved.

Bucket 1 and bucket 0 remain unopened. This audit authorizes only artifact freezing and a publish-once Plan; it does not itself authorize Confirmation, Review, Delivery or Ready.
