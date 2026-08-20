from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Mapping, Sequence
from uuid import uuid4

from crl_v3.hypotheses import EVIDENCE_FIDELITIES, HypothesisRecord, SubjectScope
from crl_v3.workspace import _sha256, _validate_utf8_lf, safe_relative_path

if TYPE_CHECKING:
    from crl_v3.knowledge import KnowledgeStore
    from crl_v3.workspace import ResearchWorkspace


SCHEMA_VERSION = 2
SUPPORTED_SCHEMA_VERSIONS = (1, 2)
CLAIM_STATUSES = (
    "proposed",
    "testing",
    "falsified",
    "supported_locally",
    "scope_reduced",
    "unresolved",
)
EXPERIMENT_PURPOSES = (
    "mechanism_consistency",
    "independent_claim_validation",
    "expansion",
)
PARITY_FIELDS = (
    "information_access",
    "tool_capability",
    "model_provider_revision",
    "sampling_protocol",
    "budget",
)
PARITY_STATUSES = ("matched", "different", "unknown")

_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
_CARD_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,127}")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_VERSION = re.compile(r"v\d{3,}")
_PLAN_CREATION_FIELDS = {
    "hypothesis_id",
    "plan_id",
    "claims",
    "global_confounders",
}
_PLAN_FIELDS = _PLAN_CREATION_FIELDS | {
    "schema_version",
    "run_id",
    "version",
    "created_at",
    "updated_at",
}
_CLAIM_FIELDS = {
    "claim_id",
    "claim_text",
    "scope",
    "observable",
    "falsifier",
    "minimum_effect_or_decision_rule",
    "alternative_explanations",
    "killer_experiment_id",
    "supporting_experiment_ids",
    "status",
    "status_reason",
}
_SPEC_CREATION_FIELDS = {
    "experiment_id",
    "hypothesis_id",
    "claim_ids",
    "purpose",
    "research_question",
    "independent_ground_truth",
    "primary_metric",
    "secondary_metrics",
    "sampling_unit",
    "dataset",
    "model",
    "provider",
    "revision",
    "baseline_specs",
    "parity_dimensions",
    "seeds",
    "budget_ceiling",
    "expected_signatures",
    "falsification_rule",
    "confounders",
    "declared_inputs",
    "declared_outputs",
}
_SPEC_V2_FIELDS = _SPEC_CREATION_FIELDS | {
    "evidence_fidelity",
    "subject_scope",
    "independent_implementation_count",
}
_SPEC_FIELDS = _SPEC_CREATION_FIELDS | {"schema_version", "run_id", "version"}
_SPEC_V2_DOCUMENT_FIELDS = _SPEC_V2_FIELDS | {
    "schema_version",
    "run_id",
    "version",
}
_GROUND_TRUTH_FIELDS = {
    "description",
    "external_evidence_ids",
    "external_card_ids",
    "external_literature_refs",
    "run_local_fact_refs",
}
_PARITY_VALUE_FIELDS = {"status", "notes"}

_replace_file = os.replace


@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: str
    claim_text: str
    scope: str
    observable: str
    falsifier: str
    minimum_effect_or_decision_rule: str
    alternative_explanations: tuple[str, ...]
    killer_experiment_id: str
    supporting_experiment_ids: tuple[str, ...]
    status: str
    status_reason: str


@dataclass(frozen=True, slots=True)
class FalsificationPlan:
    schema_version: int
    run_id: str
    version: str
    hypothesis_id: str
    plan_id: str
    claims: tuple[Claim, ...]
    global_confounders: tuple[str, ...]
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class IndependentGroundTruth:
    description: str
    external_evidence_ids: tuple[str, ...]
    external_card_ids: tuple[str, ...]
    external_literature_refs: tuple[str, ...]
    run_local_fact_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ParityDimension:
    status: str
    notes: str


@dataclass(frozen=True, slots=True)
class ExperimentSpec:
    schema_version: int
    run_id: str
    version: str
    experiment_id: str
    hypothesis_id: str
    claim_ids: tuple[str, ...]
    purpose: str
    research_question: str
    independent_ground_truth: IndependentGroundTruth
    primary_metric: str
    secondary_metrics: tuple[str, ...]
    sampling_unit: str
    dataset: str
    model: str
    provider: str
    revision: str
    baseline_specs: tuple[str, ...]
    parity_dimensions: tuple[tuple[str, ParityDimension], ...]
    seeds: tuple[int, ...]
    budget_ceiling: str
    expected_signatures: tuple[str, ...]
    falsification_rule: str
    confounders: tuple[str, ...]
    declared_inputs: tuple[str, ...]
    declared_outputs: tuple[str, ...]
    evidence_fidelity: str | None
    subject_scope: SubjectScope
    independent_implementation_count: int


@dataclass(frozen=True, slots=True)
class FalsificationPlanDocument:
    path: str
    plan: FalsificationPlan
    sha256: str


@dataclass(frozen=True, slots=True)
class ExperimentSpecDocument:
    path: str
    spec: ExperimentSpec
    sha256: str


def create_plan(
    workspace: ResearchWorkspace,
    value: Mapping[str, object],
    *,
    now: str | None = None,
) -> FalsificationPlanDocument:
    workspace.assert_run_writable()
    mapping = _mapping(value, "new falsification plan", _PLAN_CREATION_FIELDS)
    timestamp = now or _utc_now()
    hypothesis_id = _single_line_text(mapping["hypothesis_id"], "hypothesis_id")
    _find_hypothesis(workspace, hypothesis_id)
    plan = plan_from_mapping(
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": workspace.workspace_path.name,
            "version": workspace.version,
            "hypothesis_id": hypothesis_id,
            "plan_id": mapping["plan_id"],
            "claims": mapping["claims"],
            "global_confounders": mapping["global_confounders"],
            "created_at": timestamp,
            "updated_at": timestamp,
        }
    )
    _assert_claim_ids_available(workspace, plan.claims)
    data = plan_to_json_bytes(plan)
    path = plan_path(workspace, plan.plan_id)
    _atomic_publish(workspace, path, data, expected_sha256=None, create_only=True)
    return FalsificationPlanDocument(str(path), plan, _sha256(data))


def add_claim(
    workspace: ResearchWorkspace,
    plan_id: str,
    value: Mapping[str, object],
    *,
    now: str | None = None,
) -> FalsificationPlanDocument:
    document = read_plan(workspace, plan_id)
    claim = claim_from_mapping(_mapping(value, "new claim", _CLAIM_FIELDS))
    _assert_claim_ids_available(workspace, (claim,))
    updated = replace(
        document.plan,
        claims=document.plan.claims + (claim,),
        updated_at=now or _utc_now(),
    )
    validate_plan(
        updated,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
    )
    return write_plan(workspace, updated, expected_sha256=document.sha256)


def update_claim(
    workspace: ResearchWorkspace,
    plan_id: str,
    claim_id: str,
    patch: Mapping[str, object],
    *,
    now: str | None = None,
) -> FalsificationPlanDocument:
    if not isinstance(patch, Mapping) or not patch:
        raise ValueError("claim patch must be a non-empty JSON object")
    unknown = set(patch) - _CLAIM_FIELDS
    if unknown:
        raise ValueError(f"claim patch contains unsupported fields: {sorted(unknown)}")
    if "claim_id" in patch:
        raise ValueError("claim_id is immutable")
    changes_status = "status" in patch
    if changes_status and "status_reason" not in patch:
        raise ValueError("an explicit status change requires status_reason")

    document = read_plan(workspace, plan_id)
    index, current = _find_claim(document.plan, claim_id)
    merged = claim_to_dict(current)
    merged.update(patch)
    replacement_claim = claim_from_mapping(merged)
    claims = list(document.plan.claims)
    claims[index] = replacement_claim
    updated = replace(
        document.plan,
        claims=tuple(claims),
        updated_at=now or _utc_now(),
    )
    validate_plan(
        updated,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
    )
    return write_plan(workspace, updated, expected_sha256=document.sha256)


def write_plan(
    workspace: ResearchWorkspace,
    plan: FalsificationPlan,
    *,
    expected_sha256: str,
) -> FalsificationPlanDocument:
    workspace.assert_run_writable()
    validate_plan(
        plan,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
    )
    _find_hypothesis(workspace, plan.hypothesis_id)
    data = plan_to_json_bytes(plan)
    path = plan_path(workspace, plan.plan_id)
    _atomic_publish(
        workspace,
        path,
        data,
        expected_sha256=expected_sha256,
        create_only=False,
    )
    return FalsificationPlanDocument(str(path), plan, _sha256(data))


def read_plan(workspace: ResearchWorkspace, plan_id: str) -> FalsificationPlanDocument:
    identifier = _identifier(plan_id, "plan_id")
    path = plan_path(workspace, identifier)
    data = workspace.assert_read_target(path).read_bytes()
    _validate_utf8_lf(data, str(path))
    if not data:
        raise ValueError(f"empty falsification plan: {path}")
    try:
        value = json.loads(data)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid falsification plan JSON: {path}") from error
    plan = plan_from_mapping(value)
    validate_plan(
        plan,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
    )
    if plan.plan_id != identifier:
        raise ValueError("falsification plan_id does not match its filename")
    _find_hypothesis(workspace, plan.hypothesis_id)
    return FalsificationPlanDocument(str(path), plan, _sha256(data))


def list_plans(workspace: ResearchWorkspace) -> tuple[FalsificationPlanDocument, ...]:
    root = workspace.assert_write_target(
        workspace.workspace_path / f"hypotheses_{workspace.version}" / "falsification"
    )
    if not root.exists():
        return ()
    if not root.is_dir():
        raise ValueError(f"falsification plan root is not a directory: {root}")
    documents = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if path.name.startswith("."):
            continue
        if path.suffix != ".json":
            raise ValueError(f"unexpected falsification plan file: {path}")
        documents.append(read_plan(workspace, path.stem))
    return tuple(documents)


def create_experiment_spec(
    workspace: ResearchWorkspace,
    value: Mapping[str, object],
) -> ExperimentSpecDocument:
    workspace.assert_run_writable()
    if not isinstance(value, Mapping):
        raise ValueError("new experiment spec must be an object")
    unknown = set(value) - _SPEC_V2_FIELDS
    missing = _SPEC_CREATION_FIELDS - set(value)
    if unknown or missing:
        raise ValueError(
            "new experiment spec fields do not match schema 2: "
            f"missing={sorted(missing)}, unknown={sorted(unknown)}"
        )
    mapping = dict(value)
    mapping.setdefault("evidence_fidelity", "SCREENING")
    mapping.setdefault(
        "subject_scope",
        {
            "models": [str(mapping["model"])],
            "tasks": [str(mapping["research_question"])],
            "datasets": [str(mapping["dataset"])],
            "seeds": [str(item) for item in mapping["seeds"]]
            if isinstance(mapping["seeds"], list)
            else [],
            "environment": f"{mapping['provider']} / {mapping['revision']}",
        },
    )
    mapping.setdefault("independent_implementation_count", 1)
    spec = experiment_spec_from_mapping(
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": workspace.workspace_path.name,
            "version": workspace.version,
            **mapping,
        }
    )
    _find_hypothesis(workspace, spec.hypothesis_id)
    claims = _claim_index(list_plans(workspace))
    _validate_spec_claims(spec, claims)
    _validate_external_evidence(spec.independent_ground_truth, workspace.knowledge_store)
    data = experiment_spec_to_json_bytes(spec)
    path = experiment_spec_path(workspace, spec.experiment_id)
    _atomic_publish(workspace, path, data, expected_sha256=None, create_only=True)
    return ExperimentSpecDocument(str(path), spec, _sha256(data))


def read_experiment_spec(
    workspace: ResearchWorkspace, experiment_id: str
) -> ExperimentSpecDocument:
    identifier = _identifier(experiment_id, "experiment_id")
    path = experiment_spec_path(workspace, identifier)
    data = workspace.assert_read_target(path).read_bytes()
    _validate_utf8_lf(data, str(path))
    if not data:
        raise ValueError(f"empty experiment spec: {path}")
    try:
        value = json.loads(data)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid experiment spec JSON: {path}") from error
    spec = experiment_spec_from_mapping(value)
    validate_experiment_spec(
        spec,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
    )
    if spec.experiment_id != identifier:
        raise ValueError("experiment_id does not match its filename")
    _find_hypothesis(workspace, spec.hypothesis_id)
    _validate_external_evidence(spec.independent_ground_truth, workspace.knowledge_store)
    return ExperimentSpecDocument(str(path), spec, _sha256(data))


def list_experiment_specs(
    workspace: ResearchWorkspace,
) -> tuple[ExperimentSpecDocument, ...]:
    root = workspace.assert_write_target(workspace.experiment_path / "specs")
    if not root.exists():
        return ()
    if not root.is_dir():
        raise ValueError(f"experiment spec root is not a directory: {root}")
    documents = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if path.name.startswith("."):
            continue
        if path.suffix != ".json":
            raise ValueError(f"unexpected experiment spec file: {path}")
        documents.append(read_experiment_spec(workspace, path.stem))
    return tuple(documents)


def validate_repository(workspace: ResearchWorkspace) -> dict[str, int]:
    plans = list_plans(workspace)
    specs = list_experiment_specs(workspace)
    claims = _claim_index(plans)
    for spec_document in specs:
        _validate_spec_claims(spec_document.spec, claims)
    experiment_ids = {item.spec.experiment_id for item in specs}
    for plan_document in plans:
        for claim in plan_document.plan.claims:
            referenced = (claim.killer_experiment_id,) + claim.supporting_experiment_ids
            missing = sorted(set(referenced) - experiment_ids)
            if missing:
                raise KeyError(
                    f"claim {claim.claim_id!r} references unknown experiment ids: {missing}"
                )
    return {
        "schema_version": SCHEMA_VERSION,
        "plan_count": len(plans),
        "claim_count": len(claims),
        "experiment_spec_count": len(specs),
    }


def plan_from_mapping(value: object) -> FalsificationPlan:
    mapping = _mapping(value, "falsification plan", _PLAN_FIELDS)
    schema_version = mapping["schema_version"]
    if type(schema_version) is not int or schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError("unsupported falsification plan schema version")
    claims = mapping["claims"]
    if not isinstance(claims, list):
        raise ValueError("claims must be an array")
    return FalsificationPlan(
        schema_version=schema_version,
        run_id=_identifier(mapping["run_id"], "run_id"),
        version=_version(mapping["version"]),
        hypothesis_id=_single_line_text(mapping["hypothesis_id"], "hypothesis_id"),
        plan_id=_identifier(mapping["plan_id"], "plan_id"),
        claims=tuple(claim_from_mapping(item) for item in claims),
        global_confounders=_string_array(
            mapping["global_confounders"], "global_confounders"
        ),
        created_at=_timestamp(mapping["created_at"], "created_at"),
        updated_at=_timestamp(mapping["updated_at"], "updated_at"),
    )


def claim_from_mapping(value: object) -> Claim:
    mapping = _mapping(value, "claim", _CLAIM_FIELDS)
    status = mapping["status"]
    if not isinstance(status, str) or status not in CLAIM_STATUSES:
        raise ValueError(f"invalid claim status: {status!r}")
    return Claim(
        claim_id=_identifier(mapping["claim_id"], "claim_id"),
        claim_text=_required_text(mapping["claim_text"], "claim_text"),
        scope=_required_text(mapping["scope"], "scope"),
        observable=_required_text(mapping["observable"], "observable"),
        falsifier=_required_text(mapping["falsifier"], "falsifier"),
        minimum_effect_or_decision_rule=_required_text(
            mapping["minimum_effect_or_decision_rule"],
            "minimum_effect_or_decision_rule",
        ),
        alternative_explanations=_string_array(
            mapping["alternative_explanations"], "alternative_explanations"
        ),
        killer_experiment_id=_identifier(
            mapping["killer_experiment_id"], "killer_experiment_id"
        ),
        supporting_experiment_ids=_identifier_array(
            mapping["supporting_experiment_ids"], "supporting_experiment_ids"
        ),
        status=status,
        status_reason=_required_text(mapping["status_reason"], "status_reason"),
    )


def validate_plan(
    plan: FalsificationPlan,
    *,
    expected_run_id: str | None = None,
    expected_version: str | None = None,
) -> None:
    canonical = plan_from_mapping(plan_to_dict(plan))
    if canonical != plan:
        raise ValueError("falsification plan dataclass values do not match its schema")
    if expected_run_id is not None and plan.run_id != expected_run_id:
        raise ValueError("falsification plan run_id does not match the bound Run")
    if expected_version is not None and plan.version != expected_version:
        raise ValueError("falsification plan version does not match workspace version")
    if _parse_timestamp(plan.updated_at, "updated_at") < _parse_timestamp(
        plan.created_at, "created_at"
    ):
        raise ValueError("falsification plan updated_at precedes created_at")
    claim_ids = [item.claim_id for item in plan.claims]
    if len(claim_ids) != len(set(claim_ids)):
        raise ValueError("claim_id values must be unique")


def experiment_spec_from_mapping(value: object) -> ExperimentSpec:
    if not isinstance(value, dict):
        raise ValueError("experiment spec must be an object")
    schema_version = value.get("schema_version")
    if type(schema_version) is not int or schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError("unsupported experiment spec schema version")
    fields = _SPEC_V2_DOCUMENT_FIELDS if schema_version == 2 else _SPEC_FIELDS
    mapping = _mapping(value, "experiment spec", fields)
    purpose = mapping["purpose"]
    if not isinstance(purpose, str) or purpose not in EXPERIMENT_PURPOSES:
        raise ValueError(f"invalid experiment purpose: {purpose!r}")
    ground_truth = _mapping(
        mapping["independent_ground_truth"],
        "independent_ground_truth",
        _GROUND_TRUTH_FIELDS,
    )
    parity = _mapping(
        mapping["parity_dimensions"], "parity_dimensions", set(PARITY_FIELDS)
    )
    parity_values: list[tuple[str, ParityDimension]] = []
    for name in PARITY_FIELDS:
        item = _mapping(parity[name], f"parity_dimensions.{name}", _PARITY_VALUE_FIELDS)
        parity_status = item["status"]
        if not isinstance(parity_status, str) or parity_status not in PARITY_STATUSES:
            raise ValueError(
                f"invalid parity status for {name}: {parity_status!r}"
            )
        parity_values.append(
            (
                name,
                ParityDimension(
                    status=parity_status,
                    notes=_required_text(item["notes"], f"parity_dimensions.{name}.notes"),
                ),
            )
        )
    if schema_version == 2:
        fidelity = mapping["evidence_fidelity"]
        if fidelity is not None and fidelity not in EVIDENCE_FIDELITIES:
            raise ValueError(f"invalid evidence_fidelity: {fidelity!r}")
        scope_mapping = _mapping(
            mapping["subject_scope"],
            "subject_scope",
            {"models", "tasks", "datasets", "seeds", "environment"},
        )
        subject_scope = SubjectScope(
            models=_string_array(scope_mapping["models"], "subject_scope.models"),
            tasks=_string_array(scope_mapping["tasks"], "subject_scope.tasks"),
            datasets=_string_array(
                scope_mapping["datasets"], "subject_scope.datasets"
            ),
            seeds=_string_array(scope_mapping["seeds"], "subject_scope.seeds"),
            environment=_optional_text(
                scope_mapping["environment"], "subject_scope.environment"
            ),
        )
        independent_count = _nonnegative_integer(
            mapping["independent_implementation_count"],
            "independent_implementation_count",
        )
    else:
        fidelity = None
        subject_scope = SubjectScope((), (), (), (), "")
        independent_count = 0
    return ExperimentSpec(
        schema_version=schema_version,
        run_id=_identifier(mapping["run_id"], "run_id"),
        version=_version(mapping["version"]),
        experiment_id=_identifier(mapping["experiment_id"], "experiment_id"),
        hypothesis_id=_single_line_text(mapping["hypothesis_id"], "hypothesis_id"),
        claim_ids=_identifier_array(mapping["claim_ids"], "claim_ids", required=True),
        purpose=purpose,
        research_question=_required_text(
            mapping["research_question"], "research_question"
        ),
        independent_ground_truth=IndependentGroundTruth(
            description=_required_text(ground_truth["description"], "independent_ground_truth.description"),
            external_evidence_ids=_string_array(
                ground_truth["external_evidence_ids"],
                "independent_ground_truth.external_evidence_ids",
            ),
            external_card_ids=_card_id_array(
                ground_truth["external_card_ids"],
                "independent_ground_truth.external_card_ids",
            ),
            external_literature_refs=_string_array(
                ground_truth["external_literature_refs"],
                "independent_ground_truth.external_literature_refs",
            ),
            run_local_fact_refs=_relative_path_array(
                ground_truth["run_local_fact_refs"],
                "independent_ground_truth.run_local_fact_refs",
            ),
        ),
        primary_metric=_required_text(mapping["primary_metric"], "primary_metric"),
        secondary_metrics=_string_array(
            mapping["secondary_metrics"], "secondary_metrics"
        ),
        sampling_unit=_required_text(mapping["sampling_unit"], "sampling_unit"),
        dataset=_required_text(mapping["dataset"], "dataset"),
        model=_required_text(mapping["model"], "model"),
        provider=_required_text(mapping["provider"], "provider"),
        revision=_required_text(mapping["revision"], "revision"),
        baseline_specs=_string_array(mapping["baseline_specs"], "baseline_specs"),
        parity_dimensions=tuple(parity_values),
        seeds=_seed_array(mapping["seeds"]),
        budget_ceiling=_required_text(mapping["budget_ceiling"], "budget_ceiling"),
        expected_signatures=_string_array(
            mapping["expected_signatures"], "expected_signatures"
        ),
        falsification_rule=_required_text(
            mapping["falsification_rule"], "falsification_rule"
        ),
        confounders=_string_array(mapping["confounders"], "confounders"),
        declared_inputs=_relative_path_array(
            mapping["declared_inputs"], "declared_inputs"
        ),
        declared_outputs=_relative_path_array(
            mapping["declared_outputs"], "declared_outputs"
        ),
        evidence_fidelity=fidelity,
        subject_scope=subject_scope,
        independent_implementation_count=independent_count,
    )


def validate_experiment_spec(
    spec: ExperimentSpec,
    *,
    expected_run_id: str | None = None,
    expected_version: str | None = None,
) -> None:
    canonical = experiment_spec_from_mapping(experiment_spec_to_dict(spec))
    if canonical != spec:
        raise ValueError("experiment spec dataclass values do not match its schema")
    if expected_run_id is not None and spec.run_id != expected_run_id:
        raise ValueError("experiment spec run_id does not match the bound Run")
    if expected_version is not None and spec.version != expected_version:
        raise ValueError("experiment spec version does not match workspace version")
    overlap = set(spec.declared_inputs) & set(spec.declared_outputs)
    if overlap:
        raise ValueError(f"declared inputs and outputs overlap: {sorted(overlap)}")


def experiment_spec_warning_codes(spec: ExperimentSpec) -> tuple[str, ...]:
    """Return advisory field-combination warnings without judging sufficiency."""
    if spec.evidence_fidelity != "REPRESENTATIVE":
        return ()
    scope = spec.subject_scope
    if any(
        (
            scope.models,
            scope.tasks,
            scope.datasets,
            scope.seeds,
            scope.environment,
        )
    ):
        return ()
    return ("representative_subject_scope_empty",)


def plan_to_dict(plan: FalsificationPlan) -> dict[str, object]:
    if type(plan) is not FalsificationPlan or type(plan.claims) is not tuple:
        raise ValueError("plan must be a FalsificationPlan with tuple claims")
    return {
        "schema_version": plan.schema_version,
        "run_id": plan.run_id,
        "version": plan.version,
        "hypothesis_id": plan.hypothesis_id,
        "plan_id": plan.plan_id,
        "claims": [claim_to_dict(item) for item in plan.claims],
        "global_confounders": list(plan.global_confounders),
        "created_at": plan.created_at,
        "updated_at": plan.updated_at,
    }


def claim_to_dict(claim: Claim) -> dict[str, object]:
    if type(claim) is not Claim:
        raise ValueError("claim must be a Claim")
    return {
        "claim_id": claim.claim_id,
        "claim_text": claim.claim_text,
        "scope": claim.scope,
        "observable": claim.observable,
        "falsifier": claim.falsifier,
        "minimum_effect_or_decision_rule": claim.minimum_effect_or_decision_rule,
        "alternative_explanations": list(claim.alternative_explanations),
        "killer_experiment_id": claim.killer_experiment_id,
        "supporting_experiment_ids": list(claim.supporting_experiment_ids),
        "status": claim.status,
        "status_reason": claim.status_reason,
    }


def experiment_spec_to_dict(spec: ExperimentSpec) -> dict[str, object]:
    if type(spec) is not ExperimentSpec:
        raise ValueError("spec must be an ExperimentSpec")
    parity = dict(spec.parity_dimensions)
    mapping: dict[str, object] = {
        "schema_version": spec.schema_version,
        "run_id": spec.run_id,
        "version": spec.version,
        "experiment_id": spec.experiment_id,
        "hypothesis_id": spec.hypothesis_id,
        "claim_ids": list(spec.claim_ids),
        "purpose": spec.purpose,
        "research_question": spec.research_question,
        "independent_ground_truth": {
            "description": spec.independent_ground_truth.description,
            "external_evidence_ids": list(
                spec.independent_ground_truth.external_evidence_ids
            ),
            "external_card_ids": list(spec.independent_ground_truth.external_card_ids),
            "external_literature_refs": list(
                spec.independent_ground_truth.external_literature_refs
            ),
            "run_local_fact_refs": list(
                spec.independent_ground_truth.run_local_fact_refs
            ),
        },
        "primary_metric": spec.primary_metric,
        "secondary_metrics": list(spec.secondary_metrics),
        "sampling_unit": spec.sampling_unit,
        "dataset": spec.dataset,
        "model": spec.model,
        "provider": spec.provider,
        "revision": spec.revision,
        "baseline_specs": list(spec.baseline_specs),
        "parity_dimensions": {
            name: {"status": parity[name].status, "notes": parity[name].notes}
            for name in PARITY_FIELDS
        },
        "seeds": list(spec.seeds),
        "budget_ceiling": spec.budget_ceiling,
        "expected_signatures": list(spec.expected_signatures),
        "falsification_rule": spec.falsification_rule,
        "confounders": list(spec.confounders),
        "declared_inputs": list(spec.declared_inputs),
        "declared_outputs": list(spec.declared_outputs),
    }
    if spec.schema_version == 2:
        mapping.update(
            {
                "evidence_fidelity": spec.evidence_fidelity,
                "subject_scope": {
                    "models": list(spec.subject_scope.models),
                    "tasks": list(spec.subject_scope.tasks),
                    "datasets": list(spec.subject_scope.datasets),
                    "seeds": list(spec.subject_scope.seeds),
                    "environment": spec.subject_scope.environment,
                },
                "independent_implementation_count": (
                    spec.independent_implementation_count
                ),
            }
        )
    return mapping


def plan_to_json_bytes(plan: FalsificationPlan) -> bytes:
    validate_plan(plan)
    return _json_bytes(plan_to_dict(plan))


def experiment_spec_to_json_bytes(spec: ExperimentSpec) -> bytes:
    validate_experiment_spec(spec)
    return _json_bytes(experiment_spec_to_dict(spec))


def plan_path(workspace: ResearchWorkspace, plan_id: str) -> Path:
    identifier = _identifier(plan_id, "plan_id")
    return (
        workspace.workspace_path
        / f"hypotheses_{workspace.version}"
        / "falsification"
        / f"{identifier}.json"
    )


def experiment_spec_path(workspace: ResearchWorkspace, experiment_id: str) -> Path:
    identifier = _identifier(experiment_id, "experiment_id")
    return workspace.experiment_path / "specs" / f"{identifier}.json"


def render_plan_markdown(
    plan: FalsificationPlan,
    *,
    hypothesis: HypothesisRecord,
    specs: Sequence[ExperimentSpec],
) -> str:
    validate_plan(plan)
    if hypothesis.hypothesis_id != plan.hypothesis_id:
        raise ValueError("render hypothesis does not match falsification plan")
    spec_index = {item.experiment_id: item for item in specs}
    if len(spec_index) != len(specs):
        raise ValueError("render experiment specs contain duplicate experiment IDs")
    lines = [
        f"# Claim—Falsifier—Experiment 反证计划 `{plan.plan_id}`",
        "",
        "> Run-local 透明研究记录；不是科研评分、Claim 自动裁决、Seed、Delivery 或交付 Gate。",
        "",
        f"- Run：`{plan.run_id}`",
        f"- 科学版本：`{plan.version}`",
        f"- 假设：`{plan.hypothesis_id}`",
        f"- 创建时间：`{plan.created_at}`",
        f"- 更新时间：`{plan.updated_at}`",
        "",
        "## 权威来源分离",
        "",
        "### 外部论文权威（不等同于 Run-local 实验事实）",
        "",
        f"- Evidence IDs：{_render_code_items(hypothesis.target_failure.evidence_ids)}",
        f"- Card IDs：{_render_code_items(hypothesis.target_failure.card_ids)}",
        f"- Literature refs：{_render_items(hypothesis.literature_refs)}",
        "",
        "### 全局混淆因素",
        "",
        _render_items(plan.global_confounders),
        "",
    ]
    for claim in plan.claims:
        killer = spec_index.get(claim.killer_experiment_id)
        lines.extend(
            [
                f"## Claim `{claim.claim_id}`",
                "",
                f"- 显式状态：`{claim.status}`",
                f"- 状态理由：{claim.status_reason}",
                f"- Claim：{claim.claim_text}",
                f"- 适用范围：{claim.scope}",
                f"- 可观测量：{claim.observable}",
                "",
                "### 什么结果会杀死该 Claim",
                "",
                f"- 反证条件：{claim.falsifier}",
                f"- 最小效应或决策规则：{claim.minimum_effect_or_decision_rule}",
                "",
                "### 主研究者声明的最便宜 killer experiment",
                "",
                f"- 实验 ID：`{claim.killer_experiment_id}`",
            ]
        )
        if killer is None:
            lines.extend(
                [
                    "- 规范：尚未在当前版本注册",
                    "- 独立真值来源：尚未在当前版本注册",
                    "- 预算上限：尚未在当前版本注册",
                    "- 预算公平性未知项：尚未在当前版本注册",
                    "",
                ]
            )
        else:
            parity = dict(killer.parity_dimensions)
            unknown = [name for name in PARITY_FIELDS if parity[name].status == "unknown"]
            ground = killer.independent_ground_truth
            lines.extend(
                [
                    f"- 目的：`{killer.purpose}`",
                    f"- 证据保真度：`{killer.evidence_fidelity or 'LEGACY_UNSPECIFIED'}`",
                    f"- 独立实现数：{killer.independent_implementation_count}",
                    f"- 模型范围：{_render_items(killer.subject_scope.models)}",
                    f"- 任务范围：{_render_items(killer.subject_scope.tasks)}",
                    f"- 数据集范围：{_render_items(killer.subject_scope.datasets)}",
                    f"- 种子范围：{_render_items(killer.subject_scope.seeds)}",
                    f"- 环境范围：{killer.subject_scope.environment or '(legacy unspecified)'}",
                    f"- 研究问题：{killer.research_question}",
                    f"- 主指标：{killer.primary_metric}",
                    f"- 独立真值说明：{ground.description}",
                    f"- 真值的外部 Evidence：{_render_code_items(ground.external_evidence_ids)}",
                    f"- 真值的外部 Card：{_render_code_items(ground.external_card_ids)}",
                    f"- 真值的外部 literature refs：{_render_items(ground.external_literature_refs)}",
                    f"- 真值的 Run-local 事实路径：{_render_code_items(ground.run_local_fact_refs)}",
                    f"- 预算上限：{killer.budget_ceiling}",
                    f"- 预算公平性未知项：{_render_code_items(unknown)}",
                    "",
                    "#### 公平性声明",
                    "",
                    "| 维度 | 显式状态 | 说明 |",
                    "| --- | --- | --- |",
                ]
            )
            for name in PARITY_FIELDS:
                lines.append(f"| `{name}` | `{parity[name].status}` | {parity[name].notes} |")
            lines.append("")
        lines.extend(
            [
                "### 替代解释与 Run-local 支持",
                "",
                f"- 替代解释：{_render_items(claim.alternative_explanations)}",
                f"- Run-local supporting experiment IDs：{_render_code_items(claim.supporting_experiment_ids)}",
                "- 权威说明：上述 Run-local 标识不等同于外部论文 Evidence/Card；工具也不据此自动改变 Claim 状态。",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _claim_index(
    plans: Sequence[FalsificationPlanDocument],
) -> dict[str, tuple[str, Claim]]:
    result: dict[str, tuple[str, Claim]] = {}
    for document in plans:
        for claim in document.plan.claims:
            if claim.claim_id in result:
                raise ValueError(
                    f"claim_id appears in multiple falsification plans: {claim.claim_id}"
                )
            result[claim.claim_id] = (document.plan.hypothesis_id, claim)
    return result


def _validate_spec_claims(
    spec: ExperimentSpec, claims: Mapping[str, tuple[str, Claim]]
) -> None:
    unknown = sorted(set(spec.claim_ids) - set(claims))
    if unknown:
        raise KeyError(f"experiment spec references unknown claim ids: {unknown}")
    mismatched = sorted(
        claim_id
        for claim_id in spec.claim_ids
        if claims[claim_id][0] != spec.hypothesis_id
    )
    if mismatched:
        raise ValueError(
            "experiment spec claim ids belong to another hypothesis: "
            f"{mismatched}"
        )


def _assert_claim_ids_available(
    workspace: ResearchWorkspace, claims: Sequence[Claim]
) -> None:
    existing = _claim_index(list_plans(workspace))
    incoming = [item.claim_id for item in claims]
    if len(incoming) != len(set(incoming)):
        raise ValueError("claim_id values must be unique")
    duplicate = sorted(set(incoming) & set(existing))
    if duplicate:
        raise ValueError(f"claim_id already exists in this Run version: {duplicate}")


def _find_hypothesis(
    workspace: ResearchWorkspace, hypothesis_id: str
) -> HypothesisRecord:
    document = workspace.read_hypotheses(required=True)
    assert document is not None
    matches = [
        item for item in document.portfolio.hypotheses if item.hypothesis_id == hypothesis_id
    ]
    if not matches:
        raise KeyError(f"unknown hypothesis id: {hypothesis_id}")
    return matches[0]


def _find_claim(plan: FalsificationPlan, claim_id: str) -> tuple[int, Claim]:
    identifier = _identifier(claim_id, "claim_id")
    matches = [
        (index, item)
        for index, item in enumerate(plan.claims)
        if item.claim_id == identifier
    ]
    if not matches:
        raise KeyError(f"unknown claim id: {identifier}")
    return matches[0]


def _validate_external_evidence(
    ground_truth: IndependentGroundTruth, knowledge_store: KnowledgeStore | None
) -> None:
    if ground_truth.external_evidence_ids and knowledge_store is None:
        raise ValueError("a KnowledgeStore is required when external Evidence IDs are supplied")
    for evidence_id in ground_truth.external_evidence_ids:
        assert knowledge_store is not None
        evidence = knowledge_store.get_evidence(evidence_id)
        if evidence is None:
            raise KeyError(f"unknown evidence id: {evidence_id}")
        if not evidence.fulltext_is_current or evidence.passage_is_current is False:
            raise ValueError(f"Evidence is not current: {evidence_id}")


def _atomic_publish(
    workspace: ResearchWorkspace,
    path: Path,
    data: bytes,
    *,
    expected_sha256: str | None,
    create_only: bool,
) -> None:
    workspace.assert_run_writable()
    target = workspace.assert_write_target(path)
    parent = workspace.assert_write_target(target.parent)
    parent.mkdir(parents=True, exist_ok=True)
    workspace.assert_write_target(target)
    lock = target.with_name(f".{target.name}.lock")
    workspace.assert_write_target(lock)
    try:
        with lock.open("xb"):
            pass
    except FileExistsError as error:
        raise FileExistsError("another falsification document write is in progress") from error
    temporary = target.with_name(f".{target.name}.{uuid4().hex}.tmp")
    try:
        exists = target.exists() or target.is_symlink()
        if create_only:
            if exists:
                raise FileExistsError(f"falsification document already exists: {target}")
            if expected_sha256 is not None:
                raise ValueError("create-only write cannot have expected_sha256")
        else:
            if not isinstance(expected_sha256, str) or _SHA256.fullmatch(expected_sha256) is None:
                raise ValueError("document update requires its previously read SHA-256")
            current = workspace.assert_read_target(target).read_bytes()
            if _sha256(current) != expected_sha256:
                raise FileExistsError("falsification document changed since it was read")
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        workspace.assert_write_target(target)
        if create_only:
            try:
                os.link(temporary, target)
            except FileExistsError as error:
                raise FileExistsError(
                    "falsification document was concurrently created"
                ) from error
        else:
            current = workspace.assert_read_target(target).read_bytes()
            if _sha256(current) != expected_sha256:
                raise FileExistsError("falsification document changed during update")
            _replace_file(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
        if lock.exists() and not lock.is_symlink():
            lock.unlink()


def _mapping(value: object, label: str, fields: set[str]) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"{label} fields do not match schema 1")
    return value


def _identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise ValueError(f"{label} must be a safe identifier")
    return value


def _single_line_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ValueError(f"{label} must be non-empty single-line text")
    return value.strip()


def _version(value: object) -> str:
    if not isinstance(value, str) or _VERSION.fullmatch(value) is None:
        raise ValueError(f"invalid falsification version: {value!r}")
    return value


def _required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\r" in value:
        raise ValueError(f"{label} must be non-empty text with LF newlines")
    if value.startswith("\ufeff"):
        raise ValueError(f"{label} must not begin with a BOM marker")
    return value.strip()


def _optional_text(value: object, label: str) -> str:
    if not isinstance(value, str) or "\r" in value:
        raise ValueError(f"{label} must be text with LF newlines")
    if value.startswith("\ufeff"):
        raise ValueError(f"{label} must not begin with a BOM marker")
    return value.strip()


def _nonnegative_integer(value: object, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def _string_array(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a string array")
    items = tuple(_required_text(item, label) for item in value)
    if len(items) != len(set(items)):
        raise ValueError(f"{label} must not contain duplicates")
    return items


def _identifier_array(
    value: object, label: str, *, required: bool = False
) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an identifier array")
    items = tuple(_identifier(item, label) for item in value)
    if required and not items:
        raise ValueError(f"{label} must not be empty")
    if len(items) != len(set(items)):
        raise ValueError(f"{label} must not contain duplicates")
    return items


def _card_id_array(value: object, label: str) -> tuple[str, ...]:
    items = _string_array(value, label)
    for item in items:
        if _CARD_ID.fullmatch(item) is None:
            raise ValueError(f"{label} contains invalid Card ID: {item!r}")
    return items


def _relative_path_array(value: object, label: str) -> tuple[str, ...]:
    items = _string_array(value, label)
    normalized = tuple(safe_relative_path(item).as_posix() for item in items)
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{label} must not contain duplicate normalized paths")
    return normalized


def _seed_array(value: object) -> tuple[int, ...]:
    if not isinstance(value, list):
        raise ValueError("seeds must be an integer array")
    if any(type(item) is not int or item < 0 for item in value):
        raise ValueError("seeds must contain non-negative integers")
    if len(value) != len(set(value)):
        raise ValueError("seeds must not contain duplicates")
    return tuple(value)


def _timestamp(value: object, label: str) -> str:
    _parse_timestamp(value, label)
    assert isinstance(value, str)
    return value


def _parse_timestamp(value: object, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{label} must be an ISO-8601 UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError(f"{label} must be an ISO-8601 UTC timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise ValueError(f"{label} must be UTC")
    return parsed


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def _render_items(items: Sequence[str]) -> str:
    return "；".join(items) if items else "（无）"


def _render_code_items(items: Sequence[str]) -> str:
    return "、".join(f"`{item}`" for item in items) if items else "（无）"
