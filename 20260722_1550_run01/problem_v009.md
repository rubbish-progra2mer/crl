# Research Problem

Can a query-to-schema retriever reduce wrong-function selection in compact menus of semantically related tools by aligning observable query value spans to required parameters with type constraints, one-use capacity, and an explicit null option?

The target failure is the documented degradation under BFCL expanded toolkits: the user request is fixed while related but functionally distinct tools are added, and failures include wrong function selection and wrong parameter assignment. [[evidence:ev-p084-expanded-toolkit-controlled-setting]] [[evidence:ev-p084-related-toolkit-error-types]]

Development uses all 200 items from `ibm-research/BFCL-FC-robustness@2ec93e790cf5fa3753d477a83cd596115387f1c5` together with the matching BFCL v3 questions and gold calls from `ShishirPatil/gorilla@c15b2a151662cac9839c96d7dfb1493b5329c975`. The untouched Confirmation source is fixed before Development as `BFCL_v4_live_multiple.json` and its gold-answer file from `ShishirPatil/gorilla@6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`; those bytes must not be downloaded or read before Main Codex promotion.

The outcome is whether the retriever's top-ranked function belongs to the row's ground-truth function set. For any row with multiple gold functions, this is a top-1 membership metric, not complete call-set recall or end-to-end correctness. This version does not claim argument filling, tool execution, multi-step planning, Agent task success, or large-corpus retrieval.

<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p086-required-parameter-score","ev-p086-near-identical-distribution","ev-p089-forced-alignment-proxy"]
-->
