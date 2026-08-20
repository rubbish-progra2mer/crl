# Evidence Packet

```json
{
  "candidate_sha256": "50ad937e5aa6df51e76223ef002a675273902a59d71170082d05c222db61fff5",
  "evidence": [
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
    },
    {
      "evidence_id": "ev-p080-fixed-depth-under-over-search",
      "paper_id": "P080",
      "paper_title": "AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning",
      "evidence_kind": "failure",
      "section": "Related Work",
      "page_start": 3,
      "page_end": 3,
      "locator": "P080:p0003:s0001; exact extracted span beginning 'As shown in Fig.2(a), NQ reaches\\nnear-optimal pe'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P080_autosearch.pdf",
      "fulltext_sha256": "ab078ee4e0221166d92ea3856d028f92a9348899f8fa9d63ec8841764edd8a86",
      "source_content": "As shown in Fig.2(a), NQ reaches\nnear-optimal performance with a single search step,\nwhile additional steps provide little benefit. In con-\ntrast, Bamboogle requires up to three steps to peak,\nafter which further searches reduce performance.\nFig. 2(b) further shows that exceeding the near-\noptimal depth leads to a notable increase in the over-\nsearching ratio for both datasets, with the effect\nbeing more pronounced on the more complex Ban-\nboogle dataset. These results indicate that the ap-\npropriate search depth is task-dependent, with a\nminimal sufficient depth achieves near-optimal\naccuracy while mitigating over-searching.\n3.2\nWhat Affects Appropriate Search Depth?\nDifferent LLMs exhibit varying reasoning and re-\ntrieval capabilities, which in turn affect their answer\naccuracy in agentic RAG systems. This raises a\nnatural question: does the agent’s capability also\ninfluence the appropriate search depth? To inves-\ntigate this, we conduct controlled experiments on\nthe Bamboogle dataset using Qwen-3B, Qwen-7B,\nand Qwen-14B models, each performing a range\nof search steps to answer the same set of questions.\nAs shown in Fig. 2(c), the 3B model steadily im-\nproves with increasing search depth, achieving its\npeak performance at the final search step within\nthe evaluated range. In contrast, the 7B and 14B\nmodels reach their optimal performance at the sec-\nond and third search steps, respectively, after which\nadditional searches lead to performance degrada-\ntion. Fig. 2(d) further shows that over-searching\nbecomes increasingly pronounced as search depth\ngrows, with stronger models exhibiting more pro-\nnounced degradation. Taken together, these results\nfrom the previous and current subsections indicate\nthat the minimal sufficient search depth, which\nbalances accuracy and efficiency, is jointly deter-\nmined by question complexity and the agent’s\ncapability.",
      "source_content_sha256": "fc82122d863f271ca54714a42b2e0a8d79be623f962270396fd7774e3c2605f7",
      "codex_note": "Fixed depth under-searches some tasks and over-searches others; the appropriate depth depends on task and model capability.",
      "passage_id": "P080:p0003:s0001",
      "passage_text_sha256": "3afc67bb25fc0ef06c494902b1823bf57c956fc861bb2ddc38426e6833daf6fa",
      "quote_start": 1230,
      "quote_end": 3111
    },
    {
      "evidence_id": "ev-p080-gold-supervised-minimal-depth",
      "paper_id": "P080",
      "paper_title": "AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning",
      "evidence_kind": "operator",
      "section": "Related Work",
      "page_start": 5,
      "page_end": 5,
      "locator": "P080:p0005:s0001; exact extracted span beginning 'Us-\\ning the sequence of intermediate answers, we'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P080_autosearch.pdf",
      "fulltext_sha256": "ab078ee4e0221166d92ea3856d028f92a9348899f8fa9d63ec8841764edd8a86",
      "source_content": "Us-\ning the sequence of intermediate answers, we\nidentify the capability-aware optimal search depth\ntc. Specifically, tc is defined as the earliest step\nat which the intermediate answer ainter\ni,t\nexactly\nmatches the ground-truth answer agold:\n\b\nt | EM(ainter\n.\n(6)\ntc = min\ni,t , agold) = 1\nIf the agent fails to answer correctly, we set tc =\n−1. This depth represents the minimal retrieval\nsteps required for the agent to answer the question\ncorrectly, reflecting its capability for the given task.",
      "source_content_sha256": "88879db3a14b22584bcf2871970a0b61cc7f735eaa6488b94d8765eb8b470d80",
      "codex_note": "Training labels the earliest correct intermediate answer against gold as the capability-aware depth.",
      "passage_id": "P080:p0005:s0001",
      "passage_text_sha256": "54adc39ce2ed3d1d168a1849154ef8afbaabc66bb2a10229363a9f8b921e8bc4",
      "quote_start": 923,
      "quote_end": 1423
    }
  ]
}
```
