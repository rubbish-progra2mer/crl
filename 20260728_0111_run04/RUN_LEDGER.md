# RUN_LEDGER

- EVENT: RUN_CREATED
  AT: 2026-07-28T01:11:37+08:00
  MODE: COMMISSIONING
  VERSION: v001

- EVENT: CHARTER_PAID_API_PREAUTH_RECORDED
  AT: 2026-07-28T01:12:44.9112525+08:00
  VERSION: v001
  ARTIFACT: RUN_CHARTER.md
  SHA256: 89c47f1f4e1666ec75413078e257e8c9269a04822a657da06060e85351a8ed44
  BASIS: CRL.md DeepSeek standing preauthorization dated 2026-07-27

- EVENT: PROBLEM_COMMITTED
  AT: 2026-07-28T01:18:40.4437313+08:00
  VERSION: v001
  ARTIFACT: problem_v001.md
  SHA256: d9f814f3896c7cf6732acd5487c202e5b102b2ad8c5a3aaa34884b3d0bebe5ec
  NOTE: Occupancy scan killed the initially explored multi-tool retrieval node before Problem commitment; v001 targets pre-execution constraint-sensitive validation of adapted cached plans.

- EVENT: PROBLEM_LEVEL_KERNEL_KILL_AND_VERSION_ADVANCE
  AT: 2026-07-28T01:29:25.5443435+08:00
  VERSION: v001
  ARTIFACT: research_map_v001.md
  SHA256: 8900678d4a2f888dabbaec824a58c950b3149bdd9c62e0b3e1b988b5609237fa
  DISPOSITION: No Candidate formed. Under fair information access, the counterfactual response gate is dominated by direct static checking when the constraint-to-plan mapping is known, and is not semantically decidable when that mapping is unknown.
  NEXT_VERSION: v002

- EVENT: PROBLEM_COMMITTED
  AT: 2026-07-28T01:34:48.5898242+08:00
  VERSION: v002
  ARTIFACT: problem_v002.md
  SHA256: 4269ed04ff40f6c9f9a628044a9c814f63c1be2d86961a77446999c40601003e
  NOTE: v002 targets post-failure epistemic-state-conditioned tool visibility, with transaction systems, authorization gates, and static dynamic-menu systems reserved as nearest comparators.

- EVENT: WORKBENCH_EXECUTION_ONLY_FAILURE_RETAINED
  AT: 2026-07-28T01:42:47.5609704+08:00
  VERSION: v002
  ARTIFACT: workbench_v002/result.json
  SHA256: 8fb7f4688ad04e63d07541046ccd1c2afd6e2538b783b5d1fde1507d8dbc5b76
  EXECUTION_ONLY_CORRECTION: The simulator emitted a tool-role message without tool_call_id on second-step episodes, producing HTTP 400. Successful subsets are not used scientifically.

- EVENT: PROBLEM_LEVEL_KERNEL_KILL_AND_VERSION_ADVANCE
  AT: 2026-07-28T01:42:47.5609704+08:00
  VERSION: v002
  ARTIFACT: research_map_v002.md
  SHA256: 7bcca55c60b8a23bd3520f401f28482a08fd488e6baf9b2d9078c8c60c0c2a42
  SUPPORTING_WORKBENCH: workbench_v002_retry01/result.json
  SUPPORTING_WORKBENCH_SHA256: 59fc1d9ce5bce123fa5720850103fdd4551ec2a98f24e17b6a2d188ed0330ab8
  DISPOSITION: No Candidate formed. Full-menu baselines already had zero unsafe retries and 11/12 task success; dynamic menus added one exploratory success but no safety correction.
  NEXT_VERSION: v003

- EVENT: PROBLEM_COMMITTED
  AT: 2026-07-28T01:43:54.2870953+08:00
  VERSION: v003
  ARTIFACT: problem_v003.md
  SHA256: 1a5d2154cdb7aeb838b6668a1467936c042b80878f58c5e00374066f39312913
  NOTE: v003 tests whether nuisance-order disagreement from a cheap black-box tool selector can route only risky queries to a stronger model and improve the execution-success/cost frontier.

- EVENT: PROBLEM_LEVEL_KERNEL_KILL_AND_VERSION_ADVANCE
  AT: 2026-07-28T01:49:19.8477991+08:00
  VERSION: v003
  ARTIFACT: research_map_v003.md
  SHA256: 2f0e785874bd4f1d4d446b1e66fc78cdd0a676ee6aa48657aa40c2ac2fefb7a3
  SUPPORTING_WORKBENCH: workbench_v003/result.json
  SUPPORTING_WORKBENCH_SHA256: 34455f1e0ede6761db3c86d78a46710cf3fbfab609ce50d8d330bd8d20916390
  DISPOSITION: No Candidate formed. Cheap-model forward/reverse order disagreement was 0/21; its sole error was in the agreement set and the stronger model did not repair it.
  NEXT_VERSION: v004

- EVENT: API_SPEND_ESTIMATE_RECORDED
  AT: 2026-07-28T01:50:08.4070996+08:00
  VERSION: v004
  PROVIDER: deepseek
  USAGE: deepseek-v4-flash 134 successful responses, 10112 cache-hit input tokens, 27815 cache-miss input tokens, 20864 output tokens; deepseek-v4-pro 21 successful responses, 1920 cache-hit input tokens, 6712 cache-miss input tokens, 2138 output tokens.
  PRICING_SOURCE: https://api-docs.deepseek.com/quick_start/pricing/
  ESTIMATED_SPEND_USD: 0.01455
  NOTE: Estimate uses the official 2026-07-28 per-million-token prices; failed requests without usage records are excluded. This is far below the 20 USD per-step and 50 USD per-Run ceilings.
