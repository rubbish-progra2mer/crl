"""Construct local preferences from student-induced decision-time states."""

from __future__ import annotations

import json
import re
import unicodedata
from difflib import SequenceMatcher
from typing import Any, Dict, Iterator

from prompts import (
    SEARCH_POLICY_SYSTEM,
    brief_messages,
    chosen_messages,
    diagnosis_messages,
    negative_messages,
    render_student_prompt,
)
from schema import BOUNDARIES, Action, Brief, RolloutStep, SearchState
from teacher import Teacher


# These strings identify construction-side information that must never be
# copied into student-facing continuations.  Plain field names are included in
# addition to quoted/bracketed forms because a model may reproduce a field name
# without its original JSON punctuation.
_TEACHER_ONLY_MARKERS = (
    "original search target",
    "key constraints",
    "confirmed evidence",
    "missing information",
    "drift status",
    "search-state brief",
    "search state brief",
    "evidence_completion",
    "target_maintenance",
    "answerability",
    "not_selected",
    "student_action_is_error",
    "rollout outcome",
    "rollout_outcome",
    "assessment justification",
    "diagnosis reason",
    "auxiliary construction tag",
    "teacher-only information",
    "teacher only information",
    "future observation",
    "future information",
)

_PROTOCOL_TAGS = ("[thought]", "[action]", "[parameter]")

# Conservative boilerplate removal used only to decide whether two retrieval
# parameters express the same local intent.  We deliberately do not use an
# embedding model here: validation must remain deterministic and should reject
# only high-confidence near-duplicates.
_QUERY_BOILERPLATE = {
    "a",
    "an",
    "and",
    "about",
    "for",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
    "search",
    "searching",
    "find",
    "finding",
    "lookup",
    "look",
    "up",
    "retrieve",
    "retrieval",
    "information",
    "details",
}

_TOKEN_RE = re.compile(r"[\w]+", flags=re.UNICODE)


def _validate_diagnosis(value: Dict[str, Any]) -> Dict[str, Any]:
    required = {"boundary", "reason", "student_action_is_error"}
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError(
            "diagnosis must contain exactly boundary, reason, and student_action_is_error"
        )
    boundary = value["boundary"]
    if boundary not in BOUNDARIES:
        raise ValueError(f"invalid boundary: {boundary!r}")
    if not isinstance(value["reason"], str) or not value["reason"].strip():
        raise ValueError("diagnosis.reason must be a non-empty string")
    if not isinstance(value["student_action_is_error"], bool):
        raise ValueError("student_action_is_error must be boolean")
    return dict(value)


def _normalize_text(value: str) -> str:
    """Normalize free text for deterministic comparison."""

    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(value.split())


def _normalize_parameter(value: str) -> str:
    """Normalize a parameter for deterministic local-decision comparison."""

    return _normalize_text(value)


def _tokens(value: str) -> list[str]:
    return _TOKEN_RE.findall(_normalize_text(value))


def _content_tokens(value: str) -> list[str]:
    return [token for token in _tokens(value) if token not in _QUERY_BOILERPLATE]


def _intent_signature(value: str) -> tuple[str, ...]:
    """Return a conservative lexical signature for a local retrieval intent."""

    tokens = _content_tokens(value)
    normalized: list[str] = []
    for token in tokens:
        # Small inflection normalization catches superficial variants such as
        # "studies"/"study" and "experiments"/"experiment" without turning
        # this into a language-dependent stemming pipeline.
        if len(token) > 4 and token.endswith("ies"):
            token = token[:-3] + "y"
        elif len(token) > 4 and token.endswith("es"):
            token = token[:-2]
        elif len(token) > 3 and token.endswith("s"):
            token = token[:-1]
        normalized.append(token)
    return tuple(normalized)


def _same_search_control_decision(left: Action, right: Action) -> bool:
    """Return True when two continuations differ only in reasoning text."""

    return (
        left.action == right.action
        and _normalize_parameter(left.parameter)
        == _normalize_parameter(right.parameter)
    )


def _equivalent_local_intent(left: Action, right: Action) -> bool:
    """Detect high-confidence superficial rewrites of the same local intent.

    Different action labels are different search-control decisions under the
    BOUND interface, even when their parameters are lexically similar.  For
    equal action labels, exact normalized parameters and very close lexical
    rewrites are rejected.
    """

    if left.action != right.action:
        return False
    if _same_search_control_decision(left, right):
        return True

    left_sig = _intent_signature(left.parameter)
    right_sig = _intent_signature(right.parameter)
    if not left_sig or not right_sig:
        return False
    if left_sig == right_sig:
        return True

    left_set = set(left_sig)
    right_set = set(right_sig)
    union = left_set | right_set
    jaccard = len(left_set & right_set) / len(union) if union else 0.0
    sequence = SequenceMatcher(
        None,
        " ".join(left_sig),
        " ".join(right_sig),
    ).ratio()

    # Deliberately conservative thresholds: validation should remove pairs
    # that clearly differ only superficially, not collapse genuinely distinct
    # retrieval subgoals that happen to share task entities.
    return jaccard >= 0.90 and sequence >= 0.92


def _state_text(state: SearchState, *, context_only: bool = False) -> str:
    if context_only:
        payload: Any = state.context
    else:
        payload = state.to_dict()
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _lexical_overlap_ratio(parameter: str, source_text: str) -> float:
    parameter_tokens = set(_content_tokens(parameter))
    if not parameter_tokens:
        return 0.0
    source_tokens = set(_content_tokens(source_text))
    return len(parameter_tokens & source_tokens) / len(parameter_tokens)


def _retrieval_is_state_grounded(action: Action, state: SearchState) -> bool:
    """Reject retrieval continuations that are lexically unrelated to s_t.

    This is a conservative lower-bound check for decision-time grounding.  It
    catches unrelated/new-topic generations while allowing paraphrases and
    ordinary query reformulations as long as at least one substantive term is
    anchored in the observable state.
    """

    if action.action not in {"Continue", "Reroute"}:
        return True
    return _lexical_overlap_ratio(action.parameter, _state_text(state)) > 0.0


def _answer_has_state_evidence(answer: Action, state: SearchState) -> bool:
    """Check that a chosen Answer has lexical support in available evidence.

    The check is intentionally conservative: it accepts exact normalized
    mentions, single-token mentions, and partial multi-token aliases.  It is
    used only for *chosen* answers; an erroneous rejected student Answer is not
    required to be supported.
    """

    if answer.action != "Answer":
        return True

    answer_norm = _normalize_text(answer.parameter)
    context_norm = _normalize_text(_state_text(state, context_only=True))
    if answer_norm and answer_norm in context_norm:
        return True

    answer_tokens = set(_content_tokens(answer.parameter))
    if not answer_tokens:
        return False
    context_tokens = set(_content_tokens(context_norm))
    overlap = answer_tokens & context_tokens

    if len(answer_tokens) == 1:
        return bool(overlap)

    # Multi-token answers often include a qualifier (e.g. city + country) that
    # is not repeated verbatim in one passage.  Requiring at least half of the
    # substantive answer tokens, and at least one token, avoids rejecting such
    # grounded aliases while still blocking unsupported answers.
    return bool(overlap) and len(overlap) / len(answer_tokens) >= 0.5


def _action_parameter_is_consistent(action: Action) -> bool:
    """Catch clear action/parameter mismatches without semantic overreach."""

    parameter = _normalize_text(action.parameter)
    tokens = _tokens(parameter)

    if action.action in {"Continue", "Reroute"}:
        # A retrieval action should contain a query/subgoal, not an explicit
        # final-answer assertion.
        final_answer_prefixes = (
            "answer:",
            "final answer:",
            "the answer is ",
            "my answer is ",
        )
        return not parameter.startswith(final_answer_prefixes)

    # An Answer should not obviously be a retrieval instruction.  Requiring a
    # longer directive avoids rejecting legitimate short titles such as
    # "Search for Tomorrow".
    retrieval_verbs = {
        "search",
        "lookup",
        "retrieve",
        "find",
        "verify",
        "check",
        "investigate",
    }
    if len(tokens) >= 5 and tokens and tokens[0] in retrieval_verbs:
        return False
    return True


def _contains_protocol_tag_inside_field(action: Action) -> bool:
    for value in (action.thought, action.parameter):
        lowered = value.casefold()
        if any(tag in lowered for tag in _PROTOCOL_TAGS):
            return True
    return False


def _leaks_teacher_metadata(action: Action) -> bool:
    lowered = f"{action.thought}\n{action.parameter}".casefold()
    return any(marker in lowered for marker in _TEACHER_ONLY_MARKERS)


def select_boundary(
    rollout_success: bool,
    diagnosis: Dict[str, Any],
    student_action: Action,
) -> Dict[str, Any]:
    """Select states using the outcome-conditioned construction rules.

    Successful rollouts contribute only the earliest locally supported Answer
    decision.  Unsuccessful rollouts contribute only diagnosed local errors
    for which a consequential construction route is authorized.
    """

    boundary = diagnosis["boundary"]
    error = diagnosis["student_action_is_error"]

    retain_student_answer = (
        rollout_success
        and boundary == "answerability"
        and student_action.action == "Answer"
        and not error
    )

    if rollout_success:
        selected = retain_student_answer
    else:
        selected = boundary != "not_selected" and error

    return {
        "selected": selected,
        "rollout_success": rollout_success,
    }


def validate_pair(
    state: SearchState,
    diagnosis: Dict[str, Any],
    student_action: Action,
    chosen: Action,
    rejected: Action,
    *,
    retained_student_answer: bool,
) -> Dict[str, Any]:
    """Apply the paper's pair-validation checks at one decision-time state.

    Validation covers construction-route consistency, distinct local
    search-control decisions, conservative same-intent filtering,
    decision-time grounding of generated continuations, action/parameter
    consistency, protocol conformance, and teacher-only information leakage.
    """

    reasons: list[str] = []
    boundary = diagnosis["boundary"]
    error = diagnosis["student_action_is_error"]

    expected_action = {
        "evidence_completion": "Continue",
        "target_maintenance": "Reroute",
        "answerability": "Answer",
    }.get(boundary)

    if expected_action is None:
        reasons.append("no_consequential_boundary")
    elif chosen.action != expected_action:
        reasons.append("chosen_action_conflicts_with_boundary")

    # Construction-route consistency.
    if retained_student_answer:
        if boundary != "answerability" or error:
            reasons.append("invalid_supported_answer_route")
        if student_action.action != "Answer":
            reasons.append("supported_answer_source_must_answer")
        if chosen != student_action:
            reasons.append("supported_answer_must_retain_student_continuation")
        if rejected.action not in {"Continue", "Reroute"}:
            reasons.append("answer_negative_must_retrieve")
    else:
        if not error or boundary == "not_selected":
            reasons.append("invalid_corrective_route")
        if rejected != student_action:
            reasons.append("corrective_rejected_must_be_student_continuation")

    if chosen == rejected:
        reasons.append("chosen_equals_rejected")
    elif _same_search_control_decision(chosen, rejected):
        reasons.append("no_distinct_search_control_decision")
    elif _equivalent_local_intent(chosen, rejected):
        reasons.append("equivalent_local_search_intent")

    for label, action in (("chosen", chosen), ("rejected", rejected)):
        if len(action.parameter) > 512:
            reasons.append(f"{label}_parameter_too_long")

        if _contains_protocol_tag_inside_field(action):
            reasons.append(f"{label}_contains_embedded_protocol_tag")

        if _leaks_teacher_metadata(action):
            reasons.append(f"{label}_leaks_teacher_metadata")

        if not _action_parameter_is_consistent(action):
            reasons.append(f"{label}_action_parameter_inconsistent")

    # Generated/selected chosen decisions must be expressible from s_t.  The
    # rejected student continuation in corrective pairs is allowed to be wrong
    # or unsupported; it is the behavior being corrected.
    if chosen.action in {"Continue", "Reroute"} and not _retrieval_is_state_grounded(
        chosen, state
    ):
        reasons.append("chosen_not_grounded_in_state")

    if chosen.action == "Answer" and not _answer_has_state_evidence(chosen, state):
        reasons.append("chosen_answer_not_supported_by_state_evidence")

    # For the supported-answer route, the synthetic negative must be a
    # concrete but unnecessary retrieval subgoal grounded in the same state,
    # rather than an unrelated new topic.
    if retained_student_answer and not _retrieval_is_state_grounded(rejected, state):
        reasons.append("answer_negative_not_grounded_in_state")

    return {
        "valid": not reasons,
        "reasons": reasons,
    }


def _well_formed_candidate(value: Dict[str, Any]) -> RolloutStep | None:
    """Validate only s_t and y_t^0 (plus the step identifier), never o_t."""

    try:
        step_number = value["step"]
        if (
            not isinstance(step_number, int)
            or isinstance(step_number, bool)
            or step_number < 1
        ):
            return None

        state = SearchState.from_dict(value["state"])
        student_action = Action.from_dict(value["student_action"])
    except (KeyError, TypeError, ValueError):
        return None

    observation = value.get("observation", [])
    if not isinstance(observation, list):
        observation = []

    return RolloutStep(
        step_number,
        state,
        student_action,
        observation,
    )


def _safe_brief(teacher: Teacher, state: SearchState) -> Brief | None:
    """Generate one brief; malformed teacher output causes state abstention."""

    try:
        return Brief.from_dict(teacher.json(brief_messages(state)))
    except (TypeError, ValueError, KeyError):
        return None


def _safe_diagnosis(
    teacher: Teacher,
    state: SearchState,
    brief: Brief,
    student_action: Action,
) -> Dict[str, Any] | None:
    """Generate one local assessment; malformed output causes abstention."""

    try:
        return _validate_diagnosis(
            teacher.json(
                diagnosis_messages(
                    state,
                    brief,
                    student_action.to_dict(),
                )
            )
        )
    except (TypeError, ValueError, KeyError):
        return None


def _safe_generated_action(
    teacher: Teacher,
    messages: list[Dict[str, str]],
) -> Action | None:
    """Parse one generated continuation without allowing malformed pairs through."""

    try:
        return Action.from_dict(teacher.json(messages))
    except (TypeError, ValueError, KeyError):
        return None


def construct_preferences(
    record: Dict[str, Any],
    teacher: Teacher,
) -> Iterator[Dict[str, Any]]:
    trajectory_id = str(record["trajectory_id"])

    outcome = record.get("outcome", {})
    rollout_success = False
    if isinstance(outcome, dict) and isinstance(outcome.get("success"), bool):
        rollout_success = outcome["success"]

    steps = [
        step
        for value in record.get("steps", [])
        if isinstance(value, dict)
        and (step := _well_formed_candidate(value)) is not None
    ]

    candidates: list[
        tuple[RolloutStep, Brief, Dict[str, Any], Dict[str, Any]]
    ] = []

    for step in steps:
        # The post-action observation is deliberately absent from all same-step
        # prompts.  Malformed construction-side generations cause abstention
        # for this state rather than terminating the full dataset build.
        brief = _safe_brief(teacher, step.state)
        if brief is None:
            continue

        diagnosis = _safe_diagnosis(
            teacher,
            step.state,
            brief,
            step.student_action,
        )
        if diagnosis is None:
            continue

        selection = select_boundary(
            rollout_success,
            diagnosis,
            step.student_action,
        )

        if selection["selected"]:
            candidates.append(
                (
                    step,
                    brief,
                    diagnosis,
                    selection,
                )
            )

    # Successful rollouts contribute only the earliest evidence-supported
    # Answer selected by the decision-time assessment.
    retained_answer_steps = [
        step.step
        for step, _, diagnosis, _ in candidates
        if diagnosis["boundary"] == "answerability"
        and step.student_action.action == "Answer"
        and not diagnosis["student_action_is_error"]
    ]

    first_retained_answer = (
        min(retained_answer_steps)
        if rollout_success and retained_answer_steps
        else None
    )

    for step, brief, diagnosis, selection in sorted(
        candidates,
        key=lambda item: item[0].step,
    ):
        boundary = diagnosis["boundary"]

        if (
            rollout_success
            and boundary == "answerability"
            and step.student_action.action == "Answer"
            and not diagnosis["student_action_is_error"]
            and step.step != first_retained_answer
        ):
            continue

        original_state = step.state

        retained_student_answer = (
            rollout_success
            and boundary == "answerability"
            and step.student_action.action == "Answer"
            and not diagnosis["student_action_is_error"]
        )

        if retained_student_answer:
            chosen = step.student_action
            rejected = _safe_generated_action(
                teacher,
                negative_messages(
                    original_state,
                    brief,
                    boundary,
                    chosen.to_dict(),
                ),
            )
            if rejected is None:
                continue

            chosen_source = "student_rollout"
            rejected_source = "teacher_over_search"

        elif diagnosis["student_action_is_error"]:
            chosen = _safe_generated_action(
                teacher,
                chosen_messages(
                    original_state,
                    brief,
                    diagnosis,
                    step.student_action.to_dict(),
                ),
            )
            if chosen is None:
                continue

            rejected = step.student_action

            chosen_source = "teacher_correction"
            rejected_source = "student_rollout"

        else:
            continue

        validation = validate_pair(
            original_state,
            diagnosis,
            step.student_action,
            chosen,
            rejected,
            retained_student_answer=retained_student_answer,
        )

        if not validation["valid"]:
            continue

        yield {
            "pair_id": f"{trajectory_id}:{step.step}",
            "trajectory_id": trajectory_id,
            "step": step.step,
            "boundary": boundary,
            "selection": selection,
            "original_state": original_state.to_dict(),
            "prompt": render_student_prompt(original_state),
            "chosen": chosen.to_dict(),
            "rejected": rejected.to_dict(),
            "chosen_source": chosen_source,
            "rejected_source": rejected_source,
            "brief": brief.to_dict(),
            "diagnosis": diagnosis,
            "validation": validation,
            "rollout_outcome": {
                "success": rollout_success,
            },
        }


def to_training_record(pair: Dict[str, Any]) -> Dict[str, Any]:
    """Project an audit pair to the three student-visible DPO fields."""

    chosen = Action.from_dict(pair["chosen"])
    rejected = Action.from_dict(pair["rejected"])

    return {
        "prompt": pair["prompt"],
        "chosen": [
            {
                "role": "assistant",
                "content": chosen.render(),
            }
        ],
        "rejected": [
            {
                "role": "assistant",
                "content": rejected.render(),
            }
        ],
    }


def validate_training_record(record: Dict[str, Any]) -> None:
    """Validate the strict, brief-free, tagged-text DPO protocol."""

    if (
        not isinstance(record, dict)
        or set(record) != {"prompt", "chosen", "rejected"}
    ):
        raise ValueError(
            "training rows must contain only prompt, chosen, and rejected"
        )

    prompt = record["prompt"]

    if not isinstance(prompt, list) or len(prompt) != 2:
        raise ValueError(
            "prompt must be a two-message system/user conversation"
        )

    if any(
        not isinstance(message, dict)
        or set(message) != {"role", "content"}
        for message in prompt
    ):
        raise ValueError(
            "prompt messages must contain exactly role and content"
        )

    if [message["role"] for message in prompt] != ["system", "user"]:
        raise ValueError(
            "prompt roles must be system followed by user"
        )

    if prompt[0]["content"] != SEARCH_POLICY_SYSTEM:
        raise ValueError(
            "training prompt does not use the public inference system prompt"
        )

    try:
        state_value = json.loads(prompt[1]["content"])
        SearchState.from_dict(state_value)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError(
            "training user message must contain a valid search state"
        ) from exc

    parsed: list[Action] = []

    for field in ("chosen", "rejected"):
        messages = record[field]

        if (
            not isinstance(messages, list)
            or len(messages) != 1
            or not isinstance(messages[0], dict)
            or set(messages[0]) != {"role", "content"}
            or messages[0]["role"] != "assistant"
        ):
            raise ValueError(
                f"{field} must be one assistant message"
            )

        content = messages[0]["content"]

        try:
            action = Action.parse(content)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"{field} must contain one valid tagged-text action"
            ) from exc

        if len(action.parameter) > 512:
            raise ValueError(f"{field} parameter exceeds 512 characters")

        if _contains_protocol_tag_inside_field(action):
            raise ValueError(
                f"{field} contains an embedded protocol tag"
            )

        if _leaks_teacher_metadata(action):
            raise ValueError(
                f"{field} leaks teacher-only construction metadata"
            )

        if not _action_parameter_is_consistent(action):
            raise ValueError(
                f"{field} has an action/parameter mismatch"
            )

        parsed.append(action)

    if parsed[0] == parsed[1]:
        raise ValueError(
            "chosen and rejected continuations must differ"
        )

    if _same_search_control_decision(parsed[0], parsed[1]):
        raise ValueError(
            "chosen and rejected must differ in action or parameter"
        )

    if _equivalent_local_intent(parsed[0], parsed[1]):
        raise ValueError(
            "chosen and rejected express equivalent local search intent"
        )
