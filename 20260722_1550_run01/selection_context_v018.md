# Neutral Selection Context

## Version scope

v018 began after v017 closed two direct-prior collisions before Candidate freeze. It was required to avoid P084 reranking/document rewriting and hidden-state tool-necessity or utility controllers, while retaining a fresh prospective Confirmation path.

## Routes checked

### Generic argument provenance and pre-execution grounding

The proposed boundary was to reject a function call when an argument value lacked traceable support in the user request or schema. This collided with direct current work before implementation:

- SAAG decomposes agent-call assessment into registry conformance, structural completeness, and argument grounding, then uses stage-specific feedback for repair.
- PACT tracks argument-level provenance with role-specific trust contracts across replanning steps.
- ProvenanceGuard treats action support by traceable context evidence as a pre-execution alignment gate.

The frozen `sources_v018/saag_2607.18245.pdf` confirms the argument-grounding and structured-feedback computation. A literal/evidence-span variant would not provide a distinct research contribution.

### Multilingual schema-domain projection

`Lost in Execution` establishes a narrower failure: semantically appropriate argument values are emitted in the query language although the execution interface requires English surface forms. Its existing comparators are explicit prompting, pre-translation, and post-translation. A schema-domain projection restricted to declared enum/canonical values remained computationally distinct from unrestricted post-translation.

The carrier could not be fixed, however. The paper's only code/data URL, `https://anonymous.4open.science/r/multilingual_robustness_tool_calling-CA44`, returned HTTP 200 for the static application shell, while its repository API returned HTTP 401 for the same public slug. No MLCL data bytes were acquired. Recreating Chinese, Hindi, and Igbo examples by machine translation would discard the paper's human semantic verification and would not be a valid substitute for the real benchmark.

### Constraint-faithful planning formalization

The proposed computation was a structural delta gate over constrained versus unconstrained formal specifications. Primary-source and repository inspection showed:

- CoPE already includes an `Edit` method that first generates unconstrained PDDL and then modifies it for the constraint, plus up to three syntax revisions.
- `NL-PDDL-Bench` already uses planner/validator diagnostics for localized edits and evaluates specification similarity and plan-level consistency.
- The fixed CoPE repository at commit `e13535ebbc581c8a7ad824ee741701cc33669695` contains 4,292 data files (4,325,701 bytes) but no paper `output/` directory or frozen model generations.
- The authoritative shared environment has `transformers` and `torch`, but not Kani, VAL, TCORE, Z3, Spot, or a PDDL library. The repository explicitly requires those external components or model APIs.

Writing a temporary PDDL platform, changing the shared lock, or manufacturing omitted-constraint fixtures would expand the task or violate the real-experiment boundary. This route therefore had no fair runnable candidate pool.

### Incomplete contract semantics

P074 ToolGate uses `Q=True` for tools without response schemas, creating a genuine unknown-versus-verified boundary. Changing that fallback to a three-valued result is a necessary correction, but not by itself a new method. `Partial Contracts Suffice` makes soundness depend on returning an unprovable result rather than a false proof, and `Contract2Tool` directly infers missing preconditions/effects from metadata, documentation, schemas, and execution traces. A simple fail-closed rename did not survive novelty screening.

### Memory-poisoning anomaly detection

ASB records high false-negative rates for an LLM memory detector, but 2026 work already evaluates stateful runtime controllers, behavioral firewalls, and provenance-aware guards on ASB or adjacent agent-security suites. A generic text anomaly classifier would be weaker than those direct comparators and was not promoted.

## Data exposure and prospective boundaries

- The CoPE repository and all of its dataset bytes were acquired during selection. They cannot serve as untouched Confirmation in a later version.
- The MLCL repository data were not acquired because the repository API denied access.
- No model weights, inference outputs, ToolGate runtime traces, ASB attack instances, or benchmark Confirmation bytes were acquired.
- No empirical method outcome was observed in v018.

## Disposition

v018 closes at selection. No Candidate claim, implementation, Evidence Packet, Experiment Plan, Development, Confirmation, Review Packet, Reviewer, Decision, or Delivery was created.

