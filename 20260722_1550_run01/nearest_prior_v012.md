# Nearest Prior Work v012

## Search question

What is the nearest existing method to a task-conditioned action-only terminal reward-hack detector that compares an evaluated command sequence with one successful same-task trajectory?

## Direct comparison

| Work | Input and split | Core computation | Exact overlap with RCED | Remaining difference |
|---|---|---|---|---|
| Cheap Reward Hacking Detection, arXiv:2606.08893 | Terminal Wrench, task-ID-disjoint; includes a separately trained stripped-trajectory encoder | Learned text encoder/classifier over trajectory content | Same benchmark family, action-only ablation, reward-hack label | Does not designate one successful same-task reference or compute explicit evaluated-minus-reference shell-effect/dataflow features |
| Praetor, arXiv:2604.26274 | Verified benign structured tool-call telemetry | Learns pDFA sequence and parameter guards and enforces them online | Benign-reference trajectory constraints, sequence and parameter deviations | Assumes structured/repeated workflows and multiple benign traces; RCED uses one task-specific shell trace, coarse parser features, and supervised offline classification |
| TRACE, arXiv:2601.20103 | Curated synthetic paired trajectories | Contrastive LLM analysis of benign and hacking behavior | Contrastive trajectory inspection | LLM reasoning rather than deterministic effect deltas; synthetic benchmark rather than Terminal Wrench task-disjoint evaluation |
| Terminal Wrench, arXiv:2604.17596 | 331 real terminal tasks, serious exploit and successful baseline trajectories | Benchmark plus LLM-as-judge monitoring baselines | Exact dataset and action-visible evaluation surface | Supplies data/evaluation, not RCED's reference-conditioned representation |

## Collision judgment

- **Exact method collision:** not found in the four directly read closest sources.
- **Component collision:** present. Praetor covers benign trajectory envelopes; Cheap Reward Hacking covers stripped action-only detection; TRACE covers contrastive analysis.
- **Surviving narrow contribution:** the combination of a deterministic single-reference task control with ordered open-shell effect/dataflow deltas, evaluated as an additive computation against the same text learner on task-disjoint Terminal Wrench.
- **Novelty ceiling:** at most a narrow empirical method claim. The work cannot claim the first trajectory monitor, first action-only monitor, first benign-reference monitor, or first reward-hack detector.

## Fixed source bytes

| Path | SHA-256 |
|---|---|
| `sources_v012/cheap_reward_hacking_2606.08893.pdf` | `C5FD945125B1B6CD4739B2AACF150156BBFC8E47AFF2D7240EA05ED697075CE0` |
| `sources_v012/praetor_2604.26274.pdf` | `842D593F53486481D384C8407D2FD688BBFBF90B69E505DB54BC31008A15AA98` |
| `sources_v012/terminal_wrench_2604.17596.pdf` | `140DF68E633BCB5544E37B67A6F362A917F7A38B566B25E1B42FE86BEB619E8A` |
| `sources_v012/trace_2601.20103.pdf` | `98A3121DE46018F08F47A8DB18B4ED55C9D117BEB5E984EAA9F3C2A47F3A5649` |

