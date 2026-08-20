#!/usr/bin/env python3
"""与候选闭式规则分离的有限隐藏世界语义判定器。

该模块不导入候选编译器。它穷举二元隐藏值、隐藏行为和投影映射，
按观察签名分组，判断同一观察类中主张真值是否恒定。
"""

from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


VALUES = (0, 1)
MAPS = ("identity", "swap")


@dataclass(frozen=True)
class OracleCounterexample:
    claim_id: str
    visibility: str
    shared_observation: tuple[int, int]
    true_outputs: tuple[int, int]
    true_maps: tuple[str, str]
    false_outputs: tuple[int, int]
    false_maps: tuple[str, str]


def _map_value(map_name: str, value: int) -> int:
    if map_name == "identity":
        return value
    if map_name == "swap":
        return 1 - value
    raise ValueError(f"未知映射：{map_name}")


def _mapping_pairs(visibility: str) -> tuple[tuple[str, str], ...]:
    if visibility == "revealed":
        return (("identity", "identity"),)
    if visibility == "stable_anonymous":
        return (("identity", "identity"), ("swap", "swap"))
    if visibility == "clone_local_anonymous":
        return tuple(itertools.product(MAPS, repeat=2))
    raise ValueError(f"未知可见性：{visibility}")


def _truth(claim_id: str, outputs: tuple[int, int]) -> bool:
    if claim_id == "relation.target.responsive":
        return outputs[0] != outputs[1]
    if claim_id == "relation.target.identity":
        return outputs == (0, 1)
    if claim_id.startswith("relation.payload.invariant:"):
        return outputs[0] == outputs[1]
    raise ValueError(f"未知主张：{claim_id}")


def enumerate_observation_classes(
    claim_id: str, visibility: str
) -> dict[tuple[int, int], tuple[tuple[tuple[int, int], tuple[str, str], bool], ...]]:
    classes: dict[
        tuple[int, int],
        list[tuple[tuple[int, int], tuple[str, str], bool]],
    ] = defaultdict(list)
    for outputs in itertools.product(VALUES, repeat=2):
        output_pair = (outputs[0], outputs[1])
        for maps in _mapping_pairs(visibility):
            observation = (
                _map_value(maps[0], output_pair[0]),
                _map_value(maps[1], output_pair[1]),
            )
            classes[observation].append(
                (output_pair, maps, _truth(claim_id, output_pair))
            )
    return {
        observation: tuple(entries)
        for observation, entries in sorted(classes.items())
    }


def oracle_identifiable(claim_id: str, visibility: str) -> bool:
    for entries in enumerate_observation_classes(claim_id, visibility).values():
        if len({entry[2] for entry in entries}) > 1:
            return False
    return True


def oracle_counterexample(
    claim_id: str, visibility: str
) -> OracleCounterexample | None:
    for observation, entries in enumerate_observation_classes(
        claim_id, visibility
    ).items():
        true_entry = next((entry for entry in entries if entry[2]), None)
        false_entry = next((entry for entry in entries if not entry[2]), None)
        if true_entry is not None and false_entry is not None:
            return OracleCounterexample(
                claim_id=claim_id,
                visibility=visibility,
                shared_observation=observation,
                true_outputs=true_entry[0],
                true_maps=true_entry[1],
                false_outputs=false_entry[0],
                false_maps=false_entry[1],
            )
    return None


def expected_identifiability_table() -> dict[str, dict[str, bool]]:
    claims = (
        "relation.target.responsive",
        "relation.target.identity",
        "relation.payload.invariant:ambient_canary",
        "relation.payload.invariant:sensitive_input",
    )
    visibilities = (
        "revealed",
        "stable_anonymous",
        "clone_local_anonymous",
    )
    return {
        claim: {
            visibility: oracle_identifiable(claim, visibility)
            for visibility in visibilities
        }
        for claim in claims
    }


def _parse_hidden_value(value: str, *, channel: str) -> int:
    prefix = "t" if channel == "target" else "p"
    if value == f"{prefix}0":
        return 0
    if value == f"{prefix}1":
        return 1
    raise ValueError(f"非法隐藏值：{value}")


def _validate_map_scope(maps: tuple[str, str], visibility: str) -> bool:
    if visibility == "revealed":
        return maps == ("identity", "identity")
    if visibility == "stable_anonymous":
        return maps[0] == maps[1] and all(item in MAPS for item in maps)
    if visibility == "clone_local_anonymous":
        return all(item in MAPS for item in maps)
    return False


def validate_candidate_witness(
    *,
    claim_id: str,
    visibility: str,
    world_true: dict[str, Iterable[str]],
    world_false: dict[str, Iterable[str]],
) -> dict[str, object]:
    """独立检查候选见证确实是同观察、异真值的一对隐藏世界。"""

    channel = "payload" if claim_id.startswith("relation.payload.") else "target"
    output_key = f"{channel}_outputs"
    map_key = f"{channel}_maps"

    def normalize(world: dict[str, Iterable[str]]) -> tuple[
        tuple[int, int], tuple[str, str], tuple[int, int]
    ]:
        raw_outputs = tuple(world[output_key])
        raw_maps = tuple(world[map_key])
        if len(raw_outputs) != 2 or len(raw_maps) != 2:
            raise ValueError("见证必须包含两个输出和两个映射")
        outputs = (
            _parse_hidden_value(str(raw_outputs[0]), channel=channel),
            _parse_hidden_value(str(raw_outputs[1]), channel=channel),
        )
        maps = (str(raw_maps[0]), str(raw_maps[1]))
        observation = (
            _map_value(maps[0], outputs[0]),
            _map_value(maps[1], outputs[1]),
        )
        return outputs, maps, observation

    true_outputs, true_maps, true_observation = normalize(world_true)
    false_outputs, false_maps, false_observation = normalize(world_false)
    scope_ok = _validate_map_scope(
        true_maps, visibility
    ) and _validate_map_scope(false_maps, visibility)
    true_truth = _truth(claim_id, true_outputs)
    false_truth = _truth(claim_id, false_outputs)
    shared = true_observation == false_observation
    valid = scope_ok and true_truth and not false_truth and shared
    return {
        "valid": valid,
        "scope_ok": scope_ok,
        "true_truth": true_truth,
        "false_truth": false_truth,
        "shared_observation": shared,
        "observation": true_observation if shared else None,
    }
