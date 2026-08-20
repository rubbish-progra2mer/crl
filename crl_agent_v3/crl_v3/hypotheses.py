from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Mapping, Sequence
from uuid import uuid4

from crl_v3.workspace import _sha256, _validate_utf8_lf

if TYPE_CHECKING:
    from crl_v3.knowledge import KnowledgeStore
    from crl_v3.workspace import ResearchWorkspace


SCHEMA_VERSION = 2
SUPPORTED_SCHEMA_VERSIONS = (1, 2)
HYPOTHESIS_STATUSES = (
    "draft",
    "active",
    "falsified",
    "prior_collision",
    "parked",
    "escalated",
)

_CARD_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,127}")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_RECORD_FIELDS = {
    "hypothesis_id",
    "title",
    "status",
    "status_reason",
    "parent_ids",
    "lineage_note",
    "problem",
    "target_failure",
    "changed_computation",
    "mechanism_claim",
    "falsifier",
    "minimal_killer_experiment",
    "nearest_prior_risk",
    "alternative_explanations",
    "descriptors",
    "literature_refs",
    "created_at_utc",
    "updated_at_utc",
    "revision",
}
_RECORD_V2_FIELDS = _RECORD_FIELDS | {"decision_history"}
_CREATION_FIELDS = _RECORD_FIELDS - {
    "status_reason",
    "created_at_utc",
    "updated_at_utc",
    "revision",
}
_IMMUTABLE_PATCH_FIELDS = {
    "hypothesis_id",
    "status",
    "status_reason",
    "created_at_utc",
    "updated_at_utc",
    "revision",
    "decision_history",
}
_PORTFOLIO_FIELDS = {
    "schema_version",
    "run_id",
    "version",
    "revision",
    "created_at_utc",
    "updated_at_utc",
    "hypotheses",
}

_replace_file = os.replace

EVIDENCE_FIDELITIES = ("SCREENING", "REPRESENTATIVE")
KILL_TARGETS = (
    "IMPLEMENTATION",
    "LOCAL_EMPIRICAL_CLAIM",
    "METHOD_CORE",
    "PAPER_DIRECTION",
)
DECISION_REQUIRED_STATUSES = {"falsified", "prior_collision", "escalated"}
_SUBJECT_SCOPE_FIELDS = {"models", "tasks", "datasets", "seeds", "environment"}
_DECISION_INPUT_FIELDS = {
    "evidence_fidelity",
    "kill_target",
    "subject_scope",
    "independent_implementation_count",
    "structural_refutation",
    "structural_refutation_reason",
    "killed",
    "survives",
    "why",
}
_DECISION_EVENT_FIELDS = _DECISION_INPUT_FIELDS | {
    "from_status",
    "to_status",
    "reason",
    "decided_at_utc",
}


@dataclass(frozen=True, slots=True)
class TargetFailure:
    summary: str
    card_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ChangedComputation:
    baseline: str
    intervention: str
    information_available: str
    timing: str
    budget_effect: str


@dataclass(frozen=True, slots=True)
class HypothesisDescriptors:
    problem_family: str
    computation_stage: str
    intervention_family: str
    information_source: str
    timing_class: str
    budget_class: str
    evaluation_mode: str


@dataclass(frozen=True, slots=True)
class SubjectScope:
    models: tuple[str, ...]
    tasks: tuple[str, ...]
    datasets: tuple[str, ...]
    seeds: tuple[str, ...]
    environment: str


@dataclass(frozen=True, slots=True)
class HypothesisDecision:
    from_status: str
    to_status: str
    reason: str
    decided_at_utc: str
    evidence_fidelity: str | None
    kill_target: str | None
    subject_scope: SubjectScope
    independent_implementation_count: int
    structural_refutation: bool
    structural_refutation_reason: str
    killed: str
    survives: str
    why: str


@dataclass(frozen=True, slots=True)
class HypothesisRecord:
    hypothesis_id: str
    title: str
    status: str
    status_reason: str
    parent_ids: tuple[str, ...]
    lineage_note: str
    problem: str
    target_failure: TargetFailure
    changed_computation: ChangedComputation
    mechanism_claim: str
    falsifier: str
    minimal_killer_experiment: str
    nearest_prior_risk: str
    alternative_explanations: tuple[str, ...]
    descriptors: HypothesisDescriptors
    literature_refs: tuple[str, ...]
    created_at_utc: str
    updated_at_utc: str
    revision: int
    decision_history: tuple[HypothesisDecision, ...]


@dataclass(frozen=True, slots=True)
class HypothesisPortfolio:
    schema_version: int
    run_id: str
    version: str
    revision: int
    created_at_utc: str
    updated_at_utc: str
    hypotheses: tuple[HypothesisRecord, ...]


@dataclass(frozen=True, slots=True)
class HypothesisPortfolioDocument:
    path: str
    portfolio: HypothesisPortfolio
    sha256: str


def empty_portfolio(run_id: str, version: str, *, now: str | None = None) -> HypothesisPortfolio:
    timestamp = now or _utc_now()
    _timestamp(timestamp, "portfolio timestamp")
    return HypothesisPortfolio(
        schema_version=SCHEMA_VERSION,
        run_id=_text(run_id, "run_id"),
        version=_version(version),
        revision=0,
        created_at_utc=timestamp,
        updated_at_utc=timestamp,
        hypotheses=(),
    )


def create_hypothesis_record(
    value: Mapping[str, object], *, now: str | None = None
) -> HypothesisRecord:
    if not isinstance(value, Mapping):
        raise ValueError("new hypothesis must be a JSON object")
    unknown = set(value) - _CREATION_FIELDS
    if unknown:
        raise ValueError(f"new hypothesis contains unsupported fields: {sorted(unknown)}")
    if "hypothesis_id" not in value:
        raise ValueError("new hypothesis requires hypothesis_id")
    supplied_status = value.get("status", "draft")
    if supplied_status != "draft":
        raise ValueError("new hypotheses begin as draft; use transition to change status")
    timestamp = now or _utc_now()
    normalized: dict[str, object] = {
        "hypothesis_id": value.get("hypothesis_id"),
        "title": value.get("title", ""),
        "status": "draft",
        "status_reason": "",
        "parent_ids": value.get("parent_ids", []),
        "lineage_note": value.get("lineage_note", ""),
        "problem": value.get("problem", ""),
        "target_failure": value.get(
            "target_failure", {"summary": "", "card_ids": [], "evidence_ids": []}
        ),
        "changed_computation": value.get(
            "changed_computation",
            {
                "baseline": "",
                "intervention": "",
                "information_available": "",
                "timing": "",
                "budget_effect": "",
            },
        ),
        "mechanism_claim": value.get("mechanism_claim", ""),
        "falsifier": value.get("falsifier", ""),
        "minimal_killer_experiment": value.get("minimal_killer_experiment", ""),
        "nearest_prior_risk": value.get("nearest_prior_risk", ""),
        "alternative_explanations": value.get("alternative_explanations", []),
        "descriptors": value.get(
            "descriptors",
            {
                "problem_family": "",
                "computation_stage": "",
                "intervention_family": "",
                "information_source": "",
                "timing_class": "",
                "budget_class": "",
                "evaluation_mode": "",
            },
        ),
        "literature_refs": value.get("literature_refs", []),
        "created_at_utc": timestamp,
        "updated_at_utc": timestamp,
        "revision": 1,
        "decision_history": [],
    }
    return _record_from_mapping(normalized, schema_version=2)


def add_hypothesis(
    portfolio: HypothesisPortfolio,
    record: HypothesisRecord,
    *,
    knowledge_store: KnowledgeStore | None = None,
    now: str | None = None,
) -> HypothesisPortfolio:
    updated = replace(
        portfolio,
        revision=portfolio.revision + 1,
        updated_at_utc=now or _utc_now(),
        hypotheses=portfolio.hypotheses + (record,),
    )
    validate_portfolio(
        updated,
        expected_run_id=portfolio.run_id,
        expected_version=portfolio.version,
        knowledge_store=knowledge_store,
    )
    return updated


def update_hypothesis(
    portfolio: HypothesisPortfolio,
    hypothesis_id: str,
    patch: Mapping[str, object],
    *,
    knowledge_store: KnowledgeStore | None = None,
    now: str | None = None,
) -> HypothesisPortfolio:
    if not isinstance(patch, Mapping) or not patch:
        raise ValueError("hypothesis patch must be a non-empty JSON object")
    forbidden = set(patch) & _IMMUTABLE_PATCH_FIELDS
    unknown = set(patch) - _RECORD_FIELDS
    if forbidden:
        raise ValueError(
            "update cannot change identity, status, timestamps, or revision; "
            "use transition for status"
        )
    if unknown:
        raise ValueError(f"hypothesis patch contains unsupported fields: {sorted(unknown)}")
    index, current = _find_record(portfolio, hypothesis_id)
    mapping = hypothesis_record_to_dict(
        current, schema_version=portfolio.schema_version
    )
    merged = _merge_mapping(mapping, patch)
    merged["updated_at_utc"] = now or _utc_now()
    merged["revision"] = current.revision + 1
    replacement_record = _record_from_mapping(
        merged, schema_version=portfolio.schema_version
    )
    records = list(portfolio.hypotheses)
    records[index] = replacement_record
    updated = replace(
        portfolio,
        revision=portfolio.revision + 1,
        updated_at_utc=merged["updated_at_utc"],
        hypotheses=tuple(records),
    )
    validate_portfolio(
        updated,
        expected_run_id=portfolio.run_id,
        expected_version=portfolio.version,
        knowledge_store=knowledge_store,
    )
    return updated


def transition_hypothesis(
    portfolio: HypothesisPortfolio,
    hypothesis_id: str,
    status: str,
    reason: str,
    *,
    decision: Mapping[str, object] | None = None,
    knowledge_store: KnowledgeStore | None = None,
    now: str | None = None,
) -> HypothesisPortfolio:
    if status not in HYPOTHESIS_STATUSES:
        raise ValueError(f"invalid hypothesis status: {status!r}")
    index, current = _find_record(portfolio, hypothesis_id)
    if current.status == status:
        raise ValueError(f"hypothesis {hypothesis_id!r} already has status {status!r}")
    timestamp = now or _utc_now()
    normalized_reason = _text(reason, "status reason")
    if portfolio.schema_version == 1:
        if decision is not None:
            raise ValueError(
                "schema 1 hypothesis portfolios cannot store decision metadata"
            )
        decision_history = current.decision_history
    else:
        if status in DECISION_REQUIRED_STATUSES and decision is None:
            raise ValueError(
                f"transition to {status!r} requires decision metadata"
            )
        event = _decision_from_input(
            decision if decision is not None else _empty_decision_input(),
            from_status=current.status,
            to_status=status,
            reason=normalized_reason,
            decided_at_utc=timestamp,
        )
        decision_history = current.decision_history + (event,)
    replacement_record = replace(
        current,
        status=status,
        status_reason=normalized_reason,
        updated_at_utc=timestamp,
        revision=current.revision + 1,
        decision_history=decision_history,
    )
    records = list(portfolio.hypotheses)
    records[index] = replacement_record
    updated = replace(
        portfolio,
        revision=portfolio.revision + 1,
        updated_at_utc=timestamp,
        hypotheses=tuple(records),
    )
    validate_portfolio(
        updated,
        expected_run_id=portfolio.run_id,
        expected_version=portfolio.version,
        knowledge_store=knowledge_store,
    )
    return updated


def read_portfolio(
    workspace: ResearchWorkspace, *, required: bool = True
) -> HypothesisPortfolioDocument | None:
    path = workspace.hypotheses_path
    try:
        target = workspace.assert_read_target(path)
    except FileNotFoundError:
        if required:
            raise
        return None
    data = target.read_bytes()
    _validate_utf8_lf(data, str(path))
    if not data:
        raise ValueError(f"empty hypothesis portfolio: {path}")
    try:
        value = json.loads(data)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid hypothesis portfolio JSON: {path}") from error
    portfolio = portfolio_from_mapping(value)
    validate_portfolio(
        portfolio,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
        knowledge_store=workspace.knowledge_store,
    )
    return HypothesisPortfolioDocument(str(path), portfolio, _sha256(data))


def write_portfolio(
    workspace: ResearchWorkspace,
    portfolio: HypothesisPortfolio,
    *,
    expected_sha256: str | None,
    create_only: bool = False,
) -> HypothesisPortfolioDocument:
    workspace.assert_run_writable()
    validate_portfolio(
        portfolio,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
        knowledge_store=workspace.knowledge_store,
    )
    data = portfolio_to_json_bytes(portfolio)
    _atomic_publish_portfolio(
        workspace,
        workspace.hypotheses_path,
        data,
        expected_sha256=expected_sha256,
        create_only=create_only,
    )
    return HypothesisPortfolioDocument(
        str(workspace.hypotheses_path), portfolio, _sha256(data)
    )


def portfolio_from_mapping(value: object) -> HypothesisPortfolio:
    mapping = _object(value, "hypothesis portfolio", _PORTFOLIO_FIELDS)
    schema_version = mapping["schema_version"]
    if (
        type(schema_version) is not int
        or schema_version not in SUPPORTED_SCHEMA_VERSIONS
    ):
        raise ValueError("unsupported hypothesis portfolio schema version")
    revision = _nonnegative_integer(mapping["revision"], "portfolio revision")
    hypotheses = mapping["hypotheses"]
    if not isinstance(hypotheses, list):
        raise ValueError("portfolio hypotheses must be an array")
    return HypothesisPortfolio(
        schema_version=schema_version,
        run_id=_text(mapping["run_id"], "run_id"),
        version=_version(mapping["version"]),
        revision=revision,
        created_at_utc=_timestamp(mapping["created_at_utc"], "created_at_utc"),
        updated_at_utc=_timestamp(mapping["updated_at_utc"], "updated_at_utc"),
        hypotheses=tuple(
            _record_from_mapping(item, schema_version=schema_version)
            for item in hypotheses
        ),
    )


def validate_portfolio(
    portfolio: HypothesisPortfolio,
    *,
    expected_run_id: str | None = None,
    expected_version: str | None = None,
    knowledge_store: KnowledgeStore | None = None,
) -> None:
    canonical = portfolio_from_mapping(_portfolio_dataclass_mapping(portfolio))
    if canonical != portfolio:
        raise ValueError(
            "hypothesis portfolio dataclass values do not match its schema"
        )
    if portfolio.schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError("unsupported hypothesis portfolio schema version")
    if expected_run_id is not None and portfolio.run_id != expected_run_id:
        raise ValueError("hypothesis portfolio run_id does not match the bound Run")
    if expected_version is not None and portfolio.version != expected_version:
        raise ValueError("hypothesis portfolio version does not match workspace version")
    created_at = _parse_timestamp(
        portfolio.created_at_utc, "portfolio created_at_utc"
    )
    updated_at = _parse_timestamp(
        portfolio.updated_at_utc, "portfolio updated_at_utc"
    )
    if updated_at < created_at:
        raise ValueError("portfolio updated_at_utc precedes created_at_utc")
    ids = [item.hypothesis_id for item in portfolio.hypotheses]
    if len(ids) != len(set(ids)):
        raise ValueError("hypothesis_id values must be unique")
    known = set(ids)
    for record in portfolio.hypotheses:
        _validate_record(record, knowledge_store=knowledge_store)
        unknown = set(record.parent_ids) - known
        if unknown:
            raise ValueError(
                f"hypothesis {record.hypothesis_id!r} has unknown parents: {sorted(unknown)}"
            )
        if record.hypothesis_id in record.parent_ids:
            raise ValueError(f"hypothesis {record.hypothesis_id!r} cannot parent itself")
    _validate_acyclic(portfolio.hypotheses)


def portfolio_to_dict(portfolio: HypothesisPortfolio) -> dict[str, object]:
    return _portfolio_dataclass_mapping(portfolio)


def hypothesis_record_to_dict(
    record: HypothesisRecord, *, schema_version: int = SCHEMA_VERSION
) -> dict[str, object]:
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError("unsupported hypothesis portfolio schema version")
    return _record_dataclass_mapping(record, schema_version=schema_version)


def portfolio_to_json_bytes(portfolio: HypothesisPortfolio) -> bytes:
    return (
        json.dumps(
            portfolio_to_dict(portfolio),
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")


def render_portfolio_markdown(portfolio: HypothesisPortfolio) -> str:
    lines = [
        f"# Hypothesis Portfolio {portfolio.version}",
        "",
        "> Run-local non-authoritative research memory. It is not a scientific score, Gate, Seed, Delivery, or No-Go decision.",
        "",
        f"- Run: `{portfolio.run_id}`",
        f"- Portfolio revision: {portfolio.revision}",
        f"- Hypotheses: {len(portfolio.hypotheses)}",
        "",
    ]
    for record in portfolio.hypotheses:
        lines.extend(
            [
                f"## {record.hypothesis_id}: {record.title or '(untitled draft)'}",
                "",
                f"- Status: `{record.status}`",
                f"- Status reason: {record.status_reason or '(not set)'}",
                f"- Parents: {', '.join(f'`{item}`' for item in record.parent_ids) or '(none)'}",
                f"- Revision: {record.revision}",
                "",
                "### Lineage",
                "",
                record.lineage_note or "(not set)",
                "",
                "### Problem and target failure",
                "",
                record.problem or "(not set)",
                "",
                f"Target failure: {record.target_failure.summary or '(not set)'}",
                "",
                f"Cards: {', '.join(f'`{item}`' for item in record.target_failure.card_ids) or '(none)'}",
                f"Evidence: {', '.join(f'`{item}`' for item in record.target_failure.evidence_ids) or '(none)'}",
                "",
                "### Changed computation",
                "",
                f"- Baseline: {record.changed_computation.baseline or '(not set)'}",
                f"- Intervention: {record.changed_computation.intervention or '(not set)'}",
                f"- Information available: {record.changed_computation.information_available or '(not set)'}",
                f"- Timing: {record.changed_computation.timing or '(not set)'}",
                f"- Budget effect: {record.changed_computation.budget_effect or '(not set)'}",
                "",
                "### Claim and falsification",
                "",
                f"- Mechanism claim: {record.mechanism_claim or '(not set)'}",
                f"- Falsifier: {record.falsifier or '(not set)'}",
                f"- Minimal killer experiment: {record.minimal_killer_experiment or '(not set)'}",
                f"- Nearest-prior risk: {record.nearest_prior_risk or '(not set)'}",
                "",
                f"Alternative explanations: {_render_items(record.alternative_explanations)}",
                f"Literature references: {_render_items(record.literature_refs)}",
                "",
                "### Descriptors",
                "",
                *(
                    f"- {name.replace('_', ' ')}: {value or '(not set)'}"
                    for name, value in asdict(record.descriptors).items()
                ),
                "",
            ]
        )
        if record.decision_history:
            lines.extend(["### Decision history", ""])
            for event in record.decision_history:
                lines.extend(
                    [
                        f"- {event.decided_at_utc}: `{event.from_status}` → `{event.to_status}`",
                        f"  - Evidence fidelity: `{event.evidence_fidelity or 'NOT_APPLICABLE'}`",
                        f"  - Kill target: `{event.kill_target or 'NONE'}`",
                        f"  - Independent implementations: {event.independent_implementation_count}",
                        f"  - Structural refutation: {str(event.structural_refutation).lower()}",
                        f"  - KILLED: {event.killed}",
                        f"  - SURVIVES: {event.survives}",
                        f"  - WHY: {event.why}",
                    ]
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _portfolio_dataclass_mapping(
    portfolio: HypothesisPortfolio,
) -> dict[str, object]:
    if type(portfolio) is not HypothesisPortfolio:
        raise ValueError("portfolio must be a HypothesisPortfolio")
    if type(portfolio.hypotheses) is not tuple:
        raise ValueError("portfolio hypotheses must be a tuple")
    return {
        "schema_version": portfolio.schema_version,
        "run_id": portfolio.run_id,
        "version": portfolio.version,
        "revision": portfolio.revision,
        "created_at_utc": portfolio.created_at_utc,
        "updated_at_utc": portfolio.updated_at_utc,
        "hypotheses": [
            _record_dataclass_mapping(item, schema_version=portfolio.schema_version)
            for item in portfolio.hypotheses
        ],
    }


def _record_dataclass_mapping(
    record: HypothesisRecord, *, schema_version: int
) -> dict[str, object]:
    if type(record) is not HypothesisRecord:
        raise ValueError("portfolio hypotheses must contain HypothesisRecord values")
    if type(record.parent_ids) is not tuple:
        raise ValueError("parent_ids must be a tuple")
    if type(record.target_failure) is not TargetFailure:
        raise ValueError("target_failure must be a TargetFailure")
    if type(record.target_failure.card_ids) is not tuple:
        raise ValueError("target_failure.card_ids must be a tuple")
    if type(record.target_failure.evidence_ids) is not tuple:
        raise ValueError("target_failure.evidence_ids must be a tuple")
    if type(record.changed_computation) is not ChangedComputation:
        raise ValueError("changed_computation must be a ChangedComputation")
    if type(record.alternative_explanations) is not tuple:
        raise ValueError("alternative_explanations must be a tuple")
    if type(record.descriptors) is not HypothesisDescriptors:
        raise ValueError("descriptors must be HypothesisDescriptors")
    if type(record.literature_refs) is not tuple:
        raise ValueError("literature_refs must be a tuple")
    if type(record.decision_history) is not tuple:
        raise ValueError("decision_history must be a tuple")
    mapping: dict[str, object] = {
        "hypothesis_id": record.hypothesis_id,
        "title": record.title,
        "status": record.status,
        "status_reason": record.status_reason,
        "parent_ids": list(record.parent_ids),
        "lineage_note": record.lineage_note,
        "problem": record.problem,
        "target_failure": {
            "summary": record.target_failure.summary,
            "card_ids": list(record.target_failure.card_ids),
            "evidence_ids": list(record.target_failure.evidence_ids),
        },
        "changed_computation": {
            "baseline": record.changed_computation.baseline,
            "intervention": record.changed_computation.intervention,
            "information_available": record.changed_computation.information_available,
            "timing": record.changed_computation.timing,
            "budget_effect": record.changed_computation.budget_effect,
        },
        "mechanism_claim": record.mechanism_claim,
        "falsifier": record.falsifier,
        "minimal_killer_experiment": record.minimal_killer_experiment,
        "nearest_prior_risk": record.nearest_prior_risk,
        "alternative_explanations": list(record.alternative_explanations),
        "descriptors": {
            "problem_family": record.descriptors.problem_family,
            "computation_stage": record.descriptors.computation_stage,
            "intervention_family": record.descriptors.intervention_family,
            "information_source": record.descriptors.information_source,
            "timing_class": record.descriptors.timing_class,
            "budget_class": record.descriptors.budget_class,
            "evaluation_mode": record.descriptors.evaluation_mode,
        },
        "literature_refs": list(record.literature_refs),
        "created_at_utc": record.created_at_utc,
        "updated_at_utc": record.updated_at_utc,
        "revision": record.revision,
    }
    if schema_version == 2:
        mapping["decision_history"] = [
            _decision_dataclass_mapping(item) for item in record.decision_history
        ]
    return mapping


def _record_from_mapping(
    value: object, *, schema_version: int
) -> HypothesisRecord:
    fields = _RECORD_V2_FIELDS if schema_version == 2 else _RECORD_FIELDS
    mapping = _object(value, "hypothesis record", fields)
    target = _object(
        mapping["target_failure"],
        "target_failure",
        {"summary", "card_ids", "evidence_ids"},
    )
    computation = _object(
        mapping["changed_computation"],
        "changed_computation",
        {"baseline", "intervention", "information_available", "timing", "budget_effect"},
    )
    descriptor = _object(
        mapping["descriptors"],
        "descriptors",
        {
            "problem_family",
            "computation_stage",
            "intervention_family",
            "information_source",
            "timing_class",
            "budget_class",
            "evaluation_mode",
        },
    )
    status = mapping["status"]
    if not isinstance(status, str) or status not in HYPOTHESIS_STATUSES:
        raise ValueError(f"invalid hypothesis status: {status!r}")
    return HypothesisRecord(
        hypothesis_id=_text(mapping["hypothesis_id"], "hypothesis_id"),
        title=_optional_text(mapping["title"], "title"),
        status=status,
        status_reason=_optional_text(mapping["status_reason"], "status_reason"),
        parent_ids=_string_array(mapping["parent_ids"], "parent_ids"),
        lineage_note=_optional_text(mapping["lineage_note"], "lineage_note"),
        problem=_optional_text(mapping["problem"], "problem"),
        target_failure=TargetFailure(
            summary=_optional_text(target["summary"], "target_failure.summary"),
            card_ids=_string_array(target["card_ids"], "target_failure.card_ids"),
            evidence_ids=_string_array(
                target["evidence_ids"], "target_failure.evidence_ids"
            ),
        ),
        changed_computation=ChangedComputation(
            baseline=_optional_text(computation["baseline"], "changed_computation.baseline"),
            intervention=_optional_text(
                computation["intervention"], "changed_computation.intervention"
            ),
            information_available=_optional_text(
                computation["information_available"],
                "changed_computation.information_available",
            ),
            timing=_optional_text(computation["timing"], "changed_computation.timing"),
            budget_effect=_optional_text(
                computation["budget_effect"], "changed_computation.budget_effect"
            ),
        ),
        mechanism_claim=_optional_text(mapping["mechanism_claim"], "mechanism_claim"),
        falsifier=_optional_text(mapping["falsifier"], "falsifier"),
        minimal_killer_experiment=_optional_text(
            mapping["minimal_killer_experiment"], "minimal_killer_experiment"
        ),
        nearest_prior_risk=_optional_text(mapping["nearest_prior_risk"], "nearest_prior_risk"),
        alternative_explanations=_string_array(
            mapping["alternative_explanations"], "alternative_explanations"
        ),
        descriptors=HypothesisDescriptors(
            problem_family=_optional_text(descriptor["problem_family"], "descriptors.problem_family"),
            computation_stage=_optional_text(
                descriptor["computation_stage"], "descriptors.computation_stage"
            ),
            intervention_family=_optional_text(
                descriptor["intervention_family"], "descriptors.intervention_family"
            ),
            information_source=_optional_text(
                descriptor["information_source"], "descriptors.information_source"
            ),
            timing_class=_optional_text(descriptor["timing_class"], "descriptors.timing_class"),
            budget_class=_optional_text(descriptor["budget_class"], "descriptors.budget_class"),
            evaluation_mode=_optional_text(
                descriptor["evaluation_mode"], "descriptors.evaluation_mode"
            ),
        ),
        literature_refs=_string_array(mapping["literature_refs"], "literature_refs"),
        created_at_utc=_timestamp(mapping["created_at_utc"], "created_at_utc"),
        updated_at_utc=_timestamp(mapping["updated_at_utc"], "updated_at_utc"),
        revision=_positive_integer(mapping["revision"], "hypothesis revision"),
        decision_history=(
            _decision_history(mapping["decision_history"])
            if schema_version == 2
            else ()
        ),
    )


def _decision_from_input(
    value: Mapping[str, object],
    *,
    from_status: str,
    to_status: str,
    reason: str,
    decided_at_utc: str,
) -> HypothesisDecision:
    if not isinstance(value, Mapping):
        raise ValueError("decision metadata must be a JSON object")
    mapping = _object(dict(value), "decision metadata", _DECISION_INPUT_FIELDS)
    return _decision_from_mapping(
        {
            **mapping,
            "from_status": from_status,
            "to_status": to_status,
            "reason": reason,
            "decided_at_utc": decided_at_utc,
        }
    )


def _empty_decision_input() -> dict[str, object]:
    return {
        "evidence_fidelity": None,
        "kill_target": None,
        "subject_scope": {
            "models": [],
            "tasks": [],
            "datasets": [],
            "seeds": [],
            "environment": "",
        },
        "independent_implementation_count": 0,
        "structural_refutation": False,
        "structural_refutation_reason": "",
        "killed": "",
        "survives": "",
        "why": "",
    }


def _decision_history(value: object) -> tuple[HypothesisDecision, ...]:
    if not isinstance(value, list):
        raise ValueError("decision_history must be an array")
    return tuple(_decision_from_mapping(item) for item in value)


def _decision_from_mapping(value: object) -> HypothesisDecision:
    mapping = _object(value, "hypothesis decision", _DECISION_EVENT_FIELDS)
    from_status = mapping["from_status"]
    to_status = mapping["to_status"]
    for label, status in (("from_status", from_status), ("to_status", to_status)):
        if not isinstance(status, str) or status not in HYPOTHESIS_STATUSES:
            raise ValueError(f"invalid decision {label}: {status!r}")
    fidelity = mapping["evidence_fidelity"]
    if fidelity is not None and fidelity not in EVIDENCE_FIDELITIES:
        raise ValueError(f"invalid evidence_fidelity: {fidelity!r}")
    kill_target = mapping["kill_target"]
    if kill_target is not None and kill_target not in KILL_TARGETS:
        raise ValueError(f"invalid kill_target: {kill_target!r}")
    if to_status in {"falsified", "prior_collision"} and kill_target is None:
        raise ValueError(f"transition to {to_status!r} requires kill_target")
    scope = _object(mapping["subject_scope"], "subject_scope", _SUBJECT_SCOPE_FIELDS)
    structural = mapping["structural_refutation"]
    if type(structural) is not bool:
        raise ValueError("structural_refutation must be boolean")
    structural_reason = _optional_text(
        mapping["structural_refutation_reason"],
        "structural_refutation_reason",
    )
    if structural and not structural_reason:
        raise ValueError(
            "structural_refutation_reason is required when structural_refutation is true"
        )
    killed = _optional_text(mapping["killed"], "killed")
    survives = _optional_text(mapping["survives"], "survives")
    why = _optional_text(mapping["why"], "why")
    if to_status in DECISION_REQUIRED_STATUSES:
        missing = [
            name
            for name, text in (("killed", killed), ("survives", survives), ("why", why))
            if not text
        ]
        if missing:
            raise ValueError(
                f"transition to {to_status!r} requires non-empty decision fields: {missing}"
            )
    return HypothesisDecision(
        from_status=from_status,
        to_status=to_status,
        reason=_text(mapping["reason"], "decision reason"),
        decided_at_utc=_timestamp(mapping["decided_at_utc"], "decided_at_utc"),
        evidence_fidelity=fidelity,
        kill_target=kill_target,
        subject_scope=SubjectScope(
            models=_string_array(scope["models"], "subject_scope.models"),
            tasks=_string_array(scope["tasks"], "subject_scope.tasks"),
            datasets=_string_array(scope["datasets"], "subject_scope.datasets"),
            seeds=_string_array(scope["seeds"], "subject_scope.seeds"),
            environment=_optional_text(
                scope["environment"], "subject_scope.environment"
            ),
        ),
        independent_implementation_count=_nonnegative_integer(
            mapping["independent_implementation_count"],
            "independent_implementation_count",
        ),
        structural_refutation=structural,
        structural_refutation_reason=structural_reason,
        killed=killed,
        survives=survives,
        why=why,
    )


def _decision_dataclass_mapping(event: HypothesisDecision) -> dict[str, object]:
    if type(event) is not HypothesisDecision:
        raise ValueError("decision_history must contain HypothesisDecision values")
    if type(event.subject_scope) is not SubjectScope:
        raise ValueError("decision subject_scope must be SubjectScope")
    return {
        "from_status": event.from_status,
        "to_status": event.to_status,
        "reason": event.reason,
        "decided_at_utc": event.decided_at_utc,
        "evidence_fidelity": event.evidence_fidelity,
        "kill_target": event.kill_target,
        "subject_scope": {
            "models": list(event.subject_scope.models),
            "tasks": list(event.subject_scope.tasks),
            "datasets": list(event.subject_scope.datasets),
            "seeds": list(event.subject_scope.seeds),
            "environment": event.subject_scope.environment,
        },
        "independent_implementation_count": event.independent_implementation_count,
        "structural_refutation": event.structural_refutation,
        "structural_refutation_reason": event.structural_refutation_reason,
        "killed": event.killed,
        "survives": event.survives,
        "why": event.why,
    }


def decision_warning_codes(event: HypothesisDecision) -> tuple[str, ...]:
    """Return mechanical advisory warnings without making a scientific decision."""
    warnings: list[str] = []
    paper_level = event.kill_target in {"METHOD_CORE", "PAPER_DIRECTION"}
    if (
        event.evidence_fidelity == "SCREENING"
        and paper_level
        and not event.structural_refutation
    ):
        warnings.append("screening_paper_level_kill_without_structural_refutation")
    if (
        event.evidence_fidelity is not None
        and event.independent_implementation_count <= 1
        and paper_level
        and not event.structural_refutation
    ):
        warnings.append("single_implementation_paper_level_kill")
    scope = event.subject_scope
    if event.evidence_fidelity == "REPRESENTATIVE" and not any(
        (
            scope.models,
            scope.tasks,
            scope.datasets,
            scope.seeds,
            scope.environment,
        )
    ):
        warnings.append("representative_subject_scope_empty")
    if event.structural_refutation and not event.structural_refutation_reason:
        warnings.append("structural_refutation_reason_missing")
    if event.to_status == "prior_collision" and not event.survives.strip():
        warnings.append("prior_collision_survives_unchecked")
    return tuple(warnings)


def _validate_record(
    record: HypothesisRecord, *, knowledge_store: KnowledgeStore | None
) -> None:
    created_at = _parse_timestamp(record.created_at_utc, "created_at_utc")
    updated_at = _parse_timestamp(record.updated_at_utc, "updated_at_utc")
    if updated_at < created_at:
        raise ValueError(
            f"hypothesis {record.hypothesis_id!r} updated_at_utc precedes created_at_utc"
        )
    previous_status = "draft"
    previous_time = created_at
    for event in record.decision_history:
        event_time = _parse_timestamp(event.decided_at_utc, "decided_at_utc")
        if event.from_status != previous_status:
            raise ValueError(
                f"hypothesis {record.hypothesis_id!r} decision history is discontinuous"
            )
        if event_time < previous_time or event_time > updated_at:
            raise ValueError(
                f"hypothesis {record.hypothesis_id!r} decision timestamp is out of order"
            )
        previous_status = event.to_status
        previous_time = event_time
    if record.decision_history:
        if record.decision_history[-1].to_status != record.status:
            raise ValueError(
                f"hypothesis {record.hypothesis_id!r} status differs from decision history"
            )
        if record.decision_history[-1].reason != record.status_reason:
            raise ValueError(
                f"hypothesis {record.hypothesis_id!r} status reason differs from decision history"
            )
    if len(record.parent_ids) != len(set(record.parent_ids)):
        raise ValueError(f"hypothesis {record.hypothesis_id!r} has duplicate parent_ids")
    for card_id in record.target_failure.card_ids:
        if _CARD_ID.fullmatch(card_id) is None:
            raise ValueError(
                f"hypothesis {record.hypothesis_id!r} has invalid Card ID: {card_id!r}"
            )
    for evidence_id in record.target_failure.evidence_ids:
        if knowledge_store is None:
            raise ValueError("a KnowledgeStore is required when Evidence IDs are supplied")
        evidence = knowledge_store.get_evidence(evidence_id)
        if evidence is None:
            raise KeyError(f"unknown evidence id: {evidence_id}")
        if not evidence.fulltext_is_current or evidence.passage_is_current is False:
            raise ValueError(f"Evidence is not current: {evidence_id}")
    if record.status in {"active", "escalated"}:
        required = {
            "status_reason": record.status_reason,
            "title": record.title,
            "problem": record.problem,
            "target_failure.summary": record.target_failure.summary,
            "changed_computation.baseline": record.changed_computation.baseline,
            "changed_computation.intervention": record.changed_computation.intervention,
            "changed_computation.information_available": record.changed_computation.information_available,
            "changed_computation.timing": record.changed_computation.timing,
            "changed_computation.budget_effect": record.changed_computation.budget_effect,
            "mechanism_claim": record.mechanism_claim,
            "falsifier": record.falsifier,
            "minimal_killer_experiment": record.minimal_killer_experiment,
            "nearest_prior_risk": record.nearest_prior_risk,
            "descriptors.problem_family": record.descriptors.problem_family,
            "descriptors.computation_stage": record.descriptors.computation_stage,
            "descriptors.intervention_family": record.descriptors.intervention_family,
            "descriptors.information_source": record.descriptors.information_source,
            "descriptors.timing_class": record.descriptors.timing_class,
            "descriptors.budget_class": record.descriptors.budget_class,
            "descriptors.evaluation_mode": record.descriptors.evaluation_mode,
        }
        missing = sorted(name for name, value in required.items() if not value.strip())
        if missing:
            raise ValueError(
                f"{record.status} hypothesis {record.hypothesis_id!r} is record-incomplete: {missing}"
            )


def _validate_acyclic(records: Sequence[HypothesisRecord]) -> None:
    parents = {item.hypothesis_id: item.parent_ids for item in records}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            raise ValueError(f"hypothesis lineage contains a cycle at {identifier!r}")
        if identifier in visited:
            return
        visiting.add(identifier)
        for parent in parents[identifier]:
            visit(parent)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in parents:
        visit(identifier)


def _atomic_publish_portfolio(
    workspace: ResearchWorkspace,
    path: Path,
    data: bytes,
    *,
    expected_sha256: str | None,
    create_only: bool,
) -> None:
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
        raise FileExistsError("another hypothesis portfolio write is in progress") from error
    temporary = target.with_name(f".{target.name}.{uuid4().hex}.tmp")
    try:
        exists = target.exists() or target.is_symlink()
        if create_only:
            if exists:
                raise FileExistsError(f"hypothesis portfolio already exists: {target}")
            if expected_sha256 is not None:
                raise ValueError("create-only portfolio write cannot have expected_sha256")
        else:
            if not isinstance(expected_sha256, str) or _SHA256.fullmatch(expected_sha256) is None:
                raise ValueError("portfolio update requires its previously read SHA-256")
            current = workspace.assert_read_target(target).read_bytes()
            if _sha256(current) != expected_sha256:
                raise FileExistsError("hypothesis portfolio changed since it was read")
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
                    "hypothesis portfolio was concurrently created"
                ) from error
        else:
            current = workspace.assert_read_target(target).read_bytes()
            if _sha256(current) != expected_sha256:
                raise FileExistsError("hypothesis portfolio changed during update")
            _replace_file(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
        if lock.exists() and not lock.is_symlink():
            lock.unlink()


def _find_record(
    portfolio: HypothesisPortfolio, hypothesis_id: str
) -> tuple[int, HypothesisRecord]:
    identifier = _text(hypothesis_id, "hypothesis_id")
    matches = [
        (index, item)
        for index, item in enumerate(portfolio.hypotheses)
        if item.hypothesis_id == identifier
    ]
    if not matches:
        raise KeyError(f"unknown hypothesis id: {identifier}")
    return matches[0]


def _merge_mapping(
    original: Mapping[str, object], patch: Mapping[str, object]
) -> dict[str, object]:
    result = dict(original)
    for key, value in patch.items():
        current = result.get(key)
        if isinstance(current, Mapping) and isinstance(value, Mapping):
            result[key] = _merge_mapping(current, value)
        else:
            result[key] = value
    return result


def _object(value: object, label: str, fields: set[str]) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"{label} fields do not match schema 1")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ValueError(f"{label} must be non-empty single-line text")
    return value.strip()


def _optional_text(value: object, label: str) -> str:
    if not isinstance(value, str) or "\r" in value:
        raise ValueError(f"{label} must be text")
    return value.replace("\r\n", "\n").strip()


def _decision_text(value: object, label: str) -> str:
    text = _optional_text(value, label)
    if not text:
        raise ValueError(f"{label} must be non-empty text")
    return text


def _string_array(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a string array")
    items = tuple(_text(item, label) for item in value)
    if len(items) != len(set(items)):
        raise ValueError(f"{label} must not contain duplicates")
    return items


def _version(value: object) -> str:
    if not isinstance(value, str) or re.fullmatch(r"v\d{3,}", value) is None:
        raise ValueError(f"invalid hypothesis portfolio version: {value!r}")
    return value


def _positive_integer(value: object, label: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{label} must be a positive integer")
    return value


def _nonnegative_integer(value: object, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


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


def _render_items(items: Sequence[str]) -> str:
    return "; ".join(items) if items else "(none)"
