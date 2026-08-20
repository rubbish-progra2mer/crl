# v033 Result

Disposition: `NO_GO_FOR_CONFIRMATION`.

## Frozen identity

- Candidate:
  `2fd145cce11845463d765dababf8160e5a575502aa20ccee2e631368472824ce`;
- Evidence Packet:
  `b6ec4b27d4e3c052a6b3072b69202bc128b09ec60cdc14b621e8798f7763d040`;
- Plan:
  `7c3c5b0ec3099b1d26c0b01bafbcef5fef7d35c746f112ad0fb3f9cf025ef36d`;
- preexecution Artifact Manifest:
  `34b0551ecf099d924450aebe0160419534aa324e67f7c7d29064fce4d1a00b08`;
- Attempts Manifest:
  `7a998849bc31fb189426fae5836a433faed7c4fcecfa50db7e31e81715e6ee8d`,
  binding 49 files and 174,594,974 bytes.

## Development execution

- runner exit `0`;
- duration `2843.6096924999983s`;
- execution SHA
  `54e4b8dbfa322106ee22d4f5d0b09b9de947f3b407703930a68e254505c64526`;
- raw predictions SHA
  `9ab3c5baf379a9cf7eef62df382a3773ff9c7b69cec2c2484363e3a8336cd9e0`;
- dense feature rows SHA
  `950fb87afe79c46e26db1874c84e3bb416272d0846106c7ae695e59ff7459a73`;
- summary SHA
  `5f55f518ff5fced3c78a6925ab6d378236b45c501585499523be324f8b644d53`;
- frozen full model SHA
  `0f8b0ccb0fedddd640a82b80413cf74dd9ec421347211eb2c7f2e3516e923a82`;
- environment SHA
  `bd32685715ddc66e0bf3e62ab88891063ee2d54ef665e4967e15440cb7852722`.

The capture records Python 3.11.15, NumPy 2.3.5, SciPy 1.16.0,
scikit-learn 1.9.0, PyTorch 2.12.0+cu130, CUDA 13.0 and NVIDIA GeForce RTX
5060 Ti capability 12.0.

## Independent audit

- runner exit `0`;
- duration `2077.2381069000003s`;
- execution SHA
  `673fcb87ae3f42e10d53d4fdf7d004db1db779d8b449ee9539d883e8d7c7f9b7`;
- report SHA
  `6ddbeb02565085f28c8607c7462bf7f6d8126cb3107e69db02a8689e35bac4f2`;
- status `AUDIT_OK`;
- 4,256 rows, 1,361,920 dense values and 25,536 OOF scores independently
  recomputed;
- identity mismatches and maximum feature, score, summary and
  frozen-full-model errors all `0.0`.

A generated undeclared `base_v012.cpython-311.pyc`, SHA
`692a37a1446ed2c784e27518ca61822d5892c7d168e2729f3bf4bc4ac7e65410`,
may have been used by the auditor. The exact source remained Manifest-bound and
was rehashed. The cache was recorded and precisely deleted; Manifest rehash is
again zero-error and the Run has zero non-venv `.pyc`. This deviation
independently prevents positive promotion.

## Results

| Method | AUC | TPR@5%FPR |
|---|---:|---:|
| task_concat | 0.864683659857255 | 0.5312753858651503 |
| direct_action | 0.8622011090311871 | 0.50446791226645 |
| latent_additive | 0.8354665384298414 | 0.5004061738424046 |
| identity_innovation | 0.7934350171661654 | 0.3688058489033306 |
| successful_innovation | 0.7714432167157064 | 0.3233143785540211 |
| all_row_innovation | 0.7711036064795822 | 0.2859463850528026 |

Candidate-minus-strongest AUC is `-0.09324044314154867`, with task-cluster
interval `[-0.11247750427560299, -0.07437509357832868]`. Every generator,
source and target-generator×fold delta is negative. Candidate passes `0/8`
gates.

The complete Main-Codex raw analysis is
`raw_analysis_v033.md`, SHA
`7527daecb78b09f8be02318cabad63ce87835ea20d9efceaef251523bee58e56`.
The Promotion Audit is `NO_GO_FOR_CONFIRMATION`, SHA
`67bc045a10c486aa5878296408bba6960c500b1352bc3a49d6b5becea7ed9409`.

## Scientific conclusion

The successful-only cross-task conditional map does not improve serious
reward-hack detection. It treats many legitimate task-specific operations as
abnormal, trails direct surface methods in all slices, and creates 688
operating-point regressions versus 177 corrections relative to task-concat.

No ridge, SVD, vocabulary, residual, normalization, fold, control, subset,
gate or Claim retuning is allowed under v033.

## Run disposition

Bucket 0 remains absent and unread. No Review Packet, Reviewer, Decision or
Delivery exists for v033. Advance the same Run to v034 with a scientifically
distinct computation. Future frozen runner processes must inherit
`PYTHONDONTWRITEBYTECODE=1`.

Run remains `ACTIVE`. System remains `DEVELOPMENT_NOT_COMMISSIONED`.
