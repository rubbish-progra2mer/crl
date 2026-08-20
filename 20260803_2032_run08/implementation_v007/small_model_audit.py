#!/usr/bin/env python3
"""不调用候选求值器的有限模型语义预言机审计。"""

from __future__ import annotations

import itertools
import json
from collections import defaultdict

from compiler import compile_contract
from typed_model import (
    BooleanExpr,
    ChannelProjection,
    CompareExpr,
    EffectContract,
    FieldRef,
    LiteralValue,
    ProbeSpec,
    ProjectionPolicy,
    RelationClaim,
)


KINDS = (
    "identity",
    "global_bijection",
    "probe_local_bijection",
    "constant_redaction",
)


def _refs(formula):
    found = set()

    def walk(node):
        if isinstance(node, CompareExpr):
            if isinstance(node.left, FieldRef):
                found.add((node.left.probe_id, node.left.channel))
            if isinstance(node.right, FieldRef):
                found.add((node.right.probe_id, node.right.channel))
        else:
            for child in node.children:
                walk(child)

    walk(formula)
    return tuple(sorted(found))


def _truth(formula, hidden):
    if isinstance(formula, CompareExpr):
        left = (
            hidden[(formula.left.probe_id, formula.left.channel)]
            if isinstance(formula.left, FieldRef)
            else formula.left.value
        )
        right = (
            hidden[(formula.right.probe_id, formula.right.channel)]
            if isinstance(formula.right, FieldRef)
            else formula.right.value
        )
        return left == right if formula.operator == "eq" else left != right
    values = [_truth(child, hidden) for child in formula.children]
    if formula.operator == "and":
        return all(values)
    if formula.operator == "or":
        return any(values)
    return not values[0]


def _map_options(kind, domain, channel, probe_ids):
    if kind == "identity":
        return ({(channel, "*", value): value for value in domain},)
    if kind == "constant_redaction":
        return ({(channel, "*", value): f"R-{channel}" for value in domain},)
    permutations = tuple(itertools.permutations(domain))
    maps = tuple(dict(zip(domain, permutation)) for permutation in permutations)
    if kind == "global_bijection":
        return tuple(
            {(channel, "*", source): observed for source, observed in mapping.items()}
            for mapping in maps
        )
    result = []
    for selection in itertools.product(maps, repeat=len(probe_ids)):
        combined = {}
        for probe_id, mapping in zip(probe_ids, selection):
            combined.update(
                {
                    (channel, probe_id, source): observed
                    for source, observed in mapping.items()
                }
            )
        result.append(combined)
    return tuple(result)


def _observe(refs, hidden, mapping):
    result = []
    for probe_id, channel in refs:
        value = hidden[(probe_id, channel)]
        global_key = (channel, "*", value)
        local_key = (channel, probe_id, value)
        result.append(mapping[global_key] if global_key in mapping else mapping[local_key])
    return tuple(result)


def _oracle(formula, target_kind, payload_kind, domain):
    refs = _refs(formula)
    by_channel = {
        channel: tuple(sorted({probe for probe, item_channel in refs if item_channel == channel}))
        for channel in ("target", "payload")
    }
    options = []
    for channel, kind in (("target", target_kind), ("payload", payload_kind)):
        if by_channel[channel]:
            options.append(_map_options(kind, domain, channel, by_channel[channel]))
    groups = defaultdict(set)
    bindings = 0
    for values in itertools.product(domain, repeat=len(refs)):
        hidden = dict(zip(refs, values))
        truth = _truth(formula, hidden)
        for selected in itertools.product(*options):
            mapping = {}
            for item in selected:
                mapping.update(item)
            groups[_observe(refs, hidden, mapping)].add(truth)
            bindings += 1
    identifiable = all(len(results) == 1 for results in groups.values())
    table = {
        observation: next(iter(results))
        for observation, results in groups.items()
        if len(results) == 1
    }
    return identifiable, table, len(groups), bindings


def _formulas():
    t1 = FieldRef(probe_id="p1", channel="target")
    t2 = FieldRef(probe_id="p2", channel="target")
    d1 = FieldRef(probe_id="p1", channel="payload")
    d2 = FieldRef(probe_id="p2", channel="payload")
    eq_target = CompareExpr(operator="eq", left=t1, right=t2)
    eq_payload = CompareExpr(operator="eq", left=d1, right=d2)
    return (
        ("target_eq", eq_target),
        ("target_ne", CompareExpr(operator="ne", left=t1, right=t2)),
        ("target_literal", CompareExpr(operator="eq", left=t1, right=LiteralValue("0"))),
        ("cross_channel", CompareExpr(operator="eq", left=t1, right=d1)),
        (
            "both_equal",
            BooleanExpr(operator="and", children=(eq_target, eq_payload)),
        ),
        (
            "either_equal",
            BooleanExpr(operator="or", children=(eq_target, eq_payload)),
        ),
        (
            "not_target_equal",
            BooleanExpr(operator="not", children=(eq_target,)),
        ),
    )


def _contract(formula):
    probes = (
        ProbeSpec(probe_id="p1", factors=(("case", "one"),)),
        ProbeSpec(probe_id="p2", factors=(("case", "two"),)),
    )
    return EffectContract(
        contract_id="small-model",
        contract_version="7",
        primary_kind="write",
        relation_claims=(
            RelationClaim(
                display_name="catalogue claim",
                probes=probes,
                formula=formula,
            ),
        ),
    )


def _projection(target_kind, payload_kind, domain):
    return ProjectionPolicy(
        policy_id="small-model-projection",
        policy_version="7",
        target=ChannelProjection(
            kind=target_kind,
            domain=domain,
            redaction_token="R-target",
        ),
        payload=ChannelProjection(
            kind=payload_kind,
            domain=domain,
            redaction_token="R-payload",
        ),
    )


def main() -> int:
    rows = []
    discrepancies = []
    stability = {}
    total_bindings = 0
    total_classes = 0
    for domain_size in (2, 3):
        domain = tuple(str(index) for index in range(domain_size))
        for formula_name, formula in _formulas():
            for target_kind, payload_kind in itertools.product(KINDS, repeat=2):
                oracle_identifiable, oracle_table, classes, bindings = _oracle(
                    formula, target_kind, payload_kind, domain
                )
                plan = compile_contract(
                    _contract(formula),
                    _projection(target_kind, payload_kind, domain),
                )
                candidate_identifiable = len(plan.monitors) == 1
                candidate_table = (
                    {
                        case.observation_signature: case.result
                        for case in plan.monitors[0].cases
                    }
                    if candidate_identifiable
                    else {}
                )
                if candidate_identifiable != oracle_identifiable or (
                    oracle_identifiable and candidate_table != oracle_table
                ):
                    discrepancies.append(
                        [domain_size, formula_name, target_kind, payload_kind]
                    )
                key = (formula_name, target_kind, payload_kind)
                stability.setdefault(key, []).append(oracle_identifiable)
                rows.append(
                    {
                        "domain_size": domain_size,
                        "formula": formula_name,
                        "target_projection": target_kind,
                        "payload_projection": payload_kind,
                        "identifiable": oracle_identifiable,
                        "observation_classes": classes,
                        "bindings_examined": bindings,
                    }
                )
                total_bindings += bindings
                total_classes += classes
    unstable = [list(key) for key, values in stability.items() if len(set(values)) != 1]
    summary = {
        "schema": "v007-small-model-audit-1",
        "formula_count": len(_formulas()),
        "projection_pairs": len(KINDS) ** 2,
        "domain_sizes": [2, 3],
        "enumerated_configurations": len(rows),
        "hidden_projection_bindings_examined": total_bindings,
        "observation_classes_examined": total_classes,
        "candidate_oracle_disagreements": len(discrepancies),
        "disagreement_examples": discrepancies[:10],
        "domain_2_to_3_identifiability_changes": len(unstable),
        "unstable_examples": unstable[:10],
        "identifiable_configurations": sum(row["identifiable"] for row in rows),
        "nonidentifiable_configurations": sum(not row["identifiable"] for row in rows),
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if not discrepancies else 1


if __name__ == "__main__":
    raise SystemExit(main())
