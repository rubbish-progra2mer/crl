from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Mapping, Sequence

from obligation_core import (
    ABSTAIN,
    PROCEED,
    Atom,
    CompiledObligations,
    GateResult,
    PlanAction,
    compile_obligations,
    minimum_cost_probe_cover,
    run_atom_gate,
    run_compiled_gate,
)
from plan_variation_bench import (
    PlanVariant,
    PlanVariationDomain,
    build_plan_variation_domains,
    validate_plan_variation_domains,
)


EXPERIMENT_ID = "pdeo-plan-variation-suite-v2"
METHODS = (
    "no_verification",
    "fixed_target_readback",
    "static_domain_contract",
    "pdeo_direct_commit_only",
    "pdeo",
    "human_per_plan_minimal",
)


@dataclass(frozen=True, slots=True)
class HeldoutRule:
    atoms: tuple[Atom, ...]


@dataclass(frozen=True, slots=True)
class HeldoutDomain:
    canonical_state: Mapping[str, str]
    field_values: Mapping[str, tuple[str, ...]]
    variants: Mapping[str, HeldoutRule]


@dataclass(frozen=True, slots=True)
class VariationCase:
    case_id: str
    domain: str
    variant: str
    split: str
    state: Mapping[str, str]
    expected: str


def load_heldout_rules(path: Path) -> dict[str, HeldoutDomain]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError("heldout rules schema_version must be 1")
    domains: dict[str, HeldoutDomain] = {}
    for domain_name, raw_domain in value["domains"].items():
        variants = {
            name: HeldoutRule(tuple(Atom(field, expected) for field, expected in rows))
            for name, rows in raw_domain["variants"].items()
        }
        domains[domain_name] = HeldoutDomain(
            canonical_state=dict(raw_domain["canonical_state"]),
            field_values={
                field: tuple(values)
                for field, values in raw_domain["field_values"].items()
            },
            variants=variants,
        )
    return domains


def validate_candidate_against_rules(
    candidates: Sequence[PlanVariationDomain],
    rules: Mapping[str, HeldoutDomain],
) -> None:
    candidate_domains = {domain.name: domain for domain in candidates}
    if set(candidate_domains) != set(rules):
        raise ValueError("candidate and heldout domain names differ")
    for domain_name, heldout in rules.items():
        candidate_names = {variant.name for variant in candidate_domains[domain_name].variants}
        if candidate_names != set(heldout.variants):
            raise ValueError(f"candidate and heldout variants differ: {domain_name}")
        if set(heldout.canonical_state) != set(heldout.field_values):
            raise ValueError(f"heldout state vocabulary differs: {domain_name}")
        for field, current in heldout.canonical_state.items():
            if current not in heldout.field_values[field]:
                raise ValueError(f"canonical value missing from vocabulary: {domain_name}/{field}")


def _is_safe(rule: HeldoutRule, state: Mapping[str, str]) -> bool:
    return all(state.get(atom.field) == atom.expected for atom in rule.atoms)


def _first_bad_value(
    heldout: HeldoutDomain, atom: Atom
) -> str:
    return next(value for value in heldout.field_values[atom.field] if value != atom.expected)


def build_cases(rules: Mapping[str, HeldoutDomain]) -> tuple[VariationCase, ...]:
    cases: list[VariationCase] = []
    seen: set[tuple[str, str, str, tuple[tuple[str, str], ...]]] = set()

    def add(
        domain_name: str,
        variant_name: str,
        split: str,
        state: Mapping[str, str],
        label: str,
    ) -> None:
        key = (domain_name, variant_name, split, tuple(sorted(state.items())))
        if key in seen:
            return
        seen.add(key)
        rule = rules[domain_name].variants[variant_name]
        expected = PROCEED if _is_safe(rule, state) else ABSTAIN
        cases.append(
            VariationCase(
                case_id=f"{domain_name}-{variant_name}-{label}-{len(cases):04d}",
                domain=domain_name,
                variant=variant_name,
                split=split,
                state=dict(state),
                expected=expected,
            )
        )

    for domain_name, heldout in rules.items():
        all_fields = set(heldout.canonical_state)
        for variant_name, rule in heldout.variants.items():
            base = dict(heldout.canonical_state)
            add(domain_name, variant_name, "canonical_safe", base, "canonical")

            for atom in rule.atoms:
                for alternative in heldout.field_values[atom.field]:
                    if alternative == atom.expected:
                        continue
                    mutated = dict(base)
                    mutated[atom.field] = alternative
                    add(
                        domain_name,
                        variant_name,
                        "single_obligation_faults",
                        mutated,
                        f"{atom.field}-{alternative}",
                    )

            required_fields = {atom.field for atom in rule.atoms}
            nuisance_fields = sorted(all_fields - required_fields)
            for field in nuisance_fields:
                for alternative in heldout.field_values[field]:
                    if alternative == base[field]:
                        continue
                    mutated = dict(base)
                    mutated[field] = alternative
                    add(
                        domain_name,
                        variant_name,
                        "safe_nuisance_variants",
                        mutated,
                        f"{field}-{alternative}",
                    )

            for left, right in combinations(rule.atoms, 2):
                mutated = dict(base)
                mutated[left.field] = _first_bad_value(heldout, left)
                mutated[right.field] = _first_bad_value(heldout, right)
                add(
                    domain_name,
                    variant_name,
                    "paired_obligation_faults",
                    mutated,
                    f"{left.field}-{right.field}",
                )

            if nuisance_fields:
                nuisance = nuisance_fields[0]
                nuisance_bad = next(
                    value
                    for value in heldout.field_values[nuisance]
                    if value != base[nuisance]
                )
                for atom in rule.atoms:
                    mutated = dict(base)
                    mutated[atom.field] = _first_bad_value(heldout, atom)
                    mutated[nuisance] = nuisance_bad
                    add(
                        domain_name,
                        variant_name,
                        "obligation_plus_nuisance_faults",
                        mutated,
                        f"{atom.field}-plus-{nuisance}",
                    )
    return tuple(cases)


def _find_variant(domain: PlanVariationDomain, name: str) -> PlanVariant:
    return next(variant for variant in domain.variants if variant.name == name)


def _run_method(
    method: str,
    domain: PlanVariationDomain,
    variant: PlanVariant,
    rule: HeldoutRule,
    state: Mapping[str, str],
    expected: str,
    compiled: CompiledObligations,
) -> GateResult:
    if method == "no_verification":
        return GateResult(method, PROCEED, expected, (), 0)
    if method == "fixed_target_readback":
        return run_atom_gate(
            method,
            (domain.fixed_target_atom,),
            domain.probes,
            state,
            expected=expected,
        )
    if method == "static_domain_contract":
        return run_atom_gate(
            method,
            domain.static_domain_atoms,
            domain.probes,
            state,
            expected=expected,
        )
    if method == "pdeo_direct_commit_only":
        return GateResult(method, ABSTAIN, expected, (), 0)
    if method == "pdeo":
        return run_compiled_gate(compiled, state, expected=expected, method=method)
    if method == "human_per_plan_minimal":
        return run_atom_gate(
            method,
            rule.atoms,
            domain.probes,
            state,
            expected=expected,
        )
    raise ValueError(f"unsupported method: {method}")


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _metric(
    name: str,
    value: float,
    *,
    unit: str,
    split: str,
    aggregation: str,
    n: int,
) -> dict[str, object]:
    return {
        "name": name,
        "value": value,
        "unit": unit,
        "split": split,
        "aggregation": aggregation,
        "n": n,
    }


def _corrupt_variant(variant: PlanVariant, omitted: Atom) -> PlanVariant:
    if len(variant.prefix_actions) != 1:
        raise ValueError("spec omission test expects one prefix action")
    current = variant.prefix_actions[0]
    reduced = tuple(atom for atom in current.preconditions if atom != omitted)
    corrupted = PlanAction(
        name=current.name + "_omitted",
        preconditions=reduced,
        effects=current.effects,
        trusted_deterministic=current.trusted_deterministic,
    )
    return PlanVariant(variant.name + "_omitted", (corrupted,), variant.protected_commit)


def run_formal(rules_path: Path) -> tuple[dict, dict]:
    started = time.perf_counter()
    domains = build_plan_variation_domains()
    validate_plan_variation_domains(domains)
    rules = load_heldout_rules(rules_path)
    validate_candidate_against_rules(domains, rules)
    domain_by_name = {domain.name: domain for domain in domains}

    compiled: dict[tuple[str, str], CompiledObligations] = {}
    exact_atom_matches: list[float] = []
    exact_probe_matches: list[float] = []
    plan_cost_rows: list[dict[str, object]] = []
    for domain in domains:
        heldout = rules[domain.name]
        static_probes = minimum_cost_probe_cover(domain.static_domain_atoms, domain.probes)
        static_cost = sum(probe.cost for probe in static_probes)
        for variant in domain.variants:
            key = (domain.name, variant.name)
            item = compile_obligations(
                variant.prefix_actions, variant.protected_commit, domain.probes
            )
            compiled[key] = item
            rule = heldout.variants[variant.name]
            oracle_probes = minimum_cost_probe_cover(rule.atoms, domain.probes)
            exact_atom_matches.append(float(set(item.atoms) == set(rule.atoms)))
            exact_probe_matches.append(
                float(
                    {probe.name for probe in item.probes}
                    == {probe.name for probe in oracle_probes}
                )
            )
            plan_cost_rows.append(
                {
                    "domain": domain.name,
                    "variant": variant.name,
                    "pdeo_cost": item.total_cost,
                    "static_domain_cost": static_cost,
                    "compiled_atoms": [
                        [atom.field, atom.expected] for atom in item.atoms
                    ],
                    "heldout_atoms": [
                        [atom.field, atom.expected] for atom in rule.atoms
                    ],
                    "compiled_probes": [probe.name for probe in item.probes],
                    "oracle_probes": [probe.name for probe in oracle_probes],
                }
            )

    cases = build_cases(rules)
    rows: list[dict[str, object]] = []
    for case in cases:
        domain = domain_by_name[case.domain]
        variant = _find_variant(domain, case.variant)
        rule = rules[case.domain].variants[case.variant]
        for method in METHODS:
            result = _run_method(
                method,
                domain,
                variant,
                rule,
                case.state,
                case.expected,
                compiled[(case.domain, case.variant)],
            )
            rows.append(
                {
                    "case_id": case.case_id,
                    "domain": case.domain,
                    "variant": case.variant,
                    "split": case.split,
                    "state": dict(case.state),
                    "method": method,
                    "selected": result.selected,
                    "expected": case.expected,
                    "correct": result.correct,
                    "unsafe_commit": result.unsafe_commit,
                    "probe_cost": result.probe_cost,
                    "probes": list(result.probe_names),
                }
            )

    omission_rows: list[dict[str, object]] = []
    for domain in domains:
        heldout = rules[domain.name]
        for variant in domain.variants:
            rule = heldout.variants[variant.name]
            omitted = rule.atoms[0]
            corrupted = _corrupt_variant(variant, omitted)
            corrupted_compiled = compile_obligations(
                corrupted.prefix_actions, corrupted.protected_commit, domain.probes
            )
            state = dict(heldout.canonical_state)
            state[omitted.field] = _first_bad_value(heldout, omitted)
            result = run_compiled_gate(
                corrupted_compiled, state, expected=ABSTAIN, method="pdeo_spec_omission"
            )
            omission_rows.append(
                {
                    "domain": domain.name,
                    "variant": variant.name,
                    "omitted_atom": [omitted.field, omitted.expected],
                    "state": state,
                    "compiled_atoms": [
                        [atom.field, atom.expected] for atom in corrupted_compiled.atoms
                    ],
                    "selected": result.selected,
                    "unsafe_commit": result.unsafe_commit,
                }
            )

    records: list[dict[str, object]] = [
        _metric(
            "pdeo_compiled_obligation_exact_match_rate",
            _mean(exact_atom_matches),
            unit="proportion",
            split="heldout_plan_variants",
            aggregation="plan_mean",
            n=len(exact_atom_matches),
        ),
        _metric(
            "pdeo_compiled_probe_set_exact_match_rate",
            _mean(exact_probe_matches),
            unit="proportion",
            split="heldout_plan_variants",
            aggregation="plan_mean",
            n=len(exact_probe_matches),
        ),
        _metric(
            "pdeo_mean_plan_probe_cost",
            _mean([float(row["pdeo_cost"]) for row in plan_cost_rows]),
            unit="cost_units",
            split="heldout_plan_variants",
            aggregation="plan_mean",
            n=len(plan_cost_rows),
        ),
        _metric(
            "static_domain_contract_mean_plan_probe_cost",
            _mean([float(row["static_domain_cost"]) for row in plan_cost_rows]),
            unit="cost_units",
            split="heldout_plan_variants",
            aggregation="plan_mean",
            n=len(plan_cost_rows),
        ),
        _metric(
            "pdeo_spec_omission_unsafe_commit_rate",
            _mean([float(row["unsafe_commit"]) for row in omission_rows]),
            unit="proportion",
            split="specification_omission_sensitivity",
            aggregation="plan_mean",
            n=len(omission_rows),
        ),
    ]

    splits = sorted({case.split for case in cases})
    for split in splits:
        for method in METHODS:
            subset = [
                row
                for row in rows
                if row["split"] == split and row["method"] == method
            ]
            safe = [row for row in subset if row["expected"] == PROCEED]
            records.extend(
                [
                    _metric(
                        f"{method}_unsafe_commit_rate_{split}",
                        _mean([float(row["unsafe_commit"]) for row in subset]),
                        unit="proportion",
                        split=split,
                        aggregation="case_mean",
                        n=len(subset),
                    ),
                    _metric(
                        f"{method}_gate_accuracy_{split}",
                        _mean([float(row["correct"]) for row in subset]),
                        unit="proportion",
                        split=split,
                        aggregation="case_mean",
                        n=len(subset),
                    ),
                    _metric(
                        f"{method}_average_probe_cost_{split}",
                        _mean([float(row["probe_cost"]) for row in subset]),
                        unit="cost_units",
                        split=split,
                        aggregation="case_mean",
                        n=len(subset),
                    ),
                ]
            )
            if safe:
                records.append(
                    _metric(
                        f"{method}_valid_commit_recall_{split}",
                        _mean(
                            [float(row["selected"] == PROCEED) for row in safe]
                        ),
                        unit="proportion",
                        split=split,
                        aggregation="case_mean",
                        n=len(safe),
                    )
                )

    for domain_name in sorted(rules):
        plan_rows = [row for row in plan_cost_rows if row["domain"] == domain_name]
        records.extend(
            [
                _metric(
                    f"pdeo_mean_plan_probe_cost_{domain_name}",
                    _mean([float(row["pdeo_cost"]) for row in plan_rows]),
                    unit="cost_units",
                    split=f"domain:{domain_name}",
                    aggregation="plan_mean",
                    n=len(plan_rows),
                ),
                _metric(
                    f"static_domain_contract_mean_plan_probe_cost_{domain_name}",
                    _mean([float(row["static_domain_cost"]) for row in plan_rows]),
                    unit="cost_units",
                    split=f"domain:{domain_name}",
                    aggregation="plan_mean",
                    n=len(plan_rows),
                ),
            ]
        )
        for method in ("static_domain_contract", "pdeo", "human_per_plan_minimal"):
            faults = [
                row
                for row in rows
                if row["domain"] == domain_name
                and row["method"] == method
                and row["split"]
                in {
                    "single_obligation_faults",
                    "paired_obligation_faults",
                    "obligation_plus_nuisance_faults",
                }
            ]
            safe_nuisance = [
                row
                for row in rows
                if row["domain"] == domain_name
                and row["method"] == method
                and row["split"] == "safe_nuisance_variants"
            ]
            records.extend(
                [
                    _metric(
                        f"{method}_unsafe_commit_rate_all_faults_{domain_name}",
                        _mean([float(row["unsafe_commit"]) for row in faults]),
                        unit="proportion",
                        split=f"domain:{domain_name}",
                        aggregation="fault_case_mean",
                        n=len(faults),
                    ),
                    _metric(
                        f"{method}_valid_commit_recall_safe_nuisance_{domain_name}",
                        _mean(
                            [
                                float(row["selected"] == PROCEED)
                                for row in safe_nuisance
                            ]
                        ),
                        unit="proportion",
                        split=f"domain:{domain_name}",
                        aggregation="safe_case_mean",
                        n=len(safe_nuisance),
                    ),
                ]
            )

    metrics = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "records": records,
        "resource_usage": {
            "tokens": 0,
            "api_calls": 0,
            "wall_time_seconds": time.perf_counter() - started,
            "gpu_time_seconds": 0,
            "estimated_cost": 0,
        },
        "errors": [],
        "warnings": [
            "Heldout rules are byte-frozen in a separate declared input, but were authored within the same Run rather than by an external team.",
            "All domains remain synthetic and all read probes are deterministic and noise-free.",
            "Specification omission sensitivity is an expected failure test outside the correct-specification claim scope."
        ],
    }
    details = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "rules_path": str(rules_path),
        "case_count": len(cases),
        "cases_by_split": {
            split: sum(case.split == split for case in cases) for split in splits
        },
        "plan_cost_and_exactness": plan_cost_rows,
        "specification_omission_rows": omission_rows,
        "rows": rows,
    }
    return metrics, details


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules-input", type=Path, required=True)
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--details-output", type=Path, required=True)
    args = parser.parse_args()
    metrics, details = run_formal(args.rules_input)
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
    wanted = {
        "pdeo_compiled_obligation_exact_match_rate",
        "pdeo_compiled_probe_set_exact_match_rate",
        "pdeo_mean_plan_probe_cost",
        "static_domain_contract_mean_plan_probe_cost",
        "pdeo_spec_omission_unsafe_commit_rate",
        "pdeo_unsafe_commit_rate_single_obligation_faults",
        "pdeo_valid_commit_recall_safe_nuisance_variants",
        "static_domain_contract_valid_commit_recall_safe_nuisance_variants",
    }
    print(
        json.dumps(
            {
                "experiment_id": EXPERIMENT_ID,
                "case_count": details["case_count"],
                "key_records": [
                    record for record in metrics["records"] if record["name"] in wanted
                ],
                "warnings": metrics["warnings"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
