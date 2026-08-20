# Problem v024 — Does Verifier Inspection Mark a Distinct Reward-Hack Phase?

Reward-hackable terminal tasks expose a checker or verifier that an agent can inspect before choosing how to satisfy its surface conditions. A bag of all commands can learn checker-related words but assigns the same coefficient to an action regardless of whether it occurred before or after the first verifier-inspection event. A generic fixed time split can model early/late position but does not identify the event that changes the agent's information state.

The target question is whether a fixed, label-free verifier-inspection anchor yields a task-transferable action phase:

```text
all commands -> commands before first verifier inspection | inspection and later commands
```

The final outcome is released Terminal Wrench rewarded-serious-exploit versus successful-baseline identity. The method is falsified if the anchored representation fails to beat the same-width duplicated-command detector, fixed chronological halves, a position-free anchor-word partition, and all lower-information comparators on task-disjoint data.

No claim is made about hidden intent, causal proof of hacking, exact error localization, online prevention, task success, or trajectories that do not expose verifier inspection in command text.
