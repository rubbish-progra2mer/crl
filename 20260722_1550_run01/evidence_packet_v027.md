# Evidence Packet

```json
{
  "candidate_sha256": "249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3",
  "evidence": [
    {
      "evidence_id": "ev-p084-expanded-toolkit-controlled-setting",
      "paper_id": "P084",
      "paper_title": "On the Robustness of Agentic Function Calling",
      "evidence_kind": "evaluation",
      "section": "Agentic FC Robustness Evaluation",
      "page_start": 4,
      "page_end": 4,
      "locator": "P084:p0004:s0001; exact extracted span beginning 'expanded toolkit is 5.6 compared to the 2.7'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P084_function_calling_robustness.pdf",
      "fulltext_sha256": "8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7",
      "source_content": "expanded toolkit is 5.6 compared to the 2.7 (seem-\ningly unrelated) tools in the original BFCL dataset,\nmeaning that three semantically-related functions\nwere added on average to each one of the 200 test-\ncases. Next, we evaluate the FC performance of\nmultiple agents using the generated benchmark.\n3\nAgentic FC Robustness Evaluation\n3.1\nExperimental Setup\nModels\nWe evaluate several top-performing\nLLMs from the BFCL leaderboard, both API-\naccessible and locally hosted, as FC agents. Closed\nmodels include GPT4o-mini and o1-mini,4 as well\nas Claude-3.5-Haiku and Claude-3.5-Sonnet.5 Lo-\ncally hosted models include Llama3.1-70B and\nits more advanced version Llama3.3-70B (Dubey\net al., 2024), Granite3.1-8B-instruct (Granite Team,\n2024), DeepSeek-v2.5 (DeepSeek-AI, 2024), and\nQwen2.5-72B (Qwen Team, 2024).\nEvaluation Approach\nBFCL employ a two-\nphase FC evaluation approach: (1) assessment of\nthe generated tool call through the tree-matching\nabstract syntax tree (AST) methodology, and (2)\nevaluation of the tool execution in a simulated en-\nvironment (Patil et al., 2023). Our focus in this\nstudy is the evaluation of FC construction provided\ninterventions in its input; we, therefore, adhere to\nthe first evaluation phase – namely, AST. A robust\nagent will generate correct function call regardless\nof the precise request wording and of its toolkit size:\n\"thin\" (as it comes with the original benchmark),\nor expanded, simulating a shortlister selection.\n3.2\nExperimental Results\nWe report AST averaged over the 200 dataset ex-\namples, including three variants: (a) the original\nversion, (b) original (\"thin\") toolkit + rephrased\nuser request, (c) expanded toolkit + original user\nrequest. Table 2 (left) reports the results.",
      "source_content_sha256": "ef529a2bfa93c286fc5c553150583882ca1fa7cc2bbc472e1817c5d2c9a22142",
      "codex_note": "The source compares the original request with thin versus expanded related-function toolkits over 200 cases and evaluates AST construction only.",
      "passage_id": "P084:p0004:s0001",
      "passage_text_sha256": "24569f556e418bb8f8655f657948e872f459ea3236a2e128704a8d14b86b74c2",
      "quote_start": 0,
      "quote_end": 1731
    },
    {
      "evidence_id": "ev-p084-related-toolkit-error-types",
      "paper_id": "P084",
      "paper_title": "On the Robustness of Agentic Function Calling",
      "evidence_kind": "failure",
      "section": "Agentic FC Robustness Evaluation",
      "page_start": 4,
      "page_end": 4,
      "locator": "P084:p0004:s0001; exact extracted span beginning 'Agents’ Sensitivity to Toolkit Expansion'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P084_function_calling_robustness.pdf",
      "fulltext_sha256": "8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7",
      "source_content": "Agents’ Sensitivity to Toolkit Expansion\nEv-\nidently, expanding an agent’s toolkit with a set\nof related functions caused performance degra-\ndation across the board (Table 2, left).\nHere,\nobjective agent failures span a range of error\ntypes: wrong function selected, wrong number\nof functions generated (typically two instead of\none), wrong parameter assignment to a correctly-\nselected function, parameter hallucinations, etc.\nAs an example, in response to the request \"What\nis the ranking of Manchester United in Premier\nLeague?\", an agent with the expanded toolkit\nproduces football_league.ranking(\"premier\nleague\"), retrieving the complete ranking ta-\nble of the league, instead of the more appro-\npriate sports_ranking(\"Manchester United\",\n\"premier league\"), answering the query.\nTable 2 (right) presents error breakdown for\nagents in this study in the expanded toolkit sce-\nnario, showing the proportion of each error type\nwithin the set of failures stemming from toolkit\nexpansion. While no clear pattern dominates, it\nis evident that agents struggle with both accurate\nfunction selection and parameter assignment.",
      "source_content_sha256": "a5b7de37609c028ac0d2e1f2316980cf05086d3dc5af1de8621cd33d618c07ab",
      "codex_note": "Related-function expansion degrades AST construction and produces wrong function, function-count and parameter-assignment errors; category-specific baseline increases are not reported.",
      "passage_id": "P084:p0004:s0001",
      "passage_text_sha256": "24569f556e418bb8f8655f657948e872f459ea3236a2e128704a8d14b86b74c2",
      "quote_start": 3543,
      "quote_end": 4664
    },
    {
      "evidence_id": "ev-p087-structured-query-independent-expansion",
      "paper_id": "P087",
      "paper_title": "Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval",
      "evidence_kind": "operator",
      "section": "2.2  PROCESS OF TOOL DOCUMENT EXPANSION",
      "page_start": 3,
      "page_end": 3,
      "locator": "P087:p0003:s0003; exact extracted span beginning 'Step 1: Expansion.'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P087_tool_document_expansion.pdf",
      "fulltext_sha256": "0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff",
      "source_content": "Step 1: Expansion.  We use Qwen3-32B, a model with strong instruction-following capabil-\nity, to expand raw tool documents into structured profiles.  During generation, we enable its\nreasoning mode to improve the quality and consistency of outputs.  Given the original docu-\nmentation doriginal as input, the model produces an expanded profile dprofile containing the fields\nfunction description, tags, when to use, limitations, and example usage.\nAmong them, function description and tags are always required, while the other three\nfields are generated only if explicitly supported by the documentation. The expansion is query-\nindependent and strictly grounded in the tool doc, with unsupported fields omitted.",
      "source_content_sha256": "f98396336f94ae9d30f2e0c23f02f8d880739e4a1b413fcb41bbc8ff7294e45f",
      "codex_note": "TOOL-DE generates a query-independent structured profile from each original tool document, with optional fields conditioned on source support.",
      "passage_id": "P087:p0003:s0003",
      "passage_text_sha256": "807b72b7fe46746389ef3cdbc254410ab616e282aaeae56050495da509f052a6",
      "quote_start": 527,
      "quote_end": 1239
    },
    {
      "evidence_id": "ev-p087-fields-not-universally-beneficial",
      "paper_id": "P087",
      "paper_title": "Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval",
      "evidence_kind": "failure",
      "section": "4.1  IMPACT OF GENERATED FIELDS ON TOOL RETRIEVAL",
      "page_start": 8,
      "page_end": 8,
      "locator": "P087:p0008:s0001; exact extracted span beginning 'Two consistent observations emerge.'",
      "fulltext_path": "D:\\Desktop\\crl\\crl_agent_v3\\knowledge_base\\papers\\P087_tool_document_expansion.pdf",
      "fulltext_sha256": "0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff",
      "source_content": "Two consistent observations emerge.  First, full expan-\nsion is not uniformly optimal: removing example usage in the One-out protocol yields higher\nN@10 than keeping it.  Second, example usage provides the smallest (often negative) gains\nin Add-one.  In contrast, function description and tags are neutral-to-positive under\nAdd-one, and their removal produces noticeable drops in One-out. Guided by these findings, we\nexclude example usage from the expanded profiles and retain function description,\nwhen to use, limitations, and tags for retrieval.",
      "source_content_sha256": "0c93f1f34ea495a90e3a100780f1e5a25e18276191805f6d5418a4b1591b9390",
      "codex_note": "Document expansion is field-sensitive; adding more generated text is not uniformly beneficial, and example usage is removed after negative/weak ablations.",
      "passage_id": "P087:p0008:s0001",
      "passage_text_sha256": "5bbb5b5532bb3ee1b2437e1f00c82a587f6db05222e3102fdf6d1a7146167d32",
      "quote_start": 630,
      "quote_end": 1179
    }
  ]
}
```
