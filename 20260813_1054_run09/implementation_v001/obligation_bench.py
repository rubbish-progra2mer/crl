from __future__ import annotations

from dataclasses import dataclass

from dqbp_core import ABSTAIN as DQBP_ABSTAIN
from dqbp_core import Branch, Domain
from obligation_core import ABSTAIN, PROCEED, Atom, EvidenceProbe, PlanAction
from statefault_bench import build_domains


@dataclass(frozen=True, slots=True)
class ObligationDomain:
    name: str
    branch_model: Domain
    probes: tuple[EvidenceProbe, ...]
    protected_commit: PlanAction
    prefix_actions: tuple[PlanAction, ...]
    target_atom: Atom
    tool_contract_atoms: tuple[Atom, ...]
    unseen_faults: tuple[Branch, ...]


def _probe_specs(domain: Domain) -> tuple[EvidenceProbe, ...]:
    return tuple(
        EvidenceProbe(probe.name, probe.cost, frozenset({probe.name}))
        for probe in domain.probes
    )


def _branch(
    name: str, observations: dict[str, str], *, decision: str = DQBP_ABSTAIN
) -> Branch:
    return Branch(name=name, decision=decision, observations=observations, prior=0.0)


def build_obligation_domains() -> tuple[ObligationDomain, ...]:
    reservation, access, inventory = build_domains()

    reservation_prefix = PlanAction(
        "render_confirmation_draft",
        (Atom("payment_state", "CAPTURED"),),
        {"confirmation_ready": "YES"},
    )
    reservation_commit = PlanAction(
        "issue_travel_confirmation",
        (
            Atom("target_status", "CONFIRMED"),
            Atom("other_booking", "UNCHANGED"),
            Atom("confirmation_ready", "YES"),
        ),
        {},
    )
    reservation_domain = ObligationDomain(
        name="reservation",
        branch_model=reservation,
        probes=_probe_specs(reservation),
        protected_commit=reservation_commit,
        prefix_actions=(reservation_prefix,),
        target_atom=Atom("target_status", "CONFIRMED"),
        tool_contract_atoms=(
            Atom("target_status", "CONFIRMED"),
            Atom("payment_state", "CAPTURED"),
            Atom("other_booking", "UNCHANGED"),
            Atom("audit_event", "TARGET_CONFIRMED"),
        ),
        unseen_faults=(
            _branch(
                "spoofed_target_failure",
                {
                    "target_status": "PENDING",
                    "payment_state": "CAPTURED",
                    "other_booking": "UNCHANGED",
                    "receipt_state": "SYNCED",
                    "audit_event": "TARGET_CONFIRMED",
                },
            ),
        ),
    )

    access_prefix = PlanAction(
        "build_project_capability",
        (
            Atom("target_role", "EDITOR"),
            Atom("scope_state", "PROJECT_ONLY"),
        ),
        {"capability_ready": "YES"},
    )
    access_commit = PlanAction(
        "permit_editor_operation",
        (
            Atom("other_principal", "UNCHANGED"),
            Atom("capability_ready", "YES"),
        ),
        {},
    )
    access_domain = ObligationDomain(
        name="access_control",
        branch_model=access,
        probes=_probe_specs(access),
        protected_commit=access_commit,
        prefix_actions=(access_prefix,),
        target_atom=Atom("target_role", "EDITOR"),
        tool_contract_atoms=(
            Atom("target_role", "EDITOR"),
            Atom("scope_state", "PROJECT_ONLY"),
            Atom("other_principal", "UNCHANGED"),
            Atom("audit_event", "TARGET_GRANTED"),
        ),
        unseen_faults=(
            _branch(
                "spoofed_other_principal_failure",
                {
                    "target_role": "EDITOR",
                    "scope_state": "PROJECT_ONLY",
                    "other_principal": "EDITOR",
                    "etag_state": "CURRENT",
                    "audit_event": "TARGET_GRANTED",
                },
            ),
        ),
    )

    inventory_prefix = PlanAction(
        "build_restock_certificate",
        (
            Atom("target_quantity", "PLUS_5"),
            Atom("warehouse_balance", "BALANCED"),
        ),
        {"restock_certificate": "READY"},
    )
    inventory_commit = PlanAction(
        "publish_restock_complete",
        (
            Atom("other_sku", "UNCHANGED"),
            Atom("restock_certificate", "READY"),
        ),
        {},
    )
    inventory_domain = ObligationDomain(
        name="inventory",
        branch_model=inventory,
        probes=_probe_specs(inventory),
        protected_commit=inventory_commit,
        prefix_actions=(inventory_prefix,),
        target_atom=Atom("target_quantity", "PLUS_5"),
        tool_contract_atoms=(
            Atom("target_quantity", "PLUS_5"),
            Atom("warehouse_balance", "BALANCED"),
            Atom("other_sku", "UNCHANGED"),
            Atom("audit_event", "TARGET_INCREMENTED"),
        ),
        unseen_faults=(
            _branch(
                "spoofed_other_sku_failure",
                {
                    "target_quantity": "PLUS_5",
                    "warehouse_balance": "BALANCED",
                    "other_sku": "PLUS_5",
                    "sync_version": "CURRENT",
                    "audit_event": "TARGET_INCREMENTED",
                },
            ),
        ),
    )
    return reservation_domain, access_domain, inventory_domain


def expected_gate(branch: Branch) -> str:
    return PROCEED if branch.decision == PROCEED else ABSTAIN


def validate_obligation_domains(domains: tuple[ObligationDomain, ...]) -> None:
    for domain in domains:
        model_probe_names = {probe.name for probe in domain.branch_model.probes}
        evidence_probe_names = {probe.name for probe in domain.probes}
        if model_probe_names != evidence_probe_names:
            raise ValueError(f"probe mismatch: {domain.name}")
        for fault in domain.unseen_faults:
            if set(fault.observations) != model_probe_names:
                raise ValueError(f"unseen fault observation mismatch: {fault.name}")
            if expected_gate(fault) != ABSTAIN:
                raise ValueError(f"unseen fault must block commit: {fault.name}")
