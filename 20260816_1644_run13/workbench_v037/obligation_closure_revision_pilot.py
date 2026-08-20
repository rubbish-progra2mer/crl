from __future__ import annotations

import difflib
import json
import re
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:7b"
OUT = Path(__file__).with_name("obligation_closure_revision_qwen2_5_7b.json")
SECTION_ORDER = [
    "SUMMARY",
    "ALPHA_FINDING",
    "ALPHA_COMPARISON",
    "BETA_FINDING",
    "BETA_RECOMMENDATION",
    "LIMITATIONS",
    "SOURCES",
]


@dataclass(frozen=True)
class Case:
    case_id: str
    project: str
    alpha_label: str
    alpha_old: str
    alpha_new: str
    alpha_old_cite: str
    alpha_new_cite: str
    beta_label: str
    beta_old: str
    beta_new: str
    beta_old_cite: str
    beta_new_cite: str
    sentinel: str


CASES = [
    Case("energy", "Orion microgrid", "verified households", "120", "168", "[A17]", "[A91]", "storage loss", "14%", "9%", "[B22]", "[B88]", "SENTINEL-CEDAR-41"),
    Case("farming", "Lumen irrigation", "participating farms", "46", "73", "[A24]", "[A92]", "water waste", "19%", "11%", "[B31]", "[B89]", "SENTINEL-EMBER-52"),
    Case("schools", "Nacre tutoring", "completed cohorts", "18", "27", "[A35]", "[A93]", "dropout rate", "16%", "7%", "[B42]", "[B90]", "SENTINEL-FJORD-63"),
    Case("transit", "Vela bus trial", "daily riders", "840", "1120", "[A46]", "[A94]", "missed connections", "12%", "5%", "[B53]", "[B91]", "SENTINEL-GARNET-74"),
]


def render_initial(c: Case) -> str:
    return f"""## SUMMARY
The {c.project} currently reports {c.alpha_old} {c.alpha_label} {c.alpha_old_cite}. Its {c.beta_label} remains {c.beta_old} {c.beta_old_cite}.

## ALPHA_FINDING
Audited enrollment records list {c.alpha_old} {c.alpha_label} for the {c.project} {c.alpha_old_cite}.

## ALPHA_COMPARISON
At {c.alpha_old} {c.alpha_label}, the {c.project} remains below the comparison threshold {c.alpha_old_cite}.

## BETA_FINDING
The operations log estimates {c.beta_label} at {c.beta_old} for the {c.project} {c.beta_old_cite}.

## BETA_RECOMMENDATION
Because {c.beta_label} is {c.beta_old}, the report recommends retaining the current mitigation plan {c.beta_old_cite}.

## LIMITATIONS
The audit excludes seasonal variation and preserves the independent marker {c.sentinel}. No conclusion in this section depends on enrollment or loss estimates.

## SOURCES
{c.alpha_old_cite} Archived enrollment table supporting {c.alpha_old} {c.alpha_label}. {c.beta_old_cite} Operations log supporting {c.beta_old} {c.beta_label}. [L60] Seasonal-variation note supporting {c.sentinel}.
"""


def turn_spec(c: Case, turn: int) -> dict[str, Any]:
    if turn == 1:
        return {
            "feedback": (
                f"New verified evidence changes {c.project}'s {c.alpha_label} from {c.alpha_old} to {c.alpha_new} "
                f"and replaces citation {c.alpha_old_cite} with {c.alpha_new_cite}. Update every statement that semantically depends on this fact. "
                "Preserve every unrelated statement and citation exactly."
            ),
            "closure": ["SUMMARY", "ALPHA_FINDING", "ALPHA_COMPARISON", "SOURCES"],
            "direct": ["ALPHA_FINDING"],
            "old_tokens": [c.alpha_old, c.alpha_old_cite],
            "new_tokens": [c.alpha_new, c.alpha_new_cite],
        }
    return {
        "feedback": (
            f"A corrected operations audit changes {c.project}'s {c.beta_label} from {c.beta_old} to {c.beta_new} "
            f"and replaces citation {c.beta_old_cite} with {c.beta_new_cite}. Update every statement that semantically depends on this fact. "
            "Keep the prior enrollment correction and preserve every unrelated statement and citation exactly."
        ),
        "closure": ["SUMMARY", "BETA_FINDING", "BETA_RECOMMENDATION", "SOURCES"],
        "direct": ["BETA_FINDING"],
        "old_tokens": [c.beta_old, c.beta_old_cite],
        "new_tokens": [c.beta_new, c.beta_new_cite],
    }


def call_model(prompt: str, json_mode: bool = False) -> tuple[str, dict[str, Any]]:
    payload: dict[str, Any] = {
        "model": MODEL,
        "stream": False,
        "messages": [{"role": "user", "content": prompt}],
        "options": {"temperature": 0, "num_ctx": 8192, "num_predict": 1400},
        "keep_alive": "20m",
    }
    if json_mode:
        payload["format"] = "json"
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=240) as response:
        data = json.loads(response.read().decode("utf-8"))
    meta = {
        "seconds": time.perf_counter() - started,
        "prompt_eval_count": data.get("prompt_eval_count"),
        "eval_count": data.get("eval_count"),
        "done_reason": data.get("done_reason"),
    }
    return data["message"]["content"], meta


def parse_sections(text: str) -> dict[str, str]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:markdown|md|text)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    matches = list(re.finditer(r"(?m)^##\s+([A-Z_]+)\s*$", cleaned))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(cleaned)
        sections[match.group(1)] = cleaned[start:end].strip()
    return sections


def render_sections(sections: dict[str, str]) -> str:
    return "\n\n".join(f"## {name}\n{sections.get(name, '').strip()}" for name in SECTION_ORDER).strip() + "\n"


def parse_json_object(text: str) -> dict[str, str]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    obj = json.loads(cleaned)
    return {str(key): str(value).strip() for key, value in obj.items()}


def revise_whole(report: str, feedback: str, closure: list[str], strong: bool) -> tuple[str, dict[str, Any]]:
    if strong:
        instruction = f"""You are a precision report editor.
The only sections allowed to change are: {', '.join(closure)}.
All other sections must be copied character-for-character, including wording, numbers, citations, and the sentinel marker.
Within allowed sections, apply the feedback to every dependent statement while retaining all other correct facts from earlier turns.
Return the complete report with exactly these headings in this order: {', '.join(SECTION_ORDER)}.
Do not add commentary or code fences.
"""
    else:
        instruction = "Revise the complete report to apply the feedback. Preserve unrelated correct content and citations. Return only the complete revised report with the same headings.\n"
    prompt = f"{instruction}\nCURRENT REPORT:\n{report}\n\nFEEDBACK:\n{feedback}"
    return call_model(prompt)


def revise_splice(report: str, feedback: str, editable: list[str]) -> tuple[str, dict[str, Any]]:
    current = parse_sections(report)
    selected = {name: current.get(name, "") for name in editable}
    prompt = f"""You are a precision report editor.
Revise only the supplied sections to apply the feedback. Update all dependent statements inside these sections and retain other facts from earlier turns.
Return one JSON object whose keys are exactly {json.dumps(editable)} and whose values are the complete revised section bodies without headings.
Do not return any other keys or commentary.

EDITABLE SECTIONS:
{json.dumps(selected, ensure_ascii=False, indent=2)}

FULL REPORT FOR CONTEXT:
{report}

FEEDBACK:
{feedback}
"""
    raw, meta = call_model(prompt, json_mode=True)
    try:
        replacements = parse_json_object(raw)
        if set(replacements) != set(editable):
            raise ValueError(f"keys={sorted(replacements)}")
        for name in editable:
            current[name] = replacements[name]
        return render_sections(current), {**meta, "parse_error": None, "raw": raw}
    except Exception as exc:
        return report, {**meta, "parse_error": repr(exc), "raw": raw}


def contains_all(text: str, tokens: list[str]) -> bool:
    return all(token in text for token in tokens)


def score_turn(before: str, after: str, c: Case, turn: int) -> dict[str, Any]:
    spec = turn_spec(c, turn)
    before_sections = parse_sections(before)
    after_sections = parse_sections(after)
    structure_ok = list(after_sections) == SECTION_ORDER
    closure = spec["closure"]
    outside = [name for name in SECTION_ORDER if name not in closure]
    dependency_ok_by_section = {
        name: contains_all(after_sections.get(name, ""), spec["new_tokens"])
        and not any(token in after_sections.get(name, "") for token in spec["old_tokens"])
        for name in closure
    }
    exact_outside_by_section = {
        name: before_sections.get(name) == after_sections.get(name) for name in outside
    }
    sentinel_ok = c.sentinel in after_sections.get("LIMITATIONS", "")
    alpha_history_ok = True
    if turn == 2:
        alpha_history_ok = all(
            contains_all(after_sections.get(name, ""), [c.alpha_new, c.alpha_new_cite])
            and c.alpha_old_cite not in after_sections.get(name, "")
            for name in ["SUMMARY", "ALPHA_FINDING", "ALPHA_COMPARISON", "SOURCES"]
        )
    dependency_ok = all(dependency_ok_by_section.values())
    outside_exact = all(exact_outside_by_section.values())
    return {
        "structure_ok": structure_ok,
        "dependency_ok": dependency_ok,
        "dependency_ok_by_section": dependency_ok_by_section,
        "outside_exact": outside_exact,
        "outside_exact_by_section": exact_outside_by_section,
        "sentinel_ok": sentinel_ok,
        "alpha_history_ok": alpha_history_ok,
        "full_success": structure_ok and dependency_ok and outside_exact and sentinel_ok and alpha_history_ok,
        "character_change_ratio": 1.0 - difflib.SequenceMatcher(None, before, after).ratio(),
        "section_count": len(after_sections),
    }


def run_strategy(c: Case, strategy: str) -> dict[str, Any]:
    report = render_initial(c)
    turns: list[dict[str, Any]] = []
    for turn in (1, 2):
        spec = turn_spec(c, turn)
        before = report
        if strategy == "whole":
            report, meta = revise_whole(before, spec["feedback"], spec["closure"], strong=False)
        elif strategy == "strong_whole":
            report, meta = revise_whole(before, spec["feedback"], spec["closure"], strong=True)
        elif strategy == "direct_splice":
            report, meta = revise_splice(before, spec["feedback"], spec["direct"])
        elif strategy == "closure_splice":
            report, meta = revise_splice(before, spec["feedback"], spec["closure"])
        else:
            raise ValueError(strategy)
        turns.append({
            "turn": turn,
            "feedback": spec["feedback"],
            "score": score_turn(before, report, c, turn),
            "meta": meta,
            "report": report,
        })
    return {"case_id": c.case_id, "strategy": strategy, "initial_report": render_initial(c), "turns": turns}


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for strategy in ["whole", "strong_whole", "direct_splice", "closure_splice"]:
        selected = [run for run in runs if run["strategy"] == strategy]
        if not selected:
            continue
        scores = [turn["score"] for run in selected for turn in run["turns"]]
        second = [run["turns"][1]["score"] for run in selected]
        metas = [turn["meta"] for run in selected for turn in run["turns"]]
        summary[strategy] = {
            "turn_count": len(scores),
            "dependency_ok": sum(score["dependency_ok"] for score in scores),
            "outside_exact": sum(score["outside_exact"] for score in scores),
            "full_success": sum(score["full_success"] for score in scores),
            "turn2_alpha_history_ok": sum(score["alpha_history_ok"] for score in second),
            "mean_character_change_ratio": sum(score["character_change_ratio"] for score in scores) / len(scores),
            "parse_errors": sum(bool(meta.get("parse_error")) for meta in metas),
            "total_seconds": sum(meta["seconds"] for meta in metas),
            "total_eval_tokens": sum((meta.get("eval_count") or 0) for meta in metas),
        }
    return summary


def main() -> None:
    strategies = ["whole", "strong_whole", "direct_splice", "closure_splice"]
    runs: list[dict[str, Any]] = []
    for case in CASES:
        for strategy in strategies:
            print(f"running {case.case_id} {strategy}", flush=True)
            run = run_strategy(case, strategy)
            runs.append(run)
            OUT.write_text(json.dumps({"model": MODEL, "runs": runs, "summary": summarize(runs)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    result = {"model": MODEL, "case_count": len(CASES), "strategies": strategies, "runs": runs, "summary": summarize(runs)}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
