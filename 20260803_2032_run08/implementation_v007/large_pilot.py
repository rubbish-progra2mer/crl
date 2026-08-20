#!/usr/bin/env python3
"""SQLite 强状态与 Git 异步收敛服务上的扩大持留实验。"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import sqlite3
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from compiler import compile_contract, contract_claim_refs
from protocol import evaluate_observations, issue_attestation, verify_and_admit
from typed_model import (
    AdmissionBundle,
    AdmissionRequest,
    BooleanExpr,
    ChannelProjection,
    CompareExpr,
    EffectContract,
    EvidenceBundle,
    FieldRef,
    LiteralValue,
    ObservedEvent,
    ProbeObservation,
    ProbeSpec,
    ProjectionPolicy,
    RelationClaim,
    canonical_hash,
)


ISSUER_KEY = b"v007-formal-pilot-test-key-32bytes"
ISSUED_AT = 1_800_000_000
DOMAIN = ("0", "1")
OPERATIONS = (
    "contact_insert",
    "contact_update",
    "task_assign",
    "preference_upsert",
    "message_enqueue",
    "reminder_delete",
    "quota_set",
    "membership_add",
    "note_append",
    "token_rotate",
)


@dataclass(frozen=True)
class LogicalEvent:
    kind: str
    target: str
    payload: str


@dataclass(frozen=True)
class Variant:
    name: str
    mutation: str
    scope: str
    argument: str
    category: str


def _probe(probe_id: str) -> ProbeSpec:
    return ProbeSpec(probe_id=probe_id, factors=(("case", probe_id),))


def _formula_catalogue():
    t1 = FieldRef(probe_id="p1", channel="target")
    t2 = FieldRef(probe_id="p2", channel="target")
    d1 = FieldRef(probe_id="p1", channel="payload")
    d2 = FieldRef(probe_id="p2", channel="payload")
    teq = CompareExpr(operator="eq", left=t1, right=t2)
    deq = CompareExpr(operator="eq", left=d1, right=d2)
    return (
        ("target_eq", teq, ("0", "0", "0", "1"), "identity", "identity"),
        (
            "target_ne",
            CompareExpr(operator="ne", left=t1, right=t2),
            ("0", "1", "0", "1"),
            "global_bijection",
            "identity",
        ),
        ("payload_eq", deq, ("0", "1", "0", "0"), "identity", "identity"),
        (
            "payload_ne",
            CompareExpr(operator="ne", left=d1, right=d2),
            ("0", "1", "0", "1"),
            "identity",
            "global_bijection",
        ),
        (
            "target_literal",
            CompareExpr(operator="eq", left=t1, right=LiteralValue("0")),
            ("0", "1", "0", "1"),
            "identity",
            "identity",
        ),
        (
            "payload_literal",
            CompareExpr(operator="eq", left=d1, right=LiteralValue("0")),
            ("0", "1", "0", "1"),
            "identity",
            "identity",
        ),
        (
            "both_equal",
            BooleanExpr(operator="and", children=(teq, deq)),
            ("0", "0", "1", "1"),
            "global_bijection",
            "global_bijection",
        ),
        (
            "either_equal",
            BooleanExpr(operator="or", children=(teq, deq)),
            ("0", "0", "0", "1"),
            "probe_local_bijection",
            "global_bijection",
        ),
        (
            "not_target_equal",
            BooleanExpr(operator="not", children=(teq,)),
            ("0", "1", "0", "1"),
            "global_bijection",
            "identity",
        ),
        (
            "cross_channel",
            CompareExpr(operator="eq", left=t1, right=d1),
            ("0", "1", "0", "1"),
            "global_bijection",
            "global_bijection",
        ),
    )


def _contracts(service: str):
    result = []
    for operation, item in zip(OPERATIONS, _formula_catalogue()):
        name, formula, values, target_kind, payload_kind = item
        contract = EffectContract(
            contract_id=f"{service}.{operation}.{name}",
            contract_version="7",
            primary_kind=operation,
            allowed_auxiliary_kinds=("audit",),
            relation_claims=(
                RelationClaim(
                    display_name=name,
                    probes=(_probe("p1"), _probe("p2")),
                    formula=formula,
                ),
            ),
        )
        projection = ProjectionPolicy(
            policy_id=f"{service}.{operation}.projection",
            policy_version="7",
            target=ChannelProjection(
                kind=target_kind, domain=DOMAIN, redaction_token="T-REDACTED"
            ),
            payload=ChannelProjection(
                kind=payload_kind, domain=DOMAIN, redaction_token="P-REDACTED"
            ),
        )
        result.append((operation, name, contract, projection, values))
    return tuple(result)


def _variants(service: str) -> tuple[Variant, ...]:
    variants = []
    for mutation in ("missing", "duplicate", "forbidden"):
        for scope in ("p1", "p2", "both"):
            variants.append(Variant(f"{mutation}_{scope}", mutation, scope, "", "service"))
    for mutation in ("target_constant", "payload_constant"):
        for scope in ("p1", "p2", "both"):
            for argument in DOMAIN:
                variants.append(
                    Variant(
                        f"{mutation}_{scope}_{argument}",
                        mutation,
                        scope,
                        argument,
                        "service",
                    )
                )
    for mutation in (
        "target_flip",
        "payload_flip",
        "target_from_payload",
        "payload_from_target",
    ):
        for scope in ("p1", "p2", "both"):
            variants.append(Variant(f"{mutation}_{scope}", mutation, scope, "", "service"))
    if len(variants) != 33:
        raise AssertionError("服务故障算子数量不是 33")
    observer_pair = (
        ("observer_drop_p1", "observer_drop", "observer_loss"),
        (
            "observer_duplicate_p1" if service == "sqlite" else "observer_retry_duplicate_p1",
            "observer_duplicate",
            "observer_retry",
        ),
        ("undeclared_probe_local_projection", "projection_misdeclare", "projection"),
        ("masked_missing_p1", "masked_missing", "observer_masking"),
        ("masked_duplicate_p1", "masked_duplicate", "observer_masking"),
        ("masked_target_flip_p1", "masked_target_flip", "observer_masking"),
        ("masked_forbidden_p1", "masked_forbidden", "observer_masking"),
    )
    variants.extend(
        Variant(name, mutation, "p1", "", category)
        for name, mutation, category in observer_pair
    )
    if len(variants) != 40 or len({item.name for item in variants}) != 40:
        raise AssertionError("每个服务必须有 40 个唯一故障/回归算子")
    return tuple(variants)


def _selected(scope: str, probe_id: str) -> bool:
    return scope == "both" or scope == probe_id


def _flip(value: str) -> str:
    return "1" if value == "0" else "0"


def _mutate_actual(
    base: tuple[LogicalEvent, ...], variant: Variant, probe_id: str
) -> tuple[LogicalEvent, ...]:
    if not _selected(variant.scope, probe_id):
        return base
    mutation = variant.mutation
    if mutation in {"observer_drop", "observer_duplicate", "projection_misdeclare"}:
        return base
    if mutation == "masked_missing":
        return ()
    if mutation == "masked_duplicate":
        return base + base
    if mutation == "masked_target_flip":
        return tuple(LogicalEvent(item.kind, _flip(item.target), item.payload) for item in base)
    if mutation == "masked_forbidden":
        return base + (LogicalEvent("forbidden_side_effect", "0", "0"),)
    if mutation == "missing":
        return ()
    if mutation == "duplicate":
        return base + base
    if mutation == "forbidden":
        return base + (LogicalEvent("forbidden_side_effect", "0", "0"),)
    if mutation == "target_constant":
        return tuple(LogicalEvent(item.kind, variant.argument, item.payload) for item in base)
    if mutation == "payload_constant":
        return tuple(LogicalEvent(item.kind, item.target, variant.argument) for item in base)
    if mutation == "target_flip":
        return tuple(LogicalEvent(item.kind, _flip(item.target), item.payload) for item in base)
    if mutation == "payload_flip":
        return tuple(LogicalEvent(item.kind, item.target, _flip(item.payload)) for item in base)
    if mutation == "target_from_payload":
        return tuple(LogicalEvent(item.kind, item.payload, item.payload) for item in base)
    if mutation == "payload_from_target":
        return tuple(LogicalEvent(item.kind, item.target, item.target) for item in base)
    raise AssertionError(f"未知变异：{mutation}")


def _audit_source(
    base: tuple[LogicalEvent, ...],
    actual: tuple[LogicalEvent, ...],
    variant: Variant,
    probe_id: str,
) -> tuple[LogicalEvent, ...]:
    if _selected(variant.scope, probe_id) and variant.mutation.startswith("masked_"):
        return base
    source = actual
    if not _selected(variant.scope, probe_id):
        return source
    if variant.mutation == "observer_drop":
        return ()
    if variant.mutation == "observer_duplicate":
        return source + source
    return source


def _project_token(kind: str, value: str, probe_id: str, channel: str) -> str:
    if kind == "identity":
        return value
    if kind == "constant_redaction":
        return "T-REDACTED" if channel == "target" else "P-REDACTED"
    if kind == "global_bijection":
        return _flip(value)
    if kind == "probe_local_bijection":
        return _flip(value) if probe_id == "p1" else value
    raise AssertionError(kind)


def _observations(
    audit_by_probe,
    projection: ProjectionPolicy,
    variant: Variant,
) -> tuple[ProbeObservation, ...]:
    result = []
    for probe_id in ("p1", "p2"):
        target_kind = projection.target.kind
        if variant.mutation == "projection_misdeclare":
            target_kind = "probe_local_bijection"
        events = tuple(
            ObservedEvent(
                kind=item.kind,
                target_token=_project_token(target_kind, item.target, probe_id, "target"),
                payload_token=_project_token(
                    projection.payload.kind, item.payload, probe_id, "payload"
                ),
            )
            for item in audit_by_probe[probe_id]
        )
        result.append(ProbeObservation(probe_id=probe_id, events=events))
    return tuple(result)


def _operand_value(operand, values):
    if isinstance(operand, LiteralValue):
        return operand.value
    return values[(operand.probe_id, operand.channel)]


def _independent_truth(formula, values) -> bool:
    if isinstance(formula, CompareExpr):
        left = _operand_value(formula.left, values)
        right = _operand_value(formula.right, values)
        return left == right if formula.operator == "eq" else left != right
    results = [_independent_truth(child, values) for child in formula.children]
    if formula.operator == "and":
        return all(results)
    if formula.operator == "or":
        return any(results)
    return not results[0]


def _hidden_valid(contract, actual_by_probe) -> bool:
    allowed = set(contract.allowed_auxiliary_kinds)
    values = {}
    for probe_id in ("p1", "p2"):
        events = actual_by_probe.get(probe_id, ())
        primary = tuple(item for item in events if item.kind == contract.primary_kind)
        if len(primary) != 1:
            return False
        if any(item.kind != contract.primary_kind and item.kind not in allowed for item in events):
            return False
        values[(probe_id, "target")] = primary[0].target
        values[(probe_id, "payload")] = primary[0].payload
    return _independent_truth(contract.relation_claims[0].formula, values)


def _observed_structural_valid(contract, observations) -> bool:
    allowed = set(contract.allowed_auxiliary_kinds)
    for observation in observations:
        primary = tuple(item for item in observation.events if item.kind == contract.primary_kind)
        if len(primary) != 1:
            return False
        if any(item.kind != contract.primary_kind and item.kind not in allowed for item in observation.events):
            return False
    return True


def _direct_observable_valid(contract, observations) -> bool:
    if not _observed_structural_valid(contract, observations):
        return False
    values = {}
    for observation in observations:
        primary = next(item for item in observation.events if item.kind == contract.primary_kind)
        values[(observation.probe_id, "target")] = primary.target_token
        values[(observation.probe_id, "payload")] = primary.payload_token
    return _independent_truth(contract.relation_claims[0].formula, values)


class SQLiteEngine:
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        for operation in OPERATIONS:
            for stream in ("state", "audit"):
                self.connection.execute(
                    f'CREATE TABLE "{stream}_{operation}" '
                    "(case_id TEXT, probe_id TEXT, seq INTEGER, kind TEXT, target TEXT, payload TEXT)"
                )

    def put(self, operation, case_id, actual_by_probe, audit_by_probe):
        with self.connection:
            for stream, source in (
                ("state", actual_by_probe),
                ("audit", audit_by_probe),
            ):
                for probe_id, events in source.items():
                    for seq, item in enumerate(events):
                        self.connection.execute(
                            f'INSERT INTO "{stream}_{operation}" VALUES (?, ?, ?, ?, ?, ?)',
                            (case_id, probe_id, seq, item.kind, item.target, item.payload),
                        )

    def _read(self, stream, operation, case_id):
        rows = self.connection.execute(
            f'SELECT probe_id, kind, target, payload FROM "{stream}_{operation}" '
            "WHERE case_id = ? ORDER BY probe_id, seq",
            (case_id,),
        ).fetchall()
        result = {"p1": [], "p2": []}
        for probe_id, kind, target, payload in rows:
            result[probe_id].append(LogicalEvent(kind, target, payload))
        return {key: tuple(value) for key, value in result.items()}

    def read_actual(self, operation, case_id):
        return self._read("state", operation, case_id)

    def read_audit(self, operation, case_id):
        return self._read("audit", operation, case_id)

    def facts(self):
        return {
            "engine": "sqlite",
            "sqlite_version": sqlite3.sqlite_version,
            "journal_mode": self.connection.execute("PRAGMA journal_mode").fetchone()[0],
            "table_count": len(OPERATIONS) * 2,
            "adapter_path": "独立 audit_* 表",
        }


class GitAsyncEngine:
    def __init__(self, root: Path):
        self.root = root
        self.queue = []
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "CRL Pilot"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "crl-pilot@example.invalid"], cwd=root, check=True)

    def put(self, operation, case_id, actual_by_probe, audit_by_probe):
        for stream, source in (("state", actual_by_probe), ("collector", audit_by_probe)):
            for probe_id, events in source.items():
                self.queue.append((2, stream, operation, case_id, probe_id, events))

    def drain(self):
        attempts = 0
        applied = 0
        for round_id in (1, 2):
            pending = []
            for ready_round, stream, operation, case_id, probe_id, events in self.queue:
                attempts += 1
                if ready_round > round_id:
                    pending.append((ready_round, stream, operation, case_id, probe_id, events))
                    continue
                path = self.root / stream / operation / case_id / f"{probe_id}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps([asdict(item) for item in events], sort_keys=True),
                    encoding="utf-8",
                    newline="\n",
                )
                applied += 1
            self.queue = pending
        subprocess.run(["git", "add", "state", "collector"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "apply converged CRL pilot batch"],
            cwd=self.root,
            check=True,
        )
        self.attempts = attempts
        self.applied = applied

    def _read(self, stream, operation, case_id):
        result = {}
        for probe_id in ("p1", "p2"):
            relative = f"{stream}/{operation}/{case_id}/{probe_id}.json"
            completed = subprocess.run(
                ["git", "show", f"HEAD:{relative}"],
                cwd=self.root,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            result[probe_id] = tuple(LogicalEvent(**item) for item in json.loads(completed.stdout))
        return result

    def read_actual(self, operation, case_id):
        return self._read("state", operation, case_id)

    def read_audit(self, operation, case_id):
        return self._read("collector", operation, case_id)

    def facts(self):
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.splitlines()
        return {
            "engine": "git-async-two-round",
            "git_version": subprocess.run(
                ["git", "--version"], check=True, capture_output=True, text=True
            ).stdout.strip(),
            "converged_commit": commit,
            "working_tree_clean": not bool(status),
            "queued_task_attempts": self.attempts,
            "applied_tasks": self.applied,
            "tracked_state_files": len(tracked),
            "state_files": sum(path.startswith("state/") for path in tracked),
            "collector_files": sum(path.startswith("collector/") for path in tracked),
            "adapter_path": "独立 Git collector 跟踪文件",
        }


def _metrics(rows, method, *, trusted_only=False, identifiable_only=False):
    selected = [
        row
        for row in rows
        if not trusted_only
        or row["variant_category"] in {"clean", "service"}
    ]
    if identifiable_only:
        selected = [row for row in selected if row["identifiable"]]
    tp = sum(row["hidden_valid"] and row[method] for row in selected)
    tn = sum(not row["hidden_valid"] and not row[method] for row in selected)
    fp = sum(not row["hidden_valid"] and row[method] for row in selected)
    fn = sum(row["hidden_valid"] and not row[method] for row in selected)
    return {
        "cases": len(selected),
        "true_accept": tp,
        "true_reject": tn,
        "false_admission": fp,
        "false_rejection": fn,
        "accuracy": (tp + tn) / len(selected) if selected else 0.0,
        "false_admission_rate_on_invalid": fp / (fp + tn) if fp + tn else 0.0,
        "false_rejection_rate_on_valid": fn / (fn + tp) if fn + tp else 0.0,
    }


def _run_service(service: str, engine):
    rows = []
    plans = {}
    replay_cache = set()
    started = time.perf_counter()
    variants = (Variant("clean", "clean", "", "", "clean"),) + _variants(service)
    pending = []
    for operation, formula_name, contract, projection, desired in _contracts(service):
        compile_start = time.perf_counter_ns()
        plan = compile_contract(contract, projection)
        compile_ns = time.perf_counter_ns() - compile_start
        plans[operation] = {
            "contract_hash": canonical_hash(contract),
            "projection_hash": canonical_hash(projection),
            "plan_hash": plan.plan_hash,
            "identifiable": not bool(plan.nonidentifiable),
            "probe_count": len(plan.probes),
            "monitor_cases": sum(len(item.cases) for item in plan.monitors),
            "compile_nanoseconds": compile_ns,
        }
        desired_by_probe = {
            "p1": (desired[0], desired[2]),
            "p2": (desired[1], desired[3]),
        }
        for variant in variants:
            case_id = f"{operation}--{variant.name}"
            actual_by_probe = {}
            audit_by_probe = {}
            for probe_id in ("p1", "p2"):
                target, payload = desired_by_probe[probe_id]
                base = (LogicalEvent(contract.primary_kind, target, payload),)
                actual = base if variant.mutation == "clean" else _mutate_actual(base, variant, probe_id)
                audit = base if variant.mutation == "clean" else _audit_source(base, actual, variant, probe_id)
                actual_by_probe[probe_id] = actual
                audit_by_probe[probe_id] = audit
            engine.put(operation, case_id, actual_by_probe, audit_by_probe)
            pending.append(
                {
                    "service": service,
                    "operation": operation,
                    "formula": formula_name,
                    "variant": variant.name,
                    "variant_category": variant.category,
                    "case_id": case_id,
                    "identifiable": not bool(plan.nonidentifiable),
                    "target_projection": projection.target.kind,
                    "payload_projection": projection.payload.kind,
                    "contract": contract,
                    "projection": projection,
                    "plan": plan,
                    "variant_object": variant,
                }
            )
    if service == "git":
        engine.drain()
    for row in pending:
        actual = engine.read_actual(row["operation"], row["case_id"])
        audit = engine.read_audit(row["operation"], row["case_id"])
        contract = row["contract"]
        projection = row["projection"]
        plan = row["plan"]
        observations = _observations(audit, projection, row["variant_object"])
        report = evaluate_observations(contract, projection, plan, observations)
        evidence = EvidenceBundle(contract, projection, plan, observations, report)
        nonce = base64.urlsafe_b64encode(row["case_id"].encode("utf-8")).decode("ascii")
        record = issue_attestation(
            evidence,
            issuer_id=f"{service}-issuer",
            issuer_key=ISSUER_KEY,
            tool_id=f"{service}-tool",
            tool_version="1.0",
            issued_at=ISSUED_AT,
            expires_at=ISSUED_AT + 1000,
            nonce=nonce,
        )
        request = AdmissionRequest(
            tool_id=f"{service}-tool",
            tool_version="1.0",
            contract_hash=plan.contract_hash,
            projection_hash=plan.projection_hash,
            plan_hash=plan.plan_hash,
            required_claims=contract_claim_refs(contract),
        )
        decision = verify_and_admit(
            AdmissionBundle(contract, projection, plan, observations, report, record),
            request,
            trusted_issuers={f"{service}-issuer": ISSUER_KEY},
            replay_cache=replay_cache,
            now=ISSUED_AT + 1,
        )
        hidden_valid = _hidden_valid(row["contract"], actual)
        row["candidate"] = decision.allowed
        row["unsigned_candidate"] = (
            report.complete
            and not report.failed_claims
            and not report.nonidentifiable_claims
        )
        row["direct_observable"] = _direct_observable_valid(contract, observations)
        row["provenance_only"] = _observed_structural_valid(contract, observations)
        row["reject_all_relations"] = False
        row["hidden_valid"] = hidden_valid
        row["hidden_state_upper_bound"] = hidden_valid
        for internal in ("contract", "projection", "plan", "variant_object"):
            del row[internal]
        rows.append(row)
    elapsed = time.perf_counter() - started
    return rows, plans, engine.facts(), elapsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    sqlite_engine = SQLiteEngine()
    sqlite_rows, sqlite_plans, sqlite_facts, sqlite_seconds = _run_service(
        "sqlite", sqlite_engine
    )
    with tempfile.TemporaryDirectory(prefix="crl-v007-git-") as temporary:
        git_engine = GitAsyncEngine(Path(temporary))
        git_rows, git_plans, git_facts, git_seconds = _run_service("git", git_engine)
    rows = sqlite_rows + git_rows
    fieldnames = tuple(rows[0])
    with (output_dir / "pilot_cases.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    methods = (
        "candidate",
        "unsigned_candidate",
        "direct_observable",
        "provenance_only",
        "reject_all_relations",
        "hidden_state_upper_bound",
    )
    summary = {
        "schema": "v007-large-pilot-1",
        "services": 2,
        "contracts_per_service": 10,
        "fault_operators_per_service": 40,
        "clean_implementations_per_service": 10,
        "case_count": len(rows),
        "service_case_counts": {
            "sqlite": len(sqlite_rows),
            "git": len(git_rows),
        },
        "metrics_all": {method: _metrics(rows, method) for method in methods},
        "metrics_trusted_observer": {
            method: _metrics(rows, method, trusted_only=True) for method in methods
        },
        "metrics_trusted_observer_identifiable_contracts": {
            method: _metrics(
                rows, method, trusted_only=True, identifiable_only=True
            )
            for method in methods
        },
        "metrics_by_service": {
            service: {
                method: _metrics(
                    [row for row in rows if row["service"] == service], method
                )
                for method in methods
            }
            for service in ("sqlite", "git")
        },
        "observer_fault_cases": sum(
            row["variant_category"] not in {"clean", "service"} for row in rows
        ),
        "candidate_false_admissions_by_category": {
            category: sum(
                row["candidate"] and not row["hidden_valid"]
                for row in rows
                if row["variant_category"] == category
            )
            for category in sorted({row["variant_category"] for row in rows})
        },
        "candidate_false_rejections_by_category": {
            category: sum(
                not row["candidate"] and row["hidden_valid"]
                for row in rows
                if row["variant_category"] == category
            )
            for category in sorted({row["variant_category"] for row in rows})
        },
        "execution_seconds": {"sqlite": sqlite_seconds, "git": git_seconds},
        "probe_calls": len(rows) * 2,
        "authoring_time": None,
        "authoring_time_reason": "执行由单一 AI 研究者实现，不能捏造独立人工作者时间；报告静态合同与计划规模及运行耗时。",
    }
    (output_dir / "pilot_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "engine_facts.json").write_text(
        json.dumps(
            {"sqlite": sqlite_facts, "git": git_facts},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "contract_plans.json").write_text(
        json.dumps(
            {"sqlite": sqlite_plans, "git": git_plans},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    # 正式编排器跨 Windows 管道读取；ASCII 转义避免控制台代码页歧义。
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
