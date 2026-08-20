from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import crl_v3.decision as decision_module
from crl_v3.decision import (
    delivery_material_errors,
    read_delivery,
    read_no_delivery_history,
)
from crl_v3.experiment import experiment_material_errors
from crl_v3.workspace import ResearchWorkspace
from conftest import make_run, publish_synthetic_fixed_review, record_successful_attempt
from tools.inspect_run import inspect_run
from tools.manage_run import advance_version, start_run


def _transition() -> dict[str, object]:
    return {
        "CHANGED_COORDINATE": "evaluation carrier",
        "SURVIVING_FRONTIER": "The next scientific period remains actionable.",
        "NEXT_HIGH_INFORMATION_ACTION": "Run the next killer experiment.",
    }


def _run(
    tmp_path: Path, *, mode: str = "AUTONOMOUS"
) -> tuple[Path, ResearchWorkspace]:
    product, run = make_run(tmp_path, mode=mode)
    return run, ResearchWorkspace(run, product_root=product)


def _directed_run(tmp_path: Path) -> tuple[Path, ResearchWorkspace]:
    return _run(tmp_path, mode="DIRECTED")


def _ready_for_review(
    tmp_path: Path, *, mode: str = "AUTONOMOUS"
) -> tuple[Path, ResearchWorkspace]:
    run, workspace = _run(tmp_path, mode=mode)
    for stem, content in (
        ("problem", "# Problem\n\nP"),
        ("research_map", "# Map\n\nM"),
        ("nearest_prior", "# Prior\n\nN"),
        ("candidate", "# Candidate\n\nC"),
        ("selection_context", "# Selection\n\nS"),
    ):
        workspace.write_document(stem, content)
    workspace.write_evidence_packet([], preface="本候选当前没有额外证据条目。")
    workspace.write_experiment_plan("# Plan\n\nP")
    code = tmp_path / "method.py"
    code.write_text("print('ok')\n", encoding="utf-8")
    workspace.save_experiment_artifact(code, "method.py", area="implementation")
    completed = record_successful_attempt(
        workspace.product_root,
        run,
        workspace.version,
        run / "implementation_v001" / "method.py",
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    workspace.write_experiment_result("# Result\n\nR")
    workspace.write_seed("# Seed\n\n值得扩大验证。")
    workspace.write_review_request(
        "review the method and report",
        [
            "seed_v001.md",
            "candidate_v001.md",
            "nearest_prior_v001.md",
            "experiment_v001/plan.md",
            "experiment_v001/result.md",
        ],
    )
    for number in (1, 2, 3):
        workspace.write_reviewer_report(number, f"task-{number}", f"report {number}")
    publish_synthetic_fixed_review(
        workspace,
        supporting_attempt_id="attempt-001",
        final_delivery=True,
    )
    return run, workspace


def test_decision_requires_all_three_reviews(tmp_path: Path) -> None:
    run, workspace = _run(tmp_path)
    workspace.write_problem("problem")
    workspace.write_seed("seed")
    workspace.write_review_request("review", ["seed_v001.md", "problem_v001.md"])
    workspace.write_reviewer_report(1, "task-1", "one")
    with pytest.raises(ValueError, match="no valid fixed Review"):
        workspace.write_review_decision("continue")
    assert not (run / "decision_v001.md").exists()


def test_delivery_requires_objective_materials_and_updates_status(tmp_path: Path) -> None:
    run, workspace = _ready_for_review(tmp_path)
    decision = workspace.write_review_decision(
        "三份意见均已阅读；保留收窄后的主张并交付。"
    )
    assert Path(decision.path).name == "decision_v001.md"
    assert delivery_material_errors(workspace, ("attempt-001",)) == ()

    delivery = workspace.write_delivery(supporting_attempt_ids=("attempt-001",))
    assert delivery.status == "DELIVERED"
    assert (run / "DELIVERY.md").is_file()
    assert "STATUS: DELIVERED" in (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    assert "EVENT: SEED_DELIVERED" in (run / "RUN_LEDGER.md").read_text(
        encoding="utf-8"
    )
    assert f"ARTIFACT_SHA256: {delivery.sha256}" in (
        run / "RUN_LEDGER.md"
    ).read_text(encoding="utf-8")
    with pytest.raises(FileExistsError):
        workspace.write_no_delivery("cannot coexist")


def test_two_review_decisions_can_continue_into_third_fresh_version_and_deliver(
    tmp_path: Path,
) -> None:
    run, first = _ready_for_review(tmp_path)
    first_request = (run / "review_v001/request.md").read_bytes()
    first.write_review_decision("当前证据不足以交付；继续本轮研究并推进版本。")

    advanced = advance_version(first.product_root, run.name, transition=_transition())
    assert advanced["previous_version"] == "v001"
    assert advanced["current_version"] == "v002"

    second = ResearchWorkspace(run, version="v002", product_root=first.product_root)
    second.write_seed("# Seed v002\n\n核心主张已完成独立本地验证。")
    source = run / "workbench_v002" / "v002-input.txt"
    source.parent.mkdir()
    source.write_text("independent evidence input\n", encoding="utf-8", newline="\n")
    completed = record_successful_attempt(
        second.product_root,
        run,
        "v002",
        source,
        attempt_id="attempt-v002",
    )
    assert completed.returncode == 0, completed.stderr.decode(
        "utf-8", errors="replace"
    )

    second.write_review_request("review the revised seed", ["seed_v002.md"])
    for number in (1, 2, 3):
        second.write_reviewer_report(
            number,
            f"fresh-v002-task-{number}",
            f"v002 report {number}",
        )
    publish_synthetic_fixed_review(
        second,
        supporting_attempt_id="attempt-v002",
        final_delivery=True,
    )
    second.write_review_decision("v002 仍有核心反例待处理；继续本轮研究。")

    advanced_again = advance_version(
        first.product_root, run.name, transition=_transition()
    )
    assert advanced_again["previous_version"] == "v002"
    assert advanced_again["current_version"] == "v003"

    third = ResearchWorkspace(run, version="v003", product_root=first.product_root)
    third.write_seed("# Seed v003\n\n核心反例已转为回归实验并完成独立验证。")
    third_source = run / "workbench_v003" / "v003-input.txt"
    third_source.parent.mkdir()
    third_source.write_text(
        "counterexample regression evidence\n",
        encoding="utf-8",
        newline="\n",
    )
    third_completed = record_successful_attempt(
        third.product_root,
        run,
        "v003",
        third_source,
        attempt_id="attempt-v003",
    )
    assert third_completed.returncode == 0, third_completed.stderr.decode(
        "utf-8", errors="replace"
    )
    third.write_review_request("review the third seed", ["seed_v003.md"])
    for number in (1, 2, 3):
        third.write_reviewer_report(
            number,
            f"fresh-v003-task-{number}",
            f"v003 report {number}",
        )
    publish_synthetic_fixed_review(
        third,
        supporting_attempt_id="attempt-v003",
        final_delivery=True,
    )
    third.write_review_decision("三份全新意见均已阅读；交付 v003。")
    terminal = third.write_delivery(supporting_attempt_ids=("attempt-v003",))

    assert terminal.status == "DELIVERED"
    assert terminal.version == "v003"
    assert (run / "decision_v001.md").is_file()
    assert (run / "decision_v002.md").is_file()
    assert (run / "decision_v003.md").is_file()
    assert (run / "review_v001/request.md").read_bytes() == first_request
    assert (run / "review_v002/request.md").is_file()
    assert (run / "review_v003/request.md").is_file()


def test_delivered_run_can_resume_and_accumulate_a_second_versioned_delivery(
    tmp_path: Path,
) -> None:
    run, first = _ready_for_review(tmp_path)
    first.write_review_decision("交付第一版。")
    first_delivery = first.write_delivery(supporting_attempt_ids=("attempt-001",))
    preserved = {
        "delivery": (run / "DELIVERY.md").read_bytes(),
        "seed": (run / "seed_v001.md").read_bytes(),
        "request": (run / "review_v001/request.md").read_bytes(),
        "decision": (run / "decision_v001.md").read_bytes(),
    }

    resumed = start_run(first.product_root, requested_run=run.name)
    assert resumed["status"] == "ACTIVE"
    assert resumed["current_version"] == "v002"
    with pytest.raises(ValueError, match="CURRENT_VERSION v002"):
        first.write_problem("不得回写旧版本。")

    second = ResearchWorkspace(run, version="v002", product_root=first.product_root)
    second.write_seed("# Seed v002\n\n新增且不可覆盖的科学版本。")
    source = run / "workbench_v002" / "v002-input.txt"
    source.parent.mkdir()
    source.write_text("new evidence\n", encoding="utf-8", newline="\n")
    completed = record_successful_attempt(
        second.product_root,
        run,
        "v002",
        source,
        attempt_id="attempt-v002",
    )
    assert completed.returncode == 0, completed.stderr.decode(
        "utf-8", errors="replace"
    )
    second.write_review_request("review v002", ["seed_v002.md"])
    for number in (1, 2, 3):
        second.write_reviewer_report(
            number, f"fresh-resume-v002-{number}", f"opinion {number}"
        )
    publish_synthetic_fixed_review(
        second,
        supporting_attempt_id="attempt-v002",
        final_delivery=True,
    )
    second.write_review_decision("交付第二版。")
    second_delivery = second.write_delivery(
        supporting_attempt_ids=("attempt-v002",)
    )

    assert Path(first_delivery.path).name == "DELIVERY.md"
    assert Path(second_delivery.path).name == "DELIVERY_v002.md"
    assert (run / "DELIVERY.md").read_bytes() == preserved["delivery"]
    assert (run / "seed_v001.md").read_bytes() == preserved["seed"]
    assert (run / "review_v001/request.md").read_bytes() == preserved["request"]
    assert (run / "decision_v001.md").read_bytes() == preserved["decision"]
    report = inspect_run(run, product_root=first.product_root)
    assert report["status"] == "DELIVERED"
    assert report["delivery_count"] == 2
    assert [item["version"] for item in report["delivery_history"]] == [
        "v001",
        "v002",
    ]
    assert report["errors"] == []


def test_resumed_delivery_can_end_no_go_without_erasing_prior_delivery(
    tmp_path: Path,
) -> None:
    run, first = _ready_for_review(tmp_path, mode="DIRECTED")
    first.write_review_decision("交付第一版。")
    first.write_delivery(supporting_attempt_ids=("attempt-001",))
    original_delivery = (run / "DELIVERY.md").read_bytes()
    resumed = start_run(first.product_root, requested_run=run.name)
    second = ResearchWorkspace(
        run, version=resumed["current_version"], product_root=first.product_root
    )

    terminal = second.write_no_delivery("继续研究后没有形成值得新增交付的结果。")

    assert terminal.status == "CONCLUDED_NO_DELIVERY"
    assert (run / "DELIVERY.md").read_bytes() == original_delivery
    report = inspect_run(run, product_root=first.product_root)
    assert report["status"] == "CONCLUDED_NO_DELIVERY"
    assert report["delivery_count"] == 1
    assert report["no_delivery_count"] == 1
    assert report["errors"] == []

    no_delivery_bytes = (run / "NO_DELIVERY.md").read_bytes()
    resumed_again = start_run(first.product_root, requested_run=run.name)
    assert resumed_again["current_version"] == "v003"
    third = ResearchWorkspace(run, version="v003", product_root=first.product_root)
    third.write_seed("# Seed v003\n\n恢复后形成新的独立证据。")
    source = run / "workbench_v003" / "v003-input.txt"
    source.parent.mkdir()
    source.write_text("v003 evidence\n", encoding="utf-8", newline="\n")
    completed = record_successful_attempt(
        third.product_root,
        run,
        "v003",
        source,
        attempt_id="attempt-v003",
    )
    assert completed.returncode == 0
    third.write_review_request("review v003", ["seed_v003.md"])
    for number in (1, 2, 3):
        third.write_reviewer_report(
            number, f"fresh-v003-after-no-go-{number}", f"opinion {number}"
        )
    publish_synthetic_fixed_review(
        third,
        supporting_attempt_id="attempt-v003",
        final_delivery=True,
    )
    third.write_review_decision("交付第三版。")
    third_delivery = third.write_delivery(
        supporting_attempt_ids=("attempt-v003",)
    )

    assert Path(third_delivery.path).name == "DELIVERY_v003.md"
    assert (run / "NO_DELIVERY.md").read_bytes() == no_delivery_bytes
    final_report = inspect_run(run, product_root=first.product_root)
    assert [item["version"] for item in final_report["delivery_history"]] == [
        "v001",
        "v003",
    ]
    assert [item["version"] for item in final_report["no_delivery_history"]] == [
        "v002"
    ]
    assert final_report["errors"] == []


def test_multiple_no_delivery_versions_are_preserved_and_ordered(
    tmp_path: Path,
) -> None:
    run, first = _directed_run(tmp_path)
    initial = first.write_no_delivery("第一次无交付。")
    initial_bytes = Path(initial.path).read_bytes()
    resumed = start_run(first.product_root, requested_run=run.name)
    second = ResearchWorkspace(
        run, version=resumed["current_version"], product_root=first.product_root
    )

    later = second.write_no_delivery("第二次无交付。")

    assert Path(initial.path).name == "NO_DELIVERY.md"
    assert Path(later.path).name == "NO_DELIVERY_v002.md"
    assert (run / "NO_DELIVERY.md").read_bytes() == initial_bytes
    history = read_no_delivery_history(second)
    assert [item.version for item in history] == ["v001", "v002"]
    report = inspect_run(run, product_root=first.product_root)
    assert report["status"] == "CONCLUDED_NO_DELIVERY"
    assert report["no_delivery_count"] == 2
    assert report["errors"] == []


def test_delivery_freezes_supporting_attempt_execution_identity(tmp_path: Path) -> None:
    run, workspace = _ready_for_review(tmp_path)
    workspace.write_review_decision("deliver")
    workspace.write_delivery(supporting_attempt_ids=("attempt-001",))

    attempt = run / "experiment_v001/attempts/attempt-001"
    output = attempt / "result.txt"
    output.write_text("replacement output\n", encoding="utf-8", newline="\n")
    execution_path = attempt / "execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    execution["outputs"][0]["after"]["size_bytes"] = output.stat().st_size
    execution["outputs"][0]["after"]["sha256"] = hashlib.sha256(
        output.read_bytes()
    ).hexdigest()
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    assert experiment_material_errors(workspace, ("attempt-001",)) == ()
    with pytest.raises(ValueError, match="supporting attempt changed"):
        read_delivery(workspace)


def test_default_broad_autonomous_can_publish_no_delivery(tmp_path: Path) -> None:
    run, workspace = _run(tmp_path)
    terminal = workspace.write_no_delivery(
        "经过真实回溯、正交再扩张和必要反证后，本次 Run 继续投入的预期科研价值不足。"
    )

    assert terminal.status == "CONCLUDED_NO_DELIVERY"
    assert (run / "NO_DELIVERY.md").is_file()
    assert "STATUS: CONCLUDED_NO_DELIVERY" in (run / "RUN_STATUS.md").read_text(
        encoding="utf-8"
    )
    assert "NO_DELIVERY_CONCLUDED" in (run / "RUN_LEDGER.md").read_text(
        encoding="utf-8"
    )


def test_no_delivery_rejects_run_mode_identity_mismatch(tmp_path: Path) -> None:
    run, workspace = _run(tmp_path)
    status_path = run / "RUN_STATUS.md"
    status_path.write_text(
        status_path.read_text(encoding="utf-8").replace(
            "MODE: AUTONOMOUS", "MODE: DIRECTED"
        ),
        encoding="utf-8",
        newline="\n",
    )

    with pytest.raises(ValueError, match="MODE identity differs"):
        workspace.write_no_delivery("must not bypass mode boundary")

    assert not (run / "NO_DELIVERY.md").exists()


def test_directed_no_delivery_needs_no_review_or_downstream_documents(
    tmp_path: Path,
) -> None:
    run, workspace = _directed_run(tmp_path)
    workspace.write_problem("方向经过初步探索后无价值。")
    terminal = workspace.write_no_delivery("最强方向存在不可修复的概念缺陷。")
    assert terminal.status == "CONCLUDED_NO_DELIVERY"
    assert not (run / "review_v001").exists()
    assert "CONCLUDED_NO_DELIVERY" in (run / "RUN_STATUS.md").read_text(
        encoding="utf-8"
    )
    assert "EVENT: NO_DELIVERY_CONCLUDED" in (run / "RUN_LEDGER.md").read_text(
        encoding="utf-8"
    )


def test_delivery_needs_no_legacy_research_documents_or_plan_result(tmp_path: Path) -> None:
    run, workspace = _run(tmp_path)
    workspace.write_seed("# Seed\n\n最小但自足的研究种子。")
    source = tmp_path / "method.py"
    source.write_text("print('method')\n", encoding="utf-8", newline="\n")
    artifact = workspace.save_experiment_artifact(
        source, "method.py", area="implementation"
    )
    completed = record_successful_attempt(
        workspace.product_root, run, "v001", Path(artifact.path)
    )
    assert completed.returncode == 0
    workspace.write_review_request("review", ["seed_v001.md"])
    for number in (1, 2, 3):
        workspace.write_reviewer_report(number, f"minimal-task-{number}", "opinion")
    publish_synthetic_fixed_review(
        workspace,
        supporting_attempt_id="attempt-001",
        final_delivery=True,
    )
    workspace.write_review_decision("deliver")
    terminal = workspace.write_delivery(supporting_attempt_ids=("attempt-001",))
    assert terminal.status == "DELIVERED"
    for stem in (
        "problem",
        "research_map",
        "nearest_prior",
        "candidate",
        "evidence_packet",
        "selection_context",
    ):
        assert not workspace.document_path(stem).exists()
    assert not (run / "experiment_v001/plan.md").exists()
    assert not (run / "experiment_v001/result.md").exists()


def test_delivery_is_blocked_when_raw_material_is_missing(tmp_path: Path) -> None:
    run, workspace = _ready_for_review(tmp_path)
    workspace.write_review_decision("deliver")
    (run / "experiment_v001/attempts/attempt-001/stdout.bin").unlink()
    with pytest.raises(ValueError, match="supporting attempt"):
        workspace.write_delivery(supporting_attempt_ids=("attempt-001",))
    assert not (run / "DELIVERY.md").exists()


def test_terminal_run_is_immutable_even_for_identical_rewrites(tmp_path: Path) -> None:
    run, workspace = _directed_run(tmp_path)
    first = workspace.write_no_delivery("reason")
    with pytest.raises(FileExistsError):
        workspace.write_no_delivery("reason")
    with pytest.raises(FileExistsError):
        workspace.write_problem("post-terminal mutation")
    assert (run / "NO_DELIVERY.md").read_text(encoding="utf-8") == first.content


def test_terminal_body_is_scanned_before_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run, workspace = _directed_run(tmp_path)
    secret = "sk-terminal-secret-123456789"
    monkeypatch.setenv("CRL_TEST_API_KEY", secret)
    with pytest.raises(ValueError, match="credential"):
        workspace.write_no_delivery(f"reason {secret}")
    assert not (run / "NO_DELIVERY.md").exists()

    run2, workspace2 = _run(tmp_path / "second")
    workspace2.write_seed(f"seed {secret}")
    workspace2.write_review_request("review", ["seed_v001.md"])
    for number in (1, 2, 3):
        workspace2.write_reviewer_report(number, f"secret-task-{number}", "report")
    publish_synthetic_fixed_review(workspace2)
    workspace2.write_review_decision("deliver")
    with pytest.raises(ValueError, match="environment secret"):
        workspace2.write_delivery(supporting_attempt_ids=("attempt-001",))
    assert not (run2 / "DELIVERY.md").exists()


def test_controlled_metadata_prefixes_are_free_text_outside_the_header(
    tmp_path: Path,
) -> None:
    run, workspace = _ready_for_review(tmp_path / "decision")
    decision_body = (
        "正文讨论 <!-- CRL_DECISION_META 、<!-- CRL_TERMINAL_META "
        "与 <!-- CRL_REVIEW_REPORT_META ，它们都不是头部元数据。"
    )
    written = workspace.write_review_decision(decision_body)
    assert decision_body in written.content
    delivered = workspace.write_delivery(supporting_attempt_ids=("attempt-001",))
    assert decision_body not in delivered.content
    assert "seed_v001.md" in delivered.content
    assert (run / "DELIVERY.md").is_file()

    run2, workspace2 = _directed_run(tmp_path / "no-go")
    no_go = workspace2.write_no_delivery(decision_body)
    assert decision_body in no_go.content
    assert (run2 / "NO_DELIVERY.md").is_file()


def test_duplicate_terminal_header_metadata_fails_before_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run, workspace = _directed_run(tmp_path)
    malformed = (
        '# No-Go\n'
        '<!-- CRL_TERMINAL_META {"status":"CONCLUDED_NO_DELIVERY","version":"v001"} -->\n'
        '<!-- CRL_TERMINAL_META {"status":"CONCLUDED_NO_DELIVERY","version":"v001"} -->\n'
        'reason\n'
    )
    monkeypatch.setattr(decision_module, "_render_terminal", lambda *args: malformed)
    with pytest.raises(ValueError, match="duplicate bounded metadata"):
        workspace.write_no_delivery("reason")
    assert not (run / "NO_DELIVERY.md").exists()
    assert "STATUS: ACTIVE" in (run / "RUN_STATUS.md").read_text(encoding="utf-8")


def test_terminal_control_write_failure_rolls_back_and_can_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run, workspace = _directed_run(tmp_path)
    original_status = (run / "RUN_STATUS.md").read_bytes()
    original_ledger = (run / "RUN_LEDGER.md").read_bytes()
    real_atomic_write = decision_module._atomic_write_text
    failed = False

    def fail_first_status_write(path, content, *, within=None):
        nonlocal failed
        if Path(path).name == "RUN_STATUS.md" and not failed:
            failed = True
            raise OSError("injected status write failure")
        return real_atomic_write(path, content, within=within)

    monkeypatch.setattr(
        decision_module, "_atomic_write_text", fail_first_status_write
    )
    with pytest.raises(OSError, match="injected status write failure"):
        workspace.write_no_delivery("reason")
    assert not (run / "NO_DELIVERY.md").exists()
    assert (run / "RUN_STATUS.md").read_bytes() == original_status
    assert (run / "RUN_LEDGER.md").read_bytes() == original_ledger

    monkeypatch.setattr(decision_module, "_atomic_write_text", real_atomic_write)
    terminal = workspace.write_no_delivery("reason")
    assert terminal.status == "CONCLUDED_NO_DELIVERY"


def test_binary_heuristic_is_warning_for_no_go_but_text_is_blocking(
    tmp_path: Path,
) -> None:
    run, workspace = _directed_run(tmp_path / "binary")
    (run / "model.bin").write_bytes(b"label=password=abcdefgh")
    terminal = workspace.write_no_delivery("no-go remains available")
    assert any("model.bin" in warning for warning in terminal.warnings)

    run2, workspace2 = _directed_run(tmp_path / "text")
    (run2 / "notes.txt").write_text(
        "password=abcdefgh\n", encoding="utf-8", newline="\n"
    )
    with pytest.raises(ValueError, match="credential-like text"):
        workspace2.write_no_delivery("must review text credential")
    assert not (run2 / "NO_DELIVERY.md").exists()


def test_third_party_credential_fixture_warns_without_moving_or_blocking(
    tmp_path: Path,
) -> None:
    run, workspace = _directed_run(tmp_path)
    fixture = run / "external" / "benchmark" / "fixture.py"
    fixture.parent.mkdir(parents=True)
    fixture.write_text(
        "password=abcdefgh\ntoken=abcdefghijkl\n",
        encoding="utf-8",
        newline="\n",
    )
    before = fixture.read_bytes()

    terminal = workspace.write_no_delivery("third-party fixture is preserved")

    assert terminal.status == "CONCLUDED_NO_DELIVERY"
    assert any("external/benchmark/fixture.py" in warning for warning in terminal.warnings)
    assert fixture.read_bytes() == before


def test_raw_search_and_run_source_fixtures_warn_without_blocking(
    tmp_path: Path,
) -> None:
    run, workspace = _directed_run(tmp_path)
    raw = run / "hypotheses_v001" / "searches" / "q" / "result.json"
    source = run / "workbench_v001" / "probe.py"
    raw.parent.mkdir(parents=True)
    source.parent.mkdir(parents=True)
    raw.write_text('{"example":"password=abcdefgh"}\n', encoding="utf-8", newline="\n")
    source.write_text("access_token='abcdefghijkl'\n", encoding="utf-8", newline="\n")

    terminal = workspace.write_no_delivery("fixtures remain auditable")

    assert terminal.status == "CONCLUDED_NO_DELIVERY"
    assert any("result.json" in warning for warning in terminal.warnings)
    assert any("probe.py" in warning for warning in terminal.warnings)


def test_many_nonblocking_heuristics_produce_one_bounded_summary_warning(
    tmp_path: Path,
) -> None:
    run, workspace = _directed_run(tmp_path)
    fixtures = run / "external" / "benchmark" / "fixtures"
    fixtures.mkdir(parents=True)
    for index in range(40):
        (fixtures / f"credential_fixture_{index:02d}.py").write_text(
            f"password=fixturevalue{index:02d}\n",
            encoding="utf-8",
            newline="\n",
        )

    terminal = workspace.write_no_delivery("large fixture tree remains auditable")

    assert terminal.status == "CONCLUDED_NO_DELIVERY"
    assert len(terminal.warnings) == 1
    warning = terminal.warnings[0]
    assert "40 Run files" in warning
    assert "representative paths (5/40)" in warning
    assert "credential_fixture_00.py" in warning
    assert "credential_fixture_04.py" in warning
    assert "credential_fixture_05.py" not in warning
    assert "credential_fixture_39.py" not in warning


def test_no_delivery_reuses_one_run_secret_scan_for_errors_and_warnings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run, workspace = _directed_run(tmp_path)
    fixture = run / "external" / "benchmark" / "fixture.py"
    fixture.parent.mkdir(parents=True)
    fixture.write_text("password=abcdefgh\n", encoding="utf-8", newline="\n")
    scanned_paths = []
    real_scan = decision_module.scan_file_secrets

    def counted_scan(path, secrets=None):
        scanned_paths.append(Path(path).relative_to(run).as_posix())
        return real_scan(path, secrets)

    monkeypatch.setattr(decision_module, "scan_file_secrets", counted_scan)

    terminal = workspace.write_no_delivery("reuse one scan")

    assert terminal.status == "CONCLUDED_NO_DELIVERY"
    assert scanned_paths
    assert len(scanned_paths) == len(set(scanned_paths))
    assert scanned_paths.count("external/benchmark/fixture.py") == 1


@pytest.mark.parametrize(
    ("relative", "content", "message"),
    [
        (".env", "UNMATCHED_NAME=value\n", "sensitive credential path"),
        (
            "research_workspace/key.txt",
            "-----BEGIN PRIVATE KEY-----\nfixture\n-----END PRIVATE KEY-----\n",
            "private key",
        ),
    ],
)
def test_high_confidence_secret_material_still_blocks_no_delivery(
    tmp_path: Path, relative: str, content: str, message: str
) -> None:
    run, workspace = _directed_run(tmp_path)
    path = run / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")

    with pytest.raises(ValueError, match=message) as caught:
        workspace.write_no_delivery("must block real secret material")

    assert relative in str(caught.value)
    assert not (run / "NO_DELIVERY.md").exists()


def test_real_environment_secret_in_binary_blocks_no_go(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run, workspace = _directed_run(tmp_path)
    secret = "real-binary-secret-123456789"
    monkeypatch.setenv("CRL_TEST_API_KEY", secret)
    (run / "model.bin").write_bytes(b"prefix\x00" + secret.encode("utf-8"))
    with pytest.raises(ValueError, match="environment secret"):
        workspace.write_no_delivery("must not terminalize with a real secret")
    assert not (run / "NO_DELIVERY.md").exists()
