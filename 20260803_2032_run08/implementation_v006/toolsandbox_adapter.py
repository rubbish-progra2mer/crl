#!/usr/bin/env python3
"""固定 ToolSandbox 提交到 v006 观察闭包计划的外部工具适配器。"""

from __future__ import annotations

import hashlib
import json
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path

from observation_closed_effects import (
    CompiledPlan,
    ObservedEvent,
    Probe,
    ProbeObservation,
    ProjectionSpec,
    canonical_hash,
)


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "vendor"))

from tool_sandbox.common.execution_context import (  # noqa: E402
    DatabaseNamespace,
    ExecutionContext,
    new_context,
)
from tool_sandbox.tools.contact import add_contact, modify_contact  # noqa: E402
from tool_sandbox.tools.messaging import (  # noqa: E402
    send_message_with_phone_number,
)
from tool_sandbox.tools.reminder import add_reminder, modify_reminder  # noqa: E402


FAMILIES = (
    "contact_add",
    "contact_modify",
    "message_send",
    "reminder_add",
    "reminder_modify",
)


@dataclass(frozen=True, order=True)
class RawEvent:
    kind: str
    target: str
    payload: str


def deterministic_id(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, name))


CONTACT_IDS = {
    "contact-alpha": deterministic_id("ocec-toolsandbox-contact-alpha"),
    "contact-beta": deterministic_id("ocec-toolsandbox-contact-beta"),
    "contact-gamma": deterministic_id("ocec-toolsandbox-contact-gamma"),
}
REMINDER_IDS = {
    "reminder-alpha": deterministic_id("ocec-toolsandbox-reminder-alpha"),
    "reminder-beta": deterministic_id("ocec-toolsandbox-reminder-beta"),
    "reminder-gamma": deterministic_id("ocec-toolsandbox-reminder-gamma"),
}


TARGETS = {
    "contact_add": {
        "base": "+12025550101",
        "target_zero": "+12025550102",
        "target_one": "+12025550103",
    },
    "contact_modify": {
        "base": "contact-alpha",
        "target_zero": "contact-beta",
        "target_one": "contact-gamma",
    },
    "message_send": {
        "base": "+12025550111",
        "target_zero": "+12025550112",
        "target_one": "+12025550113",
    },
    "reminder_add": {
        "base": "2000000100.0",
        "target_zero": "2000000200.0",
        "target_one": "2000000300.0",
    },
    "reminder_modify": {
        "base": "reminder-alpha",
        "target_zero": "reminder-beta",
        "target_one": "reminder-gamma",
    },
}


PUBLIC_PAYLOADS = {
    "contact_add": "friend",
    "contact_modify": "trusted-friend",
    "message_send": "status update",
    "reminder_add": "review the report",
    "reminder_modify": "updated reminder",
}


def make_context() -> ExecutionContext:
    context = ExecutionContext()
    context.add_to_database(
        namespace=DatabaseNamespace.CONTACT,
        rows=[
            {
                "person_id": deterministic_id("ocec-toolsandbox-self"),
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


def _canonical(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _indexed(
    rows: list[dict[str, object]], key: str
) -> dict[str, dict[str, object]]:
    return {str(row[key]): row for row in rows}


def audit_diff(
    before: dict[str, list[dict[str, object]]],
    after: dict[str, list[dict[str, object]]],
) -> tuple[RawEvent, ...]:
    events: list[RawEvent] = []

    contact_key = str(DatabaseNamespace.CONTACT)
    left_contacts = _indexed(before[contact_key], "person_id")
    right_contacts = _indexed(after[contact_key], "person_id")
    for person_id in sorted(right_contacts.keys() - left_contacts.keys()):
        row = right_contacts[person_id]
        events.append(
            RawEvent(
                "contact_add",
                str(row["phone_number"]),
                _canonical(
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
                    _canonical(
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
    left_messages = _indexed(before[message_key], "message_id")
    right_messages = _indexed(after[message_key], "message_id")
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
    left_reminders = _indexed(before[reminder_key], "reminder_id")
    right_reminders = _indexed(after[reminder_key], "reminder_id")
    for reminder_id in sorted(right_reminders.keys() - left_reminders.keys()):
        row = right_reminders[reminder_id]
        events.append(
            RawEvent(
                "reminder_add",
                str(row["reminder_timestamp"]),
                _canonical(
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
        comparable_old = {
            key: value for key, value in old.items() if key != "creation_timestamp"
        }
        comparable_new = {
            key: value for key, value in new.items() if key != "creation_timestamp"
        }
        if comparable_old != comparable_new:
            events.append(
                RawEvent(
                    "reminder_modify",
                    reminder_id,
                    _canonical(
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


def target_for(family: str, logical_value: str) -> str:
    target = TARGETS[family][logical_value]
    if family == "contact_modify":
        return CONTACT_IDS[target]
    if family == "reminder_modify":
        return REMINDER_IDS[target]
    return target


def _logical_target(family: str, raw_target: str) -> str | None:
    for logical in TARGETS[family]:
        if target_for(family, logical) == raw_target:
            return logical
    return None


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
        raise ValueError(f"未知 ToolSandbox 工具族：{family}")


def _invoke_same_kind_extra(family: str) -> None:
    invoke_primary(
        family,
        target_for(family, "target_one"),
        PUBLIC_PAYLOADS[family] + "|extra",
    )


def _invoke_allowed_auxiliary(family: str) -> None:
    if family == "message_send":
        add_contact(
            name="auxiliary-contact",
            phone_number="+12025550999",
            relationship="auxiliary",
        )
    else:
        send_message_with_phone_number(
            phone_number="+12025550998",
            content="auxiliary external effect",
        )


def _invoke_forbidden_auxiliary(family: str) -> None:
    if family == "message_send":
        add_reminder(
            content="forbidden auxiliary reminder",
            reminder_timestamp=2000000999.0,
        )
    else:
        add_contact(
            name="forbidden-contact",
            phone_number="+12025550997",
            relationship="forbidden",
        )


def _mapped_target(logical_value: str) -> str:
    return {
        "base": "target_zero",
        "target_zero": "target_one",
        "target_one": "base",
    }[logical_value]


def invoke_variant(
    family: str,
    variant: str,
    probe: Probe,
) -> None:
    actual_target_value = probe.target_value
    if variant == "fixed_target":
        actual_target_value = "base"
    elif variant == "wrong_identity":
        actual_target_value = _mapped_target(probe.target_value)

    payload = PUBLIC_PAYLOADS[family]
    if variant == "ambient_payload_capture" and probe.ambient_canary != "none":
        payload += f"|ambient={probe.ambient_canary}"
    if variant == "sensitive_payload_capture" and probe.input_value != "public":
        payload += f"|sensitive={probe.input_value}"

    invoke_primary(family, target_for(family, actual_target_value), payload)
    if variant == "count_two":
        _invoke_same_kind_extra(family)
    if variant == "allowed_auxiliary":
        _invoke_allowed_auxiliary(family)
    if variant == "forbidden_auxiliary":
        _invoke_forbidden_auxiliary(family)


def execute_fresh(
    family: str, variant: str, probe: Probe
) -> tuple[RawEvent, ...]:
    context = make_context()
    before = snapshot(context)
    with new_context(context):
        invoke_variant(family, variant, probe)
    return audit_diff(before, snapshot(context))


def _token(salt: str, value: str) -> str:
    return hashlib.sha256(f"{salt}|{value}".encode("utf-8")).hexdigest()[:20]


def anonymize(
    family: str,
    probe: Probe,
    raw_events: tuple[RawEvent, ...],
    projection: ProjectionSpec,
    primary_kind: str,
) -> tuple[ObservedEvent, ...]:
    events: list[ObservedEvent] = []
    for event in raw_events:
        if projection.target_visibility == "revealed":
            logical = (
                _logical_target(family, event.target)
                if event.kind == primary_kind
                else None
            )
            target_token = logical or event.target
        else:
            target_salt = (
                projection.normalizer_id
                if projection.target_visibility == "stable_anonymous"
                else f"{projection.normalizer_id}|{probe.probe_id}"
            )
            target_token = _token(f"target|{target_salt}", event.target)

        if projection.payload_visibility == "revealed":
            payload_token = event.payload
        else:
            payload_salt = (
                projection.normalizer_id
                if projection.payload_visibility == "stable_anonymous"
                else f"{projection.normalizer_id}|{probe.probe_id}"
            )
            payload_token = _token(f"payload|{payload_salt}", event.payload)
        events.append(
            ObservedEvent(event.kind, target_token, payload_token)
        )
    return tuple(sorted(events))


def observe_plan(
    family: str,
    variant: str,
    plan: CompiledPlan,
    projection: ProjectionSpec,
) -> tuple[ProbeObservation, ...]:
    return tuple(
        ProbeObservation(
            probe.probe_id,
            anonymize(
                family,
                probe,
                execute_fresh(family, variant, probe),
                projection,
                plan.primary_kind,
            ),
        )
        for probe in plan.probes
    )


def raw_execution_hash(
    family: str, variant: str, plan: CompiledPlan
) -> str:
    rows = [
        {
            "probe": probe.probe_id,
            "events": [
                {
                    "kind": event.kind,
                    "target": event.target,
                    "payload": event.payload,
                }
                for event in execute_fresh(family, variant, probe)
            ],
        }
        for probe in plan.probes
    ]
    return canonical_hash(rows)


def verify_upstream_lock() -> dict[str, object]:
    lock = json.loads((ROOT / "upstream_lock.json").read_text(encoding="utf-8"))
    checked = []
    for relative, expected in sorted(lock["files"].items()):
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"上游文件哈希不匹配：{relative}")
        checked.append(relative)
    return {
        "repository": lock["repository"],
        "commit": lock["commit"],
        "verified_files": checked,
        "verified_count": len(checked),
    }
