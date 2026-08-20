# Research Map v039

Scientific map: exactly v037/v038 ECDS.

Execution-binding delta:

```text
- --output dev_output_001
+ --output dev_output_001/raw_predictions.jsonl
+ --output dev_output_001/summary.json
+ --output dev_output_001/environment.json
+ --output dev_output_001/frozen_state.json
```

No executable scientific byte changes. v038 disclosed output hashes but lacks a
valid capture and cannot be audited under its Plan. v039 permits one new,
non-overwriting output path and one exact capture; the unchanged preregistered
gates decide promotion.
