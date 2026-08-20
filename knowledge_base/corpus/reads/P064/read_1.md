# P064 first read — experience-following and memory error propagation

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior
- Authors: Zidi Xiong et al.
- Venue: ACL 2026 long paper
- PDF: `knowledge_base/staging/plan05_sat_a1/P064_experience_following_memory.pdf`
- PDF SHA-256: `2c3992d238f5d6dec4ed96faae0a82e3b88edc6e37b26d8622a2b780f2160400`
- Parse check: 23 physical pages

## Changed computation studied

This is primarily negative/mechanistic evidence rather than a general new CRL operator. It studies episodic-memory addition and deletion across four agents and measures “experience following”: input-similar retrieved demonstrations induce output-similar executions. Controlled variants compare fixed memory, add-all, increasingly capable automatic evaluators and a ground-truth-simulated strict evaluator; history-based deletion uses downstream utility observed whenever a memory is retrieved.

## Evidence and closest lineage

Add-all underperforms fixed memory across all four reported agents, while strict selective addition is best. Error-free replacement of stored outputs improves running performance, directly supporting error propagation. History-based deletion can improve performance with a reliable evaluator but is unstable with coarse evaluators. The paper also identifies “misaligned experience replay”: an execution can pass its original evaluator yet harm later tasks as a demonstration.

## Measurement and scope boundaries

- The strict evaluator is simulated by ground-truth comparison and is an oracle, not a deployable component.
- Benefits of addition/deletion depend strongly on evaluator quality; vanilla LLM judges can be worse than fixed memory.
- The study intentionally excludes structural transformation, summarization and reflection, so findings should not be generalized without checks.
- Three real-agent domains include healthcare, driving and IoT, partly outside CRL's application scope; their value here is the cross-domain negative mechanism.
- The user excludes environment-feedback learning/recovery from core directions. Accordingly, this source contributes Failure knowledge only; its evaluator-driven deletion is not promoted as a core Operator.

## Draft knowledge object

### Failure draft: `Experience-Following Propagates Stored Execution Error`

Similarity-based episodic retrieval encourages the agent to imitate stored outputs. If inaccurate or task-misaligned executions enter memory, later executions repeat/amplify them and may be re-added, while deletion guided by a noisy evaluator can make performance worse.

## Draft Evidence locators

- pp.1–5: experience-following definition, four-agent setup, add-all/strict results and error-free comparison.
- pp.6–8: utility-history deletion, evaluator-dependent regressions and misaligned replay.
- p.9: distribution/capacity results and explicit limitations.

All claims remain draft until independent read and reconciliation.
