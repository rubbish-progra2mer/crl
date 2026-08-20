# Research Problem

## User intent

v006 = v005 with one corrected reader parameter. The scientific problem,
Use Thesis, occupancy scan, Mechanism Demand, carrier-independent
statement and kill conditions are UNCHANGED from problem_v005.md (SHA
3ffc013a67aae7331cd6975ec62eb866e6781a4bc1e6eb5d89a05a41bdbb9fec),
incorporated here by reference per the version-advance rule: the v005
reader arm was invalidated by a config defect (max_tokens=100 exhausted
by deepseek-v4-flash reasoning tokens in 47/111 rows, arm-varying,
confounding), so the consequence arm re-runs under max_tokens=1000.

## What v006 changes

config.json reader.max_tokens: 100 -> 1000. Nothing else: same encoder,
same prompts, same arms, same D bucket, same judge protocol.

## What v006 inherits as already established

The retrieval-stage decomposition REPLICATED on the untouched D bucket
in v005 (inversion 22/37 turn/direct; sentence 16/37 with margin
improvement; propagation ~0; recency 6/37 with non-update harm
6.52->5.91). Kills 1-2 not triggered; Kill 3 (consequence) undecided
and is the sole open question for v006.

## Cost authorization

Unchanged (deepseek preauthorized; ~111 calls expected, still < 2 USD
at max_tokens=1000).
