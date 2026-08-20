from __future__ import annotations

import argparse
import json
import random
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from dqbp_core import run_episode, sample_branch
from obligation_bench import (
    ObligationDomain,
    build_obligation_domains,
    expected_gate,
    validate_obligation_domains,
)
from obligation_core import (
    ABSTAIN,
    PROCEED,
    Atom,
    CompiledObligations,
    GateResult,
    compile_obligations,
    run_atom_gate,
    run_compiled_gate,
)


METHODS = (
    "no_verification",
    "static_receipt",
    "fixed_target_readback",
    "tool_local_contract",
    "state_information_gain",
    "dqbp",
    "pdeo",
    "full_readback",
    "human_minimal_obligations",
)


def _adaptive_gate(
    domain: ObligationDomain,
    branch,
    method: str,
    *,
    budget: int,
    rng: random.Random,
) -> GateResult:
    raw = run_episode(
        domain.branch_model,
        branch,
        method=method,
        budget=budget,
        rng=rng,
    )
    selected = PROCEED if raw.selected_decision == PROCEED else ABSTAIN
    return GateResult(
        method=method,
        selected=selected,
        expected=expected_gate(branch),
        probe_names=raw.probes,
        probe_cost=raw.probe_cost,
    )


def _run_method(
    domain: ObligationDomain,
    branch,
    method: str,
    *,
    budget: int,
    rng: random.Random,
    compiled: CompiledObligations | None = None,
) -> GateResult:
    expected = expected_gate(branch)
    state = branch.observations
    if compiled is None:
        compiled = compile_obligations(
            domain.prefix_actions, domain.protected_commit, domain.probes
        )
    if method in {"no_verification", "static_receipt"}:
        return GateResult(method, PROCEED, expected, (), 0)
    if method == "fixed_target_readback":
        return run_atom_gate(
            method,
            (domain.target_atom,),
            domain.probes,
            state,
            expected=expected,
        )
    if method == "tool_local_contract":
        return run_atom_gate(
            method,
            domain.tool_contract_atoms,
            domain.probes,
            state,
            expected=expected,
        )
    if method in {"state_information_gain", "dqbp"}:
        return _adaptive_gate(domain, branch, method, budget=budget, rng=rng)
    if method == "pdeo":
        return run_compiled_gate(compiled, state, expected=expected, method=method)
    if method == "full_readback":
        required = compiled.atoms
        selected = PROCEED if all(
            state.get(atom.field) == atom.expected for atom in required
        ) else ABSTAIN
        return GateResult(
            method,
            selected,
            expected,
            tuple(probe.name for probe in domain.probes),
            sum(probe.cost for probe in domain.probes),
        )
    if method == "human_minimal_obligations":
        return run_atom_gate(
            method,
            compiled.atoms,
            domain.probes,
            state,
            expected=expected,
        )
    raise ValueError(f"unsupported method: {method}")


def _sample(
    domain: ObligationDomain,
    rng: random.Random,
    *,
    condition: str,
):
    if condition == "known":
        return sample_branch(domain.branch_model, rng, condition="in_distribution")
    if condition == "open_world":
        return rng.choice(domain.unseen_faults)
    if condition == "mixed":
        if rng.random() < 0.2:
            return rng.choice(domain.unseen_faults)
        return sample_branch(domain.branch_model, rng, condition="in_distribution")
    raise ValueError(f"unsupported condition: {condition}")


def _mean(values: Iterable[float]) -> float:
    values = tuple(values)
    return sum(values) / len(values) if values else 0.0


def run_experiment(
    *, episodes_per_domain: int, budget: int, seed: int
) -> tuple[dict, dict]:
    domains = build_obligation_domains()
    validate_obligation_domains(domains)
    rng = random.Random(seed)
    started = time.perf_counter()
    rows: list[dict] = []
    trace_counts: dict[str, Counter] = defaultdict(Counter)
    compiled_by_domain = {
        domain.name: compile_obligations(
            domain.prefix_actions, domain.protected_commit, domain.probes
        )
        for domain in domains
    }

    for condition in ("known", "open_world", "mixed"):
        for domain in domains:
            for _ in range(episodes_per_domain):
                branch = _sample(domain, rng, condition=condition)
                for method in METHODS:
                    result = _run_method(
                        domain,
                        branch,
                        method,
                        budget=budget,
                        rng=rng,
                        compiled=compiled_by_domain[domain.name],
                    )
                    rows.append(
                        {
                            "condition": condition,
                            "domain": domain.name,
                            "branch": branch.name,
                            "method": method,
                            "selected": result.selected,
                            "expected": result.expected,
                            "correct": result.correct,
                            "unsafe_commit": result.unsafe_commit,
                            "valid_commit": result.selected == PROCEED
                            and result.expected == PROCEED,
                            "probe_cost": result.probe_cost,
                            "probes": list(result.probe_names),
                        }
                    )
                    key = f"{condition}/{domain.name}/{method}"
                    trace_counts[key][result.probe_names] += 1

    summaries = []
    for condition in ("known", "open_world", "mixed"):
        for method in METHODS:
            subset = [
                row
                for row in rows
                if row["condition"] == condition and row["method"] == method
            ]
            valid = [row for row in subset if row["expected"] == PROCEED]
            summaries.append(
                {
                    "condition": condition,
                    "method": method,
                    "n": len(subset),
                    "gate_accuracy": _mean(float(row["correct"]) for row in subset),
                    "unsafe_commit_rate": _mean(
                        float(row["unsafe_commit"]) for row in subset
                    ),
                    "valid_commit_recall": _mean(
                        float(row["selected"] == PROCEED) for row in valid
                    )
                    if valid
                    else None,
                    "average_probe_cost": _mean(
                        float(row["probe_cost"]) for row in subset
                    ),
                }
            )

    metrics = {
        "schema_version": 1,
        "experiment_id": "pdeo-controller-v1",
        "episodes_per_domain": episodes_per_domain,
        "budget": budget,
        "seed": seed,
        "summaries": summaries,
        "resource_usage": {
            "tokens": 0,
            "api_calls": 0,
            "wall_time_seconds": time.perf_counter() - started,
            "gpu_time_seconds": 0,
            "estimated_cost": 0,
        },
        "warnings": [
            "Controller-isolation experiment over typed plans; natural-language plan extraction is not evaluated."
        ],
    }
    details = {
        "schema_version": 1,
        "experiment_id": "pdeo-controller-v1",
        "trace_counts": {
            key: [
                {"probes": list(trace), "count": count}
                for trace, count in counter.most_common()
            ]
            for key, counter in sorted(trace_counts.items())
        },
        "domain_specs": [
            {
                "name": domain.name,
                "obligations": [
                    {"field": atom.field, "expected": atom.expected}
                    for atom in compile_obligations(
                        domain.prefix_actions,
                        domain.protected_commit,
                        domain.probes,
                    ).atoms
                ],
                "tool_contract_atoms": [
                    {"field": atom.field, "expected": atom.expected}
                    for atom in domain.tool_contract_atoms
                ],
                "unseen_faults": [fault.name for fault in domain.unseen_faults],
            }
            for domain in domains
        ],
    }
    return metrics, details


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes-per-domain", type=int, default=10000)
    parser.add_argument("--budget", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260813)
    parser.add_argument("--metrics-out", type=Path, required=True)
    parser.add_argument("--details-out", type=Path, required=True)
    args = parser.parse_args()
    metrics, details = run_experiment(
        episodes_per_domain=args.episodes_per_domain,
        budget=args.budget,
        seed=args.seed,
    )
    args.metrics_out.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    args.details_out.write_text(
        json.dumps(details, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
