from __future__ import annotations

from dqbp_core import Branch, Domain, Probe


def _branches(
    rows: list[tuple[str, str, dict[str, str], float]]
) -> tuple[Branch, ...]:
    return tuple(
        Branch(name=name, decision=decision, observations=observations, prior=prior)
        for name, decision, observations, prior in rows
    )


def build_domains() -> tuple[Domain, ...]:
    """Return three stateful tool domains with schema-valid ambiguous writes.

    The branch priors are part of the controller specification, not hidden labels.
    Receipt/version variants deliberately differ in state identity while sharing the
    same downstream decision. This tests whether a selector spends budget on
    decision-irrelevant state reconstruction.
    """

    reservation_probes = (
        Probe("target_status", 1),
        Probe("payment_state", 1),
        Probe("other_booking", 1),
        Probe("receipt_state", 1),
        Probe("audit_event", 2),
    )
    reservation = Domain(
        name="reservation",
        fixed_probe="target_status",
        probes=reservation_probes,
        branches=_branches(
            [
                (
                    "correct_receipt_synced",
                    "PROCEED",
                    {
                        "target_status": "CONFIRMED",
                        "payment_state": "CAPTURED",
                        "other_booking": "UNCHANGED",
                        "receipt_state": "SYNCED",
                        "audit_event": "TARGET_CONFIRMED",
                    },
                    0.14,
                ),
                (
                    "correct_receipt_pending",
                    "PROCEED",
                    {
                        "target_status": "CONFIRMED",
                        "payment_state": "CAPTURED",
                        "other_booking": "UNCHANGED",
                        "receipt_state": "PENDING",
                        "audit_event": "TARGET_CONFIRMED",
                    },
                    0.12,
                ),
                (
                    "correct_receipt_external",
                    "PROCEED",
                    {
                        "target_status": "CONFIRMED",
                        "payment_state": "CAPTURED",
                        "other_booking": "UNCHANGED",
                        "receipt_state": "EXTERNAL",
                        "audit_event": "TARGET_CONFIRMED",
                    },
                    0.10,
                ),
                (
                    "correct_receipt_suppressed",
                    "PROCEED",
                    {
                        "target_status": "CONFIRMED",
                        "payment_state": "CAPTURED",
                        "other_booking": "UNCHANGED",
                        "receipt_state": "SUPPRESSED",
                        "audit_event": "TARGET_CONFIRMED",
                    },
                    0.09,
                ),
                (
                    "silent_noop",
                    "RETRY_TARGET",
                    {
                        "target_status": "PENDING",
                        "payment_state": "PENDING",
                        "other_booking": "UNCHANGED",
                        "receipt_state": "NONE",
                        "audit_event": "NO_MUTATION",
                    },
                    0.16,
                ),
                (
                    "payment_partial",
                    "PATCH_PAYMENT",
                    {
                        "target_status": "CONFIRMED",
                        "payment_state": "PENDING",
                        "other_booking": "UNCHANGED",
                        "receipt_state": "PENDING",
                        "audit_event": "TARGET_STATUS_ONLY",
                    },
                    0.14,
                ),
                (
                    "wrong_booking",
                    "REVERSE_OTHER_AND_RETRY",
                    {
                        "target_status": "PENDING",
                        "payment_state": "PENDING",
                        "other_booking": "CONFIRMED",
                        "receipt_state": "EXTERNAL",
                        "audit_event": "OTHER_CONFIRMED",
                    },
                    0.13,
                ),
                (
                    "double_capture",
                    "UNDO_DUPLICATE_PAYMENT",
                    {
                        "target_status": "CONFIRMED",
                        "payment_state": "DOUBLE_CAPTURED",
                        "other_booking": "UNCHANGED",
                        "receipt_state": "SYNCED",
                        "audit_event": "TARGET_DOUBLE_CAPTURE",
                    },
                    0.12,
                ),
            ]
        ),
    )

    access_probes = (
        Probe("target_role", 1),
        Probe("scope_state", 1),
        Probe("other_principal", 1),
        Probe("etag_state", 1),
        Probe("audit_event", 2),
    )
    access = Domain(
        name="access_control",
        fixed_probe="target_role",
        probes=access_probes,
        branches=_branches(
            [
                (
                    "correct_etag_current",
                    "PROCEED",
                    {
                        "target_role": "EDITOR",
                        "scope_state": "PROJECT_ONLY",
                        "other_principal": "UNCHANGED",
                        "etag_state": "CURRENT",
                        "audit_event": "TARGET_GRANTED",
                    },
                    0.14,
                ),
                (
                    "correct_etag_lagged",
                    "PROCEED",
                    {
                        "target_role": "EDITOR",
                        "scope_state": "PROJECT_ONLY",
                        "other_principal": "UNCHANGED",
                        "etag_state": "LAGGED",
                        "audit_event": "TARGET_GRANTED",
                    },
                    0.12,
                ),
                (
                    "correct_etag_rotated",
                    "PROCEED",
                    {
                        "target_role": "EDITOR",
                        "scope_state": "PROJECT_ONLY",
                        "other_principal": "UNCHANGED",
                        "etag_state": "ROTATED",
                        "audit_event": "TARGET_GRANTED",
                    },
                    0.10,
                ),
                (
                    "correct_etag_hidden",
                    "PROCEED",
                    {
                        "target_role": "EDITOR",
                        "scope_state": "PROJECT_ONLY",
                        "other_principal": "UNCHANGED",
                        "etag_state": "HIDDEN",
                        "audit_event": "TARGET_GRANTED",
                    },
                    0.09,
                ),
                (
                    "silent_noop",
                    "RETRY_TARGET",
                    {
                        "target_role": "VIEWER",
                        "scope_state": "PROJECT_ONLY",
                        "other_principal": "UNCHANGED",
                        "etag_state": "UNCHANGED",
                        "audit_event": "NO_MUTATION",
                    },
                    0.16,
                ),
                (
                    "scope_partial",
                    "NARROW_SCOPE",
                    {
                        "target_role": "EDITOR",
                        "scope_state": "ORGANIZATION_WIDE",
                        "other_principal": "UNCHANGED",
                        "etag_state": "CURRENT",
                        "audit_event": "TARGET_OVERBROAD",
                    },
                    0.14,
                ),
                (
                    "wrong_principal",
                    "REVOKE_OTHER_AND_RETRY",
                    {
                        "target_role": "VIEWER",
                        "scope_state": "PROJECT_ONLY",
                        "other_principal": "EDITOR",
                        "etag_state": "ROTATED",
                        "audit_event": "OTHER_GRANTED",
                    },
                    0.13,
                ),
                (
                    "duplicate_grant",
                    "REMOVE_DUPLICATE_BINDING",
                    {
                        "target_role": "EDITOR",
                        "scope_state": "DUPLICATE_BINDING",
                        "other_principal": "UNCHANGED",
                        "etag_state": "CURRENT",
                        "audit_event": "TARGET_DUPLICATED",
                    },
                    0.12,
                ),
            ]
        ),
    )

    inventory_probes = (
        Probe("target_quantity", 1),
        Probe("warehouse_balance", 1),
        Probe("other_sku", 1),
        Probe("sync_version", 1),
        Probe("audit_event", 2),
    )
    inventory = Domain(
        name="inventory",
        fixed_probe="target_quantity",
        probes=inventory_probes,
        branches=_branches(
            [
                (
                    "correct_sync_current",
                    "PROCEED",
                    {
                        "target_quantity": "PLUS_5",
                        "warehouse_balance": "BALANCED",
                        "other_sku": "UNCHANGED",
                        "sync_version": "CURRENT",
                        "audit_event": "TARGET_INCREMENTED",
                    },
                    0.14,
                ),
                (
                    "correct_sync_lagged",
                    "PROCEED",
                    {
                        "target_quantity": "PLUS_5",
                        "warehouse_balance": "BALANCED",
                        "other_sku": "UNCHANGED",
                        "sync_version": "LAGGED",
                        "audit_event": "TARGET_INCREMENTED",
                    },
                    0.12,
                ),
                (
                    "correct_sync_external",
                    "PROCEED",
                    {
                        "target_quantity": "PLUS_5",
                        "warehouse_balance": "BALANCED",
                        "other_sku": "UNCHANGED",
                        "sync_version": "EXTERNAL",
                        "audit_event": "TARGET_INCREMENTED",
                    },
                    0.10,
                ),
                (
                    "correct_sync_hidden",
                    "PROCEED",
                    {
                        "target_quantity": "PLUS_5",
                        "warehouse_balance": "BALANCED",
                        "other_sku": "UNCHANGED",
                        "sync_version": "HIDDEN",
                        "audit_event": "TARGET_INCREMENTED",
                    },
                    0.09,
                ),
                (
                    "silent_noop",
                    "RETRY_TARGET",
                    {
                        "target_quantity": "UNCHANGED",
                        "warehouse_balance": "BALANCED",
                        "other_sku": "UNCHANGED",
                        "sync_version": "UNCHANGED",
                        "audit_event": "NO_MUTATION",
                    },
                    0.16,
                ),
                (
                    "ledger_partial",
                    "RECONCILE_LEDGER",
                    {
                        "target_quantity": "PLUS_5",
                        "warehouse_balance": "UNBALANCED",
                        "other_sku": "UNCHANGED",
                        "sync_version": "LAGGED",
                        "audit_event": "TARGET_WITHOUT_LEDGER",
                    },
                    0.14,
                ),
                (
                    "wrong_sku",
                    "REVERSE_OTHER_AND_RETRY",
                    {
                        "target_quantity": "UNCHANGED",
                        "warehouse_balance": "BALANCED",
                        "other_sku": "PLUS_5",
                        "sync_version": "EXTERNAL",
                        "audit_event": "OTHER_INCREMENTED",
                    },
                    0.13,
                ),
                (
                    "double_increment",
                    "REMOVE_EXTRA_5",
                    {
                        "target_quantity": "PLUS_10",
                        "warehouse_balance": "UNBALANCED",
                        "other_sku": "UNCHANGED",
                        "sync_version": "CURRENT",
                        "audit_event": "TARGET_DOUBLE_INCREMENT",
                    },
                    0.12,
                ),
            ]
        ),
    )
    return reservation, access, inventory


def validate_domains(domains: tuple[Domain, ...]) -> None:
    for domain in domains:
        if abs(sum(branch.prior for branch in domain.branches) - 1.0) > 1e-9:
            raise ValueError(f"priors do not sum to one: {domain.name}")
        probe_names = {probe.name for probe in domain.probes}
        if domain.fixed_probe not in probe_names:
            raise ValueError(f"fixed probe is missing: {domain.name}")
        if len(probe_names) != len(domain.probes):
            raise ValueError(f"duplicate probe name: {domain.name}")
        for branch in domain.branches:
            if set(branch.observations) != probe_names:
                raise ValueError(
                    f"branch observations do not match probes: {domain.name}/{branch.name}"
                )
