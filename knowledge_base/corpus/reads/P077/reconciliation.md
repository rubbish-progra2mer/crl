# P077 Reconciliation

- Disposition: `ACCEPTED_AS_BOUNDED_TEMPORAL_CREDIT_BASELINE`
- Read 1 SHA-256: `053d618af06f08fd00ebdfe17284214561cf9ef9efbff6b41988861f4da6a631`
- Accepted read-2: `read_2_attempts/r2-20260720-p077-a1/`
- Read-2 invocation SHA-256: `c7cf9ef1c803f09b1e0640b3dfb943af485a90a876bce4f143b1ac086f4b27c5`
- Read-2 report SHA-256: `7085f5d45c620eb329bc71f245f4d84395e5a6b55c47017bde36a4c61b4c2939`
- Accepted read-3: `read_3_attempts/r3-20260720-p077-a1/`
- Read-3 invocation SHA-256: `08b93ddd99fa41b8015220c5b836ece65098c67abd24a1d8bf869e8f1748fd0e`
- Read-3 report SHA-256: `08d8015bb10a78e172bf6616d47f7e10ab4f7aaca831fa28cc5cda3e3e68940a`
- Other attempts: none.

## Source reconciliation

- `AGREE`: ArCHer learns an utterance-level off-policy TD Q/V critic over interaction history and trains the within-utterance token actor from the resulting long-horizon advantage.
- `IMPLEMENTATION_BOUNDARY`: high-level Q, high-level V and optional token-prefix baseline are distinct. The paper does not fully specify how double Q/double V estimates are combined into the implemented advantage.
- `SCOPE_BOUNDARY`: the user excludes environment-feedback learning as a target direction. ArCHer is admitted only as canonical temporal-credit lineage and strong baseline, not as a future CRL research direction by itself.
- `CLAIM_NARROWED`: “about 100x” is supported only on Twenty Questions at roughly return -17 using collected trajectories. Environment turns, oracle calls, tokens, FLOPs and wall-clock are not matched.
- `ORACLE_BOUNDARY`: Twenty Questions and Guess My City use a fine-tuned Flan-T5-small simulator; WebShop uses a partial-match scalar reward. These are not human or production task outcomes.
- `FAILURE_RETAINED`: the source shows repetition, malformed questions, contradictory oracle responses and explicit oracle exploitation. A city-name string filter does not eliminate broader reward hacking.
- `MODEL_AND_DATA_BOUNDARY`: most experiments use GPT-2/RoBERTa and task-specific SFT initialization; the 7B study is a narrow ablation, while offline results are preliminary and lack broad offline-RL baselines.
- `THEORY_BOUNDARY`: formal error results rely on strong function-class/coverage assumptions and do not prove neural implementation convergence or the empirical sample-efficiency curve.

## Frozen source role

Strong baseline and lineage source for hierarchical multi-turn credit assignment. Future delayed-credit implements must compare with temporal Bellman credit, but CRL must not import the paper's environment-feedback workflow as an approved target direction.
