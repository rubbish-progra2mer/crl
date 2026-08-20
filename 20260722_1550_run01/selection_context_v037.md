# v037 Selection Context

## Durable boundary

v036 SDEJ is frozen `NO_GO_FOR_CONFIRMATION`. Its frozen 0.6B judge chose
displayed A on 315/315 forward prompts and 313/315 reverse prompts; the
order-symmetric Candidate reached `0.507937` and only `1/8` gates. v037 may not
retune SDEJ prompts, fields, evidence, verdict tokens, aggregation, model,
controls or gates.

v037 removes verdict tokens and candidate positions entirely. It evaluates
teacher-forced likelihood of each action separately.

## Exposure

GTA, BFCL and ToolTalk remain exposed Development. ToolSandbox remains absent,
unacquired and unread. Selecting v037 after v034--v036 is optional stopping and
must be judged only as Development until untouched Confirmation.

One disclosed no-model descriptive probe compared exact token grounding of
non-shared fields. It exited `0` and produced:

- GTA accuracy `0.868644`;
- BFCL `0.414414`;
- ToolTalk `0.453488`.

This rejects exact grounding as a Candidate because its signal is
source-specific. No other v037 feature or model score was screened.

## Three formal Card queries

Exactly three production Card queries ran, each exit `0`:

1. failure:
   `pairwise judge position bias fixed label tokens action likelihood`;
2. operator:
   `conditional likelihood changed tokens tool action contrastive scoring`;
3. paper:
   `function calling reward likelihood action preference token loss`.

Key hits were:

- `failure-likelihood-utility-does-not-guarantee-agent-utility`;
- `failure-tool-description-and-order-bias`;
- `operator-future-token-loss-filtered-tool-learning`;
- `operator-action-preserving-observation-contextualization`;
- `paper-p082` Toolformer;
- `paper-p069`;
- `paper-p084`;
- `paper-p085`.

## Primary collision

The main Codex directly read Toolformer physical pages 2--4. Toolformer
retains API calls when adding the call and result lowers loss on subsequent
natural-text tokens, then finetunes a model. v037 neither executes tools nor
predicts later task text. It measures how frozen history/contracts change
likelihood at aligned differential positions inside each proposed next action.

Likelihood remains a proxy and cannot support downstream Agent-success,
cost or safety claims.

## Selected computation

For each action, compare teacher-forced mean log likelihood at deterministic
alignment-differential positions under full evidence versus an otherwise
matched evidence-withheld context. Pure insertion/deletion edits use the
adjacent shared boundary token on the empty side. The difference is
evidence-conditioned surprisal reduction. Compare this gain between chosen and
rejected actions without A/B labels, position tokens, generation, fitting or
source calibration.
