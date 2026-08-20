"""Workbench v001 shared library: instance normalization + reference checkers.

Scope: TravelPlanner-derived single-city 3-day full-slot carrier ("TP-SC3").
Plan schema (all slots required, no '-'):
    transport_out, transport_back : index into per-direction transport option
        list (flights first, then self-driving, then taxi)
    hotel                          : index into accommodations list
    meal_{d}_{m}                   : d in 1..3, m in {b, l, d2}, index into
        restaurants list (d2 = dinner)
    attr_{d}                       : d in 1..3, index into attractions list

Reference-checker semantics mirror the official TravelPlanner evaluators
(reference_upstream/hard_constraint.py, SHA 18ffc300...) with disclosed
deviations: full-slot schema, nights = days - 1, minimum-nights and
multi-city/city-routing commonsense checks out of scope. Distinctness of
restaurants and attractions mirrors the official commonsense requirement and
is stated to the formalizer as a structural rule.

stdlib only: importable from both the shared env and the z3 exception env.
"""

from __future__ import annotations

import ast
import csv
import json
import math
import re
from pathlib import Path

MEAL_SLOTS = [
    f"meal_{d}_{m}" for d in (1, 2, 3) for m in ("breakfast", "lunch", "dinner")
]
ATTR_SLOTS = [f"attr_{d}" for d in (1, 2, 3)]
ALL_SLOTS = ["transport_out", "transport_back", "hotel"] + MEAL_SLOTS + ATTR_SLOTS

ROOM_TYPE_LABEL = {
    "not shared room": None,  # violated iff room type == 'Shared room'
    "shared room": "Shared room",
    "private room": "Private room",
    "entire room": "Entire home/apt",
}


def _parse_ground_cost(text: str) -> int | None:
    match = re.search(r"cost:\s*([0-9][0-9,]*)", text)
    if match is None:
        return None
    return int(match.group(1).replace(",", ""))


def load_bucket(commit_dir: str | Path, bucket: str) -> list[dict]:
    """Mechanically load one bucket (csv rows joined with ref_info lines)."""
    commit_dir = Path(commit_dir)
    with open(commit_dir / f"bucket_{bucket}.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ref_by_index: dict[int, dict] = {}
    with open(commit_dir / f"bucket_{bucket}_ref_info.jsonl", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            ref_by_index[int(item["orig_index"])] = json.loads(item["raw"])
    out = []
    for row in rows:
        idx = int(row["orig_index"])
        out.append({"row": row, "ref": ref_by_index[idx], "orig_index": idx})
    return out


def normalize_sc3(entry: dict) -> dict | None:
    """Normalize a single-city 3-day instance; None if out of carrier scope."""
    row, ref = entry["row"], entry["ref"]
    if row["visiting_city_number"] != "1" or row["days"] != "3":
        return None
    org, dest = row["org"], row["dest"]
    dates = ast.literal_eval(row["date"])
    local = ast.literal_eval(row["local_constraint"])

    def transport_options(direction_org: str, direction_dest: str, date: str) -> list[dict]:
        options: list[dict] = []
        flight_key = f"Flight from {direction_org} to {direction_dest} on {date}"
        flights = ref.get(flight_key)
        if isinstance(flights, list):
            for f in flights:
                options.append(
                    {
                        "kind": "flight",
                        "label": f"Flight Number: {f['Flight Number']}",
                        "price": float(f["Price"]),
                        "detail": f,
                    }
                )
        for kind, key_prefix in (("self-driving", "Self-driving"), ("taxi", "Taxi")):
            key = f"{key_prefix} from {direction_org} to {direction_dest}"
            text = ref.get(key)
            if isinstance(text, str):
                cost = _parse_ground_cost(text)
                if cost is not None:
                    options.append(
                        {"kind": kind, "label": f"{key_prefix}, from {direction_org} to {direction_dest}", "price": float(cost), "detail": {"raw": text}}
                    )
        return options

    restaurants_key = f"Restaurants in {dest}"
    hotels_key = f"Accommodations in {dest}"
    attractions_key = f"Attractions in {dest}"
    if not all(isinstance(ref.get(k), list) for k in (restaurants_key, hotels_key, attractions_key)):
        return None

    instance = {
        "orig_index": entry["orig_index"],
        "org": org,
        "dest": dest,
        "dates": dates,
        "days": 3,
        "nights": 2,
        "people": int(row["people_number"]),
        "budget": float(row["budget"]),
        "level": row["level"],
        "local_constraint": local,
        "query": row["query"],
        "transport_out": transport_options(org, dest, dates[0]),
        "transport_back": transport_options(dest, org, dates[2]),
        "hotels": [
            {
                "name": h["NAME"],
                "price": float(h["price"]),
                "room_type": h["room type"],
                "house_rules": str(h["house_rules"]),
                "max_occupancy": int(h["maximum occupancy"]),
                "min_nights": h.get("minimum nights"),
            }
            for h in ref[hotels_key]
        ],
        "restaurants": [
            {"name": r["Name"], "avg_cost": float(r["Average Cost"]), "cuisines": str(r["Cuisines"])}
            for r in ref[restaurants_key]
        ],
        "attractions": [{"name": a["Name"]} for a in ref[attractions_key]],
    }
    if not instance["transport_out"] or not instance["transport_back"]:
        return None
    return instance


def transport_unit_cost(option: dict, people: int) -> float:
    if option["kind"] == "flight":
        return option["price"] * people
    if option["kind"] == "self-driving":
        return option["price"] * math.ceil(people / 5)
    return option["price"] * math.ceil(people / 4)


def total_cost(instance: dict, plan: dict) -> float:
    people = instance["people"]
    cost = 0.0
    cost += transport_unit_cost(instance["transport_out"][plan["transport_out"]], people)
    cost += transport_unit_cost(instance["transport_back"][plan["transport_back"]], people)
    hotel = instance["hotels"][plan["hotel"]]
    cost += hotel["price"] * math.ceil(people / hotel["max_occupancy"]) * instance["nights"]
    for slot in MEAL_SLOTS:
        cost += instance["restaurants"][plan[slot]]["avg_cost"] * people
    return cost


def check_category(instance: dict, plan: dict, category: str) -> bool | None:
    """True=pass, False=fail, None=not applicable. Mirrors official semantics."""
    local = instance["local_constraint"]
    if category == "budget":
        return total_cost(instance, plan) <= instance["budget"]
    if category == "house_rule":
        rule = local.get("house rule")
        if rule is None:
            return None
        hotel = instance["hotels"][plan["hotel"]]
        return f"No {rule}" not in hotel["house_rules"]
    if category == "room_type":
        want = local.get("room type")
        if want is None:
            return None
        actual = instance["hotels"][plan["hotel"]]["room_type"]
        if want == "not shared room":
            return actual != "Shared room"
        return actual == ROOM_TYPE_LABEL[want]
    if category == "cuisine":
        wanted = local.get("cuisine")
        if not wanted:
            return None
        covered = set()
        for slot in MEAL_SLOTS:
            cuisines = instance["restaurants"][plan[slot]]["cuisines"]
            for c in wanted:
                if c in cuisines:
                    covered.add(c)
        return len(covered) == len(wanted)
    if category == "transportation":
        constraint = local.get("transportation")
        if constraint is None:
            return None
        kinds = {
            instance["transport_out"][plan["transport_out"]]["kind"],
            instance["transport_back"][plan["transport_back"]]["kind"],
        }
        if constraint == "no flight":
            return "flight" not in kinds
        if constraint == "no self-driving":
            return "self-driving" not in kinds
        return None
    if category == "distinct_restaurants":
        chosen = [plan[s] for s in MEAL_SLOTS]
        return len(set(chosen)) == len(chosen)
    if category == "distinct_attractions":
        chosen = [plan[s] for s in ATTR_SLOTS]
        return len(set(chosen)) == len(chosen)
    raise ValueError(category)


CATEGORIES = [
    "budget",
    "house_rule",
    "room_type",
    "cuisine",
    "transportation",
    "distinct_restaurants",
    "distinct_attractions",
]


def evaluate_plan(instance: dict, plan: dict) -> dict:
    verdicts = {c: check_category(instance, plan, c) for c in CATEGORIES}
    applicable = {c: v for c, v in verdicts.items() if v is not None}
    return {
        "verdicts": verdicts,
        "solution_level_pass": all(applicable.values()),
        "total_cost": total_cost(instance, plan),
    }
