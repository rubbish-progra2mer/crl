"""Student and teacher prompts for search-control preference learning."""

from __future__ import annotations

import json
from typing import Any, Dict

from schema import Brief, SearchState


SEARCH_POLICY_SYSTEM = """You control an iterative search process. At each decision point, produce exactly one continuation using this three-line format:
[Thought]: <decision rationale>
[Action]: <Continue|Reroute|Answer>
[Parameter]: <query or answer>

Use Continue to retrieve missing information along the current valid direction, Reroute to restore the original target or constraints when the direction is misaligned, and Answer only when the current evidence is sufficient.

For Continue or Reroute, Parameter must be a focused retrieval query. For Answer, Parameter must be a concise final answer.

Output only the three tagged lines."""


BRIEF_SYSTEM = """Summarize the decision-time search state. Use only the question, search history, and evidence provided at this state. Do not use future actions, future observations, or a gold answer.

Return JSON only with exactly these five fields:
{
"Original Search Target": "<target asked for by the question>",
"Key Constraints": "<constraints the answer must satisfy>",
"Confirmed Evidence": "<question-relevant facts supported by the current evidence>",
"Missing Information": "<information still needed, or None>",
"Drift Status": "<aligned|at risk|drifted>: <short reason>"
}

Evidence sufficiency must be represented through Confirmed Evidence and Missing Information. Drift Status should describe only whether the current search direction remains anchored to the original target.

Do not restate the full question or copy entire evidence passages. Do not add fields or instructions."""


DIAGNOSIS_SYSTEM = """Assess one student search-control decision using only its decision-time state, search-state brief, and student continuation.

Determine whether the complete student continuation contains a specific local error and whether the state supports a reliable local contrast. Select an auxiliary construction tag when an appropriate construction route is available.

Tag meanings:

- evidence_completion: The search remains aligned, but unresolved evidence still needs to be acquired.
- target_maintenance: The search is at risk of drifting or has drifted from the Original Search Target or Key Constraints.
- answerability: The currently available evidence supports the answer and no material information remains missing.
- not_selected: No pair-construction route is authorized. This includes locally appropriate continuations, errors without a reliable correction, cases with several similarly reasonable alternatives, and states without a meaningful local preference.

Return JSON only:
{
"boundary": "<evidence_completion|target_maintenance|answerability|not_selected>",
"reason": "<short state-grounded justification>",
"student_action_is_error": <true|false>
}

The field name "boundary" is retained for implementation compatibility. Its value functions only as an auxiliary construction tag and does not independently identify a search-control boundary.

The error judgment must evaluate the complete continuation, including its thought, action, and parameter. Do not use the observation produced by the continuation, any later action or observation, the rollout outcome, or a gold answer."""


CHOSEN_SYSTEM = """Generate a student-specific correction for the given decision-time state, search-state brief, assessment record, and original student continuation.

Directly address the specific local error identified in the student continuation under the fixed student action interface.

The correction may:

- use Continue to acquire concrete unresolved evidence along an aligned search direction;
- use Reroute to restore the Original Search Target or a missing Key Constraint when the current direction is misaligned; or
- use Answer when the currently available evidence is sufficient.

Return JSON only:
{
"thought": "<brief rationale for the corrected next decision>",
"action": "<Continue|Reroute|Answer>",
"parameter": "<focused retrieval query or concise final answer>"
}

For Continue, the retrieval query must target a concrete unresolved information need along the current valid direction.

For Reroute, the continuation must restore the intended target or constraint rather than continue along the displaced direction, and Parameter must be a focused rerouting query.

For Answer, Parameter must be a concise answer supported by evidence already available in the student-visible state.

Because the correction is conditioned on the original student continuation, it should address that student's specific error rather than replace it with a generic teacher continuation.

The returned continuation must remain expressible from the student-visible state. Do not copy the search-state brief, auxiliary construction tag, assessment justification, rollout outcome, future information, or other teacher-only information into the student-facing continuation."""


NEGATIVE_SYSTEM = """Construct one rejected local continuation for an answerability decision point.

The chosen continuation correctly stops and answers using the currently available evidence. Construct a plausible alternative that performs unnecessary additional retrieval instead.

The rejected continuation must:

- be plausible under the student-visible state;
- use either Continue or Reroute;
- pursue a concrete but unnecessary subgoal suggested by the current state;
- avoid introducing a new entity, constraint, or information need;
- remain grounded in the student-visible state; and
- express a clear contrast with the chosen Answer continuation.

Return JSON only:
{
"thought": "<brief rationale that incorrectly claims further retrieval is needed>",
"action": "<Continue|Reroute>",
"parameter": "<focused but unnecessary retrieval query>"
}

Do not introduce future observations or teacher-only information."""


def _state_text(state: SearchState) -> str:
    return json.dumps(
        state.to_dict(),
        ensure_ascii=False,
    )


def brief_messages(
    state: SearchState,
) -> list[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": BRIEF_SYSTEM,
        },
        {
            "role": "user",
            "content": _state_text(state),
        },
    ]


def diagnosis_messages(
    state: SearchState,
    brief: Brief,
    student_action: Dict[str, str],
) -> list[Dict[str, str]]:
    payload = {
        "state": state.to_dict(),
        "brief": brief.to_dict(),
        "student_action": student_action,
    }

    return [
        {
            "role": "system",
            "content": DIAGNOSIS_SYSTEM,
        },
        {
            "role": "user",
            "content": json.dumps(
                payload,
                ensure_ascii=False,
            ),
        },
    ]


def chosen_messages(
    state: SearchState,
    brief: Brief,
    diagnosis: Dict[str, Any],
    student_action: Dict[str, str],
) -> list[Dict[str, str]]:
    payload = {
        "state": state.to_dict(),
        "brief": brief.to_dict(),
        "diagnosis": diagnosis,
        "student_action": student_action,
    }

    return [
        {
            "role": "system",
            "content": CHOSEN_SYSTEM,
        },
        {
            "role": "user",
            "content": json.dumps(
                payload,
                ensure_ascii=False,
            ),
        },
    ]


def negative_messages(
    state: SearchState,
    brief: Brief,
    boundary: str,
    chosen: Dict[str, str],
) -> list[Dict[str, str]]:
    """Build the unnecessary-retrieval generation prompt.

    ``boundary`` is retained in the function signature for compatibility
    with existing construction code. The teacher does not need it at this
    stage because the answerability decision point has already been selected.
    """

    if boundary != "answerability":
        raise ValueError(
            "negative continuation generation requires an answerability decision point"
        )

    payload = {
        "state": state.to_dict(),
        "brief": brief.to_dict(),
        "chosen": chosen,
    }

    return [
        {
            "role": "system",
            "content": NEGATIVE_SYSTEM,
        },
        {
            "role": "user",
            "content": json.dumps(
                payload,
                ensure_ascii=False,
            ),
        },
    ]


def render_student_prompt(
    state: SearchState,
) -> list[Dict[str, str]]:
    """Render only the student-visible state; privileged data is absent."""

    return [
        {
            "role": "system",
            "content": SEARCH_POLICY_SYSTEM,
        },
        {
            "role": "user",
            "content": _state_text(state),
        },
    ]