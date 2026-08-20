"""Workbench v001: run a generated constraint model and probe per-category
enforcement (executes in the z3 exception environment).

Usage: python wb_solve_probe.py <instance.json> <generated_code.py> <out.json>

For each applicable category the probe asks: does the generated model M admit
a solution violating the reference condition? SAT -> not enforced (witness
recorded and cross-checked with the stdlib reference checkers); UNSAT ->
enforced. The default solve plus reference verdicts give the solution-level
view; masked = category not enforced while the default solution passes it.
"""

from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import z3

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wb_lib  # noqa: E402

SOLVER_TIMEOUT_MS = 60_000


def runtime_data(instance: dict) -> dict:
    """Runtime view for the generated code: no gold local_constraint, no level."""
    return {
        "people": instance["people"],
        "nights": instance["nights"],
        "budget": instance["budget"],
        "transport_out": instance["transport_out"],
        "transport_back": instance["transport_back"],
        "hotels": instance["hotels"],
        "restaurants": instance["restaurants"],
        "attractions": instance["attractions"],
    }


def build_choices(instance: dict) -> tuple[list, dict]:
    domain_sizes = {
        "transport_out": len(instance["transport_out"]),
        "transport_back": len(instance["transport_back"]),
        "hotel": len(instance["hotels"]),
        **{slot: len(instance["restaurants"]) for slot in wb_lib.MEAL_SLOTS},
        **{slot: len(instance["attractions"]) for slot in wb_lib.ATTR_SLOTS},
    }
    choices = {name: z3.Int(name) for name in wb_lib.ALL_SLOTS}
    domain_asserts = [
        z3.And(choices[name] >= 0, choices[name] < domain_sizes[name])
        for name in wb_lib.ALL_SLOTS
    ]
    return domain_asserts, choices


def harness_cost_expr(instance: dict, choices: dict):
    import math

    people = instance["people"]

    def pick(var, values):
        expr = z3.RealVal(0)
        for i, v in enumerate(values):
            expr = z3.If(var == i, z3.RealVal(v), expr)
        return expr

    out_costs = [wb_lib.transport_unit_cost(o, people) for o in instance["transport_out"]]
    back_costs = [wb_lib.transport_unit_cost(o, people) for o in instance["transport_back"]]
    hotel_costs = [
        h["price"] * math.ceil(people / h["max_occupancy"]) * instance["nights"]
        for h in instance["hotels"]
    ]
    meal_costs = [r["avg_cost"] * people for r in instance["restaurants"]]

    total = pick(choices["transport_out"], out_costs) + pick(
        choices["transport_back"], back_costs
    ) + pick(choices["hotel"], hotel_costs)
    for slot in wb_lib.MEAL_SLOTS:
        total = total + pick(choices[slot], meal_costs)
    return total


def probe_assertions(instance: dict, choices: dict) -> dict:
    """Per applicable category: a z3 assertion meaning 'this category violated'."""
    local = instance["local_constraint"]
    probes: dict[str, object] = {}

    probes["budget"] = harness_cost_expr(instance, choices) > instance["budget"]

    rule = local.get("house rule")
    if rule is not None:
        bad = [i for i, h in enumerate(instance["hotels"]) if f"No {rule}" in h["house_rules"]]
        probes["house_rule"] = z3.Or([choices["hotel"] == i for i in bad]) if bad else None

    want = local.get("room type")
    if want is not None:
        def violates(h):
            if want == "not shared room":
                return h["room_type"] == "Shared room"
            return h["room_type"] != wb_lib.ROOM_TYPE_LABEL[want]
        bad = [i for i, h in enumerate(instance["hotels"]) if violates(h)]
        probes["room_type"] = z3.Or([choices["hotel"] == i for i in bad]) if bad else None

    wanted = local.get("cuisine")
    if wanted:
        per_cuisine = []
        for cuisine in wanted:
            lacking = [
                i for i, r in enumerate(instance["restaurants"]) if cuisine not in r["cuisines"]
            ]
            slot_conditions = [
                z3.Or([choices[slot] == i for i in lacking]) for slot in wb_lib.MEAL_SLOTS
            ]
            per_cuisine.append((cuisine, z3.And(slot_conditions)))
        probes["cuisine"] = per_cuisine  # list of (cuisine, assertion)

    constraint = local.get("transportation")
    if constraint is not None:
        forbidden_kind = "flight" if constraint == "no flight" else "self-driving"
        terms = []
        for slot_name, options in (
            ("transport_out", instance["transport_out"]),
            ("transport_back", instance["transport_back"]),
        ):
            for i, option in enumerate(options):
                if option["kind"] == forbidden_kind:
                    terms.append(choices[slot_name] == i)
        probes["transportation"] = z3.Or(terms) if terms else None

    probes["distinct_restaurants"] = z3.Or(
        [
            choices[a] == choices[b]
            for a, b in itertools.combinations(wb_lib.MEAL_SLOTS, 2)
        ]
    )
    probes["distinct_attractions"] = z3.Or(
        [
            choices[a] == choices[b]
            for a, b in itertools.combinations(wb_lib.ATTR_SLOTS, 2)
        ]
    )
    return probes


def solve(assertions, extra=None):
    solver = z3.Solver()
    solver.set("timeout", SOLVER_TIMEOUT_MS)
    for a in assertions:
        solver.add(a)
    if extra is not None:
        solver.add(extra)
    result = solver.check()
    return result, solver


def extract_plan(model, choices) -> dict:
    plan = {}
    for name, var in choices.items():
        value = model.eval(var, model_completion=True)
        plan[name] = value.as_long()
    return plan


def main() -> int:
    instance_path, code_path, out_path = sys.argv[1:4]
    instance = json.loads(Path(instance_path).read_text(encoding="utf-8"))
    code_text = Path(code_path).read_text(encoding="utf-8")

    domain_asserts, choices = build_choices(instance)

    def pick(choice_var, values):
        expr = z3.RealVal(0)
        for i, v in enumerate(values):
            expr = z3.If(choice_var == i, z3.RealVal(v), expr)
        return expr

    namespace = {"z3": z3, "pick": pick}
    result: dict = {"status": "ok"}
    started = time.time()
    try:
        exec(compile(code_text, "generated_code.py", "exec"), namespace)  # noqa: S102
        add_constraints = namespace["add_constraints"]
        model_solver = z3.Solver()
        model_solver.set("timeout", SOLVER_TIMEOUT_MS)
        for a in domain_asserts:
            model_solver.add(a)
        add_constraints(model_solver, choices, runtime_data(instance))
        model_assertions = list(model_solver.assertions())
    except Exception as error:  # noqa: BLE001 - formalization errors are data
        result["status"] = "formalization_error"
        result["error"] = f"{type(error).__name__}: {error}"[:500]
        Path(out_path).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps({"status": result["status"]}))
        return 0

    check, solver = solve(model_assertions)
    if check != z3.sat:
        result["status"] = f"default_{check}"
        result["default"] = None
    else:
        plan = extract_plan(solver.model(), choices)
        evaluation = wb_lib.evaluate_plan(instance, plan)
        result["default"] = {
            "assignment": plan,
            "verdicts": evaluation["verdicts"],
            "solution_level_pass": evaluation["solution_level_pass"],
            "total_cost": evaluation["total_cost"],
        }

    probes = probe_assertions(instance, choices)
    probe_results: dict[str, dict] = {}
    for category, assertion in probes.items():
        if assertion is None:
            probe_results[category] = {"applicable": False}
            continue
        if category == "cuisine":
            sub = {}
            enforced_all = True
            for cuisine, expr in assertion:
                probe_check, probe_solver = solve(model_assertions, expr)
                entry = {"result": str(probe_check)}
                if probe_check == z3.sat:
                    witness = extract_plan(probe_solver.model(), choices)
                    entry["witness_violates_reference"] = (
                        wb_lib.check_category(instance, witness, "cuisine") is False
                    )
                    enforced_all = False
                sub[cuisine] = entry
            probe_results[category] = {
                "applicable": True,
                "enforced": enforced_all,
                "per_cuisine": sub,
            }
            continue
        probe_check, probe_solver = solve(model_assertions, assertion)
        entry = {"applicable": True, "result": str(probe_check)}
        if probe_check == z3.sat:
            witness = extract_plan(probe_solver.model(), choices)
            entry["enforced"] = False
            entry["witness_violates_reference"] = (
                wb_lib.check_category(instance, witness, category) is False
            )
            entry["witness_cost"] = wb_lib.total_cost(instance, witness)
        elif probe_check == z3.unsat:
            entry["enforced"] = True
        else:
            entry["enforced"] = None
        probe_results[category] = entry

    result["probes"] = probe_results
    result["wall_seconds"] = round(time.time() - started, 2)
    Path(out_path).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
