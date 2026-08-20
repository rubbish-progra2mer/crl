# Nearest Prior v032

## Terminal Wrench

Terminal Wrench provides the carrier: real rewarded exploit trajectories,
legitimate baselines, task definitions and stripped command/output views across
three frontier generator families. Its paper reports that stripped monitoring
is materially harder and generator-dependent. It does not propose the v032
conditional normal-action map.

## Task Shield

Task Shield formalizes task alignment through whether lower-privilege
instructions and tool calls contribute to user objectives. Its executable
mechanism uses LLM extraction and an LLM-based continuous `ContributesTo`
judgment with feedback. v032 neither extracts instructions nor invokes an LLM
judge; the overlap is only the established importance of task/action fit.

## Trajectory Guard

Trajectory Guard is the closest method-level prior. It uses a Siamese recurrent
autoencoder, task/trajectory contrastive loss and sequence reconstruction,
trained on good trajectories plus GPT-5 synthesized anomalies. Its paper
explicitly argues that simple pretrained-embedding anomaly baselines are
insufficient. v032 instead tests a supervised direct-text detector augmented by
a successful-only linear conditional innovation on real rewarded exploits. It
does not claim to supersede or reproduce Trajectory Guard.

## D²4FAD, UniVAD and prior Run attempts

Few-normal anomaly detection, latent residuals, ridge regression, TF-IDF,
Truncated SVD and logistic regression are established components. v020-v022
already tested a same-task signed lexical residual; v026 tested same-task
cross-generator support pairs; v031 tested task-to-command cross-encoder
relevance by operation role. Those computations are mandatory negative lineage,
not novelty support.

## Collision judgment and ceiling

No first-ever component or generic anomaly-detection claim is available. The
only potentially supportable contribution is the fixed empirical composition:
equal-task-weight successful-only task-to-action mapping plus an absolute latent
innovation feature, under task-and-generator double holdout on real stripped
Terminal Wrench exploits, against the complete comparator ladder.

The result must be rejected if the successful-only map does not beat the
all-row map, because then its proposed normal-trajectory restriction is not
identified.

