from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import random
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


METHODS = (
    "rtca",
    "schema_only",
    "dependency_only",
    "temporal_unit_only",
    "literal_only",
    "size_only",
    "unweighted_union",
)
WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}
MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}
UNIT_ALIASES = {
    "meter": "meter",
    "meters": "meter",
    "metre": "meter",
    "metres": "meter",
    "feet": "foot",
    "foot": "foot",
    "ft": "foot",
    "inch": "inch",
    "inches": "inch",
    "celsius": "celsius",
    "fahrenheit": "fahrenheit",
    "kilometer": "kilometer",
    "kilometers": "kilometer",
    "mile": "mile",
    "miles": "mile",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def question_text(row: dict[str, Any]) -> str:
    texts: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("content"), str):
                texts.append(value["content"])
            else:
                for child in value.values():
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(row.get("question", []))
    return "\n".join(texts)


def function_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return function_name(node.value) + "." + node.attr
    return ""


def parse_call_string(text: str) -> tuple[str, dict[str, Any]] | None:
    try:
        node = ast.parse(text, mode="eval").body
    except (SyntaxError, ValueError):
        return None
    if not isinstance(node, ast.Call):
        return None
    kwargs: dict[str, Any] = {}
    for keyword in node.keywords:
        if keyword.arg is None:
            continue
        try:
            kwargs[keyword.arg] = ast.literal_eval(keyword.value)
        except (ValueError, TypeError):
            kwargs[keyword.arg] = None
    return function_name(node.func), kwargs


def reference_calls(reference: Any) -> list[tuple[str, dict[str, Any]]]:
    calls: list[tuple[str, dict[str, Any]]] = []

    def visit(value: Any) -> None:
        if isinstance(value, str):
            parsed = parse_call_string(value)
            if parsed:
                calls.append(parsed)
        elif isinstance(value, dict):
            for name, params in value.items():
                if isinstance(params, dict):
                    calls.append((str(name), params))
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(reference)
    return calls


def unwrap_alternative(value: Any) -> Any:
    if isinstance(value, list) and len(value) == 1:
        return unwrap_alternative(value[0])
    return value


def schema_reference_violations(
    row: dict[str, Any], calls: list[tuple[str, dict[str, Any]]]
) -> int:
    functions = {
        item.get("name"): item
        for item in row.get("function", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    if not functions:
        return 0

    def compare(params: dict[str, Any], schema: dict[str, Any]) -> int:
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            properties = {}
        errors = 0
        for key, original in params.items():
            if key not in properties:
                errors += 1
                continue
            value = unwrap_alternative(original)
            child_schema = properties[key]
            if isinstance(value, dict) and isinstance(child_schema, dict):
                errors += compare(value, child_schema)
            elif (
                isinstance(value, list)
                and value
                and isinstance(value[0], dict)
                and isinstance(child_schema, dict)
            ):
                nested = child_schema.get("items", child_schema)
                for child in value:
                    errors += compare(child, nested if isinstance(nested, dict) else {})
        return errors

    errors = 0
    for name, params in calls:
        if name not in functions:
            errors += 1
            continue
        schema = functions[name].get("parameters", {})
        if isinstance(schema, dict):
            errors += compare(params, schema)
    return errors


def flatten_scalars(value: Any) -> list[Any]:
    values: list[Any] = []
    if isinstance(value, dict):
        for child in value.values():
            values.extend(flatten_scalars(child))
    elif isinstance(value, list):
        for child in value:
            values.extend(flatten_scalars(child))
    else:
        values.append(value)
    return values


def levenshtein_one(left: str, right: str) -> bool:
    if left == right or abs(len(left) - len(right)) > 1:
        return False
    if len(left) > len(right):
        left, right = right, left
    i = j = differences = 0
    while i < len(left) and j < len(right):
        if left[i] == right[j]:
            i += 1
            j += 1
        else:
            differences += 1
            if differences > 1:
                return False
            if len(left) == len(right):
                i += 1
            j += 1
    differences += len(right) - j
    return differences == 1


def path_dependency_violations(calls: list[tuple[str, dict[str, Any]]]) -> int:
    paths: list[str] = []
    for _, params in calls:
        for value in flatten_scalars(params):
            if isinstance(value, str) and re.search(r"\.[A-Za-z0-9]{1,5}\.?$", value):
                paths.append(value)
    return sum(
        1
        for index, left in enumerate(paths)
        for right in paths[index + 1 :]
        if levenshtein_one(left, right)
    )


def units(text: str) -> set[str]:
    found: set[str] = set()
    for token in re.findall(r"[A-Za-z]+", text.lower()):
        if token in UNIT_ALIASES:
            found.add(UNIT_ALIASES[token])
    return found


def schema_text(row: dict[str, Any]) -> str:
    chunks: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, str):
            chunks.append(value)
        elif isinstance(value, dict):
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(row.get("function", []))
    return "\n".join(chunks)


def unit_contract_violations(row: dict[str, Any], text: str) -> int:
    query_units = units(text)
    contract_units = units(schema_text(row))
    if not query_units or not contract_units:
        return 0
    return len(query_units - contract_units)


def calendar_contract_violations(text: str) -> int:
    lower = text.lower()
    pattern = re.compile(
        r"\b(" + "|".join(WEEKDAYS) + r")\b[^.\n]{0,40}\b("
        + "|".join(MONTHS)
        + r")\s+(\d{1,2})(?:st|nd|rd|th)?[,]?\s+(\d{4})\b"
    )
    errors = 0
    for weekday, month, day, year in pattern.findall(lower):
        try:
            actual = datetime(int(year), MONTHS[month], int(day)).weekday()
        except ValueError:
            errors += 1
            continue
        if actual != WEEKDAYS[weekday]:
            errors += 1
    return errors


def normalize_space(text: str) -> str:
    return " ".join(text.lower().split())


def literal_provenance_violations(
    text: str, calls: list[tuple[str, dict[str, Any]]]
) -> int:
    normalized = normalize_space(text)
    errors = 0
    seen_derived = False
    for name, params in calls:
        lowered_name = name.lower()
        if any(token in lowered_name for token in ("compute", "convert", "mean", "calculate")):
            seen_derived = True
        for value in flatten_scalars(params):
            if isinstance(value, str):
                candidate = normalize_space(value)
                if (
                    len(candidate) >= 20
                    and not re.search(r"\.[A-Za-z0-9]{1,5}\.?$", candidate)
                    and candidate not in normalized
                ):
                    errors += 1
            elif isinstance(value, float) and not value.is_integer():
                rendered = f"{value:.12g}"
                if rendered not in normalized and not seen_derived:
                    errors += 1
    return errors


def score_entry(
    row: dict[str, Any],
    reference: Any,
    duplicate_count: int,
    weights: dict[str, float],
) -> tuple[dict[str, int], dict[str, float]]:
    text = question_text(row)
    calls = reference_calls(reference)
    channels = {
        "schema_reference": schema_reference_violations(row, calls),
        "path_dependency": path_dependency_violations(calls),
        "unit_contract": unit_contract_violations(row, text),
        "calendar_contract": calendar_contract_violations(text),
        "literal_provenance": literal_provenance_violations(text, calls),
        "identity_integrity": max(0, duplicate_count - 1),
    }
    scores = {
        "rtca": sum(weights[name] * value for name, value in channels.items()),
        "schema_only": float(channels["schema_reference"]),
        "dependency_only": float(channels["path_dependency"]),
        "temporal_unit_only": float(
            channels["unit_contract"] + channels["calendar_contract"]
        ),
        "literal_only": float(channels["literal_provenance"]),
        "size_only": float(len(json.dumps(row, ensure_ascii=False).encode("utf-8"))),
        "unweighted_union": float(sum(value > 0 for value in channels.values())),
    }
    return channels, scores


def rank_rows(pr: int, rows: list[dict[str, Any]], method: str) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda item: (
            -item["scores"][method],
            hashlib.sha256(f"{pr}||{item['id']}".encode()).hexdigest(),
        ),
    )


def average_precision(ranked: list[dict[str, Any]]) -> float:
    positives = sum(item["label"] for item in ranked)
    if positives == 0:
        return 0.0
    hits = 0
    total = 0.0
    for rank, item in enumerate(ranked, 1):
        if item["label"]:
            hits += 1
            total += hits / rank
    return total / positives


def bootstrap_lower(
    candidate: list[float], comparator: list[float], seed: int, resamples: int
) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(candidate)
    values = []
    for _ in range(resamples):
        indices = [rng.randrange(n) for _ in range(n)]
        values.append(
            sum(candidate[i] - comparator[i] for i in indices) / n
        )
    values.sort()
    return values[math.floor(0.025 * resamples)], values[math.floor(0.975 * resamples)]


def evaluate(
    config: dict[str, Any], source_root: Path
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    all_raw: list[dict[str, Any]] = []
    per_method: dict[str, list[dict[str, float]]] = {method: [] for method in METHODS}
    total_labels = 0
    for record in config["records"]:
        pr = int(record["pr"])
        query_path = source_root / record["query_file"]
        if sha256(query_path) != record["query_sha256"]:
            raise ValueError(f"query SHA mismatch for PR {pr}")
        query_rows = load_jsonl(query_path)
        answers: dict[str, Any] = {}
        if record["answer_file"]:
            answer_path = source_root / record["answer_file"]
            if sha256(answer_path) != record["answer_sha256"]:
                raise ValueError(f"answer SHA mismatch for PR {pr}")
            answers = {item["id"]: item.get("ground_truth") for item in load_jsonl(answer_path)}
        ids = [item["id"] for item in query_rows]
        counts = Counter(ids)
        labels = set(record["changed_ids"])
        if not labels.issubset(set(ids)):
            raise ValueError(f"missing changed IDs in PR {pr}")
        rows: list[dict[str, Any]] = []
        for row in query_rows:
            reference = answers.get(row["id"], row.get("ground_truth", []))
            channels, scores = score_entry(
                row, reference, counts[row["id"]], config["weights"]
            )
            rows.append(
                {
                    "pr": pr,
                    "id": row["id"],
                    "label": int(row["id"] in labels),
                    "channels": channels,
                    "scores": scores,
                    "question_sha256": hashlib.sha256(
                        question_text(row).encode("utf-8")
                    ).hexdigest(),
                    "reference_sha256": hashlib.sha256(
                        json.dumps(reference, ensure_ascii=False, sort_keys=True).encode(
                            "utf-8"
                        )
                    ).hexdigest(),
                }
            )
        total_labels += len(labels)
        for method in METHODS:
            ranked = rank_rows(pr, rows, method)
            for rank, item in enumerate(ranked, 1):
                item.setdefault("ranks", {})[method] = rank
            positive_ranks = [item["ranks"][method] for item in rows if item["label"]]
            per_method[method].append(
                {
                    "pr": pr,
                    "rr": 1.0 / min(positive_ranks),
                    "ap": average_precision(ranked),
                    "hits_at_10": float(sum(rank <= 10 for rank in positive_ranks)),
                    "positives": float(len(positive_ranks)),
                }
            )
        all_raw.extend(sorted(rows, key=lambda item: item["id"]))

    metrics: dict[str, dict[str, float]] = {}
    for method, records in per_method.items():
        metrics[method] = {
            "mrr": sum(item["rr"] for item in records) / len(records),
            "map": sum(item["ap"] for item in records) / len(records),
            "recall_at_10": sum(item["hits_at_10"] for item in records) / total_labels,
            "top10_prs": float(sum(item["hits_at_10"] > 0 for item in records)),
        }
    comparators = [method for method in METHODS if method != "rtca"]
    strongest = max(comparators, key=lambda method: (metrics[method]["mrr"], method))
    candidate_rr = [item["rr"] for item in per_method["rtca"]]
    comparator_rr = [item["rr"] for item in per_method[strongest]]
    interval = bootstrap_lower(
        candidate_rr,
        comparator_rr,
        int(config["bootstrap_seed"]),
        int(config["bootstrap_resamples"]),
    )
    identical = []
    for method in comparators:
        if all(
            [item["id"] for item in rank_rows(pr, [row for row in all_raw if row["pr"] == pr], "rtca")]
            == [item["id"] for item in rank_rows(pr, [row for row in all_raw if row["pr"] == pr], method)]
            for pr in config["evaluation_prs"]
        ):
            identical.append(method)

    gates_cfg = config["gates"]
    gates = {
        "pr_count": len(config["records"]) == gates_cfg["expected_prs"],
        "changed_id_count": (
            total_labels == gates_cfg["expected_changed_ids"]
            if "expected_changed_ids" in gates_cfg
            else total_labels > 0
        ),
        "candidate_mrr": metrics["rtca"]["mrr"] >= gates_cfg["minimum_mrr"],
        "candidate_recall_at_10": metrics["rtca"]["recall_at_10"]
        >= gates_cfg["minimum_recall_at_10"],
        "mrr_delta": metrics["rtca"]["mrr"] - metrics[strongest]["mrr"]
        >= gates_cfg["minimum_mrr_delta"],
        "bootstrap_lower": interval[0] > gates_cfg["minimum_bootstrap_lower"],
        "top10_prs": metrics["rtca"]["top10_prs"] >= gates_cfg["minimum_top10_prs"],
        "ranking_nonidentity": not identical,
    }
    summary = {
        "phase": config["phase"],
        "candidate": config["candidate"],
        "prs": config["evaluation_prs"],
        "entries": len(all_raw),
        "changed_ids": total_labels,
        "metrics": metrics,
        "strongest_comparator": strongest,
        "mrr_delta": metrics["rtca"]["mrr"] - metrics[strongest]["mrr"],
        "mrr_delta_bootstrap_95": list(interval),
        "identical_comparators": identical,
        "per_pr": per_method,
        "gates": gates,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
        "all_gates_passed": all(gates.values()),
    }
    return all_raw, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    raw, summary = evaluate(config, args.source_root)
    args.output_dir.mkdir()
    raw_path = args.output_dir / "raw.jsonl"
    raw_path.write_text(
        "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in raw),
        encoding="utf-8",
        newline="\n",
    )
    summary["config_sha256"] = sha256(args.config)
    summary["raw_sha256"] = sha256(raw_path)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "candidate_mrr": summary["metrics"]["rtca"]["mrr"],
                "gates": f"{summary['gates_passed']}/{summary['gates_total']}",
                "phase": summary["phase"],
                "strongest_comparator": summary["strongest_comparator"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
