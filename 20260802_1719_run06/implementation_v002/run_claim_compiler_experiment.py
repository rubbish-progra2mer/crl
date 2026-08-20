from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
FIELDS = (
    "quantifier",
    "predicate",
    "asserted_value",
    "entity_scope",
    "time_scope",
    "archive_scope",
)
ALLOWED = {
    "quantifier": {"exists", "forall"},
    "predicate": {"matches_target", "compliant"},
    "asserted_value": {True, False},
    "entity_scope": {"current_team", "current_permission", "organization"},
    "time_scope": {"recent", "all_history"},
    "archive_scope": {"active_only", "include_archived"},
}
SCOPE_RANK = {
    "entity_scope": {"current_team": 1, "current_permission": 2, "organization": 3},
    "time_scope": {"recent": 1, "all_history": 2},
    "archive_scope": {"active_only": 1, "include_archived": 2},
}


def call_model(model: str, text: str, seed: int) -> tuple[dict[str, Any], dict[str, Any], str]:
    system = (
        "你是受限的主张编译器。把句子编译成 JSON，且只能输出 JSON。字段必须是："
        "quantifier=exists|forall；predicate=matches_target|compliant；"
        "asserted_value=true|false；entity_scope=current_team|current_permission|organization；"
        "time_scope=recent|all_history；archive_scope=active_only|include_archived。"
        "不存在/没有目标仍使用 quantifier=exists、asserted_value=false；"
        "不是所有记录合规/存在不合规反例使用 quantifier=forall、asserted_value=false。"
    )
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        "stream": False,
        "format": "json",
        "think": False,
        "keep_alive": "30m",
        "options": {"temperature": 0, "seed": seed, "num_predict": 160},
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = json.loads(response.read().decode("utf-8"))
    content = str(raw.get("message", {}).get("content", ""))
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {}
    usage = {
        "prompt_eval_count": raw.get("prompt_eval_count") or 0,
        "eval_count": raw.get("eval_count") or 0,
        "total_duration": raw.get("total_duration") or 0,
        "response_model": raw.get("model"),
    }
    return parsed if isinstance(parsed, dict) else {}, usage, content


def normalized_prediction(parsed: dict[str, Any]) -> dict[str, Any] | None:
    prediction = {field: parsed.get(field) for field in FIELDS}
    if prediction["asserted_value"] == "true":
        prediction["asserted_value"] = True
    elif prediction["asserted_value"] == "false":
        prediction["asserted_value"] = False
    for field, value in prediction.items():
        if value not in ALLOWED[field]:
            return None
    return prediction


def dangerous_underapproximation(label: dict[str, Any], prediction: dict[str, Any] | None) -> bool:
    if prediction is None:
        return False
    if prediction["quantifier"] != label["quantifier"]:
        return True
    if prediction["predicate"] != label["predicate"]:
        return True
    if prediction["asserted_value"] != label["asserted_value"]:
        return True
    return any(
        SCOPE_RANK[field][prediction[field]] < SCOPE_RANK[field][label[field]]
        for field in SCOPE_RANK
    )


def fail_closed_guard(text: str, prediction: dict[str, Any] | None) -> tuple[bool, list[str]]:
    if prediction is None:
        return False, ["malformed_or_out_of_vocabulary"]
    lower = text.lower()
    requirements = []
    if any(token in lower for token in ("整个组织", "全组织", "organization-wide", "entire organization", "across the organization")):
        requirements.append(("entity_scope", "organization", "explicit_organization_scope"))
    if any(token in lower for token in ("当前权限", "可访问", "我能访问", "我可见", "currently permitted", "current permission", "my visible")):
        requirements.append(("entity_scope", "current_permission", "explicit_permission_scope"))
    if any(token in lower for token in ("全部历史", "全历史", "complete history", "full history", "across all history", "never")):
        requirements.append(("time_scope", "all_history", "explicit_all_history"))
    if any(token in lower for token in ("包括归档", "含归档", "归档和活动", "archive included", "archived records included", "including archived")):
        requirements.append(("archive_scope", "include_archived", "explicit_archive_inclusion"))
    reasons = [reason for field, expected, reason in requirements if prediction[field] != expected]
    return not reasons, reasons


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    accepted = [row for row in rows if row["guard_accept"]]
    return {
        "cases": total,
        "parse_success_rate": sum(row["prediction"] is not None for row in rows) / total,
        "exact_match_rate": sum(row["exact_match"] for row in rows) / total,
        "raw_dangerous_underapproximation_rate": sum(row["dangerous_underapproximation"] for row in rows) / total,
        "guard_accept_rate": len(accepted) / total,
        "guarded_exact_match_rate_over_all_cases": sum(row["guard_accept"] and row["exact_match"] for row in rows) / total,
        "guarded_dangerous_commit_rate_over_all_cases": sum(row["guard_accept"] and row["dangerous_underapproximation"] for row in rows) / total,
        "accepted_exact_match_rate": (
            sum(row["exact_match"] for row in accepted) / len(accepted) if accepted else None
        ),
        "prompt_tokens": sum(row["usage"]["prompt_eval_count"] for row in rows),
        "generated_tokens": sum(row["usage"]["eval_count"] for row in rows),
    }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    if args.limit is not None:
        cases = cases[: args.limit]
    started = time.time()
    rows = []
    for index, case in enumerate(cases):
        parsed, usage, raw_content = call_model(args.model, case["text"], args.seed + index)
        prediction = normalized_prediction(parsed)
        label = case["label"]
        dangerous = dangerous_underapproximation(label, prediction)
        guard_accept, guard_reasons = fail_closed_guard(case["text"], prediction)
        row = {
            "case_id": case["case_id"],
            "text": case["text"],
            "label": label,
            "prediction": prediction,
            "raw_content": raw_content,
            "exact_match": prediction == label,
            "dangerous_underapproximation": dangerous,
            "guard_accept": guard_accept,
            "guard_reasons": guard_reasons,
            "usage": usage,
        }
        rows.append(row)
        print(
            json.dumps(
                {
                    "case_id": case["case_id"],
                    "exact": row["exact_match"],
                    "dangerous": dangerous,
                    "guard_accept": guard_accept,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    document = {
        "experiment": "claim_compiler_v002",
        "model": args.model,
        "seed": args.seed,
        "case_count": len(rows),
        "elapsed_seconds": time.time() - started,
        "dataset_kind": "researcher-authored bilingual audit set; not an external benchmark or human annotation study",
        "summary": summarize(rows),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"output": str(args.output), "summary": document["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
