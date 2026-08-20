#!/usr/bin/env python3
"""在固定 ToolSandbox 外部实现上评价匿名副作用关系协议。

方法只读取编译后的关系计划、固定探针和匿名事件。评价标签来自同一
声明调用在固定上游工具实现中的干净状态差分，不读取故障变体名称。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import uuid
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "vendor"))

from tool_sandbox.common.execution_context import (  # noqa: E402
    DatabaseNamespace,
    ExecutionContext,
    new_context,
)
from tool_sandbox.tools.contact import (  # noqa: E402
    add_contact,
    modify_contact,
)
from tool_sandbox.tools.messaging import (  # noqa: E402
    send_message_with_phone_number,
)
from tool_sandbox.tools.reminder import (  # noqa: E402
    add_reminder,
    modify_reminder,
)


FAMILIES = (
    "contact_add",
    "contact_modify",
    "message_send",
    "reminder_add",
    "reminder_modify",
)

CLEAN_VARIANT = "clean"
COVERED_VARIANTS = (
    "fixed_target",
    "ambient_payload_capture",
    "sensitive_input_extra_effect",
    "neighbor_extra_effect",
    "boundary_extra_effect",
)
BOUNDARY_VARIANTS = (
    "bijective_wrong_target",
    "compound_trigger",
    "sequence_trigger",
)
VARIANTS = (CLEAN_VARIANT, *COVERED_VARIANTS, *BOUNDARY_VARIANTS)


@dataclass(frozen=True)
class ProbeConfig:
    probe_id: str
    target_value: str = "base"
    input_value: str = "public"
    neighbor: bool = False
    ambient_canary: str = "none"
    boundary: bool = False

    def without_target(self) -> tuple[str, bool, str, bool]:
        return (
            self.input_value,
            self.neighbor,
            self.ambient_canary,
            self.boundary,
        )

    def without_ambient_canary(self) -> tuple[str, str, bool, bool]:
        return (
            self.target_value,
            self.input_value,
            self.neighbor,
            self.boundary,
        )


@dataclass(frozen=True, order=True)
class RawEvent:
    kind: str
    target: str
    payload: str


@dataclass(frozen=True, order=True)
class AnonymousEvent:
    kind: str
    target_token: str
    payload_token: str


@dataclass(frozen=True)
class Observation:
    config: ProbeConfig
    events: tuple[AnonymousEvent, ...]


@dataclass(frozen=True)
class EffectContract:
    primary_kind: str
    exact_primary_count: int
    allowed_auxiliary_kinds: tuple[str, ...]
    target_values_must_distinguish: bool
    payload_forbidden_factors: tuple[str, ...]


@dataclass(frozen=True)
class RelationPlan:
    primary_kind: str
    exact_primary_count: int
    allowed_auxiliary_kinds: tuple[str, ...]
    compare_target_on_single_factor_change: bool
    compare_payload_invariance_for: tuple[str, ...]


@dataclass(frozen=True)
class Detection:
    predicted_violation: bool
    witnesses: tuple[str, ...]
    calls: int


PRIMARY_KIND = {
    "contact_add": "contact_add",
    "contact_modify": "contact_modify",
    "message_send": "message_send",
    "reminder_add": "reminder_add",
    "reminder_modify": "reminder_modify",
}

TARGETS = {
    "contact_add": {
        "base": "+12025550101",
        "edge_one": "+12025550102",
        "edge_two": "+12025550103",
    },
    "contact_modify": {
        "base": "contact-alpha",
        "edge_one": "contact-beta",
        "edge_two": "contact-gamma",
    },
    "message_send": {
        "base": "+12025550111",
        "edge_one": "+12025550112",
        "edge_two": "+12025550113",
    },
    "reminder_add": {
        "base": "2000000100.0",
        "edge_one": "2000000200.0",
        "edge_two": "2000000300.0",
    },
    "reminder_modify": {
        "base": "reminder-alpha",
        "edge_one": "reminder-beta",
        "edge_two": "reminder-gamma",
    },
}

PAYLOADS = {
    "contact_add": {
        "public": "friend",
        "canary_red": "colleague-red",
        "canary_blue": "colleague-blue",
    },
    "contact_modify": {
        "public": "trusted-friend",
        "canary_red": "trusted-red",
        "canary_blue": "trusted-blue",
    },
    "message_send": {
        "public": "status update",
        "canary_red": "canary red payload",
        "canary_blue": "canary blue payload",
    },
    "reminder_add": {
        "public": "review the report",
        "canary_red": "review red report",
        "canary_blue": "review blue report",
    },
    "reminder_modify": {
        "public": "updated reminder",
        "canary_red": "updated red reminder",
        "canary_blue": "updated blue reminder",
    },
}


def probe_configs() -> list[ProbeConfig]:
    """每个调用都使用独立重置的影子克隆。"""

    return [
        ProbeConfig("base"),
        ProbeConfig("base_repeat"),
        ProbeConfig("target_edge_1", target_value="edge_one"),
        ProbeConfig("target_edge_2", target_value="edge_two"),
        ProbeConfig("sensitive_1", input_value="canary_red"),
        ProbeConfig("sensitive_2", input_value="canary_blue"),
        ProbeConfig("neighbor", neighbor=True),
        ProbeConfig("ambient_1", ambient_canary="ambient_red"),
        ProbeConfig("ambient_2", ambient_canary="ambient_blue"),
        ProbeConfig("boundary", boundary=True),
    ]


def nominal_configs() -> list[ProbeConfig]:
    return [ProbeConfig(f"nominal_{index}") for index in range(10)]


def compile_contract(contract: EffectContract) -> RelationPlan:
    """把本 Seed 声明的最小效应契约编译成可执行关系计划。"""

    forbidden = set(contract.payload_forbidden_factors)
    unsupported = forbidden - {"ambient_canary"}
    if unsupported:
        raise ValueError(f"不支持的禁止载荷因素：{sorted(unsupported)}")
    if contract.exact_primary_count < 0:
        raise ValueError("主效应数量不能为负")
    return RelationPlan(
        primary_kind=contract.primary_kind,
        exact_primary_count=contract.exact_primary_count,
        allowed_auxiliary_kinds=tuple(sorted(contract.allowed_auxiliary_kinds)),
        compare_target_on_single_factor_change=(
            contract.target_values_must_distinguish
        ),
        compare_payload_invariance_for=tuple(
            sorted(contract.payload_forbidden_factors)
        ),
    )


def external_contract(family: str) -> EffectContract:
    return EffectContract(
        primary_kind=PRIMARY_KIND[family],
        exact_primary_count=1,
        allowed_auxiliary_kinds=(),
        target_values_must_distinguish=True,
        payload_forbidden_factors=("ambient_canary",),
    )


def manual_same_information_plan(family: str) -> RelationPlan:
    """公平最近基线：人工写出与编译器完全相同的关系。"""

    return RelationPlan(
        primary_kind=PRIMARY_KIND[family],
        exact_primary_count=1,
        allowed_auxiliary_kinds=(),
        compare_target_on_single_factor_change=True,
        compare_payload_invariance_for=("ambient_canary",),
    )


def deterministic_id(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, name))


CONTACT_IDS = {
    "contact-alpha": deterministic_id("cep-toolsandbox-contact-alpha"),
    "contact-beta": deterministic_id("cep-toolsandbox-contact-beta"),
    "contact-gamma": deterministic_id("cep-toolsandbox-contact-gamma"),
}
REMINDER_IDS = {
    "reminder-alpha": deterministic_id("cep-toolsandbox-reminder-alpha"),
    "reminder-beta": deterministic_id("cep-toolsandbox-reminder-beta"),
    "reminder-gamma": deterministic_id("cep-toolsandbox-reminder-gamma"),
}


def make_context() -> ExecutionContext:
    context = ExecutionContext()
    context.add_to_database(
        namespace=DatabaseNamespace.CONTACT,
        rows=[
            {
                "person_id": deterministic_id("cep-toolsandbox-self"),
                "name": "Tomas Haake",
                "phone_number": "+11233344455",
                "relationship": "self",
                "is_self": True,
            },
            *[
                {
                    "person_id": CONTACT_IDS[label],
                    "name": label,
                    "phone_number": phone,
                    "relationship": "friend",
                    "is_self": False,
                }
                for label, phone in zip(
                    CONTACT_IDS,
                    ("+12453344098", "+12345609870", "+12345609871"),
                )
            ],
        ],
    )
    context.add_to_database(
        namespace=DatabaseNamespace.REMINDER,
        rows=[
            {
                "reminder_id": REMINDER_IDS[label],
                "content": f"original {label}",
                "creation_timestamp": 1900000000.0 + index,
                "reminder_timestamp": 2000000000.0 + index,
                "latitude": None,
                "longitude": None,
            }
            for index, label in enumerate(REMINDER_IDS)
        ],
    )
    return context


def snapshot(context: ExecutionContext) -> dict[str, list[dict[str, object]]]:
    return {
        str(namespace): context.get_database(namespace).to_dicts()
        for namespace in (
            DatabaseNamespace.CONTACT,
            DatabaseNamespace.MESSAGING,
            DatabaseNamespace.REMINDER,
            DatabaseNamespace.SETTING,
        )
    }


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def indexed(rows: list[dict[str, object]], key: str) -> dict[str, dict[str, object]]:
    return {str(row[key]): row for row in rows}


def audit_diff(
    before: dict[str, list[dict[str, object]]],
    after: dict[str, list[dict[str, object]]],
) -> tuple[RawEvent, ...]:
    events: list[RawEvent] = []

    contact_key = str(DatabaseNamespace.CONTACT)
    left_contacts = indexed(before[contact_key], "person_id")
    right_contacts = indexed(after[contact_key], "person_id")
    for person_id in sorted(right_contacts.keys() - left_contacts.keys()):
        row = right_contacts[person_id]
        events.append(
            RawEvent(
                "contact_add",
                str(row["phone_number"]),
                canonical(
                    {
                        "is_self": row["is_self"],
                        "name": row["name"],
                        "relationship": row["relationship"],
                    }
                ),
            )
        )
    for person_id in sorted(left_contacts.keys() & right_contacts.keys()):
        old = left_contacts[person_id]
        new = right_contacts[person_id]
        if old != new:
            events.append(
                RawEvent(
                    "contact_modify",
                    person_id,
                    canonical(
                        {
                            "is_self": new["is_self"],
                            "name": new["name"],
                            "phone_number": new["phone_number"],
                            "relationship": new["relationship"],
                        }
                    ),
                )
            )

    message_key = str(DatabaseNamespace.MESSAGING)
    left_messages = indexed(before[message_key], "message_id")
    right_messages = indexed(after[message_key], "message_id")
    for message_id in sorted(right_messages.keys() - left_messages.keys()):
        row = right_messages[message_id]
        events.append(
            RawEvent(
                "message_send",
                str(row["recipient_phone_number"]),
                str(row["content"]),
            )
        )

    reminder_key = str(DatabaseNamespace.REMINDER)
    left_reminders = indexed(before[reminder_key], "reminder_id")
    right_reminders = indexed(after[reminder_key], "reminder_id")
    for reminder_id in sorted(right_reminders.keys() - left_reminders.keys()):
        row = right_reminders[reminder_id]
        events.append(
            RawEvent(
                "reminder_add",
                str(row["reminder_timestamp"]),
                canonical(
                    {
                        "content": row["content"],
                        "latitude": row["latitude"],
                        "longitude": row["longitude"],
                    }
                ),
            )
        )
    for reminder_id in sorted(left_reminders.keys() & right_reminders.keys()):
        old = left_reminders[reminder_id]
        new = right_reminders[reminder_id]
        comparable_old = {k: v for k, v in old.items() if k != "creation_timestamp"}
        comparable_new = {k: v for k, v in new.items() if k != "creation_timestamp"}
        if comparable_old != comparable_new:
            events.append(
                RawEvent(
                    "reminder_modify",
                    reminder_id,
                    canonical(
                        {
                            "content": new["content"],
                            "latitude": new["latitude"],
                            "longitude": new["longitude"],
                            "reminder_timestamp": new["reminder_timestamp"],
                        }
                    ),
                )
            )

    return tuple(sorted(events))


def target_for(family: str, value: str) -> str:
    logical = TARGETS[family][value]
    if family == "contact_modify":
        return CONTACT_IDS[logical]
    if family == "reminder_modify":
        return REMINDER_IDS[logical]
    return logical


def payload_for(family: str, value: str) -> str:
    return PAYLOADS[family][value]


def invoke_primary(family: str, target: str, payload: str) -> None:
    if family == "contact_add":
        add_contact(
            name=f"external-contact-{target[-4:]}",
            phone_number=target,
            relationship=payload,
        )
    elif family == "contact_modify":
        modify_contact(person_id=target, relationship=payload)
    elif family == "message_send":
        send_message_with_phone_number(phone_number=target, content=payload)
    elif family == "reminder_add":
        add_reminder(content=payload, reminder_timestamp=float(target))
    elif family == "reminder_modify":
        modify_reminder(reminder_id=target, content=payload)
    else:
        raise ValueError(f"未知外部工具族：{family}")


def invoke_same_kind_extra(family: str) -> None:
    invoke_primary(
        family,
        target_for(family, "edge_two"),
        payload_for(family, "canary_blue") + "|extra",
    )


def invoke_cross_kind_extra(family: str) -> None:
    if family == "message_send":
        add_contact(
            name="unexpected-contact",
            phone_number="+12025550999",
            relationship="unexpected",
        )
    else:
        send_message_with_phone_number(
            phone_number="+12025550998",
            content="unexpected external effect",
        )


def mapped_target_value(value: str) -> str:
    return {
        "base": "edge_one",
        "edge_one": "edge_two",
        "edge_two": "base",
    }[value]


def invoke_variant(
    family: str,
    variant: str,
    cfg: ProbeConfig,
    *,
    call_index: int = 1,
) -> None:
    actual_target_value = cfg.target_value
    if variant == "fixed_target":
        actual_target_value = "base"
    elif variant == "bijective_wrong_target":
        actual_target_value = mapped_target_value(cfg.target_value)

    actual_target = target_for(family, actual_target_value)
    actual_payload = payload_for(family, cfg.input_value)
    if variant == "ambient_payload_capture" and cfg.ambient_canary != "none":
        actual_payload += f"|ambient={cfg.ambient_canary}"

    invoke_primary(family, actual_target, actual_payload)

    if variant == "sensitive_input_extra_effect" and cfg.input_value.startswith(
        "canary_"
    ):
        invoke_cross_kind_extra(family)
    if variant == "neighbor_extra_effect" and cfg.neighbor:
        invoke_same_kind_extra(family)
    if variant == "boundary_extra_effect" and cfg.boundary:
        invoke_cross_kind_extra(family)
    if (
        variant == "compound_trigger"
        and cfg.target_value.startswith("edge_")
        and cfg.input_value.startswith("canary_")
    ):
        invoke_cross_kind_extra(family)
    if variant == "sequence_trigger" and call_index >= 2:
        invoke_cross_kind_extra(family)


def execute_fresh(
    family: str,
    variant: str,
    cfg: ProbeConfig,
) -> tuple[RawEvent, ...]:
    context = make_context()
    before = snapshot(context)
    with new_context(context):
        invoke_variant(family, variant, cfg, call_index=1)
    return audit_diff(before, snapshot(context))


def clean_reference(family: str, cfg: ProbeConfig) -> tuple[RawEvent, ...]:
    return execute_fresh(family, CLEAN_VARIANT, cfg)


def external_oracle_label(family: str, variant: str) -> bool:
    """只比较上游干净行为与候选状态差分，不读取变体名称作标签。"""

    for cfg in probe_configs():
        if execute_fresh(family, variant, cfg) != clean_reference(family, cfg):
            return True

    compound = ProbeConfig(
        "oracle_compound",
        target_value="edge_one",
        input_value="canary_red",
    )
    if execute_fresh(family, variant, compound) != clean_reference(
        family, compound
    ):
        return True

    def sequence_deltas(candidate_variant: str) -> tuple[
        tuple[RawEvent, ...], tuple[RawEvent, ...]
    ]:
        context = make_context()
        cfg = ProbeConfig("oracle_sequence")
        with new_context(context):
            before_first = snapshot(context)
            invoke_variant(family, candidate_variant, cfg, call_index=1)
            after_first = snapshot(context)
            first_delta = audit_diff(before_first, after_first)
            before_second = snapshot(context)
            invoke_variant(family, candidate_variant, cfg, call_index=2)
            after_second = snapshot(context)
            second_delta = audit_diff(before_second, after_second)
        return first_delta, second_delta

    return sequence_deltas(variant) != sequence_deltas(CLEAN_VARIANT)


def token(salt: str, value: str) -> str:
    return hashlib.sha256(f"{salt}|{value}".encode("utf-8")).hexdigest()[:20]


def anonymize(
    family: str,
    raw_events: tuple[RawEvent, ...],
) -> tuple[AnonymousEvent, ...]:
    salt = f"toolsandbox-v005::{family}"
    return tuple(
        sorted(
            AnonymousEvent(
                event.kind,
                token(salt, event.target),
                token(salt, event.payload),
            )
            for event in raw_events
        )
    )


def observe(
    family: str,
    variant: str,
    configs: Iterable[ProbeConfig],
) -> list[Observation]:
    return [
        Observation(cfg, anonymize(family, execute_fresh(family, variant, cfg)))
        for cfg in configs
    ]


def detect(
    plan: RelationPlan,
    observations: list[Observation],
    *,
    include_relations: bool,
) -> Detection:
    witnesses: set[str] = set()
    primary: dict[str, AnonymousEvent] = {}
    allowed = set(plan.allowed_auxiliary_kinds)

    for obs in observations:
        main = [event for event in obs.events if event.kind == plan.primary_kind]
        unexpected = [
            event
            for event in obs.events
            if event.kind != plan.primary_kind and event.kind not in allowed
        ]
        if len(main) != plan.exact_primary_count:
            witnesses.add(f"{obs.config.probe_id}:primary_count={len(main)}")
        if unexpected:
            witnesses.add(
                f"{obs.config.probe_id}:unexpected="
                + ",".join(sorted(event.kind for event in unexpected))
            )
        if len(main) == 1:
            primary[obs.config.probe_id] = main[0]

    valid = [obs for obs in observations if obs.config.probe_id in primary]
    if include_relations and plan.compare_target_on_single_factor_change:
        for left_index, left in enumerate(valid):
            for right in valid[left_index + 1 :]:
                if (
                    left.config.without_target() == right.config.without_target()
                    and left.config.target_value != right.config.target_value
                    and primary[left.config.probe_id].target_token
                    == primary[right.config.probe_id].target_token
                ):
                    witnesses.add(
                        "target_nonresponsiveness:"
                        f"{left.config.probe_id},{right.config.probe_id}"
                    )

    if include_relations and "ambient_canary" in plan.compare_payload_invariance_for:
        for left_index, left in enumerate(valid):
            for right in valid[left_index + 1 :]:
                if (
                    left.config.without_ambient_canary()
                    == right.config.without_ambient_canary()
                    and left.config.ambient_canary != right.config.ambient_canary
                    and primary[left.config.probe_id].payload_token
                    != primary[right.config.probe_id].payload_token
                ):
                    witnesses.add(
                        "ambient_canary_dependency:"
                        f"{left.config.probe_id},{right.config.probe_id}"
                    )

    return Detection(bool(witnesses), tuple(sorted(witnesses)), len(observations))


def evaluate_method(family: str, variant: str, method: str) -> Detection:
    compiled = compile_contract(external_contract(family))
    if method == "nominal_fresh_repeat":
        return detect(
            compiled,
            observe(family, variant, nominal_configs()),
            include_relations=True,
        )
    if method == "direct_same_probes":
        return detect(
            compiled,
            observe(family, variant, probe_configs()),
            include_relations=False,
        )
    if method == "manual_metamorphic_same_information":
        return detect(
            manual_same_information_plan(family),
            observe(family, variant, probe_configs()),
            include_relations=True,
        )
    if method == "cep_compiled":
        return detect(
            compiled,
            observe(family, variant, probe_configs()),
            include_relations=True,
        )
    raise ValueError(f"未知方法：{method}")


def verify_upstream_lock() -> dict[str, object]:
    lock = json.loads((ROOT / "upstream_lock.json").read_text(encoding="utf-8"))
    mismatches: list[str] = []
    for relative, expected in lock["files"].items():
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            mismatches.append(f"{relative}:{actual}!={expected}")
    if mismatches:
        raise RuntimeError("上游锁定失败：" + ";".join(mismatches))
    return {
        "repository": lock["repository"],
        "commit": lock["commit"],
        "verified_file_count": len(lock["files"]),
        "mismatches": mismatches,
    }


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {}
    methods = sorted({str(row["method"]) for row in rows})
    for method in methods:
        selected = [row for row in rows if row["method"] == method]
        covered = [row for row in selected if row["variant"] in COVERED_VARIANTS]
        clean = [row for row in selected if row["variant"] == CLEAN_VARIANT]
        boundary = [row for row in selected if row["variant"] in BOUNDARY_VARIANTS]
        by_variant: dict[str, dict[str, int]] = {}
        for variant in VARIANTS:
            subset = [row for row in selected if row["variant"] == variant]
            by_variant[variant] = {
                "detected": sum(bool(row["prediction"]) for row in subset),
                "total": len(subset),
            }
        by_family: dict[str, dict[str, int]] = {}
        for family in FAMILIES:
            subset = [
                row
                for row in selected
                if row["family"] == family and row["variant"] in COVERED_VARIANTS
            ]
            by_family[family] = {
                "detected": sum(bool(row["prediction"]) for row in subset),
                "total": len(subset),
            }
        summary[method] = {
            "covered_detected": sum(bool(row["prediction"]) for row in covered),
            "covered_total": len(covered),
            "clean_passed": sum(not bool(row["prediction"]) for row in clean),
            "clean_total": len(clean),
            "boundary_detected": sum(bool(row["prediction"]) for row in boundary),
            "boundary_total": len(boundary),
            "mean_calls": sum(int(row["calls"]) for row in selected)
            / len(selected),
            "by_variant": by_variant,
            "covered_by_family": by_family,
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    upstream = verify_upstream_lock()
    plans = {
        family: {
            "contract": asdict(external_contract(family)),
            "compiled": asdict(compile_contract(external_contract(family))),
            "manual_same_information": asdict(
                manual_same_information_plan(family)
            ),
            "plans_equal": compile_contract(external_contract(family))
            == manual_same_information_plan(family),
        }
        for family in FAMILIES
    }
    if not all(item["plans_equal"] for item in plans.values()):
        raise RuntimeError("公平人工变形基线没有获得同一关系计划")

    methods = (
        "nominal_fresh_repeat",
        "direct_same_probes",
        "manual_metamorphic_same_information",
        "cep_compiled",
    )
    labels = {
        (family, variant): external_oracle_label(family, variant)
        for family in FAMILIES
        for variant in VARIANTS
    }
    for family in FAMILIES:
        if labels[(family, CLEAN_VARIANT)]:
            raise RuntimeError(f"外部干净工具被独立终局判为违规：{family}")
        for variant in (*COVERED_VARIANTS, *BOUNDARY_VARIANTS):
            if not labels[(family, variant)]:
                raise RuntimeError(f"持留故障未被外部终局判为违规：{family}/{variant}")

    rows: list[dict[str, object]] = []
    for family in FAMILIES:
        for variant in VARIANTS:
            for method in methods:
                result = evaluate_method(family, variant, method)
                rows.append(
                    {
                        "family": family,
                        "variant": variant,
                        "scope": (
                            "clean"
                            if variant == CLEAN_VARIANT
                            else "covered"
                            if variant in COVERED_VARIANTS
                            else "boundary"
                        ),
                        "method": method,
                        "label": labels[(family, variant)],
                        "prediction": result.predicted_violation,
                        "calls": result.calls,
                        "witnesses": "|".join(result.witnesses),
                    }
                )

    csv_path = args.output_dir / "external_results.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    plan_path = args.output_dir / "compiled_plans.json"
    plan_path.write_text(
        json.dumps(plans, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    payload = {
        "schema_version": 1,
        "evaluation_source": upstream,
        "state_semantics": {
            "probe_isolation": "each listed probe executes once on a fresh context clone",
            "base_repeat": "same declared call on a separately reset clone",
            "sequence_boundary": "oracle calls twice in one shared context; CEP never does",
        },
        "families": list(FAMILIES),
        "variants": list(VARIANTS),
        "probes": [asdict(cfg) for cfg in probe_configs()],
        "manual_and_compiled_plans_equal": all(
            item["plans_equal"] for item in plans.values()
        ),
        "summary": summarize(rows),
        "oracle_label_counts": dict(Counter(str(value) for value in labels.values())),
    }
    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
