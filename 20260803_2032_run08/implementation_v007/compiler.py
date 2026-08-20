#!/usr/bin/env python3
"""投影策略族上的有限语义闭包分析与监控计划合成。"""

from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import asdict, replace
from typing import Iterable, Mapping

from typed_model import (
    BooleanExpr,
    Channel,
    ChannelProjection,
    ClaimRef,
    CompareExpr,
    CompiledMonitor,
    CompiledPlan,
    EffectContract,
    FieldRef,
    Formula,
    HiddenValue,
    HiddenWorld,
    IntegrityError,
    LiteralValue,
    MappingEntry,
    MonitorCase,
    NonIdentifiabilityWitness,
    ProbeSpec,
    ProjectionMap,
    ProjectionPolicy,
    RelationClaim,
    SchemaError,
    canonical_hash,
    decode_contract,
    decode_projection,
    encode,
    without_plan_hash,
)


MAX_SEMANTIC_STATES = 200_000


def _unique_sorted_text(values: Iterable[str], *, where: str) -> tuple[str, ...]:
    result = tuple(sorted(values))
    if any(not item for item in result):
        raise SchemaError(f"{where} 不能含空字符串")
    if len(set(result)) != len(result):
        raise SchemaError(f"{where} 不能重复")
    return result


def _validate_probe(probe: ProbeSpec) -> None:
    if not probe.probe_id:
        raise SchemaError("probe_id 不能为空")
    keys = [key for key, _ in probe.factors]
    if keys != sorted(keys) or len(set(keys)) != len(keys):
        raise SchemaError(f"探针 {probe.probe_id} 的因素必须唯一且排序")
    if any(not key for key in keys):
        raise SchemaError(f"探针 {probe.probe_id} 的因素名不能为空")


def formula_refs(formula: Formula) -> tuple[FieldRef, ...]:
    refs: set[FieldRef] = set()

    def visit(node: Formula) -> None:
        if isinstance(node, CompareExpr):
            for operand in (node.left, node.right):
                if isinstance(operand, FieldRef):
                    refs.add(operand)
            return
        if isinstance(node, BooleanExpr):
            for child in node.children:
                visit(child)
            return
        raise SchemaError("未知公式节点")

    visit(formula)
    return tuple(sorted(refs, key=lambda item: (item.probe_id, item.channel)))


def _validate_formula(formula: Formula) -> None:
    if isinstance(formula, CompareExpr):
        if formula.operator not in {"eq", "ne"}:
            raise SchemaError("比较运算符非法")
        if isinstance(formula.left, LiteralValue) and isinstance(
            formula.right, LiteralValue
        ):
            raise SchemaError("关系公式不能只比较两个常量")
        return
    if not isinstance(formula, BooleanExpr):
        raise SchemaError("未知公式节点")
    if formula.operator == "not":
        if len(formula.children) != 1:
            raise SchemaError("not 必须恰有一个子公式")
    elif formula.operator in {"and", "or"}:
        if len(formula.children) < 2:
            raise SchemaError(f"{formula.operator} 必须至少有两个子公式")
    else:
        raise SchemaError("布尔运算符非法")
    for child in formula.children:
        _validate_formula(child)


def _validate_formula_domains(
    formula: Formula, projection: ProjectionPolicy
) -> None:
    """要求每个常量都能在其比较字段的声明域中解释。"""

    if isinstance(formula, BooleanExpr):
        for child in formula.children:
            _validate_formula_domains(child, projection)
        return
    operands = (formula.left, formula.right)
    refs = tuple(item for item in operands if isinstance(item, FieldRef))
    literals = tuple(item for item in operands if isinstance(item, LiteralValue))
    if not literals:
        return
    if len(refs) != 1:
        raise SchemaError("含常量的比较必须恰好引用一个字段")
    policy = projection.target if refs[0].channel == "target" else projection.payload
    for literal in literals:
        if literal.value not in policy.domain:
            raise SchemaError(
                f"常量 {literal.value!r} 不在 {refs[0].channel} 投影域内"
            )


def _validate_channel_projection(policy: ChannelProjection, *, where: str) -> None:
    if policy.kind not in {
        "identity",
        "global_bijection",
        "probe_local_bijection",
        "constant_redaction",
    }:
        raise SchemaError(f"{where}.kind 非法")
    if len(policy.domain) < 2:
        raise SchemaError(f"{where}.domain 至少需要两个值")
    if tuple(sorted(policy.domain)) != policy.domain:
        raise SchemaError(f"{where}.domain 必须排序")
    _unique_sorted_text(policy.domain, where=f"{where}.domain")
    if not policy.redaction_token:
        raise SchemaError(f"{where}.redaction_token 不能为空")


def validate_inputs(contract: EffectContract, projection: ProjectionPolicy) -> None:
    if decode_contract(encode(contract)) != contract:
        raise SchemaError("合同未通过严格规范模式往返")
    if decode_projection(encode(projection)) != projection:
        raise SchemaError("投影未通过严格规范模式往返")
    if contract.schema_version != 1 or projection.schema_version != 1:
        raise SchemaError("只支持模式版本 1")
    for name, value in (
        ("contract_id", contract.contract_id),
        ("contract_version", contract.contract_version),
        ("primary_kind", contract.primary_kind),
        ("policy_id", projection.policy_id),
        ("policy_version", projection.policy_version),
    ):
        if not value:
            raise SchemaError(f"{name} 不能为空")
    if projection.event_metadata_visibility != "revealed":
        raise SchemaError("当前结构义务要求事件类型和数量明文可见")
    if contract.count_policy.minimum < 0:
        raise SchemaError("最小主事件数量不能为负")
    if contract.count_policy.maximum < contract.count_policy.minimum:
        raise SchemaError("主事件数量区间非法")
    allowed = _unique_sorted_text(
        contract.allowed_auxiliary_kinds,
        where="allowed_auxiliary_kinds",
    )
    if allowed != contract.allowed_auxiliary_kinds:
        raise SchemaError("allowed_auxiliary_kinds 必须排序")
    if contract.primary_kind in allowed:
        raise SchemaError("主事件类型不能同时成为辅助类型")
    _validate_probe(contract.structural_probe)
    _validate_channel_projection(projection.target, where="target")
    _validate_channel_projection(projection.payload, where="payload")

    names: set[str] = set()
    semantic_digests: set[str] = set()
    probe_catalog: dict[str, ProbeSpec] = {}
    for claim in contract.relation_claims:
        if not claim.display_name or claim.display_name in names:
            raise SchemaError("关系主张显示名必须非空且唯一")
        names.add(claim.display_name)
        if contract.count_policy.minimum != 1 or contract.count_policy.maximum != 1:
            raise SchemaError("含字段关系的合同当前要求每探针恰一个主事件")
        _validate_formula(claim.formula)
        _validate_formula_domains(claim.formula, projection)
        if not claim.probes:
            raise SchemaError("关系主张必须声明探针")
        for probe in claim.probes:
            _validate_probe(probe)
            previous = probe_catalog.get(probe.probe_id)
            if previous is not None and previous != probe:
                raise SchemaError(f"探针标识冲突：{probe.probe_id}")
            probe_catalog[probe.probe_id] = probe
        refs = formula_refs(claim.formula)
        if not refs:
            raise SchemaError("关系公式必须引用至少一个观察字段")
        declared = {probe.probe_id for probe in claim.probes}
        missing = {ref.probe_id for ref in refs} - declared
        if missing:
            raise SchemaError(f"关系公式引用未声明探针：{sorted(missing)}")
        digest = relation_claim_ref(claim).digest
        if digest in semantic_digests:
            raise SchemaError("不允许语义重复的关系主张")
        semantic_digests.add(digest)


def count_claim_ref(contract: EffectContract) -> ClaimRef:
    payload = {
        "claim_type": "event_count_interval",
        "primary_kind": contract.primary_kind,
        "minimum": contract.count_policy.minimum,
        "maximum": contract.count_policy.maximum,
    }
    return ClaimRef("event_count_interval", canonical_hash(payload))


def auxiliary_claim_ref(contract: EffectContract) -> ClaimRef:
    payload = {
        "claim_type": "allowed_auxiliary_kinds",
        "primary_kind": contract.primary_kind,
        "allowed": list(contract.allowed_auxiliary_kinds),
    }
    return ClaimRef("allowed_auxiliary_kinds", canonical_hash(payload))


def relation_claim_ref(claim: RelationClaim) -> ClaimRef:
    payload = asdict(replace(claim, display_name=""))
    return ClaimRef("finite_relation", canonical_hash(payload))


def contract_claim_refs(contract: EffectContract) -> tuple[ClaimRef, ...]:
    claims = [count_claim_ref(contract), auxiliary_claim_ref(contract)]
    claims.extend(relation_claim_ref(claim) for claim in contract.relation_claims)
    return tuple(sorted(claims))


def _formula_value(
    operand: FieldRef | LiteralValue,
    values: Mapping[tuple[str, Channel], str],
) -> str:
    if isinstance(operand, LiteralValue):
        return operand.value
    return values[(operand.probe_id, operand.channel)]


def evaluate_formula(
    formula: Formula,
    values: Mapping[tuple[str, Channel], str],
) -> bool:
    if isinstance(formula, CompareExpr):
        left = _formula_value(formula.left, values)
        right = _formula_value(formula.right, values)
        return left == right if formula.operator == "eq" else left != right
    results = tuple(evaluate_formula(child, values) for child in formula.children)
    if formula.operator == "and":
        return all(results)
    if formula.operator == "or":
        return any(results)
    if formula.operator == "not":
        return not results[0]
    raise SchemaError("未知公式运算符")


def _projection_maps(
    channel: Channel,
    policy: ChannelProjection,
    probe_ids: tuple[str, ...],
) -> tuple[tuple[ProjectionMap, ...], ...]:
    domain = policy.domain
    if policy.kind == "identity":
        entries = tuple(MappingEntry(value, value) for value in domain)
        return ((ProjectionMap(channel, "global", "*", entries),),)
    if policy.kind == "constant_redaction":
        entries = tuple(
            MappingEntry(value, policy.redaction_token) for value in domain
        )
        return ((ProjectionMap(channel, "global", "*", entries),),)
    permutations = tuple(itertools.permutations(domain))
    maps = tuple(
        tuple(MappingEntry(source, observed) for source, observed in zip(domain, perm))
        for perm in permutations
    )
    if policy.kind == "global_bijection":
        return tuple(
            (ProjectionMap(channel, "global", "*", entries),)
            for entries in maps
        )
    combinations = itertools.product(maps, repeat=len(probe_ids))
    return tuple(
        tuple(
            ProjectionMap(channel, "probe_local", probe_id, entries)
            for probe_id, entries in zip(probe_ids, selected)
        )
        for selected in combinations
    )


def _world_map(
    refs: tuple[FieldRef, ...], values: tuple[str, ...]
) -> dict[tuple[str, Channel], str]:
    return {
        (ref.probe_id, ref.channel): value
        for ref, value in zip(refs, values)
    }


def _observe_world(
    refs: tuple[FieldRef, ...],
    values: Mapping[tuple[str, Channel], str],
    projection_maps: tuple[ProjectionMap, ...],
) -> tuple[str, ...]:
    lookup: dict[tuple[Channel, str, str], str] = {}
    for projection_map in projection_maps:
        for entry in projection_map.entries:
            lookup[
                (projection_map.channel, projection_map.probe_id, entry.source)
            ] = entry.observed
    observed: list[str] = []
    for ref in refs:
        hidden = values[(ref.probe_id, ref.channel)]
        key_local = (ref.channel, ref.probe_id, hidden)
        key_global = (ref.channel, "*", hidden)
        if key_local in lookup:
            observed.append(lookup[key_local])
        elif key_global in lookup:
            observed.append(lookup[key_global])
        else:
            raise IntegrityError("投影映射不完整")
    return tuple(observed)


def _hidden_world(
    refs: tuple[FieldRef, ...],
    values: tuple[str, ...],
    maps: tuple[ProjectionMap, ...],
) -> HiddenWorld:
    return HiddenWorld(
        values=tuple(
            HiddenValue(ref.probe_id, ref.channel, value)
            for ref, value in zip(refs, values)
        ),
        projection_maps=tuple(
            sorted(maps, key=lambda item: (item.channel, item.scope, item.probe_id))
        ),
    )


def _compile_relation(
    claim: RelationClaim,
    projection: ProjectionPolicy,
) -> CompiledMonitor | NonIdentifiabilityWitness:
    claim_ref = relation_claim_ref(claim)
    refs = formula_refs(claim.formula)
    domains = tuple(
        projection.target.domain if ref.channel == "target" else projection.payload.domain
        for ref in refs
    )
    channel_maps: list[tuple[tuple[ProjectionMap, ...], ...]] = []
    for channel in ("target", "payload"):
        probes = tuple(sorted({ref.probe_id for ref in refs if ref.channel == channel}))
        if not probes:
            continue
        policy = projection.target if channel == "target" else projection.payload
        channel_maps.append(_projection_maps(channel, policy, probes))
    mapping_count = 1
    for possibilities in channel_maps:
        mapping_count *= len(possibilities)
    hidden_count = 1
    for domain in domains:
        hidden_count *= len(domain)
    if hidden_count * mapping_count > MAX_SEMANTIC_STATES:
        raise SchemaError(
            "有限语义状态空间超过上限；请缩小域或拆分关系主张"
        )

    groups: dict[
        tuple[str, ...],
        dict[bool, tuple[tuple[str, ...], tuple[ProjectionMap, ...]]],
    ] = defaultdict(dict)
    mapping_products = itertools.product(*channel_maps) if channel_maps else [()]
    all_mappings = tuple(
        tuple(item for group in selected for item in group)
        for selected in mapping_products
    )
    for hidden_values in itertools.product(*domains):
        values = tuple(str(item) for item in hidden_values)
        world_values = _world_map(refs, values)
        truth = evaluate_formula(claim.formula, world_values)
        for maps in all_mappings:
            observation = _observe_world(refs, world_values, maps)
            groups[observation].setdefault(truth, (values, maps))

    for observation in sorted(groups):
        alternatives = groups[observation]
        if True in alternatives and False in alternatives:
            true_values, true_maps = alternatives[True]
            false_values, false_maps = alternatives[False]
            return NonIdentifiabilityWitness(
                claim=claim_ref,
                refs=refs,
                world_true=_hidden_world(refs, true_values, true_maps),
                world_false=_hidden_world(refs, false_values, false_maps),
                shared_observation=observation,
            )
    cases = tuple(
        MonitorCase(observation, next(iter(groups[observation])))
        for observation in sorted(groups)
    )
    return CompiledMonitor(claim=claim_ref, refs=refs, cases=cases)


def compile_contract(
    contract: EffectContract,
    projection: ProjectionPolicy,
) -> CompiledPlan:
    validate_inputs(contract, projection)
    probes: dict[str, ProbeSpec] = {}
    monitors: list[CompiledMonitor] = []
    nonidentifiable: list[NonIdentifiabilityWitness] = []
    for claim in contract.relation_claims:
        for probe in claim.probes:
            previous = probes.get(probe.probe_id)
            if previous is not None and previous != probe:
                raise SchemaError(f"探针标识冲突：{probe.probe_id}")
            probes[probe.probe_id] = probe
        compiled = _compile_relation(claim, projection)
        if isinstance(compiled, CompiledMonitor):
            monitors.append(compiled)
        else:
            nonidentifiable.append(compiled)
    if not probes:
        probes[contract.structural_probe.probe_id] = contract.structural_probe

    contract_claims = contract_claim_refs(contract)
    structural = (count_claim_ref(contract), auxiliary_claim_ref(contract))
    identifiable = tuple(
        sorted(structural + tuple(monitor.claim for monitor in monitors))
    )
    plan = CompiledPlan(
        contract_hash=canonical_hash(contract),
        projection_hash=canonical_hash(projection),
        probes=tuple(probes[key] for key in sorted(probes)),
        contract_claims=contract_claims,
        identifiable_claims=identifiable,
        monitors=tuple(sorted(monitors, key=lambda item: item.claim)),
        nonidentifiable=tuple(
            sorted(nonidentifiable, key=lambda item: item.claim)
        ),
        plan_hash="",
    )
    plan = replace(plan, plan_hash=canonical_hash(without_plan_hash(plan)))
    validate_claim_partition(plan)
    return plan


def validate_claim_partition(plan: CompiledPlan) -> None:
    """检查计划对合同主张的两分是否完备、互斥且无重复。"""

    contract_claims = tuple(plan.contract_claims)
    identifiable = tuple(plan.identifiable_claims)
    nonidentifiable = tuple(item.claim for item in plan.nonidentifiable)
    for label, claims in (
        ("合同", contract_claims),
        ("可识别", identifiable),
        ("不可识别", nonidentifiable),
    ):
        if len(set(claims)) != len(claims):
            raise IntegrityError(f"{label}主张集合含重复项")
        if claims != tuple(sorted(claims)):
            raise IntegrityError(f"{label}主张集合未规范排序")
    contract_set = set(contract_claims)
    identifiable_set = set(identifiable)
    nonidentifiable_set = set(nonidentifiable)
    if identifiable_set & nonidentifiable_set:
        raise IntegrityError("同一主张不能同时可识别和不可识别")
    if identifiable_set | nonidentifiable_set != contract_set:
        raise IntegrityError("计划对合同主张的两分不完整")
    monitor_claims = tuple(item.claim for item in plan.monitors)
    if len(set(monitor_claims)) != len(monitor_claims):
        raise IntegrityError("监控器主张含重复项")
    if not set(monitor_claims).issubset(identifiable_set):
        raise IntegrityError("监控器绑定了非可识别主张")


def validate_plan(
    plan: CompiledPlan,
    contract: EffectContract,
    projection: ProjectionPolicy,
) -> None:
    if plan.schema_version != 1:
        raise IntegrityError("不支持的计划模式版本")
    validate_claim_partition(plan)
    if canonical_hash(without_plan_hash(plan)) != plan.plan_hash:
        raise IntegrityError("计划散列与实际字段不一致")
    expected = compile_contract(contract, projection)
    if plan != expected:
        raise IntegrityError("计划不是合同与投影的规范重编译结果")


def _world_values(world: HiddenWorld) -> dict[tuple[str, Channel], str]:
    result = {(item.probe_id, item.channel): item.value for item in world.values}
    if len(result) != len(world.values):
        raise IntegrityError("见证隐藏值含重复字段")
    return result


def _validate_projection_maps(
    maps: tuple[ProjectionMap, ...],
    refs: tuple[FieldRef, ...],
    projection: ProjectionPolicy,
) -> None:
    """验证见证使用的映射恰属于投影策略允许的映射族。"""

    for channel in ("target", "payload"):
        probe_ids = tuple(
            sorted({ref.probe_id for ref in refs if ref.channel == channel})
        )
        relevant = tuple(item for item in maps if item.channel == channel)
        if not probe_ids:
            if relevant:
                raise IntegrityError("见证包含未引用通道的投影映射")
            continue
        policy = projection.target if channel == "target" else projection.payload
        allowed = set(_projection_maps(channel, policy, probe_ids))
        if relevant not in allowed:
            raise IntegrityError("见证映射不属于声明的投影策略族")
    if len(maps) != len(
        tuple(item for item in maps if item.channel in {"target", "payload"})
    ):
        raise IntegrityError("见证包含非法通道")


def validate_witness(
    witness: NonIdentifiabilityWitness,
    claim: RelationClaim,
    projection: ProjectionPolicy,
) -> None:
    expected_ref = relation_claim_ref(claim)
    refs = formula_refs(claim.formula)
    if witness.claim != expected_ref or witness.refs != refs:
        raise IntegrityError("见证主张或字段引用不匹配")
    _validate_projection_maps(witness.world_true.projection_maps, refs, projection)
    _validate_projection_maps(witness.world_false.projection_maps, refs, projection)
    true_values = _world_values(witness.world_true)
    false_values = _world_values(witness.world_false)
    expected_keys = {(ref.probe_id, ref.channel) for ref in refs}
    if set(true_values) != expected_keys or set(false_values) != expected_keys:
        raise IntegrityError("见证隐藏值集合不完整")
    for ref in refs:
        domain = (
            projection.target.domain
            if ref.channel == "target"
            else projection.payload.domain
        )
        if true_values[(ref.probe_id, ref.channel)] not in domain:
            raise IntegrityError("真世界值不在投影域内")
        if false_values[(ref.probe_id, ref.channel)] not in domain:
            raise IntegrityError("假世界值不在投影域内")
    true_observation = _observe_world(
        refs, true_values, witness.world_true.projection_maps
    )
    false_observation = _observe_world(
        refs, false_values, witness.world_false.projection_maps
    )
    if true_observation != false_observation:
        raise IntegrityError("见证两世界观察不相同")
    if witness.shared_observation != true_observation:
        raise IntegrityError("见证声明的共享观察与实际推导不一致")
    if not evaluate_formula(claim.formula, true_values):
        raise IntegrityError("真世界不满足主张")
    if evaluate_formula(claim.formula, false_values):
        raise IntegrityError("假世界未否定主张")
