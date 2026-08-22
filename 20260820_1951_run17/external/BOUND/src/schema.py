"""Public schemas shared by rollout construction, DPO, and inference."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List


BRIEF_FIELDS = (
    "Original Search Target",
    "Key Constraints",
    "Confirmed Evidence",
    "Missing Information",
    "Drift Status",
)

ACTIONS = ("Continue", "Reroute", "Answer")
BOUNDARIES = (
    "evidence_completion",
    "target_maintenance",
    "answerability",
    "not_selected",
)

_TAGGED_ACTION = re.compile(
    r"\[Thought\]: (?P<thought>[^\r\n]+)\r?\n"
    r"\[Action\]: (?P<action>Continue|Reroute|Answer)\r?\n"
    r"\[Parameter\]: (?P<parameter>[^\r\n]+)"
)


@dataclass(frozen=True)
class Action:
    thought: str
    action: str
    parameter: str

    def __post_init__(self) -> None:
        for field_name in ("thought", "action", "parameter"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"action.{field_name} must be a non-empty string")
            if "\n" in value or "\r" in value:
                raise ValueError(f"action.{field_name} must be a single line")
        if self.action not in ACTIONS:
            raise ValueError(f"action must be one of {ACTIONS}, got {self.action!r}")

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "Action":
        if not isinstance(value, dict) or set(value) != {"thought", "action", "parameter"}:
            raise ValueError("action JSON must contain exactly thought, action, and parameter")
        if not all(isinstance(value[field], str) for field in value):
            raise ValueError("action fields must be strings")
        return cls(
            thought=value["thought"].strip(),
            action=value["action"].strip(),
            parameter=value["parameter"].strip(),
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "thought": self.thought,
            "action": self.action,
            "parameter": self.parameter,
        }

    @classmethod
    def parse(cls, text: str) -> "Action":
        if not isinstance(text, str):
            raise ValueError("student continuation must be text")
        match = _TAGGED_ACTION.fullmatch(text.strip())
        if match is None:
            raise ValueError(
                "continuation must contain exactly [Thought], [Action], and [Parameter] in order"
            )
        return cls(**match.groupdict())

    def render(self) -> str:
        return (
            f"[Thought]: {self.thought}\n"
            f"[Action]: {self.action}\n"
            f"[Parameter]: {self.parameter}"
        )


@dataclass(frozen=True)
class SearchState:
    question: str
    history: List[Dict[str, Any]]
    context: List[Dict[str, str]]

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "SearchState":
        if not isinstance(value, dict) or set(value) != {"question", "history", "context"}:
            raise ValueError("state must contain exactly question, history, and context")
        question = value["question"]
        history = value["history"]
        context = value["context"]
        if not isinstance(question, str) or not question.strip():
            raise ValueError("state.question cannot be empty")
        if not isinstance(history, list) or not isinstance(context, list):
            raise ValueError("state.history and state.context must be lists")

        normalized_history: List[Dict[str, Any]] = []
        for entry in history:
            if not isinstance(entry, dict) or set(entry) != {"step", "action", "parameter"}:
                raise ValueError("history entries must contain exactly step, action, and parameter")
            if not isinstance(entry["step"], int) or isinstance(entry["step"], bool) or entry["step"] < 1:
                raise ValueError("history step must be a positive integer")
            if entry["action"] not in ACTIONS:
                raise ValueError(f"history action must be one of {ACTIONS}")
            if not isinstance(entry["parameter"], str) or not entry["parameter"].strip():
                raise ValueError("history parameter must be a non-empty string")
            normalized_history.append(
                {
                    "step": entry["step"],
                    "action": entry["action"],
                    "parameter": entry["parameter"].strip(),
                }
            )

        if not all(isinstance(document, dict) for document in context):
            raise ValueError("state.context entries must be document objects")
        return cls(question=question.strip(), history=normalized_history, context=list(context))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "history": self.history,
            "context": self.context,
        }


@dataclass(frozen=True)
class Brief:
    values: Dict[str, str]

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "Brief":
        if not isinstance(value, dict):
            raise ValueError("brief must be a JSON object")
        missing = [field for field in BRIEF_FIELDS if field not in value]
        extra = [field for field in value if field not in BRIEF_FIELDS]
        empty = [
            field
            for field in BRIEF_FIELDS
            if field in value and (not isinstance(value[field], str) or not value[field].strip())
        ]
        if missing or extra or empty:
            raise ValueError(
                f"brief fields mismatch; missing={missing}, extra={extra}, empty={empty}"
            )
        normalized = {field: value[field].strip() for field in BRIEF_FIELDS}
        drift = normalized["Drift Status"].lower()
        if not drift.startswith(("aligned", "at risk", "drifted")):
            raise ValueError("Drift Status must start with aligned, at risk, or drifted")
        return cls(normalized)

    def to_dict(self) -> Dict[str, str]:
        return dict(self.values)


@dataclass(frozen=True)
class RolloutStep:
    step: int
    state: SearchState
    student_action: Action
    observation: List[Dict[str, str]]

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "RolloutStep":
        if not isinstance(value, dict) or set(value) != {
            "step",
            "state",
            "student_action",
            "observation",
        }:
            raise ValueError(
                "rollout step must contain exactly step, state, student_action, and observation"
            )
        step = value["step"]
        observation = value["observation"]
        if not isinstance(step, int) or isinstance(step, bool) or step < 1:
            raise ValueError("rollout step must be a positive integer")
        if not isinstance(observation, list) or not all(
            isinstance(document, dict) for document in observation
        ):
            raise ValueError("observation must be a list of document objects")
        return cls(
            step=step,
            state=SearchState.from_dict(value["state"]),
            student_action=Action.from_dict(value["student_action"]),
            observation=list(observation),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step,
            "state": self.state.to_dict(),
            "student_action": self.student_action.to_dict(),
            "observation": self.observation,
        }
