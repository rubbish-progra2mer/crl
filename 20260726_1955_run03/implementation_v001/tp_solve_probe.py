"""Implementation v001: solver-side payload (z3 exception environment).

Usage:
    python tp_solve_probe.py <instance.json> <generated_code.py> <out.json> full
    python tp_solve_probe.py <instance.json> <generated_code.py> <out.json> selftest

`full` runs: default solve + reference verdicts (A1), error signals (A2),
per-category enforcement probes with checker-cross-validated witnesses (A5),
behavioral tests (A4: budget scaling + compliant-option ablation), and
blocking-clause sampling of the model's solution space for the luck index
(M5c). `selftest` checks harness probe-encoding consistency against the
stdlib checkers on random assignments (no API, no D data).

Frozen evolution of workbench_v001/wb_solve_probe.py.
"""

from __future__ import annotations

import itertools
import json
import random
import sys
import time
from pathlib import Path

import z3

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tp_lib  # noqa: E402

SOLVER_TIMEOUT_MS = 60_000
SAMPLE_K = 50


def runtime_data(instance: dict) -> dict:
    """Runtime view for generated code: no gold local_constraint, no level."""
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


def make_pick():
    def pick(choice_var, values):
        expr = z3.RealVal(0)
        for i, v in enumerate(values):
            expr = z3.If(choice_var == i, z3.RealVal(v), expr)
        return expr

    return pick


def build_choices(instance: dict) -> tuple[list, dict]:
    domain_sizes = {
        "transport_out": len(instance["transport_out"]),
        "transport_back": len(instance["transport_back"]),
        "hotel": len(instance["hotels"]),
        **{slot: len(instance["restaurants"]) for slot in tp_lib.MEAL_SLOTS},
        **{slot: len(instance["attractions"]) for slot in tp_lib.ATTR_SLOTS},
    }
    choices = {name: z3.Int(name) for name in tp_lib.ALL_SLOTS}
    domain_asserts = [
        z3.And(choices[name] >= 0, choices[name] < domain_sizes[name])
        for name in tp_lib.ALL_SLOTS
    ]
    return domain_asserts, choices


def exec_generated(code_text: str, instance: dict, data: dict | None = None):
    """Compile + run add_constraints; returns (assertions, choices) or raises."""
    domain_asserts, choices = build_choices(instance)
    namespace = {"z3": z3, "pick": make_pick()}
    exec(compile(code_text, "generated_code.py", "exec"), namespace)  # noqa: S102
    add_constraints = namespace["add_constraints"]
    solver = z3.Solver()
    solver.set("timeout", SOLVER_TIMEOUT_MS)
    for a in domain_asserts:
        solver.add(a)
    add_constraints(solver, choices, data if data is not None else runtime_data(instance))
    return list(solver.assertions()), choices


def harness_cost_expr(instance: dict, choices: dict):
    import math

    people = instance["people"]
    pick = make_pick()
    out_costs = [tp_lib.transport_unit_cost(o, people) for o in instance["transport_out"]]
    back_costs = [tp_lib.transport_unit_cost(o, people) for o in instance["transport_back"]]
    hotel_costs = [
        h["price"] * math.ceil(people / h["max_occupancy"]) * instance["nights"]
        for h in instance["hotels"]
    ]
    meal_costs = [r["avg_cost"] * people for r in instance["restaurants"]]
    total = pick(choices["transport_out"], out_costs) + pick(
        choices["transport_back"], back_costs
    ) + pick(choices["hotel"], hotel_costs)
    for slot in tp_lib.MEAL_SLOTS:
        total = total + pick(choices[slot], meal_costs)
    return total


def probe_assertions(instance: dict, choices: dict) -> dict:
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
            return h["room_type"] != tp_lib.ROOM_TYPE_LABEL[want]
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
                z3.Or([choices[slot] == i for i in lacking]) for slot in tp_lib.MEAL_SLOTS
            ]
            per_cuisine.append((cuisine, z3.And(slot_conditions)))
        probes["cuisine"] = per_cuisine

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
        [choices[a] == choices[b] for a, b in itertools.combinations(tp_lib.MEAL_SLOTS, 2)]
    )
    probes["distinct_attractions"] = z3.Or(
        [choices[a] == choices[b] for a, b in itertools.combinations(tp_lib.ATTR_SLOTS, 2)]
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
    return {
        name: model.eval(var, model_completion=True).as_long()
        for name, var in choices.items()
    }


def run_probes(instance, model_assertions, choices) -> dict:
    probes = probe_assertions(instance, choices)
    results: dict[str, dict] = {}
    for category, assertion in probes.items():
        if assertion is None:
            results[category] = {"applicable": False}
            continue
        if category == "cuisine":
            sub = {}
            enforced_all = True
            for cuisine, expr in assertion:
                check, solver = solve(model_assertions, expr)
                entry = {"result": str(check)}
                if check == z3.sat:
                    witness = extract_plan(solver.model(), choices)
                    entry["witness_violates_reference"] = (
                        tp_lib.check_category(instance, witness, "cuisine") is False
                    )
                    entry["witness"] = witness
                    enforced_all = False
                sub[cuisine] = entry
            results[category] = {
                "applicable": True,
                "enforced": enforced_all,
                "per_cuisine": sub,
            }
            continue
        check, solver = solve(model_assertions, assertion)
        entry = {"applicable": True, "result": str(check)}
        if check == z3.sat:
            witness = extract_plan(solver.model(), choices)
            entry["enforced"] = False
            entry["witness"] = witness
            entry["witness_violates_reference"] = (
                tp_lib.check_category(instance, witness, category) is False
            )
            entry["witness_cost"] = tp_lib.total_cost(instance, witness)
        elif check == z3.unsat:
            entry["enforced"] = True
        else:
            entry["enforced"] = None
        results[category] = entry
    return results


def sample_luck(instance, model_assertions, choices, categories: list[str]) -> dict:
    """Blocking-clause sampling of M's solution space; per-category fraction of
    sampled solutions that nevertheless SATISFY the reference condition."""
    solver = z3.Solver()
    solver.set("timeout", SOLVER_TIMEOUT_MS)
    for a in model_assertions:
        solver.add(a)
    samples = []
    for _ in range(SAMPLE_K):
        if solver.check() != z3.sat:
            break
        model = solver.model()
        plan = extract_plan(model, choices)
        samples.append(plan)
        solver.add(z3.Or([choices[name] != plan[name] for name in tp_lib.ALL_SLOTS]))
    out = {"n_samples": len(samples)}
    for category in categories:
        verdicts = [tp_lib.check_category(instance, p, category) for p in samples]
        known = [v for v in verdicts if v is not None]
        out[category] = (
            sum(1 for v in known if v) / len(known) if known else None
        )
    return out


def behavioral_tests(instance, code_text) -> dict:
    """A4: ReLoop-CPT-adapted behavioral tests. Each test re-executes the
    generated code on modified data and flags 'unenforced' when the model
    still admits solutions that can only exist if the constraint is absent."""
    local = instance["local_constraint"]
    tests: dict[str, dict] = {}

    def rerun(modified_instance, modified_data):
        try:
            assertions, choices = exec_generated(
                code_text, modified_instance, modified_data
            )
        except Exception as error:  # noqa: BLE001
            return {"status": "exec_error", "error": str(error)[:200]}
        check, _ = solve(assertions)
        return {"status": "ok", "result": str(check)}

    # budget: scale the runtime budget down 1000x; enforced -> UNSAT expected
    tiny = dict(runtime_data(instance))
    tiny["budget"] = instance["budget"] * 0.001
    outcome = rerun(instance, tiny)
    tests["budget"] = {
        **outcome,
        "flag_unenforced": outcome.get("result") == "sat",
    }

    def ablate(field, keep_predicate):
        kept = [x for x in instance[field] if keep_predicate(x)]
        if not kept:
            return None
        modified_instance = dict(instance)
        modified_instance[field] = kept
        modified_data = runtime_data(modified_instance)
        outcome = rerun(modified_instance, modified_data)
        return {**outcome, "flag_unenforced": outcome.get("result") == "sat",
                "kept_options": len(kept)}

    rule = local.get("house rule")
    if rule is not None:
        tests["house_rule"] = ablate(
            "hotels", lambda h: f"No {rule}" in h["house_rules"]
        ) or {"status": "not_applicable_no_violating_options"}

    want = local.get("room type")
    if want is not None:
        def violates(h):
            if want == "not shared room":
                return h["room_type"] == "Shared room"
            return h["room_type"] != tp_lib.ROOM_TYPE_LABEL[want]
        tests["room_type"] = ablate("hotels", violates) or {
            "status": "not_applicable_no_violating_options"
        }

    wanted = local.get("cuisine")
    if wanted:
        sub = {}
        for cuisine in wanted:
            outcome = ablate(
                "restaurants", lambda r, c=cuisine: c not in r["cuisines"]
            )
            sub[cuisine] = outcome or {"status": "not_applicable_no_violating_options"}
        tests["cuisine"] = {
            "per_cuisine": sub,
            "flag_unenforced": any(
                isinstance(v, dict) and v.get("flag_unenforced") for v in sub.values()
            ),
        }

    constraint = local.get("transportation")
    if constraint is not None:
        forbidden = "flight" if constraint == "no flight" else "self-driving"
        modified_instance = dict(instance)
        keep_out = [o for o in instance["transport_out"] if o["kind"] == forbidden]
        keep_back = [o for o in instance["transport_back"] if o["kind"] == forbidden]
        if keep_out and keep_back:
            modified_instance["transport_out"] = keep_out
            modified_instance["transport_back"] = keep_back
            outcome = rerun(modified_instance, runtime_data(modified_instance))
            tests["transportation"] = {
                **outcome,
                "flag_unenforced": outcome.get("result") == "sat",
            }
        else:
            tests["transportation"] = {"status": "not_applicable_no_violating_options"}

    # distinctness: shrink the restaurant pool below the 9 required slots
    modified_instance = dict(instance)
    modified_instance["restaurants"] = instance["restaurants"][:8]
    outcome = rerun(modified_instance, runtime_data(modified_instance))
    tests["distinct_restaurants"] = {
        **outcome,
        "flag_unenforced": outcome.get("result") == "sat",
    }
    return tests


def selftest(instance, out_path) -> int:
    """Probe-encoding vs stdlib-checker consistency on random assignments."""
    rng = random.Random(20260726)
    domain_asserts, choices = build_choices(instance)
    probes = probe_assertions(instance, choices)
    mismatches = []
    checked = 0
    for _ in range(200):
        plan = {
            "transport_out": rng.randrange(len(instance["transport_out"])),
            "transport_back": rng.randrange(len(instance["transport_back"])),
            "hotel": rng.randrange(len(instance["hotels"])),
            **{s: rng.randrange(len(instance["restaurants"])) for s in tp_lib.MEAL_SLOTS},
            **{s: rng.randrange(len(instance["attractions"])) for s in tp_lib.ATTR_SLOTS},
        }
        fixed = [choices[name] == value for name, value in plan.items()]
        for category, assertion in probes.items():
            if assertion is None:
                continue
            if category == "cuisine":
                exprs = [expr for _, expr in assertion]
                probe_true_expr = z3.Or(exprs)
            else:
                probe_true_expr = assertion
            check, _ = solve(fixed, probe_true_expr)
            probe_says_violated = check == z3.sat
            checker = tp_lib.check_category(instance, plan, category)
            checker_says_violated = checker is False
            checked += 1
            if probe_says_violated != checker_says_violated:
                mismatches.append({"category": category, "plan": plan,
                                   "probe": probe_says_violated,
                                   "checker": checker_says_violated})
    result = {
        "status": "ok" if not mismatches else "mismatch",
        "assignments": 200,
        "comparisons": checked,
        "mismatches": mismatches[:10],
        "n_mismatches": len(mismatches),
    }
    Path(out_path).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"selftest": result["status"], "n_mismatches": len(mismatches)}))
    return 0 if not mismatches else 1


def main() -> int:
    instance_path, code_path, out_path, mode = sys.argv[1:5]
    instance = json.loads(Path(instance_path).read_text(encoding="utf-8"))
    code_text = Path(code_path).read_text(encoding="utf-8")
    if mode == "selftest":
        return selftest(instance, out_path)

    result: dict = {"status": "ok"}
    started = time.time()
    try:
        model_assertions, choices = exec_generated(code_text, instance)
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
        evaluation = tp_lib.evaluate_plan(instance, plan)
        result["default"] = {
            "assignment": plan,
            "verdicts": evaluation["verdicts"],
            "solution_level_pass": evaluation["solution_level_pass"],
            "total_cost": evaluation["total_cost"],
        }

    result["probes"] = run_probes(instance, model_assertions, choices)
    unenforced = [
        c for c, p in result["probes"].items()
        if p.get("applicable") and p.get("enforced") is False
    ]
    if check == z3.sat and unenforced:
        result["luck_sampling"] = sample_luck(
            instance, model_assertions, choices, unenforced
        )
    result["behavioral_tests"] = behavioral_tests(instance, code_text)
    result["wall_seconds"] = round(time.time() - started, 2)
    Path(out_path).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
