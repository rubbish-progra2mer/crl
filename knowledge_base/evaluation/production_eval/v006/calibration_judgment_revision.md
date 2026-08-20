# Production retrieval v006 calibration judgment revision

- Revised before any v006 calibration or blind retrieval execution.
- Revised query: `prod-cal-failure-002`.
- Raw independent annotation preserved at `calibration_judgment_attempts/cj-20260720-v006-a1/judgments_raw.json`, SHA-256 `252db66216de6576eab14f2b6f09d585f081ed7e7458ed86c0890fdaafc00a4f`.

The annotator required one experiment to satisfy the query's entire conjunction of model, token, tool-call, demonstration, prompt and terminal-state controls. That is stricter than the approved Gate: Card top-k tests whether CRL discovers knowledge materially bearing on the question; missing future controls stay explicit evidence boundaries.

The revised judgment therefore binds four current Failure Cards to six exact Evidence/Passage records covering independent-sampling budget confounds, description/order prompt bias, terminal-state false success and the single-turn-to-stateful evaluation gap. It does not assert that a single source has already demonstrated a gain collapse under every control.

No Card, Evidence, query, source, database, index or retrieval component was changed, and no rank or retrieval result existed when this revision was made.
