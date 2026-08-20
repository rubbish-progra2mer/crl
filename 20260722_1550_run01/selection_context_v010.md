# Neutral Selection Context

## Version scope

v010 started after v009 failed its preregistered Development promotion conditions. It was required to use a scientifically different failure or computation. TPPA retuning, lower gates, and capacity/null attribution from the v009 one-correction bundle were excluded.

## Data already touched

- The 200 P084 expanded-toolkit Development rows, their gold functions, every v009 ranking, and the 14 cross-encoder errors were already read in v008/v009.
- The pinned BFCL v4 live-multiple Confirmation files were not acquired or read.
- Any v010 analysis of P084 is therefore an explicitly outcome-informed feasibility screen, not an independent confirmation.

## Candidate routes checked

1. **Terminal-state verification on public trajectories.** The browser-visible schema for `jkazdan/taubench_traces_training_data@1c7c8606812a1ce66a28b70999d2f691120600e1` had 50 rows and only a `messages` column, despite its card mentioning success and failure reward. `Snorkeler/tau-bench-react-claude` was empty. A `jerry128` Qwen2.5 trace set had reward but only 10 rows. `mzio/aprm-sft_genthinkact-ENact_prm_taubench_retail_500_fs1-GEaprm_qwen3_ap-SE42-REv10_lr1e04-b009@f1f73975183eaeead8e951754f0937049a6d859d` exposed 500 task IDs, four generations, step state/action/observation, reward, return, and done fields, but its README contained only generated dataset metadata and did not define whether reward/return came from the τ-bench environment or a process reward model. These bytes were not used as task-success labels.
2. **NLI scope verification.** `cross-encoder/nli-MiniLM2-L6-H768@b95119ce93d3e065de6214e38cd4a97b0f2f2c6d` was investigated as an atomic scope-support scorer. A broad temporary download timed out after about 604 seconds. It left a complete ONNX file of 328,649,957 bytes whose SHA-256 `807d33fffeFD95AD60E2A91F54EED50A92AA53C077945A6842BB587A49A3FDF3` matches the repository tree manifest, but the locked Python 3.11 environment has no ONNX Runtime and the PyTorch/tokenizer snapshot remained incomplete after repeated shell TLS failures. Conda base has ONNX Runtime only under Python 3.13 and was not used. `CRL_ENVIRONMENT.md` forbids Conda fallback and requires explicit user approval before refreshing the shared lock, so no scientific result was produced.
3. **Menu-relative lexical scope reranking.** A temporary main-Codex probe used query-hash grouped five-fold out-of-fold evaluation on the 200 already-touched P084 rows. The fixed cross-encoder baseline was top-1 `0.930`, MRR `0.9591667`. A learned three-score fusion fell to top-1 `0.910` with 2 corrections and 6 regressions. Adding menu-relative name/description/parameter scope features reached top-1 `0.915`, MRR `0.95125`, with 3 corrections and 6 regressions. A nested selective threshold retained 3 changes, all regressions, and remained at top-1 `0.915`. The probe source SHA-256 is `aba97f6d7eb7e09f9f76a07319bba3f4a28ccaa5917a544faf72d10daef3d7cc`; it is a temporary selection artifact, not a frozen experiment.

## Optional-stopping disclosure

v010 was informed by the full v009 result and the observed P084 errors. No v010 Candidate, implementation, Experiment Plan, Development capture, Confirmation, Review Packet, Reviewer, or Decision was created. The three checked routes are closed for v010 rather than retuned after their observed limitations.
