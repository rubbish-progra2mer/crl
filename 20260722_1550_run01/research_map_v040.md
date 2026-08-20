# Research Map v040

## Changed computation

Let `s(q,r)` be the frozen CMCD pair classifier score for evaluated trajectory
`q` and allowed successful support trajectory `r`. Let `R_h(q)` be the supports
from generator family `h`, and `H(q)` the available support families.

```text
SFEC(q) =
  mean_{h in H(q)} mean_{r in R_h(q)} s(q,r)
```

The original CMCD control is:

```text
CMCD(q) = mean_{r in union_h R_h(q)} s(q,r)
```

The scorer training, vectorizer, absolute-deviation representation, held-out
task/generator protocol and class weighting are byte-identical. Only the
held-out inference reduction changes.

## Nearest boundaries

- CMCD is the exact nearest computation and mandatory strong control.
- generic hierarchical/equal-group means are prior art; no aggregation novelty
  is claimed.
- group DRO optimizes worst-group training loss; SFEC does not change the loss
  and is not group DRO.
- Terminal Wrench supplies the benchmark and known-good support carrier.

## Falsifiers

SFEC fails if it does not beat original CMCD and every other matched control by
the unchanged gates, if any target-generator delta is negative, or if untouched
bucket 0 does not reproduce the advantage.
