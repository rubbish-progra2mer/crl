# Evidence Packet

```json
{
  "candidate_sha256": "31df88dfa09b6b5b214236f0a364bbaf7f3a417b96af1ce0aee5c9219f0de845",
  "evidence": [
    {
      "evidence_id": "ev-p039-failure-core",
      "paper_id": "P039",
      "paper_title": "ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents",
      "evidence_kind": "failure",
      "section": "3.2. Failure Mode Taxonomy",
      "page_start": 3,
      "page_end": 3,
      "locator": "P039:p0003:s0002; exact extracted span beginning 'tool skipping'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P039_toolfailbench.pdf",
      "fulltext_sha256": "6588af66fd477d9764c20c52c2adb7d92fcbf6a788fe09713bc71916862d3009",
      "source_content": "tool skipping,\nresult ignoring, fabrication, and unnecessary tool use.\nFor tool-required tasks, a response is Correct if the model\ncalls the expected tool and uses the returned data in its final\nanswer.",
      "source_content_sha256": "38661525c6f986778dffded9a617bf2bbf7a1bf4d7ae744c2a7330aa009ed69f",
      "codex_note": "Tool-use diagnostics must separate skipping, result ignoring, fabrication, and unnecessary calls.",
      "passage_id": "P039:p0003:s0002",
      "passage_text_sha256": "349e501d5f275d1fe3a6b83e39e349de991566747d1002309fc58b7b191e3f30",
      "quote_start": 431,
      "quote_end": 633
    },
    {
      "evidence_id": "ev-p039-aggregate-score-masking",
      "paper_id": "P039",
      "paper_title": "ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents",
      "evidence_kind": "failure",
      "section": "Abstract",
      "page_start": 1,
      "page_end": 1,
      "locator": "P039:p0001:s0002; exact extracted span beginning 'aggregate benchmark scores often'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P039_toolfailbench.pdf",
      "fulltext_sha256": "6588af66fd477d9764c20c52c2adb7d92fcbf6a788fe09713bc71916862d3009",
      "source_content": "aggregate benchmark scores often\nhide where tool use fails. A model that never\ncalls a needed tool and a model that calls the tool\nbut ignores the result can look similar under fi-\nnal task accuracy.",
      "source_content_sha256": "00e0d573c1c12352aa3454c4fffbb8cec7a2cdbc6e836afac419abb7dc79cff4",
      "codex_note": "Aggregate task accuracy can make tool skipping and result ignoring look alike.",
      "passage_id": "P039:p0001:s0002",
      "passage_text_sha256": "ac1cfb90fa47e7ca1b156cc07d45debb74cc9916ff37dad6071027a9c54ba804",
      "quote_start": 70,
      "quote_end": 269
    }
  ]
}
```
