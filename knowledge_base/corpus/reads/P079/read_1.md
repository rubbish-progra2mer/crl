# P079 first read — action-preserving contextualization of web observations

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Learning to Contextualize Web Pages for Enhanced Decision Making by LLM Agents
- Authors: Dongjun Lee, Juyong Lee, Kyuyoung Kim, Jihoon Tack, Jinwoo Shin, Yee Whye Teh, Kimin Lee
- Venue: ICLR 2025
- PDF: `knowledge_base/staging/plan05_sat_a3/P079_lcow.pdf`
- PDF SHA-256: `2695ec5c912241fbdb56fc5f9ee3a4f60d1aaa23b511f35cff3d32908e97dead`
- Parse check: 35 physical pages

## Changed computation

LCoW inserts a learned contextualization model between the raw accessibility-tree observation and the decision model. The module transforms a page into an action-relevant representation, and is trained by whether downstream agents can recover the demonstrated next action. This is a learned decision-preserving observation transformation, not generic summarization or compression.

## Evidence and closest lineage

- Training begins from successful trajectories, samples several contextualizations, and asks multiple LLM agents to predict the demonstrated next action from each transformed observation.
- Action match selects the contextualization target; if every sample fails, a retry explicitly exposes the ground-truth action as a hint. The contextualizer is then supervised-fine-tuned and the procedure iterates.
- WebShop, WorkArena, and WebArena experiments use text/accessibility-tree observations. Reported gains transfer to several decision LLMs, including models not used to train the contextualizer.
- A behavior-cloning comparison uses the same 264 demonstrations, helping separate observation transformation from directly training the action policy.

## Measurement and fairness boundaries

- Training uses successful demonstrations, ground-truth next actions, multiple strong proprietary LLMs, and an explicit oracle hint on retry. It is not an oracle-free training mechanism.
- A separate contextualization call adds latency, tokens, and model cost; the paper does not present a fully matched total-compute comparison.
- Generalization is strongest within familiar UI types. On an unseen-category filter setting the contextualizer fails to extract the novel element and success stays at zero.
- The method assumes access to successful trajectories and is bottlenecked when moving to genuinely new task families.
- CRL retains only the text/interface mechanism; no visual-GUI claim is extracted.

## Draft knowledge objects

### Operator draft: `Action-Preserving Observation Contextualization`

Learn a separate observation transform by selecting representations that allow downstream agents to recover the correct next action, then keep the decision policy modular and unchanged.

### Failure draft: `Raw Interface Observations Hide Action-Relevant Structure`

Long accessibility trees can bury the element and relationship needed for the next decision; generic summarization can also discard it because its objective is not action preservation.

## Draft Evidence locators

- pp.1–5: decoupled contextualizer and decision model.
- pp.6–11: iterative selection, action-match reward, oracle retry, and training details.
- pp.12–18: WorkArena/WebShop/WebArena results and transfer.
- pp.19–25 and appendices: comparisons, unseen-UI failure, prompts, data and cost boundaries.

All claims remain draft until independent read and reconciliation.
