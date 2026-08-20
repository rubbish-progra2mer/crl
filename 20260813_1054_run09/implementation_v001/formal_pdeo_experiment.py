from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path

from dqbp_core import ABSTAIN as DQBP_ABSTAIN
from dqbp_core import Branch
from obligation_bench import ObligationDomain, build_obligation_domains
from obligation_core import ABSTAIN, PROCEED, Atom, compile_obligations
from run_obligation_experiment import METHODS, _run_method


EXPERIMENT_ID = "pdeo-systematic-fault-suite-v1"
ADAPTIVE_BUDGET = 3

# These evaluator rules are intentionally declared independently of the PDEO
# compiler. They express the operational meaning of a safe downstream commit.
SAFETY_RULES: dict[str, tuple[Atom, ...]] = {
    "reservation": (
        Atom("target_status", "CONFIRMED"),
        Atom("payment_state", "CAPTURED"),
        Atom("other_booking", "UNCHANGED"),
    ),
    "access_control": (
        Atom("target_role", "EDITOR"),
        Atom("scope_state", "PROJECT_ONLY"),
        Atom("other_principal", "UNCHANGED"),
    ),
    "inventory": (
        Atom("target_quantity", "PLUS_5"),
        Atom("warehouse_balance", "BALANCED"),
        Atom("other_sku", "UNCHANGED"),
    ),
}


@dataclass(frozen=True, slots=True)
class FormalCase:
    case_id: str
    domain: str
    split: str
    state: dict[str, str]
    expected: str


def _safe(domain: str, state: dict[str, str]) -> bool:
    return all(state.get(atom.field) == atom.expected for atom in SAFETY_RULES[domain])


def _values_by_field(domain: ObligationDomain) -> dict[str, tuple[str, ...]]:
    values: dict[str, set[str]] = {
        probe.name: set() for probe in domain.branch_model.probes
    }
    for branch in domain.branch_model.branches:
        for field, value in branch.observations.items():
            values[field].add(value)
    return {field: tuple(sorted(items)) for field, items in values.items()}


def build_systematic_cases() -> tuple[FormalCase, ...]:
    cases: list[FormalCase] = []
    seen: set[tuple[str, str, tuple[tuple[str, str], ...]]] = set()

    def add(domain: str, split: str, state: dict[str, str], label: str) -> None:
        key = (domain, split, tuple(sorted(state.items())))
        if key in seen:
            return
        seen.add(key)
        expected = PROCEED if _safe(domain, state) else ABSTAIN
        cases.append(
            FormalCase(
                case_id=f"{domain}-{label}-{len(cases):04d}",
                domain=domain,
                split=split,
                state=dict(state),
                expected=expected,
            )
        )

    for domain in build_obligation_domains():
        values = _values_by_field(domain)
        rules = SAFETY_RULES[domain.name]
        obligation_fields = {atom.field for atom in rules}
        correct = [
            branch
            for branch in domain.branch_model.branches
            if _safe(domain.name, dict(branch.observations))
        ]
        for branch in domain.branch_model.branches:
            add(domain.name, "known_branches", dict(branch.observations), branch.name)

        for base in correct:
            base_state = dict(base.observations)
            for atom in rules:
                for alternative in values[atom.field]:
                    if alternative == atom.expected:
                        continue
                    mutated = dict(base_state)
                    mutated[atom.field] = alternative
                    add(
                        domain.name,
                        "systematic_obligation_faults",
                        mutated,
                        f"{base.name}-{atom.field}-{alternative}",
                    )

            nuisance_fields = sorted(set(values) - obligation_fields)
            for field in nuisance_fields:
                for alternative in values[field]:
                    if alternative == base_state[field]:
                        continue
                    mutated = dict(base_state)
                    mutated[field] = alternative
                    add(
                        domain.name,
                        "systematic_nuisance_variants",
                        mutated,
                        f"{base.name}-{field}-{alternative}",
                    )

            first_nuisance = nuisance_fields[0]
            nuisance_alternative = next(
                value
                for value in values[first_nuisance]
                if value != base_state[first_nuisance]
            )
            for atom in rules:
                alternative = next(
                    value for value in values[atom.field] if value != atom.expected
                )
                mutated = dict(base_state)
                mutated[atom.field] = alternative
                mutated[first_nuisance] = nuisance_alternative
                add(
                    domain.name,
                    "paired_obligation_and_nuisance_faults",
                    mutated,
                    f"{base.name}-{atom.field}-paired",
                )
    return tuple(cases)


def _branch_from_case(case: FormalCase) -> Branch:
    decision = PROCEED if case.expected == PROCEED else DQBP_ABSTAIN
    return Branch(case.case_id, decision, case.state, 0.0)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def run_formal() -> tuple[dict, dict]:
    started = time.perf_counter()
    rng = random.Random(0)
    domains = {domain.name: domain for domain in build_obligation_domains()}
    compiled = {
        name: compile_obligations(
            domain.prefix_actions, domain.protected_commit, domain.probes
        )
        for name, domain in domains.items()
    }
    compiler_checks = {
        name: set(item.atoms) == set(SAFETY_RULES[name])
        for name, item in compiled.items()
    }
    if not all(compiler_checks.values()):
        raise RuntimeError(f"compiler/evaluator obligation mismatch: {compiler_checks}")

    rows: list[dict] = []
    cases = build_systematic_cases()
    for case in cases:
        domain = domains[case.domain]
        branch = _branch_from_case(case)
        for method in METHODS:
            result = _run_method(
                domain,
                branch,
                method,
                budget=ADAPTIVE_BUDGET,
                rng=rng,
                compiled=compiled[case.domain],
            )
            rows.append(
                {
                    "case_id": case.case_id,
                    "domain": case.domain,
                    "split": case.split,
                    "method": method,
                    "selected": result.selected,
                    "expected": case.expected,
                    "unsafe_commit": result.selected == PROCEED
                    and case.expected != PROCEED,
                    "correct": result.selected == case.expected,
                    "probe_cost": result.probe_cost,
                    "probes": list(result.probe_names),
                }
            )

    records: list[dict] = []
    splits = sorted({case.split for case in cases})
    for split in splits:
        for method in METHODS:
            subset = [
                row
                for row in rows
                if row["split"] == split and row["method"] == method
            ]
            safe_subset = [row for row in subset if row["expected"] == PROCEED]
            records.extend(
                [
                    {
                        "name": f"{method}_unsafe_commit_rate_{split}",
                        "value": _mean(
                            [float(row["unsafe_commit"]) for row in subset]
                        ),
                        "unit": "proportion",
                        "split": split,
                        "aggregation": "case_mean",
                        "n": len(subset),
                    },
                    {
                        "name": f"{method}_gate_accuracy_{split}",
                        "value": _mean([float(row["correct"]) for row in subset]),
                        "unit": "proportion",
                        "split": split,
                        "aggregation": "case_mean",
                        "n": len(subset),
                    },
                    {
                        "name": f"{method}_average_probe_cost_{split}",
                        "value": _mean([float(row["probe_cost"]) for row in subset]),
                        "unit": "cost_units",
                        "split": split,
                        "aggregation": "case_mean",
                        "n": len(subset),
                    },
                ]
            )
            if safe_subset:
                records.append(
                    {
                        "name": f"{method}_valid_commit_recall_{split}",
                        "value": _mean(
                            [
                                float(row["selected"] == PROCEED)
                                for row in safe_subset
                            ]
                        ),
                        "unit": "proportion",
                        "split": split,
                        "aggregation": "case_mean",
                        "n": len(safe_subset),
                    }
                )

    wall_time = time.perf_counter() - started
    metrics = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "records": records,
        "resource_usage": {
            "tokens": 0,
            "api_calls": 0,
            "wall_time_seconds": wall_time,
            "gpu_time_seconds": 0,
            "estimated_cost": 0,
        },
        "errors": [],
        "warnings": [
            "Controlled systematic simulator over typed plans; no natural-language plan extraction is evaluated.",
            "Evaluator safety rules are declared separately from the PDEO compiler and cover all systematic single-obligation mutations present in the pre-existing branch vocabulary.",
        ],
    }
    details = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "adaptive_budget": ADAPTIVE_BUDGET,
        "case_count": len(cases),
        "compiler_matches_independent_rules": compiler_checks,
        "cases_by_split": {
            split: sum(case.split == split for case in cases) for split in splits
        },
        "rows": rows,
    }
    return metrics, details


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--details-output", type=Path, required=True)
    args = parser.parse_args()
    metrics, details = run_formal()
    args.metrics_output.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    args.details_output.write_text(
        json.dumps(details, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "experiment_id": metrics["experiment_id"],
                "case_count": details["case_count"],
                "records": metrics["records"],
                "warnings": metrics["warnings"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
