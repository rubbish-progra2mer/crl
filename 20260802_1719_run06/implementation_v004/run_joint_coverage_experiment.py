from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

from joint_coverage_kernel import (
    Claim,
    Observation,
    Record,
    ScopeCell,
    SourceIdentity,
    canonical_request_payload,
    complete_joint_cells,
    evaluate_claim,
    marginal_coverage_would_accept,
    next_page_requests,
    verify_certificate,
)
from run_soundness_counterexamples import build_panel as build_soundness_panel


Method = Literal[
    "dynamic_contract",
    "dynamic_contract_with_executor",
    "uniform_negative_recheck",
    "optimized_full_scan",
    "claim_aware_planner",
    "joint_coverage_gate",
    "server_direct_query",
]

METHODS: tuple[Method, ...] = (
    "dynamic_contract",
    "dynamic_contract_with_executor",
    "uniform_negative_recheck",
    "optimized_full_scan",
    "claim_aware_planner",
    "joint_coverage_gate",
    "server_direct_query",
)
ENTITIES = ("team-a", "team-b", "team-c")
TIME_BUCKETS = ("recent", "old")
ARCHIVE_STATES = ("active", "archived")
QUERY_SIGNATURE = "list-one-joint-cell-v1"
AUTHENTICATION_SUBJECT = "fixture-subject"
SCOPE_SCHEMA_VERSION = "joint-scope-v1"
ADAPTER_VERSION = "fixture-adapter-v1"
REQUEST_SERIALIZATION_VERSION = "canonical-json-v1"


def universe_cells() -> tuple[ScopeCell, ...]:
    return tuple(
        ScopeCell(entity, time_bucket, archive_state)
        for entity in ENTITIES
        for time_bucket in TIME_BUCKETS
        for archive_state in ARCHIVE_STATES
    )


UNIVERSE = universe_cells()
INITIAL_CELL = ScopeCell("team-a", "recent", "active")


@dataclass(frozen=True)
class ConnectorProfile:
    profile_id: str
    page_size: int
    direct_predicates: tuple[str, ...]
    semantic_fixture: str

    @property
    def source(self) -> SourceIdentity:
        return SourceIdentity(
            self.profile_id,
            QUERY_SIGNATURE,
            AUTHENTICATION_SUBJECT,
            SCOPE_SCHEMA_VERSION,
            ADAPTER_VERSION,
            REQUEST_SERIALIZATION_VERSION,
        )


PROFILES = (
    ConnectorProfile(
        "issue_cursor_api",
        2,
        (),
        "议题列表：默认打开项、游标分页、归档项目分离",
    ),
    ConnectorProfile(
        "audit_window_api",
        4,
        ("matches_target",),
        "审计日志：默认近期窗口、时间分桶、可选服务器端精确检索",
    ),
    ConnectorProfile(
        "archive_split_api",
        3,
        ("matches_target", "compliant"),
        "记录目录：活动/归档分离、页式枚举、可选反例检索",
    ),
)


@dataclass(frozen=True)
class World:
    world_id: str
    seed: int
    profile: ConnectorProfile
    snapshot_id: str
    visible_entities: tuple[str, ...]
    records: tuple[Record, ...]

    @property
    def visible_cells(self) -> tuple[ScopeCell, ...]:
        return tuple(cell for cell in UNIVERSE if cell.entity in self.visible_entities)

    def records_for(self, cell: ScopeCell) -> tuple[Record, ...]:
        return tuple(
            sorted(
                (record for record in self.records if record.cell == cell),
                key=lambda record: record.record_id,
            )
        )


class SimulatedConnector:
    def __init__(self, world: World) -> None:
        self.world = world
        self.tool_calls = 0

    def fetch_page(self, cell: ScopeCell, cursor: int) -> Observation:
        self.tool_calls += 1
        source = self.world.profile.source
        observation_id = (
            f"{self.world.world_id}:{source.connector_id}:"
            f"{cell.key}:cursor-{cursor}:snapshot-{self.world.snapshot_id}"
        )
        common = {
            "query_signature": source.query_signature,
            "authentication_subject": source.authentication_subject,
            "scope_schema_version": source.scope_schema_version,
            "adapter_version": source.adapter_version,
            "request_serialization_version": source.request_serialization_version,
            "request_payload": canonical_request_payload(
                source,
                cell,
                cursor,
                self.world.snapshot_id,
            ),
        }
        if cell.entity not in self.world.visible_entities:
            return Observation(
                observation_id=observation_id,
                connector_id=source.connector_id,
                cell=cell,
                cursor=cursor,
                next_cursor=None,
                records=(),
                snapshot_id=self.world.snapshot_id,
                status="permission_denied",
                permission_complete=False,
                **common,
            )
        records = self.world.records_for(cell)
        page_size = self.world.profile.page_size
        page = records[cursor : cursor + page_size]
        next_cursor = cursor + page_size if cursor + page_size < len(records) else None
        return Observation(
            observation_id=observation_id,
            connector_id=source.connector_id,
            cell=cell,
            cursor=cursor,
            next_cursor=next_cursor,
            records=page,
            snapshot_id=self.world.snapshot_id,
            **common,
        )

    def direct_query(self, claim: Claim) -> str:
        self.tool_calls += 1
        if claim.predicate not in self.world.profile.direct_predicates:
            return "UNKNOWN"
        if any(cell.entity not in self.world.visible_entities for cell in claim.scope):
            return "UNKNOWN"
        return "TRUE" if claim_truth(self.world, claim) else "FALSE"


def build_worlds(seeds: Iterable[int], worlds_per_seed: int) -> list[World]:
    worlds: list[World] = []
    for seed in seeds:
        for world_index in range(worlds_per_seed):
            world_seed = seed * 1000 + world_index
            rng = random.Random(world_seed)
            profile = PROFILES[world_index % len(PROFILES)]
            visible_entities = ENTITIES if world_index % 5 else ENTITIES[:2]
            records: list[Record] = []
            for cell_index, cell in enumerate(UNIVERSE):
                for record_index in range(rng.randint(0, 6)):
                    records.append(
                        Record(
                            record_id=(
                                f"s{seed}-w{world_index:02d}-c{cell_index:02d}-"
                                f"r{record_index:02d}"
                            ),
                            cell=cell,
                            matches_target=rng.random() < 0.08,
                            compliant=rng.random() >= 0.10,
                        )
                    )
            worlds.append(
                World(
                    world_id=f"seed-{seed}-world-{world_index:02d}",
                    seed=world_seed,
                    profile=profile,
                    snapshot_id=f"snapshot-{seed}-{world_index:02d}",
                    visible_entities=visible_entities,
                    records=tuple(records),
                )
            )
    return worlds


def _cells(
    *,
    entities: Iterable[str],
    time_buckets: Iterable[str],
    archive_states: Iterable[str],
) -> tuple[ScopeCell, ...]:
    entity_set = set(entities)
    time_set = set(time_buckets)
    archive_set = set(archive_states)
    return tuple(
        cell
        for cell in UNIVERSE
        if cell.entity in entity_set
        and cell.time_bucket in time_set
        and cell.archive_state in archive_set
    )


def scope_families(world: World) -> dict[str, tuple[ScopeCell, ...]]:
    return {
        "current_cell": (INITIAL_CELL,),
        "team_recent_including_archive": _cells(
            entities=("team-a",),
            time_buckets=("recent",),
            archive_states=ARCHIVE_STATES,
        ),
        "team_all_history_active": _cells(
            entities=("team-a",),
            time_buckets=TIME_BUCKETS,
            archive_states=("active",),
        ),
        "team_all_history_including_archive": _cells(
            entities=("team-a",),
            time_buckets=TIME_BUCKETS,
            archive_states=ARCHIVE_STATES,
        ),
        "current_permission_scope": tuple(world.visible_cells),
        "organization_recent_including_archive": _cells(
            entities=ENTITIES,
            time_buckets=("recent",),
            archive_states=ARCHIVE_STATES,
        ),
        "organization_all_history_including_archive": UNIVERSE,
    }


def build_claims(world: World) -> list[tuple[str, Claim]]:
    claims: list[tuple[str, Claim]] = []
    for family, scope in scope_families(world).items():
        claims.append(
            (
                family,
                Claim(
                    f"{world.world_id}:{family}:exists",
                    "exists",
                    "matches_target",
                    scope,
                    world.snapshot_id,
                    world.profile.source,
                    f"在 {family} 范围内是否存在目标记录？",
                ),
            )
        )
        claims.append(
            (
                family,
                Claim(
                    f"{world.world_id}:{family}:forall",
                    "forall",
                    "compliant",
                    scope,
                    world.snapshot_id,
                    world.profile.source,
                    f"在 {family} 范围内是否所有记录都合规？",
                ),
            )
        )
    return claims


def claim_truth(world: World, claim: Claim) -> bool:
    values = [
        claim.predicate_holds(record)
        for record in world.records
        if record.cell in claim.scope
    ]
    return any(values) if claim.quantifier == "exists" else all(values)


@dataclass(frozen=True)
class Outcome:
    decision: str
    tool_calls: int
    certificate_valid: bool | None
    proof_type: str
    reason: str
    observed_digests: tuple[str, ...]


def _outcome(
    claim: Claim,
    observations: list[Observation],
    connector: SimulatedConnector,
    *,
    verify: bool,
) -> Outcome:
    evaluation = evaluate_claim(claim, observations)
    certificate_valid = (
        verify_certificate(claim, observations, evaluation.certificate)
        if verify
        else None
    )
    decision = evaluation.decision
    if verify and not certificate_valid:
        decision = "UNKNOWN"
    return Outcome(
        decision,
        connector.tool_calls,
        certificate_valid,
        evaluation.certificate.proof_type,
        evaluation.certificate.reason,
        tuple(item.digest for item in observations),
    )


def _repair_exact_scope(
    claim: Claim,
    connector: SimulatedConnector,
    observations: list[Observation],
    budget: int,
    *,
    verify: bool,
) -> Outcome:
    while True:
        evaluation = evaluate_claim(claim, observations)
        if evaluation.decision != "UNKNOWN":
            return _outcome(claim, observations, connector, verify=verify)
        requests = next_page_requests(claim, observations)
        if not requests or connector.tool_calls >= budget:
            return _outcome(claim, observations, connector, verify=verify)
        cell, cursor = requests[0]
        observations.append(connector.fetch_page(cell, int(cursor)))


def _scan_universe(
    claim: Claim,
    connector: SimulatedConnector,
    observations: list[Observation],
    budget: int,
    *,
    witness_early_stop: bool,
) -> Outcome:
    while True:
        evaluation = evaluate_claim(claim, observations)
        if witness_early_stop and evaluation.certificate.proof_type in {
            "positive_witness",
            "counterexample_witness",
        }:
            return _outcome(claim, observations, connector, verify=False)
        if len(complete_joint_cells(claim, observations, UNIVERSE)) == len(UNIVERSE):
            return _outcome(claim, observations, connector, verify=False)
        requests = next_page_requests(claim, observations, UNIVERSE)
        if not requests or connector.tool_calls >= budget:
            return _outcome(claim, observations, connector, verify=False)
        cell, cursor = requests[0]
        observations.append(connector.fetch_page(cell, int(cursor)))


def run_method(world: World, claim: Claim, method: Method, budget: int) -> Outcome:
    connector = SimulatedConnector(world)
    initial = connector.fetch_page(INITIAL_CELL, 0)
    observations = [initial]
    if method == "dynamic_contract":
        return _outcome(claim, observations, connector, verify=False)
    if method in {"claim_aware_planner", "dynamic_contract_with_executor"}:
        return _repair_exact_scope(
            claim, connector, observations, budget, verify=False
        )
    if method == "joint_coverage_gate":
        return _repair_exact_scope(
            claim, connector, observations, budget, verify=True
        )
    if method == "uniform_negative_recheck":
        return _scan_universe(
            claim, connector, observations, budget, witness_early_stop=True
        )
    if method == "optimized_full_scan":
        return _scan_universe(
            claim, connector, observations, budget, witness_early_stop=False
        )
    if method == "server_direct_query":
        initial_evaluation = evaluate_claim(claim, observations)
        if initial_evaluation.certificate.proof_type in {
            "positive_witness",
            "counterexample_witness",
        }:
            return _outcome(claim, observations, connector, verify=False)
        if connector.tool_calls >= budget:
            return _outcome(claim, observations, connector, verify=False)
        decision = connector.direct_query(claim)
        return Outcome(
            decision,
            connector.tool_calls,
            None,
            "server_direct_answer" if decision != "UNKNOWN" else "unsupported_direct_query",
            "connector-provided exact query" if decision != "UNKNOWN" else "direct query unavailable or permission-incomplete",
            (initial.digest,),
        )
    raise AssertionError(method)


def scope_isolation_panel() -> dict[str, Any]:
    source = SourceIdentity(
        "paired-panel",
        QUERY_SIGNATURE,
        AUTHENTICATION_SUBJECT,
        SCOPE_SCHEMA_VERSION,
        ADAPTER_VERSION,
        REQUEST_SERIALIZATION_VERSION,
    )
    local = ScopeCell("team-a", "recent", "active")
    old = ScopeCell("team-a", "old", "active")
    other = ScopeCell("team-b", "recent", "active")
    empty = Observation(
        "same-empty-observation",
        source.connector_id,
        local,
        0,
        None,
        (),
        "paired-snapshot",
        query_signature=source.query_signature,
        authentication_subject=source.authentication_subject,
        scope_schema_version=source.scope_schema_version,
        adapter_version=source.adapter_version,
        request_serialization_version=source.request_serialization_version,
        request_payload=canonical_request_payload(source, local, 0, "paired-snapshot"),
    )
    claims = (
        Claim("local-exists", "exists", "matches_target", (local,), "paired-snapshot", source),
        Claim("history-exists", "exists", "matches_target", (local, old), "paired-snapshot", source),
        Claim("organization-exists", "exists", "matches_target", (local, old, other), "paired-snapshot", source),
        Claim("local-forall", "forall", "compliant", (local,), "paired-snapshot", source),
        Claim("history-forall", "forall", "compliant", (local, old), "paired-snapshot", source),
    )
    return {
        "observation_digest": empty.digest,
        "rows": [
            {
                "claim_id": claim.claim_id,
                "quantifier": claim.quantifier,
                "scope_size": len(claim.scope),
                "decision": evaluate_claim(claim, [empty]).decision,
            }
            for claim in claims
        ],
    }


def joint_hole_panel() -> dict[str, Any]:
    source = SourceIdentity(
        "joint-hole-panel",
        QUERY_SIGNATURE,
        AUTHENTICATION_SUBJECT,
        SCOPE_SCHEMA_VERSION,
        ADAPTER_VERSION,
        REQUEST_SERIALIZATION_VERSION,
    )
    cells = (
        ScopeCell("A", "recent", "active"),
        ScopeCell("A", "old", "active"),
        ScopeCell("B", "recent", "active"),
        ScopeCell("B", "old", "active"),
    )
    claim = Claim("joint-hole", "exists", "matches_target", cells, "s1", source)
    rows = []
    for mask in range(1, 1 << len(cells)):
        observed = tuple(cell for index, cell in enumerate(cells) if mask & (1 << index))
        if len(observed) == len(cells) or not marginal_coverage_would_accept(cells, observed):
            continue
        missing = tuple(cell for cell in cells if cell not in observed)
        observations = [
            Observation(
                f"obs-{index}",
                source.connector_id,
                cell,
                0,
                None,
                (),
                "s1",
                query_signature=source.query_signature,
                authentication_subject=source.authentication_subject,
                scope_schema_version=source.scope_schema_version,
                adapter_version=source.adapter_version,
                request_serialization_version=source.request_serialization_version,
                request_payload=canonical_request_payload(source, cell, 0, "s1"),
            )
            for index, cell in enumerate(observed)
        ]
        joint = evaluate_claim(claim, observations)
        rows.append(
            {
                "observed_cells": [cell.key for cell in observed],
                "missing_cells": [cell.key for cell in missing],
                "independent_hidden_target_cell": missing[0].key,
                "marginal_false_commit": True,
                "joint_decision": joint.decision,
                "joint_false_commit": joint.decision == "FALSE",
            }
        )
    return {
        "counterexample_count": len(rows),
        "marginal_false_commits": len(rows),
        "joint_false_commits": sum(row["joint_false_commit"] for row in rows),
        "rows": rows,
    }


def percentile(values: list[int], fraction: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(fraction * len(ordered)) - 1))
    return float(ordered[index])


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for budget, method in sorted({(row["budget"], row["method"]) for row in rows}):
        group = [row for row in rows if row["budget"] == budget and row["method"] == method]
        answered = [row for row in group if row["decision"] != "UNKNOWN"]
        calls = [int(row["tool_calls"]) for row in group]
        cert_rows = [row for row in group if row["certificate_valid"] is not None]
        output.append(
            {
                "budget": budget,
                "method": method,
                "episodes": len(group),
                "answer_rate": len(answered) / len(group),
                "task_accuracy_unknown_is_incorrect": sum(row["correct"] for row in group) / len(group),
                "answered_accuracy": sum(row["correct"] for row in answered) / len(answered) if answered else None,
                "unsafe_commit_rate": sum(row["unsafe_commit"] for row in group) / len(group),
                "unknown_rate": sum(row["decision"] == "UNKNOWN" for row in group) / len(group),
                "mean_tool_calls": statistics.fmean(calls),
                "p95_tool_calls": percentile(calls, 0.95),
                "certificate_valid_rate": (
                    sum(row["certificate_valid"] is True for row in cert_rows) / len(cert_rows)
                    if cert_rows
                    else None
                ),
            }
        )
    return output


def world_to_dict(world: World) -> dict[str, Any]:
    return {
        "world_id": world.world_id,
        "seed": world.seed,
        "connector_profile": world.profile.profile_id,
        "source_identity_digest": world.profile.source.digest,
        "semantic_fixture": world.profile.semantic_fixture,
        "page_size": world.profile.page_size,
        "direct_predicates": list(world.profile.direct_predicates),
        "snapshot_id": world.snapshot_id,
        "visible_entities": list(world.visible_entities),
        "records": [
            {
                "record_id": record.record_id,
                "cell": record.cell.key,
                "matches_target": record.matches_target,
                "compliant": record.compliant,
            }
            for record in world.records
        ],
    }


def equivalence(rows: list[dict[str, Any]], budgets: list[int]) -> list[dict[str, Any]]:
    methods = (
        "claim_aware_planner",
        "dynamic_contract_with_executor",
        "joint_coverage_gate",
    )
    output = []
    for budget in budgets:
        grouped = {
            method: sorted(
                (row for row in rows if row["budget"] == budget and row["method"] == method),
                key=lambda row: row["claim_id"],
            )
            for method in methods
        }
        triples = zip(*(grouped[method] for method in methods))
        mismatches = sum(
            len({(row["decision"], row["tool_calls"]) for row in triple}) > 1
            for triple in triples
        )
        output.append(
            {
                "budget": budget,
                "episodes_per_method": len(grouped[methods[0]]),
                "decision_or_cost_mismatches": mismatches,
                "interpretation": "structurally shared exact-scope executor; not independent baseline systems",
            }
        )
    return output


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, nargs="+", default=[20260802, 20260803, 20260804])
    parser.add_argument("--worlds-per-seed", type=int, default=18)
    parser.add_argument("--budgets", type=int, nargs="+", default=[2, 4, 8, 16, 32])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.worlds_per_seed <= 0 or not args.budgets or any(budget < 1 for budget in args.budgets):
        raise ValueError("world count and budgets must be positive")

    started = time.time()
    worlds = build_worlds(args.seeds, args.worlds_per_seed)
    rows: list[dict[str, Any]] = []
    task_count = 0
    digest_failures = 0
    for world in worlds:
        expected_initial = SimulatedConnector(world).fetch_page(INITIAL_CELL, 0).digest
        for scope_family, claim in build_claims(world):
            task_count += 1
            truth = claim_truth(world, claim)
            for budget in args.budgets:
                for method in METHODS:
                    outcome = run_method(world, claim, method, budget)
                    initial_digest = outcome.observed_digests[0]
                    digest_failures += initial_digest != expected_initial
                    correct = outcome.decision == ("TRUE" if truth else "FALSE")
                    rows.append(
                        {
                            "world_id": world.world_id,
                            "connector_profile": world.profile.profile_id,
                            "scope_family": scope_family,
                            "claim_id": claim.claim_id,
                            "quantifier": claim.quantifier,
                            "predicate": claim.predicate,
                            "scope_size": len(claim.scope),
                            "truth": truth,
                            "budget": budget,
                            "method": method,
                            "decision": outcome.decision,
                            "correct": correct,
                            "unsafe_commit": outcome.decision != "UNKNOWN" and not correct,
                            "tool_calls": outcome.tool_calls,
                            "certificate_valid": outcome.certificate_valid,
                            "proof_type": outcome.proof_type,
                            "reason": outcome.reason,
                            "initial_observation_digest": initial_digest,
                        }
                    )

    summary = summarize(rows)
    soundness = build_soundness_panel()
    document = {
        "experiment": "request_bound_joint_claim_coverage_v004",
        "schema_version": 1,
        "seeds": args.seeds,
        "worlds_per_seed": args.worlds_per_seed,
        "budgets": args.budgets,
        "methods": METHODS,
        "task_count": task_count,
        "episode_count": len(rows),
        "elapsed_seconds": time.time() - started,
        "same_information_check": {
            "paired_initial_observation_digest_failures": digest_failures,
            "all_methods_receive_same_initial_observation": digest_failures == 0,
        },
        "scope_isolation_panel": scope_isolation_panel(),
        "joint_hole_panel": joint_hole_panel(),
        "source_bound_soundness_panel": soundness,
        "shared_executor_equivalence": equivalence(rows, args.budgets),
        "summary": summary,
        "worlds": [world_to_dict(world) for world in worlds],
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "task_count": task_count,
                "episode_count": len(rows),
                "same_information_check": document["same_information_check"],
                "joint_hole_panel": {
                    key: document["joint_hole_panel"][key]
                    for key in ("counterexample_count", "marginal_false_commits", "joint_false_commits")
                },
                "source_bound_soundness_panel": {
                    key: soundness[key]
                    for key in ("case_count", "passed", "unsafe_certified_commits", "all_passed")
                },
                "shared_executor_equivalence": document["shared_executor_equivalence"],
                "summary": summary,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
