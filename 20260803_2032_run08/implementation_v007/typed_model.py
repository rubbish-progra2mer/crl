#!/usr/bin/env python3
"""v007 的带类型合同、投影、计划、报告和接入证明数据模型。"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field, is_dataclass, replace
from typing import Any, Literal, Mapping, TypeVar


ProjectionKind = Literal[
    "identity",
    "global_bijection",
    "probe_local_bijection",
    "constant_redaction",
]
Channel = Literal["target", "payload"]
CompareOperator = Literal["eq", "ne"]
BooleanOperator = Literal["and", "or", "not"]


class SchemaError(ValueError):
    """输入不满足封闭类型模式。"""


class IntegrityError(ValueError):
    """自描述散列、签名或派生字段不一致。"""


def canonical_json(value: object) -> str:
    if is_dataclass(value) and not isinstance(value, type):
        value = asdict(value)  # type: ignore[arg-type]
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda item: asdict(item)
        if is_dataclass(item) and not isinstance(item, type)
        else _raise_not_serializable(item),
    )


def _raise_not_serializable(value: object) -> object:
    raise TypeError(f"{type(value).__name__} 不能进行规范 JSON 序列化")


def canonical_bytes(value: object) -> bytes:
    return canonical_json(value).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _strict_keys(
    value: Mapping[str, Any], expected: set[str], *, where: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise SchemaError(
            f"{where} 字段不匹配；缺少={sorted(expected-actual)}，"
            f"多余={sorted(actual-expected)}"
        )


def _text(value: Any, *, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise SchemaError(f"{where} 必须是非空字符串")
    return value


def _integer(value: Any, *, where: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SchemaError(f"{where} 必须是整数")
    return value


def _boolean(value: Any, *, where: str) -> bool:
    if not isinstance(value, bool):
        raise SchemaError(f"{where} 必须是布尔值")
    return value


def _list(value: Any, *, where: str) -> list[Any]:
    if not isinstance(value, list):
        raise SchemaError(f"{where} 必须是列表")
    return value


def _mapping(value: Any, *, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise SchemaError(f"{where} 必须是对象")
    return value


@dataclass(frozen=True)
class ProbeSpec:
    node_type: str = field(default="probe", init=False)
    probe_id: str = ""
    factors: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class FieldRef:
    node_type: str = field(default="field_ref", init=False)
    probe_id: str = ""
    channel: Channel = "target"


@dataclass(frozen=True)
class LiteralValue:
    node_type: str = field(default="literal", init=False)
    value: str = ""


Operand = FieldRef | LiteralValue


@dataclass(frozen=True)
class CompareExpr:
    node_type: str = field(default="compare", init=False)
    operator: CompareOperator = "eq"
    left: Operand = field(default_factory=FieldRef)
    right: Operand = field(default_factory=LiteralValue)


@dataclass(frozen=True)
class BooleanExpr:
    node_type: str = field(default="boolean", init=False)
    operator: BooleanOperator = "and"
    children: tuple["Formula", ...] = ()


Formula = CompareExpr | BooleanExpr


@dataclass(frozen=True)
class RelationClaim:
    node_type: str = field(default="relation_claim", init=False)
    display_name: str = ""
    probes: tuple[ProbeSpec, ...] = ()
    formula: Formula = field(default_factory=CompareExpr)


@dataclass(frozen=True)
class CountPolicy:
    node_type: str = field(default="count_policy", init=False)
    minimum: int = 1
    maximum: int = 1


@dataclass(frozen=True)
class EffectContract:
    schema_type: str = field(default="effect_contract", init=False)
    schema_version: int = 1
    contract_id: str = ""
    contract_version: str = ""
    primary_kind: str = ""
    count_policy: CountPolicy = field(default_factory=CountPolicy)
    allowed_auxiliary_kinds: tuple[str, ...] = ()
    structural_probe: ProbeSpec = field(
        default_factory=lambda: ProbeSpec(probe_id="structural_base")
    )
    relation_claims: tuple[RelationClaim, ...] = ()


@dataclass(frozen=True)
class ChannelProjection:
    node_type: str = field(default="channel_projection", init=False)
    kind: ProjectionKind = "identity"
    domain: tuple[str, ...] = ()
    redaction_token: str = "redacted"


@dataclass(frozen=True)
class ProjectionPolicy:
    schema_type: str = field(default="projection_policy", init=False)
    schema_version: int = 1
    policy_id: str = ""
    policy_version: str = ""
    event_metadata_visibility: str = "revealed"
    target: ChannelProjection = field(default_factory=ChannelProjection)
    payload: ChannelProjection = field(default_factory=ChannelProjection)


@dataclass(frozen=True, order=True)
class ClaimRef:
    node_type: str = field(default="claim_ref", init=False, compare=False)
    claim_type: str = ""
    digest: str = ""


@dataclass(frozen=True)
class MonitorCase:
    node_type: str = field(default="monitor_case", init=False)
    observation_signature: tuple[str, ...] = ()
    result: bool = False


@dataclass(frozen=True)
class CompiledMonitor:
    node_type: str = field(default="compiled_monitor", init=False)
    claim: ClaimRef = field(default_factory=ClaimRef)
    refs: tuple[FieldRef, ...] = ()
    cases: tuple[MonitorCase, ...] = ()


@dataclass(frozen=True)
class HiddenValue:
    node_type: str = field(default="hidden_value", init=False)
    probe_id: str = ""
    channel: Channel = "target"
    value: str = ""


@dataclass(frozen=True)
class MappingEntry:
    node_type: str = field(default="mapping_entry", init=False)
    source: str = ""
    observed: str = ""


@dataclass(frozen=True)
class ProjectionMap:
    node_type: str = field(default="projection_map", init=False)
    channel: Channel = "target"
    scope: str = "global"
    probe_id: str = "*"
    entries: tuple[MappingEntry, ...] = ()


@dataclass(frozen=True)
class HiddenWorld:
    node_type: str = field(default="hidden_world", init=False)
    values: tuple[HiddenValue, ...] = ()
    projection_maps: tuple[ProjectionMap, ...] = ()


@dataclass(frozen=True)
class NonIdentifiabilityWitness:
    node_type: str = field(default="nonidentifiability_witness", init=False)
    claim: ClaimRef = field(default_factory=ClaimRef)
    refs: tuple[FieldRef, ...] = ()
    world_true: HiddenWorld = field(default_factory=HiddenWorld)
    world_false: HiddenWorld = field(default_factory=HiddenWorld)
    shared_observation: tuple[str, ...] = ()


@dataclass(frozen=True)
class CompiledPlan:
    schema_type: str = field(default="compiled_plan", init=False)
    schema_version: int = 1
    contract_hash: str = ""
    projection_hash: str = ""
    probes: tuple[ProbeSpec, ...] = ()
    contract_claims: tuple[ClaimRef, ...] = ()
    identifiable_claims: tuple[ClaimRef, ...] = ()
    monitors: tuple[CompiledMonitor, ...] = ()
    nonidentifiable: tuple[NonIdentifiabilityWitness, ...] = ()
    plan_hash: str = ""


@dataclass(frozen=True, order=True)
class ObservedEvent:
    node_type: str = field(default="observed_event", init=False, compare=False)
    kind: str = ""
    target_token: str = ""
    payload_token: str = ""


@dataclass(frozen=True)
class ProbeObservation:
    node_type: str = field(default="probe_observation", init=False)
    probe_id: str = ""
    events: tuple[ObservedEvent, ...] = ()


@dataclass(frozen=True)
class ExecutionReport:
    schema_type: str = field(default="execution_report", init=False)
    schema_version: int = 1
    complete: bool = False
    passed_claims: tuple[ClaimRef, ...] = ()
    failed_claims: tuple[ClaimRef, ...] = ()
    nonidentifiable_claims: tuple[ClaimRef, ...] = ()
    observation_hash: str = ""
    observed_probe_ids: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    report_hash: str = ""


@dataclass(frozen=True)
class AttestationRecord:
    schema_type: str = field(default="attestation_record", init=False)
    schema_version: int = 1
    issuer_id: str = ""
    tool_id: str = ""
    tool_version: str = ""
    issued_at: int = 0
    expires_at: int = 0
    nonce: str = ""
    contract_hash: str = ""
    projection_hash: str = ""
    plan_hash: str = ""
    observation_hash: str = ""
    report_hash: str = ""
    contract_claims: tuple[ClaimRef, ...] = ()
    passed_claims: tuple[ClaimRef, ...] = ()
    failed_claims: tuple[ClaimRef, ...] = ()
    nonidentifiable_claims: tuple[ClaimRef, ...] = ()
    status: str = ""
    signature_algorithm: str = "hmac-sha256"
    signature: str = ""


@dataclass(frozen=True)
class AdmissionRequest:
    schema_type: str = field(default="admission_request", init=False)
    schema_version: int = 1
    tool_id: str = ""
    tool_version: str = ""
    contract_hash: str = ""
    projection_hash: str = ""
    plan_hash: str = ""
    required_claims: tuple[ClaimRef, ...] = ()


@dataclass(frozen=True)
class AdmissionDecision:
    allowed: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceBundle:
    contract: EffectContract
    projection: ProjectionPolicy
    plan: CompiledPlan
    observations: tuple[ProbeObservation, ...]
    report: ExecutionReport


@dataclass(frozen=True)
class AdmissionBundle(EvidenceBundle):
    record: AttestationRecord


def without_plan_hash(plan: CompiledPlan) -> CompiledPlan:
    return replace(plan, plan_hash="")


def without_report_hash(report: ExecutionReport) -> ExecutionReport:
    return replace(report, report_hash="")


def without_signature(record: AttestationRecord) -> AttestationRecord:
    return replace(record, signature="")


def encode(value: object) -> bytes:
    return canonical_bytes(value)


def _parse_probe(value: Any, *, where: str) -> ProbeSpec:
    data = _mapping(value, where=where)
    _strict_keys(data, {"node_type", "probe_id", "factors"}, where=where)
    if data["node_type"] != "probe":
        raise SchemaError(f"{where}.node_type 非法")
    factors = []
    for index, raw in enumerate(_list(data["factors"], where=f"{where}.factors")):
        pair = _list(raw, where=f"{where}.factors[{index}]")
        if len(pair) != 2:
            raise SchemaError(f"{where}.factors[{index}] 必须有两个元素")
        factors.append(
            (_text(pair[0], where=f"{where}.factor.key"), str(pair[1]))
        )
    return ProbeSpec(
        probe_id=_text(data["probe_id"], where=f"{where}.probe_id"),
        factors=tuple(factors),
    )


def _parse_operand(value: Any, *, where: str) -> Operand:
    data = _mapping(value, where=where)
    node_type = data.get("node_type")
    if node_type == "field_ref":
        _strict_keys(data, {"node_type", "probe_id", "channel"}, where=where)
        channel = data["channel"]
        if channel not in {"target", "payload"}:
            raise SchemaError(f"{where}.channel 非法")
        return FieldRef(
            probe_id=_text(data["probe_id"], where=f"{where}.probe_id"),
            channel=channel,
        )
    if node_type == "literal":
        _strict_keys(data, {"node_type", "value"}, where=where)
        return LiteralValue(value=str(data["value"]))
    raise SchemaError(f"{where}.node_type 非法")


def _parse_formula(value: Any, *, where: str) -> Formula:
    data = _mapping(value, where=where)
    node_type = data.get("node_type")
    if node_type == "compare":
        _strict_keys(
            data,
            {"node_type", "operator", "left", "right"},
            where=where,
        )
        operator = data["operator"]
        if operator not in {"eq", "ne"}:
            raise SchemaError(f"{where}.operator 非法")
        return CompareExpr(
            operator=operator,
            left=_parse_operand(data["left"], where=f"{where}.left"),
            right=_parse_operand(data["right"], where=f"{where}.right"),
        )
    if node_type == "boolean":
        _strict_keys(data, {"node_type", "operator", "children"}, where=where)
        operator = data["operator"]
        if operator not in {"and", "or", "not"}:
            raise SchemaError(f"{where}.operator 非法")
        children = tuple(
            _parse_formula(item, where=f"{where}.children[{index}]")
            for index, item in enumerate(
                _list(data["children"], where=f"{where}.children")
            )
        )
        return BooleanExpr(operator=operator, children=children)
    raise SchemaError(f"{where}.node_type 非法")


def _parse_relation_claim(value: Any, *, where: str) -> RelationClaim:
    data = _mapping(value, where=where)
    _strict_keys(
        data,
        {"node_type", "display_name", "probes", "formula"},
        where=where,
    )
    if data["node_type"] != "relation_claim":
        raise SchemaError(f"{where}.node_type 非法")
    return RelationClaim(
        display_name=_text(data["display_name"], where=f"{where}.display_name"),
        probes=tuple(
            _parse_probe(item, where=f"{where}.probes[{index}]")
            for index, item in enumerate(
                _list(data["probes"], where=f"{where}.probes")
            )
        ),
        formula=_parse_formula(data["formula"], where=f"{where}.formula"),
    )


def decode_contract(payload: bytes) -> EffectContract:
    try:
        root = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SchemaError("合同不是规范 UTF-8 JSON") from error
    data = _mapping(root, where="contract")
    _strict_keys(
        data,
        {
            "schema_type",
            "schema_version",
            "contract_id",
            "contract_version",
            "primary_kind",
            "count_policy",
            "allowed_auxiliary_kinds",
            "structural_probe",
            "relation_claims",
        },
        where="contract",
    )
    if data["schema_type"] != "effect_contract":
        raise SchemaError("contract.schema_type 非法")
    count = _mapping(data["count_policy"], where="contract.count_policy")
    _strict_keys(
        count,
        {"node_type", "minimum", "maximum"},
        where="contract.count_policy",
    )
    if count["node_type"] != "count_policy":
        raise SchemaError("contract.count_policy.node_type 非法")
    contract = EffectContract(
        schema_version=_integer(data["schema_version"], where="schema_version"),
        contract_id=_text(data["contract_id"], where="contract_id"),
        contract_version=_text(data["contract_version"], where="contract_version"),
        primary_kind=_text(data["primary_kind"], where="primary_kind"),
        count_policy=CountPolicy(
            minimum=_integer(count["minimum"], where="count.minimum"),
            maximum=_integer(count["maximum"], where="count.maximum"),
        ),
        allowed_auxiliary_kinds=tuple(
            _text(item, where="allowed_auxiliary_kinds[]")
            for item in _list(
                data["allowed_auxiliary_kinds"],
                where="allowed_auxiliary_kinds",
            )
        ),
        structural_probe=_parse_probe(
            data["structural_probe"], where="contract.structural_probe"
        ),
        relation_claims=tuple(
            _parse_relation_claim(item, where=f"relation_claims[{index}]")
            for index, item in enumerate(
                _list(data["relation_claims"], where="relation_claims")
            )
        ),
    )
    if encode(contract) != payload:
        raise SchemaError("合同 JSON 不是唯一规范编码")
    return contract


def _parse_channel_projection(value: Any, *, where: str) -> ChannelProjection:
    data = _mapping(value, where=where)
    _strict_keys(
        data,
        {"node_type", "kind", "domain", "redaction_token"},
        where=where,
    )
    if data["node_type"] != "channel_projection":
        raise SchemaError(f"{where}.node_type 非法")
    kind = data["kind"]
    if kind not in {
        "identity",
        "global_bijection",
        "probe_local_bijection",
        "constant_redaction",
    }:
        raise SchemaError(f"{where}.kind 非法")
    return ChannelProjection(
        kind=kind,
        domain=tuple(
            _text(item, where=f"{where}.domain[]")
            for item in _list(data["domain"], where=f"{where}.domain")
        ),
        redaction_token=_text(
            data["redaction_token"], where=f"{where}.redaction_token"
        ),
    )


def decode_projection(payload: bytes) -> ProjectionPolicy:
    try:
        root = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SchemaError("投影不是规范 UTF-8 JSON") from error
    data = _mapping(root, where="projection")
    _strict_keys(
        data,
        {
            "schema_type",
            "schema_version",
            "policy_id",
            "policy_version",
            "event_metadata_visibility",
            "target",
            "payload",
        },
        where="projection",
    )
    if data["schema_type"] != "projection_policy":
        raise SchemaError("projection.schema_type 非法")
    projection = ProjectionPolicy(
        schema_version=_integer(data["schema_version"], where="schema_version"),
        policy_id=_text(data["policy_id"], where="policy_id"),
        policy_version=_text(data["policy_version"], where="policy_version"),
        event_metadata_visibility=_text(
            data["event_metadata_visibility"],
            where="event_metadata_visibility",
        ),
        target=_parse_channel_projection(data["target"], where="target"),
        payload=_parse_channel_projection(data["payload"], where="payload"),
    )
    if encode(projection) != payload:
        raise SchemaError("投影 JSON 不是唯一规范编码")
    return projection


T = TypeVar("T")


def canonical_roundtrip(value: T, decoder) -> T:
    return decoder(encode(value))
