# Evidence Packet

```json
{
  "candidate_sha256": "c36b4847029ea234c8db9b574a128b1d9ca01dc6d425e9fddd099ba141ad8291",
  "evidence": [
    {
      "evidence_id": "ev-p085-large-corpus-scale",
      "paper_id": "P085",
      "paper_title": "Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models",
      "evidence_kind": "evaluation",
      "section": "Related work",
      "page_start": 4,
      "page_end": 4,
      "locator": "P085:p0004:s0001; exact extracted span beginning '# size of retrieval task'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P085_toolret.pdf",
      "fulltext_sha256": "26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a",
      "source_content": "# size of retrieval task\n7,615\n- # of web API retrieval task\n4,916\n- # of code function retrieval task\n950\n- # of customized app retrieval task\n1,749\n# size of tool\n43,215\n- # of web API\n36,978\n- # of code function\n3,794\n- # of customized app\n2,443",
      "source_content_sha256": "5a981249076b3ecc08d957e58a222f41006a989c7e9971719a8c662e868f4bcf",
      "codex_note": "TOOLRET evaluates 7,615 retrieval tasks against a merged 43,215-tool corpus across Web, Code and Customized formats.",
      "passage_id": "P085:p0004:s0001",
      "passage_text_sha256": "43206fc1d861366b2881cf68a0c2a967d8a31c917c20158adfc0dcca014f5611",
      "quote_start": 235,
      "quote_end": 483
    },
    {
      "evidence_id": "ev-p085-retrieval-completeness-failure",
      "paper_id": "P085",
      "paper_title": "Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models",
      "evidence_kind": "failure",
      "section": "Related work",
      "page_start": 6,
      "page_end": 6,
      "locator": "P085:p0006:s0001; exact extracted span beginning 'Specifically, all retrievers in our experiments'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P085_toolret.pdf",
      "fulltext_sha256": "26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a",
      "source_content": "Specifically, all retrievers in our experiments\nachieve less than 35% in Completeness@10 and\nunder 52% in recall@10.",
      "source_content_sha256": "0aa43692eb3e97287c5266c66da339d86590a427c6106d9fea3064544212e715",
      "codex_note": "The reported query-only systems recover complete target-tool sets poorly even at top 10.",
      "passage_id": "P085:p0006:s0001",
      "passage_text_sha256": "ad8eebc311387718fb1c5b60ff4364b20d7ddba74cd566e2d2e7d35952913865",
      "quote_start": 3936,
      "quote_end": 4052
    },
    {
      "evidence_id": "ev-p085-non-exhaustive-label",
      "paper_id": "P085",
      "paper_title": "Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models",
      "evidence_kind": "failure",
      "section": "Discussion",
      "page_start": 8,
      "page_end": 8,
      "locator": "P085:p0008:s0002; exact extracted span beginning 'The one-to-many problem arises because'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P085_toolret.pdf",
      "fulltext_sha256": "26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a",
      "source_content": "The one-to-many problem arises because our dataset com-\nbines multiple existing datasets. For example, for a query from\ndataset A, the ground truth may not be limited to the single\nannotation provided in A. Similar tools in dataset B might also\nprovide valid solutions to the same query.",
      "source_content_sha256": "037746d05afee33a77a59295bd99149ec40e916bbfe9d0c11c1528dcf436ca8f",
      "codex_note": "Merged-source labels are non-exhaustive, so an unlabelled but usable alternative can be counted as a retrieval false negative.",
      "passage_id": "P085:p0008:s0002",
      "passage_text_sha256": "4b347542b88d5ed316403afdf9edf8b0a891f65f4fee9e7ae43c108dae1f2aff",
      "quote_start": 564,
      "quote_end": 851
    }
  ]
}
```
