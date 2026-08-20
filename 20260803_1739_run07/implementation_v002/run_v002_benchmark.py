"""Independent evaluation for mutation-audited effect-frame witnesses.

Concrete state-process faults and terminal labels live in this file.  The
method module contributes only abstract mutants, feature projection and the
compiler.  The benchmark intentionally includes a strong manual exact
postcondition and preserves trust-boundary failures as negative controls.
"""

from __future__ import annotations

import argparse
import copy
import json
import random
import sqlite3
import statistics
import tempfile
import time
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from effect_frame_compiler import (
    ALL_FEATURES,
    FEATURE_COSTS,
    EffectEvent,
    EffectSpec,
    EffectTrace,
    UnwitnessableEffect,
    canonical_trace,
    compile_witness,
    direct_exact_available,
)


SCHEMAS: dict[str, dict[str, tuple[Any, ...]]] = {
    "calendar": {
        "title": ("review", "planning", "sync"),
        "visibility": ("private", "team", "public"),
        "duration": (15, 30, 60),
        "reminder": (0, 5, 15),
        "room": ("A", "B", "remote"),
    },
    "retail": {
        "status": ("ordered", "shipped", "returned"),
        "quantity": (1, 2, 3),
        "priority": ("normal", "expedited", "hold"),
        "channel": ("store", "locker", "courier"),
        "refund": (0, 10, 20),
    },
    "airline": {
        "status": ("booked", "checked_in", "cancelled"),
        "cabin": ("economy", "premium", "business"),
        "passengers": (1, 2, 3),
        "meal": ("standard", "vegetarian", "halal"),
        "seat": ("aisle", "window", "middle"),
    },
    "crm": {
        "stage": ("lead", "qualified", "won"),
        "owner": ("alice", "bob", "carol"),
        "priority": ("low", "medium", "high"),
        "consent": (True, False),
        "region": ("east", "west", "central"),
    },
}

HIDDEN_FAULTS = (
    "honest",
    "ack_without_write",
    "payload_drift",
    "different_object",
    "coalesced_replay",
    "sidecar_mutation",
    "hidden_attribute_flip",
    "attribute_erasure",
    "tombstone_cycle",
    "precheck_reversion",
    "compound_frame_and_replay",
)


def _different(value: Any, choices: Iterable[Any] = ()) -> Any:
    for choice in choices:
        if choice != value:
            return choice
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    return f"drift::{value}"


def make_spec(domain: str, operation: str, rng: random.Random, index: int) -> EffectSpec:
    schema = SCHEMAS[domain]
    target = f"{domain}-{index:05d}"
    before = {field: rng.choice(values) for field, values in schema.items()}
    if operation == "create":
        updates = {field: rng.choice(values) for field, values in schema.items()}
        prior = None
    elif operation == "delete":
        updates = {}
        prior = before
    else:
        changed = rng.sample(sorted(schema), k=rng.randint(1, 2))
        updates = {
            field: _different(before[field], schema[field]) for field in changed
        }
        prior = before
    return EffectSpec(
        nonce=f"{domain}-{operation}-{index:05d}-{rng.getrandbits(48):012x}",
        operation=operation,
        target_id=target,
        schema_fields=tuple(sorted(schema)),
        allowed_updates=updates,
        before=prior,
    )


def terminal_success(spec: EffectSpec, trace: EffectTrace) -> bool:
    """Strict process oracle, implemented without method predicates."""

    if len(trace.events) != 1:
        return False
    event = trace.events[0]
    desired = spec.desired()
    if event.nonce != spec.nonce or event.target_id != spec.target_id:
        return False
    if event.kind != spec.operation or event.ordinal != 1:
        return False
    if event.before != spec.before or event.after != desired:
        return False
    if trace.current_exists != (desired is not None):
        return False
    if trace.current != desired:
        return False
    if event.commit_version != trace.current_version:
        return False
    return True


def _event(event: EffectEvent, **updates: Any) -> EffectEvent:
    payload = asdict(event)
    payload.update(updates)
    return EffectEvent(**payload)


def concrete_hidden_fault(spec: EffectSpec, fault: str, rng: random.Random) -> EffectTrace:
    correct = canonical_trace(spec)
    event = correct.events[0]
    desired = spec.desired()
    if fault == "honest":
        return correct
    if fault == "ack_without_write":
        return EffectTrace((), spec.before is not None, spec.before, 10)
    if fault == "payload_drift":
        if desired is None:
            return EffectTrace(
                (_event(event, kind="update", after=spec.before),),
                True,
                spec.before,
                11,
            )
        field = rng.choice(sorted(desired))
        changed = dict(desired)
        changed[field] = _different(changed[field], SCHEMAS[next(d for d in SCHEMAS if spec.target_id.startswith(d))][field])
        return EffectTrace((_event(event, after=changed),), True, changed, 11)
    if fault == "different_object":
        return EffectTrace(
            (_event(event, target_id=f"other-{spec.target_id}"),),
            correct.current_exists,
            correct.current,
            11,
        )
    if fault == "coalesced_replay":
        return EffectTrace(
            (event, _event(event, ordinal=2)),
            correct.current_exists,
            correct.current,
            11,
        )
    if fault == "sidecar_mutation":
        return EffectTrace(
            (event, _event(event, target_id=f"sidecar-{spec.target_id}", ordinal=2)),
            correct.current_exists,
            correct.current,
            11,
        )
    if fault in {"hidden_attribute_flip", "attribute_erasure", "compound_frame_and_replay"}:
        if desired is None:
            return EffectTrace(
                (event, _event(event, kind="create", before=None, after=spec.before, ordinal=2)),
                True,
                spec.before,
                12,
            )
        frame = list(spec.frame_fields) or list(spec.schema_fields)
        field = rng.choice(frame)
        changed = dict(desired)
        if fault == "attribute_erasure":
            changed.pop(field, None)
        else:
            domain = next(d for d in SCHEMAS if spec.target_id.startswith(d))
            changed[field] = _different(changed.get(field), SCHEMAS[domain][field])
        events = (_event(event, after=changed),)
        if fault == "compound_frame_and_replay":
            events = (events[0], _event(events[0], ordinal=2))
        return EffectTrace(events, True, changed, 11)
    if fault == "tombstone_cycle":
        return EffectTrace(
            (
                _event(event, kind="delete", after=None, ordinal=1),
                _event(event, kind="create", before=None, after=desired, ordinal=2),
            ),
            desired is not None,
            desired,
            11,
        )
    if fault == "precheck_reversion":
        reverted = spec.before
        return EffectTrace(correct.events, reverted is not None, reverted, 12)
    raise ValueError(fault)


def manual_complete_postcondition(spec: EffectSpec, trace: EffectTrace) -> bool:
    """Strong full-evidence baseline; deliberately independent of compiler."""

    return terminal_success(spec, trace)


def schema_direct_witness(spec: EffectSpec, trace: EffectTrace) -> bool:
    """Direct contract generator with no frame, multiplicity, or stability audit."""

    if not trace.current_exists or trace.current is None:
        return spec.operation == "delete" and not trace.current_exists
    if spec.operation == "delete":
        return False
    return all(trace.current.get(key) == value for key, value in spec.allowed_updates.items())


def observation_profiles(rng: random.Random, count: int) -> list[tuple[str, ...]]:
    profiles: list[tuple[str, ...]] = [ALL_FEATURES]
    seen = {ALL_FEATURES}
    while len(profiles) < count:
        size = rng.randint(3, len(ALL_FEATURES) - 1)
        profile = tuple(name for name in ALL_FEATURES if name in set(rng.sample(list(ALL_FEATURES), size)))
        if profile not in seen:
            seen.add(profile)
            profiles.append(profile)
    return profiles


def run_model_suite(seed: int, specs_per_family: int, profiles_per_spec: int) -> dict[str, Any]:
    rng = random.Random(seed)
    runtime_rows: list[dict[str, Any]] = []
    audit_configs = Counter()
    selected_counts: list[int] = []
    selected_costs: list[int] = []
    full_cost = sum(FEATURE_COSTS.values())
    certificate_samples: list[dict[str, Any]] = []
    index = 0
    for domain in sorted(SCHEMAS):
        for operation in ("create", "delete", "update"):
            for _ in range(specs_per_family):
                index += 1
                spec = make_spec(domain, operation, rng, index)
                profiles = observation_profiles(rng, profiles_per_spec)
                traces = {
                    fault: concrete_hidden_fault(spec, fault, rng) for fault in HIDDEN_FAULTS
                }
                assert terminal_success(spec, traces["honest"])
                assert all(not terminal_success(spec, traces[fault]) for fault in HIDDEN_FAULTS if fault != "honest")

                for profile in profiles:
                    direct_unsafe = any(
                        direct_exact_available(spec, traces[fault], profile)
                        for fault in HIDDEN_FAULTS
                        if fault != "honest"
                    )
                    audit_configs["direct_configs"] += 1
                    audit_configs["direct_unsafe_configs"] += int(direct_unsafe)
                    rigid_deploy = profile == ALL_FEATURES
                    audit_configs["rigid_deployed_configs"] += int(rigid_deploy)
                    audit_configs["rigid_safe_configs"] += int(rigid_deploy and not direct_unsafe)

                    try:
                        compiled = compile_witness(spec, profile)
                    except UnwitnessableEffect:
                        audit_configs["candidate_rejected_configs"] += 1
                        continue
                    audit_configs["candidate_deployed_configs"] += 1
                    selected_counts.append(len(compiled.selected_features))
                    selected_costs.append(compiled.read_cost)
                    unsafe = False
                    for fault, trace in traces.items():
                        accepted = compiled.verify(spec, trace)
                        truth = terminal_success(spec, trace)
                        runtime_rows.append(
                            {
                                "method": "mutation_audited_compiled",
                                "fault": fault,
                                "accepted": accepted,
                                "truth": truth,
                            }
                        )
                        unsafe = unsafe or (accepted and not truth)
                    audit_configs["candidate_unsafe_configs"] += int(unsafe)
                    if len(certificate_samples) < 4 and profile == ALL_FEATURES:
                        certificate_samples.append(
                            {
                                "domain": domain,
                                "operation": operation,
                                "selected_features": compiled.selected_features,
                                "certificate": dict(compiled.certificate),
                            }
                        )

                for fault, trace in traces.items():
                    truth = terminal_success(spec, trace)
                    runtime_rows.extend(
                        (
                            {
                                "method": "schema_direct",
                                "fault": fault,
                                "accepted": schema_direct_witness(spec, trace),
                                "truth": truth,
                            },
                            {
                                "method": "manual_complete_full_evidence",
                                "fault": fault,
                                "accepted": manual_complete_postcondition(spec, trace),
                                "truth": truth,
                            },
                        )
                    )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in runtime_rows:
        grouped[row["method"]].append(row)
    runtime_summary: dict[str, Any] = {}
    for method, rows in sorted(grouped.items()):
        failures = [row for row in rows if not row["truth"]]
        successes = [row for row in rows if row["truth"]]
        runtime_summary[method] = {
            "evaluations": len(rows),
            "failure_evaluations": len(failures),
            "success_evaluations": len(successes),
            "unsafe_accept_rate": sum(row["accepted"] for row in failures) / len(failures),
            "normal_accept_rate": sum(row["accepted"] for row in successes) / len(successes),
            "unsafe_accept_by_fault": {
                fault: sum(row["accepted"] for row in failures if row["fault"] == fault)
                / sum(1 for row in failures if row["fault"] == fault)
                for fault in HIDDEN_FAULTS
                if fault != "honest"
            },
        }
    audit_summary: dict[str, Any] = dict(audit_configs)
    empirically_safe = (
        audit_configs["direct_configs"] - audit_configs["direct_unsafe_configs"]
    )
    candidate_safe = (
        audit_configs["candidate_deployed_configs"]
        - audit_configs["candidate_unsafe_configs"]
    )
    audit_summary.update(
        {
            "empirically_safe_configs": empirically_safe,
            "candidate_empirically_safe_deployed": candidate_safe,
            "candidate_safe_deployment_coverage": candidate_safe / empirically_safe,
            "candidate_conservative_rejections": empirically_safe - candidate_safe,
            "rigid_safe_deployment_coverage": audit_configs["rigid_safe_configs"]
            / empirically_safe,
        }
    )
    return {
        "configuration": {
            "seed": seed,
            "domains": sorted(SCHEMAS),
            "operation_families": ["create", "delete", "update"],
            "specs_per_domain_family": specs_per_family,
            "profiles_per_spec": profiles_per_spec,
            "hidden_faults": list(HIDDEN_FAULTS),
        },
        "audit": audit_summary,
        "runtime": runtime_summary,
        "projection": {
            "mean_selected_features": statistics.fmean(selected_counts),
            "mean_selected_cost": statistics.fmean(selected_costs),
            "full_feature_count": len(ALL_FEATURES),
            "full_cost": full_cost,
            "mean_cost_reduction_vs_full": 1 - statistics.fmean(selected_costs) / full_cost,
        },
        "certificate_samples": certificate_samples,
    }


def _percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    return ordered[min(len(ordered) - 1, int(q * (len(ordered) - 1)))]


def run_sqlite_prototype(seed: int, operations: int) -> dict[str, Any]:
    rng = random.Random(seed ^ 0x51A17E)
    plain_latencies: list[float] = []
    logged_latencies: list[float] = []
    read_latencies: list[float] = []
    verify_latencies: list[float] = []
    snapshot_latencies: list[float] = []
    with tempfile.TemporaryDirectory(prefix="crl-v002-sqlite-") as temp_dir:
        plain = sqlite3.connect(str(Path(temp_dir) / "plain.db"))
        logged = sqlite3.connect(str(Path(temp_dir) / "logged.db"))
        for connection in (plain, logged):
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute(
                "CREATE TABLE entities(record_id TEXT PRIMARY KEY, body TEXT NOT NULL, version INTEGER NOT NULL)"
            )
        logged.execute(
            "CREATE TABLE effect_events(seq INTEGER PRIMARY KEY AUTOINCREMENT, nonce TEXT NOT NULL, target_id TEXT NOT NULL, kind TEXT NOT NULL, before_body TEXT, after_body TEXT, ordinal INTEGER NOT NULL, commit_version INTEGER NOT NULL)"
        )
        logged.execute("CREATE INDEX effect_events_nonce_idx ON effect_events(nonce)")
        initial: list[tuple[str, str, int]] = []
        schema = SCHEMAS["calendar"]
        for index in range(1000):
            body = {field: rng.choice(values) for field, values in schema.items()}
            initial.append((f"calendar-{index:05d}", json.dumps(body, sort_keys=True), 1))
        plain.executemany("INSERT INTO entities VALUES (?, ?, ?)", initial)
        logged.executemany("INSERT INTO entities VALUES (?, ?, ?)", initial)
        plain.commit()
        logged.commit()

        accepted = 0
        for index in range(operations):
            record_id = f"calendar-{rng.randrange(1000):05d}"
            before = json.loads(logged.execute("SELECT body FROM entities WHERE record_id=?", (record_id,)).fetchone()[0])
            field = rng.choice(sorted(schema))
            update = {field: _different(before[field], schema[field])}
            desired = dict(before)
            desired.update(update)
            nonce = f"sqlite-{index:06d}-{rng.getrandbits(40):010x}"
            spec = EffectSpec(nonce, "update", record_id, tuple(sorted(schema)), update, before)
            compiled = compile_witness(spec, ALL_FEATURES)
            desired_json = json.dumps(desired, sort_keys=True)

            start = time.perf_counter_ns()
            with plain:
                plain.execute(
                    "UPDATE entities SET body=?, version=version+1 WHERE record_id=?",
                    (desired_json, record_id),
                )
            plain_latencies.append((time.perf_counter_ns() - start) / 1000)

            version = logged.execute("SELECT version FROM entities WHERE record_id=?", (record_id,)).fetchone()[0] + 1
            start = time.perf_counter_ns()
            with logged:
                logged.execute(
                    "UPDATE entities SET body=?, version=? WHERE record_id=?",
                    (desired_json, version, record_id),
                )
                logged.execute(
                    "INSERT INTO effect_events(nonce,target_id,kind,before_body,after_body,ordinal,commit_version) VALUES (?,?,?,?,?,?,?)",
                    (nonce, record_id, "update", json.dumps(before, sort_keys=True), desired_json, 1, version),
                )
            logged_latencies.append((time.perf_counter_ns() - start) / 1000)

            start = time.perf_counter_ns()
            event_rows = logged.execute(
                "SELECT nonce,target_id,kind,before_body,after_body,ordinal,commit_version FROM effect_events WHERE nonce=? ORDER BY ordinal",
                (nonce,),
            ).fetchall()
            current_body, current_version = logged.execute(
                "SELECT body,version FROM entities WHERE record_id=?", (record_id,)
            ).fetchone()
            read_latencies.append((time.perf_counter_ns() - start) / 1000)
            trace = EffectTrace(
                tuple(
                    EffectEvent(row[0], row[1], row[2], json.loads(row[3]) if row[3] else None, json.loads(row[4]) if row[4] else None, row[5], row[6])
                    for row in event_rows
                ),
                True,
                json.loads(current_body),
                current_version,
            )
            start = time.perf_counter_ns()
            accepted += int(compiled.verify(spec, trace))
            verify_latencies.append((time.perf_counter_ns() - start) / 1000)

            if index < min(100, operations):
                start = time.perf_counter_ns()
                list(logged.execute("SELECT record_id,body,version FROM entities"))
                list(logged.execute("SELECT nonce,target_id,kind,ordinal,commit_version FROM effect_events"))
                snapshot_latencies.append((time.perf_counter_ns() - start) / 1000)
        plain.close()
        logged.close()

    def latency(values: list[float]) -> dict[str, float]:
        return {
            "median_us": statistics.median(values),
            "p95_us": _percentile(values, 0.95),
        }

    return {
        "configuration": {"entities": 1000, "operations": operations, "engine": "python sqlite3", "journal_mode": "WAL"},
        "honest_acceptance": {"accepted": accepted, "total": operations},
        "plain_write": latency(plain_latencies),
        "atomic_logged_write": latency(logged_latencies),
        "indexed_evidence_read": latency(read_latencies),
        "compiled_verify": latency(verify_latencies),
        "full_snapshot_read": latency(snapshot_latencies),
        "scope_note": "Prototype mechanics only; the wrapper is not a security boundary against direct database writers.",
    }


def negative_controls(seed: int, cases: int) -> dict[str, Any]:
    rng = random.Random(seed ^ 0xBAD5EED)
    counts = Counter()
    for index in range(cases):
        domain = rng.choice(sorted(SCHEMAS))
        spec = make_spec(domain, "update", rng, index)
        compiled = compile_witness(spec, ALL_FEATURES)
        correct = canonical_trace(spec)

        # A malicious read surface forges the canonical evidence after a no-op.
        counts["forged_read"] += int(compiled.verify(spec, correct))

        # An unlogged collateral write is outside the nonce-indexed evidence.
        counts["unlogged_collateral"] += int(compiled.verify(spec, correct))

        # The witness is true at revision 11, then a later revision reverts it.
        witnessed = compiled.verify(spec, correct)
        delayed = EffectTrace(correct.events, spec.before is not None, spec.before, 12)
        assert witnessed and not terminal_success(spec, delayed)
        counts["delayed_change_after_witness"] += int(witnessed)
    return {
        "cases_each": cases,
        "unsafe_accept_rate": {name: counts[name] / cases for name in sorted(counts)},
        "interpretation": {
            "forged_read": "trusted evidence reads remain an external premise",
            "unlogged_collateral": "complete, enforced lineage remains an external premise",
            "delayed_change_after_witness": "the claim is bound to the observed committed revision, not future state",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260803)
    parser.add_argument("--specs-per-family", type=int, default=24)
    parser.add_argument("--profiles-per-spec", type=int, default=24)
    parser.add_argument("--sqlite-operations", type=int, default=600)
    parser.add_argument("--negative-cases", type=int, default=600)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if min(args.specs_per_family, args.profiles_per_spec, args.sqlite_operations, args.negative_cases) <= 0:
        parser.error("all counts must be positive")
    payload = {
        "schema_version": 2,
        "experiment": "mutation-audited contrastive observability certificates for effect frames",
        "model_suite": run_model_suite(args.seed, args.specs_per_family, args.profiles_per_spec),
        "sqlite_prototype": run_sqlite_prototype(args.seed, args.sqlite_operations),
        "negative_controls": negative_controls(args.seed, args.negative_cases),
        "independence_note": "The method module sees abstract traces only; concrete fault processes and strict terminal labels are defined here. This is implementation separation, not evidence of real-world defect-distribution independence.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"model_suite": payload["model_suite"], "sqlite_prototype": payload["sqlite_prototype"], "negative_controls": payload["negative_controls"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
