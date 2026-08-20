# Research Map v037

## Changed computation

For candidate action `a`, context evidence `e` and an evidence-withheld matched
context `e0`, let `D(a,b)` be token positions in the non-equal token-alignment
opcodes. On the empty side of a pure insertion/deletion, `D` contains the
immediately following shared boundary token, or the preceding token for an
end edit.

```text
gain(a | e, e0, b) =
  mean_{t in D(a,b)} log p(a_t | e, a_<t)
  - mean_{t in D(a,b)} log p(a_t | e0, a_<t)
```

The Candidate prefers the action with larger gain. This is
Evidence-Conditioned Differential Surprisal (`ECDS`).

## Nearest families and boundary

- Toolformer uses reduction in future natural-text loss after a tool call and
  result to filter training calls; ECDS scores tokens inside frozen candidate
  actions and performs no tool execution or training.
- ToolRM trains full-pair reward models; ECDS is training-free and pointwise.
- generic language-model sequence scoring is prior art; only the complete
  evidence-subtracted, aligned-differential-position composition is under test.
- v036 SDEJ uses A/B verdict probabilities; ECDS has no verdict token or pair
  position.

## Mandatory controls

1. full-evidence differential-token likelihood without evidence subtraction;
2. evidence gain over every action token rather than only differential
   positions;
3. evidence-withheld differential-token likelihood;
4. full-evidence full-action likelihood.

The strongest observed control is fixed from Development and carried unchanged
to Confirmation.

## Falsifiers

ECDS fails if it does not beat both differential-token likelihood and
full-action evidence gain, if gains are confined to one source, or if
evidence-withheld fluency performs as well. Language-model likelihood cannot
be promoted to task utility under any result.
