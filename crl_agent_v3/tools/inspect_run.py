from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crl_v3.decision import (
    delivery_record_paths,
    no_delivery_record_paths,
    read_delivery_history,
    read_no_delivery_history,
    read_terminal,
    secret_scan_errors,
    secret_scan_warnings,
)
from crl_v3.experiment import valid_supporting_attempt_ids
from crl_v3.recall import inspection_run_files
from crl_v3.reviewer_decision import read_fixed_review_decision
from crl_v3.reviewer_protocol import EVALUATOR_VERSION
from crl_v3.workspace import (
    CURRENT_CONTRACT_VERSION,
    PERMANENT_TERMINAL_FILE_STATUS,
    ResearchWorkspace,
    _assert_read_target,
    _is_reparse_point,
    _required_file,
    bind_run,
    contract_version,
)


_VERSION_PATTERN = re.compile(r"^v\d{3,}$")
_VERSION_IN_NAME = re.compile(r"(?:^|_)(v\d{3,})(?:\.md|$)")
_PERMANENT_TERMINAL_STATUSES = set(PERMANENT_TERMINAL_FILE_STATUS.values())
_CLOSED_STATUSES = _PERMANENT_TERMINAL_STATUSES | {
    "DELIVERED",
    "CONCLUDED_NO_DELIVERY",
}


def inspect_run(
    run_root: str | Path,
    version: str | None = None,
    *,
    product_root: str | Path | None = None,
) -> dict[str, Any]:
    if product_root is None:
        raise ValueError("product_root is required; it must not be inferred from run_root")
    product = Path(product_root).resolve(strict=True)
    root = bind_run(product, run_root)
    fields = _read_fields(root / "RUN_STATUS.md", root)
    status_current_version = fields.get("CURRENT_VERSION", "v001")
    current_version = version or status_current_version
    if not _VERSION_PATTERN.fullmatch(status_current_version):
        raise ValueError(f"invalid RUN_STATUS.md CURRENT_VERSION: {status_current_version!r}")
    if not _VERSION_PATTERN.fullmatch(current_version):
        raise ValueError(f"invalid CURRENT_VERSION: {current_version!r}")
    declared_status = fields.get("STATUS", "UNKNOWN")
    run_contract = contract_version(root)
    delivery_paths = list(delivery_record_paths(root))
    no_delivery_paths = list(no_delivery_record_paths(root))
    permanent_terminal_paths = [
        root / name
        for name in PERMANENT_TERMINAL_FILE_STATUS
        if (root / name).is_file()
    ]
    effective_status = declared_status
    if len(permanent_terminal_paths) == 1:
        effective_status = PERMANENT_TERMINAL_FILE_STATUS[
            permanent_terminal_paths[0].name
        ]

    report: dict[str, Any] = {
        "run_root": str(root),
        "run_id": fields.get("RUN_ID", root.name),
        "contract_version": run_contract,
        "current_contract": run_contract == CURRENT_CONTRACT_VERSION,
        "legacy_read_only": run_contract != CURRENT_CONTRACT_VERSION,
        "declared_status": declared_status,
        "effective_status": effective_status,
        "status": effective_status,
        "mode": fields.get("MODE"),
        "current_version": current_version,
        "status_current_version": status_current_version,
        "available_versions": sorted(_run_versions(root)),
        "terminal": effective_status in _CLOSED_STATUSES,
        "delivery_count": len(delivery_paths),
        "delivery_history": [],
        "latest_delivery": None,
        "no_delivery_count": len(no_delivery_paths),
        "no_delivery_history": [],
        "latest_no_delivery": None,
        "documents": {},
        "directories": {},
        "experiment": {},
        "review": {},
        "errors": [],
        "warnings": [],
    }
    try:
        research_owned_files, security_scan_files, excluded_paths = (
            inspection_run_files(root)
        )
    except (OSError, ValueError) as error:
        research_owned_files = ()
        security_scan_files = ()
        excluded_paths = ()
        report["errors"].append(f"RUN_RESEARCH_PATH_SCAN_UNSAFE: {error}")
    if run_contract != CURRENT_CONTRACT_VERSION:
        report["warnings"].append(
            "legacy Run is maintenance-readable only and cannot enter current CRL operations"
        )
        legacy_documents = (
            "RUN_CHARTER.md",
            "RUN_STATUS.md",
            "RUN_LEDGER.md",
            "DELIVERY.md",
            "NO_DELIVERY.md",
            *PERMANENT_TERMINAL_FILE_STATUS,
        )
        for name in legacy_documents:
            report["documents"][name] = _file_fact(root / name, root)
        for path in delivery_paths[1:]:
            report["documents"][path.name] = _file_fact(path, root)
        for path in no_delivery_paths[1:]:
            report["documents"][path.name] = _file_fact(path, root)
        _append_markdown_integrity(root, report, research_owned_files)
        if len(permanent_terminal_paths) > 1:
            report["errors"].append("multiple permanent terminal documents exist")
        elif permanent_terminal_paths and declared_status != effective_status:
            report["errors"].append(
                "RUN_STATUS.md disagrees with the authoritative terminal document"
            )
        report["errors"] = list(dict.fromkeys(report["errors"]))
        report["warnings"] = list(dict.fromkeys(report["warnings"]))
        return report

    workspace = ResearchWorkspace(root, version=current_version, product_root=product)
    future_versions = [
        item
        for item in report["available_versions"]
        if int(item[1:]) > int(status_current_version[1:])
    ]
    if future_versions:
        report["errors"].append(
            "Run has version artifacts newer than RUN_STATUS.md CURRENT_VERSION: "
            + ", ".join(future_versions)
        )
    report["errors"].extend(
        secret_scan_errors(
            root, for_no_delivery=True, paths=security_scan_files
        )
    )
    report["errors"].extend(
        "sensitive credential path in Run directory: " + str(item["path"])
        for item in excluded_paths
        if item.get("reason") == "credential_store_tree"
    )
    report["warnings"].extend(
        secret_scan_warnings(root, paths=security_scan_files)
    )
    for stem in (
        "problem",
        "research_map",
        "nearest_prior",
        "candidate",
        "evidence_packet",
        "selection_context",
        "decision",
        "memory",
        "failure_attribution",
        "seed",
    ):
        path = workspace.document_path(stem)
        report["documents"][path.name] = _file_fact(path, root)
    for path in (
        workspace.implementation_path,
        workspace.experiment_path,
        workspace.review_path,
        workspace.workbench_path,
        root / f"audit_{current_version}",
    ):
        report["directories"][path.name] = _directory_fact(
            path, root, research_owned_files
        )
    report["documents"]["DELIVERY.md"] = _file_fact(root / "DELIVERY.md", root)
    for path in delivery_paths[1:]:
        report["documents"][path.name] = _file_fact(path, root)
    report["documents"]["NO_DELIVERY.md"] = _file_fact(
        root / "NO_DELIVERY.md", root
    )
    for path in no_delivery_paths[1:]:
        report["documents"][path.name] = _file_fact(path, root)
    for name in PERMANENT_TERMINAL_FILE_STATUS:
        report["documents"][name] = _file_fact(root / name, root)
    _append_markdown_integrity(root, report, research_owned_files)
    report["current_version_activity"] = _current_version_activity(
        root, current_version, research_owned_files, fields
    )
    if declared_status == "ACTIVE" and current_version == status_current_version:
        activity = report["current_version_activity"]
        if activity["status"] in {
            "ACTIVE_CURRENT_VERSION_EMPTY",
            "ACTIVE_CURRENT_VERSION_INVALID_CONTINUATION",
        }:
            report["errors"].append("ACTIVE_CURRENT_VERSION_EMPTY")
        elif activity["new_research_action_present"] is False:
            report["warnings"].append(
                "ACTIVE_CURRENT_VERSION_NO_NEW_RESEARCH_ACTION: "
                + str(activity["status"])
            )

    experiment_exists, experiment_error = _workspace_directory_state(
        workspace, workspace.experiment_path
    )
    if experiment_error is not None:
        report["errors"].append(experiment_error)
    attempts_root = workspace.experiment_path / "attempts"
    attempt_count = 0
    attempts_exist, attempts_error = _workspace_directory_state(
        workspace, attempts_root
    )
    if attempts_error is not None:
        report["errors"].append(attempts_error)
    unsafe_attempt_directory = False
    if attempts_exist:
        for item in attempts_root.iterdir():
            if _is_reparse_point(item):
                unsafe_attempt_directory = True
                report["errors"].append(
                    f"unsafe experiment attempt directory: {item.relative_to(root).as_posix()}"
                )
            elif item.is_dir():
                attempt_count += 1
    report["experiment"] = {
        "exists": experiment_exists,
        "attempt_count": attempt_count,
        "valid_attempt_ids": (
            list(valid_supporting_attempt_ids(workspace))
            if experiment_exists
            and attempts_error is None
            and not unsafe_attempt_directory
            else []
        ),
    }

    report["review"] = _fixed_review_facts(workspace)

    delivery_history = ()
    try:
        delivery_history = read_delivery_history(workspace)
        report["delivery_history"] = [
            {
                "path": Path(item.path).relative_to(root).as_posix(),
                "version": item.version,
                "sha256": item.sha256,
            }
            for item in delivery_history
        ]
        report["delivery_count"] = len(delivery_history)
        report["latest_delivery"] = (
            report["delivery_history"][-1] if report["delivery_history"] else None
        )
    except (OSError, UnicodeError, ValueError) as error:
        if delivery_paths:
            report["errors"].append(f"invalid Delivery history: {error}")

    no_delivery_history = ()
    try:
        no_delivery_history = read_no_delivery_history(workspace)
        report["no_delivery_history"] = [
            {
                "path": Path(item.path).relative_to(root).as_posix(),
                "version": item.version,
                "sha256": item.sha256,
            }
            for item in no_delivery_history
        ]
        report["no_delivery_count"] = len(no_delivery_history)
        report["latest_no_delivery"] = (
            report["no_delivery_history"][-1]
            if report["no_delivery_history"]
            else None
        )
    except (OSError, UnicodeError, ValueError) as error:
        if no_delivery_paths:
            report["errors"].append(f"invalid No-Delivery history: {error}")

    conclusions = sorted(
        (*delivery_history, *no_delivery_history),
        key=lambda item: int(item.version[1:]),
    )
    conclusion_versions = [item.version for item in conclusions]
    if len(conclusion_versions) != len(set(conclusion_versions)):
        report["errors"].append(
            "multiple scientific conclusions exist for one version"
        )
    latest_conclusion = conclusions[-1] if conclusions else None

    if len(permanent_terminal_paths) > 1:
        report["errors"].append("multiple permanent terminal documents exist")
    elif permanent_terminal_paths:
        terminal = permanent_terminal_paths[0]
        try:
            read_terminal(
                terminal,
                PERMANENT_TERMINAL_FILE_STATUS[terminal.name],
                status_current_version,
            )
        except (OSError, UnicodeError, ValueError) as error:
            report["errors"].append(str(error))
    elif declared_status in _PERMANENT_TERMINAL_STATUSES:
        report["errors"].append(
            "RUN_STATUS.md declares a terminal status but no terminal document exists"
        )

    if permanent_terminal_paths and declared_status != effective_status:
        report["errors"].append(
            "RUN_STATUS.md disagrees with the authoritative terminal document"
        )
    if declared_status == "DELIVERED":
        if permanent_terminal_paths:
            report["errors"].append(
                "DELIVERED status conflicts with a permanent terminal document"
            )
        if latest_conclusion is None or latest_conclusion.status != "DELIVERED":
            report["errors"].append(
                "RUN_STATUS.md declares DELIVERED but the latest conclusion is not Delivery"
            )
        elif latest_conclusion.version != status_current_version:
            report["errors"].append(
                "latest Delivery version disagrees with RUN_STATUS.md CURRENT_VERSION"
            )
    elif declared_status == "CONCLUDED_NO_DELIVERY":
        if permanent_terminal_paths:
            report["errors"].append(
                "CONCLUDED_NO_DELIVERY conflicts with a permanent terminal document"
            )
        if (
            latest_conclusion is None
            or latest_conclusion.status != "CONCLUDED_NO_DELIVERY"
        ):
            report["errors"].append(
                "RUN_STATUS.md declares CONCLUDED_NO_DELIVERY but the latest "
                "conclusion is not No-Delivery"
            )
        elif latest_conclusion.version != status_current_version:
            report["errors"].append(
                "latest No-Delivery version disagrees with RUN_STATUS.md CURRENT_VERSION"
            )
    elif latest_conclusion and declared_status in {"ACTIVE", "PAUSED_BY_USER"}:
        if int(status_current_version[1:]) <= int(latest_conclusion.version[1:]):
            report["errors"].append(
                "an active or paused Run must be newer than its latest scientific conclusion"
            )
    if (
        declared_status == "TERMINATED_BY_USER"
        and latest_conclusion is not None
        and int(status_current_version[1:]) <= int(latest_conclusion.version[1:])
    ):
        report["errors"].append(
            "user termination version must be newer than prior scientific conclusions"
        )

    report["errors"] = list(dict.fromkeys(report["errors"]))
    report["warnings"] = list(dict.fromkeys(report["warnings"]))
    return report


def _fixed_review_facts(workspace: ResearchWorkspace) -> dict[str, Any]:
    evaluations_root = workspace.review_path / "evaluations"
    evaluations: list[dict[str, Any]] = []
    errors: list[str] = []
    review_exists, review_error = _workspace_directory_state(
        workspace, workspace.review_path
    )
    if review_error is not None:
        errors.append(review_error)
    evaluations_exist = False
    if review_exists and review_error is None:
        evaluations_exist, evaluations_error = _workspace_directory_state(
            workspace, evaluations_root
        )
        if evaluations_error is not None:
            errors.append(evaluations_error)
    if evaluations_exist:
        for directory in sorted(evaluations_root.iterdir()):
            if _is_reparse_point(directory):
                errors.append(
                    "unsafe fixed evaluation directory: "
                    + directory.relative_to(workspace.workspace_path).as_posix()
                )
                continue
            if not directory.is_dir():
                continue
            try:
                request = json.loads(
                    _required_file(
                        directory / "request.json", within=workspace.workspace_path
                    ).decode("utf-8")
                )
                if not isinstance(request, dict):
                    raise ValueError("request.json is not an object")
                aggregate = None
                aggregate_path = directory / "aggregate.json"
                if aggregate_path.is_file():
                    aggregate = json.loads(
                        _required_file(
                            aggregate_path, within=workspace.workspace_path
                        ).decode("utf-8")
                    )
                    if not isinstance(aggregate, dict):
                        raise ValueError("aggregate.json is not an object")
                evaluations.append(
                    {
                        "evaluation_id": directory.name,
                        "implementation_key": request.get("implementation_key"),
                        "packet_key": request.get("packet_key"),
                        "measurement_key": request.get("measurement_key"),
                        "final_delivery_review": request.get("final_delivery_review") is True,
                        "complete": aggregate is not None,
                        "valid": aggregate.get("valid") if aggregate else None,
                        "measurement_kind": aggregate.get("measurement_kind") if aggregate else None,
                        "canonical_evaluation_id": aggregate.get("canonical_evaluation_id") if aggregate else None,
                        "overall_score_percent": aggregate.get("overall_score_percent") if aggregate else None,
                    }
                )
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
                errors.append(f"invalid fixed evaluation {directory.name}: {error}")

    decision = None
    if workspace.document_path("decision").is_file():
        try:
            bound = read_fixed_review_decision(workspace)
            decision = {
                "implementation_key": bound.implementation_key,
                "packet_key": bound.packet_key,
                "measurement_key": bound.measurement_key,
                "canonical_evaluation_id": bound.canonical_evaluation_id,
                "aggregate_sha256": bound.aggregate_sha256,
                "sha256": bound.sha256,
            }
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"invalid fixed Review decision: {error}")

    return {
        "protocol": "FIXED_REVIEWER_V3",
        "evaluator_version": EVALUATOR_VERSION,
        "evaluation_count": len(evaluations),
        "valid_evaluation_count": sum(item["valid"] is True for item in evaluations),
        "canonical_measurement_count": sum(
            item["measurement_kind"] == "CANONICAL_IMPLEMENTATION_SCORE"
            for item in evaluations
        ),
        "stability_measurement_count": sum(
            item["measurement_kind"] == "STABILITY_MEASUREMENT"
            for item in evaluations
        ),
        "evaluations": evaluations,
        "decision_exists": decision is not None,
        "decision": decision,
        "material_errors": errors,
    }


def _append_markdown_integrity(
    root: Path, report: dict[str, Any], research_owned_files: Sequence[Path]
) -> None:
    for path in sorted(
        item for item in research_owned_files if item.suffix.casefold() == ".md"
    ):
        fact = _file_fact(path, root)
        relative = path.relative_to(root).as_posix()
        if fact.get("unsafe"):
            report["errors"].append(
                f"Markdown is not a safe regular Run-local file: {relative}"
            )
            continue
        if not fact.get("utf8", False):
            report["errors"].append(f"Markdown is not valid UTF-8: {relative}")
        if fact.get("bom"):
            report["errors"].append(f"Markdown has a UTF-8 BOM: {relative}")
        if fact.get("lf_only") is False:
            report["errors"].append(f"Markdown does not use LF-only newlines: {relative}")


def _read_fields(path: Path, run_root: Path) -> dict[str, str]:
    fact = _file_fact(path, run_root)
    if not fact["exists"]:
        raise FileNotFoundError(path)
    if not fact.get("utf8") or fact.get("bom") or fact.get("lf_only") is False:
        raise ValueError(f"invalid Run status encoding or newline format: {path}")
    fields: dict[str, str] = {}
    data = _required_file(path, within=run_root)
    for line in data.decode("utf-8").splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip():
            fields[key.strip()] = value.strip()
    return fields


def _file_fact(path: Path, run_root: Path) -> dict[str, Any]:
    try:
        safe_path = _assert_read_target(path, run_root)
    except FileNotFoundError:
        return {"exists": False, "bytes": None}
    except (OSError, ValueError) as error:
        return {
            "exists": path.exists() or path.is_symlink(),
            "bytes": None,
            "unsafe": str(error),
        }
    fact: dict[str, Any] = {
        "exists": True,
        "bytes": safe_path.stat().st_size,
    }
    if safe_path.suffix.casefold() == ".md":
        data = safe_path.read_bytes()
        fact["bom"] = data.startswith(b"\xef\xbb\xbf")
        fact["lf_only"] = b"\r" not in data
        fact["nonempty"] = bool(data)
        try:
            data.decode("utf-8")
            fact["utf8"] = True
        except UnicodeDecodeError:
            fact["utf8"] = False
    return fact


def _workspace_directory_state(
    workspace: ResearchWorkspace, path: Path
) -> tuple[bool, str | None]:
    try:
        safe = workspace.assert_write_target(path)
    except (OSError, ValueError) as error:
        relative = path.relative_to(workspace.workspace_path).as_posix()
        return False, f"unsafe Run directory {relative}: {error}"
    if not safe.exists():
        return False, None
    if not safe.is_dir():
        relative = safe.relative_to(workspace.workspace_path).as_posix()
        return False, f"Run directory path is not a directory: {relative}"
    return True, None


def _directory_fact(
    path: Path, run_root: Path, research_owned_files: Sequence[Path]
) -> dict[str, Any]:
    if _is_reparse_point(path):
        return {"exists": True, "file_count": 0, "unsafe": "reparse point"}
    if not path.is_dir():
        return {"exists": False, "file_count": 0}
    count = 0
    unsafe = 0
    for item in research_owned_files:
        try:
            item.relative_to(path)
        except ValueError:
            continue
        try:
            _assert_read_target(item, run_root)
            count += 1
        except (OSError, ValueError):
            unsafe += 1
    fact = {"exists": True, "file_count": count}
    if unsafe:
        fact["unsafe_file_count"] = unsafe
    return fact


def _current_version_activity(
    run_root: Path,
    version: str,
    research_owned_files: Sequence[Path],
    status_fields: dict[str, str],
) -> dict[str, Any]:
    current_directory_names = tuple(
        f"{stem}_{version}"
        for stem in (
            "hypotheses",
            "implementation",
            "experiment",
            "review",
            "workbench",
            "audit",
        )
    )
    directories = [
        name
        for name in current_directory_names
        if not _is_reparse_point(run_root / name) and (run_root / name).is_dir()
    ]
    current_files = []
    for path in research_owned_files:
        relative = path.relative_to(run_root)
        if (
            relative.name.endswith(f"_{version}.md")
            or (relative.parts and relative.parts[0] in current_directory_names)
        ):
            current_files.append(relative.as_posix())
    current_files.sort()
    continuation_name = f"selection_context_{version}.md"
    continuation_path = run_root / continuation_name
    continuation_shaped = current_files == [continuation_name] and (
        _looks_like_continuation(continuation_path)
    )
    continuation_only = continuation_shaped and _is_continuation(
        continuation_path, run_root, status_fields
    )
    if not current_files and not directories:
        status = "ACTIVE_CURRENT_VERSION_EMPTY"
        new_action = False
    elif continuation_only:
        status = "ACTIVE_CURRENT_VERSION_CONTINUATION_ONLY"
        new_action = False
    elif continuation_shaped:
        status = "ACTIVE_CURRENT_VERSION_INVALID_CONTINUATION"
        new_action = False
    elif not current_files:
        status = "ACTIVE_CURRENT_VERSION_DIRECTORIES_ONLY"
        new_action = False
    else:
        status = "ACTIVE_CURRENT_VERSION_RESEARCH_ACTION_PRESENT"
        new_action = True
    return {
        "status": status,
        "research_owned_files": current_files,
        "research_owned_directories": directories,
        "continuation_only": continuation_only,
        "continuation_shaped_but_unbound": (
            continuation_shaped and not continuation_only
        ),
        "new_research_action_present": new_action,
        "quality_semantics": "raw_activity_fact_not_a_research_quality_metric",
    }


def _looks_like_continuation(path: Path) -> bool:
    try:
        text = _required_file(path, within=path.parent).decode("utf-8")
    except (FileNotFoundError, OSError, UnicodeError, ValueError):
        return False
    if not text.startswith("# Scientific Continuation ") or "- FROM_VERSION:" not in text:
        return False
    legacy_shape = all(
        marker in text
        for marker in (
            "- CHANGED_COORDINATE:",
            "## SURVIVING_FRONTIER",
            "## NEXT_HIGH_INFORMATION_ACTION",
        )
    )
    six_section_shape = all(
        marker in text
        for marker in (
            "## 当前最佳候选集合",
            "INCUMBENT_SET: INSUFFICIENT",
            "CHALLENGERS: INSUFFICIENT",
            "SURVIVING_FRONTIER:",
            "## 新增正向证据",
            "## 已失效或被杀范围",
            "## 剩余致命不确定性",
            "## 下一项最高信息量动作",
            "NEXT_HIGH_INFORMATION_ACTION:",
            "## 策略变化",
            "CHANGED_COORDINATE:",
        )
    )
    return legacy_shape or six_section_shape


def _is_continuation(
    path: Path, run_root: Path, status_fields: dict[str, str]
) -> bool:
    if not _looks_like_continuation(path):
        return False
    try:
        data = _required_file(path, within=run_root)
        text = data.decode("utf-8")
        ledger = _required_file(
            run_root / "RUN_LEDGER.md", within=run_root
        ).decode("utf-8")
    except (FileNotFoundError, OSError, UnicodeError, ValueError):
        return False
    if status_fields.get("LAST_DURABLE_ARTIFACT") != path.name:
        return False
    version_match = re.fullmatch(r"selection_context_(v\d{3,})\.md", path.name)
    from_match = re.search(r"(?m)^- FROM_VERSION: `?(v\d{3,})`?\s*$", text)
    if version_match is None or from_match is None:
        return False
    digest = hashlib.sha256(data).hexdigest()
    for event in _ledger_events(ledger):
        if (
            event.get("EVENT") == "VERSION_ADVANCED"
            and event.get("FROM_VERSION") == from_match.group(1)
            and event.get("VERSION") == version_match.group(1)
            and event.get("CONTINUATION") == path.name
            and event.get("CONTINUATION_SHA256") == digest
        ):
            return True
    return False


def _ledger_events(text: str) -> list[dict[str, str]]:
    events = []
    for chunk in re.split(r"(?m)^- EVENT: ", text)[1:]:
        lines = chunk.splitlines()
        if not lines:
            continue
        event = {"EVENT": lines[0].strip()}
        for line in lines[1:]:
            if not line.startswith("  "):
                break
            key, separator, value = line.strip().partition(":")
            if separator:
                event[key.strip()] = value.strip()
        events.append(event)
    return events


def _run_versions(run_root: Path) -> set[str]:
    versions: set[str] = set()
    for path in run_root.iterdir():
        versions.update(
            match.group(1) for match in _VERSION_IN_NAME.finditer(path.name)
        )
    return versions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect objective file facts for one CRL Run.")
    parser.add_argument("--product-root", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--version")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        report = inspect_run(
            arguments.run_root,
            arguments.version,
            product_root=arguments.product_root,
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"inspect_run: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
