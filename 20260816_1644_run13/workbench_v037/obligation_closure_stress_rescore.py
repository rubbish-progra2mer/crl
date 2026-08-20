from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import obligation_closure_revision_pilot as base
import obligation_closure_stress as stress


SOURCE = Path(__file__).with_name("obligation_closure_stress_qwen2_5_7b.json")
OUT = Path(__file__).with_name("obligation_closure_stress_semantic_rescore.json")
base.SECTION_ORDER = stress.ORDER


def has(text: str, term: str) -> bool:
    return term.lower() in text.lower()


def has_number(text: str, number: str) -> bool:
    return re.search(rf"(?<![\d.]){re.escape(number)}(?![\d.])", text) is not None


def relation_requirements(relation: str) -> tuple[list[str], list[str]]:
    numbers = re.findall(r"\d+(?:\.\d+)?%?", relation)
    if "above" in relation:
        directions = ["above", "exceed", "over", "higher"]
    else:
        directions = ["below", "under", "lower"]
    return numbers, directions


def relation_ok(text: str, relation: str) -> bool:
    numbers, directions = relation_requirements(relation)
    return all(has_number(text, number) for number in numbers) and any(has(text, word) for word in directions)


def action_ok(text: str, action: str) -> bool:
    return all(has(text, word) for word in action.split())


def expected_sections(c: stress.StressCase, turn: int, sections: dict[str, str]) -> dict[str, bool]:
    if turn == 1:
        return {
            "SUMMARY": has_number(sections.get("SUMMARY", ""), c.alpha_new)
            and has(sections.get("SUMMARY", ""), c.alpha_new_cite)
            and relation_ok(sections.get("SUMMARY", ""), c.alpha_new_relation)
            and action_ok(sections.get("SUMMARY", ""), c.alpha_new_decision),
            "ALPHA_FINDING": has_number(sections.get("ALPHA_FINDING", ""), c.alpha_new)
            and has(sections.get("ALPHA_FINDING", ""), c.alpha_new_cite),
            "ALPHA_COMPARISON": relation_ok(sections.get("ALPHA_COMPARISON", ""), c.alpha_new_relation)
            and has(sections.get("ALPHA_COMPARISON", ""), c.alpha_new_cite),
            "ALPHA_DECISION": action_ok(sections.get("ALPHA_DECISION", ""), c.alpha_new_decision)
            and has(sections.get("ALPHA_DECISION", ""), c.alpha_new_cite),
            "SOURCES": has_number(sections.get("SOURCES", ""), c.alpha_new)
            and has(sections.get("SOURCES", ""), c.alpha_new_cite),
        }
    return {
        "SUMMARY": has_number(sections.get("SUMMARY", ""), c.beta_new.rstrip("%"))
        and has(sections.get("SUMMARY", ""), c.beta_new)
        and has(sections.get("SUMMARY", ""), c.beta_new_cite)
        and relation_ok(sections.get("SUMMARY", ""), c.beta_new_relation)
        and action_ok(sections.get("SUMMARY", ""), c.beta_new_decision),
        "BETA_FINDING": has(sections.get("BETA_FINDING", ""), c.beta_new)
        and has(sections.get("BETA_FINDING", ""), c.beta_new_cite),
        "BETA_COMPARISON": relation_ok(sections.get("BETA_COMPARISON", ""), c.beta_new_relation)
        and has(sections.get("BETA_COMPARISON", ""), c.beta_new_cite),
        "BETA_DECISION": action_ok(sections.get("BETA_DECISION", ""), c.beta_new_decision)
        and has(sections.get("BETA_DECISION", ""), c.beta_new_cite),
        "SOURCES": has(sections.get("SOURCES", ""), c.beta_new)
        and has(sections.get("SOURCES", ""), c.beta_new_cite),
    }


def alpha_history_ok(c: stress.StressCase, sections: dict[str, str]) -> bool:
    checks = expected_sections(c, 1, sections)
    return all(checks.values())


def old_tokens_absent(c: stress.StressCase, turn: int, sections: dict[str, str]) -> bool:
    closure = stress.spec(c, turn)["closure"]
    text = "\n".join(sections.get(name, "") for name in closure)
    if turn == 1:
        return not has_number(text, c.alpha_old) and not has(text, c.alpha_old_cite) and not action_ok(text, c.alpha_old_decision)
    return not has(text, c.beta_old) and not has(text, c.beta_old_cite) and not action_ok(text, c.beta_old_decision)


def rescore_turn(before: str, after: str, c: stress.StressCase, turn: int, selected: list[str] | None) -> dict[str, Any]:
    before_sections = base.parse_sections(before)
    after_sections = base.parse_sections(after)
    closure = stress.spec(c, turn)["closure"]
    outside = [name for name in stress.ORDER if name not in closure]
    section_checks = expected_sections(c, turn, after_sections)
    dependencies_ok = all(section_checks.values()) and old_tokens_absent(c, turn, after_sections)
    outside_by_section = {name: before_sections.get(name) == after_sections.get(name) for name in outside}
    outside_exact = all(outside_by_section.values())
    history_ok = True if turn == 1 else alpha_history_ok(c, after_sections)
    structure_ok = list(after_sections) == stress.ORDER
    precision = None
    recall = None
    if selected is not None:
        intersection = len(set(selected) & set(closure))
        precision = intersection / len(set(selected)) if selected else 0.0
        recall = intersection / len(set(closure))
    return {
        "structure_ok": structure_ok,
        "dependencies_ok": dependencies_ok,
        "expected_by_section": section_checks,
        "old_tokens_absent": old_tokens_absent(c, turn, after_sections),
        "outside_exact": outside_exact,
        "outside_by_section": outside_by_section,
        "history_ok": history_ok,
        "full_success": structure_ok and dependencies_ok and outside_exact and history_ok,
        "selected": selected,
        "selection_precision": precision,
        "selection_recall": recall,
    }


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for strategy in ["whole", "strong_whole", "oracle_closure_splice", "auto_closure_splice"]:
        chosen = [run for run in runs if run["strategy"] == strategy]
        turns = [turn for run in chosen for turn in run["turns"]]
        scores = [turn["semantic_score"] for turn in turns]
        selection = [score for score in scores if score["selection_recall"] is not None]
        result[strategy] = {
            "turn_count": len(scores),
            "dependencies_ok": sum(score["dependencies_ok"] for score in scores),
            "outside_exact": sum(score["outside_exact"] for score in scores),
            "full_success": sum(score["full_success"] for score in scores),
            "turn2_history_ok": sum(run["turns"][1]["semantic_score"]["history_ok"] for run in chosen),
            "mean_selection_precision": sum(score["selection_precision"] for score in selection) / len(selection) if selection else None,
            "mean_selection_recall": sum(score["selection_recall"] for score in selection) / len(selection) if selection else None,
        }
    return result


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    case_by_id = {case.case_id: case for case in stress.CASES}
    rescored_runs = []
    for run in payload["runs"]:
        case = case_by_id[run["case_id"]]
        before = run["initial_report"]
        turns = []
        for turn in run["turns"]:
            selected = turn["score"].get("selected")
            semantic_score = rescore_turn(before, turn["report"], case, turn["turn"], selected)
            turns.append({"turn": turn["turn"], "semantic_score": semantic_score})
            before = turn["report"]
        rescored_runs.append({"case_id": run["case_id"], "strategy": run["strategy"], "turns": turns})
    result = {
        "source": SOURCE.name,
        "scoring_note": "独立语义重评分；保留原始结果，不重新调用模型。关系允许 above/exceed/over/higher 与 below/under/lower 等等价方向表达。",
        "runs": rescored_runs,
        "summary": summarize(rescored_runs),
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
