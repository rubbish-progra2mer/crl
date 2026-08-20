# Evidence Packet

```json
{
  "candidate_sha256": "65f86fb5c8508c9353437c2d41345ed5891049f9c9b55deb5a80e5c512e97b91",
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
      "evidence_id": "ev-p079-action-conditioned-contextualization",
      "paper_id": "P079",
      "paper_title": "Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents",
      "evidence_kind": "operator",
      "section": "3.2  ALGORITHM FOR TRAINING THE CONTEXTUALIZATION MODULE",
      "page_start": 4,
      "page_end": 4,
      "locator": "P079:p0004:s0002; exact extracted span beginning 'For each observation ot in the\\ncollected traject'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P079_lcow.pdf",
      "fulltext_sha256": "2695ec5c912241fbdb56fc5f9ee3a4f60d1aaa23b511f35cff3d32908e97dead",
      "source_content": "For each observation ot in the\ncollected trajectories, we sample multiple candidate contextualized observations, and select the one\nthat best provides the relevant context for multiple LLM agents to accurately predict the next action\nat. Based on the chosen target observations, we update fθ via supervised fine-tuning.",
      "source_content_sha256": "e4f8dffd29a90d75f4514356998bef7dfc0f10a93f5c3f9f0b1ef011f06a0d98",
      "codex_note": "LCoW selects observation subsets by whether multiple agents can recover the demonstrated next action.",
      "passage_id": "P079:p0004:s0002",
      "passage_text_sha256": "ab23e1217f3a3d56fa983e0110fa35036ddc69d07192ba6f99e118a7b6be73ff",
      "quote_start": 515,
      "quote_end": 834
    },
    {
      "evidence_id": "ev-p079-unseen-ui-boundary",
      "paper_id": "P079",
      "paper_title": "Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents",
      "evidence_kind": "failure",
      "section": "REFERENCES",
      "page_start": 21,
      "page_end": 21,
      "locator": "P079:p0021:s0001; exact extracted span beginning 'Specifically, we set the 30 tasks included in “F'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P079_lcow.pdf",
      "fulltext_sha256": "2695ec5c912241fbdb56fc5f9ee3a4f60d1aaa23b511f35cff3d32908e97dead",
      "source_content": "Specifically, we set the 30 tasks included in “Filter-List” task category as unseen-category\ntasks. As shown in Table 3, LCoW fails to improve both GPT-4o and Gemini-1.5-flash agents\nin unseen-category tasks. The main reason for this failure in the unseen-category tasks is that the\ncontextualization module does not extract the necessary UI element required to dropdown the hidden\nmenu when manipulating filters in Filter-List-related tasks. Since the training tasks do not\ninvolve any UI elements related to filter functionality, the contextualization module does not learn\nany knowledge about the UI element during training, resulting in no performance improvement in\nunseen-category tasks.",
      "source_content_sha256": "517916a5a85700814f8851ea9e1fe8ead521089b44390b285eddf03397461061",
      "codex_note": "The contextualizer fails on an unseen UI category because training never exposed the needed filter affordance.",
      "passage_id": "P079:p0021:s0001",
      "passage_text_sha256": "ce89ec8ef4e99abc0353c0fe801d63e57e6589ed6ba60490898d8c28be6a4b98",
      "quote_start": 995,
      "quote_end": 1688
    }
  ]
}
```
