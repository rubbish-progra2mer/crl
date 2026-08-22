"""Resolve external question references before DPO preprocessing."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Iterator


QUESTION_REF = re.compile(r"^<QUESTION_REF:([^<>]+)>$")


def _iter_records(path: str | Path) -> Iterator[dict[str, Any]]:
    source = Path(path)
    text = source.read_text(encoding="utf-8-sig")
    stripped = text.lstrip()
    if not stripped:
        return
    if stripped.startswith("[") or stripped.startswith("{"):
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            value = None
        if isinstance(value, list):
            yield from (row for row in value if isinstance(row, dict))
            return
        if isinstance(value, dict):
            for key in ("data", "records", "examples", "train"):
                rows = value.get(key)
                if isinstance(rows, list):
                    yield from (row for row in rows if isinstance(row, dict))
                    return
            yield value
            return
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{source}:{line_number} is not a JSON object")
        yield value


def _mapping_question_id(row: dict[str, Any]) -> str | None:
    raw = row.get("question_id", row.get("id", row.get("_id")))
    if raw is None:
        return None
    value = str(raw).strip()
    if not value:
        return None
    if value.startswith(("hotpotqa:", "musique:", "synthetic_")):
        return value
    sub_source = str(row.get("sub_source", "")).casefold().strip()
    if sub_source == "hotpotqa":
        if value.startswith("hotpot_"):
            value = value[len("hotpot_") :]
        return f"hotpotqa:{value}"
    if sub_source == "musique":
        return f"musique:{value}"
    return None


def load_question_mapping(paths: Iterable[str | Path]) -> dict[str, str]:
    """Load one or more normalized or source-aware question tables."""

    mapping: dict[str, str] = {}
    for path in paths:
        for row in _iter_records(path):
            question_id = _mapping_question_id(row)
            if question_id is None:
                continue
            question = row.get("question")
            if not isinstance(question, str) or not question.strip():
                raise ValueError(f"question mapping entry {question_id!r} has no question text")
            normalized = question.strip()
            previous = mapping.setdefault(question_id, normalized)
            if previous != normalized:
                raise ValueError(f"conflicting question text for {question_id}")
    return mapping


def _resolved_question(question_id: str, mapping: dict[str, str]) -> str:
    if question_id not in mapping:
        raise KeyError(f"question ID is missing from the supplied mapping: {question_id}")
    question = mapping[question_id]
    if not question.strip():
        raise ValueError(f"resolved question is empty: {question_id}")
    return question


def resolve_training_record(
    record: dict[str, Any], mapping: dict[str, str]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a strict prompt/chosen/rejected row with one full question field."""

    if not isinstance(record, dict):
        raise ValueError("DPO record must be an object")
    prompt = deepcopy(record.get("prompt"))
    if (
        not isinstance(prompt, list)
        or len(prompt) != 2
        or [message.get("role") for message in prompt if isinstance(message, dict)]
        != ["system", "user"]
    ):
        raise ValueError("prompt must be a system/user conversation")
    try:
        state = json.loads(prompt[1]["content"])
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("prompt user content must be a JSON search state") from exc
    if not isinstance(state, dict):
        raise ValueError("prompt search state must be an object")

    top_question_id = record.get("question_id")
    if top_question_id is not None:
        top_question_id = str(top_question_id).strip()
    separate_question = record.get("question")
    if separate_question is not None and (
        not isinstance(separate_question, str) or not separate_question.strip()
    ):
        raise ValueError("top-level question must be a non-empty string")

    mode = "embedded"
    resolved_id = None
    if set(state) == {"question", "history", "context"}:
        question_value = state["question"]
        if not isinstance(question_value, str) or not question_value.strip():
            raise ValueError("state.question must be a non-empty string")
        match = QUESTION_REF.fullmatch(question_value.strip())
        if match:
            resolved_id = match.group(1)
            if top_question_id and top_question_id != resolved_id:
                raise ValueError("top-level question_id disagrees with QUESTION_REF")
            state["question"] = _resolved_question(resolved_id, mapping)
            mode = "question_ref"
        elif top_question_id and top_question_id in mapping:
            if mapping[top_question_id] != question_value.strip():
                raise ValueError("embedded question disagrees with question mapping")
            state["question"] = question_value.strip()
            resolved_id = top_question_id
        else:
            state["question"] = question_value.strip()
    elif set(state) == {"question_id", "history", "context"}:
        resolved_id = str(state["question_id"]).strip()
        if not resolved_id:
            raise ValueError("state.question_id cannot be empty")
        if top_question_id and top_question_id != resolved_id:
            raise ValueError("top-level and state question IDs disagree")
        state = {
            "question": _resolved_question(resolved_id, mapping),
            "history": state["history"],
            "context": state["context"],
        }
        mode = "question_id"
    elif set(state) == {"history", "context"}:
        if isinstance(separate_question, str):
            state = {
                "question": separate_question.strip(),
                "history": state["history"],
                "context": state["context"],
            }
            mode = "separate_question"
        elif top_question_id:
            resolved_id = top_question_id
            state = {
                "question": _resolved_question(resolved_id, mapping),
                "history": state["history"],
                "context": state["context"],
            }
            mode = "top_level_question_id"
        else:
            raise ValueError("decoupled state has neither question nor question_id")
    else:
        raise ValueError(
            "state must contain question/history/context, question_id/history/context, "
            "or history/context with a top-level question reference"
        )

    if isinstance(separate_question, str) and separate_question.strip() != state["question"]:
        raise ValueError("top-level and reconstructed questions disagree")
    if QUESTION_REF.fullmatch(state["question"]):
        raise ValueError("QUESTION_REF remained after reconstruction")
    prompt[1] = {
        "role": "user",
        "content": json.dumps(state, ensure_ascii=False),
    }
    result = {
        "prompt": prompt,
        "chosen": deepcopy(record.get("chosen")),
        "rejected": deepcopy(record.get("rejected")),
    }
    return result, {"mode": mode, "question_id": resolved_id}
