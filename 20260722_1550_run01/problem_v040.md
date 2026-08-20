# Problem v040

CMCD averages a pair classifier's scores over all successful support traces.
When the two allowed support generator families contribute different numbers of
traces, the family with more traces receives more inference mass. That trace
count is an availability artifact, not a preregistered reliability estimate.

The research question is whether equal mass per support generator family,
without retraining or target-generator calibration, improves reward-hack
detection under held-out task and generator evaluation relative to the original
trace mean and all v026 controls.

The problem is not generic group robustness. It is restricted to Terminal
Wrench's fixed known-good cross-generator support protocol.
