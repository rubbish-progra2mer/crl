# Nearest Prior v040

## Cross-Model Consensus Deviation

The exact nearest implementation is frozen v026 CMCD:

- Candidate:
  `b43922594122236b08fcdd94836a5731a8d1cc91c49e7a0a918b51a225bc5f61`;
- raw predictions:
  `ee4a8c5961def6500b8f82105821c104347a337589f1ef0a067fa3ae961a87b8`;
- summary:
  `a14aab0834aea724daa6daa29d658b5f6c0544b6b9fb61257adf8ee43cfb000c`.

CMCD uses the same pair scorer but trace-level mean aggregation. SFEC changes
only the reduction to equal support-family mass. Original CMCD remains a
mandatory comparator.

## Group DRO

Sagawa et al. minimize worst empirical loss across predefined training groups
and show that worst-group generalization in overparameterized models depends on
regularization. SFEC neither optimizes a worst-group loss nor changes training.
The source bounds the broader collision and cautions against a generic
group-robustness claim.

Frozen PDF SHA-256:
`7342848c5921ff5cedf2c27a0f84e38c221c085a9ce28befd9208f2bb0fe36d6`.

## Terminal Wrench and detection lineage

Terminal Wrench defines the stripped-action reward-hack carrier. Cheap Reward
Hacking and Trajectory-Guard bound the reward-hack detection and trajectory
monitoring families. SFEC claims none of their tasks or generic safety scope.

PDF SHA-256:

- Terminal Wrench:
  `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`;
- Cheap Reward Hacking:
  `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`;
- Trajectory-Guard:
  `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`.

## Claim ceiling

Even a pass supports only equal support-generator-family aggregation for the
fixed Terminal Wrench protocol. No generic group DRO, unseen-model universality,
online monitoring, safety guarantee or first-ever novelty claim is allowed.
