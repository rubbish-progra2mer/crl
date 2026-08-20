from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

import crl_v3.recall as recall_module
import crl_v3.recorded as recorded_module
from conftest import (
    make_directory_reparse_point,
    make_run,
    prepare_experiment_spec,
    record_successful_attempt,
    set_current_version,
)
from crl_v3.cli import main
from crl_v3.diagnosis import collect_diagnosis
from crl_v3.experiment import valid_supporting_attempt_ids
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
    portfolio_to_dict,
    transition_hypothesis,
)
from crl_v3.recall import rebuild_recall, resume_recall, search_recall
from crl_v3.recorded import run_recorded
from crl_v3.tool_forge import RunToolContext, create_run_tool
from crl_v3.workspace import ResearchWorkspace


def _diagnosis_hypothesis_payload(hypothesis_id: str) -> dict[str, object]:
    text = f"完整候选 {hypothesis_id}"
    return {
        "hypothesis_id": hypothesis_id,
        "title": text,
        "parent_ids": [],
        "lineage_note": "独立测试候选。",
        "problem": text,
        "target_failure": {"summary": text, "card_ids": [], "evidence_ids": []},
        "changed_computation": {
            "baseline": text,
            "intervention": text,
            "information_available": text,
            "timing": text,
            "budget_effect": text,
        },
        "mechanism_claim": text,
        "falsifier": text,
        "minimal_killer_experiment": text,
        "nearest_prior_risk": text,
        "alternative_explanations": ["替代解释"],
        "descriptors": {
            "problem_family": text,
            "computation_stage": text,
            "intervention_family": text,
            "information_source": text,
            "timing_class": text,
            "budget_class": text,
            "evaluation_mode": text,
        },
        "literature_refs": [],
    }


def _diagnosis_decision() -> dict[str, object]:
    return {
        "evidence_fidelity": "SCREENING",
        "kill_target": "METHOD_CORE",
        "subject_scope": {
            "models": ["local"],
            "tasks": ["probe"],
            "datasets": ["fixture"],
            "seeds": ["1"],
            "environment": "local",
        },
        "independent_implementation_count": 1,
        "structural_refutation": False,
        "structural_refutation_reason": "",
        "killed": "当前方法核心",
        "survives": "现象仍需检查",
        "why": "测试决策事件。",
    }


def _write_closed_hypotheses(
    workspace: ResearchWorkspace, statuses: list[str]
) -> None:
    portfolio = empty_portfolio(
        workspace.workspace_path.name,
        workspace.version,
        now="2026-08-18T00:00:00Z",
    )
    for index in range(len(statuses)):
        portfolio = add_hypothesis(
            portfolio,
            create_hypothesis_record(
                _diagnosis_hypothesis_payload(f"h-{index + 1:03d}"),
                now=f"2026-08-18T00:{index:02d}:00Z",
            ),
            now=f"2026-08-18T00:{index:02d}:01Z",
        )
    for index in range(len(statuses)):
        portfolio = transition_hypothesis(
            portfolio,
            f"h-{index + 1:03d}",
            "active",
            "进入验证",
            now=f"2026-08-18T01:{index:02d}:00Z",
        )
    for index, status in enumerate(statuses):
        portfolio = transition_hypothesis(
            portfolio,
            f"h-{index + 1:03d}",
            status,
            "实验前关闭",
            decision=_diagnosis_decision(),
            now=f"2026-08-18T02:{index:02d}:00Z",
        )
    workspace.write_hypotheses(
        portfolio, expected_sha256=None, create_only=True
    )


def test_recall_fts_finds_early_thought_and_excludes_secrets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    note = run / "workbench_v001" / "notes" / "early.md"
    note.parent.mkdir(parents=True)
    note.write_text(
        "The stale trajectory evidence contradicts the current memory story.\n",
        encoding="utf-8",
        newline="\n",
    )
    (run / ".env").write_text("PASSWORD=do-not-index\n", encoding="utf-8", newline="\n")
    secret = "unique-secret-value-2026"
    monkeypatch.setenv("CRL_TEST_TOKEN", secret)
    (note.parent / "ordinary.log").write_text(
        f"accidental {secret}\n", encoding="utf-8", newline="\n"
    )

    manifest = rebuild_recall(workspace)
    result = search_recall(workspace, "memory contradiction", limit=5)

    assert manifest["semantic_status"] == "DEGRADED"
    assert result["semantic_status"] == "DEGRADED"
    assert result["hits"][0]["path"].endswith("early.md")
    excluded = {item["path"]: item["reason"] for item in manifest["excluded_files"]}
    assert excluded[".env"] == "sensitive_filename"
    assert excluded["workbench_v001/notes/ordinary.log"] == "environment_secret_match"
    assert secret not in json.dumps(result)


def test_recall_allows_security_topic_names_and_research_solution_directories(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    safe_files = {
        "workbench_v001/secret_sharing_agent_failure.md": "shamir-topic-marker\n",
        "workbench_v001/credential_delegation_study.md": (
            "credential and password safety discussion delegation-topic-marker\n"
        ),
        "workbench_v001/solution/analysis.md": "research-solution-marker\n",
        "workbench_v001/answers/interpretation.md": "research-answer-marker\n",
    }
    for relative, text in safe_files.items():
        path = run / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    credential_store = run / "workbench_v001" / "credentials" / "profile.txt"
    credential_store.parent.mkdir(parents=True)
    credential_store.write_text("credential-store-marker\n", encoding="utf-8", newline="\n")
    private_key = run / "workbench_v001" / "notes" / "agent.pem"
    private_key.parent.mkdir(parents=True)
    private_key.write_text("not a real key\n", encoding="utf-8", newline="\n")

    manifest = rebuild_recall(workspace)

    indexed = {item["path"] for item in manifest["indexed_files"]}
    assert set(safe_files).issubset(indexed)
    assert search_recall(workspace, "shamir topic marker")["hits"]
    assert search_recall(workspace, "delegation topic marker")["hits"]
    assert search_recall(workspace, "research solution marker")["hits"]
    excluded = {item["path"]: item["reason"] for item in manifest["excluded_files"]}
    assert excluded["workbench_v001/credentials/"] == "credential_store_tree"
    assert excluded["workbench_v001/notes/agent.pem"] == "sensitive_filename"


def test_recall_root_research_files_follow_current_runtime_guide(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    portfolio = run / "hypothesis_portfolio_v001.md"
    no_delivery = run / "NO_DELIVERY_v002.md"
    portfolio.write_text("portfolio-root-marker\n", encoding="utf-8", newline="\n")
    no_delivery.write_text("historical-nogo-marker\n", encoding="utf-8", newline="\n")

    manifest = rebuild_recall(workspace)

    indexed = {item["path"] for item in manifest["indexed_files"]}
    assert "hypothesis_portfolio_v001.md" in indexed
    assert "NO_DELIVERY_v002.md" in indexed
    assert search_recall(workspace, "portfolio root marker")["hits"][0]["path"] == (
        "hypothesis_portfolio_v001.md"
    )


def test_recall_indexes_research_owned_material_and_excludes_raw_and_third_party(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    research = run / "research_workspace" / "note.md"
    summary = run / "workbench_v001" / "result_summary.md"
    search = run / "hypotheses_v001" / "searches" / "q"
    external = run / "external" / "appworld" / "ground_truth"
    hidden = run / "research_workspace" / "ground_truth"
    environment = run / "env" / "package"
    for path, text in (
        (research, "research-owned alpha\n"),
        (summary, "scratch-owned beta\n"),
        (search / "report.md", "compact-owned gamma\n"),
        (search / "result.json", '{"raw": "raw-only delta"}\n'),
        (external / "solution.py", "third-party epsilon\n"),
        (hidden / "answer.txt", "hidden zeta\n"),
        (environment / "module.py", "environment eta\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    manifest = rebuild_recall(workspace)

    assert search_recall(workspace, "alpha")["hits"][0]["path"] == "research_workspace/note.md"
    assert search_recall(workspace, "beta")["hits"][0]["path"] == "workbench_v001/result_summary.md"
    assert search_recall(workspace, "gamma")["hits"][0]["path"].endswith("report.md")
    assert search_recall(workspace, "delta")["hits"] == []
    excluded = {item["path"]: item["reason"] for item in manifest["excluded_files"]}
    assert excluded["hypotheses_v001/searches/q/result.json"] == "raw_search_payload"
    assert excluded["external/"] == "third_party_tree"
    assert excluded["env/"] == "generated_environment_tree"
    assert excluded["research_workspace/ground_truth/"] == "ground_truth_tree"


def test_recall_excludes_nested_git_roots_and_derived_diagnosis(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    repository = run / "workbench_v001" / "cloned-project"
    (repository / ".git").mkdir(parents=True)
    (repository / "source.py").write_text(
        "nested-repository-marker\n", encoding="utf-8", newline="\n"
    )
    worktree = run / "workbench_v001" / "linked-worktree"
    worktree.mkdir(parents=True)
    (worktree / ".git").write_text(
        "gitdir: C:/elsewhere/.git/worktrees/x\n",
        encoding="utf-8",
        newline="\n",
    )
    (worktree / "source.py").write_text(
        "worktree-marker\n", encoding="utf-8", newline="\n"
    )
    diagnosis = run / "workbench_v001" / "diagnosis" / "old" / "report.md"
    diagnosis.parent.mkdir(parents=True)
    diagnosis.write_text("diagnosis-self-marker\n", encoding="utf-8", newline="\n")

    manifest = rebuild_recall(workspace)

    indexed = {item["path"] for item in manifest["indexed_files"]}
    assert not any("cloned-project" in path for path in indexed)
    assert not any("linked-worktree" in path for path in indexed)
    assert not any("/diagnosis/" in path for path in indexed)
    excluded = {item["path"]: item["reason"] for item in manifest["excluded_files"]}
    assert excluded["workbench_v001/cloned-project/"] == "nested_repository_tree"
    assert excluded["workbench_v001/linked-worktree/"] == "nested_repository_tree"
    assert excluded["workbench_v001/diagnosis/"] == "derived_diagnosis_tree"


def test_recall_indexes_prior_audit_reports_but_not_its_vendor_tree(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    report = run / "audit_v001" / "audit-001" / "report.md"
    report.parent.mkdir(parents=True)
    report.write_text("prior-audit-owned-marker\n", encoding="utf-8", newline="\n")
    vendor = run / "audit_v001" / "audit-001" / "vendor" / "noise.md"
    vendor.parent.mkdir()
    vendor.write_text("vendor-noise-marker\n", encoding="utf-8", newline="\n")

    manifest = rebuild_recall(workspace)

    indexed = {item["path"] for item in manifest["indexed_files"]}
    assert "audit_v001/audit-001/report.md" in indexed
    assert "audit_v001/audit-001/vendor/noise.md" not in indexed


def test_recall_does_not_return_changed_or_deleted_sources_and_rebuild_removes_them(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    note = run / "research_workspace" / "stale.md"
    note.parent.mkdir(parents=True)
    note.write_text("old-stale-marker\n", encoding="utf-8", newline="\n")
    rebuild_recall(workspace)

    note.write_text("replacement-marker\n", encoding="utf-8", newline="\n")
    stale = search_recall(workspace, "old stale marker")
    assert stale["hits"] == []
    assert stale["stale_sources"] == ["research_workspace/stale.md"]

    note.unlink()
    rebuilt = rebuild_recall(workspace)
    assert all(item["path"] != "research_workspace/stale.md" for item in rebuilt["indexed_files"])
    assert search_recall(workspace, "old stale marker")["hits"] == []


def test_recall_resume_uses_recent_key_context_and_degrades_to_fts(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    early = run / "workbench_v001" / "notes" / "early.md"
    early.parent.mkdir(parents=True)
    early.write_text(
        "Sparse handoffs expose a latent delegation bottleneck.\n",
        encoding="utf-8",
        newline="\n",
    )
    (run / "selection_context_v001.md").write_text(
        "The current candidate targets the delegation bottleneck under sparse handoffs.\n",
        encoding="utf-8",
        newline="\n",
    )
    rebuild_recall(workspace)

    result = resume_recall(workspace, limit=8)

    recovery = next(
        section
        for section in result["sections"]
        if section["kind"] == "recent_context_recovery"
    )
    assert result["semantic_status"] == "DEGRADED"
    assert recovery["semantic_reason"] == "semantic_index_missing"
    assert recovery["source_files"][0]["path"] == "selection_context_v001.md"
    assert any(hit["path"].endswith("early.md") for hit in recovery["hits"])
    anchors = [
        section["query"]
        for section in result["sections"]
        if section["kind"] == "fixed_anchor"
    ]
    assert all(" OR " not in query for query in anchors)
    assert any("失败" in query for query in anchors)
    assert any("实验" in query for query in anchors)


def test_recall_resume_uses_existing_semantic_index_for_early_paraphrase(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    early = run / "workbench_v001" / "notes" / "early.md"
    early.parent.mkdir(parents=True)
    early.write_text(
        "An orphaned latent trail appeared before convergence.\n",
        encoding="utf-8",
        newline="\n",
    )
    (run / "selection_context_v001.md").write_text(
        "The current candidate addresses coordination obstruction.\n",
        encoding="utf-8",
        newline="\n",
    )

    def fake_encode(texts, *_arguments):
        return np.asarray(
            [
                [1.0, 0.0]
                if "orphaned latent trail" in text.casefold()
                or "coordination obstruction" in text.casefold()
                else [0.0, 1.0]
                for text in texts
            ],
            dtype=np.float32,
        )

    monkeypatch.setattr(recall_module, "_encode", fake_encode)
    rebuild_recall(workspace, semantic=True)

    result = resume_recall(workspace, limit=8)

    recovery = next(
        section
        for section in result["sections"]
        if section["kind"] == "recent_context_recovery"
    )
    early_hit = next(hit for hit in recovery["hits"] if hit["path"].endswith("early.md"))
    assert result["semantic_status"] == "READY"
    assert recovery["semantic_status"] == "READY"
    assert early_hit["semantic_rank"] is not None


def test_fts_refresh_preserves_only_compatible_semantic_derivative(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    note = run / "research_workspace" / "semantic.md"
    note.parent.mkdir(parents=True)
    note.write_text("stable semantic marker\n", encoding="utf-8", newline="\n")

    def fake_encode(texts, *_arguments):
        return np.asarray([[1.0, 0.0] for _ in texts], dtype=np.float32)

    monkeypatch.setattr(recall_module, "_encode", fake_encode)
    first = rebuild_recall(workspace, semantic=True)
    vector_path = run / ".crl" / "recall" / "semantic_vectors.npz"
    vector_bytes = vector_path.read_bytes()

    unchanged = rebuild_recall(workspace)

    assert first["semantic_status"] == "READY"
    assert unchanged["semantic_status"] == "READY"
    assert unchanged["semantic_reason"] is None
    assert vector_path.read_bytes() == vector_bytes
    assert search_recall(workspace, "stable marker")["semantic_status"] == "READY"

    note.write_text("changed semantic marker\n", encoding="utf-8", newline="\n")
    changed = rebuild_recall(workspace)
    result = search_recall(workspace, "changed marker")

    assert vector_path.is_file()
    assert changed["semantic_status"] == "DEGRADED"
    assert changed["semantic_reason"] == "semantic_index_stale"
    assert result["semantic_status"] == "DEGRADED"
    assert result["semantic_reason"] == "semantic_index_stale"
    assert result["hits"][0]["fts_rank"] == 1


def test_semantic_query_rejects_embedding_identity_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    note = run / "research_workspace" / "identity.md"
    note.parent.mkdir(parents=True)
    note.write_text("embedding identity marker\n", encoding="utf-8", newline="\n")

    def fake_encode(texts, *_arguments):
        return np.asarray([[1.0, 0.0] for _ in texts], dtype=np.float32)

    monkeypatch.setattr(recall_module, "_encode", fake_encode)
    rebuild_recall(workspace, semantic=True)
    monkeypatch.setattr(recall_module, "DEFAULT_MODEL_REVISION", "incompatible-revision")

    result = search_recall(workspace, "identity marker")

    assert result["semantic_status"] == "DEGRADED"
    assert result["semantic_reason"] == "semantic_model_identity_mismatch"
    assert result["hits"][0]["fts_rank"] == 1


def test_semantic_query_rejects_reparse_vector_and_keeps_fts_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    note = run / "research_workspace" / "reparse.md"
    note.parent.mkdir(parents=True)
    note.write_text("reparsefallbackonly\n", encoding="utf-8", newline="\n")

    def fake_encode(texts, *_arguments):
        return np.asarray([[1.0, 0.0] for _ in texts], dtype=np.float32)

    monkeypatch.setattr(recall_module, "_encode", fake_encode)
    rebuild_recall(workspace, semantic=True)
    vector_path = run / ".crl" / "recall" / "semantic_vectors.npz"
    vector_path.unlink()
    make_directory_reparse_point(vector_path, tmp_path / "outside-semantic-vector")

    def fail_if_followed(*_arguments, **_keywords):
        raise AssertionError("unsafe semantic vector was followed")

    monkeypatch.setattr(recall_module.np, "load", fail_if_followed)
    result = search_recall(workspace, "reparsefallbackonly")

    assert result["semantic_status"] == "DEGRADED"
    assert result["semantic_reason"] == "semantic_index_unsafe"
    assert result["hits"][0]["fts_rank"] == 1
    assert result["hits"][0]["semantic_rank"] is None


def test_recall_excludes_raw_reviewer_telemetry_but_keeps_normalized_report(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    evaluation = run / "review_v001" / "evaluations" / "eval-0001"
    role = evaluation / "SCI"
    role.mkdir(parents=True)
    files = {
        evaluation / "packet.md": "packetduplicateonly\n",
        role / "events.jsonl": '{"raw":"eventtelemetryonly"}\n',
        role / "raw_output.json": '{"raw":"reviewerrawonly"}\n',
        role / "report.json": '{"diagnostic":"normalizedreviewonly"}\n',
    }
    for path, text in files.items():
        path.write_text(text, encoding="utf-8", newline="\n")

    manifest = rebuild_recall(workspace)

    assert search_recall(workspace, "normalizedreviewonly")["hits"][0]["path"] == (
        "review_v001/evaluations/eval-0001/SCI/report.json"
    )
    assert search_recall(workspace, "eventtelemetryonly")["hits"] == []
    assert search_recall(workspace, "reviewerrawonly")["hits"] == []
    assert search_recall(workspace, "packetduplicateonly")["hits"] == []
    excluded = {item["path"]: item["reason"] for item in manifest["excluded_files"]}
    assert excluded["review_v001/evaluations/eval-0001/packet.md"] == (
        "duplicate_review_packet"
    )
    assert excluded["review_v001/evaluations/eval-0001/SCI/events.jsonl"] == (
        "raw_reviewer_telemetry"
    )
    assert excluded["review_v001/evaluations/eval-0001/SCI/raw_output.json"] == (
        "raw_reviewer_telemetry"
    )


def test_diagnosis_is_fact_only_and_does_not_change_run_status(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    (run / "problem_v001.md").write_text(
        "TODO test an assumption after a failed baseline.\n",
        encoding="utf-8",
        newline="\n",
    )
    for search_id in ("initial-scope-001", "orthogonal-tool-retrieval-001"):
        search = run / "hypotheses_v001" / "searches" / search_id
        search.mkdir(parents=True)
        (search / "request.json").write_text(
            "{}\n", encoding="utf-8", newline="\n"
        )
    (run / ".pytest_cache").mkdir()
    (run / ".pytest_cache" / "noise.txt").write_text(
        "cache noise\n", encoding="utf-8", newline="\n"
    )
    (run / "workbench_v001" / "__pycache__").mkdir(parents=True)
    (run / "workbench_v001" / "__pycache__" / "noise.pyc").write_bytes(
        b"bytecode"
    )
    rebuild_recall(workspace)
    before = (run / "RUN_STATUS.md").read_bytes()
    ledger_before = (run / "RUN_LEDGER.md").read_bytes()

    result = collect_diagnosis(workspace, "before-review")

    assert result["authority"] == "ADVISORY_NON_AUTHORITATIVE"
    facts = result["facts"]
    assert facts["non_judgments"]
    assert [item["path"] for item in facts["search_snapshot_files"]] == [
        "hypotheses_v001/searches/initial-scope-001/request.json",
        "hypotheses_v001/searches/orthogonal-tool-retrieval-001/request.json",
    ]
    assert facts["recall_status"]["status"] == "READY"
    assert facts["recall_status"]["semantic_status"] == "DEGRADED"
    assert facts["recall_status"]["semantic_reason"] == "semantic_index_missing"
    assert "machine_fingerprint" not in facts
    assert ".pyc" not in facts["file_type_counts"]
    assert all(
        ".pytest_cache" not in item["path"] and "__pycache__" not in item["path"]
        for item in facts["recent_files"]
    )
    assert (run / "RUN_STATUS.md").read_bytes() == before
    assert (run / "RUN_LEDGER.md").read_bytes() == ledger_before
    assert not (run / "NO_DELIVERY.md").exists()


def test_diagnosis_uses_formal_integrity_validation(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    source = run / "workbench_v001" / "input.txt"
    source.parent.mkdir(parents=True)
    source.write_text("diagnosis formal input\n", encoding="utf-8", newline="\n")
    completed = record_successful_attempt(product, run, "v001", source)
    assert completed.returncode == 0, completed.stderr.decode(
        "utf-8", errors="replace"
    )
    workspace = ResearchWorkspace(run, product_root=product)
    rebuild_recall(workspace)

    facts = collect_diagnosis(workspace, "formal-validity")["facts"]

    assert facts["experiments"]["valid_formal_count"] == 1
    formal = facts["run_wide"]["experiments"]["formal_review_support"]
    assert formal["valid_attempt_count"] == 1
    assert formal["attempts"][0]["valid_review_support"] is True


def test_diagnosis_separates_current_version_and_run_wide_research_facts(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    set_current_version(run, "v002")
    workspace = ResearchWorkspace(run, product_root=product, version="v002")
    for version in ("v001", "v002"):
        workbench = run / f"workbench_{version}"
        workbench.mkdir()
        (workbench / "scratch_report.md").write_text(
            f"scratch {version}\n", encoding="utf-8", newline="\n"
        )
    portfolio = run / "hypotheses_v001" / "portfolio.json"
    portfolio.parent.mkdir()
    portfolio.write_text(
        json.dumps(
            {
                "hypotheses": [
                    {"status": "prior_collision", "status_reason": "direct prior"},
                    {"status": "falsified", "status_reason": "fair baseline"},
                ]
            }
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    search = run / "hypotheses_v002" / "searches" / "targeted"
    search.mkdir(parents=True)
    (search / "request.json").write_text(
        json.dumps(
            {
                "input_identity": {"query_count": 1},
                "queries": [
                    {
                        "query_id": "q001",
                        "original_query": "same query",
                        "normalized_query": '"same" OR "query"',
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (search / "report.md").write_text(
        "- 代表项：3 / 去重 Paper：7\n", encoding="utf-8", newline="\n"
    )
    (search / "result.json").write_text(
        '{"large":"raw"}\n', encoding="utf-8", newline="\n"
    )
    subagent = run / "research_workspace" / "subagents" / "prior_attack.md"
    subagent.parent.mkdir(parents=True)
    subagent.write_text("summary\n", encoding="utf-8", newline="\n")
    rebuild_recall(workspace)
    manifest_path = run / ".crl" / "recall" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["indexed_files"].extend(
        [
            {"path": "external/appworld/source.py", "size_bytes": 10, "sha256": "0" * 64},
            {"path": "external/appworld/ground_truth/solution.py", "size_bytes": 10, "sha256": "1" * 64},
            {"path": "hypotheses_v001/searches/old/result.json", "size_bytes": 10, "sha256": "2" * 64},
        ]
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    facts = collect_diagnosis(workspace, "run-wide-replay")["facts"]

    assert facts["current_version"]["version"] == "v002"
    run_wide = facts["run_wide"]
    assert run_wide["scientific_versions"]["version_count"] == 2
    assert run_wide["experiments"]["scratch"]["report_count"] == 2
    assert run_wide["experiments"]["recorded"]["attempt_count"] == 0
    assert run_wide["experiments"]["formal_review_support"]["attempt_count"] == 0
    assert run_wide["hypotheses"]["status_distribution"] == {
        "falsified": 1,
        "prior_collision": 1,
    }
    assert run_wide["searches"]["search_count"] == 1
    assert run_wide["searches"]["searches"][0]["query_count"] == 1
    assert run_wide["searches"]["raw_result_bytes"] > 0
    assert run_wide["searches"]["searches"][0]["deduplicated_paper_count"] == 7
    assert run_wide["subagents"]["summary_artifact_count"] == 1
    assert run_wide["subagents"]["summary_count"] == 1
    assert run_wide["subagents"]["summary_artifacts"][0]["path"] == (
        "research_workspace/subagents/prior_attack.md"
    )
    assert run_wide["subagents"]["native_delegation_evidence"] == {
        "status": "UNAVAILABLE",
        "verified_delegation_count": None,
        "reason": "no_stable_machine_verifiable_native_delegation_evidence_source",
        "summary_artifacts_verify_native_delegation": False,
    }
    composition = run_wide["recall_composition"]
    assert composition["external_or_vendor_indexed_count"] == 2
    assert composition["ground_truth_like_indexed_count"] == 1
    assert composition["raw_search_payload_indexed_count"] == 1
    assert composition["contamination_present"] is True
    assert facts["non_judgments"]


def test_diagnosis_reports_five_tail_pre_experiment_closures(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    _write_closed_hypotheses(workspace, ["prior_collision"] * 5)

    facts = collect_diagnosis(workspace, "five-pre-experiment")["facts"]
    hypotheses = facts["run_wide"]["hypotheses"]

    assert hypotheses["pre_experiment_closure_history_status"] == "READY"
    assert hypotheses["pre_experiment_closure_streak"] == 5
    assert hypotheses["prior_collision_pre_experiment_closure_streak"] == 5
    assert hypotheses["pre_experiment_closure_significant_warning"] is True
    latest = facts["run_wide"]["latest_structured_activity"]
    assert latest["structured_candidate"] == {
        "latest_version": "v001",
        "versions_since": 0,
    }
    assert latest["recorded"]["latest_version"] == "UNAVAILABLE"


def test_diagnosis_does_not_count_candidate_with_bound_spec_as_pre_experiment(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    _write_closed_hypotheses(workspace, ["prior_collision"] * 5)
    spec_path = prepare_experiment_spec(
        product, run, experiment_id="bound-candidate"
    )
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["hypothesis_id"] = "h-005"
    spec_path.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    hypotheses = collect_diagnosis(workspace, "bound-candidate")["facts"][
        "run_wide"
    ]["hypotheses"]

    assert hypotheses["pre_experiment_closure_streak"] == 0
    h5 = next(
        item
        for item in hypotheses["raw_candidate_observations"]
        if item["hypothesis_id"] == "h-005"
    )
    assert h5["experiment_binding"]["has_experiment_spec"] is True


def test_diagnosis_reports_schema_1_closure_history_as_unknown(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    portfolio = empty_portfolio(run.name, "v001", now="2026-08-18T00:00:00Z")
    portfolio = add_hypothesis(
        portfolio,
        create_hypothesis_record(
            _diagnosis_hypothesis_payload("legacy-001"),
            now="2026-08-18T00:00:01Z",
        ),
        now="2026-08-18T00:00:02Z",
    )
    mapping = portfolio_to_dict(portfolio)
    mapping["schema_version"] = 1
    mapping["hypotheses"][0].pop("decision_history")
    mapping["hypotheses"][0]["status"] = "prior_collision"
    mapping["hypotheses"][0]["status_reason"] = "旧模式没有决策时间线"
    workspace.hypotheses_path.parent.mkdir()
    workspace.hypotheses_path.write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    hypotheses = collect_diagnosis(workspace, "legacy-history")["facts"][
        "run_wide"
    ]["hypotheses"]

    assert hypotheses["pre_experiment_closure_history_status"] == "UNKNOWN"
    assert hypotheses["pre_experiment_closure_streak"] == "UNKNOWN"
    assert hypotheses["ordered_decision_events"] == []
    assert "schema_version_1_decision_history_unavailable" in hypotheses[
        "pre_experiment_closure_unknown_reasons"
    ]


def test_diagnosis_reports_schema_1_active_history_as_unknown(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    portfolio = empty_portfolio(run.name, "v001", now="2026-08-18T00:00:00Z")
    portfolio = add_hypothesis(
        portfolio,
        create_hypothesis_record(
            _diagnosis_hypothesis_payload("legacy-active"),
            now="2026-08-18T00:00:01Z",
        ),
        now="2026-08-18T00:00:02Z",
    )
    mapping = portfolio_to_dict(portfolio)
    mapping["schema_version"] = 1
    mapping["hypotheses"][0].pop("decision_history")
    mapping["hypotheses"][0]["status"] = "active"
    mapping["hypotheses"][0]["status_reason"] = "旧模式当前活动"
    workspace.hypotheses_path.parent.mkdir()
    workspace.hypotheses_path.write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    hypotheses = collect_diagnosis(workspace, "legacy-active")["facts"][
        "run_wide"
    ]["hypotheses"]

    assert hypotheses["pre_experiment_closure_streak"] == "UNKNOWN"
    assert "schema_version_1_decision_history_unavailable" in hypotheses[
        "pre_experiment_closure_unknown_reasons"
    ]


def test_diagnosis_invalid_portfolio_does_not_fabricate_history(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.hypotheses_path.parent.mkdir()
    workspace.hypotheses_path.write_text(
        "{not-json}\n", encoding="utf-8", newline="\n"
    )

    hypotheses = collect_diagnosis(workspace, "invalid-portfolio")["facts"][
        "run_wide"
    ]["hypotheses"]

    assert hypotheses["pre_experiment_closure_streak"] == "UNKNOWN"
    assert hypotheses["ordered_decision_events"] == []
    assert hypotheses["unparseable_portfolio_count"] == 1


def test_diagnosis_experiment_binding_and_decisions_are_run_wide_by_hypothesis_id(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace_v1 = ResearchWorkspace(run, product_root=product, version="v001")
    _write_closed_hypotheses(workspace_v1, ["prior_collision"])
    spec_path = prepare_experiment_spec(product, run, experiment_id="v1-bound")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["hypothesis_id"] = "h-001"
    spec_path.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    set_current_version(run, "v002")
    workspace_v2 = ResearchWorkspace(run, product_root=product, version="v002")
    _write_closed_hypotheses(workspace_v2, ["prior_collision"] * 5)

    hypotheses = collect_diagnosis(workspace_v2, "version-scoped-binding")[
        "facts"
    ]["run_wide"]["hypotheses"]

    assert hypotheses["pre_experiment_closure_streak"] == 4
    assert hypotheses["unique_ordered_decision_event_count"] == 10
    observations = {
        (item["version"], item["hypothesis_id"]): item["experiment_binding"]
        for item in hypotheses["raw_candidate_observations"]
    }
    assert observations[("v001", "h-001")]["any_bound"] is True
    assert observations[("v002", "h-001")]["any_bound"] is True


def test_diagnosis_sorts_fractional_utc_decision_times_chronologically(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    portfolio = empty_portfolio(run.name, "v001", now="2026-08-18T00:00:00Z")
    for index in (1, 2):
        portfolio = add_hypothesis(
            portfolio,
            create_hypothesis_record(
                _diagnosis_hypothesis_payload(f"time-{index}"),
                now=f"2026-08-18T00:00:0{index}Z",
            ),
            now=f"2026-08-18T00:00:1{index}Z",
        )
        portfolio = transition_hypothesis(
            portfolio,
            f"time-{index}",
            "active",
            "进入验证",
            now=f"2026-08-18T01:00:0{index}Z",
        )
    portfolio = transition_hypothesis(
        portfolio,
        "time-1",
        "prior_collision",
        "较早关闭",
        decision=_diagnosis_decision(),
        now="2026-08-18T02:00:00Z",
    )
    portfolio = transition_hypothesis(
        portfolio,
        "time-2",
        "escalated",
        "较晚但不是实验前关闭",
        decision=_diagnosis_decision(),
        now="2026-08-18T02:00:00.500000Z",
    )
    workspace.write_hypotheses(
        portfolio, expected_sha256=None, create_only=True
    )

    hypotheses = collect_diagnosis(workspace, "fractional-time")["facts"][
        "run_wide"
    ]["hypotheses"]

    assert hypotheses["ordered_decision_events"][-1]["hypothesis_id"] == "time-2"
    assert hypotheses["pre_experiment_closure_streak"] == 0


def test_diagnosis_reads_six_selection_context_sections_and_tied_best_set(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        """## 当前最佳候选集合

h-001 与 h-002 并列，分别覆盖方法与评价贡献。

## 新增正向证据

实现与筛选实验均已记录。

## 已失效或被杀范围

只杀死旧实现。

## 剩余致命不确定性

强基线公平性。

## 下一项最高信息量动作

运行匹配预算的强基线。

## 策略变化

由方法优先转为现象优先。
"""
    )

    selection = collect_diagnosis(workspace, "selection-template")["facts"][
        "current_version"
    ]["selection_context"]

    assert selection["status"] == "READY"
    assert "h-001 与 h-002" in selection["sections"]["best_candidate_set"]["text"]
    assert all(
        item["status"] == "PRESENT" for item in selection["sections"].values()
    )


def test_diagnosis_selection_context_missing_degrades_to_unavailable(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)

    selection = collect_diagnosis(workspace, "selection-missing")["facts"][
        "current_version"
    ]["selection_context"]

    assert selection["status"] == "UNAVAILABLE"
    assert all(
        item["status"] == "UNAVAILABLE"
        for item in selection["sections"].values()
    )


def test_diagnosis_ignores_template_headings_inside_fenced_code(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        """## 当前最佳候选集合

REAL BEST

## 新增正向证据

REAL EVIDENCE

## 已失效或被杀范围

REAL KILL

## 剩余致命不确定性

REAL UNCERTAINTY

## 下一项最高信息量动作

REAL ACTION

## 策略变化

REAL STRATEGY

```markdown
## 当前最佳候选集合

EXAMPLE ONLY
```
"""
    )

    selection = collect_diagnosis(workspace, "selection-fence")["facts"][
        "current_version"
    ]["selection_context"]

    assert selection["status"] == "READY"
    assert selection["sections"]["best_candidate_set"]["text"] == "REAL BEST"


def test_diagnosis_duplicate_real_selection_heading_is_unavailable(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        """## 当前最佳候选集合

FIRST

## 当前最佳候选集合

SECOND
"""
    )

    selection = collect_diagnosis(workspace, "selection-duplicate")["facts"][
        "current_version"
    ]["selection_context"]

    assert selection["status"] == "PARTIAL"
    assert selection["reason"] == "duplicate_template_sections"
    assert selection["sections"]["best_candidate_set"]["status"] == "UNAVAILABLE"
    assert "best_candidate_set" in selection["duplicate_sections"]


def test_diagnosis_does_not_treat_markdown_summary_as_native_delegation(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    summary = run / "research_workspace" / "subagents" / "benchmark_scout.md"
    summary.parent.mkdir(parents=True)
    summary.write_text("saved summary only\n", encoding="utf-8", newline="\n")

    result = collect_diagnosis(workspace, "subagent-artifact-only")
    subagents = result["facts"]["run_wide"]["subagents"]
    report = (Path(result["path"]) / "report.md").read_text(encoding="utf-8")

    assert subagents["summary_artifact_count"] == 1
    assert subagents["summary_count"] == 1
    assert subagents["category_distribution"] == {"prior_or_falsification": 1}
    assert subagents["classification_basis"] == (
        "filename_only_artifact_classification_no_native_delegation_verification"
    )
    assert subagents["native_delegation_evidence"]["status"] == "UNAVAILABLE"
    assert subagents["native_delegation_evidence"]["verified_delegation_count"] is None
    assert (
        subagents["native_delegation_evidence"][
            "summary_artifacts_verify_native_delegation"
        ]
        is False
    )
    assert "Run-local subagent-related Markdown summary artifacts: 1" in report
    assert "Native delegation evidence: UNAVAILABLE" in report
    assert "Verified native delegation count: UNKNOWN" in report
    assert "Saved Research Subagent summaries" not in report


def test_diagnosis_reports_missing_fts_recall_as_structured_unavailable(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)

    result = collect_diagnosis(workspace, "without-recall")

    status = result["facts"]["recall_status"]
    assert status == {
        "status": "UNAVAILABLE",
        "reason": "fts_index_missing_or_unreadable",
        "semantic_status": None,
        "semantic_reason": None,
    }
    assert result["facts"]["recall_resume"] is None


def test_tool_forge_stays_run_local_and_writes_atomic_outputs(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    created = create_run_tool(workspace, "log-audit")
    context = RunToolContext(workspace, "log-audit")

    output = context.write_json("facts.json", {"count": 2})

    assert Path(created["path"]).is_relative_to(run)
    assert json.loads(output.read_text(encoding="utf-8")) == {"count": 2}
    with pytest.raises(ValueError, match="safe and relative"):
        context.output_path("../escape.json")


def test_recorded_captures_success_redacts_and_never_supports_delivery(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.implementation_path.mkdir()
    (workspace.implementation_path / "method.py").write_text(
        "print('method')\n", encoding="utf-8", newline="\n"
    )
    output = workspace.workbench_path / "recorded-output.txt"
    workspace.workbench_path.mkdir()
    secret = "recorded-secret-value"
    monkeypatch.setenv("CRL_CAPTURE_TOKEN", secret)
    monkeypatch.setenv("CRL_RECORDED_NORMAL_ENV", "ordinary-recorded-value")
    auxiliary_environments: list[dict[str, str]] = []

    def git_facts(
        _root: Path, *, environment: dict[str, str] | None = None
    ) -> dict[str, object]:
        assert environment is not None
        auxiliary_environments.append(environment)
        return {"status": "unavailable", "commit": None}

    monkeypatch.setattr(recorded_module, "_git_facts", git_facts)
    command = [
        sys.executable,
        "-c",
        "from pathlib import Path; import os,sys; Path(sys.argv[1]).write_text('ok'); print(os.environ['CRL_CAPTURE_TOKEN'])",
        str(output),
    ]

    record = run_recorded(
        workspace,
        "quick-check",
        command,
        outputs=[output],
        allow_sensitive_environment=["CRL_CAPTURE_TOKEN"],
    )

    capture = workspace.experiment_path / "recorded" / "quick-check"
    assert record["status"] == "SUCCESS"
    assert record["tier"] == "RECORDED_NON_SUPPORTING"
    assert secret.encode("utf-8") not in (capture / "stdout.bin").read_bytes()
    assert b"[REDACTED]" in (capture / "stdout.bin").read_bytes()
    assert record["capture"]["redaction_applied"] is True
    assert record["environment"]["sensitive_environment_passthrough"] == [
        "CRL_CAPTURE_TOKEN"
    ]
    assert len(auxiliary_environments) == 1
    assert "CRL_CAPTURE_TOKEN" not in auxiliary_environments[0]
    assert (
        auxiliary_environments[0]["CRL_RECORDED_NORMAL_ENV"]
        == "ordinary-recorded-value"
    )
    assert all(
        secret.encode("utf-8") not in path.read_bytes()
        for path in capture.iterdir()
        if path.is_file()
    )
    assert valid_supporting_attempt_ids(workspace) == ()


def test_recorded_child_withholds_ambient_secret_but_keeps_normal_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.workbench_path.mkdir()
    output = workspace.workbench_path / "environment.json"
    monkeypatch.setenv("CRL_RECORDED_API_KEY", "recorded-ambient-secret-123456789")
    monkeypatch.setenv("CRL_RECORDED_NORMAL_ENV", "ordinary-recorded-value")
    script = (
        "from pathlib import Path; import json,os,sys; "
        "Path(sys.argv[1]).write_text(json.dumps({"
        "'secret_visible': 'CRL_RECORDED_API_KEY' in os.environ, "
        "'normal': os.environ['CRL_RECORDED_NORMAL_ENV'], "
        "'python_exists': os.path.isfile(sys.executable)}), encoding='utf-8')"
    )

    record = run_recorded(
        workspace,
        "sanitized-environment",
        [sys.executable, "-c", script, str(output)],
        outputs=[output],
    )

    assert record["status"] == "SUCCESS"
    assert json.loads(output.read_text(encoding="utf-8")) == {
        "secret_visible": False,
        "normal": "ordinary-recorded-value",
        "python_exists": True,
    }
    assert record["environment"]["sensitive_environment_passthrough"] == []


def test_recorded_timeout_is_preserved(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)

    record = run_recorded(
        workspace,
        "timeout-check",
        [sys.executable, "-c", "import time; time.sleep(2)"],
        timeout_seconds=0.1,
    )

    assert record["status"] == "TIMEOUT"
    assert record["timed_out"] is True
    assert (workspace.experiment_path / "recorded" / "timeout-check" / "record.json").is_file()


def test_thin_cli_exposes_optional_capabilities_without_workflow_gate(capsys) -> None:
    assert main(["capabilities"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["contract_version"] == "3"
    assert payload["required"] == []
    assert payload["workflow_gate"] is False


def test_cli_discovers_run_product_and_current_version_from_nested_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    _, run = make_run(tmp_path)
    set_current_version(run, "v002")
    nested = run / "workbench_v002" / "notes"
    nested.mkdir(parents=True)
    (run / "selection_context_v002.md").write_text(
        "Current version context.\n", encoding="utf-8", newline="\n"
    )
    monkeypatch.chdir(nested)

    assert main(["recall", "rebuild"]) == 0
    capsys.readouterr()
    assert main(["recall", "resume"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["run_id"] == run.name
    assert payload["version"] == "v002"


def test_review_decision_body_must_be_a_run_local_safe_file(
    tmp_path: Path, capsys
) -> None:
    product, run = make_run(tmp_path)
    outside = tmp_path / "outside-decision.md"
    outside.write_text("do not read across the Run boundary\n", encoding="utf-8", newline="\n")

    exit_code = main(
        [
            "review",
            "decide",
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--version",
            "v001",
            "--body-file",
            str(outside),
        ]
    )

    assert exit_code == 2
    assert "escapes Run root" in capsys.readouterr().err
