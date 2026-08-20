"""Independent hidden-fault benchmark for effect-witness verification.

The terminal oracle and concrete state transitions are deliberately implemented
here rather than imported from the method module.  Labels depend on final state,
not on witness predicates.
"""

from __future__ import annotations

import argparse
import copy
import json
import random
import statistics
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

from effect_witness import (
    EffectIntent,
    EffectRecord,
    compile_witness,
    predicate_names,
    weak_positive_witness,
)


DOMAINS: dict[str, dict[str, tuple[Any, ...]]] = {
    "airline": {
        "status": ("booked", "checked_in", "cancelled"),
        "cabin": ("economy", "premium", "business"),
        "passengers": (1, 2, 3, 4),
        "meal": ("standard", "vegetarian", "halal"),
    },
    "retail": {
        "status": ("ordered", "shipped", "return_requested", "refunded"),
        "quantity": (1, 2, 3, 4),
        "channel": ("store", "courier", "locker"),
        "priority": ("normal", "expedited"),
    },
    "calendar": {
        "status": ("tentative", "confirmed", "cancelled"),
        "duration": (15, 30, 45, 60),
        "visibility": ("private", "team", "public"),
        "reminder": (0, 5, 10, 30),
    },
}

FAULTS = (
    "honest",
    "noop_ack",
    "partial_ack",
    "wrong_target_ack",
    "duplicate_effect_ack",
    "spillover_ack",
    "rollback_after_ack",
)


@dataclass
class Operation:
    domain: str
    nonce: str
    target_id: str
    expected_fields: dict[str, Any]


@dataclass
class Event:
    nonce: str
    record_id: str


@dataclass
class Trial:
    operation: Operation
    before: dict[str, dict[str, Any]]
    after: dict[str, dict[str, Any]]
    events: list[Event]
    output: dict[str, Any]
    fault: str


@dataclass
class Decision:
    accepted: bool
    read_calls: int
    returned_scalars: int


def make_records(domain: str, rng: random.Random, count: int = 24) -> dict[str, dict[str, Any]]:
    schema = DOMAINS[domain]
    records: dict[str, dict[str, Any]] = {}
    for index in range(count):
        records[f"{domain}-{index:03d}"] = {
            field: rng.choice(values) for field, values in schema.items()
        }
    return records


def make_operation(domain: str, records: dict[str, dict[str, Any]], rng: random.Random, seq: int) -> Operation:
    target_id = rng.choice(sorted(records))
    schema = DOMAINS[domain]
    fields = rng.sample(sorted(schema), k=rng.randint(2, len(schema)))
    expected: dict[str, Any] = {}
    for field in fields:
        alternatives = [value for value in schema[field] if value != records[target_id][field]]
        expected[field] = rng.choice(alternatives)
    return Operation(
        domain=domain,
        nonce=f"{domain}-nonce-{seq:06d}-{rng.getrandbits(48):012x}",
        target_id=target_id,
        expected_fields=expected,
    )


def execute_hidden_fault(
    records: dict[str, dict[str, Any]], operation: Operation, fault: str, rng: random.Random
) -> Trial:
    before = copy.deepcopy(records)
    after = copy.deepcopy(records)
    events: list[Event] = []

    def apply(record_id: str, updates: dict[str, Any]) -> None:
        after[record_id].update(updates)
        events.append(Event(operation.nonce, record_id))

    if fault == "honest":
        apply(operation.target_id, operation.expected_fields)
    elif fault == "noop_ack":
        pass
    elif fault == "partial_ack":
        keys = sorted(operation.expected_fields)
        omitted = rng.choice(keys)
        apply(
            operation.target_id,
            {key: value for key, value in operation.expected_fields.items() if key != omitted},
        )
    elif fault == "wrong_target_ack":
        wrong = rng.choice([key for key in sorted(after) if key != operation.target_id])
        apply(wrong, operation.expected_fields)
    elif fault == "duplicate_effect_ack":
        apply(operation.target_id, operation.expected_fields)
        events.append(Event(operation.nonce, operation.target_id))
    elif fault == "spillover_ack":
        apply(operation.target_id, operation.expected_fields)
        other = rng.choice([key for key in sorted(after) if key != operation.target_id])
        field = rng.choice(sorted(DOMAINS[operation.domain]))
        alternatives = [
            value
            for value in DOMAINS[operation.domain][field]
            if value != after[other][field]
        ]
        apply(other, {field: rng.choice(alternatives)})
    elif fault == "rollback_after_ack":
        apply(operation.target_id, operation.expected_fields)
        rollback_field = rng.choice(sorted(operation.expected_fields))
        after[operation.target_id][rollback_field] = before[operation.target_id][rollback_field]
    else:
        raise ValueError(f"unknown fault: {fault}")

    output = {
        "ok": True,
        "nonce": operation.nonce,
        "target_id": operation.target_id,
        "message": "operation completed",
    }
    return Trial(operation, before, after, events, output, fault)


def terminal_success(trial: Trial) -> bool:
    """Independent terminal label: exact intended delta and no other effects."""

    operation = trial.operation
    related = [event for event in trial.events if event.nonce == operation.nonce]
    if len(related) != 1 or related[0].record_id != operation.target_id:
        return False
    target = trial.after[operation.target_id]
    if any(target.get(field) != value for field, value in operation.expected_fields.items()):
        return False
    for record_id, old_record in trial.before.items():
        if record_id == operation.target_id:
            allowed = dict(old_record)
            allowed.update(operation.expected_fields)
            if trial.after[record_id] != allowed:
                return False
        elif trial.after[record_id] != old_record:
            return False
    return True


def read_target(trial: Trial) -> tuple[dict[str, Any], int]:
    record = trial.after[trial.operation.target_id]
    return record, len(record) + 1


def read_by_nonce(trial: Trial, corrupt: bool = False) -> tuple[list[EffectRecord], int]:
    if corrupt:
        forged = dict(trial.after[trial.operation.target_id])
        forged.update(trial.operation.expected_fields)
        return [EffectRecord(trial.operation.target_id, forged)], len(forged) + 1
    rows = [
        EffectRecord(event.record_id, dict(trial.after[event.record_id]))
        for event in trial.events
        if event.nonce == trial.operation.nonce
    ]
    scalars = sum(len(row.current) + 1 for row in rows)
    return rows, scalars


def verify_output(trial: Trial) -> Decision:
    return Decision(bool(trial.output.get("ok")), 0, 0)


def verify_schema_contract(trial: Trial) -> Decision:
    output = trial.output
    accepted = (
        output.get("ok") is True
        and isinstance(output.get("message"), str)
        and output.get("nonce") == trial.operation.nonce
        and output.get("target_id") == trial.operation.target_id
    )
    return Decision(accepted, 0, 0)


def verify_target_postread(trial: Trial) -> Decision:
    row, scalars = read_target(trial)
    accepted = all(
        row.get(field) == value for field, value in trial.operation.expected_fields.items()
    )
    return Decision(accepted, 1, scalars)


def _intent(trial: Trial) -> EffectIntent:
    return EffectIntent(
        nonce=trial.operation.nonce,
        target_id=trial.operation.target_id,
        expected_fields=trial.operation.expected_fields,
    )


def verify_weak_nonce(trial: Trial) -> Decision:
    rows, scalars = read_by_nonce(trial)
    return Decision(weak_positive_witness(_intent(trial), rows), 1, scalars)


def verify_compiled_witness(trial: Trial, corrupt_read: bool = False) -> Decision:
    rows, scalars = read_by_nonce(trial, corrupt=corrupt_read)
    compiled = compile_witness(_intent(trial))
    return Decision(compiled.verify(rows), 1, scalars)


def verify_full_snapshot(trial: Trial) -> Decision:
    scalar_count = sum(len(record) + 1 for record in trial.after.values()) + 2 * len(trial.events)
    return Decision(terminal_success(trial), 1, scalar_count)


VERIFIERS: dict[str, Callable[[Trial], Decision]] = {
    "output_trust": verify_output,
    "schema_contract": verify_schema_contract,
    "target_postread": verify_target_postread,
    "weak_nonce_witness": verify_weak_nonce,
    "compiled_mutation_sufficient_witness": verify_compiled_witness,
    "full_snapshot_oracle": verify_full_snapshot,
}


def run(seed: int, trials_per_domain: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = random.Random(seed)
    rows: list[dict[str, Any]] = []
    compile_samples: dict[str, Any] = {}
    sequence = 0
    for domain in sorted(DOMAINS):
        records = make_records(domain, rng)
        for _ in range(trials_per_domain):
            sequence += 1
            operation = make_operation(domain, records, rng, sequence)
            fault = rng.choice(FAULTS)
            trial = execute_hidden_fault(records, operation, fault, rng)
            truth = terminal_success(trial)
            for verifier_name, verifier in VERIFIERS.items():
                decision = verifier(trial)
                rows.append(
                    {
                        "seed": seed,
                        "domain": domain,
                        "fault": fault,
                        "verifier": verifier_name,
                        "truth": truth,
                        "accepted": decision.accepted,
                        "read_calls": decision.read_calls,
                        "returned_scalars": decision.returned_scalars,
                    }
                )
            if domain not in compile_samples:
                compiled = compile_witness(_intent(trial))
                compile_samples[domain] = {
                    "coverage": compiled.coverage,
                    "killed_mutants": compiled.killed_mutants,
                    "total_mutants": compiled.total_mutants,
                    "selected_predicates": predicate_names(compiled),
                }
    return rows, compile_samples


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["verifier"]].append(row)
    summary: dict[str, Any] = {}
    for verifier, items in sorted(grouped.items()):
        failures = [item for item in items if not item["truth"]]
        successes = [item for item in items if item["truth"]]
        unsafe = sum(item["accepted"] for item in failures)
        accepted_success = sum(item["accepted"] for item in successes)
        by_fault: dict[str, float] = {}
        for fault in FAULTS:
            fault_failures = [
                item for item in failures if item["fault"] == fault
            ]
            if fault_failures:
                by_fault[fault] = sum(item["accepted"] for item in fault_failures) / len(
                    fault_failures
                )
        summary[verifier] = {
            "trials": len(items),
            "failure_trials": len(failures),
            "success_trials": len(successes),
            "unsafe_accept_rate": unsafe / len(failures) if failures else 0.0,
            "normal_accept_rate": accepted_success / len(successes) if successes else 0.0,
            "mean_read_calls": statistics.fmean(item["read_calls"] for item in items),
            "mean_returned_scalars": statistics.fmean(
                item["returned_scalars"] for item in items
            ),
            "unsafe_accept_rate_by_fault": by_fault,
        }
    return summary


def trust_boundary_negative_controls(seed: int, cases: int) -> dict[str, Any]:
    rng = random.Random(seed ^ 0xC0FFEE)
    forged_read_accepted = 0
    unattributed_spillover_accepted = 0
    for index in range(cases):
        domain = rng.choice(sorted(DOMAINS))
        records = make_records(domain, rng)
        operation = make_operation(domain, records, rng, index)
        trial = execute_hidden_fault(records, operation, "noop_ack", rng)
        decision = verify_compiled_witness(trial, corrupt_read=True)
        forged_read_accepted += int(decision.accepted)

        spillover = execute_hidden_fault(records, operation, "honest", rng)
        other = rng.choice(
            [key for key in sorted(spillover.after) if key != operation.target_id]
        )
        field = rng.choice(sorted(DOMAINS[domain]))
        alternatives = [
            value
            for value in DOMAINS[domain][field]
            if value != spillover.after[other][field]
        ]
        spillover.after[other][field] = rng.choice(alternatives)
        assert not terminal_success(spillover)
        unattributed_spillover_accepted += int(
            verify_compiled_witness(spillover).accepted
        )
    return {
        "cases": cases,
        "forged_nonce_read": {
            "fault": "noop_ack_with_forged_nonce_read",
            "unsafe_accept_rate": forged_read_accepted / cases,
        },
        "unattributed_spillover": {
            "fault": "correct_target_plus_unattributed_collateral_mutation",
            "unsafe_accept_rate": unattributed_spillover_accepted / cases,
        },
        "expected_interpretation": (
            "a trustworthy current-state read and complete nonce propagation to every "
            "caused durable effect are necessary external premises"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--trials-per-domain", type=int, default=600)
    parser.add_argument("--negative-control-cases", type=int, default=600)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.seeds <= 0 or args.trials_per_domain <= 0 or args.negative_control_cases <= 0:
        parser.error("all counts must be positive")

    all_rows: list[dict[str, Any]] = []
    compile_samples: dict[str, Any] = {}
    per_seed: list[dict[str, Any]] = []
    fault_counts: Counter[str] = Counter()
    for seed in range(args.seeds):
        rows, samples = run(seed, args.trials_per_domain)
        all_rows.extend(rows)
        compile_samples.update(samples)
        per_seed.append({"seed": seed, "summary": summarize(rows)})
        fault_counts.update(
            row["fault"] for row in rows if row["verifier"] == "output_trust"
        )

    payload = {
        "schema_version": 1,
        "experiment": "mutation-sufficient causally bound effect witnesses",
        "configuration": {
            "seeds": args.seeds,
            "trials_per_domain": args.trials_per_domain,
            "domains": sorted(DOMAINS),
            "faults": list(FAULTS),
            "records_per_trial": 24,
        },
        "fault_counts": dict(sorted(fault_counts.items())),
        "compiler_samples": compile_samples,
        "aggregate": summarize(all_rows),
        "per_seed": per_seed,
        "negative_control": trust_boundary_negative_controls(
            seed=args.seeds, cases=args.negative_control_cases
        ),
        "independence_note": (
            "terminal labels and concrete process faults are implemented in run_benchmark.py; "
            "the compiler sees only abstract relation mutants in effect_witness.py"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(payload["aggregate"], ensure_ascii=False, sort_keys=True))
    print(json.dumps(payload["negative_control"], ensure_ascii=False, sort_keys=True))
    print(json.dumps(payload["compiler_samples"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
