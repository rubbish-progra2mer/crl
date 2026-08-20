# Problem v023 — Does Mixing Actions and Observations Hide Role-Specific Reward-Hack Evidence?

Terminal-agent trajectories interleave actions with environment observations. A mixed bag-of-n-grams cannot assign different meanings to the same lexical fragment when it is issued as a command versus returned by the terminal. For example, writing a success claim and observing an independently produced success message have different evidential roles even if they share words.

The target question is whether independent action and observation coefficient blocks improve task-disjoint, reference-free reward-hack detection beyond:

- mixed text, commands only, outputs only and simple command/output concatenation;
- identical three-block capacity with mixed text repeated;
- identical three-block capacity with commands or outputs repeated.

The problem is falsified if AORF fails to beat any capacity-matched duplication control under the preregistered task-cluster test. No general semantic understanding, sequence modeling or causal verification claim is permitted.
