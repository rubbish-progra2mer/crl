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


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


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
                    errors += compare(
                        child, nested if isinstance(nested, dict) else {}
                    )
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
            if isinstance(value, str) and re.search(
                r"\.[A-Za-z0-9]{1,5}\.?$", value
            ):
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
        r"\b("
        + "|".join(WEEKDAYS)
        + r")\b[^.\n]{0,40}\b("
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
        if any(
            token in lowered_name
            for token in ("compute", "convert", "mean", "calculate")
        ):
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


def feature_row(
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


def removed_ids(files: list[dict[str, Any]]) -> list[str]:
    labels: list[str] = []
    for item in files:
        if "/data/" not in str(item["filename"]) or "CHANGELOG" in str(
            item["filename"]
        ):
            continue
        for line in str(item.get("patch", "")).splitlines():
            if not line.startswith("-") or line.startswith("---"):
                continue
            try:
                value = json.loads(line[1:])
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict) and isinstance(value.get("id"), str):
                labels.append(value["id"])
    return sorted(set(labels))


def order(pr: int, rows: list[dict[str, Any]], method: str) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            -float(row["scores"][method]),
            hashlib.sha256(f"{pr}||{row['id']}".encode()).hexdigest(),
        ),
    )


def average_precision(ranked: list[dict[str, Any]]) -> float:
    positives = sum(int(row["label"]) for row in ranked)
    hits = 0
    total = 0.0
    for index, row in enumerate(ranked, 1):
        if row["label"]:
            hits += 1
            total += hits / index
    return total / positives


def interval(
    candidate: list[float], comparator: list[float], seed: int, count: int
) -> list[float]:
    generator = random.Random(seed)
    n = len(candidate)
    deltas = []
    for _ in range(count):
        sample = [generator.randrange(n) for _ in range(n)]
        deltas.append(sum(candidate[i] - comparator[i] for i in sample) / n)
    deltas.sort()
    return [
        deltas[math.floor(0.025 * count)],
        deltas[math.floor(0.975 * count)],
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    raw = [
        json.loads(line)
        for line in args.raw.read_text(encoding="utf-8").splitlines()
    ]
    primary = json.loads(args.summary.read_text(encoding="utf-8"))

    errors: list[str] = []
    if primary["raw_sha256"] != file_sha(args.raw):
        errors.append("raw_sha_mismatch")
    if primary["config_sha256"] != file_sha(args.config):
        errors.append("config_sha_mismatch")

    expected_by_pr: dict[int, list[dict[str, Any]]] = {}
    source_files_verified = 0
    total_labels = 0
    for record in config["records"]:
        pr = int(record["pr"])
        meta_path = args.source_root / record["metadata_file"]
        files_path = args.source_root / record["files_file"]
        query_path = args.source_root / record["query_file"]
        for path, expected in (
            (meta_path, record["metadata_sha256"]),
            (files_path, record["files_sha256"]),
            (query_path, record["query_sha256"]),
        ):
            if file_sha(path) != expected:
                errors.append(f"source_sha_mismatch_pr_{pr}_{path.name}")
            source_files_verified += 1
        meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
        files = json.loads(files_path.read_text(encoding="utf-8-sig"))
        if not meta["merged"] or meta["base"]["sha"] != record["base_sha"]:
            errors.append(f"metadata_mismatch_pr_{pr}")
        labels = set(removed_ids(files))
        if labels != set(record["changed_ids"]):
            errors.append(f"patch_label_mismatch_pr_{pr}")

        answers: dict[str, Any] = {}
        if record["answer_file"]:
            answer_path = args.source_root / record["answer_file"]
            if file_sha(answer_path) != record["answer_sha256"]:
                errors.append(f"source_sha_mismatch_pr_{pr}_{answer_path.name}")
            source_files_verified += 1
            answers = {
                row["id"]: row.get("ground_truth") for row in load_jsonl(answer_path)
            }
        query_rows = load_jsonl(query_path)
        counts = Counter(row["id"] for row in query_rows)
        if not labels.issubset(counts):
            errors.append(f"missing_changed_id_pr_{pr}")
        expected_rows: list[dict[str, Any]] = []
        for row in query_rows:
            reference = answers.get(row["id"], row.get("ground_truth", []))
            channels, scores = feature_row(
                row, reference, counts[row["id"]], config["weights"]
            )
            expected_rows.append(
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
                        json.dumps(
                            reference, ensure_ascii=False, sort_keys=True
                        ).encode("utf-8")
                    ).hexdigest(),
                }
            )
        for method in METHODS:
            for rank, row in enumerate(order(pr, expected_rows, method), 1):
                row.setdefault("ranks", {})[method] = rank
        expected_by_pr[pr] = sorted(expected_rows, key=lambda row: row["id"])
        total_labels += len(labels)

    raw_by_pr = {
        pr: sorted(
            [row for row in raw if int(row["pr"]) == pr],
            key=lambda row: row["id"],
        )
        for pr in expected_by_pr
    }
    maximum_channel_error = 0
    maximum_score_error = 0.0
    maximum_rank_error = 0
    source_feature_rows = 0
    for pr, expected_rows in expected_by_pr.items():
        actual_rows = raw_by_pr[pr]
        if len(actual_rows) != len(expected_rows):
            errors.append(f"row_count_mismatch_pr_{pr}")
            continue
        for expected, actual in zip(expected_rows, actual_rows):
            if (
                expected["id"] != actual["id"]
                or expected["pr"] != actual["pr"]
                or expected["label"] != actual["label"]
                or expected["question_sha256"] != actual["question_sha256"]
                or expected["reference_sha256"] != actual["reference_sha256"]
            ):
                errors.append(f"row_identity_mismatch_pr_{pr}_{expected['id']}")
            for channel, value in expected["channels"].items():
                maximum_channel_error = max(
                    maximum_channel_error,
                    abs(int(value) - int(actual["channels"][channel])),
                )
            for method, value in expected["scores"].items():
                maximum_score_error = max(
                    maximum_score_error,
                    abs(float(value) - float(actual["scores"][method])),
                )
                maximum_rank_error = max(
                    maximum_rank_error,
                    abs(
                        int(expected["ranks"][method])
                        - int(actual["ranks"][method])
                    ),
                )
            source_feature_rows += 1
    if len(raw) != sum(len(rows) for rows in expected_by_pr.values()):
        errors.append("raw_total_row_count_mismatch")
    if maximum_channel_error:
        errors.append("channel_mismatch")
    if maximum_score_error > 1e-15:
        errors.append("score_mismatch")
    if maximum_rank_error:
        errors.append("rank_mismatch")

    replay: dict[str, dict[str, float]] = {}
    rr_lists: dict[str, list[float]] = {}
    for method in METHODS:
        rrs = []
        aps = []
        hits = 0
        top10_prs = 0
        for pr, rows in expected_by_pr.items():
            ranked = order(pr, rows, method)
            ranks = {row["id"]: index for index, row in enumerate(ranked, 1)}
            positive_ranks = [ranks[row["id"]] for row in rows if row["label"]]
            rrs.append(1.0 / min(positive_ranks))
            aps.append(average_precision(ranked))
            local_hits = sum(value <= 10 for value in positive_ranks)
            hits += local_hits
            top10_prs += int(local_hits > 0)
        rr_lists[method] = rrs
        replay[method] = {
            "mrr": sum(rrs) / len(rrs),
            "map": sum(aps) / len(aps),
            "recall_at_10": hits / total_labels,
            "top10_prs": float(top10_prs),
        }

    maximum_metric_error = 0.0
    for method in METHODS:
        for metric, value in replay[method].items():
            maximum_metric_error = max(
                maximum_metric_error,
                abs(value - float(primary["metrics"][method][metric])),
            )
    strongest = max(
        [method for method in METHODS if method != "rtca"],
        key=lambda method: (replay[method]["mrr"], method),
    )
    boot = interval(
        rr_lists["rtca"],
        rr_lists[strongest],
        int(config["bootstrap_seed"]),
        int(config["bootstrap_resamples"]),
    )
    maximum_metric_error = max(
        maximum_metric_error,
        abs(
            (replay["rtca"]["mrr"] - replay[strongest]["mrr"])
            - primary["mrr_delta"]
        ),
        abs(boot[0] - primary["mrr_delta_bootstrap_95"][0]),
        abs(boot[1] - primary["mrr_delta_bootstrap_95"][1]),
    )
    if strongest != primary["strongest_comparator"]:
        errors.append("strongest_comparator_mismatch")
    if maximum_metric_error > 1e-15:
        errors.append("metric_mismatch")

    identical = []
    for method in METHODS:
        if method == "rtca":
            continue
        if all(
            [row["id"] for row in order(pr, rows, "rtca")]
            == [row["id"] for row in order(pr, rows, method)]
            for pr, rows in expected_by_pr.items()
        ):
            identical.append(method)
    gate_config = config["gates"]
    replayed_gates = {
        "pr_count": len(config["records"]) == gate_config["expected_prs"],
        "changed_id_count": (
            total_labels == gate_config["expected_changed_ids"]
            if "expected_changed_ids" in gate_config
            else total_labels > 0
        ),
        "candidate_mrr": replay["rtca"]["mrr"]
        >= gate_config["minimum_mrr"],
        "candidate_recall_at_10": replay["rtca"]["recall_at_10"]
        >= gate_config["minimum_recall_at_10"],
        "mrr_delta": replay["rtca"]["mrr"] - replay[strongest]["mrr"]
        >= gate_config["minimum_mrr_delta"],
        "bootstrap_lower": boot[0] > gate_config["minimum_bootstrap_lower"],
        "top10_prs": replay["rtca"]["top10_prs"]
        >= gate_config["minimum_top10_prs"],
        "ranking_nonidentity": not identical,
    }
    if (
        primary["phase"] != config["phase"]
        or primary["prs"] != config["evaluation_prs"]
        or int(primary["changed_ids"]) != total_labels
        or primary["identical_comparators"] != identical
        or primary["gates"] != replayed_gates
        or int(primary["gates_passed"]) != sum(replayed_gates.values())
        or bool(primary["all_gates_passed"]) != all(replayed_gates.values())
    ):
        errors.append("summary_contract_mismatch")

    report = {
        "status": "AUDIT_OK" if not errors else "AUDIT_FAILED",
        "errors": errors,
        "rows": len(raw),
        "source_feature_rows": source_feature_rows,
        "changed_ids": total_labels,
        "prs": len(expected_by_pr),
        "source_files_verified": source_files_verified,
        "maximum_channel_error": maximum_channel_error,
        "maximum_score_error": maximum_score_error,
        "maximum_rank_error": maximum_rank_error,
        "maximum_metric_error": maximum_metric_error,
        "strongest_comparator": strongest,
        "replayed_gates": replayed_gates,
        "replayed_metrics": replay,
        "replayed_bootstrap_95": boot,
        "raw_sha256": file_sha(args.raw),
        "summary_sha256": file_sha(args.summary),
        "config_sha256": file_sha(args.config),
    }
    args.report.parent.mkdir()
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "maximum_channel_error": maximum_channel_error,
                "maximum_metric_error": maximum_metric_error,
                "maximum_rank_error": maximum_rank_error,
                "maximum_score_error": maximum_score_error,
                "rows": len(raw),
                "status": report["status"],
            },
            sort_keys=True,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
