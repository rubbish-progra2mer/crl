#!/usr/bin/env python3
"""观察闭包效应证书的最小参考实现。

该实现只支持一元主效应合同。它把合同义务、匿名审计投影和关系探针
一起编译，并把不可由该投影辨识的主张保留为成对隐藏世界见证。
消费端只能使用绑定一致、已通过且属于观察闭包的主张。
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from typing import Iterable, Literal


TargetRequirement = Literal["none", "responsive", "identity"]
Visibility = Literal["revealed", "stable_anonymous", "clone_local_anonymous"]

SUPPORTED_FACTORS = ("ambient_canary", "sensitive_input")
SUPPORTED_VISIBILITIES = (
    "revealed",
    "stable_anonymous",
    "clone_local_anonymous",
)
SUPPORTED_TARGET_REQUIREMENTS = ("none", "responsive", "identity")

CLAIM_COUNT = "probe.primary_count.exactly_one"
CLAIM_AUXILIARY = "probe.auxiliary_kinds.allowed_only"
CLAIM_TARGET_RESPONSIVE = "relation.target.responsive"
CLAIM_TARGET_IDENTITY = "relation.target.identity"


class UnsupportedContract(ValueError):
    """合同落在本实现明确拒绝的域外。"""


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)  # type: ignore[arg-type]
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def payload_claim(factor: str) -> str:
    return f"relation.payload.invariant:{factor}"


@dataclass(frozen=True)
class EffectContract:
    contract_version: str
    primary_kind: str
    exact_primary_count: int
    allowed_auxiliary_kinds: tuple[str, ...]
    target_requirement: TargetRequirement
    payload_forbidden_factors: tuple[str, ...]


@dataclass(frozen=True)
class ProjectionSpec:
    projection_version: str
    target_visibility: Visibility
    payload_visibility: Visibility
    normalizer_id: str


@dataclass(frozen=True)
class Probe:
    probe_id: str
    target_value: str = "base"
    input_value: str = "public"
    ambient_canary: str = "none"


@dataclass(frozen=True)
class Relation:
    claim_id: str
    relation_kind: str
    left_probe: str
    right_probe: str | None
    expected_value: str | None = None


@dataclass(frozen=True)
class HiddenWorld:
    target_outputs: tuple[str, str]
    payload_outputs: tuple[str, str]
    target_maps: tuple[str, str]
    payload_maps: tuple[str, str]


@dataclass(frozen=True)
class NonIdentifiabilityWitness:
    claim_id: str
    reason: str
    world_true: HiddenWorld
    world_false: HiddenWorld
    shared_observation: tuple[str, ...]


@dataclass(frozen=True)
class CompiledPlan:
    schema_version: int
    contract_hash: str
    projection_hash: str
    probe_catalog_hash: str
    plan_hash: str
    primary_kind: str
    exact_primary_count: int
    allowed_auxiliary_kinds: tuple[str, ...]
    probes: tuple[Probe, ...]
    relations: tuple[Relation, ...]
    contract_claims: tuple[str, ...]
    identifiable_claims: tuple[str, ...]
    nonidentifiable: tuple[NonIdentifiabilityWitness, ...]


@dataclass(frozen=True, order=True)
class ObservedEvent:
    kind: str
    target_token: str
    payload_token: str


@dataclass(frozen=True)
class ProbeObservation:
    probe_id: str
    events: tuple[ObservedEvent, ...]


@dataclass(frozen=True)
class ExecutionReport:
    complete: bool
    passed_claims: tuple[str, ...]
    failed_claims: tuple[str, ...]
    witnesses: tuple[str, ...]
    observed_probe_ids: tuple[str, ...]


@dataclass(frozen=True)
class CoverageRecord:
    schema_version: int
    status: str
    tool_id: str
    tool_version: str
    contract_hash: str
    projection_hash: str
    probe_catalog_hash: str
    plan_hash: str
    evidence_hash: str
    contract_claims: tuple[str, ...]
    passed_claims: tuple[str, ...]
    failed_claims: tuple[str, ...]
    nonidentifiable_claims: tuple[str, ...]
    nonidentifiability_witness_hashes: tuple[str, ...]
    record_digest: str


@dataclass(frozen=True)
class AdmissionRequest:
    tool_id: str
    tool_version: str
    contract_hash: str
    projection_hash: str
    probe_catalog_hash: str
    plan_hash: str
    evidence_hash: str
    required_claims: tuple[str, ...]


@dataclass(frozen=True)
class AdmissionDecision:
    allowed: bool
    reasons: tuple[str, ...]


def _validate_contract(contract: EffectContract, projection: ProjectionSpec) -> None:
    if not contract.contract_version:
        raise UnsupportedContract("合同版本不能为空")
    if not contract.primary_kind:
        raise UnsupportedContract("主效应类型不能为空")
    if contract.exact_primary_count != 1:
        raise UnsupportedContract(
            "当前方法只支持一元主效应合同；exact_primary_count 必须等于 1"
        )
    if contract.target_requirement not in SUPPORTED_TARGET_REQUIREMENTS:
        raise UnsupportedContract(
            f"不支持的目标义务：{contract.target_requirement!r}"
        )
    unknown_factors = set(contract.payload_forbidden_factors) - set(
        SUPPORTED_FACTORS
    )
    if unknown_factors:
        raise UnsupportedContract(
            f"不支持的载荷禁止因素：{sorted(unknown_factors)}"
        )
    if len(set(contract.payload_forbidden_factors)) != len(
        contract.payload_forbidden_factors
    ):
        raise UnsupportedContract("载荷禁止因素不能重复")
    if contract.primary_kind in set(contract.allowed_auxiliary_kinds):
        raise UnsupportedContract("主效应类型不能同时声明为辅助效应")
    if len(set(contract.allowed_auxiliary_kinds)) != len(
        contract.allowed_auxiliary_kinds
    ):
        raise UnsupportedContract("允许的辅助效应类型不能重复")
    if projection.target_visibility not in SUPPORTED_VISIBILITIES:
        raise UnsupportedContract(
            f"不支持的目标可见性：{projection.target_visibility!r}"
        )
    if projection.payload_visibility not in SUPPORTED_VISIBILITIES:
        raise UnsupportedContract(
            f"不支持的载荷可见性：{projection.payload_visibility!r}"
        )
    if not projection.projection_version or not projection.normalizer_id:
        raise UnsupportedContract("投影版本和规范化器标识不能为空")


def _world(
    targets: tuple[str, str],
    payloads: tuple[str, str],
    target_maps: tuple[str, str],
    payload_maps: tuple[str, str],
) -> HiddenWorld:
    return HiddenWorld(targets, payloads, target_maps, payload_maps)


def _target_responsive_witness() -> NonIdentifiabilityWitness:
    return NonIdentifiabilityWitness(
        claim_id=CLAIM_TARGET_RESPONSIVE,
        reason="克隆局部目标令牌不能跨探针对齐",
        world_true=_world(
            ("t0", "t1"), ("p0", "p0"), ("identity", "swap"), ("identity", "identity")
        ),
        world_false=_world(
            ("t0", "t0"), ("p0", "p0"), ("identity", "identity"), ("identity", "identity")
        ),
        shared_observation=("target:q0", "target:q0"),
    )


def _target_identity_witness(stable: bool) -> NonIdentifiabilityWitness:
    maps_true = ("identity", "identity")
    maps_false = ("swap", "swap") if stable else ("swap", "swap")
    return NonIdentifiabilityWitness(
        claim_id=CLAIM_TARGET_IDENTITY,
        reason=(
            "稳定匿名目标令牌保留相等关系但不暴露输入身份"
            if stable
            else "克隆局部目标令牌既不暴露身份也不能跨探针对齐"
        ),
        world_true=_world(
            ("t0", "t1"), ("p0", "p0"), maps_true, ("identity", "identity")
        ),
        world_false=_world(
            ("t1", "t0"), ("p0", "p0"), maps_false, ("identity", "identity")
        ),
        shared_observation=("target:q0", "target:q1"),
    )


def _payload_witness(factor: str) -> NonIdentifiabilityWitness:
    claim_id = payload_claim(factor)
    return NonIdentifiabilityWitness(
        claim_id=claim_id,
        reason=f"克隆局部载荷令牌不能跨 {factor} 探针对齐",
        world_true=_world(
            ("t0", "t0"), ("p0", "p0"), ("identity", "identity"), ("identity", "identity")
        ),
        world_false=_world(
            ("t0", "t0"), ("p0", "p1"), ("identity", "identity"), ("identity", "swap")
        ),
        shared_observation=("payload:q0", "payload:q0"),
    )


def _add_probe(probes: dict[str, Probe], probe: Probe) -> None:
    previous = probes.get(probe.probe_id)
    if previous is not None and previous != probe:
        raise RuntimeError(f"探针标识冲突：{probe.probe_id}")
    probes[probe.probe_id] = probe


def compile_contract(
    contract: EffectContract, projection: ProjectionSpec
) -> CompiledPlan:
    """编译一元合同，并显式保留投影相关的不可辨识见证。"""

    _validate_contract(contract, projection)
    contract_hash = canonical_hash(contract)
    projection_hash = canonical_hash(projection)
    probes: dict[str, Probe] = {"base": Probe("base")}
    relations: list[Relation] = []
    nonidentifiable: list[NonIdentifiabilityWitness] = []
    contract_claims = [CLAIM_COUNT, CLAIM_AUXILIARY]
    identifiable = [CLAIM_COUNT, CLAIM_AUXILIARY]

    if contract.target_requirement == "responsive":
        contract_claims.append(CLAIM_TARGET_RESPONSIVE)
        if projection.target_visibility in {"revealed", "stable_anonymous"}:
            left = Probe("target_0", target_value="target_zero")
            right = Probe("target_1", target_value="target_one")
            _add_probe(probes, left)
            _add_probe(probes, right)
            relations.append(
                Relation(
                    CLAIM_TARGET_RESPONSIVE,
                    "target_not_equal",
                    left.probe_id,
                    right.probe_id,
                )
            )
            identifiable.append(CLAIM_TARGET_RESPONSIVE)
        else:
            nonidentifiable.append(_target_responsive_witness())
    elif contract.target_requirement == "identity":
        contract_claims.append(CLAIM_TARGET_IDENTITY)
        if projection.target_visibility == "revealed":
            for index, target_value in enumerate(("target_zero", "target_one")):
                probe = Probe(f"target_identity_{index}", target_value=target_value)
                _add_probe(probes, probe)
                relations.append(
                    Relation(
                        CLAIM_TARGET_IDENTITY,
                        "target_equals_expected",
                        probe.probe_id,
                        None,
                        expected_value=target_value,
                    )
                )
            identifiable.append(CLAIM_TARGET_IDENTITY)
        else:
            nonidentifiable.append(
                _target_identity_witness(
                    projection.target_visibility == "stable_anonymous"
                )
            )

    for factor in sorted(contract.payload_forbidden_factors):
        claim_id = payload_claim(factor)
        contract_claims.append(claim_id)
        if projection.payload_visibility in {"revealed", "stable_anonymous"}:
            if factor == "ambient_canary":
                left = Probe("ambient_0", ambient_canary="ambient_red")
                right = Probe("ambient_1", ambient_canary="ambient_blue")
            elif factor == "sensitive_input":
                left = Probe("sensitive_0", input_value="canary_red")
                right = Probe("sensitive_1", input_value="canary_blue")
            else:  # 被 _validate_contract 封闭，仅作防御性保护。
                raise UnsupportedContract(f"未知载荷因素：{factor}")
            _add_probe(probes, left)
            _add_probe(probes, right)
            relations.append(
                Relation(
                    claim_id,
                    "payload_equal",
                    left.probe_id,
                    right.probe_id,
                )
            )
            identifiable.append(claim_id)
        else:
            nonidentifiable.append(_payload_witness(factor))

    ordered_probes = tuple(probes[key] for key in sorted(probes))
    ordered_relations = tuple(
        sorted(
            relations,
            key=lambda item: (
                item.claim_id,
                item.relation_kind,
                item.left_probe,
                item.right_probe or "",
            ),
        )
    )
    probe_catalog_hash = canonical_hash([asdict(item) for item in ordered_probes])
    plan_payload = {
        "schema_version": 1,
        "contract_hash": contract_hash,
        "projection_hash": projection_hash,
        "probe_catalog_hash": probe_catalog_hash,
        "primary_kind": contract.primary_kind,
        "exact_primary_count": contract.exact_primary_count,
        "allowed_auxiliary_kinds": sorted(contract.allowed_auxiliary_kinds),
        "probes": [asdict(item) for item in ordered_probes],
        "relations": [asdict(item) for item in ordered_relations],
        "contract_claims": sorted(contract_claims),
        "identifiable_claims": sorted(identifiable),
        "nonidentifiable": [asdict(item) for item in nonidentifiable],
    }
    return CompiledPlan(
        schema_version=1,
        contract_hash=contract_hash,
        projection_hash=projection_hash,
        probe_catalog_hash=probe_catalog_hash,
        plan_hash=canonical_hash(plan_payload),
        primary_kind=contract.primary_kind,
        exact_primary_count=contract.exact_primary_count,
        allowed_auxiliary_kinds=tuple(sorted(contract.allowed_auxiliary_kinds)),
        probes=ordered_probes,
        relations=ordered_relations,
        contract_claims=tuple(sorted(contract_claims)),
        identifiable_claims=tuple(sorted(identifiable)),
        nonidentifiable=tuple(nonidentifiable),
    )


def evaluate_observations(
    plan: CompiledPlan, observations: Iterable[ProbeObservation]
) -> ExecutionReport:
    """在匿名观察上执行计划，不访问合同或隐藏世界。"""

    observation_list = list(observations)
    by_probe: dict[str, ProbeObservation] = {}
    witnesses: set[str] = set()
    expected_probe_ids = {probe.probe_id for probe in plan.probes}
    for observation in observation_list:
        if observation.probe_id in by_probe:
            witnesses.add(f"duplicate_probe:{observation.probe_id}")
        by_probe[observation.probe_id] = observation
    observed_ids = set(by_probe)
    for missing in sorted(expected_probe_ids - observed_ids):
        witnesses.add(f"missing_probe:{missing}")
    for extra in sorted(observed_ids - expected_probe_ids):
        witnesses.add(f"unexpected_probe:{extra}")

    primary: dict[str, ObservedEvent] = {}
    count_ok = True
    auxiliary_ok = True
    allowed = set(plan.allowed_auxiliary_kinds)
    for probe_id in sorted(expected_probe_ids & observed_ids):
        events = by_probe[probe_id].events
        main = [event for event in events if event.kind == plan.primary_kind]
        unexpected = [
            event
            for event in events
            if event.kind != plan.primary_kind and event.kind not in allowed
        ]
        if len(main) != plan.exact_primary_count:
            count_ok = False
            witnesses.add(f"{probe_id}:primary_count={len(main)}")
        if unexpected:
            auxiliary_ok = False
            witnesses.add(
                f"{probe_id}:unexpected="
                + ",".join(sorted(event.kind for event in unexpected))
            )
        if len(main) == 1:
            primary[probe_id] = main[0]

    complete = (
        observed_ids == expected_probe_ids
        and len(observation_list) == len(expected_probe_ids)
    )
    if not complete:
        count_ok = False
        auxiliary_ok = False

    claim_results: dict[str, list[bool]] = {
        CLAIM_COUNT: [count_ok],
        CLAIM_AUXILIARY: [auxiliary_ok],
    }
    for relation in plan.relations:
        left = primary.get(relation.left_probe)
        right = primary.get(relation.right_probe) if relation.right_probe else None
        passed = False
        if relation.relation_kind == "target_not_equal":
            passed = left is not None and right is not None and (
                left.target_token != right.target_token
            )
        elif relation.relation_kind == "target_equals_expected":
            passed = (
                left is not None
                and relation.expected_value is not None
                and left.target_token == relation.expected_value
            )
        elif relation.relation_kind == "payload_equal":
            passed = left is not None and right is not None and (
                left.payload_token == right.payload_token
            )
        else:
            raise RuntimeError(f"未知关系类型：{relation.relation_kind}")
        claim_results.setdefault(relation.claim_id, []).append(passed)
        if not passed:
            witnesses.add(
                f"relation_failed:{relation.claim_id}:{relation.left_probe}:"
                f"{relation.right_probe or '-'}"
            )

    passed_claims = tuple(
        sorted(claim for claim, results in claim_results.items() if all(results))
    )
    failed_claims = tuple(
        sorted(claim for claim, results in claim_results.items() if not all(results))
    )
    return ExecutionReport(
        complete=complete,
        passed_claims=passed_claims,
        failed_claims=failed_claims,
        witnesses=tuple(sorted(witnesses)),
        observed_probe_ids=tuple(sorted(observed_ids)),
    )


def _record_payload(record: CoverageRecord) -> dict[str, object]:
    payload = asdict(record)
    payload.pop("record_digest", None)
    return payload


def issue_record(
    plan: CompiledPlan,
    report: ExecutionReport,
    *,
    tool_id: str,
    tool_version: str,
    evidence_hash: str | None = None,
) -> CoverageRecord:
    """签发语义记录；散列只用于绑定，不提供恶意签发者认证。"""

    if not tool_id or not tool_version:
        raise ValueError("工具标识和版本不能为空")
    evidence_hash = evidence_hash or canonical_hash(report)
    nonidentifiable_claims = tuple(
        sorted(item.claim_id for item in plan.nonidentifiable)
    )
    witness_hashes = tuple(
        sorted(canonical_hash(item) for item in plan.nonidentifiable)
    )
    status = (
        "pass"
        if report.complete
        and not report.failed_claims
        and not nonidentifiable_claims
        and set(plan.contract_claims).issubset(set(report.passed_claims))
        else "incomplete_or_failed"
    )
    record = CoverageRecord(
        schema_version=1,
        status=status,
        tool_id=tool_id,
        tool_version=tool_version,
        contract_hash=plan.contract_hash,
        projection_hash=plan.projection_hash,
        probe_catalog_hash=plan.probe_catalog_hash,
        plan_hash=plan.plan_hash,
        evidence_hash=evidence_hash,
        contract_claims=plan.contract_claims,
        passed_claims=report.passed_claims,
        failed_claims=report.failed_claims,
        nonidentifiable_claims=nonidentifiable_claims,
        nonidentifiability_witness_hashes=witness_hashes,
        record_digest="",
    )
    return replace(record, record_digest=canonical_hash(_record_payload(record)))


def consume_record(
    record: CoverageRecord, request: AdmissionRequest
) -> AdmissionDecision:
    """失败关闭的最小接入消费者。"""

    reasons: list[str] = []
    if record.schema_version != 1:
        reasons.append(f"unsupported_record_schema:{record.schema_version}")
    if canonical_hash(_record_payload(record)) != record.record_digest:
        reasons.append("record_digest_mismatch")
    bindings = (
        ("tool_id", record.tool_id, request.tool_id),
        ("tool_version", record.tool_version, request.tool_version),
        ("contract_hash", record.contract_hash, request.contract_hash),
        ("projection_hash", record.projection_hash, request.projection_hash),
        (
            "probe_catalog_hash",
            record.probe_catalog_hash,
            request.probe_catalog_hash,
        ),
        ("plan_hash", record.plan_hash, request.plan_hash),
        ("evidence_hash", record.evidence_hash, request.evidence_hash),
    )
    for name, actual, expected in bindings:
        if actual != expected:
            reasons.append(f"{name}_mismatch")
    if record.status != "pass":
        reasons.append(f"record_status:{record.status}")
    required = set(request.required_claims)
    contract_claims = set(record.contract_claims)
    passed = set(record.passed_claims)
    nonidentifiable = set(record.nonidentifiable_claims)
    if not required:
        reasons.append("empty_required_claims")
    for claim in sorted(required - contract_claims):
        reasons.append(f"claim_not_in_contract:{claim}")
    for claim in sorted(required & nonidentifiable):
        reasons.append(f"claim_nonidentifiable:{claim}")
    for claim in sorted(required - passed):
        reasons.append(f"claim_not_passed:{claim}")
    return AdmissionDecision(not reasons, tuple(reasons))


def request_for_plan(
    plan: CompiledPlan,
    *,
    tool_id: str,
    tool_version: str,
    evidence_hash: str,
) -> AdmissionRequest:
    return AdmissionRequest(
        tool_id=tool_id,
        tool_version=tool_version,
        contract_hash=plan.contract_hash,
        projection_hash=plan.projection_hash,
        probe_catalog_hash=plan.probe_catalog_hash,
        plan_hash=plan.plan_hash,
        evidence_hash=evidence_hash,
        required_claims=plan.contract_claims,
    )
