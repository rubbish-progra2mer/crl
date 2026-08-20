# Nearest Prior v034

## ToolPRMBench

ToolPRMBench is the data and task carrier. It defines pairwise step-level
judgment from interaction history, a correct action, a plausible incorrect
action and tool metadata. Its paper evaluates open models, general reward
models and tool-specialized PRMs and reports that scale alone is insufficient.
It trains ToolPRM Base, CoT and GRPO variants and does not propose v034's fixed
pointwise obligation projections, other-source empirical calibration or
weakest-obligation score.

The v034 source PDF has SHA-256
`f7ac155d9862f0def0b1f5c09e992dc7b626fdf90601a8cb2e8a9bcbd6712455`.

## Recursive Rubric Decomposition

RRD is the closest decomposition prior. It recursively decomposes evaluation
rubrics, filters misaligned and redundant sub-rubrics, and uses
correlation-aware aggregation. Therefore neither decomposition nor
multi-criterion judging is novel here.

v034 differs narrowly: its five obligations and evidence projections are fixed
before execution and mechanically tied to tool schemas and histories; it
generates no rubric, estimates no rubric relevance from labels, and uses a hard
minimum after unlabeled cross-source empirical calibration rather than a
weighted aggregate. These differences are a testable composition, not a broad
method novelty claim.

The frozen RRD PDF has SHA-256
`0d8220373db270500024e34575ce77129bad1a31842443838742d2cc8c22110c`.

## ToolRM

ToolRM is the closest learned pairwise evaluator. It constructs tool-use
preference data, includes rule-based matching of tool calls, and trains
generative and discriminative reward models to choose between paired
responses. v034 does not reproduce or compete with its training pipeline. Its
supervised linear ensemble is only a fixed same-evidence Development control;
the language model remains frozen.

The frozen ToolRM PDF has SHA-256
`9679fe106dfc881cfdaf7e77cd6b38c871da2e503b4964f91f2fe0a8293f714f`.

## Tool-Verifier and ToolGate

Tool-Verifier combines an executable outcome-consistency check against golden
database state with an LLM committee's process-consistency judgment, then
trains a 7B verifier. ToolGate uses Hoare-style preconditions and
postconditions over trusted state, while noting limitations when response
schemas are unavailable.

v034 executes nothing, has no trusted state hash and provides no formal
guarantee. Its `grounding` and `progress` obligations are text-only
likelihoods. Any passing Claim must keep this distinction explicit.

The frozen Tool-Verifier PDF has SHA-256
`2ab5d9b8a426c138d1bfdd0b8d4af01feb2d7d1dfae989417862c19b05133945`.
The formal-knowledge-base ToolGate PDF has SHA-256
`7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d`.

## Collision judgment and ceiling

The components—pairwise judging, fixed criteria, empirical calibration,
minimum aggregation and tool-contract inspection—are not individually novel.
The only potentially supportable contribution is the complete fixed
composition under source holdout and untouched ToolSandbox confirmation,
against controls that isolate projection, aggregation and supervised
combination.

The result must be rejected if CCCB does not strictly beat the same-evidence
calibrated mean, selected-single and supervised linear ensemble, because then
the proposed conjunctive bottleneck is not identified.
