from __future__ import annotations

from pathlib import Path

from crl_v3.workspace import ResearchWorkspace
from tools.manage_run import advance_version
from tools.inspect_run import inspect_run
from conftest import (
    make_directory_reparse_point,
    make_file_symlink,
    make_run,
    publish_synthetic_fixed_review,
    record_successful_attempt,
)


def _run(tmp_path: Path, status: str = "ACTIVE") -> Path:
    _, run = make_run(tmp_path, status=status)
    return run


def test_active_run_reports_facts_without_calling_incompleteness_failure(tmp_path: Path) -> None:
    run = _run(tmp_path)
    (run / "problem_v001.md").write_bytes(b"problem\n")
    report = inspect_run(run, product_root=run.parent)
    assert report["status"] == "ACTIVE"
    assert report["documents"]["problem_v001.md"]["exists"] is True
    assert report["errors"] == []
    assert report["warnings"] == []


def test_optional_empty_markdown_and_plan_only_are_not_research_failures(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    experiment = run / "experiment_v001"
    experiment.mkdir()
    (experiment / "plan.md").write_bytes(b"plan\n")
    (run / "memory_v001.md").write_bytes(b"")
    report = inspect_run(run, product_root=run.parent)
    assert report["experiment"]["attempt_count"] == 0
    assert not any("experiment material" in item for item in report["warnings"])
    assert not any("Markdown is empty" in item for item in report["errors"])


def test_inspect_reports_run_markdown_symlink_as_unsafe(tmp_path: Path) -> None:
    run = _run(tmp_path)
    outside = tmp_path / "outside.md"
    outside.write_text("outside\n", encoding="utf-8", newline="\n")
    make_file_symlink(run / "problem_v001.md", outside)
    report = inspect_run(run, product_root=run.parent)
    assert any("safe regular Run-local" in item for item in report["errors"])


def test_no_delivery_needs_only_matching_terminal_file(tmp_path: Path) -> None:
    run = _run(tmp_path, "CONCLUDED_NO_DELIVERY")
    (run / "NO_DELIVERY.md").write_bytes(
        b'# No-Go\n<!-- CRL_TERMINAL_META {"status":"CONCLUDED_NO_DELIVERY","version":"v001"} -->\n\nreason\n'
    )
    report = inspect_run(run, product_root=run.parent)
    assert report["terminal"] is True
    assert report["no_delivery_count"] == 1
    assert report["no_delivery_history"][0]["version"] == "v001"
    assert report["latest_no_delivery"]["path"] == "NO_DELIVERY.md"
    assert report["errors"] == []


def test_same_version_delivery_and_no_delivery_are_reported_as_conflict(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=run.parent)
    workspace.write_seed("# Seed\n\nvalidated")
    source = run / "workbench_v001" / "input.txt"
    source.parent.mkdir()
    source.write_text("evidence\n", encoding="utf-8", newline="\n")
    completed = record_successful_attempt(run.parent, run, "v001", source)
    assert completed.returncode == 0
    workspace.write_review_request("review", ["seed_v001.md"])
    for number in (1, 2, 3):
        workspace.write_reviewer_report(number, f"task-{number}", "opinion")
    publish_synthetic_fixed_review(
        workspace,
        supporting_attempt_id="attempt-001",
        final_delivery=True,
    )
    workspace.write_review_decision("deliver")
    workspace.write_delivery(supporting_attempt_ids=("attempt-001",))
    (run / "NO_DELIVERY.md").write_bytes(
        b'# No-Go\n<!-- CRL_TERMINAL_META {"status":"CONCLUDED_NO_DELIVERY","version":"v001"} -->\n\nreason\n'
    )

    report = inspect_run(run, product_root=run.parent)

    assert any(
        "multiple scientific conclusions exist for one version" in error
        for error in report["errors"]
    )


def test_unverifiable_delivery_history_is_an_error(tmp_path: Path) -> None:
    run = _run(tmp_path)
    (run / "DELIVERY.md").write_bytes(
        b'# Delivery\n<!-- CRL_TERMINAL_META {"status":"DELIVERED","version":"v001"} -->\n\nseed\n'
    )
    report = inspect_run(run, product_root=run.parent)
    assert any("invalid Delivery history" in error for error in report["errors"])


def test_no_go_with_an_unverifiable_delivery_record_is_rejected(tmp_path: Path) -> None:
    run = _run(tmp_path, "CONCLUDED_NO_DELIVERY")
    (run / "DELIVERY.md").write_bytes(
        b'# Delivery\n<!-- CRL_TERMINAL_META {"status":"DELIVERED","version":"v001"} -->\n\nseed\n'
    )
    (run / "NO_DELIVERY.md").write_bytes(
        b'# No-Go\n<!-- CRL_TERMINAL_META {"status":"CONCLUDED_NO_DELIVERY","version":"v001"} -->\n\nreason\n'
    )
    report = inspect_run(run, product_root=run.parent)
    assert any("invalid Delivery history" in error for error in report["errors"])


def test_delivered_status_exposes_missing_mechanical_materials(tmp_path: Path) -> None:
    run = _run(tmp_path, "DELIVERED")
    (run / "DELIVERY.md").write_bytes(
        b'# Delivery\n<!-- CRL_TERMINAL_META {"status":"DELIVERED","version":"v001"} -->\n\nseed\n'
    )
    report = inspect_run(run, product_root=run.parent)
    assert report["errors"]
    assert any("metadata" in error.lower() for error in report["errors"])


def test_future_version_artifact_is_reported_instead_of_silently_selected(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    (run / "candidate_v002.md").write_text(
        "future\n", encoding="utf-8", newline="\n"
    )
    report = inspect_run(run, product_root=run.parent)
    assert report["status_current_version"] == "v001"
    assert report["current_version"] == "v001"
    assert "v002" in report["available_versions"]
    assert any("newer than RUN_STATUS" in error for error in report["errors"])


def test_binary_credential_heuristic_is_visible_as_warning(tmp_path: Path) -> None:
    run = _run(tmp_path)
    (run / "problem_v001.md").write_bytes(b"problem\n")
    implementation = run / "implementation_v001"
    implementation.mkdir()
    (implementation / "model.bin").write_bytes(b"label=password=abcdefgh")
    report = inspect_run(run, product_root=run.parent)
    assert any("model.bin" in warning for warning in report["warnings"])
    assert not any("model.bin" in error for error in report["errors"])


def test_inspect_excludes_dependency_vendor_external_and_nested_repository_markdown(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    (run / "problem_v001.md").write_bytes(b"problem\n")
    excluded_paths = (
        run / "workbench_v001" / "external" / "bad.md",
        run / "implementation_v001" / "vendor" / "bad.md",
        run / "implementation_v001" / ".venv" / "bad.md",
        run / "implementation_v001" / "build" / "bad.md",
        run / "implementation_v001" / "dist" / "bad.md",
        run / "workbench_v001" / "repo" / "bad.md",
    )
    for path in excluded_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"third party\r\n")
    (run / "workbench_v001" / "repo" / ".git").mkdir()

    report = inspect_run(run, product_root=run.parent)

    serialized_errors = "\n".join(report["errors"])
    assert "bad.md" not in serialized_errors
    assert report["current_version_activity"]["new_research_action_present"] is True


def test_inspect_still_checks_research_owned_markdown_integrity(tmp_path: Path) -> None:
    run = _run(tmp_path)
    note = run / "workbench_v001" / "notes" / "research.md"
    note.parent.mkdir(parents=True)
    note.write_bytes("研究正文\r\n".encode("utf-8"))

    report = inspect_run(run, product_root=run.parent)

    assert any(
        "workbench_v001/notes/research.md" in error
        and "LF-only" in error
        for error in report["errors"]
    )


def test_inspect_rejects_invalid_utf8_and_bom_in_research_owned_markdown(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    (run / "problem_v001.md").write_bytes(b"\xffnot-utf8\n")
    (run / "candidate_v001.md").write_bytes(
        b"\xef\xbb\xbf# candidate\n"
    )

    report = inspect_run(run, product_root=run.parent)

    assert any(
        "problem_v001.md" in error and "valid UTF-8" in error
        for error in report["errors"]
    )
    assert any(
        "candidate_v001.md" in error and "UTF-8 BOM" in error
        for error in report["errors"]
    )


def test_active_empty_current_version_is_prominent(tmp_path: Path) -> None:
    run = _run(tmp_path)

    report = inspect_run(run, product_root=run.parent)

    assert "ACTIVE_CURRENT_VERSION_EMPTY" in report["errors"]
    assert report["current_version_activity"]["status"] == (
        "ACTIVE_CURRENT_VERSION_EMPTY"
    )


def test_legal_continuation_is_not_empty_but_has_no_new_research_action(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    advance_version(
        run.parent,
        run.name,
        transition={
            "CHANGED_COORDINATE": "测试坐标",
            "SURVIVING_FRONTIER": "仍存方向。",
            "NEXT_HIGH_INFORMATION_ACTION": "执行测试。",
        },
    )

    report = inspect_run(run, product_root=run.parent)

    assert "ACTIVE_CURRENT_VERSION_EMPTY" not in report["errors"]
    activity = report["current_version_activity"]
    assert activity["status"] == "ACTIVE_CURRENT_VERSION_CONTINUATION_ONLY"
    assert activity["continuation_only"] is True
    assert activity["new_research_action_present"] is False
    assert any("NO_NEW_RESEARCH_ACTION" in item for item in report["warnings"])


def test_handwritten_unbound_continuation_does_not_hide_empty_version(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    (run / "selection_context_v001.md").write_text(
        """# Scientific Continuation v001

- FROM_VERSION: `v000`
- CHANGED_COORDINATE: 测试坐标

## SURVIVING_FRONTIER

仍存方向。

## NEXT_HIGH_INFORMATION_ACTION

执行测试。
""",
        encoding="utf-8",
        newline="\n",
    )

    report = inspect_run(run, product_root=run.parent)

    assert "ACTIVE_CURRENT_VERSION_EMPTY" in report["errors"]
    activity = report["current_version_activity"]
    assert activity["status"] == "ACTIVE_CURRENT_VERSION_INVALID_CONTINUATION"
    assert activity["continuation_only"] is False
    assert activity["continuation_shaped_but_unbound"] is True
    assert activity["new_research_action_present"] is False


def test_tampered_continuation_hash_does_not_hide_empty_version(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    advance_version(
        run.parent,
        run.name,
        transition={
            "CHANGED_COORDINATE": "测试坐标",
            "SURVIVING_FRONTIER": "仍存方向。",
            "NEXT_HIGH_INFORMATION_ACTION": "执行测试。",
        },
    )
    continuation = run / "selection_context_v002.md"
    continuation.write_text(
        continuation.read_text(encoding="utf-8") + "\n被修改。\n",
        encoding="utf-8",
        newline="\n",
    )

    report = inspect_run(run, product_root=run.parent)

    assert "ACTIVE_CURRENT_VERSION_EMPTY" in report["errors"]
    assert report["current_version_activity"]["status"] == (
        "ACTIVE_CURRENT_VERSION_INVALID_CONTINUATION"
    )


def test_inspect_checks_prior_audit_markdown_and_excludes_its_vendor_tree(
    tmp_path: Path,
) -> None:
    run = _run(tmp_path)
    report_path = run / "audit_v001" / "audit-001" / "report.md"
    report_path.parent.mkdir(parents=True)
    report_path.write_bytes("先行审计\r\n".encode("utf-8"))
    vendor = run / "audit_v001" / "audit-001" / "vendor" / "bad.md"
    vendor.parent.mkdir()
    vendor.write_bytes(b"third party\r\n")

    report = inspect_run(run, product_root=run.parent)

    errors = "\n".join(report["errors"])
    assert "audit_v001/audit-001/report.md" in errors
    assert "audit_v001/audit-001/vendor/bad.md" not in errors


def test_excluded_directory_name_does_not_hide_reparse_point(tmp_path: Path) -> None:
    run = _run(tmp_path)
    implementation = run / "implementation_v001"
    implementation.mkdir()
    outside = tmp_path / "outside-vendor"
    make_directory_reparse_point(implementation / "vendor", outside)

    report = inspect_run(run, product_root=run.parent)

    assert any("RUN_RESEARCH_PATH_SCAN_UNSAFE" in item for item in report["errors"])


def test_experiment_ancestor_junction_is_not_enumerated(tmp_path: Path) -> None:
    run = _run(tmp_path)
    outside = tmp_path / "outside-experiment"
    (outside / "attempts" / "leaked-external-name").mkdir(parents=True)
    make_directory_reparse_point(run / "experiment_v001", outside)

    report = inspect_run(run, product_root=run.parent)

    errors = "\n".join(report["errors"])
    assert "RUN_RESEARCH_PATH_SCAN_UNSAFE" in errors
    assert "unsafe Run directory experiment_v001" in errors
    assert "leaked-external-name" not in errors
    assert report["experiment"]["attempt_count"] == 0


def test_review_ancestor_junction_is_not_enumerated(tmp_path: Path) -> None:
    run = _run(tmp_path)
    outside = tmp_path / "outside-review"
    (outside / "evaluations" / "leaked-review-name").mkdir(parents=True)
    make_directory_reparse_point(run / "review_v001", outside)

    report = inspect_run(run, product_root=run.parent)

    errors = "\n".join(report["errors"])
    review_errors = "\n".join(report["review"]["material_errors"])
    assert "RUN_RESEARCH_PATH_SCAN_UNSAFE" in errors
    assert "unsafe Run directory review_v001" in review_errors
    assert "leaked-review-name" not in errors + review_errors


def test_inspect_blocks_real_environment_secret_in_research_file(
    tmp_path: Path, monkeypatch
) -> None:
    run = _run(tmp_path)
    secret = "crl-inspect-real-secret-value-20260818"
    monkeypatch.setenv("CRL_INSPECT_TEST_SECRET", secret)
    (run / "problem_v001.md").write_text(
        f"accidental {secret}\n", encoding="utf-8", newline="\n"
    )

    report = inspect_run(run, product_root=run.parent)

    assert any(
        "environment secret" in item and "problem_v001.md" in item
        for item in report["errors"]
    )


def test_inspect_blocks_root_sensitive_file_and_credential_store(tmp_path: Path) -> None:
    run = _run(tmp_path)
    (run / "problem_v001.md").write_bytes(b"problem\n")
    (run / ".env").write_bytes(b"PLACEHOLDER=value\n")
    credential = run / "workbench_v001" / "credentials" / "profile.txt"
    credential.parent.mkdir(parents=True)
    credential.write_bytes(b"not-read-by-inspector\n")

    report = inspect_run(run, product_root=run.parent)

    errors = "\n".join(report["errors"])
    assert "sensitive credential path" in errors
    assert ".env" in errors
    assert "workbench_v001/credentials/" in errors
