#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import requests


RUN_ROOT = Path(__file__).resolve().parents[1]
REPO = RUN_ROOT / "workbench_v115" / "OADD-Bench"
METHODS = REPO / "Methods"
if str(METHODS) not in sys.path:
    sys.path.insert(0, str(METHODS))

from retrieval import (  # noqa: E402
    RetrievalIndex,
    load_or_build_families,
    ranking_to_columns,
    reciprocal_rank_fusion,
)


BENCHMARK = REPO / "benchmark" / "OADD-Bench" / "OADD_Bench.csv"
EVIDENCE = REPO / "benchmark" / "OADD-Bench" / "OADD_Bench_evidence.jsonl"
METADATA = REPO / "benchmark" / "HRS_metadata" / "metadata.jsonl"
FIXES = REPO / "benchmark" / "HRS_metadata" / "metadata_fixes.jsonl"
CACHE = REPO / "cache"
BLIND_CASES = RUN_ROOT / "workbench_v115" / "blind_cases_v115.jsonl"
SAMPLE_SALT = "v115-oadd-pilot-001"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
TOP_K = 1000


PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "roles": {
            "type": "array",
            "minItems": 1,
            "maxItems": 4,
            "items": {
                "type": "object",
                "properties": {
                    "role": {"type": "string"},
                    "concept": {"type": "string"},
                    "components": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": 6,
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "search_query": {"type": "string"},
                            },
                            "required": ["name", "search_query"],
                        },
                    },
                },
                "required": ["role", "concept", "components"],
            },
        }
    },
    "required": ["roles"],
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sample_key(record_id: str) -> str:
    return hashlib.sha256(f"{SAMPLE_SALT}:{record_id}".encode("utf-8")).hexdigest()


def prepare_blind_manifest() -> None:
    with BENCHMARK.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    cases = []
    for row in rows:
        target_size = sum(bool(value.strip()) for value in row["hrs_column_ids"].split(";"))
        cases.append(
            {
                "record_id": row["record_id"],
                "question": row["research_question"],
                "years": sorted(
                    value.strip()
                    for value in row["allowed_years"].split(";")
                    if value.strip()
                ),
                "target_size": target_size,
                "sample_key": sample_key(row["record_id"]),
            }
        )
    write_jsonl(BLIND_CASES, cases)


def load_generation_cases(sample_size: int) -> list[dict[str, Any]]:
    if not BLIND_CASES.exists():
        raise FileNotFoundError(
            f"Missing {BLIND_CASES}; run this script once with --prepare-blind-manifest"
        )
    with BLIND_CASES.open(encoding="utf-8") as handle:
        cases = [json.loads(line) for line in handle if line.strip()]
    cases.sort(key=lambda row: row["sample_key"])
    return cases[:sample_size]


def generation_prompt(case: dict[str, Any]) -> str:
    years = ", ".join(case["years"]) if case["years"] else "any available year"
    return f"""You are planning measurement discovery in the Health and Retirement Study (HRS) codebooks.

Research question: {case['question']}
Allowed years: {years}

Infer the focal measurement roles needed to answer the question (for example exposure, outcome, mediator, or moderator). For each role, propose observable components that could defensibly operationalize the concept using fields that may exist in HRS. A component should be a concrete observable, survey item, test, biomarker, event, or derived quantity—not a database identifier and not a generic synonym. Provide one concise English codebook search query per component. Cover complementary components when a construct is normally a scale or bundle. Do not invent exact HRS identifiers. Return only the required JSON."""


def normalize_plan(raw: Any) -> tuple[dict[str, Any], bool, str]:
    if not isinstance(raw, dict) or not isinstance(raw.get("roles"), list):
        return {"roles": []}, False, "missing_roles"
    roles = []
    total_components = 0
    for role_raw in raw["roles"][:4]:
        if not isinstance(role_raw, dict):
            continue
        role = str(role_raw.get("role", "")).strip()[:80]
        concept = str(role_raw.get("concept", "")).strip()[:240]
        components = []
        for component_raw in role_raw.get("components", [])[:6]:
            if not isinstance(component_raw, dict) or total_components >= 12:
                continue
            name = str(component_raw.get("name", "")).strip()[:240]
            query = " ".join(str(component_raw.get("search_query", "")).split())[:500]
            if not name or not query:
                continue
            components.append({"name": name, "search_query": query})
            total_components += 1
        if role and concept and components:
            roles.append({"role": role, "concept": concept, "components": components})
    valid = bool(roles and total_components)
    return {"roles": roles}, valid, "ok" if valid else "no_valid_components"


def generate_plan(model: str, case: dict[str, Any]) -> dict[str, Any]:
    seed = int(hashlib.sha256(case["record_id"].encode("utf-8")).hexdigest()[:8], 16)
    payload = {
        "model": model,
        "prompt": generation_prompt(case),
        "format": PLAN_SCHEMA,
        "stream": False,
        "options": {"temperature": 0, "seed": seed, "num_ctx": 4096},
    }
    started = time.monotonic()
    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    response.raise_for_status()
    body = response.json()
    try:
        raw = json.loads(body["response"])
        plan, valid, reason = normalize_plan(raw)
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        plan, valid, reason = {"roles": []}, False, f"parse_error:{type(error).__name__}"
    return {
        "record_id": case["record_id"],
        "valid": valid,
        "reason": reason,
        "plan": plan,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "eval_count": body.get("eval_count"),
    }


def component_queries(plan: dict[str, Any]) -> list[list[str]]:
    groups = []
    for role in plan.get("roles", []):
        role_queries = []
        for component in role["components"]:
            role_queries.append(
                "; ".join(
                    [role["concept"], component["name"], component["search_query"]]
                )
            )
        if role_queries:
            groups.append(role_queries)
    return groups


def next_unseen(ranking: list[int], cursor: int, seen: set[int]) -> tuple[int | None, int]:
    while cursor < len(ranking):
        value = ranking[cursor]
        cursor += 1
        if value not in seen:
            return value, cursor
    return None, cursor


def hierarchical_round_robin(
    role_rankings: list[list[list[int]]], top_k: int
) -> list[int]:
    if not role_rankings:
        return []
    cursors = [[0 for _ in role] for role in role_rankings]
    component_turn = [0 for _ in role_rankings]
    output: list[int] = []
    seen: set[int] = set()
    active = True
    while len(output) < top_k and active:
        active = False
        for role_index, components in enumerate(role_rankings):
            if not components or len(output) >= top_k:
                continue
            for offset in range(len(components)):
                component_index = (component_turn[role_index] + offset) % len(components)
                value, cursor = next_unseen(
                    components[component_index],
                    cursors[role_index][component_index],
                    seen,
                )
                cursors[role_index][component_index] = cursor
                if value is None:
                    continue
                output.append(value)
                seen.add(value)
                component_turn[role_index] = (component_index + 1) % len(components)
                active = True
                break
    return output


def predictions_for_ranking(
    ranking: list[int],
    families: list[dict[str, Any]],
    years: list[str],
    target_size: int,
) -> dict[str, list[str]]:
    columns = ranking_to_columns(ranking, families, set(years), 5 * target_size)
    return {str(multiplier): columns[: multiplier * target_size] for multiplier in (1, 2, 5)}


def load_targets() -> dict[str, set[str]]:
    with BENCHMARK.open(newline="", encoding="utf-8") as handle:
        return {
            row["record_id"]: {
                value.strip().upper()
                for value in row["hrs_column_ids"].split(";")
                if value.strip()
            }
            for row in csv.DictReader(handle)
        }


def load_measurement_groups() -> dict[str, list[set[str]]]:
    groups: dict[str, list[set[str]]] = {}
    with EVIDENCE.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            record_groups = []
            for measurement in row.get("measurement_groups", []):
                columns = {
                    value.upper()
                    for mapping in measurement.get("hrs_mappings", [])
                    for value in mapping.get("column_ids", [])
                    if value
                }
                if columns:
                    record_groups.append(columns)
            groups[row["question_id"]] = record_groups
    return groups


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def paired_bootstrap_ci(differences: list[float], samples: int = 20000) -> list[float]:
    generator = random.Random(115001)
    estimates = []
    for _ in range(samples):
        estimates.append(mean([generator.choice(differences) for _ in differences]))
    estimates.sort()
    return [estimates[int(0.025 * samples)], estimates[int(0.975 * samples)]]


def score_condition(
    cases: list[dict[str, Any]],
    predictions: dict[str, dict[str, list[str]]],
    targets: dict[str, set[str]],
    measurement_groups: dict[str, list[set[str]]],
) -> dict[str, Any]:
    recalls: dict[str, list[float]] = {str(value): [] for value in (1, 2, 5)}
    component_any = []
    component_complete = []
    every_component = 0
    output_sizes = []
    per_question_recall_5r = {}
    for case in cases:
        record_id = case["record_id"]
        target = targets[record_id]
        for multiplier in (1, 2, 5):
            predicted = {value.upper() for value in predictions[record_id][str(multiplier)]}
            recalls[str(multiplier)].append(len(predicted & target) / len(target))
        predicted_5r = {value.upper() for value in predictions[record_id]["5"]}
        per_question_recall_5r[record_id] = len(predicted_5r & target) / len(target)
        groups = measurement_groups.get(record_id, [])
        if groups:
            any_flags = [bool(group & predicted_5r) for group in groups]
            complete_flags = [group <= predicted_5r for group in groups]
            component_any.append(mean([float(value) for value in any_flags]))
            component_complete.append(mean([float(value) for value in complete_flags]))
            every_component += int(all(any_flags))
        output_sizes.append(len(predictions[record_id]["5"]))
    return {
        "macro_exact_column_recall": {
            f"{multiplier}R": mean(values) for multiplier, values in recalls.items()
        },
        "macro_component_any_rate_5R": mean(component_any),
        "macro_component_complete_rate_5R": mean(component_complete),
        "every_component_question_count_5R": every_component,
        "every_component_question_rate_5R": every_component / len(cases),
        "mean_output_size_5R": mean([float(value) for value in output_sizes]),
        "per_question_recall_5R": per_question_recall_5r,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen2.5:7b")
    parser.add_argument("--sample-size", type=int, default=32)
    parser.add_argument("--prepare-blind-manifest", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=RUN_ROOT / "experiment_v115" / "result_001.json",
    )
    args = parser.parse_args()

    if args.prepare_blind_manifest:
        prepare_blind_manifest()
        print(json.dumps({"blind_manifest": str(BLIND_CASES), "records": 160}))
        return

    cases = load_generation_cases(args.sample_size)
    families, fingerprint = load_or_build_families(METADATA, FIXES, CACHE)
    index = RetrievalIndex(families, fingerprint, CACHE)
    direct_rankings = index.bm25([case["question"] for case in cases], TOP_K)

    plan_rows = []
    condition_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    prediction_maps: dict[str, dict[str, dict[str, list[str]]]] = defaultdict(dict)

    for position, (case, direct_ranking) in enumerate(
        zip(cases, direct_rankings, strict=True), start=1
    ):
        plan_row = generate_plan(args.model, case)
        plan_rows.append(plan_row)
        grouped_queries = component_queries(plan_row["plan"]) if plan_row["valid"] else []
        flat_queries = [query for role in grouped_queries for query in role]
        if flat_queries:
            flat_rankings = index.bm25(flat_queries, TOP_K)
            role_rankings = []
            cursor = 0
            for role_queries in grouped_queries:
                role_rankings.append(flat_rankings[cursor : cursor + len(role_queries)])
                cursor += len(role_queries)
            flat_ranking = reciprocal_rank_fusion(flat_rankings, TOP_K)
            closure_ranking = hierarchical_round_robin(role_rankings, TOP_K)
        else:
            flat_ranking = direct_ranking
            closure_ranking = direct_ranking

        rankings = {
            "direct_bm25": direct_ranking,
            "flat_rrf": flat_ranking,
            "role_closure": closure_ranking,
        }
        for condition, ranking in rankings.items():
            prediction = predictions_for_ranking(
                ranking, families, case["years"], case["target_size"]
            )
            prediction_maps[condition][case["record_id"]] = prediction
            condition_rows[condition].append(
                {"record_id": case["record_id"], "predictions": prediction}
            )
        print(
            json.dumps(
                {
                    "stage": "generation",
                    "completed": position,
                    "total": len(cases),
                    "record_id": case["record_id"],
                    "valid": plan_row["valid"],
                    "roles": len(plan_row["plan"]["roles"]),
                    "components": len(flat_queries),
                }
            ),
            flush=True,
        )

    output_dir = args.output.parent
    write_jsonl(output_dir / "plans_001.jsonl", plan_rows)
    for condition, rows in condition_rows.items():
        write_jsonl(output_dir / f"predictions_{condition}_001.jsonl", rows)

    # The hidden target identifiers and measurement-group evidence are loaded only
    # after every condition's prediction file has been durably written above.
    targets = load_targets()
    groups = load_measurement_groups()
    scores = {
        condition: score_condition(cases, predictions, targets, groups)
        for condition, predictions in prediction_maps.items()
    }
    flat_per_question = scores["flat_rrf"].pop("per_question_recall_5R")
    closure_per_question = scores["role_closure"].pop("per_question_recall_5R")
    scores["direct_bm25"].pop("per_question_recall_5R")
    differences = [
        closure_per_question[case["record_id"]] - flat_per_question[case["record_id"]]
        for case in cases
    ]
    paired = {
        "mean_recall_5R_difference": mean(differences),
        "bootstrap_95_percent_ci": paired_bootstrap_ci(differences),
        "wins": sum(value > 0 for value in differences),
        "losses": sum(value < 0 for value in differences),
        "ties": sum(value == 0 for value in differences),
    }
    valid_plans = sum(bool(row["valid"]) for row in plan_rows)
    role_counts = [len(row["plan"]["roles"]) for row in plan_rows]
    component_counts = [
        sum(len(role["components"]) for role in row["plan"]["roles"])
        for row in plan_rows
    ]
    recall_delta = (
        scores["role_closure"]["macro_exact_column_recall"]["5R"]
        - scores["flat_rrf"]["macro_exact_column_recall"]["5R"]
    )
    every_count_delta = (
        scores["role_closure"]["every_component_question_count_5R"]
        - scores["flat_rrf"]["every_component_question_count_5R"]
    )
    every_rate_delta = (
        scores["role_closure"]["every_component_question_rate_5R"]
        - scores["flat_rrf"]["every_component_question_rate_5R"]
    )
    complete_delta = (
        scores["role_closure"]["macro_component_complete_rate_5R"]
        - scores["flat_rrf"]["macro_component_complete_rate_5R"]
    )
    gates = {
        "valid_plan_count_at_least_30": valid_plans >= 30,
        "recall_5R_delta_at_least_0_025": recall_delta >= 0.025,
        "every_component_count_gain_at_least_4": every_count_delta >= 4,
        "every_component_rate_delta_at_least_0_10": every_rate_delta >= 0.10,
        "complete_component_delta_at_least_0_025": complete_delta >= 0.025,
        "closure_recall_not_below_direct": (
            scores["role_closure"]["macro_exact_column_recall"]["5R"]
            >= scores["direct_bm25"]["macro_exact_column_recall"]["5R"]
        ),
    }
    result = {
        "schema_version": 1,
        "record_id": "oadd-role-closure-qwen2-5-7b-001",
        "benchmark_commit": "cb60f8951075980ff8c76d3e95f201d11de6030d",
        "model": args.model,
        "sample_salt": SAMPLE_SALT,
        "sample_size": len(cases),
        "sample_record_ids": [case["record_id"] for case in cases],
        "catalog_family_fingerprint": fingerprint,
        "valid_plan_count": valid_plans,
        "mean_role_count": mean([float(value) for value in role_counts]),
        "mean_component_count": mean([float(value) for value in component_counts]),
        "scores": scores,
        "paired_role_closure_minus_flat_rrf": paired,
        "registered_deltas": {
            "recall_5R": recall_delta,
            "every_component_question_count_5R": every_count_delta,
            "every_component_question_rate_5R": every_rate_delta,
            "macro_component_complete_rate_5R": complete_delta,
        },
        "gates": gates,
        "all_continue_conditions_met": all(gates.values()),
        "generation_data_boundary": (
            "source papers, explanations, provenance, targets, and evidence were loaded "
            "only after all prediction files were written"
        ),
    }
    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
