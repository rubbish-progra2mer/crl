from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

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
    current_version = {
        "version": workspace.version,
        "experiments": experiments,
        "comparison_files": comparisons,
        "search_snapshot_files": searches,
        "review_evaluation_files": evaluations,
        "selection_context": _selection_context_facts(workspace),
    }
    run_wide = _run_wide_facts(workspace)
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
    }


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
