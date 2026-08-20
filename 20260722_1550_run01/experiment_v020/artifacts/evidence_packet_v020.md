# Evidence Packet

```json
{
  "candidate_sha256": "7c1326b3309cd0e21f52c749b38724c965821e81cf6880f20dde07678462f690",
  "evidence": [
    {
      "evidence_id": "ev-p040-failure-core",
      "paper_id": "P040",
      "paper_title": "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents",
      "evidence_kind": "failure",
      "section": "Abstract",
      "page_start": 1,
      "page_end": 1,
      "locator": "P040:p0001:s0002; exact extracted span beginning 'LLM agents can fail silently'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P040_false_success.pdf",
      "fulltext_sha256": "ab1307fdaaf97841bd09296bca225b736e8e9a712002ac123b1fab663f35ba6a",
      "source_content": "LLM agents can fail silently by asserting task\ncompletion when the environment state shows\notherwise.\nWe study this failure mode, false\nsuccess, across two agent benchmarks: 9,876\ntau2-bench trajectories from 8 model families and\n1,879 AppWorld trajectories from 4 model fam-\nilies with text-independent ground truth.",
      "source_content_sha256": "851fa888995cf4808a25a1e05894aaaaa4729a94d9343d0237bfc1b55119b532",
      "codex_note": "Environment-grounded evaluation exposes agents that claim completion despite an unmet task state.",
      "passage_id": "P040:p0001:s0002",
      "passage_text_sha256": "63e6eb5645cb4e944997f1f2c68f320773ad9cb30fc2fd9c9d0425e57c36ef63",
      "quote_start": 9,
      "quote_end": 326
    },
    {
      "evidence_id": "ev-p074-contract-state-commit",
      "paper_id": "P074",
      "paper_title": "ToolGate: Contract-Grounded and Verified Tool Execution for LLMs",
      "evidence_kind": "operator",
      "section": "§3.2 Tool Contracts",
      "page_start": 4,
      "page_end": 4,
      "locator": "P074:p0004:s0001; exact extracted span beginning 'The precondition Pt : Σ →{true, false} spec-\\nifi'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P074_toolgate.pdf",
      "fulltext_sha256": "7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d",
      "source_content": "The precondition Pt : Σ →{true, false} spec-\nifies the minimal state requirements that must be\nsatisfied for the tool to be legally callable, mean-\ning a tool is not executable unless S |= Pt holds.\nMeanwhile, the postcondition Qt : Σ × Rt →\n{true, false}. constrains the structural validity, typ-\ning correctness, and semantic consistency of the\nruntime output rt, while also defining how a veri-\nfied result updates the system state.",
      "source_content_sha256": "23348deac49dcd13e4b48ad0ea3b57e7c96b98f97c9142625ca7ac9e5ed964ac",
      "codex_note": "Preconditions gate calls and postconditions gate whether returned data enters trusted symbolic state.",
      "passage_id": "P074:p0004:s0001",
      "passage_text_sha256": "1d030336ce745d19885eb7f0bd9e85db9503b012ba737ca44cd1c9fc594a8cb6",
      "quote_start": 200,
      "quote_end": 635
    },
    {
      "evidence_id": "ev-p074-missing-schema-true-postcondition",
      "paper_id": "P074",
      "paper_title": "ToolGate: Contract-Grounded and Verified Tool Execution for LLMs",
      "evidence_kind": "failure",
      "section": "§3.2 Tool Contracts",
      "page_start": 4,
      "page_end": 4,
      "locator": "P074:p0004:s0001; exact extracted span beginning 'When the documenta-\\ntion does not provide a stru'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P074_toolgate.pdf",
      "fulltext_sha256": "7073bc0a27cf0f002ea4d1ef0ec3726d5c70c7e44a218e78f46d92284aba289d",
      "source_content": "When the documenta-\ntion does not provide a structured schema (approxi-\nmately 25% of tools in ToolBench provide only de-\nfault response_examples of the form {api_list:\n[]}), we adopt Q = True as the default postcondi-\ntion.",
      "source_content_sha256": "3965c203b86d673e3b900bb829e9d284fa73ebe247870fae03399f7272bd7cf5",
      "codex_note": "For roughly one quarter of ToolBench tools without structured response schemas, the implementation defaults the postcondition to true.",
      "passage_id": "P074:p0004:s0001",
      "passage_text_sha256": "1d030336ce745d19885eb7f0bd9e85db9503b012ba737ca44cd1c9fc594a8cb6",
      "quote_start": 1513,
      "quote_end": 1737
    }
  ]
}
```
