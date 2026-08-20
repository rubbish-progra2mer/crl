from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import obligation_closure_revision_pilot as base


OUT = Path(__file__).with_name("obligation_closure_stress_qwen2_5_7b.json")
ORDER = [
    "SUMMARY",
    "METHODS",
    "ALPHA_FINDING",
    "ALPHA_COMPARISON",
    "ALPHA_DECISION",
    "BETA_FINDING",
    "BETA_COMPARISON",
    "BETA_DECISION",
    "CONTEXT_A",
    "CONTEXT_B",
    "CONTEXT_C",
    "CONTEXT_D",
    "CONTEXT_E",
    "CONTEXT_F",
    "LIMITATIONS",
    "SOURCES",
]
base.SECTION_ORDER = ORDER


@dataclass(frozen=True)
class StressCase:
    case_id: str
    project: str
    alpha_label: str
    alpha_old: str
    alpha_new: str
    alpha_old_cite: str
    alpha_new_cite: str
    alpha_old_relation: str
    alpha_new_relation: str
    alpha_old_decision: str
    alpha_new_decision: str
    beta_label: str
    beta_old: str
    beta_new: str
    beta_old_cite: str
    beta_new_cite: str
    beta_old_relation: str
    beta_new_relation: str
    beta_old_decision: str
    beta_new_decision: str
    sentinel_prefix: str


CASES = [
    StressCase(
        "cobalt",
        "Cobalt learning network",
        "verified learners",
        "120",
        "168",
        "[A17]",
        "[A91]",
        "30 below the 150-learner threshold",
        "18 above the 150-learner threshold",
        "defer phase two",
        "expand phase two",
        "completion gap",
        "14%",
        "6%",
        "[B22]",
        "[B88]",
        "4 percentage points above the 10% ceiling",
        "4 percentage points below the 10% ceiling",
        "retain remedial review",
        "retire remedial review",
        "COBALT",
    ),
    StressCase(
        "harbor",
        "Harbor mobility trial",
        "verified daily riders",
        "840",
        "1120",
        "[A46]",
        "[A94]",
        "160 below the 1000-rider threshold",
        "120 above the 1000-rider threshold",
        "defer route expansion",
        "approve route expansion",
        "missed-connection rate",
        "12%",
        "5%",
        "[B53]",
        "[B91]",
        "4 percentage points above the 8% ceiling",
        "3 percentage points below the 8% ceiling",
        "retain transfer buffer",
        "retire transfer buffer",
        "HARBOR",
    ),
]


def context_paragraph(project: str, marker: str, topic: str) -> str:
    return (
        f"The {project} maintains a separate {topic} record identified by {marker}. "
        "This record describes governance, staffing, archival practice, stakeholder meetings, and routine quality checks. "
        "It is independent of the enrollment and outcome thresholds analyzed elsewhere in the report. "
        "The wording, marker, and citation in this paragraph are intentionally stable across revisions so that an unrelated edit cannot silently rewrite established context. "
        f"The supporting archive is cited as [{marker}-SRC]."
    )


def render_initial(c: StressCase) -> str:
    sections = {
        "SUMMARY": (
            f"The {c.project} reports {c.alpha_old} {c.alpha_label} {c.alpha_old_cite}, leaving it {c.alpha_old_relation}; the current recommendation is to {c.alpha_old_decision}. "
            f"Its {c.beta_label} is {c.beta_old} {c.beta_old_cite}, which is {c.beta_old_relation}, so managers should {c.beta_old_decision}."
        ),
        "METHODS": (
            "The report uses audited administrative records, a fixed threshold comparison, and explicit source markers. "
            "Threshold consequences are derived from the stated measurements rather than from unstated background assumptions."
        ),
        "ALPHA_FINDING": f"Audited records list {c.alpha_old} {c.alpha_label} for the {c.project} {c.alpha_old_cite}.",
        "ALPHA_COMPARISON": f"The audited count is {c.alpha_old_relation} {c.alpha_old_cite}.",
        "ALPHA_DECISION": f"Because the count has not reached the threshold, the decision is to {c.alpha_old_decision} {c.alpha_old_cite}.",
        "BETA_FINDING": f"The outcome audit estimates the {c.beta_label} at {c.beta_old} {c.beta_old_cite}.",
        "BETA_COMPARISON": f"The measured gap is {c.beta_old_relation} {c.beta_old_cite}.",
        "BETA_DECISION": f"Because the ceiling is not met, managers should {c.beta_old_decision} {c.beta_old_cite}.",
        "CONTEXT_A": context_paragraph(c.project, f"{c.sentinel_prefix}-A11", "governance"),
        "CONTEXT_B": context_paragraph(c.project, f"{c.sentinel_prefix}-B12", "staffing"),
        "CONTEXT_C": context_paragraph(c.project, f"{c.sentinel_prefix}-C13", "procurement"),
        "CONTEXT_D": context_paragraph(c.project, f"{c.sentinel_prefix}-D14", "communications"),
        "CONTEXT_E": context_paragraph(c.project, f"{c.sentinel_prefix}-E15", "archiving"),
        "CONTEXT_F": context_paragraph(c.project, f"{c.sentinel_prefix}-F16", "meeting cadence"),
        "LIMITATIONS": (
            f"The analysis excludes seasonal effects and preserves the independent audit marker {c.sentinel_prefix}-LIMIT-77 [L77]. "
            "These limitations do not depend on either corrected measurement."
        ),
        "SOURCES": (
            f"{c.alpha_old_cite} Enrollment audit supporting {c.alpha_old} {c.alpha_label}. "
            f"{c.beta_old_cite} Outcome audit supporting {c.beta_old} {c.beta_label}. "
            f"[L77] Limitations register for {c.sentinel_prefix}-LIMIT-77."
        ),
    }
    return base.render_sections(sections)


def spec(c: StressCase, turn: int) -> dict[str, Any]:
    if turn == 1:
        return {
            "feedback": (
                f"A new enrollment audit changes {c.project}'s {c.alpha_label} from {c.alpha_old} to {c.alpha_new} and replaces {c.alpha_old_cite} with {c.alpha_new_cite}. "
                f"The corrected count is {c.alpha_new_relation}; therefore change the recommendation from '{c.alpha_old_decision}' to '{c.alpha_new_decision}'. "
                "Update every dependent statement and source entry, while preserving all unrelated text exactly."
            ),
            "closure": ["SUMMARY", "ALPHA_FINDING", "ALPHA_COMPARISON", "ALPHA_DECISION", "SOURCES"],
            "expected": {
                "SUMMARY": [c.alpha_new, c.alpha_new_cite, c.alpha_new_relation, c.alpha_new_decision],
                "ALPHA_FINDING": [c.alpha_new, c.alpha_new_cite],
                "ALPHA_COMPARISON": [c.alpha_new_relation, c.alpha_new_cite],
                "ALPHA_DECISION": [c.alpha_new_decision, c.alpha_new_cite],
                "SOURCES": [c.alpha_new, c.alpha_new_cite],
            },
            "forbidden": [c.alpha_old, c.alpha_old_cite, c.alpha_old_relation, c.alpha_old_decision],
        }
    return {
        "feedback": (
            f"A corrected outcome audit changes {c.project}'s {c.beta_label} from {c.beta_old} to {c.beta_new} and replaces {c.beta_old_cite} with {c.beta_new_cite}. "
            f"The corrected result is {c.beta_new_relation}; therefore change the recommendation from '{c.beta_old_decision}' to '{c.beta_new_decision}'. "
            "Update every dependent statement and source entry, preserve the prior enrollment correction, and preserve all unrelated text exactly."
        ),
        "closure": ["SUMMARY", "BETA_FINDING", "BETA_COMPARISON", "BETA_DECISION", "SOURCES"],
        "expected": {
            "SUMMARY": [c.beta_new, c.beta_new_cite, c.beta_new_relation, c.beta_new_decision],
            "BETA_FINDING": [c.beta_new, c.beta_new_cite],
            "BETA_COMPARISON": [c.beta_new_relation, c.beta_new_cite],
            "BETA_DECISION": [c.beta_new_decision, c.beta_new_cite],
            "SOURCES": [c.beta_new, c.beta_new_cite],
        },
        "forbidden": [c.beta_old, c.beta_old_cite, c.beta_old_relation, c.beta_old_decision],
    }


def plan_closure(report: str, feedback: str) -> tuple[list[str], dict[str, Any]]:
    prompt = f"""Identify the minimal set of report sections that must change to apply the feedback without leaving any stale dependent statement or source entry.
Return JSON as {{"sections": [section names]}}. Use only names from {json.dumps(ORDER)}. Include a section only if its current content semantically depends on the corrected fact or contains the replaced source entry.

REPORT:
{report}

FEEDBACK:
{feedback}
"""
    raw, meta = base.call_model(prompt, json_mode=True)
    try:
        obj = base.parse_json_object(raw)
        value: Any = json.loads(raw).get("sections")
        if not isinstance(value, list) or any(item not in ORDER for item in value):
            raise ValueError(value)
        chosen = list(dict.fromkeys(str(item) for item in value))
        return chosen, {**meta, "parse_error": None, "raw": raw}
    except Exception as exc:
        return [], {**meta, "parse_error": repr(exc), "raw": raw}


def alpha_history(c: StressCase, sections: dict[str, str]) -> bool:
    required = {
        "SUMMARY": [c.alpha_new, c.alpha_new_cite, c.alpha_new_relation, c.alpha_new_decision],
        "ALPHA_FINDING": [c.alpha_new, c.alpha_new_cite],
        "ALPHA_COMPARISON": [c.alpha_new_relation, c.alpha_new_cite],
        "ALPHA_DECISION": [c.alpha_new_decision, c.alpha_new_cite],
        "SOURCES": [c.alpha_new, c.alpha_new_cite],
    }
    return all(all(token in sections.get(name, "") for token in tokens) for name, tokens in required.items())


def score(before: str, after: str, c: StressCase, turn: int, selected: list[str] | None) -> dict[str, Any]:
    current = spec(c, turn)
    before_sections = base.parse_sections(before)
    after_sections = base.parse_sections(after)
    closure = current["closure"]
    outside = [name for name in ORDER if name not in closure]
    expected_by_section = {
        name: all(token in after_sections.get(name, "") for token in tokens)
        and not any(token in after_sections.get(name, "") for token in current["forbidden"])
        for name, tokens in current["expected"].items()
    }
    outside_by_section = {name: before_sections.get(name) == after_sections.get(name) for name in outside}
    selection_precision = None
    selection_recall = None
    if selected is not None:
        intersection = len(set(selected) & set(closure))
        selection_precision = intersection / len(set(selected)) if selected else 0.0
        selection_recall = intersection / len(set(closure))
    history_ok = True if turn == 1 else alpha_history(c, after_sections)
    dependencies_ok = all(expected_by_section.values())
    outside_exact = all(outside_by_section.values())
    structure_ok = list(after_sections) == ORDER
    return {
        "structure_ok": structure_ok,
        "dependencies_ok": dependencies_ok,
        "expected_by_section": expected_by_section,
        "outside_exact": outside_exact,
        "outside_by_section": outside_by_section,
        "history_ok": history_ok,
        "full_success": structure_ok and dependencies_ok and outside_exact and history_ok,
        "selected": selected,
        "selection_precision": selection_precision,
        "selection_recall": selection_recall,
    }


def run(c: StressCase, strategy: str) -> dict[str, Any]:
    report = render_initial(c)
    turns = []
    for turn in (1, 2):
        current = spec(c, turn)
        before = report
        selected = None
        plan_meta = None
        if strategy == "whole":
            report, edit_meta = base.revise_whole(before, current["feedback"], current["closure"], strong=False)
        elif strategy == "strong_whole":
            report, edit_meta = base.revise_whole(before, current["feedback"], current["closure"], strong=True)
        elif strategy == "oracle_closure_splice":
            selected = current["closure"]
            report, edit_meta = base.revise_splice(before, current["feedback"], selected)
        elif strategy == "auto_closure_splice":
            selected, plan_meta = plan_closure(before, current["feedback"])
            report, edit_meta = base.revise_splice(before, current["feedback"], selected) if selected else (before, {"parse_error": "empty_selection", "seconds": 0, "eval_count": 0})
        else:
            raise ValueError(strategy)
        turns.append({
            "turn": turn,
            "feedback": current["feedback"],
            "score": score(before, report, c, turn, selected),
            "plan_meta": plan_meta,
            "edit_meta": edit_meta,
            "report": report,
        })
    return {"case_id": c.case_id, "strategy": strategy, "initial_report": render_initial(c), "turns": turns}


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for strategy in ["whole", "strong_whole", "oracle_closure_splice", "auto_closure_splice"]:
        chosen = [item for item in runs if item["strategy"] == strategy]
        if not chosen:
            continue
        turns = [turn for item in chosen for turn in item["turns"]]
        scores = [turn["score"] for turn in turns]
        all_meta = [turn["edit_meta"] for turn in turns] + [turn["plan_meta"] for turn in turns if turn["plan_meta"]]
        selection_scores = [score for score in scores if score["selection_recall"] is not None]
        result[strategy] = {
            "turn_count": len(turns),
            "dependencies_ok": sum(score["dependencies_ok"] for score in scores),
            "outside_exact": sum(score["outside_exact"] for score in scores),
            "full_success": sum(score["full_success"] for score in scores),
            "turn2_history_ok": sum(item["turns"][1]["score"]["history_ok"] for item in chosen),
            "mean_selection_precision": sum(score["selection_precision"] for score in selection_scores) / len(selection_scores) if selection_scores else None,
            "mean_selection_recall": sum(score["selection_recall"] for score in selection_scores) / len(selection_scores) if selection_scores else None,
            "parse_errors": sum(bool(meta.get("parse_error")) for meta in all_meta),
            "total_seconds": sum(meta.get("seconds", 0) for meta in all_meta),
            "total_eval_tokens": sum(meta.get("eval_count") or 0 for meta in all_meta),
        }
    return result


def main() -> None:
    strategies = ["whole", "strong_whole", "oracle_closure_splice", "auto_closure_splice"]
    runs = []
    for c in CASES:
        for strategy in strategies:
            print(f"running {c.case_id} {strategy}", flush=True)
            runs.append(run(c, strategy))
            OUT.write_text(json.dumps({"model": base.MODEL, "runs": runs, "summary": summarize(runs)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    payload = {"model": base.MODEL, "case_count": len(CASES), "runs": runs, "summary": summarize(runs)}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
