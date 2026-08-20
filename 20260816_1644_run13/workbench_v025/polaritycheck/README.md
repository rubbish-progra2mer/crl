# polaritycheck

**Corpus, harness, and frozen results for** *Similarity Gates Approve Reversals: A Validity Audit of Embedding-Cosine Thresholds in Agent Systems*

**Scott E. Frias · Eigenforma / Freemind Labs** · [eigenforma.com](https://eigenforma.com) · 2026 · arXiv ID pending · paper: [`docs/paper.md`](docs/paper.md)

Agent systems ship quality gates that threshold the cosine similarity of two texts'
embeddings: deduplication filters, semantic caches, drift guards, answer graders. This
artifact contains everything behind the paper's audit of that gate class: the balanced
2×2 factorial corpus and the encoder-blind method that builds it, the two drift-guard
corpora (one authored under documented isolation), the audit harnesses for nine encoder
configurations and the shipped framework components, the frozen results every number in
the paper is read from, the prevalence survey's source record, and the machine check of
the §9 closed form. Everything runs offline against pinned local models; the headline
numbers also recompute from the frozen JSON with no models installed at all.

**Licences.** Code is MIT (see [LICENSE](LICENSE)). **The corpora and frozen measurement
records (`corpus/`, `results/`, `survey/`) are CC-BY-4.0**, not MIT.

---

## Quickstart: recompute the headline numbers (no models, no installs)

Pure standard library — works on a bare Python ≥ 3.10:

```
python scripts/recompute_headline_counts.py
```

verifies, from the frozen JSON in `results/`: the naive design's decision AUROC of
exactly 0.000 in **13 of 18** configuration-task cells (≤ 0.040 in all 18); the matched-overlap
**29-of-36** direction count; the stratified decision-AUROC field 0.440–0.815 with the
production configuration at 0.535/0.440; the drift guard's **0-of-56** catches including
the `withhold → administer` specimen at cosine 0.9608; the NLI drop-in at 0.831
in-sample / 0.533 held-out; and the repair arms at 0.485/0.433 and 0.750/0.533 (§3, §5,
§6, §7).

Also model-free:

```
python harness/threshold_free_reanalysis/run_auroc_reanalysis.py   # re-derives every AUROC/CI from frozen per-row scores
python harness/factorial_pilot/build_corpus.py                     # rebuilds the 2x2 corpora, encoder-blind, + balance check
python harness/lib/stats.py                                        # statistics self-check (AUROC vs brute force, edge cases)
python harness/r13_hyperbolic/wild_instance_check.py               # §9 no-op demonstrated on described third-party code (numpy only)
python harness/r13_hyperbolic/proposition.py                       # §9 closed form: symbolic proof + check vs audited code (sympy+torch, no models)
```

## Full reproduction against pinned local models

1. Install the pinned environment (the audited packages must be at these exact
   versions — the harness reads their shipped thresholds from the installed code):

   ```
   pip install -r requirements.txt
   ```

2. Download the checkpoints once, with the network on (afterwards everything runs with
   `HF_HUB_OFFLINE=1`, which the harness sets itself):

   ```
   python -c "from sentence_transformers import SentenceTransformer as S; [S(m) for m in ['sentence-transformers/all-MiniLM-L6-v2','sentence-transformers/all-mpnet-base-v2','BAAI/bge-base-en-v1.5','thenlper/gte-base','intfloat/e5-base-v2','mixedbread-ai/mxbai-embed-large-v1']]"
   python -c "from transformers import AutoModel; AutoModel.from_pretrained('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True)"
   python -c "from huggingface_hub import snapshot_download; snapshot_download('cross-encoder/nli-MiniLM2-L6-H768', revision='b95119ce93d3e065de6214e38cd4a97b0f2f2c6d')"
   ```

3. Run any experiment with one command from the repository root (each writes a
   date-stamped JSON next to the frozen evidence; frozen files are never overwritten):

| paper § | experiment | one command | needs models? |
|---|---|---|---|
| §3, §5 | factorial pilot: manipulation check, 9 configurations, naive-vs-stratified, shipped thresholds | `python harness/factorial_pilot/run_factorial_pilot.py` | yes (all 7 checkpoints) |
| §5 | graded lexical reanalysis (pole-placement control) | `python harness/factorial_pilot/run_graded_lexical.py` | yes |
| §5 | mechanism variance: continuous score, top-k mining, adaptive chunker | `python harness/framework_audit/run_mechanism_variance.py` | yes |
| §6 | framework components at installed defaults (grader / filter / cache) | `python harness/framework_audit/run_framework_audit.py` | yes |
| §6 | drift guard vs in-sample corpus (reproduces frozen cosine+NLI bit-for-bit) | `python harness/guard_stack/run_guard_stack.py` | yes (nomic + NLI) |
| §6 | drift guard vs held-out corpus | `python harness/guard_stack/run_guard_stack.py --heldout` | yes (nomic + NLI) |
| §7 | pre-registered repairs (encoder swap; conditioned gate) | `python harness/h2_intervention/run_h2_intervention.py` | yes (mxbai + nomic) |
| §3, §7 | hypothesis-distinctness probe (cosine gate vs NLI) | `python harness/r14_nli_distinctness/run_r14_falsifier.py --holdout` | yes (nomic + NLI) |
| §3, §7 | threshold-free reanalysis of the frozen evidence | `python harness/threshold_free_reanalysis/run_auroc_reanalysis.py` | **no** |
| §9 | closed-form machine check across curvatures + wild-instance demonstration | `python harness/r13_hyperbolic/proposition.py` and `.../wild_instance_check.py` | **no** |
| §2, §10 | prevalence survey | source record at `survey/prevalence_survey_2026-07-26.md` (queries recorded verbatim) | — |

### Pinned model checkpoints

| checkpoint | role | pin |
|---|---|---|
| `nomic-ai/nomic-embed-text-v1.5` | the audited production path (MRL-256, `search_document:` prefix) and the `clustering:` sensitivity variant | model card revision current at run date; MRL truncation + pooling fixed in `harness/audited_system.py` |
| `sentence-transformers/all-MiniLM-L6-v2` | encoder field | HF hub |
| `sentence-transformers/all-mpnet-base-v2` | encoder field | HF hub |
| `BAAI/bge-base-en-v1.5` | encoder field | HF hub |
| `thenlper/gte-base` | encoder field | HF hub |
| `intfloat/e5-base-v2` | encoder field (2 prefix variants) | HF hub |
| `mixedbread-ai/mxbai-embed-large-v1` | encoder field (explicitly normalised) | HF hub |
| `cross-encoder/nli-MiniLM2-L6-H768` | the NLI drop-in (§7) and guard NLI layer | **revision `b95119ce93d3e065de6214e38cd4a97b0f2f2c6d`** |

All models run on CPU. Nine encoder configurations are derived from the seven embedding
checkpoints (two prefix variants each for nomic and e5); see
`harness/factorial_pilot/encoders.py`.

## Inventory

| path | contents |
|---|---|
| `docs/paper.md` | the paper (markdown source) |
| `corpus/distinctness_2x2.jsonl`, `corpus/constraint_2x2.jsonl` | the 2×2 factorial corpora: 80 pairs, 10 anchors × 4 cells × 2 tasks, per-pair provenance (`match_target`, `match_achieved`, `candidates_considered`, author, annotator slots) |
| `corpus/negation_corpus.json` | in-sample drift corpus: 26 mutations + 5 faithful controls, per-case provenance |
| `corpus/heldout_drift_corpus.json` | held-out drift corpus: 30 mutations + 10 controls, `authoring_isolation` documented |
| `harness/audited_system.py` | the audited system's production embedding path and pinned NLI classifier, extracted verbatim in their math (drift threshold 0.40; duplicate-gate threshold 0.85) |
| `harness/factorial_pilot/` | corpus builder (encoder-blind matching), lexical metrics, encoder registry, §3/§5 runners |
| `harness/guard_stack/` | §6 drift-guard runners + shared catch predicates |
| `harness/framework_audit/` | §5/§6 framework probes at installed defaults |
| `harness/h2_intervention/` | §7 pre-registered repair study |
| `harness/r14_nli_distinctness/` | §3/§7 distinctness probe |
| `harness/threshold_free_reanalysis/` | model-free AUROC/CI re-derivation |
| `harness/r13_hyperbolic/` | §9: audited Poincaré implementation (first-party, extracted), symbolic + numeric closed-form check, wild-instance demonstration |
| `harness/lib/` | pure-stdlib statistics (AUROC, bootstrap, exact permutation p, κ) and evidence hygiene |
| `results/` | the frozen evidence, one JSON per run date — every number in the paper reads from these |
| `survey/prevalence_survey_2026-07-26.md` | the prevalence survey source record (queries verbatim, opened-and-read verdicts, caps reported, correction appended) |
| `scripts/recompute_headline_counts.py` | the no-model headline verification |

## Notes for auditors

* **Redaction (2026-07-28).** Before release, the frozen JSONs under `results/` were
  redacted of internal run context: machine hostnames now read `redacted`, and
  provenance strings that pointed into the private research repository (file paths,
  config pointers, internal unit and document names) were rewritten as neutral
  descriptions of the same facts. **No measurement field was touched.** The one probe
  whose *input texts* contained internal names (the distinctness probe,
  `harness/r14_nli_distinctness/`) was re-run after a like-for-like rename of those
  inputs, and the threshold-free reanalysis was re-derived from the re-run evidence;
  every paper-cited number reproduced exactly, and
  `scripts/recompute_headline_counts.py` passes all headline checks against the
  released files. Harness runners no longer stamp the machine hostname into output.
* **The audited system's third guard layer.** The audited guard stack includes a stdlib
  constraint-ledger layer that belongs to the audited system's internal codebase and is
  not redistributed. The frozen guard-stack JSONs retain its columns; the paper's §6/§7
  claims rest on the `cosine` and `nli` columns, which `harness/guard_stack/` reproduces
  bit-for-bit (an automatic reproduction check runs on every execution).
* **No third-party code is redistributed.** See `THIRD_PARTY_NOTICES.md`, in
  particular why `wild_instance_check.py` re-implements the wild instance from a prose
  description.
* **Re-runs never overwrite frozen files.** Runners write date-stamped (or
  `_rerun_`-tagged) siblings and, where applicable, assert bit-level reproduction
  against the frozen evidence.
