# Evidence Packet

```json
{
  "candidate_sha256": "eba1d5c72c2fe852d89d087db340ee06baf184d102d5fb225f7743f952626466",
  "evidence": [
    {
      "evidence_id": "ev-p010-index-retrieve-read",
      "paper_id": "P010",
      "paper_title": "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory",
      "evidence_kind": "operator",
      "section": "ABSTRACT",
      "page_start": 1,
      "page_end": 1,
      "locator": "P010:p0001:s0002; exact extracted span beginning 'breaks down the long-term memory design'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P010_longmemeval.pdf",
      "fulltext_sha256": "c6c6d75072d316d7b040dbbbb9caf7607821e6dd34d986e6f6c7e3e1721179f7",
      "source_content": "breaks down the long-term memory design\n         into three stages: indexing, retrieval, and reading.",
      "source_content_sha256": "85e956b568e2179db35ef1d822aa521c6404dd8c2ea39941a9e2fffd5e31ff8a",
      "codex_note": "LongMemEval decomposes memory into indexing, retrieval, and reading.",
      "passage_id": "P010:p0001:s0002",
      "passage_text_sha256": "6519c6d02d0fcf78ea6bf67998afcd46ba86eecbf4429101e05f71a033454dea",
      "quote_start": 992,
      "quote_end": 1093
    },
    {
      "evidence_id": "ev-p030-failure-core",
      "paper_id": "P030",
      "paper_title": "STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?",
      "evidence_kind": "failure",
      "section": "4.2  Overall Performance",
      "page_start": 7,
      "page_end": 7,
      "locator": "P030:p0007:s0002; exact extracted span beginning 'Recognition does not imply application'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P030_stale_memory.pdf",
      "fulltext_sha256": "388f71f1eb952e7d7e7b19c2f25bfc744c47efa8ee00a548093b949432495109",
      "source_content": "Recognition does not imply application. SR measures whether a model can invalidate\nan outdated belief under direct questioning; IPA tests whether the updated state is integrated into\nrealistic downstream behavior.",
      "source_content_sha256": "831ce39e31cfca79a9ffc996264b2a2b7d215defe36fa829f4ad24627049a75a",
      "codex_note": "Recognizing stale memory does not guarantee that updated state governs downstream action.",
      "passage_id": "P030:p0007:s0002",
      "passage_text_sha256": "bbd545b7ad1ea2d96a78da5095488066effdb4b205483a2980ca8d5c0ccccc2d",
      "quote_start": 571,
      "quote_end": 784
    },
    {
      "evidence_id": "ev-p011-failure-core",
      "paper_id": "P011",
      "paper_title": "On Memory Construction and Retrieval for Personalized Conversational Agents",
      "evidence_kind": "failure",
      "section": "ABSTRACT",
      "page_start": 1,
      "page_end": 1,
      "locator": "P011:p0001:s0003; exact extracted span beginning 'The granularity of memory unit matters'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P011_secom.pdf",
      "fulltext_sha256": "998ab05ece554a83870b1baf5762f314837165e99f22ef2af8ffd7ba473c5004",
      "source_content": "The granularity of memory unit matters: Turn-level, session-\n          level, and summarization-based methods each exhibit limitations in both memory\n          retrieval accuracy and the semantic quality of the retrieved content.",
      "source_content_sha256": "8eefd4f8f5c4691bff7894d500bccf2437c15e87d42ac13be4a6a4c2c4ea277d",
      "codex_note": "Memory construction granularity changes retrieval accuracy and semantic quality.",
      "passage_id": "P011:p0001:s0003",
      "passage_text_sha256": "ec6f00078b9e8e0b92690c772c0f300499e4189e52a64568b97432d55cfe43e3",
      "quote_start": 391,
      "quote_end": 620
    },
    {
      "evidence_id": "ev-p064-experience-following-error",
      "paper_id": "P064",
      "paper_title": "How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior",
      "evidence_kind": "failure",
      "section": "Introduction",
      "page_start": 2,
      "page_end": 2,
      "locator": "P064:p0002:s0001; exact extracted span beginning 'Through extensive experiments'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P064_experience_following_memory.pdf",
      "fulltext_sha256": "2c3992d238f5d6dec4ed96faae0a82e3b88edc6e37b26d8622a2b780f2160400",
      "source_content": "Through extensive experiments, we identify an\nimportant phenomenon that we term the experience-\nfollowing property: a high ‘input similarity’ be-\ntween the current task query and the one from\nthe retrieved record often yields a high ‘output\nsimilarity’ between their corresponding (output)\nexecutions. While this property enables effective\nreuse of successful experiences, we uncover two\nsignificant challenges arising from the dynamic and\nnoisy nature of agentic memory banks. First, we\nobserve the problem of error propagation: if a re-\ntrieved memory record contains noisy or incorrect\noutputs, the agent is likely to replicate and even\namplify these errors during the current task. If the\nresulting execution is then added back into mem-\nory, the error is likely to be further propagated to\nfuture tasks. Second, we recognize the issue of mis-\naligned experience replay, which limits the benefits\nof experience following—certain memory records,\nwhen retrieved as demonstrations, consistently lead\nto poor execution due to their misalignment with\nthe current task, indicating t",
      "source_content_sha256": "215bad88286c6787ba7a177499d000196f850ecee1f0443640f8669d3d042ae4",
      "codex_note": "Retrieved execution similarity can reproduce and compound incorrect stored experience.",
      "passage_id": "P064:p0002:s0001",
      "passage_text_sha256": "6425ac9ab3f6612101a9f2e15d05f3b475d270ca1a5e1f1c019f2292faa2a338",
      "quote_start": 378,
      "quote_end": 1458
    }
  ]
}
```
