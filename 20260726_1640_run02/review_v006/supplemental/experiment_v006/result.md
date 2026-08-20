# Experiment Result

```json
{
  "experiment_id": "v006",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "6ac36d2acaf1e374fdf931457aae39e7b677fbb07e12ae6d9ea1c8b8031b76fb",
  "candidate_sha256": "3dcadcdbb8aa88e81a1d0c8d51d15a30f154cf6c949aab7fb84a94a6412c6317",
  "evidence_packet_sha256": "e45c15b3dc5c98badc93f20ca92880e44f6fd8ea5673b16c9dd567b89316f4f1",
  "execution": {
    "command": "captured: dev_reader_001 (reader_arm.py, corrected config), argv in captures/dev_reader_001/execution.json",
    "cwd": "D:\\Desktop\\crl\\20260726_1640_run02\\implementation_v006",
    "exit_code": 0,
    "stdout": "see captures/dev_reader_001/stdout.bin",
    "stderr": "see captures/dev_reader_001/stderr.bin",
    "environment": {
      "encoder": "all-MiniLM-L6-v2",
      "python": "3.11.15 (.venv)",
      "reader_max_tokens": "1000",
      "reader_model_field": "deepseek-v4-flash"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v006/artifacts/measure_decomposition.py",
      "byte_count": 7547,
      "sha256": "c171a710986453350d7c24e214f7a0f5ee8338e86613d7d6b4bece44f3a108bc"
    },
    {
      "relative_path": "experiment_v006/artifacts/reader_arm.py",
      "byte_count": 6678,
      "sha256": "dbbd3233eecb40a2ae33c1dc8f62aae77447529af3e2814317c658d8c894a4f0"
    },
    {
      "relative_path": "experiment_v006/artifacts/config.json",
      "byte_count": 972,
      "sha256": "daf7c2e76ac4d7859327a97479eb7cb0dc8e4a23ee1b45eb6299e533f0c5c18f"
    }
  ]
}
```

## Codex Interpretation

v006 dev_reader_001 (corrected config, max_tokens=1000): 111/111
rows complete, 0 empty answers, model_field deepseek-v4-flash on every
row, usage 123,704 in / 14,496 out tokens (cumulative both versions
well under 1 USD).

Automatic scoring (normalized substring + 0.8 content-word overlap):
turn_topk 21/37, sentence_topk 24/37, oracle_current 22/37.

MANUAL REVIEW (required by plan; every changed verdict listed):
Equivalent-expression corrections (auto-scorer false negatives):
- 6a1eabeb all 3 arms: "25:50" == gold "(or 25:50)" -> correct.
- 89941a93 all 3 arms: "four bikes" == gold "4" -> correct.
- a1eacc2a all 3 arms: "7 short stories" == gold "seven" -> correct.
- e493bb7c all 3 arms: answer states bedroom placement == gold -> correct.
- 5c40ec5b all 3 arms: "twice"/"2 times" == gold -> correct.
- 8fb83627 sentence arm: "5 issues" == gold "Five" -> correct.
- 07741c45 oracle arm: "shoe rack in your closet" == gold -> correct.
- Abstention items (031748ae_abs, 2698e78f_abs, 0ddfec37_abs,
  f685340e_abs): all 3 arms correctly answer information-not-available
  == gold -> correct (12 verdicts changed).
- 031748ae oracle arm: partial (gives 5, omits 4) -> left INCORRECT
  (conservative).
Post-review accuracies: turn_topk 30/37 (81.1%), sentence_topk 34/37
(91.9%), oracle_current 32/37 (86.5%).

KILL 3 NOT TRIGGERED: turn_topk shows a real deficit (30 vs 32 oracle,
30 vs 34 sentence), and its unique errors are dominated by STALE
answers - the reader confidently returns the superseded value in 5
items (852ce960 "$350,000" vs gold "$400,000"; 618f13b2 "four times"
vs "six"; 59524333 "7:00 pm" vs "6:00 pm"; c7dc5443 "3-2" vs "5-2";
affe2881 "27" vs "32"), exactly the answer-level conversion of the
retrieval-stage inversion. Sentence-level retrieval removes most stale
answers (its 3 residual errors are 1 miss, 1 abstention-miss, 1 partial),
consistent with the dilution share measured at the retrieval stage.
Note: sentence_topk even exceeds oracle_current (34 vs 32) because the
oracle arm restricts context to the current evidence session and loses
cross-session context on 2 items - an honest boundary observation, not
a claim.

All three preregistered kill conditions are now resolved as
NOT TRIGGERED (kills 1-2 in v005 dev_local_001; kill 3 here). The
candidate's decomposition claims hold on fresh D-bucket data at both
the retrieval stage and the answer stage, within the scoped claim
contract (single encoder, single reader, this dataset). Sample-size
honesty: 37 update items; the turn-vs-sentence answer delta is
4/37 (~11pp) with a wide interval; claims carry intervals, not point
brags. C bucket remains reserved and untouched.