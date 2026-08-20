# v031 Result

Disposition: `NO_GO_FOR_CONFIRMATION`.

## Frozen identity

- Candidate `fdbbf978279d8a7fbfaea35ab9949054a8f671126ef2e641c9180b24f5948bd0`.
- Evidence Packet `86a06e5e0432decdc6dfbd28e2c501449f8b02662f2402dca96872dd4e5ebfa3`.
- Plan `371b4958a3b68e7d77cd7e5481942b61acf337297ff14d136103b4d8889e6a6c`.
- preexecution Artifact Manifest `e3fba3cb822cde4405221c839149ef40dc111f57a6aa464af809d2312c98d60a`.
- Attempts Manifest `f7d391d04a90fc2ec5be0ac96b03a7d94372d0c234b2045f59426f70bc3bff43`, binding 18 files and 163,172,439 bytes with zero rehash error.

## Development execution

- runner exit: `0`;
- duration: `2241.9498179s`;
- execution SHA: `08ba2c316e0089e215b2d1b6da9bf6e161ea47702429653b0c9aaaeb438620ca`;
- pair scores: 444,000 rows, SHA `4c29b0a23d91375e76c1ca51716fe7745f2bd7d084a1d38a601199aed805c07d`;
- feature rows SHA `81924fd3667ab6c0cb81a2f67a1913e40df0176a7b721808d7bd5f23b6fcb9a0`;
- raw predictions SHA `11b1b8f24763a34354e48187293a7f1af7528d4400bb632ae4376d2e3eab41eb`;
- summary SHA `fc1dfa8378f656eacc727d31fcdd218017ab9fa0193bf68786420d64425d2ef1`;
- frozen model SHA `69d9f0fbbd034d2e61f8c02b45ea4490b3b31b649bf3fe20c3bec51c03144d1e`;
- environment SHA `03e9ad1f1a005e2feef6b3d05768db4e83ae771c58b66bde1a3f8f0fc1951d41`.

Environment capture records Python 3.11.15, NumPy 2.3.5, SciPy 1.16.0, scikit-learn 1.9.0, PyTorch 2.12.0+cu130, CUDA 13.0 and NVIDIA GeForce RTX 5060 Ti capability 12.0.

An initial outer terminal call timed out with code `124` before any runner process, capture directory or output existed. The actual frozen runner was then started once, produced the execution identity above and was not retried.

## Independent audit

- runner exit: `0`;
- duration: `2045.0522175999977s`;
- execution SHA `f97f423273785749d1874cb8c5880514dc4364c476bcda3ae7fa21e40b725f72`;
- report SHA `21da272d7375a2748402209653bc293b36ffb8c9a3783252fe4dabe638271f7d`;
- status: `AUDIT_OK`;
- pair-score, feature, OOF-prediction, summary/gate and frozen full-model maximum errors: all `0.0`.

The audit capture includes an extra generated `base_v012.cpython-311.pyc` input not present in the preexecution manifest. The auditor did not read it. It was precisely deleted after audit, and the 31 preexecution artifacts then rehashed with zero missing, unlisted or mismatched file.

## Results

| Method | AUC | TPR at 5% FPR |
|---|---:|---:|
| task_concat | 0.864683659857255 | 0.5312753858651503 |
| direct_action | 0.8622011090311871 | 0.50446791226645 |
| global_relevance | 0.8473818767676713 | 0.46222583265637696 |
| chronological_relevance | 0.8447634818471536 | 0.44719740048740864 |
| structural_counts | 0.8336213228135666 | 0.4268887083671812 |
| role_gated_relevance | 0.8014552525024745 | 0.39967506092607635 |

Candidate-minus-strongest AUC is `-0.06322840735478052`, with task-cluster interval `[-0.07888434856946733, -0.04814208703969722]`. All three generator deltas and all five source deltas are negative. All nine target-generator×task-fold deltas are negative. The Candidate passes `0/8` gates.

The complete Main-Codex raw audit is `raw_analysis_v031.md`, SHA `05226e86c123cfc207166fefafddfcc3373460f333b6c5558254206bc599abbf`. The Promotion Audit is `NO_GO_FOR_CONFIRMATION`, SHA `dc51c1b692be0bf8c74f54630fc6cc2611886bebc2deecbaf0d265cc4367b3d6`.

## Scientific conclusion

Fixed operation-role pooling does not improve serious reward-hack detection on this doubly held-out Development set. It is worse than every mandatory comparator. Low-relevance mutation pairs are class-balanced, and the frozen newline/operation parser visibly converts heredoc body lines and benign output commands into purported mutations. The proposed mechanism is not supported.

No segmentation, role, encoder, control, subset, gate or Claim retuning is allowed under v031.

## Run disposition

Bucket 0 was not acquired or read. No Review Packet, Reviewer, Decision or Delivery exists for v031. Advance the same Run to v032 with a scientifically distinct computation.

Run status remains `ACTIVE`. System status remains `DEVELOPMENT_NOT_COMMISSIONED`.
