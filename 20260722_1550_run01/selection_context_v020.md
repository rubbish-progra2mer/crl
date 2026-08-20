# Selection Context v020

## Starting boundary

v019 is frozen `NO_GO_FOR_CONFIRMATION`: its coverage-constrained DQN selected all 370 tools for every Development query in all three seeds. v020 does not retune that optimizer, dual, episode count, or gate.

The initially considered exact adaptive-depth route was rejected during selection. Bounded current-prior search found direct coverage of query-specific adaptive K, conformal retrieval sets, adaptive coverage policies, score-threshold Adaptive-k, AutoSearch, and training-free stopping. Replacing DQN with a calibrated predictor or exact threshold solver would therefore be a crowded optimization substitution rather than a defensible new computation.

## Selected failure carrier

v012 left a real prospective boundary in Terminal Wrench:

- fixed repository commit `d8a29613235a0ef56a8b70b3142626a533da28c2`;
- exposed Development bucket `SHA256(task_id)[0] mod 4 == 2`;
- unacquired Confirmation bucket `SHA256(task_id)[0] mod 4 == 3`;
- one successful baseline trajectory can be reserved per eligible task and excluded from evaluated rows;
- the evaluation condition contains task prompt, shell commands, and terminal outputs but no agent commentary.

The v012 Development bytes and held-out outcomes are exposed. v020 therefore has elevated optional-stopping risk and cannot use its Development split as confirmation. v020 may reuse those bytes only for a scientifically different representation and must preserve bucket 3 as unread until a positive main-Codex Promotion Audit.

## Empirical failure inherited from v012

v012 compressed each evaluated/reference pair into 29 coarse executable, effect, path, write, sequence, and dataflow features, then appended them to a strong character TF-IDF classifier. On 20 held-out Development tasks, the text baseline reached AUC `0.9002797831`, while RCED reached `0.8261890781`; task-bootstrap delta was negative. Main-Codex case readback found legitimate alternate workflows can diverge strongly from one reference, while coarse effect sequences can make exploits resemble normal implementation.

The v020 intervention therefore does not add or retune another coarse scalar. It preserves exact lexical/action fragments in a signed sparse residual relative to the same excluded successful trajectory. It tests whether the failure came from semantic compression rather than from task-relative comparison itself.

## Primary-source boundary

- Terminal Wrench reports that action/observation-only monitoring remains possible but weaker than reasoning-visible monitoring: stripped AUC `0.9168`, TPR@5%FPR `0.44` for its LLM judge.
- Cheap Reward Hacking Detection reports a stripped-trained action-surface encoder at AUC `0.7631`, TPR@5%FPR `0.2275`; its full reasoning-visible encoder is much stronger. Those published numbers are not on the v020 split and are context, not same-byte baselines.
- TRACE reports that contrastive clusters improve LLM reward-hack detection over isolated classification. v020 therefore does not claim the first contrastive detector.
- Praetor compiles multiple verified benign tool traces into a sequential pDFA and is a nearest benign-envelope system, but it targets structured-workflow runtime blocking rather than task-disjoint Terminal Wrench trajectory classification.

## Selection decision

Promote one v020 Candidate for one frozen Development execution: Task-Relative Signed Sparse Residuals. No model generation, LLM judge call, environment mutation, or new trajectory generation is required. If the representation does not beat all same-input, same-learner comparators under the frozen gates, v020 ends without Confirmation.

No Reviewer is authorized during selection, implementation, Development, or Promotion Audit.
