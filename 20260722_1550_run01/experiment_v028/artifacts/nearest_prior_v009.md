# Main Codex Nearest Prior Record

## Search Boundary

The Main Codex performed four neutral OpenAlex searches on 2026-07-23: `query value required parameter schema tool retrieval`, `type constrained partial bipartite matching function calling`, `user query schema parameter matching tool selection`, and `Hungarian alignment function calling tool retrieval`. Their first five results did not surface a direct function-calling composition; the output was dominated by generic schema matching and unrelated bipartite work. This is a search result, not proof of absence.

A Semantic Scholar search for `tool retrieval parameter schema function calling` surfaced DTDR, Meta-Tool, Self-Guided Function Calling, ToolRegistry, NaviAgent, and ToolSpec among the first eight results. Two follow-up Semantic Scholar queries returned HTTP 429 and are recorded as incomplete coverage. GitHub repository searches for three neutral or title-based combinations returned zero repositories. Direct repository checks found `qinshengqian/Meta-Tool@3430cd70626033be3c2486da966d31d6ccb14b1e`, whose recursive tree contains only `README.md`, while the ToolDreamer paper's `https://github.com/boschresearch/ToolDreamer` link returned HTTP 404. These repository results do not prove that no other implementation exists.

## Closest Components

Meta-Tool (P086, PDF SHA-256 `02064499a8345eb333e4fdd71abaa5ee69133af5be7b81626ba09816f48d194b`) is the closest parameter-level retrieval component. It generates a desired tool and desired required-parameter descriptions, then independently takes the best real required-parameter match for each desired parameter. Its public README specifies a Meta-Llama-3.1-8B base model, a LoRA, and multilingual-e5-large; the fixed repository tree does not expose the stated evaluation scripts. An exact full Meta-Tool run would therefore add a generative model, learned LoRA, different embeddings, and unavailable code, so it is not a fair executable comparator for the present deterministic query-span delta.

ToolDreamer (P089, PDF SHA-256 `d13b84ab7c2a66069f8d160ab78dfb3e7efd5dabab06c219995c5f92b2093918`) is the closest alignment component. It uses Hungarian matching between generated hypothetical and gold tools, but its square assignment forces a match and is acknowledged as an imperfect training proxy. TPPA cannot claim Hungarian matching or one-to-one capacity as inventions.

## Closest Full Pipeline

`Dynamic Tool Dependency Retrieval for Lightweight Function Calling`, DOI `10.18653/v1/2026.findings-acl.1680`, was read from the original 24-page PDF at `sources_v008/DTDR_2026_findings_acl_1680.pdf`, SHA-256 `099f012ad01bd8b24154093c2bfe55ad9eabdb668ddc7ecf0c2735e01d89a833`. Physical pages 1-2 define retrieval conditioned on the user query and evolving tool plan. Physical pages 4-5 define DTDR-C and DTDR-L from demonstration trajectories and full tool history. DTDR is a strong retrieval-to-function-selection neighbor, but it does not align observable query values to required schema parameters in a fixed single-step menu.

## Comparator And Claim Boundary

The primary comparator is the identical frozen cross-encoder without TPPA. The closest executable component comparator reuses TPPA's exact spans, edge features, selected global tuple, and fusion weight, but relaxes one-to-one capacity by independently choosing each span's best parameter. It tests the added capacity/null computation without pretending to reproduce Meta-Tool's generator or ToolDreamer's training pipeline.

The possible contribution is limited to the combined inference-time computation: deterministic observable query spans, coarse type compatibility, capacity-one partial alignment, explicit null rejection, and fusion with a fixed cross-encoder. It is not a claim to invent schema matching, embedding similarity, Hungarian assignment, null matching, or tool retrieval. Reviewer 1 must reject Delivery if a closer exact composition is found or if this combination is not a sufficient method contribution.
