from __future__ import annotations

from dataclasses import dataclass

from obligation_core import Atom, EvidenceProbe, PlanAction


@dataclass(frozen=True, slots=True)
class PlanVariant:
    name: str
    prefix_actions: tuple[PlanAction, ...]
    protected_commit: PlanAction


@dataclass(frozen=True, slots=True)
class PlanVariationDomain:
    name: str
    variants: tuple[PlanVariant, ...]
    probes: tuple[EvidenceProbe, ...]
    static_domain_atoms: tuple[Atom, ...]
    fixed_target_atom: Atom


def _derived_variant(
    name: str,
    required_environment_atoms: tuple[Atom, ...],
    derived_field: str,
) -> PlanVariant:
    prefix = PlanAction(
        name=f"prepare_{name}",
        preconditions=required_environment_atoms,
        effects={derived_field: "READY"},
        trusted_deterministic=True,
    )
    commit = PlanAction(
        name=f"commit_{name}",
        preconditions=(Atom(derived_field, "READY"),),
        effects={},
        trusted_deterministic=True,
    )
    return PlanVariant(name, (prefix,), commit)


def _single_field_probes(
    fields: tuple[str, ...], *, audit_field: str = "audit_event"
) -> tuple[EvidenceProbe, ...]:
    probes = [EvidenceProbe(f"read_{field}", 1, frozenset({field})) for field in fields]
    probes.append(EvidenceProbe("read_audit_event", 2, frozenset({audit_field})))
    return tuple(probes)


def build_plan_variation_domains() -> tuple[PlanVariationDomain, ...]:
    reservation_atoms = (
        Atom("target_status", "CONFIRMED"),
        Atom("payment_state", "CAPTURED"),
        Atom("other_booking", "UNCHANGED"),
    )
    reservation = PlanVariationDomain(
        name="reservation",
        variants=(
            _derived_variant(
                "full_confirmation", reservation_atoms, "confirmation_ready"
            ),
            _derived_variant(
                "status_notice", (reservation_atoms[0],), "status_notice_ready"
            ),
            _derived_variant(
                "payment_receipt", (reservation_atoms[1],), "receipt_ready"
            ),
            _derived_variant(
                "exclusive_itinerary",
                (reservation_atoms[0], reservation_atoms[2]),
                "itinerary_ready",
            ),
        ),
        probes=_single_field_probes(tuple(atom.field for atom in reservation_atoms)),
        static_domain_atoms=reservation_atoms,
        fixed_target_atom=reservation_atoms[0],
    )

    access_atoms = (
        Atom("target_role", "EDITOR"),
        Atom("scope_state", "PROJECT_ONLY"),
        Atom("other_principal", "UNCHANGED"),
    )
    access = PlanVariationDomain(
        name="access_control",
        variants=(
            _derived_variant("editor_operation", access_atoms, "editor_ready"),
            _derived_variant("role_notice", (access_atoms[0],), "role_notice_ready"),
            _derived_variant(
                "scoped_editor",
                (access_atoms[0], access_atoms[1]),
                "scoped_editor_ready",
            ),
            _derived_variant(
                "isolation_attestation",
                (access_atoms[1], access_atoms[2]),
                "isolation_ready",
            ),
        ),
        probes=_single_field_probes(tuple(atom.field for atom in access_atoms)),
        static_domain_atoms=access_atoms,
        fixed_target_atom=access_atoms[0],
    )

    inventory_atoms = (
        Atom("target_quantity", "PLUS_5"),
        Atom("warehouse_balance", "BALANCED"),
        Atom("other_sku", "UNCHANGED"),
    )
    inventory = PlanVariationDomain(
        name="inventory",
        variants=(
            _derived_variant("publish_restock", inventory_atoms, "restock_ready"),
            _derived_variant(
                "quantity_notice", (inventory_atoms[0],), "quantity_notice_ready"
            ),
            _derived_variant(
                "balanced_restock",
                (inventory_atoms[0], inventory_atoms[1]),
                "balanced_restock_ready",
            ),
            _derived_variant(
                "isolation_attestation",
                (inventory_atoms[1], inventory_atoms[2]),
                "inventory_isolation_ready",
            ),
        ),
        probes=_single_field_probes(tuple(atom.field for atom in inventory_atoms)),
        static_domain_atoms=inventory_atoms,
        fixed_target_atom=inventory_atoms[0],
    )

    document_atoms = (
        Atom("document_signature", "SIGNED"),
        Atom("audience_state", "PUBLIC"),
        Atom("sibling_document", "UNCHANGED"),
        Atom("checksum_state", "MATCH"),
    )
    document = PlanVariationDomain(
        name="document_release",
        variants=(
            _derived_variant("public_release", document_atoms, "public_release_ready"),
            _derived_variant(
                "internal_archive",
                (document_atoms[0], document_atoms[3]),
                "archive_ready",
            ),
            _derived_variant(
                "public_preview",
                (document_atoms[1], document_atoms[3]),
                "preview_ready",
            ),
            _derived_variant(
                "signature_notice", (document_atoms[0],), "signature_notice_ready"
            ),
        ),
        probes=(
            EvidenceProbe(
                "read_document_snapshot",
                2,
                frozenset({"document_signature", "checksum_state"}),
            ),
            EvidenceProbe("read_audience_state", 1, frozenset({"audience_state"})),
            EvidenceProbe(
                "read_sibling_document", 1, frozenset({"sibling_document"})
            ),
            EvidenceProbe(
                "read_document_signature", 1, frozenset({"document_signature"})
            ),
            EvidenceProbe("read_checksum_state", 1, frozenset({"checksum_state"})),
            EvidenceProbe("read_audit_event", 2, frozenset({"audit_event"})),
        ),
        static_domain_atoms=document_atoms,
        fixed_target_atom=document_atoms[0],
    )
    return reservation, access, inventory, document


def validate_plan_variation_domains(
    domains: tuple[PlanVariationDomain, ...],
) -> None:
    for domain in domains:
        variant_names = [variant.name for variant in domain.variants]
        if len(variant_names) != len(set(variant_names)):
            raise ValueError(f"duplicate plan variant: {domain.name}")
        covered = set().union(*(probe.covers for probe in domain.probes))
        static_fields = {atom.field for atom in domain.static_domain_atoms}
        if not static_fields.issubset(covered):
            raise ValueError(f"static contract lacks probe cover: {domain.name}")
        if domain.fixed_target_atom not in domain.static_domain_atoms:
            raise ValueError(f"fixed target is outside static atoms: {domain.name}")
