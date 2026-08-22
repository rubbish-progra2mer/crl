from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Iterable

from .experiment import experiment_material_errors
from .falsification import (
    experiment_spec_from_mapping,
    experiment_spec_warning_codes,
)
from .hypotheses import decision_warning_codes, portfolio_from_mapping
from .prior_audit import _load_assessment
from .recall import resume_recall
from .workspace import ResearchWorkspace, _publish_once, _required_file, _sha256


_DIAGNOSIS_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,63}")
_EXCLUDED_DIRS = {
    ".crl",
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "external",
    "vendor",
    "third_party",
    "ground_truth",
    "hidden_test",
    "hidden_tests",
}
_EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
_SELECTION_CONTEXT_SECTIONS = (
    ("best_candidate_set", "当前最佳候选集合"),
    ("positive_evidence_delta", "新增正向证据"),
    ("killed_or_invalidated_scope", "已失效或被杀范围"),
    ("fatal_uncertainties", "剩余致命不确定性"),
    ("next_high_information_action", "下一项最高信息量动作"),
    ("strategy_change", "策略变化"),
)
_PREFERENCE_VERDICTS = {
    "A_PREFERRED",
    "B_PREFERRED",
    "INCOMPARABLE",
    "INSUFFICIENT_EVIDENCE",
}
_UNRESOLVED_DECLARATIONS = {"UNAVAILABLE", "UNKNOWN", "INSUFFICIENT"}
_EMPTY_SET_DECLARATIONS = {"NONE", "EMPTY", "NOT_APPLICABLE"}
_STRUCTURED_BLOCK_MARKERS = {
    "PAIRWISE_COMPARISON",
    "CANDIDATE_ADMISSION",
    "LOCAL_REWARD_CONTRACT",
    "EVIDENCE_ROLE",
    "INDEPENDENT_IMPLEMENTATION",
    "IMPLEMENTATION_LOTTERY_EXCEPTION",
    "PREFERENCE_UPDATE",
}
_CANDIDATE_ADMISSION_FIELDS = (
    "TARGET_CLAIM",
    "CONTRIBUTION_COORDINATE",
    "CHANGED_COMPUTATION",
    "RESEARCH_ARTIFACT",
    "STRONGEST_CONSTRUCTIVE_BASELINE",
    "FATAL_UNCERTAINTY",
    "REVERSAL_TEST",
)
_LOCAL_REWARD_FIELDS = (
    "PRIMARY_OBSERVABLE",
    "STRONG_BASELINE",
    "METRIC_DIRECTION",
    "MINIMUM_MEANINGFUL_DELTA",
    "REPETITIONS_OR_UNCERTAINTY",
    "FAILURE_NEGATIVE_INCONCLUSIVE",
    "EXECUTION_COST",
    "LOW_FIDELITY_SCOPE",
    "INDEPENDENT_ADMISSION_CHECK",
    "SCALE_BRIDGE_ASSUMPTION",
    "MUTATION_ACCEPTANCE_CONDITION",
)
_INDEPENDENT_IMPLEMENTATION_FIELDS = (
    "IMPLEMENTATION_ID",
    "ARTIFACT_PATH",
    "FRESH_SESSION_ID",
    "FROZEN_CANDIDATE_PATH",
    "FIDELITY_CHECK_PATH",
)
_IMPLEMENTATION_LOTTERY_EXCEPTION_TYPES = {
    "MECHANICALLY_UNIQUE",
    "STRUCTURAL_REFUTATION",
}
_PREFERENCE_UPDATE_FIELDS = (
    "ACTION_ID",
    "AFFECTED_PAIR",
    "VERDICT_BEFORE",
    "VERDICT_AFTER",
    "FATAL_UNCERTAINTY_REDUCED",
    "EVIDENCE_PATHS",
    "STOP_REPEATING",
    "EXPANDED_COORDINATE",
)


def collect_diagnosis(
    workspace: ResearchWorkspace, diagnosis_id: str
) -> dict[str, object]:
    workspace.assert_run_writable()
    identifier = _diagnosis_id(diagnosis_id)
    destination = workspace.assert_write_target(
        workspace.workbench_path / "diagnosis" / identifier
    )
    if destination.exists():
        raise FileExistsError(f"diagnosis id already exists: {identifier}")
    destination.mkdir(parents=True)
    try:
        facts = _facts(workspace, identifier)
        facts_bytes = _json_bytes(facts)
        report = _render_report(facts, _sha256(facts_bytes))
        _publish_once(
            destination / "diagnosis_facts.json",
            facts_bytes,
            within=workspace.workspace_path,
        )
        _publish_once(
            destination / "report.md",
            report,
            within=workspace.workspace_path,
        )
    except BaseException:
        for path in destination.iterdir():
            if path.is_file():
                path.unlink()
        destination.rmdir()
        raise
    return show_diagnosis(workspace, identifier)


def show_diagnosis(
    workspace: ResearchWorkspace, diagnosis_id: str
) -> dict[str, object]:
    identifier = _diagnosis_id(diagnosis_id)
    destination = workspace.workbench_path / "diagnosis" / identifier
    facts_data = _required_file(
        destination / "diagnosis_facts.json", within=workspace.workspace_path
    )
    report_data = _required_file(destination / "report.md", within=workspace.workspace_path)
    facts = json.loads(facts_data.decode("utf-8"))
    marker = f"FACTS_SHA256: {_sha256(facts_data)}"
    if marker not in report_data.decode("utf-8"):
        raise ValueError("diagnosis report is not bound to its facts package")
    return {
        "diagnosis_id": identifier,
        "path": str(destination),
        "facts_sha256": _sha256(facts_data),
        "report_sha256": _sha256(report_data),
        "facts": facts,
        "authority": "ADVISORY_NON_AUTHORITATIVE",
    }


def _facts(workspace: ResearchWorkspace, diagnosis_id: str) -> dict[str, object]:
    files = []
    suffix_counts: Counter[str] = Counter()
    marker_counts: Counter[str] = Counter()
    for path in _ordinary_files(workspace):
        relative = path.relative_to(workspace.workspace_path).as_posix()
        data = path.read_bytes()
        suffix_counts[path.suffix.casefold() or "<none>"] += 1
        if path.suffix.casefold() in {".md", ".txt", ".json", ".jsonl", ".py"}:
            text = data.decode("utf-8", errors="ignore").casefold()
            for marker in ("not provided", "todo", "assumption", "failed", "contradiction"):
                marker_counts[marker] += text.count(marker)
        files.append(
            {
                "path": relative,
                "size_bytes": len(data),
                "mtime_ns": path.stat().st_mtime_ns,
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    files.sort(key=lambda item: (-int(item["mtime_ns"]), str(item["path"])))
    experiments = _experiment_facts(workspace)
    comparisons = _file_group(workspace.experiment_path / "comparisons", workspace)
    searches = _file_group(workspace.hypotheses_path.parent / "searches", workspace)
    evaluations = _file_group(workspace.review_path / "evaluations", workspace)
    try:
        recall = resume_recall(workspace, limit=8)
        recall_status = {
            "status": "READY",
            "reason": None,
            "semantic_status": recall.get("semantic_status"),
            "semantic_reason": recall.get("semantic_reason"),
        }
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as error:
        recall = None
        recall_status = {
            "status": "UNAVAILABLE",
            "reason": _recall_unavailable_reason(error),
            "semantic_status": None,
            "semantic_reason": None,
        }
    selection_context = _selection_context_facts(workspace)
    current_version = {
        "version": workspace.version,
        "experiments": experiments,
        "comparison_files": comparisons,
        "search_snapshot_files": searches,
        "review_evaluation_files": evaluations,
        "selection_context": selection_context,
    }
    run_wide = _run_wide_facts(workspace)
    preference = selection_context["candidate_preference"]
    hypothesis_implementation_risks = []
    for item in run_wide["hypotheses"]["semantic_overreach_warnings"]:
        if "single_implementation_paper_level_kill" not in item["warning_codes"]:
            continue
        hypothesis_implementation_risks.append(
            {
                "source": "HYPOTHESIS_V2_DECISION",
                "version": item["version"],
                "hypothesis_id": item["hypothesis_id"],
                "decision_index": item["decision_index"],
                "code": "single_implementation_paper_level_kill",
            }
        )
    preference["single_implementation_idea_level_risks"].extend(
        hypothesis_implementation_risks
    )
    preference["single_implementation_idea_level_risk_count"] = len(
        preference["single_implementation_idea_level_risks"]
    )
    return {
        "schema_version": 1,
        "diagnosis_id": diagnosis_id,
        "authority": "ADVISORY_NON_AUTHORITATIVE_FACTS_ONLY",
        "run_id": workspace.workspace_path.name,
        "contract_version": workspace.contract_version,
        "version": workspace.version,
        "current_version": current_version,
        "run_wide": run_wide,
        "generated_at_utc": _utc_now(),
        "file_count": len(files),
        "file_type_counts": dict(sorted(suffix_counts.items())),
        "marker_occurrences": dict(sorted(marker_counts.items())),
        "recent_files": files[:30],
        "experiments": experiments,
        "comparison_files": comparisons,
        "search_snapshot_files": searches,
        "review_evaluation_files": evaluations,
        "recall_resume": recall,
        "recall_status": recall_status,
        "non_judgments": [
            "no candidate is killed or selected by this package",
            "no novelty, delivery, or next-action decision is computed",
            "the main researcher interprets these traceable facts",
        ],
    }


def _experiment_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    facts = []
    for tier, root in (
        ("formal", workspace.experiment_path / "attempts"),
        ("recorded", workspace.experiment_path / "recorded"),
    ):
        if not root.is_dir():
            continue
        for directory in sorted(item for item in root.iterdir() if item.is_dir()):
            record_path = directory / ("execution.json" if tier == "formal" else "record.json")
            record: object = None
            record_sha256 = None
            error = None
            try:
                data = _required_file(record_path, within=workspace.workspace_path)
                record = json.loads(data.decode("utf-8"))
                record_sha256 = _sha256(data)
            except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError, ValueError) as caught:
                error = str(caught)
            status = None
            valid_review_support = None
            validation_errors: list[str] = []
            if isinstance(record, dict):
                status = record.get("status")
                if status is None:
                    status = "SUCCESS" if record.get("runner_exit_code") == 0 else "FAILED"
            if tier == "formal":
                validation_errors = list(
                    experiment_material_errors(workspace, (directory.name,))
                )
                valid_review_support = not validation_errors
            facts.append(
                {
                    "tier": tier,
                    "id": directory.name,
                    "path": directory.relative_to(workspace.workspace_path).as_posix(),
                    "record_sha256": record_sha256,
                    "status": status,
                    "read_error": error,
                    "valid_review_support": valid_review_support,
                    "validation_errors": validation_errors,
                }
            )
    return {
        "attempt_count": len(facts),
        "tier_counts": dict(Counter(str(item["tier"]) for item in facts)),
        "status_counts": dict(Counter(str(item["status"]) for item in facts)),
        "valid_formal_count": sum(
            1 for item in facts if item["valid_review_support"] is True
        ),
        "attempts": facts,
    }


def _run_wide_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    scientific_versions = _scientific_version_facts(workspace)
    hypotheses = _hypothesis_facts(workspace)
    experiments = _run_wide_experiment_facts(workspace)
    return {
        "scientific_versions": scientific_versions,
        "hypotheses": hypotheses,
        "experiments": experiments,
        "searches": _search_facts(workspace),
        "prior_collisions": _prior_collision_facts(workspace),
        "subagents": _subagent_facts(workspace),
        "recall_composition": _recall_composition(workspace),
        "latest_structured_activity": _latest_structured_activity_facts(
            workspace, hypotheses, experiments
        ),
    }


def _scientific_version_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    version_pattern = re.compile(r"(?:^|_)(v\d{3,})(?:$|[._/])")
    bounds: dict[str, list[int]] = {}
    for path in _ordinary_files(workspace):
        relative = path.relative_to(workspace.workspace_path).as_posix()
        matches = version_pattern.findall(relative)
        for version in matches:
            bounds.setdefault(version, []).append(path.stat().st_mtime_ns)
    versions = sorted(bounds, key=lambda item: int(item[1:]))
    items = []
    for version in versions:
        mtimes = bounds[version]
        items.append(
            {
                "version": version,
                "first_artifact_mtime_ns": min(mtimes),
                "last_artifact_mtime_ns": max(mtimes),
                "artifact_span_seconds": (max(mtimes) - min(mtimes)) / 1_000_000_000,
                "artifact_count": len(mtimes),
            }
        )
    return {
        "current_version": workspace.version,
        "version_count": len(versions),
        "versions": items,
        "current_version_artifact_count": next(
            (
                int(item["artifact_count"])
                for item in items
                if item["version"] == workspace.version
            ),
            0,
        ),
        "empty_current_version": workspace.version not in versions,
    }


def _selection_context_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    path = workspace.document_path("selection_context")
    relative = path.relative_to(workspace.workspace_path).as_posix()
    unavailable = {
        key: {"heading": heading, "status": "UNAVAILABLE", "text": None}
        for key, heading in _SELECTION_CONTEXT_SECTIONS
    }
    try:
        data = _required_file(path, within=workspace.workspace_path)
        text = data.decode("utf-8")
    except (FileNotFoundError, OSError, UnicodeError, ValueError) as error:
        return {
            "status": "UNAVAILABLE",
            "path": relative,
            "reason": type(error).__name__,
            "sections": unavailable,
            "candidate_preference": _unavailable_candidate_preference(
                "selection_context_unavailable"
            ),
        }
    extracted = _markdown_h2_sections(text)
    sections = {}
    duplicates = []
    for key, heading in _SELECTION_CONTEXT_SECTIONS:
        occurrences = extracted.get(heading, [])
        if len(occurrences) > 1:
            duplicates.append(key)
        content = occurrences[0].strip() if len(occurrences) == 1 else ""
        sections[key] = {
            "heading": heading,
            "status": "PRESENT" if content else "UNAVAILABLE",
            "text": content or None,
        }
    missing = [
        key for key, item in sections.items() if item["status"] == "UNAVAILABLE"
    ]
    return {
        "status": "READY" if not missing else "PARTIAL",
        "path": relative,
        "reason": (
            None
            if not missing
            else "duplicate_template_sections"
            if duplicates
            else "missing_or_empty_template_sections"
        ),
        "missing_sections": missing,
        "duplicate_sections": duplicates,
        "sections": sections,
        "candidate_preference": _selection_preference_facts(workspace, sections),
    }


def _unavailable_candidate_preference(reason: str) -> dict[str, object]:
    unavailable_set = {
        "status": "UNAVAILABLE",
        "candidate_ids": [],
        "raw_values": [],
        "occurrence_count": 0,
    }
    return {
        "status": "UNAVAILABLE",
        "reason": reason,
        "incumbent_set": dict(unavailable_set),
        "challengers": dict(unavailable_set),
        "active_candidate_ids": [],
        "pairwise_comparison_count": 0,
        "pairwise_comparisons": [],
        "candidate_admission_contract_count": 0,
        "candidate_admission_contracts": [],
        "local_reward_contract_count": 0,
        "local_reward_contracts": [],
        "evidence_role_count": 0,
        "evidence_roles": [],
        "independent_implementation_record_count": 0,
        "independent_implementations": [],
        "independent_implementation_summaries": [],
        "implementation_lottery_exception_count": 0,
        "implementation_lottery_exceptions": [],
        "preference_update_count": 0,
        "preference_updates": [],
        "preference_stagnation": {
            "assessment_status": "INSUFFICIENT_HISTORY",
            "warning": False,
            "warning_code": None,
            "evaluated_action_ids": [],
            "selected_action_last_positions": [],
        },
        "advisory_count": 0,
        "advisories": [],
        "single_implementation_idea_level_risk_count": 0,
        "single_implementation_idea_level_risks": [],
    }


def _selection_preference_facts(
    workspace: ResearchWorkspace, sections: dict[str, dict[str, object]]
) -> dict[str, object]:
    best_text = str(sections["best_candidate_set"].get("text") or "")
    strategy_text = str(sections["strategy_change"].get("text") or "")
    incumbent_set = _candidate_set_declaration(best_text, "INCUMBENT_SET")
    challengers = _candidate_set_declaration(best_text, "CHALLENGERS")
    best_blocks = _structured_markdown_blocks(best_text)
    strategy_blocks = _structured_markdown_blocks(strategy_text)
    advisories: list[dict[str, object]] = []
    for label, declaration in (
        ("INCUMBENT_SET", incumbent_set),
        ("CHALLENGERS", challengers),
    ):
        empty_marker_conflicts = [
            item["occurrence_index"]
            for item in declaration["declarations"]
            if item.get("conflict_reason")
            == "empty_marker_mixed_with_candidate_ids"
        ]
        if empty_marker_conflicts:
            advisories.append(
                {
                    "code": "candidate_set_empty_marker_conflict",
                    "field": label,
                    "occurrence_indexes": empty_marker_conflicts,
                }
            )
        if declaration["repetition"] == "CONFLICTING":
            advisories.append(
                {
                    "code": "candidate_set_declaration_conflict",
                    "field": label,
                    "occurrence_count": declaration["occurrence_count"],
                }
            )
        elif declaration["occurrence_count"] > 1:
            advisories.append(
                {
                    "code": "candidate_set_declaration_repeated",
                    "field": label,
                    "occurrence_count": declaration["occurrence_count"],
                    "repetition": declaration["repetition"],
                }
            )

    pairwise_comparisons = [
        _pairwise_comparison_fact(workspace, record, index)
        for index, record in enumerate(
            (
                item
                for item in best_blocks
                if item["marker"] == "PAIRWISE_COMPARISON"
            ),
            start=1,
        )
    ]
    pairwise_group_advisories = _reconcile_pairwise_comparisons(
        pairwise_comparisons
    )
    for pair in pairwise_comparisons:
        advisories.extend(pair["advisories"])
    advisories.extend(pairwise_group_advisories)

    admission_contracts = [
        _contract_fact(item, _CANDIDATE_ADMISSION_FIELDS, index)
        for index, item in enumerate(
            (
                record
                for record in best_blocks
                if record["marker"] == "CANDIDATE_ADMISSION"
            ),
            start=1,
        )
    ]
    reward_contracts = [
        _contract_fact(item, _LOCAL_REWARD_FIELDS, index)
        for index, item in enumerate(
            (
                record
                for record in best_blocks
                if record["marker"] == "LOCAL_REWARD_CONTRACT"
            ),
            start=1,
        )
    ]
    evidence_roles = [
        _evidence_role_fact(workspace, item, index)
        for index, item in enumerate(
            (record for record in best_blocks if record["marker"] == "EVIDENCE_ROLE"),
            start=1,
        )
    ]
    for item in [*admission_contracts, *reward_contracts, *evidence_roles]:
        advisories.extend(item["advisories"])
    for item in evidence_roles:
        if item["reference_relationship"] == "OVERLAP":
            advisories.append(
                {
                    "code": "development_and_admission_evidence_overlap",
                    "candidate_id": item["candidate_id"],
                    "overlapping_references": item["overlapping_references"],
                }
            )

    implementations = [
        _independent_implementation_fact(workspace, item, index)
        for index, item in enumerate(
            (
                record
                for record in best_blocks
                if record["marker"] == "INDEPENDENT_IMPLEMENTATION"
            ),
            start=1,
        )
    ]
    for item in implementations:
        advisories.extend(item["advisories"])
    implementation_summaries = _implementation_summaries(implementations)
    for item in implementations:
        if "duplicate_artifact_record_index" in item:
            advisories.append(
                {
                    "code": "duplicate_implementation_artifact_bytes",
                    "candidate_id": item["candidate_id"],
                    "record_index": item["record_index"],
                    "duplicate_of_record_index": item[
                        "duplicate_artifact_record_index"
                    ],
                    "artifact_sha256": item["fields"]["ARTIFACT_PATH"]["sha256"],
                }
            )
    exceptions = [
        _implementation_lottery_exception_fact(workspace, item, index)
        for index, item in enumerate(
            (
                record
                for record in best_blocks
                if record["marker"] == "IMPLEMENTATION_LOTTERY_EXCEPTION"
            ),
            start=1,
        )
    ]
    for item in exceptions:
        advisories.extend(item["advisories"])
        if not item["valid"]:
            advisories.append(
                {
                    "code": "implementation_lottery_exception_incomplete_or_unverified",
                    "candidate_id": item["candidate_id"],
                    "record_index": item["record_index"],
                }
            )

    preference_updates = [
        _preference_update_fact(workspace, item, index)
        for index, item in enumerate(
            (
                record
                for record in strategy_blocks
                if record["marker"] == "PREFERENCE_UPDATE"
            ),
            start=1,
        )
    ]
    preference_update_group_advisories = _reconcile_preference_updates(
        preference_updates
    )
    for item in preference_updates:
        advisories.extend(item["advisories"])
    advisories.extend(preference_update_group_advisories)
    preference_stagnation = _preference_stagnation_fact(preference_updates)

    active_candidate_ids = _ordered_unique(
        [
            *incumbent_set["candidate_ids"],
            *challengers["candidate_ids"],
        ]
    )
    overlap = sorted(
        set(incumbent_set["candidate_ids"]) & set(challengers["candidate_ids"])
    )
    if overlap:
        advisories.append(
            {
                "code": "candidate_declared_as_incumbent_and_challenger",
                "candidate_ids": overlap,
            }
        )

    admission_by_candidate = _records_by_candidate(admission_contracts)
    reward_by_candidate = _records_by_candidate(reward_contracts)
    evidence_by_candidate = _records_by_candidate(evidence_roles)
    implementation_by_candidate = _records_by_candidate(implementations)
    local_activity_candidates = _local_activity_candidate_ids(
        workspace, implementations, reward_contracts
    )
    for candidate_id in active_candidate_ids:
        admissions = admission_by_candidate.get(candidate_id, [])
        if not admissions:
            advisories.append(
                {
                    "code": "candidate_admission_contract_missing",
                    "candidate_id": candidate_id,
                }
            )
        else:
            _append_contract_advisories(
                advisories, candidate_id, admissions, "candidate_admission"
            )
        if len(admissions) > 1:
            advisories.append(
                {
                    "code": "duplicate_candidate_admission_contract",
                    "candidate_id": candidate_id,
                    "record_count": len(admissions),
                }
            )

        if not evidence_by_candidate.get(candidate_id):
            advisories.append(
                {
                    "code": "candidate_evidence_role_declaration_missing",
                    "candidate_id": candidate_id,
                }
            )

        if candidate_id in local_activity_candidates:
            rewards = reward_by_candidate.get(candidate_id, [])
            if not rewards:
                advisories.append(
                    {
                        "code": "local_reward_contract_missing_for_local_activity",
                        "candidate_id": candidate_id,
                    }
                )
            else:
                _append_contract_advisories(
                    advisories, candidate_id, rewards, "local_reward"
                )

        for item in implementation_by_candidate.get(candidate_id, []):
            if not item["declaration_complete"]:
                advisories.append(
                    {
                        "code": "independent_implementation_declaration_incomplete",
                        "candidate_id": candidate_id,
                        "record_index": item["record_index"],
                        "missing_fields": item["missing_fields"],
                    }
                )
            elif not item["artifact_files_verified"]:
                advisories.append(
                    {
                        "code": "independent_implementation_trace_unverified",
                        "candidate_id": candidate_id,
                        "record_index": item["record_index"],
                    }
                )

    single_implementation_risks = _pairwise_implementation_risks(
        pairwise_comparisons, implementation_summaries, exceptions
    )
    has_structured_declaration = bool(
        incumbent_set["occurrence_count"]
        or challengers["occurrence_count"]
        or best_blocks
        or preference_updates
    )
    if not has_structured_declaration:
        status = "UNAVAILABLE"
        reason = "no_structured_candidate_preference_declarations"
    elif (
        incumbent_set["status"]
        in _UNRESOLVED_DECLARATIONS | {"UNAVAILABLE", "AMBIGUOUS"}
        or challengers["status"]
        in _UNRESOLVED_DECLARATIONS | {"UNAVAILABLE", "AMBIGUOUS"}
    ):
        status = "PARTIAL"
        reason = "candidate_sets_unavailable_or_unresolved"
    else:
        status = "READY"
        reason = None
    return {
        "status": status,
        "reason": reason,
        "incumbent_set": incumbent_set,
        "challengers": challengers,
        "active_candidate_ids": active_candidate_ids,
        "pairwise_comparison_count": len(pairwise_comparisons),
        "pairwise_comparisons": pairwise_comparisons,
        "candidate_admission_contract_count": len(admission_contracts),
        "candidate_admission_contracts": admission_contracts,
        "local_reward_contract_count": len(reward_contracts),
        "local_reward_contracts": reward_contracts,
        "evidence_role_count": len(evidence_roles),
        "evidence_roles": evidence_roles,
        "independent_implementation_record_count": len(implementations),
        "independent_implementations": implementations,
        "independent_implementation_summaries": implementation_summaries,
        "implementation_lottery_exception_count": len(exceptions),
        "implementation_lottery_exceptions": exceptions,
        "preference_update_count": len(preference_updates),
        "preference_updates": preference_updates,
        "preference_stagnation": preference_stagnation,
        "advisory_count": len(advisories),
        "advisories": advisories,
        "single_implementation_idea_level_risk_count": len(
            single_implementation_risks
        ),
        "single_implementation_idea_level_risks": single_implementation_risks,
    }


def _markdown_data_lines(text: str) -> list[str]:
    output = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        if fence_match is not None:
            fence = fence_match.group(1)[0] * len(fence_match.group(1))
            continue
        output.append(line)
    return output


def _label_match(line: str) -> re.Match[str] | None:
    return re.match(
        r"^\s*(?:[-*+]\s+)?([A-Z][A-Z0-9_]*):\s*(.*?)\s*$", line
    )


def _structured_markdown_blocks(text: str) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in _markdown_data_lines(text):
        match = _label_match(line)
        if match is None:
            continue
        label, value = match.groups()
        if label in _STRUCTURED_BLOCK_MARKERS:
            if current is not None:
                records.append(current)
            current = {
                "marker": label,
                "subject": _clean_declared_value(value) or None,
                "fields": {},
            }
            continue
        if current is not None:
            fields = current["fields"]
            assert isinstance(fields, dict)
            occurrences = fields.setdefault(label, [])
            assert isinstance(occurrences, list)
            occurrences.append(_clean_declared_value(value) or None)
    if current is not None:
        records.append(current)
    return records


def _candidate_set_declaration(text: str, label: str) -> dict[str, object]:
    lines = _markdown_data_lines(text)
    declarations: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        match = _label_match(lines[index])
        if match is None or match.group(1) != label:
            index += 1
            continue
        values: list[str] = []
        inline = _clean_declared_value(match.group(2))
        if inline:
            values.extend(_split_declared_values(inline))
        index += 1
        while index < len(lines):
            next_match = _label_match(lines[index])
            if next_match is not None:
                break
            bullet = re.match(r"^\s*[-*+]\s+(.+?)\s*$", lines[index])
            if bullet is not None:
                values.extend(_split_declared_values(bullet.group(1)))
            index += 1
        declarations.append(
            {
                "occurrence_index": len(declarations) + 1,
                **_candidate_set_occurrence(values),
            }
        )
    if not declarations:
        return {
            "status": "UNAVAILABLE",
            "candidate_ids": [],
            "raw_values": [],
            "occurrence_count": 0,
            "declarations": [],
            "repetition": "NONE",
        }
    signatures = {
        (
            item["status"],
            tuple(sorted(str(value) for value in item["candidate_ids"])),
            tuple(sorted(str(value).upper() for value in item["raw_values"])),
        )
        for item in declarations
    }
    exact_signatures = {
        tuple(str(value) for value in item["raw_values"]) for item in declarations
    }
    conflict = len(signatures) > 1
    canonical = declarations[0]
    repetition = (
        "CONFLICTING"
        if conflict
        else "IDENTICAL"
        if len(declarations) > 1 and len(exact_signatures) == 1
        else "EQUIVALENT"
        if len(declarations) > 1
        else "NONE"
    )
    return {
        "status": "AMBIGUOUS" if conflict else canonical["status"],
        "candidate_ids": [] if conflict else canonical["candidate_ids"],
        "raw_values": [] if conflict else canonical["raw_values"],
        "occurrence_count": len(declarations),
        "declarations": declarations,
        "repetition": repetition,
    }


def _candidate_set_occurrence(values: list[str]) -> dict[str, object]:
    raw_values = _ordered_unique(item for item in values if item)
    candidate_ids = [
        item
        for item in raw_values
        if item.upper()
        not in _UNRESOLVED_DECLARATIONS | _EMPTY_SET_DECLARATIONS
    ]
    declarations = {item.upper() for item in raw_values}
    empty_marker_conflict = bool(
        candidate_ids and declarations & _EMPTY_SET_DECLARATIONS
    )
    if empty_marker_conflict:
        status = "AMBIGUOUS"
        candidate_ids = []
    elif candidate_ids:
        status = "PARTIAL" if declarations & _UNRESOLVED_DECLARATIONS else "PRESENT"
    elif declarations & _UNRESOLVED_DECLARATIONS:
        status = next(
            item
            for item in ("UNAVAILABLE", "UNKNOWN", "INSUFFICIENT")
            if item in declarations
        )
    elif declarations and declarations <= _EMPTY_SET_DECLARATIONS:
        status = "EMPTY"
    else:
        status = "UNAVAILABLE"
    return {
        "status": status,
        "candidate_ids": candidate_ids,
        "raw_values": raw_values,
        "conflict_reason": (
            "empty_marker_mixed_with_candidate_ids"
            if empty_marker_conflict
            else None
        ),
    }


def _clean_declared_value(value: object) -> str:
    if not isinstance(value, str):
        return ""
    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in "`\"'":
        cleaned = cleaned[1:-1].strip()
    return cleaned


def _split_declared_values(value: str) -> list[str]:
    cleaned = _clean_declared_value(value)
    if len(cleaned) >= 2 and cleaned[0] == "[" and cleaned[-1] == "]":
        cleaned = cleaned[1:-1].strip()
    return [
        item
        for part in re.split(r"[,，;；|]", cleaned)
        if (item := _clean_declared_value(part))
    ]


def _ordered_unique(values: Iterable[str]) -> list[str]:
    output = []
    seen = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def _record_subject_fact(record: dict[str, object]) -> dict[str, object]:
    values: list[object] = []
    subject = _clean_declared_value(record.get("subject"))
    if subject:
        values.append(subject)
    fields = record.get("fields")
    if isinstance(fields, dict):
        candidate_occurrences = fields.get("CANDIDATE_ID", [])
        if isinstance(candidate_occurrences, list):
            values.extend(candidate_occurrences)
    return _field_fact(values)


def _record_subject(record: dict[str, object]) -> str | None:
    fact = _record_subject_fact(record)
    value = fact["value"] if fact["status"] == "PRESENT" else None
    return str(value) if value is not None else None


def _field_fact(
    value: object,
    *,
    conflict_normalizer: Callable[[str], str] | None = None,
) -> dict[str, object]:
    raw_occurrences = (
        list(value) if isinstance(value, list) else ([] if value is None else [value])
    )
    occurrences = [(_clean_declared_value(item) or None) for item in raw_occurrences]

    def semantic_key(item: str | None) -> str | None:
        if item is None:
            return None
        upper = item.upper()
        if upper in _UNRESOLVED_DECLARATIONS | _EMPTY_SET_DECLARATIONS:
            return upper
        return conflict_normalizer(item) if conflict_normalizer is not None else item

    semantic_values = _ordered_unique_object(semantic_key(item) for item in occurrences)
    exact_values = _ordered_unique_object(occurrences)
    conflict = len(semantic_values) > 1
    repetition = (
        "CONFLICTING"
        if conflict
        else "IDENTICAL"
        if len(occurrences) > 1 and len(exact_values) == 1
        else "EQUIVALENT"
        if len(occurrences) > 1
        else "NONE"
    )
    base = {
        "occurrence_count": len(occurrences),
        "occurrences": occurrences,
        "repetition": repetition,
    }
    if conflict:
        return {**base, "status": "AMBIGUOUS", "value": None}
    cleaned = occurrences[0] if occurrences else None
    if not cleaned:
        return {**base, "status": "UNAVAILABLE", "value": None}
    upper = cleaned.upper()
    if upper in _UNRESOLVED_DECLARATIONS | _EMPTY_SET_DECLARATIONS:
        return {**base, "status": upper, "value": cleaned}
    return {**base, "status": "PRESENT", "value": cleaned}


def _ordered_unique_object(values: Iterable[object]) -> list[object]:
    output: list[object] = []
    for value in values:
        if value not in output:
            output.append(value)
    return output


def _record_field_fact(
    record: dict[str, object],
    name: str,
    *,
    conflict_normalizer: Callable[[str], str] | None = None,
) -> dict[str, object]:
    raw_fields = record["fields"]
    assert isinstance(raw_fields, dict)
    return _field_fact(
        raw_fields.get(name, []), conflict_normalizer=conflict_normalizer
    )


def _record_repetition_advisories(
    record: dict[str, object],
    facts: dict[str, dict[str, object]],
    *,
    record_index: int,
    candidate_id: str | None = None,
) -> list[dict[str, object]]:
    advisories = []
    for field_name, fact in facts.items():
        repetition = fact.get("repetition")
        if repetition not in {"CONFLICTING", "IDENTICAL", "EQUIVALENT"}:
            continue
        code = (
            "structured_field_conflict"
            if repetition == "CONFLICTING"
            else "structured_field_repeated_identical"
            if repetition == "IDENTICAL"
            else "structured_field_repeated_equivalent"
        )
        advisory: dict[str, object] = {
            "code": code,
            "marker": record["marker"],
            "record_index": record_index,
            "field": field_name,
            "occurrence_count": fact["occurrence_count"],
        }
        if candidate_id is not None:
            advisory["candidate_id"] = candidate_id
        advisories.append(advisory)
    return advisories


def _block_status(
    subject: dict[str, object], fields: dict[str, dict[str, object]]
) -> str:
    statuses = [subject["status"], *(item["status"] for item in fields.values())]
    if "AMBIGUOUS" in statuses:
        return "AMBIGUOUS"
    if any(status in {"INVALID", "UNVERIFIED"} for status in statuses):
        return "UNKNOWN"
    if any(
        status in _UNRESOLVED_DECLARATIONS | _EMPTY_SET_DECLARATIONS
        for status in statuses
    ):
        return "PARTIAL"
    return "PRESENT"


def _contract_fact(
    record: dict[str, object], required_fields: tuple[str, ...], index: int
) -> dict[str, object]:
    subject = _record_subject_fact(record)
    fields = {name: _record_field_fact(record, name) for name in required_fields}
    missing = [name for name, item in fields.items() if item["status"] == "UNAVAILABLE"]
    unresolved = [
        name
        for name, item in fields.items()
        if item["status"] in _UNRESOLVED_DECLARATIONS | {"AMBIGUOUS"}
    ]
    candidate_id = _record_subject(record)
    advisories = _record_repetition_advisories(
        record,
        {"CANDIDATE_ID": subject, **fields},
        record_index=index,
        candidate_id=candidate_id,
    )
    return {
        "record_index": index,
        "status": _block_status(subject, fields),
        "candidate_id": candidate_id,
        "candidate_id_fact": subject,
        "fields": fields,
        "missing_fields": missing,
        "unresolved_fields": unresolved,
        "declared_complete": not missing and subject["status"] != "UNAVAILABLE",
        "resolved_complete": not missing and not unresolved and subject["status"] == "PRESENT",
        "advisories": advisories,
    }


def _pairwise_comparison_fact(
    workspace: ResearchWorkspace, record: dict[str, object], index: int
) -> dict[str, object]:
    pair_fact = _record_field_fact(record, "PAIR")
    verdict_fact = _record_field_fact(
        record, "VERDICT", conflict_normalizer=str.upper
    )
    pair_value = str(pair_fact["value"] or "")
    pair = _pair_candidates(pair_value)
    verdict = str(verdict_fact["value"] or "").upper()
    verdict_status = (
        "AMBIGUOUS"
        if verdict_fact["status"] == "AMBIGUOUS"
        else "PRESENT"
        if verdict in _PREFERENCE_VERDICTS
        else "UNAVAILABLE"
        if not verdict
        else "INVALID"
    )
    fields = {
        "DECISIVE_EVIDENCE": _evidence_path_field_fact(
            workspace, record, "DECISIVE_EVIDENCE"
        ),
        **{
            name: _record_field_fact(record, name)
            for name in (
                "A_SURVIVING_ADVANTAGES",
                "B_SURVIVING_ADVANTAGES",
                "SURVIVING_FATAL_UNCERTAINTIES",
                "REVERSAL_CONDITION",
                "NEXT_DISCRIMINATING_ACTION",
            )
        },
    }
    all_fields = {"PAIR": pair_fact, "VERDICT": verdict_fact, **fields}
    advisories = _record_repetition_advisories(
        record, all_fields, record_index=index
    )
    advisories.extend(
        _unverified_path_advisories(
            fields["DECISIVE_EVIDENCE"],
            marker=str(record["marker"]),
            record_index=index,
            field_name="DECISIVE_EVIDENCE",
        )
    )
    if pair is None:
        advisories.append(
            {"code": "pairwise_pair_unavailable_or_invalid", "pair_index": index}
        )
    if verdict_status != "PRESENT":
        advisories.append(
            {
                "code": "pairwise_verdict_unavailable_or_invalid",
                "pair_index": index,
            }
        )
    for field in (
        "DECISIVE_EVIDENCE",
        "SURVIVING_FATAL_UNCERTAINTIES",
        "REVERSAL_CONDITION",
        "NEXT_DISCRIMINATING_ACTION",
    ):
        if fields[field]["status"] not in {"PRESENT", "NOT_APPLICABLE"}:
            advisories.append(
                {
                    "code": "pairwise_required_field_unresolved",
                    "pair_index": index,
                    "field": field,
                    "field_status": fields[field]["status"],
                }
            )
    a_id = pair[0] if pair is not None else None
    b_id = pair[1] if pair is not None else None
    ambiguous = any(item["status"] == "AMBIGUOUS" for item in all_fields.values())
    declared_verdict = verdict if verdict_status == "PRESENT" else None
    declared_outcome = _normalized_preference_outcome(pair, declared_verdict)
    declared_preferred_candidate_id = (
        declared_outcome.removeprefix("PREFERRED::")
        if declared_outcome is not None
        and declared_outcome.startswith("PREFERRED::")
        else None
    )
    required_fields_parseable = bool(
        fields["DECISIVE_EVIDENCE"]["status"] == "PRESENT"
        and all(
            fields[name]["status"] in {"PRESENT", "NOT_APPLICABLE"}
            for name in (
                "SURVIVING_FATAL_UNCERTAINTIES",
                "REVERSAL_CONDITION",
                "NEXT_DISCRIMINATING_ACTION",
            )
        )
    )
    preferred_verdict = declared_verdict in {"A_PREFERRED", "B_PREFERRED"}
    mechanically_supported_winner = bool(
        preferred_verdict
        and pair is not None
        and not ambiguous
        and required_fields_parseable
    )
    winner = (
        declared_preferred_candidate_id if mechanically_supported_winner else None
    )
    if preferred_verdict and not mechanically_supported_winner:
        advisories.append(
            {
                "code": "pairwise_preferred_verdict_not_mechanically_supported",
                "pair_index": index,
                "required_fields_parseable": required_fields_parseable,
                "decisive_evidence_status": fields["DECISIVE_EVIDENCE"]["status"],
            }
        )
    return {
        "pair_index": index,
        "status": (
            "AMBIGUOUS"
            if ambiguous
            else "UNKNOWN"
            if preferred_verdict and not mechanically_supported_winner
            else "PRESENT"
            if pair is not None and verdict_status == "PRESENT"
            else "UNKNOWN"
        ),
        "pair": pair_value or None,
        "pair_fact": pair_fact,
        "a_candidate_id": a_id,
        "b_candidate_id": b_id,
        "normalized_pair": (
            list(_normalized_candidate_pair(pair)) if pair is not None else None
        ),
        "verdict": declared_verdict,
        "verdict_fact": verdict_fact,
        "verdict_status": verdict_status,
        "normalized_declared_outcome": declared_outcome,
        "declared_preferred_candidate_id": declared_preferred_candidate_id,
        "required_fields_parseable": required_fields_parseable,
        "mechanically_usable_for_inference": mechanically_supported_winner,
        "winner_candidate_id": winner,
        "fields": fields,
        "advisories": advisories,
    }


def _pair_candidates(value: str) -> tuple[str, str] | None:
    if not value:
        return None
    parts = re.split(r"\s*\|\s*", value)
    if len(parts) != 2:
        parts = re.split(r"\s+(?:VS\.?|VERSUS)\s+", value, flags=re.I)
    cleaned = tuple(_clean_declared_value(item) for item in parts)
    if len(cleaned) != 2 or not all(cleaned):
        return None
    return cleaned[0], cleaned[1]


def _normalized_candidate_pair(pair: tuple[str, str]) -> tuple[str, str]:
    return tuple(sorted(pair, key=lambda item: (item.casefold(), item)))


def _normalized_preference_outcome(
    pair: tuple[str, str] | None, verdict: str | None
) -> str | None:
    if pair is None or verdict not in _PREFERENCE_VERDICTS:
        return None
    if verdict == "A_PREFERRED":
        return f"PREFERRED::{pair[0]}"
    if verdict == "B_PREFERRED":
        return f"PREFERRED::{pair[1]}"
    return verdict


def _reconcile_pairwise_comparisons(
    comparisons: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[dict[str, object]]] = {}
    for comparison in comparisons:
        normalized_pair = comparison.get("normalized_pair")
        if not isinstance(normalized_pair, list) or len(normalized_pair) != 2:
            continue
        groups.setdefault(
            (str(normalized_pair[0]), str(normalized_pair[1])), []
        ).append(comparison)

    advisories: list[dict[str, object]] = []
    for pair, records in groups.items():
        if len(records) < 2:
            continue
        outcomes = {
            str(outcome)
            for item in records
            if (outcome := item.get("normalized_declared_outcome")) is not None
        }
        record_indexes = [item["pair_index"] for item in records]
        if len(outcomes) > 1:
            for item in records:
                item["status"] = "AMBIGUOUS"
                item["winner_candidate_id"] = None
                item["mechanically_usable_for_inference"] = False
            advisories.append(
                {
                    "code": "pairwise_group_verdict_conflict",
                    "normalized_pair": list(pair),
                    "pair_indexes": record_indexes,
                    "normalized_declared_outcomes": sorted(outcomes),
                }
            )
        elif len(outcomes) == 1 and all(
            item.get("normalized_declared_outcome") is not None for item in records
        ):
            advisories.append(
                {
                    "code": "pairwise_group_repeated_same_verdict",
                    "normalized_pair": list(pair),
                    "pair_indexes": record_indexes,
                    "normalized_declared_outcome": next(iter(outcomes)),
                }
            )
        else:
            advisories.append(
                {
                    "code": "pairwise_group_repeated_with_unresolved_verdict",
                    "normalized_pair": list(pair),
                    "pair_indexes": record_indexes,
                }
            )
    return advisories


def _evidence_role_fact(
    workspace: ResearchWorkspace, record: dict[str, object], index: int
) -> dict[str, object]:
    subject = _record_subject_fact(record)
    development = _reference_field_fact(workspace, record, "DEVELOPMENT_EVIDENCE")
    admission = _reference_field_fact(workspace, record, "ADMISSION_EVIDENCE")
    overlap = sorted(set(development["references"]) & set(admission["references"]))
    ambiguous = any(
        item["status"] == "AMBIGUOUS" for item in (development, admission)
    ) or subject["status"] == "AMBIGUOUS"
    unverified = any(
        item.get("verification_status") == "UNVERIFIED"
        for item in (development, admission)
    )
    if ambiguous:
        relationship = "UNKNOWN"
    elif overlap:
        relationship = "OVERLAP"
    elif development["references"] and admission["references"] and not unverified:
        relationship = "DISTINCT_DECLARATIONS"
    elif development["references"] and admission["references"]:
        relationship = "UNKNOWN"
    elif (
        development["status"] == "NOT_APPLICABLE"
        or admission["status"] == "NOT_APPLICABLE"
    ):
        relationship = "NOT_APPLICABLE"
    else:
        relationship = "UNAVAILABLE"
    candidate_id = _record_subject(record)
    fields = {
        "DEVELOPMENT_EVIDENCE": development,
        "ADMISSION_EVIDENCE": admission,
    }
    advisories = _record_repetition_advisories(
        record,
        {"CANDIDATE_ID": subject, **fields},
        record_index=index,
        candidate_id=candidate_id,
    )
    for field_name, field in fields.items():
        advisories.extend(
            _unverified_path_advisories(
                field,
                marker=str(record["marker"]),
                record_index=index,
                field_name=field_name,
                candidate_id=candidate_id,
            )
        )
    return {
        "record_index": index,
        "status": (
            "AMBIGUOUS" if ambiguous else "UNKNOWN" if unverified else "PRESENT"
        ),
        "candidate_id": candidate_id,
        "candidate_id_fact": subject,
        "development_evidence": development,
        "admission_evidence": admission,
        "reference_relationship": relationship,
        "overlapping_references": overlap,
        "interpretation_policy": (
            "declared_references_and_verified_files_do_not_establish_scientific_independence"
        ),
        "advisories": advisories,
    }


def _reference_field_fact(
    workspace: ResearchWorkspace, record: dict[str, object], name: str
) -> dict[str, object]:
    field = _evidence_path_field_fact(workspace, record, name)
    return {
        **field,
        "references": (
            _split_declared_values(str(field["value"]))
            if field.get("declared_status", field["status"]) == "PRESENT"
            else []
        ),
    }


def _evidence_path_field_fact(
    workspace: ResearchWorkspace, record: dict[str, object], name: str
) -> dict[str, object]:
    field = _record_field_fact(record, name)
    if field["status"] != "PRESENT":
        return {**field, "entries": [], "verification_status": field["status"]}
    entries = [
        _evidence_reference_fact(workspace, item)
        for item in _split_declared_values(str(field["value"]))
    ]
    unverified = any(item["status"] == "UNVERIFIED" for item in entries)
    return {
        **field,
        "status": "UNVERIFIED" if unverified else field["status"],
        "declared_status": field["status"],
        "entries": entries,
        "verification_status": (
            "UNVERIFIED" if unverified else "VERIFIED_OR_DECLARED_TEXT"
        ),
    }


def _evidence_reference_fact(
    workspace: ResearchWorkspace, value: str
) -> dict[str, object]:
    path_value = _run_path_declaration(workspace, value)
    if path_value is None:
        return {
            "kind": "DECLARED_TEXT",
            "status": "DECLARED_TEXT",
            "value": value,
        }
    try:
        safe = workspace.assert_read_target(path_value)
        data = safe.read_bytes()
    except (FileNotFoundError, OSError, ValueError) as error:
        return {
            "kind": "RUN_LOCAL_PATH",
            "status": "UNVERIFIED",
            "value": path_value,
            "declared_value": value,
            "reason": type(error).__name__,
        }
    return {
        "kind": "RUN_LOCAL_PATH",
        "status": "VERIFIED_FILE",
        "value": safe.relative_to(workspace.workspace_path).as_posix(),
        "declared_value": value,
        "size_bytes": len(data),
        "sha256": _sha256(data),
    }


def _run_path_declaration(workspace: ResearchWorkspace, value: str) -> str | None:
    cleaned = _clean_declared_value(value)
    markdown_link = re.fullmatch(r"\[[^\]]+\]\(([^)]+)\)", cleaned)
    candidate = _clean_declared_value(markdown_link.group(1)) if markdown_link else cleaned
    if not candidate:
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*://", candidate, flags=re.I):
        return None
    if re.match(r"^(?:doi:\s*)?10\.\d{4,9}/\S+$", candidate, flags=re.I):
        return None
    if re.match(
        r"^(?:arxiv:\s*)?\d{4}\.\d{4,5}(?:v\d+)?$", candidate, flags=re.I
    ):
        return None
    if re.match(r"^(?:pmid|isbn):\s*\S+$", candidate, flags=re.I):
        return None
    if Path(candidate).is_absolute() or re.match(r"^[A-Za-z]:[\\/]", candidate):
        return candidate
    if candidate.startswith(("./", ".\\", "../", "..\\")):
        return candidate
    if "/" in candidate or "\\" in candidate:
        return candidate
    if re.search(r"\.[A-Za-z0-9]{1,12}$", candidate):
        return candidate
    if (workspace.workspace_path / candidate).exists():
        return candidate
    return None


def _unverified_path_advisories(
    field: dict[str, object],
    *,
    marker: str,
    record_index: int,
    field_name: str,
    candidate_id: str | None = None,
) -> list[dict[str, object]]:
    advisories = []
    for entry in field.get("entries", []):
        if not isinstance(entry, dict) or entry.get("status") != "UNVERIFIED":
            continue
        advisory: dict[str, object] = {
            "code": "declared_run_path_unverified",
            "marker": marker,
            "record_index": record_index,
            "field": field_name,
            "path": entry.get("value"),
            "reason": entry.get("reason"),
        }
        if candidate_id is not None:
            advisory["candidate_id"] = candidate_id
        advisories.append(advisory)
    return advisories


def _trace_path_fact(
    workspace: ResearchWorkspace, field: dict[str, object]
) -> dict[str, object]:
    if field["status"] != "PRESENT":
        return {
            **field,
            "verification_status": "UNVERIFIED",
            "evidence_class": "UNVERIFIED_ARTIFACT",
            "sha256": None,
            "size_bytes": None,
        }
    try:
        safe = workspace.assert_read_target(str(field["value"]))
        data = safe.read_bytes()
    except (FileNotFoundError, OSError, ValueError) as error:
        return {
            **field,
            "status": "UNVERIFIED",
            "verification_status": "UNVERIFIED",
            "evidence_class": "UNVERIFIED_ARTIFACT",
            "sha256": None,
            "size_bytes": None,
            "reason": type(error).__name__,
        }
    return {
        **field,
        "status": "PRESENT",
        "value": safe.relative_to(workspace.workspace_path).as_posix(),
        "verification_status": "VERIFIED_ARTIFACT",
        "evidence_class": "VERIFIED_ARTIFACT",
        "sha256": _sha256(data),
        "size_bytes": len(data),
    }


def _independent_implementation_fact(
    workspace: ResearchWorkspace, record: dict[str, object], index: int
) -> dict[str, object]:
    subject = _record_subject_fact(record)
    fields = {
        name: (
            _trace_path_fact(workspace, _record_field_fact(record, name))
            if name
            in {"ARTIFACT_PATH", "FROZEN_CANDIDATE_PATH", "FIDELITY_CHECK_PATH"}
            else {
                **_record_field_fact(record, name),
                "evidence_class": "DECLARED_SESSION",
                "scientific_independence_certified": False,
            }
            if name == "FRESH_SESSION_ID"
            else _record_field_fact(record, name)
        )
        for name in _INDEPENDENT_IMPLEMENTATION_FIELDS
    }
    missing = [name for name, item in fields.items() if item["status"] == "UNAVAILABLE"]
    unresolved = [
        name
        for name, item in fields.items()
        if item["status"] in _UNRESOLVED_DECLARATIONS | {"AMBIGUOUS", "UNVERIFIED"}
    ]
    artifact_files_verified = all(
        fields[name].get("verification_status") == "VERIFIED_ARTIFACT"
        for name in {"ARTIFACT_PATH", "FROZEN_CANDIDATE_PATH", "FIDELITY_CHECK_PATH"}
    )
    candidate_id = _record_subject(record)
    advisories = _record_repetition_advisories(
        record,
        {"CANDIDATE_ID": subject, **fields},
        record_index=index,
        candidate_id=candidate_id,
    )
    return {
        "record_index": index,
        "status": _block_status(subject, fields),
        "candidate_id": candidate_id,
        "candidate_id_fact": subject,
        "fields": fields,
        "missing_fields": missing,
        "unresolved_fields": unresolved,
        "declaration_complete": not missing and subject["status"] != "UNAVAILABLE",
        "artifact_files_verified": artifact_files_verified,
        "eligible_verified_artifact_record": (
            not missing
            and not unresolved
            and artifact_files_verified
            and subject["status"] == "PRESENT"
        ),
        "counts_toward_verified_artifact_set": False,
        "scientific_independence_certified": False,
        "advisories": advisories,
    }


def _implementation_summaries(
    implementations: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_candidate = _records_by_candidate(implementations)
    summaries = []
    for candidate_id, records in by_candidate.items():
        by_frozen_card: dict[str, list[dict[str, object]]] = {}
        for record in records:
            frozen = record["fields"]["FROZEN_CANDIDATE_PATH"]
            digest = frozen.get("sha256")
            key = str(digest) if digest is not None else "UNVERIFIED"
            by_frozen_card.setdefault(key, []).append(record)
        groups = []
        for frozen_digest, group_records in by_frozen_card.items():
            selected = []
            seen_artifacts: dict[str, int] = {}
            seen_sessions = set()
            for record in group_records:
                session = record["fields"]["FRESH_SESSION_ID"]["value"]
                if session is not None:
                    seen_sessions.add(session)
                if not record["eligible_verified_artifact_record"]:
                    continue
                artifact = record["fields"]["ARTIFACT_PATH"]["sha256"]
                if artifact in seen_artifacts:
                    record["duplicate_artifact_record_index"] = seen_artifacts[artifact]
                    continue
                seen_artifacts[artifact] = int(record["record_index"])
                record["counts_toward_verified_artifact_set"] = True
                selected.append(record["record_index"])
            groups.append(
                {
                    "frozen_candidate_sha256": (
                        frozen_digest if frozen_digest != "UNVERIFIED" else None
                    ),
                    "frozen_candidate_paths": _ordered_unique(
                        str(item["fields"]["FROZEN_CANDIDATE_PATH"]["value"])
                        for item in group_records
                        if item["fields"]["FROZEN_CANDIDATE_PATH"]["value"] is not None
                    ),
                    "declared_record_count": len(group_records),
                    "verified_artifact_count": len(selected),
                    "counted_record_indexes": selected,
                    "distinct_verified_artifact_count": len(seen_artifacts),
                    "declared_session_id_count": len(seen_sessions),
                    "artifact_sha256s": sorted(seen_artifacts),
                }
            )
        verified_artifact_count = max(
            (item["verified_artifact_count"] for item in groups),
            default=0,
        )
        declared_session_id_count = max(
            (item["declared_session_id_count"] for item in groups),
            default=0,
        )
        summaries.append(
            {
                "candidate_id": candidate_id,
                "declared_record_count": len(records),
                "verified_artifact_count": verified_artifact_count,
                "declared_session_id_count": declared_session_id_count,
                "same_frozen_candidate_groups": groups,
                "counting_policy": (
                    "distinct_artifact_sha256_under_same_frozen_candidate_sha256"
                ),
                "declared_sessions_are_self_reports": True,
                "scientific_independence_certified": False,
            }
        )
    return summaries


def _implementation_lottery_exception_fact(
    workspace: ResearchWorkspace, record: dict[str, object], index: int
) -> dict[str, object]:
    subject = _record_subject_fact(record)
    type_fact = _record_field_fact(record, "TYPE", conflict_normalizer=str.upper)
    exception_type = str(type_fact["value"] or "").upper()
    reason = _record_field_fact(record, "REASON")
    evidence_path = _trace_path_fact(
        workspace, _record_field_fact(record, "EVIDENCE_PATH")
    )
    fields = {"TYPE": type_fact, "REASON": reason, "EVIDENCE_PATH": evidence_path}
    candidate_id = _record_subject(record)
    advisories = _record_repetition_advisories(
        record,
        {"CANDIDATE_ID": subject, **fields},
        record_index=index,
        candidate_id=candidate_id,
    )
    valid = bool(
        candidate_id
        and exception_type in _IMPLEMENTATION_LOTTERY_EXCEPTION_TYPES
        and reason["status"] == "PRESENT"
        and evidence_path["verification_status"] == "VERIFIED_ARTIFACT"
        and not any(item["status"] == "AMBIGUOUS" for item in fields.values())
    )
    return {
        "record_index": index,
        "status": _block_status(subject, fields),
        "candidate_id": candidate_id,
        "candidate_id_fact": subject,
        "type": exception_type or None,
        "type_status": (
            "PRESENT"
            if exception_type in _IMPLEMENTATION_LOTTERY_EXCEPTION_TYPES
            else "UNAVAILABLE"
            if not exception_type
            else "INVALID"
        ),
        "reason": reason,
        "evidence_path": evidence_path,
        "valid": valid,
        "advisories": advisories,
    }


def _preference_update_fact(
    workspace: ResearchWorkspace, record: dict[str, object], index: int
) -> dict[str, object]:
    fields = {
        name: (
            _evidence_path_field_fact(workspace, record, name)
            if name == "EVIDENCE_PATHS"
            else _record_field_fact(
                record,
                name,
                conflict_normalizer=(
                    str.upper
                    if name
                    in {
                        "VERDICT_BEFORE",
                        "VERDICT_AFTER",
                        "FATAL_UNCERTAINTY_REDUCED",
                    }
                    else None
                ),
            )
        )
        for name in _PREFERENCE_UPDATE_FIELDS
    }
    before = str(fields["VERDICT_BEFORE"]["value"] or "").upper()
    after = str(fields["VERDICT_AFTER"]["value"] or "").upper()
    reduced = str(fields["FATAL_UNCERTAINTY_REDUCED"]["value"] or "").upper()
    affected_pair = _pair_candidates(str(fields["AFFECTED_PAIR"]["value"] or ""))
    normalized_pair = (
        _normalized_candidate_pair(affected_pair)
        if affected_pair is not None
        else None
    )
    before_outcome = _normalized_preference_outcome(
        affected_pair, before if before in _PREFERENCE_VERDICTS else None
    )
    after_outcome = _normalized_preference_outcome(
        affected_pair, after if after in _PREFERENCE_VERDICTS else None
    )
    ambiguous = any(item["status"] == "AMBIGUOUS" for item in fields.values())
    evaluable = bool(
        not ambiguous
        and fields["ACTION_ID"]["status"] == "PRESENT"
        and fields["AFFECTED_PAIR"]["status"] == "PRESENT"
        and affected_pair is not None
        and before in _PREFERENCE_VERDICTS
        and after in _PREFERENCE_VERDICTS
        and reduced in {"YES", "NO"}
        and fields["EVIDENCE_PATHS"]["status"] == "PRESENT"
    )
    advisories = _record_repetition_advisories(
        record, fields, record_index=index
    )
    advisories.extend(
        _unverified_path_advisories(
            fields["EVIDENCE_PATHS"],
            marker=str(record["marker"]),
            record_index=index,
            field_name="EVIDENCE_PATHS",
        )
    )
    if fields["EVIDENCE_PATHS"]["status"] == "UNVERIFIED":
        advisories.append(
            {
                "code": "preference_update_unverified_evidence_not_evaluable",
                "record_index": index,
            }
        )
    return {
        "record_index": index,
        "status": (
            "AMBIGUOUS" if ambiguous else "PRESENT" if evaluable else "UNKNOWN"
        ),
        "fields": fields,
        "affected_pair_candidates": (
            list(affected_pair) if affected_pair is not None else None
        ),
        "normalized_affected_pair": (
            list(normalized_pair) if normalized_pair is not None else None
        ),
        "declared_verdict_before": (
            before if before in _PREFERENCE_VERDICTS else None
        ),
        "declared_verdict_after": after if after in _PREFERENCE_VERDICTS else None,
        "normalized_declared_outcome_before": before_outcome,
        "normalized_declared_outcome_after": after_outcome,
        "evaluable_for_stagnation": evaluable,
        "verdict_changed": before_outcome != after_outcome if evaluable else None,
        "fatal_uncertainty_reduced": reduced == "YES" if evaluable else None,
        "declared_high_information_action": True,
        "advisories": advisories,
    }


def _reconcile_preference_updates(
    updates: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups: dict[tuple[str, tuple[str, str]], list[dict[str, object]]] = {}
    for update in updates:
        action_fact = update["fields"]["ACTION_ID"]
        action_id = action_fact["value"] if action_fact["status"] == "PRESENT" else None
        normalized_pair = update.get("normalized_affected_pair")
        if (
            not isinstance(action_id, str)
            or not action_id
            or not isinstance(normalized_pair, list)
            or len(normalized_pair) != 2
        ):
            continue
        groups.setdefault(
            (action_id, (str(normalized_pair[0]), str(normalized_pair[1]))), []
        ).append(update)

    advisories: list[dict[str, object]] = []
    for (action_id, pair), records in groups.items():
        if len(records) < 2:
            continue
        signatures = {
            (
                str(before),
                str(after),
                str(reduced).upper(),
            )
            for item in records
            if (before := item.get("normalized_declared_outcome_before")) is not None
            and (after := item.get("normalized_declared_outcome_after")) is not None
            and (
                reduced := item["fields"]["FATAL_UNCERTAINTY_REDUCED"]["value"]
            )
            is not None
            and str(reduced).upper() in {"YES", "NO"}
        }
        record_indexes = [item["record_index"] for item in records]
        if len(signatures) > 1:
            for item in records:
                item["status"] = "AMBIGUOUS"
                item["evaluable_for_stagnation"] = False
                item["verdict_changed"] = None
                item["fatal_uncertainty_reduced"] = None
            advisories.append(
                {
                    "code": "preference_update_group_conflict",
                    "action_id": action_id,
                    "normalized_affected_pair": list(pair),
                    "record_indexes": record_indexes,
                }
            )
        elif len(signatures) == 1 and all(
            item.get("normalized_declared_outcome_before") is not None
            and item.get("normalized_declared_outcome_after") is not None
            and str(
                item["fields"]["FATAL_UNCERTAINTY_REDUCED"]["value"] or ""
            ).upper()
            in {"YES", "NO"}
            for item in records
        ):
            advisories.append(
                {
                    "code": "preference_update_group_repeated_same_result",
                    "action_id": action_id,
                    "normalized_affected_pair": list(pair),
                    "record_indexes": record_indexes,
                }
            )
        else:
            advisories.append(
                {
                    "code": "preference_update_group_repeated_with_unresolved_result",
                    "action_id": action_id,
                    "normalized_affected_pair": list(pair),
                    "record_indexes": record_indexes,
                }
            )
    return advisories


def _preference_stagnation_fact(
    updates: list[dict[str, object]],
) -> dict[str, object]:
    grouped: dict[str, dict[str, object]] = {}
    for item in updates:
        action_value = item["fields"]["ACTION_ID"]["value"]
        action_id = str(action_value) if action_value is not None else None
        key = action_id or f"__UNAVAILABLE_ACTION_{item['record_index']}"
        if key not in grouped:
            grouped[key] = {
                "action_id": action_id,
                "updates": [],
                "last_record_index": item["record_index"],
            }
        grouped[key]["updates"].append(item)
        grouped[key]["last_record_index"] = item["record_index"]
    ordered = sorted(grouped.values(), key=lambda item: int(item["last_record_index"]))
    latest = ordered[-3:]
    action_ids = [
        item["action_id"] if item["action_id"] is not None else "UNAVAILABLE"
        for item in latest
    ]
    last_positions = [item["last_record_index"] for item in latest]
    if len(latest) < 3:
        return {
            "assessment_status": "INSUFFICIENT_HISTORY",
            "warning": False,
            "warning_code": None,
            "evaluated_action_ids": action_ids,
            "selected_action_last_positions": last_positions,
        }
    if not all(
        all(update["evaluable_for_stagnation"] for update in item["updates"])
        for item in latest
    ):
        return {
            "assessment_status": "UNKNOWN",
            "warning": False,
            "warning_code": None,
            "evaluated_action_ids": action_ids,
            "selected_action_last_positions": last_positions,
        }
    warning = all(
        all(
            update["verdict_changed"] is False
            and update["fatal_uncertainty_reduced"] is False
            for update in item["updates"]
        )
        for item in latest
    )
    return {
        "assessment_status": "READY",
        "warning": warning,
        "warning_code": "PREFERENCE_STAGNATION_WARNING" if warning else None,
        "evaluated_action_ids": action_ids,
        "selected_action_last_positions": last_positions,
        "required_researcher_response": (
            {
                "update_selection_context": True,
                "declare_stop_repeating": True,
                "expand_contribution_coordinate": True,
                "declare_new_discriminating_action": True,
                "run_status_policy": "KEEP_ACTIVE",
            }
            if warning
            else None
        ),
    }


def _records_by_candidate(
    records: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    output: dict[str, list[dict[str, object]]] = {}
    for record in records:
        candidate_id = record.get("candidate_id")
        if isinstance(candidate_id, str) and candidate_id:
            output.setdefault(candidate_id, []).append(record)
    return output


def _append_contract_advisories(
    advisories: list[dict[str, object]],
    candidate_id: str,
    contracts: list[dict[str, object]],
    prefix: str,
) -> None:
    signatures = {
        tuple(
            (name, field["status"], field["value"])
            for name, field in contract["fields"].items()
        )
        for contract in contracts
    }
    if len(contracts) > 1:
        conflict = len(signatures) > 1
        advisories.append(
            {
                "code": (
                    f"{prefix}_contract_conflict"
                    if conflict
                    else f"{prefix}_contract_repeated_identical"
                ),
                "candidate_id": candidate_id,
                "record_count": len(contracts),
                "record_indexes": [item["record_index"] for item in contracts],
            }
        )
        if conflict:
            for contract in contracts:
                contract["status"] = "AMBIGUOUS"
                contract["resolved_complete"] = False
                contract["group_conflict"] = True
    for contract in contracts:
        if contract["missing_fields"]:
            advisories.append(
                {
                    "code": f"{prefix}_contract_fields_missing",
                    "candidate_id": candidate_id,
                    "record_index": contract["record_index"],
                    "missing_fields": contract["missing_fields"],
                }
            )
        if contract["unresolved_fields"]:
            advisories.append(
                {
                    "code": f"{prefix}_contract_fields_unresolved",
                    "candidate_id": candidate_id,
                    "record_index": contract["record_index"],
                    "unresolved_fields": contract["unresolved_fields"],
                }
            )


def _local_activity_candidate_ids(
    workspace: ResearchWorkspace,
    implementations: list[dict[str, object]],
    reward_contracts: list[dict[str, object]],
) -> set[str]:
    bindings, _ = _experiment_hypothesis_bindings(workspace)
    candidates = {
        hypothesis_id
        for hypothesis_id, tiers in bindings.items()
        if any(tiers.values())
    }
    for item in [*implementations, *reward_contracts]:
        candidate_id = item.get("candidate_id")
        if isinstance(candidate_id, str) and candidate_id:
            candidates.add(candidate_id)
    return candidates


def _pairwise_implementation_risks(
    comparisons: list[dict[str, object]],
    summaries: list[dict[str, object]],
    exceptions: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_candidate = {
        item["candidate_id"]: item
        for item in summaries
        if isinstance(item.get("candidate_id"), str)
    }
    excepted = {
        item["candidate_id"]
        for item in exceptions
        if item["valid"] and isinstance(item.get("candidate_id"), str)
    }
    risks = []
    for comparison in comparisons:
        if comparison.get("mechanically_usable_for_inference") is not True:
            continue
        winner = comparison["winner_candidate_id"]
        summary = by_candidate.get(winner)
        if winner is None or summary is None:
            continue
        verified_artifacts = summary["verified_artifact_count"]
        if (
            summary["declared_record_count"]
            and verified_artifacts < 2
            and winner not in excepted
        ):
            risks.append(
                {
                    "source": "SELECTION_CONTEXT_PAIRWISE_COMPARISON",
                    "pair_index": comparison["pair_index"],
                    "candidate_id": winner,
                    "code": "single_implementation_idea_level_preference",
                    "verified_artifact_count": verified_artifacts,
                    "scientific_independence_certified": False,
                }
            )
    return risks


def _markdown_h2_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None
    current_lines: list[str] = []
    fence: str | None = None

    def finish() -> None:
        if current_heading is not None:
            sections.setdefault(current_heading, []).append(
                "\n".join(current_lines).strip()
            )

    for line in text.splitlines():
        stripped = line.strip()
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            if current_heading is not None:
                current_lines.append(line)
            continue
        if fence_match is not None:
            fence = fence_match.group(1)[0] * len(fence_match.group(1))
            if current_heading is not None:
                current_lines.append(line)
            continue
        heading_match = re.match(r"^##(?!#)\s+(.+?)\s*#*\s*$", line)
        if heading_match is not None:
            finish()
            current_heading = heading_match.group(1).strip()
            current_lines = []
        elif current_heading is not None:
            current_lines.append(line)
    finish()
    return sections


def _hypothesis_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    bindings, binding_recovery = _experiment_hypothesis_bindings(workspace)
    statuses: Counter[str] = Counter()
    reasons: Counter[str] = Counter()
    versions = []
    schema_versions: set[int] = set()
    count = 0
    decision_count = 0
    warning_items = []
    raw_observations = []
    decision_events = []
    seen_decisions: set[tuple[object, ...]] = set()
    legacy_closed_without_decision_metadata = 0
    unparseable_portfolio_count = 0
    for path in sorted(workspace.workspace_path.glob("hypotheses_v*/portfolio.json")):
        try:
            safe = workspace.assert_read_target(path)
            value = json.loads(safe.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            unparseable_portfolio_count += 1
            continue
        try:
            portfolio = portfolio_from_mapping(value)
        except ValueError:
            unparseable_portfolio_count += 1
            records = value.get("hypotheses") if isinstance(value, dict) else None
            if not isinstance(records, list):
                continue
            versions.append(path.parent.name.removeprefix("hypotheses_"))
            for record in records:
                if not isinstance(record, dict):
                    continue
                count += 1
                statuses[str(record.get("status", "UNKNOWN"))] += 1
                reason = record.get("status_reason")
                if isinstance(reason, str) and reason.strip():
                    reasons[reason.strip()] += 1
            continue
        schema_versions.add(portfolio.schema_version)
        versions.append(path.parent.name.removeprefix("hypotheses_"))
        for record in portfolio.hypotheses:
            count += 1
            statuses[record.status] += 1
            if record.status_reason.strip():
                reasons[record.status_reason.strip()] += 1
            decision_count += len(record.decision_history)
            if (
                portfolio.schema_version == 1
                and record.status in {"falsified", "prior_collision", "escalated"}
            ):
                legacy_closed_without_decision_metadata += 1
            raw_observations.append(
                {
                    "version": portfolio.version,
                    "hypothesis_id": record.hypothesis_id,
                    "status": record.status,
                    "revision": record.revision,
                    "created_at_utc": record.created_at_utc,
                    "updated_at_utc": record.updated_at_utc,
                    "decision_count": len(record.decision_history),
                    "experiment_binding": _binding_fact(
                        bindings.get(record.hypothesis_id)
                    ),
                }
            )
            for index, event in enumerate(record.decision_history, start=1):
                decision_key = (
                    record.hypothesis_id,
                    event.decided_at_utc,
                    event.from_status,
                    event.to_status,
                    event.reason,
                )
                if decision_key not in seen_decisions:
                    seen_decisions.add(decision_key)
                    binding = _binding_fact(bindings.get(record.hypothesis_id))
                    decision_events.append(
                        {
                            "version": portfolio.version,
                            "hypothesis_id": record.hypothesis_id,
                            "decision_index": index,
                            "decided_at_utc": event.decided_at_utc,
                            "from_status": event.from_status,
                            "to_status": event.to_status,
                            "experiment_binding": binding,
                            "pre_experiment_closure": (
                                event.to_status in {"falsified", "prior_collision"}
                                and binding["any_bound"] is False
                            ),
                        }
                    )
                codes = decision_warning_codes(event)
                if codes:
                    warning_items.append(
                        {
                            "version": portfolio.version,
                            "hypothesis_id": record.hypothesis_id,
                            "decision_index": index,
                            "to_status": event.to_status,
                            "warning_codes": list(codes),
                        }
                    )
    spec_warning_items = []
    for path in sorted(workspace.workspace_path.glob("experiment_v*/specs/*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            spec = experiment_spec_from_mapping(value)
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
            continue
        codes = experiment_spec_warning_codes(spec)
        if codes:
            spec_warning_items.append(
                {
                    "version": spec.version,
                    "hypothesis_id": spec.hypothesis_id,
                    "experiment_id": spec.experiment_id,
                    "path": path.relative_to(workspace.workspace_path).as_posix(),
                    "warning_codes": list(codes),
                }
            )
    decision_events.sort(
        key=lambda item: (
            _decision_timestamp(str(item["decided_at_utc"])),
            int(str(item["version"])[1:]),
            str(item["hypothesis_id"]),
            int(item["decision_index"]),
        )
    )
    history_unknown_reasons = []
    if 1 in schema_versions:
        history_unknown_reasons.append("schema_version_1_decision_history_unavailable")
    if unparseable_portfolio_count:
        history_unknown_reasons.append("unparseable_hypothesis_portfolio")
    if binding_recovery["unresolved_record_count"]:
        history_unknown_reasons.append("experiment_binding_unrecoverable")
    if binding_recovery["invalid_spec_count"]:
        history_unknown_reasons.append("experiment_spec_unreadable")
    if history_unknown_reasons:
        streak: int | str = "UNKNOWN"
        prior_collision_streak: int | str = "UNKNOWN"
    else:
        streak = _tail_pre_experiment_closure_count(decision_events)
        prior_collision_streak = _tail_pre_experiment_closure_count(
            decision_events, prior_collision_only=True
        )
    significant_warning = isinstance(streak, int) and streak >= 5
    return {
        "hypothesis_count": count,
        "versions_with_portfolios": versions,
        "status_distribution": dict(sorted(statuses.items())),
        "status_reason_distribution": dict(sorted(reasons.items())),
        "decision_event_count": decision_count,
        "unique_ordered_decision_event_count": len(decision_events),
        "ordered_decision_events": decision_events,
        "portfolio_schema_versions": sorted(schema_versions),
        "pre_experiment_closure_streak": streak,
        "prior_collision_pre_experiment_closure_streak": prior_collision_streak,
        "pre_experiment_closure_history_status": (
            "UNKNOWN" if history_unknown_reasons else "READY"
        ),
        "pre_experiment_closure_unknown_reasons": history_unknown_reasons,
        "pre_experiment_closure_significant_warning": significant_warning,
        "pre_experiment_closure_warning_threshold": 5,
        "semantic_overreach_warning_count": len(warning_items),
        "semantic_overreach_warnings": warning_items,
        "experiment_spec_warning_count": len(spec_warning_items),
        "experiment_spec_warnings": spec_warning_items,
        "legacy_closed_without_decision_metadata": (
            legacy_closed_without_decision_metadata
        ),
        "unparseable_portfolio_count": unparseable_portfolio_count,
        "experiment_binding_recovery": binding_recovery,
        "raw_candidate_observations": raw_observations,
        "observation_policy": (
            "raw_duration_revision_and_activity_facts_are_not_quality_scores"
        ),
    }


def _experiment_hypothesis_bindings(
    workspace: ResearchWorkspace,
) -> tuple[dict[str, dict[str, list[str]]], dict[str, object]]:
    bindings: dict[str, dict[str, list[str]]] = {}
    invalid_specs = []
    unresolved_records = []
    for path in sorted(workspace.workspace_path.glob("experiment_v*/specs/*.json")):
        identity = _spec_hypothesis_identity(workspace, path)
        relative = path.relative_to(workspace.workspace_path).as_posix()
        if identity is None:
            invalid_specs.append(relative)
            continue
        _add_experiment_binding(bindings, identity[1], "specs", relative)
    for experiment_root in sorted(workspace.workspace_path.glob("experiment_v*")):
        for tier, directory_name, record_name in (
            ("recorded", "recorded", "record.json"),
            ("formal", "attempts", "execution.json"),
        ):
            root = experiment_root / directory_name
            if not root.is_dir():
                continue
            for directory in sorted(item for item in root.iterdir() if item.is_dir()):
                record_path = directory / record_name
                relative = directory.relative_to(workspace.workspace_path).as_posix()
                identity = _record_hypothesis_identity(
                    workspace, directory, record_path, tier=tier
                )
                if identity is None:
                    unresolved_records.append({"tier": tier, "path": relative})
                    continue
                _add_experiment_binding(bindings, identity[1], tier, relative)
    return bindings, {
        "status": (
            "READY" if not invalid_specs and not unresolved_records else "PARTIAL"
        ),
        "invalid_spec_count": len(invalid_specs),
        "invalid_specs": invalid_specs,
        "unresolved_record_count": len(unresolved_records),
        "unresolved_records": unresolved_records,
        "binding_policy": (
            "run_wide_explicit_hypothesis_id_or_parseable_experiment_spec_"
            "only_no_filename_guess"
        ),
    }


def _spec_hypothesis_identity(
    workspace: ResearchWorkspace, path: Path
) -> tuple[str, str] | None:
    try:
        data = _required_file(path, within=workspace.workspace_path)
        spec = experiment_spec_from_mapping(json.loads(data.decode("utf-8")))
    except (FileNotFoundError, OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return None
    return spec.version, spec.hypothesis_id


def _record_hypothesis_identity(
    workspace: ResearchWorkspace,
    directory: Path,
    record_path: Path,
    *,
    tier: str,
) -> tuple[str, str] | None:
    try:
        data = _required_file(record_path, within=workspace.workspace_path)
        record = json.loads(data.decode("utf-8"))
    except (FileNotFoundError, OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return None
    if not isinstance(record, dict):
        return None
    direct = record.get("hypothesis_id")
    record_version = record.get("version")
    if (
        isinstance(direct, str)
        and direct.strip()
        and isinstance(record_version, str)
        and re.fullmatch(r"v\d{3,}", record_version) is not None
    ):
        return record_version, direct.strip()
    candidate_paths: list[Path] = []
    if tier == "formal":
        candidate_paths.append(directory / "spec.json")
        spec_fact = record.get("experiment_spec")
        if isinstance(spec_fact, dict):
            source_path = spec_fact.get("source_path")
            if isinstance(source_path, str) and source_path.strip():
                candidate_paths.append(workspace.workspace_path / source_path)
    else:
        inputs = record.get("inputs")
        if isinstance(inputs, list):
            for item in inputs:
                value = item.get("path") if isinstance(item, dict) else None
                if isinstance(value, str) and value.strip():
                    candidate_paths.append(Path(value))
    for candidate in candidate_paths:
        path = candidate if candidate.is_absolute() else workspace.workspace_path / candidate
        if path.name == "spec.json" or path.parent.name == "specs":
            identity = _spec_hypothesis_identity(workspace, path)
            if identity is not None:
                return identity
    return None


def _add_experiment_binding(
    bindings: dict[str, dict[str, list[str]]],
    hypothesis_id: str,
    tier: str,
    path: str,
) -> None:
    item = bindings.setdefault(
        hypothesis_id, {"specs": [], "recorded": [], "formal": []}
    )
    if path not in item[tier]:
        item[tier].append(path)


def _binding_fact(value: dict[str, list[str]] | None) -> dict[str, object]:
    item = value or {"specs": [], "recorded": [], "formal": []}
    paths = {
        tier: sorted(item.get(tier, []))
        for tier in ("specs", "recorded", "formal")
    }
    return {
        "has_experiment_spec": bool(paths["specs"]),
        "has_recorded": bool(paths["recorded"]),
        "has_formal": bool(paths["formal"]),
        "any_bound": any(paths.values()),
        "paths": paths,
    }


def _tail_pre_experiment_closure_count(
    decision_events: list[dict[str, object]], *, prior_collision_only: bool = False
) -> int:
    count = 0
    for event in reversed(decision_events):
        if event["pre_experiment_closure"] is not True:
            break
        if prior_collision_only and event["to_status"] != "prior_collision":
            break
        count += 1
    return count


def _decision_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _run_wide_experiment_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    scratch_versions = []
    scratch_reports = []
    for root in sorted(workspace.workspace_path.glob("workbench_v*")):
        if not root.is_dir():
            continue
        scratch_versions.append(root.name.removeprefix("workbench_"))
        for path in sorted(root.rglob("*.md")):
            relative_parts = {
                part.casefold() for part in path.relative_to(root).parts[:-1]
            }
            name = path.name.casefold()
            if "diagnosis" not in relative_parts and (
                name == "scratch_report.md"
                or name == "result_summary.md"
                or name.endswith("_probe_report.md")
            ):
                scratch_reports.append(
                    path.relative_to(workspace.workspace_path).as_posix()
                )
    tier_items: dict[str, list[dict[str, object]]] = {"recorded": [], "formal": []}
    for experiment_root in sorted(workspace.workspace_path.glob("experiment_v*")):
        version = experiment_root.name.removeprefix("experiment_")
        version_workspace = ResearchWorkspace(
            workspace.workspace_path,
            knowledge_store=workspace.knowledge_store,
            version=version,
            product_root=workspace.product_root,
        )
        for tier, directory_name, record_name in (
            ("recorded", "recorded", "record.json"),
            ("formal", "attempts", "execution.json"),
        ):
            root = experiment_root / directory_name
            if not root.is_dir():
                continue
            for directory in sorted(item for item in root.iterdir() if item.is_dir()):
                record_path = directory / record_name
                status = None
                valid_review_support = None
                validation_errors: list[str] = []
                if record_path.is_file():
                    try:
                        record = json.loads(record_path.read_text(encoding="utf-8"))
                        if isinstance(record, dict):
                            status = record.get("status")
                    except (OSError, UnicodeError, json.JSONDecodeError):
                        pass
                if tier == "formal":
                    validation_errors = list(
                        experiment_material_errors(
                            version_workspace, (directory.name,)
                        )
                    )
                    valid_review_support = not validation_errors
                tier_items[tier].append(
                    {
                        "version": version,
                        "id": directory.name,
                        "status": status,
                        "path": directory.relative_to(workspace.workspace_path).as_posix(),
                        "valid_review_support": valid_review_support,
                        "validation_errors": validation_errors,
                    }
                )
    return {
        "scratch": {
            "version_count": len(scratch_versions),
            "versions": scratch_versions,
            "report_count": len(scratch_reports),
            "reports": scratch_reports,
        },
        "recorded": {
            "attempt_count": len(tier_items["recorded"]),
            "attempts": tier_items["recorded"],
        },
        "formal_review_support": {
            "attempt_count": len(tier_items["formal"]),
            "valid_attempt_count": sum(
                1
                for item in tier_items["formal"]
                if item["valid_review_support"] is True
            ),
            "attempts": tier_items["formal"],
        },
    }


def _latest_structured_activity_facts(
    workspace: ResearchWorkspace,
    hypotheses: dict[str, object],
    experiments: dict[str, object],
) -> dict[str, object]:
    candidate_versions = [
        str(item["version"])
        for item in hypotheses.get("raw_candidate_observations", [])
    ]
    recorded_versions = [
        str(item["version"])
        for item in experiments["recorded"]["attempts"]
    ]
    formal_versions = [
        str(item["version"])
        for item in experiments["formal_review_support"]["attempts"]
    ]
    prior_versions = []
    for path in workspace.workspace_path.glob("hypotheses_v*/priors/*/request.json"):
        version_name = path.parents[2].name
        if version_name.startswith("hypotheses_"):
            prior_versions.append(version_name.removeprefix("hypotheses_"))
    return {
        "structured_candidate": _version_distance_fact(
            workspace.version, candidate_versions
        ),
        "recorded": _version_distance_fact(workspace.version, recorded_versions),
        "formal": _version_distance_fact(workspace.version, formal_versions),
        "prior_audit": _version_distance_fact(workspace.version, prior_versions),
        "quality_semantics": (
            "raw_scientific_version_distances_only_not_research_quality_indicators"
        ),
    }


def _version_distance_fact(
    current_version: str, observed_versions: Iterable[str]
) -> dict[str, object]:
    valid = sorted(
        {
            item
            for item in observed_versions
            if re.fullmatch(r"v\d{3,}", item) is not None
        },
        key=lambda item: int(item[1:]),
    )
    if not valid:
        return {"latest_version": "UNAVAILABLE", "versions_since": "UNAVAILABLE"}
    latest = valid[-1]
    return {
        "latest_version": latest,
        "versions_since": int(current_version[1:]) - int(latest[1:]),
    }


def _search_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    searches = []
    query_fingerprints: Counter[str] = Counter()
    raw_bytes = 0
    report_bytes = 0
    source_distribution: Counter[str] = Counter()
    network_response_count = 0
    for root in sorted(workspace.workspace_path.glob("hypotheses_v*/searches/*")):
        if not root.is_dir():
            continue
        report = root / "report.md"
        request = root / "request.json"
        result = root / "result.json"
        paper_coverage = None
        query_count = None
        if report.is_file():
            data = report.read_bytes()
            report_bytes += len(data)
            match = re.search(r"去重 Paper[：:]\s*(\d+)", data.decode("utf-8", errors="ignore"))
            if match:
                paper_coverage = int(match.group(1))
        if request.is_file():
            try:
                payload = json.loads(request.read_text(encoding="utf-8"))
                texts = _query_texts(payload)
                query_count = len(texts)
                for text in texts:
                    query_fingerprints[hashlib.sha256(text.encode("utf-8")).hexdigest()] += 1
            except (OSError, UnicodeError, json.JSONDecodeError):
                pass
        if result.is_file():
            raw_bytes += result.stat().st_size
        searches.append(
            {
                "path": root.relative_to(workspace.workspace_path).as_posix(),
                "query_count": query_count,
                "deduplicated_paper_count": paper_coverage,
                "raw_result_bytes": result.stat().st_size if result.is_file() else 0,
                "compact_report_bytes": report.stat().st_size if report.is_file() else 0,
            }
        )
        source_distribution["research_retrieval_snapshot"] += 1
    prior_audit_count = 0
    for request in sorted(
        workspace.workspace_path.glob("hypotheses_v*/priors/*/request.json")
    ):
        try:
            payload = json.loads(request.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        prior_audit_count += 1
        sources = payload.get("sources")
        if isinstance(sources, list):
            for source in sources:
                if isinstance(source, str) and source.strip():
                    source_distribution[f"prior_audit:{source.strip()}"] += 1
        responses = payload.get("network_responses")
        if isinstance(responses, list):
            network_response_count += len(responses)
    return {
        "search_count": len(searches),
        "raw_result_bytes": raw_bytes,
        "compact_report_bytes": report_bytes,
        "repeated_query_fingerprint_count": sum(
            count - 1 for count in query_fingerprints.values() if count > 1
        ),
        "prior_audit_count": prior_audit_count,
        "network_response_count": network_response_count,
        "structured_source_distribution": dict(sorted(source_distribution.items())),
        "provenance_scope": (
            "structured_research_retrieval_and_prior_audit_artifacts_only"
        ),
        "searches": searches,
    }


def _query_texts(value: object) -> list[str]:
    output = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"query", "text", "raw_query", "original_query"} and isinstance(item, str) and item.strip():
                output.append(item.strip())
            else:
                output.extend(_query_texts(item))
    elif isinstance(value, list):
        for item in value:
            output.extend(_query_texts(item))
    return output


def _prior_collision_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    kinds: Counter[str] = Counter()
    audit_count = 0
    unclassified_count = 0
    warning_items = []
    for path in sorted(workspace.workspace_path.glob("hypotheses_v*/priors/*/request.json")):
        audit_count += 1
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            _, interpreted_kind, warnings, marker_present = _load_assessment(
                workspace,
                path.parent,
                path.parent.name,
                required=value.get("schema_version") == 3,
            )
            kind = interpreted_kind if marker_present else value.get("collision_kind")
            if warnings:
                warning_items.append(
                    {
                        "audit_id": path.parent.name,
                        "path": path.parent.relative_to(
                            workspace.workspace_path
                        ).as_posix()
                        + "/assessment.md",
                        "warnings": list(warnings),
                    }
                )
            if isinstance(kind, str) and kind:
                kinds[kind] += 1
            elif not warnings:
                unclassified_count += 1
    return {
        "prior_audit_count": audit_count,
        "collision_kind_distribution": dict(sorted(kinds.items())),
        "unclassified_audit_count": unclassified_count,
        "assessment_warning_audit_count": len(warning_items),
        "assessment_warning_count": sum(
            len(item["warnings"]) for item in warning_items
        ),
        "assessment_warnings": warning_items,
    }


def _subagent_facts(workspace: ResearchWorkspace) -> dict[str, object]:
    root = workspace.workspace_path / "research_workspace" / "subagents"
    artifacts = []
    categories: Counter[str] = Counter()
    if root.is_dir():
        for path in sorted(root.glob("*.md")):
            stem = path.stem.casefold()
            if any(token in stem for token in ("prior", "collision", "scout")):
                category = "prior_or_falsification"
            elif any(token in stem for token in ("impl", "benchmark", "experiment")):
                category = "implementation_or_experiment"
            else:
                category = "unclassified"
            categories[category] += 1
            artifacts.append(
                {
                    "topic": path.stem,
                    "category_from_filename": category,
                    "path": path.relative_to(workspace.workspace_path).as_posix(),
                    "fact_basis": "path_and_filename_only",
                }
            )
    return {
        "summary_artifact_count": len(artifacts),
        "summary_artifacts": artifacts,
        "category_distribution": dict(sorted(categories.items())),
        "classification_basis": (
            "filename_only_artifact_classification_no_native_delegation_verification"
        ),
        "native_delegation_evidence": {
            "status": "UNAVAILABLE",
            "verified_delegation_count": None,
            "reason": "no_stable_machine_verifiable_native_delegation_evidence_source",
            "summary_artifacts_verify_native_delegation": False,
        },
        # Compatibility aliases for existing facts consumers. These still count
        # Markdown artifacts, not native delegation events.
        "summary_count": len(artifacts),
        "tasks": artifacts,
    }


def _recall_composition(workspace: ResearchWorkspace) -> dict[str, object]:
    manifest_path = workspace.workspace_path / ".crl" / "recall" / "manifest.json"
    if not manifest_path.is_file():
        return {"status": "UNAVAILABLE", "reason": "manifest_missing"}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return {"status": "UNAVAILABLE", "reason": f"manifest_invalid:{type(error).__name__}"}
    indexed = manifest.get("indexed_files", [])
    excluded = manifest.get("excluded_files", [])
    prefixes: Counter[str] = Counter()
    stale = 0
    indexed_bytes = 0
    nested_repository_count = 0
    nested_repository_bytes = 0
    diagnosis_indexed_count = 0
    diagnosis_indexed_bytes = 0
    repository_roots = _nested_repository_roots(workspace)
    if isinstance(indexed, list):
        for item in indexed:
            if not isinstance(item, dict):
                continue
            path = str(item.get("path", ""))
            indexed_bytes += int(item.get("size_bytes", 0) or 0)
            size_bytes = int(item.get("size_bytes", 0) or 0)
            if path.startswith(("external/", "vendor/", "third_party/")):
                prefixes["external_or_vendor"] += 1
            if any(
                path == root or path.startswith(root.rstrip("/") + "/")
                for root in repository_roots
            ):
                nested_repository_count += 1
                nested_repository_bytes += size_bytes
            if re.match(r"workbench_v\d{3,}/diagnosis/", path):
                diagnosis_indexed_count += 1
                diagnosis_indexed_bytes += size_bytes
            if any(part in {"ground_truth", "hidden_test", "hidden_tests"} for part in Path(path).parts):
                prefixes["ground_truth_like"] += 1
            if re.fullmatch(r"hypotheses_v\d{3,}/searches/[^/]+/result\.json", path):
                prefixes["raw_search_payload"] += 1
            source = workspace.workspace_path / Path(path)
            try:
                if not source.is_file() or _sha256(source.read_bytes()) != item.get("sha256"):
                    stale += 1
            except OSError:
                stale += 1
    return {
        "status": "READY",
        "manifest_schema_version": manifest.get("schema_version"),
        "indexed_file_count": len(indexed) if isinstance(indexed, list) else 0,
        "indexed_bytes": indexed_bytes,
        "excluded_entry_count": len(excluded) if isinstance(excluded, list) else 0,
        "external_or_vendor_indexed_count": prefixes["external_or_vendor"],
        "nested_repository_indexed_count": nested_repository_count,
        "nested_repository_indexed_bytes": nested_repository_bytes,
        "diagnosis_indexed_count": diagnosis_indexed_count,
        "diagnosis_indexed_bytes": diagnosis_indexed_bytes,
        "ground_truth_like_indexed_count": prefixes["ground_truth_like"],
        "raw_search_payload_indexed_count": prefixes["raw_search_payload"],
        "stale_indexed_source_count": stale,
        "contamination_present": (
            any(prefixes.values())
            or nested_repository_count > 0
            or diagnosis_indexed_count > 0
        ),
        "source_ownership": {
            "research_owned_bytes": max(
                indexed_bytes - nested_repository_bytes - diagnosis_indexed_bytes,
                0,
            ),
            "nested_repository_bytes": nested_repository_bytes,
            "derived_diagnosis_bytes": diagnosis_indexed_bytes,
        },
    }


def _nested_repository_roots(workspace: ResearchWorkspace) -> tuple[str, ...]:
    roots = set()
    for marker in workspace.workspace_path.rglob(".git"):
        try:
            relative = marker.parent.relative_to(workspace.workspace_path).as_posix()
        except ValueError:
            continue
        if relative and (marker.is_file() or marker.is_dir() or marker.is_symlink()):
            roots.add(relative)
    return tuple(sorted(roots))


def _ordinary_files(workspace: ResearchWorkspace) -> Iterable[Path]:
    for path in workspace.workspace_path.rglob("*"):
        relative = path.relative_to(workspace.workspace_path)
        if (
            not path.is_file()
            or any(part.casefold() in _EXCLUDED_DIRS for part in relative.parts[:-1])
            or path.suffix.casefold() in _EXCLUDED_SUFFIXES
        ):
            continue
        yield workspace.assert_read_target(path)


def _recall_unavailable_reason(error: BaseException) -> str:
    if isinstance(error, FileNotFoundError):
        return "fts_index_missing_or_unreadable"
    return f"fts_recall_failed:{type(error).__name__}:{error}"


def _file_group(root: Path, workspace: ResearchWorkspace) -> list[dict[str, object]]:
    if not root.is_dir():
        return []
    output = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        safe = workspace.assert_read_target(path)
        data = safe.read_bytes()
        output.append(
            {
                "path": safe.relative_to(workspace.workspace_path).as_posix(),
                "size_bytes": len(data),
                "sha256": _sha256(data),
            }
        )
    return output


def _render_report(facts: dict[str, object], facts_sha256: str) -> bytes:
    experiments = facts["experiments"]
    run_wide = facts["run_wide"]
    versions = run_wide["scientific_versions"]
    run_experiments = run_wide["experiments"]
    searches = run_wide["searches"]
    hypotheses = run_wide["hypotheses"]
    latest_activity = run_wide["latest_structured_activity"]
    selection_context = facts["current_version"]["selection_context"]
    preference = selection_context["candidate_preference"]
    collisions = run_wide["prior_collisions"]
    subagents = run_wide["subagents"]
    native_delegation = subagents["native_delegation_evidence"]
    verified_delegation_count = native_delegation["verified_delegation_count"]
    recall_composition = run_wide["recall_composition"]
    recall_status = facts["recall_status"]
    recall_reason = recall_status["reason"] or "无"
    lines = [
        "# CRL Active Diagnosis Facts",
        "",
        "STATUS: ADVISORY_NON_AUTHORITATIVE",
        f"FACTS_SHA256: {facts_sha256}",
        "",
        "> 这是机械事实视图，不是科研裁决。主研究者负责解释矛盾、盲点和高信息量下一步。",
        "",
        f"- Run: `{facts['run_id']}`",
        f"- Version: `{facts['version']}`",
        f"- Indexed ordinary files: {facts['file_count']}",
        f"- Current-version Recorded/Formal attempts: {experiments['attempt_count']}",
        f"- Comparison files: {len(facts['comparison_files'])}",
        f"- Search snapshot files: {len(facts['search_snapshot_files'])}",
        f"- Review evaluation files: {len(facts['review_evaluation_files'])}",
        f"- Recall FTS: {recall_status['status']}（{recall_reason}）",
        f"- Recall semantic: {recall_status['semantic_status'] or 'UNAVAILABLE'}"
        f"（{recall_status['semantic_reason'] or '无'}）",
        f"- Selection context template: {selection_context['status']}",
        f"- Candidate preference declarations: {preference['status']}",
        "",
        "## Run-wide mechanical facts",
        "",
        f"- Scientific versions: {versions['version_count']}",
        f"- Empty current version: {versions['empty_current_version']}",
        f"- Scratch report files: {run_experiments['scratch']['report_count']}",
        f"- Recorded attempts: {run_experiments['recorded']['attempt_count']}",
        f"- Formal / Review-support attempts: {run_experiments['formal_review_support']['attempt_count']}",
        f"- Valid Formal / Review-support attempts: {run_experiments['formal_review_support']['valid_attempt_count']}",
        f"- Search snapshots: {searches['search_count']}",
        f"- Raw search bytes: {searches['raw_result_bytes']}",
        f"- Compact search report bytes: {searches['compact_report_bytes']}",
        f"- Prior audits: {collisions['prior_audit_count']}",
        f"- Classified collision kinds: {sum(collisions['collision_kind_distribution'].values())}",
        f"- Normally unclassified prior audits: {collisions['unclassified_audit_count']}",
        f"- Prior assessment warning audits: {collisions['assessment_warning_audit_count']}",
        "- Tail consecutive pre-experiment closures: "
        f"{hypotheses['pre_experiment_closure_streak']}",
        "- Tail consecutive prior-collision pre-experiment closures: "
        f"{hypotheses['prior_collision_pre_experiment_closure_streak']}",
        "- Experiment binding recovery: "
        f"{hypotheses['experiment_binding_recovery']['status']}",
        f"- Run-local subagent-related Markdown summary artifacts: {subagents['summary_artifact_count']}",
        f"- Native delegation evidence: {native_delegation['status']}",
        "- Verified native delegation count: "
        f"{verified_delegation_count if verified_delegation_count is not None else 'UNKNOWN'}",
        f"- Recall contamination present: {recall_composition.get('contamination_present', 'UNKNOWN')}",
        f"- Nested repository indexed bytes: {recall_composition.get('nested_repository_indexed_bytes', 'UNKNOWN')}",
        f"- Diagnosis indexed bytes: {recall_composition.get('diagnosis_indexed_bytes', 'UNKNOWN')}",
        f"- Recall stale indexed sources: {recall_composition.get('stale_indexed_source_count', 'UNKNOWN')}",
        "",
        "## Selection context evidence facts",
        "",
    ]
    for item in selection_context["sections"].values():
        content = item["text"] if item["text"] is not None else "UNAVAILABLE"
        lines.append(f"- {item['heading']} [{item['status']}]: {content}")
    lines.extend(
        [
            "",
            "## Candidate preference facts",
            "",
            "- INCUMBENT_SET "
            f"[{preference['incumbent_set']['status']}]: "
            f"{', '.join(preference['incumbent_set']['candidate_ids']) or 'UNAVAILABLE'} "
            f"(occurrences={preference['incumbent_set']['occurrence_count']})",
            "- CHALLENGERS "
            f"[{preference['challengers']['status']}]: "
            f"{', '.join(preference['challengers']['candidate_ids']) or 'UNAVAILABLE'} "
            f"(occurrences={preference['challengers']['occurrence_count']})",
            f"- Pairwise comparisons: {preference['pairwise_comparison_count']}",
            "- Candidate admission contracts: "
            f"{preference['candidate_admission_contract_count']}",
            f"- Local reward contracts: {preference['local_reward_contract_count']}",
            "- Implementation declarations with self-declared sessions: "
            f"{preference['independent_implementation_record_count']}",
            f"- Preference updates: {preference['preference_update_count']}",
        ]
    )
    for item in preference["pairwise_comparisons"]:
        fields = item["fields"]
        lines.extend(
            [
                "- Pair "
                f"{item['pair_index']}: {item['pair'] or 'UNAVAILABLE'} -> "
                f"declared_verdict={item['verdict'] or item['verdict_status']}; "
                f"comparison_status={item['status']}; "
                "mechanically_supported_winner="
                f"{item['winner_candidate_id'] or 'NONE'}",
                "  - DECISIVE_EVIDENCE "
                f"[{fields['DECISIVE_EVIDENCE']['status']}]: "
                f"{fields['DECISIVE_EVIDENCE']['value'] or 'UNAVAILABLE'}",
                "  - SURVIVING_FATAL_UNCERTAINTIES: "
                f"{fields['SURVIVING_FATAL_UNCERTAINTIES']['value'] or fields['SURVIVING_FATAL_UNCERTAINTIES']['status']}",
                "  - REVERSAL_CONDITION: "
                f"{fields['REVERSAL_CONDITION']['value'] or fields['REVERSAL_CONDITION']['status']}",
                "  - NEXT_DISCRIMINATING_ACTION: "
                f"{fields['NEXT_DISCRIMINATING_ACTION']['value'] or fields['NEXT_DISCRIMINATING_ACTION']['status']}",
            ]
        )
    for item in preference["independent_implementation_summaries"]:
        lines.append(
            "- Implementation evidence "
            f"`{item['candidate_id']}`: declared={item['declared_record_count']}, "
            "DECLARED_SESSION ids="
            f"{item['declared_session_id_count']}, "
            "distinct VERIFIED_ARTIFACT bytes under one frozen Candidate Card hash="
            f"{item['verified_artifact_count']}"
        )
    if preference["independent_implementation_summaries"]:
        lines.append(
            "> DECLARED_SESSION 仅是 Markdown 自报标识；VERIFIED_ARTIFACT 仅表示 Run 边界内普通文件及 SHA-256 已机械核验。脚本不能认证真实会话隔离或科学独立性。"
        )
    if preference["advisories"]:
        lines.append("- Advisory codes:")
        for item in preference["advisories"]:
            candidate = item.get("candidate_id")
            suffix = f" candidate={candidate}" if candidate else ""
            lines.append(f"  - {item['code']}{suffix}")
    lines.append("")
    lines.extend(
        [
            "",
            "## Latest structured activity version facts",
            "",
        ]
    )
    for label, key in (
        ("Structured candidate", "structured_candidate"),
        ("Recorded", "recorded"),
        ("Formal", "formal"),
        ("Prior Audit", "prior_audit"),
    ):
        item = latest_activity[key]
        lines.append(
            f"- {label}: latest={item['latest_version']}, versions_since={item['versions_since']}"
        )
    lines.extend(
        [
            "",
            "> 上述版本距离只是原始活动事实，不是科研质量、成熟度或停滞指标。",
            "",
        ]
    )
    if hypotheses["pre_experiment_closure_significant_warning"]:
        lines.extend(
            [
                "## Significant pre-experiment closure warning",
                "",
                "> 已达到连续 5 个实验前关闭。主研究者必须解释重复模式、更新 selection context，并改用不同的高信息量策略；Diagnosis 不自动改变候选状态或结束 Run。",
                "",
            ]
        )
    if hypotheses["semantic_overreach_warnings"]:
        lines.extend(["## Semantic overreach warnings", ""])
        for item in hypotheses["semantic_overreach_warnings"]:
            codes = ", ".join(item["warning_codes"])
            lines.append(
                f"- `{item['version']}/{item['hypothesis_id']}` decision "
                f"{item['decision_index']}: {codes}"
            )
        lines.extend(
            [
                "",
                "> 以上仅为声明字段的机械组合警告，不否定主研究者解释，也不自动改变候选状态。",
                "",
            ]
        )
    if hypotheses["experiment_spec_warnings"]:
        lines.extend(["## Experiment specification warnings", ""])
        for item in hypotheses["experiment_spec_warnings"]:
            codes = ", ".join(item["warning_codes"])
            lines.append(f"- `{item['path']}`: {codes}")
        lines.extend(
            [
                "",
                "> 以上只说明 Representative 声明的 subject scope 为空，不判断实验是否充分。",
                "",
            ]
        )
    if preference["preference_stagnation"]["warning"]:
        stagnation = preference["preference_stagnation"]
        lines.extend(
            [
                "## PREFERENCE_STAGNATION_WARNING",
                "",
                "- Evaluated declared high-information actions: "
                f"{', '.join(str(item) for item in stagnation['evaluated_action_ids'])}",
                "> 按每个 ACTION_ID 的最后出现位置选出的最近三个不同高信息量动作，既未改变四值偏好结论，也未减少致命不确定性。主研究者必须更新 selection_context，明确 STOP_REPEATING，扩展贡献坐标并声明新的辨别动作；Run 保持 ACTIVE。Diagnosis 不改变状态、版本、候选或终局。",
                "",
            ]
        )
    if preference["single_implementation_idea_level_risks"]:
        lines.extend(["## Implementation-lottery advisories", ""])
        for item in preference["single_implementation_idea_level_risks"]:
            identity = item.get("candidate_id") or item.get("hypothesis_id") or "UNKNOWN"
            lines.append(f"- `{identity}`: {item['code']} ({item['source']})")
        lines.extend(
            [
                "",
                "> 单一工件或同字节工件的重复声明不能单独支撑想法级偏好或死亡；不同 SHA-256 也只证明工件字节不同，不证明真实会话隔离或科学独立性。以上只是事实风险提示，不自动撤销比较或改变 Hypothesis。",
                "",
            ]
        )
    if collisions["assessment_warnings"]:
        lines.extend(["## Prior assessment warnings", ""])
        for item in collisions["assessment_warnings"]:
            lines.append(f"- `{item['path']}`")
            lines.extend(f"  - {warning}" for warning in item["warnings"])
        lines.append("")
    lines.extend(
        [
            "## Main researcher interpretation prompts",
            "",
            "- 当前注意力是否只围绕同一实现或同一证据簇？",
            "- 重复失败是否共享可检验的机制或隐藏前提？",
            "- 哪些假设、基线公平性或评价依据仍未验证？",
            "- 当前负面证据真正杀死的是实现、候选、方法谱系、局部研究盆地，还是整个 Run 边界？",
            "- 所谓正交路线是只做了文献扫描，还是已形成结构不同的问题、失败模式或算子并做了最小高信息量检查？",
            "- 哪个下一步最能减少不确定性，正反结果分别会改变什么？",
            "- 连续方法碰撞时，是否应先验证一个跨模型、任务或种子稳定的现象，再生成新方法？",
            "- 当前碰撞是直接同构、经验吸收、可构造组合、类比约化，还是仅问题已被提出？其杀伤范围是否被夸大？",
            "- 不要从 summary artifact 数量推断原生委派已经发生；若另有平台可核验的真实子智能体任务，其认知任务是否只集中于先行攻击？",
            "- 版本变化是否改变了问题、现象、干预位置、可用信息、机制族、评价载体或贡献形态？",
            "- 候选成熟度是否真的提高，还是只有科研信息增益来自一次真实反证？两者必须分开解释。",
            "- 当前 INCUMBENT_SET 与 CHALLENGERS 是否完整保留了不可比候选，而没有把 INCOMPARABLE 偷换成平局、失败或淘汰？",
            "- INSUFFICIENT_EVIDENCE 是否绑定了能区分候选的下一动作、逆转条件和仍存致命不确定性？",
            "- 本地奖励是否只用于本候选的局部变异与实验设计，并与新颖性、终局和 Delivery 判断隔离？",
            "- 开发证据和准入证据是否只是路径不同，还是确有独立的评价角色？不要从不同路径自动推断科学独立性。",
            "- 想法级偏好或死亡若依赖经验实现，主研究者是否确认同一冻结 Candidate Card 下有两份实际隔离完成的实现及盲保真检查，或有明确且可核验的例外？DECLARED_SESSION 与不同 VERIFIED_ARTIFACT 都不能替代这一科学判断。",
            "- 若已出现连续 5 个实验前关闭，明确停止重复什么动作，并从回溯、正交扩展、现象优先、贡献形态变化或长期推迟的高信息量实验中选择不同动作。",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def _json_bytes(value: dict[str, object]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _diagnosis_id(value: str) -> str:
    if not isinstance(value, str) or _DIAGNOSIS_ID.fullmatch(value) is None:
        raise ValueError("diagnosis id must be 3-64 lowercase safe characters")
    return value


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
