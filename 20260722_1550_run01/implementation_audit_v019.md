# Main-Codex Implementation Audit v019

Audit time: `2026-07-24T11:58:22+08:00`

Audit status: `IMPLEMENTATION_READY_FOR_ONE_SHOT_DEVELOPMENT`

This is a pre-execution code and protocol audit by the main Codex. It is not a Development result, Promotion Audit, Confirmation result, Review, Decision, or Delivery.

## Frozen scientific bindings checked

- Candidate: `candidate_v019.md`, SHA-256 `30C51E3CBADB8AFFC925D42FF91B12240DC3E018E83DF0069D5DCDBDB21026DE`.
- Rebuilt Evidence Packet: `evidence_packet_v019.md`, SHA-256 `D9239666B23A0AADC725F67C95DACCCAD1EF280A4537D3F48DEBA8D6ED2481F1`.
- Packet rebuild reported `candidate_is_current=True`, three Evidence entries, and current PDF/passage bytes for every entry.
- BFCL v3 simple Development input: 280,474 bytes, SHA-256 `FBC37B2AD252BF9AF985582E0E07B456173FE627D957491472EA9CEF5FB83158`.
- `rank-bm25==0.2.2` wheel: 8,584 bytes, SHA-256 `7BD4A95571ADADFC271746FA146A4BCFD89C0CF731E49C3D1AD863290ADBE8AE`.
- Target repository commit: `9759eb9f0e7ed90ff289d34300acc15453f7851a`.
- Target notebook: 171,036 bytes, SHA-256 `61DA53127597D7A90A440A87FF2EFCEA77665454852D50552DF9BB2972A6FF81`.
- Target paper: 400,683 bytes, SHA-256 `4DB89BFAC79BC90DD5B532D04AC1012ED1691657A45379BBBB2312682847164C`.

## Official comparator protocol readback

The main Codex directly read the fixed target notebook's BFCL/BM25 cell before freezing this implementation. The source fixes:

- seeds `[42, 123, 456]`, `CAND_N=370`, all 400 queries, and `TRAIN_EPS=8000`;
- sorted registry names, BM25 over tool name/description/parameter-name text, and a gold-included two-stage candidate ranking;
- `train_test_split(..., test_size=0.30, random_state=42)`;
- the seven score-only state features and `7 -> 64 -> 64 -> 2` network;
- replay 50,000, batch 128, Adam `0.001`, epsilon `1.0 -> 0.05`, target copy every 500 environment steps, continuation cost `0.01`, and discount `0.95`;
- target terminal rewards `hit * -log2(K/N)` and `hit * 2/(K+1)`.

The final code uses those bytes and values for both target comparators. All four learned policies receive the same 8,000-episode, three-seed budget. Training is deliberately CPU-only; the shared environment's CUDA readiness is captured separately and in the program summary. This is an algorithmic same-platform comparator rerun, not a claim that stochastic model weights or published table values must reproduce bit-for-bit.

The earlier v013 learned policies are excluded because their state contained a gold-dependent `found` feature and their split/training protocol differed. Their frozen bytes were not modified or reused as v019 learned-policy evidence.

## Program audit

`implementation_v019/program.py`, 28,918 bytes, SHA-256 `DDB36E59145228362597DA2E559ED22CA987499E32CB25519293C9D3F4C4375A`:

- constructs the sorted registry and exact two-stage full-370 candidate ranking;
- uses no gold-dependent state feature;
- isolates the Development split and uses training queries only for slow-controller updates;
- reruns target BoR-DQN and target F1-DQN in the same code path as Candidate and ratio ablation;
- implements Candidate terminal utility `lambda*hit-K/N`, zero intermediate utility, `gamma=1`, and the preregistered training-coverage dual update;
- freezes all model weights, split IDs, raw per-query rows, controller histories, conditions, source hashes, elapsed time, and runtime environment;
- has no code path that downloads or opens the prospective Confirmation source during Development.

The actual-data ranking preflight exited `0` and reported `INSTANCE_COUNT=400`, `REGISTRY_SIZE=370`, `CANDIDATE_SIZE=370`, `FOUND_AT_1=0.655000000000`, unique 400 query IDs, and gold-rank range 1 through 370. This fixed-input value is 0.5 percentage points above the notebook's stored `65.0%` display, so v019 does not claim numerical reproduction of that stored output. The paired v019 comparison remains valid because every policy uses the same bound input bytes and rebuilt ranking; the difference further requires keeping the claim at this frozen-input protocol rather than a published-number replication claim.

## Independent audit audit

`implementation_v019/audit.py`, 21,848 bytes, SHA-256 `806794C0D46E706065C058281FE7DB6B1FC598368CB3E59D5D9A78263A1C67C1`:

- independently reopens the fixed input and wheel, rebuilds the registry/rankings, and reconstructs the official split;
- binds config, input, wheel, raw rows, summaries, histories, and every saved model by SHA/size;
- independently recomputes row arithmetic, policy/group query sets, group metrics, policy means, preregistered conditions, slow-controller update values, update episode sequence, and controller continuity;
- independently loads every model and replays every expected learned-policy action over reconstructed score states, so raw K values cannot pass merely because their arithmetic is self-consistent;
- reports maximum raw-row, metric, controller, and model-rollout K errors; any audit error returns exit code `1`.

## Config and tests

- `implementation_v019/config.json`: 2,312 bytes, SHA-256 `BDD2683AF36F5BABED46203A66C419FF3017625A204649909F59B4B0AA478CBF`.
- `implementation_v019/test_objective.py`: 1,516 bytes, SHA-256 `E0FC74C3033B9010158E69829E95E9AC9B571F759B2895001A0894C6BA66E367`.
- Final `py_compile` command over program, audit, and test: exit `0`.
- Final `pytest -q implementation_v019/test_objective.py`: exit `0`, `4 passed in 2.07s`.
- The tests cover gold-independent state, both target reward equations, Candidate/ratio terminal utilities, and both slow-controller updates.

## Shared environment readback

The authoritative interpreter command exited `0` and reported Python `3.11.15`, PyTorch `2.12.0+cu130`, CUDA runtime `13.0`, `cuda_available=true`, one `NVIDIA GeForce RTX 5060 Ti`, capability `12.0`. `nvidia-smi` exited `0` and reported driver `591.86` and 16,311 MiB VRAM. v019 trains these small DQNs on CPU; this readback confirms that the product's shared GPU environment remains callable for later experiments.

## Main-Codex conclusion

No remaining code/protocol defect found in the bounded pre-execution audit would invalidate the one-shot Development. The implementation, config, input, dependency, and cited primary-source bytes must now be copied through `ResearchWorkspace.save_experiment_artifact()`, and the Experiment Plan must bind their resulting hashes before any scientific execution. No Reviewer is authorized at this stage.
