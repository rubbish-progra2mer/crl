from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

import crl_v3.research_retrieval as research_retrieval_module
import tools.query_research as query_research_module
from conftest import make_directory_reparse_point, make_run
from crl_v3.cards import card_source_signature, rebuild_card_index
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
)
from crl_v3.knowledge import KnowledgeStore, Paper, Passage
from crl_v3.research_retrieval import ResearchQuery, build_research_bundle
from crl_v3.workspace import ResearchWorkspace


TOOL = Path(__file__).resolve().parents[1] / "tools" / "query_research.py"

_HEADINGS = {
    "failure": (
        "Observed failure",
        "Conditions and scope",
        "Failed intervention",
        "Evidence and alternative explanations",
        "Warning for future candidates",
        "Possible repair boundary",
        "Evidence ledger",
        "Retrieval vocabulary",
    ),
    "operator": (
        "Intervention target",
        "Before and after computation",
        "Inputs outputs information and timing",
        "Mechanism hypothesis",
        "Predicted observable signature",
        "Preconditions and transfer risks",
        "Source lineage",
        "Evidence ledger",
        "Retrieval vocabulary",
    ),
    "paper": (
        "Role in the knowledge base",
        "Problem and setting",
        "Changed computation",
        "Evidence-backed findings",
        "Limitations and failure signals",
        "Lineage and baselines",
        "Evidence ledger",
        "Retrieval vocabulary",
    ),
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _card_body(kind: str) -> str:
    sections = []
    for index, heading in enumerate(_HEADINGS[kind]):
        content = (
            "[AUTHOR_FACT] Coordination verifier evidence. [[evidence:evidence-a]]"
            if index == 0
            else "[CODEX_SYNTHESIS] Coordination verifier problem failure operator prior measurement."
        )
        sections.append(f"## {heading}\n\n{content}")
    return f"# {kind.title()} coordination card\n\n" + "\n\n".join(sections) + "\n"


def _write_card(root: Path, kind: str, pdf_sha: str) -> None:
    card_id = f"{kind}-coordination-card"
    path = root / "cards" / kind / f"{card_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "schema_version": 1,
        "card_id": card_id,
        "card_kind": kind,
        "paper_id": "paper-a",
        "evidence_ids": ["evidence-a"],
        "source_refs": [{"path": "papers/paper-a.pdf", "sha256": pdf_sha}],
    }
    path.write_text(
        "<!-- CRL_CARD_META "
        + json.dumps(metadata, sort_keys=True)
        + " -->\n"
        + _card_body(kind),
        encoding="utf-8",
        newline="\n",
    )


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path]:
    product, run = make_run(tmp_path)
    knowledge = product / "knowledge_base"
    papers = knowledge / "papers"
    papers.mkdir(parents=True)
    pdf = papers / "paper-a.pdf"
    pdf.write_bytes(b"authoritative fixture pdf")
    pdf_sha = _sha256(pdf.read_bytes())
    text = "Coordination verifier problem failure operator prior measurement passage."
    passage = Passage(
        passage_id="passage-a",
        paper_id="paper-a",
        section="Methods",
        page_start=3,
        page_end=3,
        char_start=0,
        char_end=len(text),
        text=text,
        text_sha256=_sha256(text.encode("utf-8")),
    )
    paper = Paper(
        paper_id="paper-a",
        title="Coordination Study",
        year=2025,
        source="fixture",
        venue="Fixture Venue",
        publication_status="preprint",
        fulltext_path="papers/paper-a.pdf",
        fulltext_sha256=pdf_sha,
    )
    store = KnowledgeStore(knowledge / "knowledge.sqlite", read_only=False)
    store.add_paper(paper, [passage])
    quote = "Coordination verifier"
    store.add_evidence(
        evidence_id="evidence-a",
        paper_id=paper.paper_id,
        fulltext_sha256=pdf_sha,
        evidence_kind="text",
        section="Methods",
        page_start=3,
        page_end=3,
        locator="page 3, paragraph 1",
        source_content=quote,
        codex_note="Fixture locator.",
        passage_id=passage.passage_id,
        passage_text_sha256=passage.text_sha256,
        quote_start=0,
        quote_end=len(quote),
    )
    for kind in ("failure", "operator", "paper"):
        _write_card(knowledge, kind, pdf_sha)
    rebuild_card_index(
        knowledge / "cards",
        knowledge / "cards_fts.sqlite",
        store=store,
        project_root=knowledge,
    )
    store.close()
    return product, run, knowledge


def _run(product: Path, run: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--version",
            "v001",
            *arguments,
        ],
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _explicit_arguments() -> tuple[str, ...]:
    values = []
    for purpose in ("problem", "failure", "operator", "prior", "measurement"):
        values.extend(("--query", f"{purpose}=coordination"))
    return tuple(values)


def test_explicit_queries_retain_routes_hashes_and_backtrack_without_portfolio(
    tmp_path: Path,
) -> None:
    product, run, _ = _fixture(tmp_path)
    portfolio = run / "hypotheses_v001" / "portfolio.json"

    completed = _run(product, run, *_explicit_arguments(), "--full-json")

    assert completed.returncode == 0, completed.stderr
    assert not portfolio.exists()
    payload = json.loads(completed.stdout)
    request = payload["request"]
    result = payload["result"]
    assert [query["purpose"] for query in request["queries"]] == [
        "problem",
        "failure",
        "operator",
        "prior",
        "measurement",
    ]
    routes = result["queries"][0]["routes"]
    assert [route["route"] for route in routes] == [
        "paper_card_fts",
        "failure_card_fts",
        "passage_hybrid",
        "operator_card_fts",
    ]
    for route in (routes[0], routes[1], routes[3]):
        hit = route["hits"][0]
        assert hit["rank"] == 1
        assert isinstance(hit["score"], float)
        assert hit["noise_flags"] == []
        assert hit["attention_weight_kind"].endswith("not_relevance")
        assert len(hit["card_markdown_sha256"]) == 64
        assert hit["source_refs"] == [
            {
                "path": "papers/paper-a.pdf",
                "sha256": hit["papers"][0]["fulltext_sha256"],
            }
        ]
        assert hit["evidence"][0]["evidence_id"] == "evidence-a"
        assert hit["evidence"][0]["passage_id"] == "passage-a"
        assert hit["papers"][0]["paper_id"] == "paper-a"
        assert hit["papers"][0]["fulltext_resolution_mode"] == "knowledge_relative"
    passage_route = routes[2]
    assert passage_route["degraded"] is True
    assert passage_route["degradation_reason"] == "index_missing"
    passage_hit = passage_route["hits"][0]
    assert passage_hit["passage_id"] == "passage-a"
    assert "route_degraded" in passage_hit["noise_flags"]
    assert "Coordination verifier" in passage_hit["text"]
    compact = result["compact_research_map"]
    assert result["report_format"] == "compact-v2"
    assert compact["deduplication_key"] == "paper_id"
    assert compact["ranking_kind"].endswith("not_relevance")
    assert compact["entry_count"] == 1
    assert compact["entries"][0]["paper_id"] == "paper-a"
    assert compact["entries"][0]["duplicate_observation_count"] > 0
    assert "route_degraded" in compact["entries"][0]["noise_flags"]
    assert compact["representative_entry_count"] == 1
    representative = compact["representative_entries"][0]
    assert representative["paper_id"] == "paper-a"
    assert representative["route"] == "paper_card_fts"
    assert representative["rank"] == 1
    assert representative["card_id"] == "paper-coordination-card"
    assert representative["evidence_ids"] == ["evidence-a"]
    diagnostics = result["diagnostics"]
    paper = next(item for item in diagnostics["paper_route_hits"] if item["paper_id"] == "paper-a")
    assert len(paper["routes"]) >= 4
    assert request["knowledge_identity"]["cards_fts_sqlite"]["card_source_signature"]
    assert (
        request["knowledge_identity"]["cards_fts_sqlite"]["card_source_signature"]
        == card_source_signature(product / "knowledge_base" / "cards")
    )
    assert len(request["code_identity"]["files"]) >= 6

    route_orders = {
        query["purpose"]: [route["route"] for route in query["routes"]]
        for query in result["queries"]
    }
    assert len({tuple(order) for order in route_orders.values()}) == 5
    assert result["queries"][0]["output_focus"]


def test_default_stdout_is_compact_without_route_hits_or_persistence(
    tmp_path: Path,
) -> None:
    product, run, _ = _fixture(tmp_path)

    completed = _run(product, run, *_explicit_arguments())

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["schema_version"] == 1
    assert payload["stdout_format"] == "compact-v1"
    assert "request" not in payload
    assert "result" not in payload
    assert [item["purpose"] for item in payload["query"]["queries"]] == [
        "problem",
        "failure",
        "operator",
        "prior",
        "measurement",
    ]
    compact = payload["representative_compact_map"]
    assert compact["entry_count"] == 1
    assert compact["representative_entry_count"] == 1
    assert compact["representative_entries"][0]["paper_id"] == "paper-a"
    assert payload["route_coverage"][0]["routes"][0]["hit_count"] == 1
    assert payload["coverage"]["observation_count"] == 20
    persistence = payload["persistence"]
    assert persistence["full_result_persisted"] is False
    assert persistence["status"] == "not_saved"
    assert persistence["snapshot"] is None
    assert persistence["artifact_paths"] == {}
    assert "未持久化" in persistence["message"]
    assert not (run / "hypotheses_v001" / "searches").exists()

    def contains_hits(value: object) -> bool:
        if isinstance(value, dict):
            return "hits" in value or any(contains_hits(item) for item in value.values())
        if isinstance(value, list):
            return any(contains_hits(item) for item in value)
        return False

    assert contains_hits(payload) is False


def test_full_json_preserves_legacy_complete_stdout(tmp_path: Path) -> None:
    product, run, _ = _fixture(tmp_path)

    completed = _run(
        product,
        run,
        "--query",
        "problem=coordination",
        "--full-json",
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert set(payload) == {"request", "result"}
    assert payload["request"]["input_mode"] == "explicit"
    routes = payload["result"]["queries"][0]["routes"]
    assert len(routes) == 4
    assert routes[0]["hits"][0]["card_id"] == "paper-coordination-card"
    assert routes[2]["hits"][0]["passage_id"] == "passage-a"


def test_cli_binds_knowledge_assets_before_constructing_store(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []

    def reject_binding(product_root: Path, knowledge_root: Path):
        events.append("bind")
        raise ValueError("injected unsafe knowledge root")

    def forbidden_store(*args, **kwargs):
        events.append("store")
        raise AssertionError("KnowledgeStore must not be constructed before binding")

    monkeypatch.setattr(
        query_research_module, "bind_research_knowledge_root", reject_binding
    )
    monkeypatch.setattr(query_research_module, "KnowledgeStore", forbidden_store)

    exit_code = query_research_module.main(
        [
            "--product-root",
            str(tmp_path / "product"),
            "--run-root",
            str(tmp_path / "product" / "20260810_1200_run01"),
            "--query",
            "problem=coordination",
        ]
    )

    assert exit_code == 2
    assert events == ["bind"]


def test_knowledge_identity_drift_during_query_rejects_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    product, _, knowledge = _fixture(tmp_path)
    store = KnowledgeStore(knowledge / "knowledge.sqlite", read_only=True)
    original = research_retrieval_module._execute_query

    def execute_then_change(*args, **kwargs):
        result = original(*args, **kwargs)
        card = knowledge / "cards" / "operator" / "operator-coordination-card.md"
        card.write_bytes(card.read_bytes() + b"\n")
        return result

    monkeypatch.setattr(
        research_retrieval_module, "_execute_query", execute_then_change
    )
    with pytest.raises(RuntimeError, match="identity changed"):
        build_research_bundle(
            product,
            knowledge,
            store,
            (ResearchQuery("problem", "coordination", "explicit_query"),),
            input_mode="explicit",
            input_identity={"run_id": "fixture", "version": "v001"},
        )
    store.close()


def test_stale_card_index_degrades_three_card_routes_but_keeps_passage_recall(
    tmp_path: Path,
) -> None:
    product, run, knowledge = _fixture(tmp_path)
    card = knowledge / "cards" / "failure" / "failure-coordination-card.md"
    card.write_text(
        card.read_text(encoding="utf-8") + "\n",
        encoding="utf-8",
        newline="\n",
    )

    completed = _run(product, run, "--query", "problem=coordination")

    assert completed.returncode == 0, completed.stderr
    routes = json.loads(completed.stdout)["route_coverage"][0]["routes"]
    card_routes = (routes[0], routes[1], routes[3])
    assert all(route["degraded"] is True for route in card_routes)
    assert all(
        route["degradation_reason"] == "card_sources_changed"
        for route in card_routes
    )
    assert routes[2]["hit_count"] == 1


def test_stale_evidence_rejects_authoritative_card_expansion(tmp_path: Path) -> None:
    product, run, knowledge = _fixture(tmp_path)
    store = KnowledgeStore(knowledge / "knowledge.sqlite", read_only=False)
    old = store.get_paper("paper-a")
    passage = store.get_passage("passage-a")
    assert old is not None and passage is not None
    store.add_paper(
        Paper(
            paper_id=old.paper_id,
            title=old.title,
            year=old.year,
            source=old.source,
            venue=old.venue,
            publication_status=old.publication_status,
            fulltext_path=old.fulltext_path,
            fulltext_sha256="f" * 64,
        ),
        [passage],
    )
    store.close()

    completed = _run(product, run, "--query", "problem=coordination")

    assert completed.returncode == 2
    assert "stale Evidence" in completed.stderr


def test_hypothesis_id_builds_bundle_without_modifying_portfolio(tmp_path: Path) -> None:
    product, run, knowledge = _fixture(tmp_path)
    store = KnowledgeStore(knowledge / "knowledge.sqlite", read_only=True)
    workspace = ResearchWorkspace(run, store, product_root=product, version="v001")
    portfolio = empty_portfolio(run.name, "v001", now="2026-08-10T00:00:00Z")
    record = create_hypothesis_record(
        {
            "hypothesis_id": "hypothesis-001",
            "title": "Coordination hypothesis",
            "parent_ids": [],
            "lineage_note": "Root hypothesis.",
            "problem": "coordination problem",
            "target_failure": {
                "summary": "coordination failure",
                "card_ids": ["failure-coordination-card"],
                "evidence_ids": ["evidence-a"],
            },
            "changed_computation": {
                "baseline": "coordination baseline",
                "intervention": "coordination operator",
                "information_available": "coordination information",
                "timing": "before execution",
                "budget_effect": "fixed",
            },
            "mechanism_claim": "coordination mechanism",
            "falsifier": "coordination measurement",
            "minimal_killer_experiment": "coordination experiment",
            "nearest_prior_risk": "coordination prior",
            "alternative_explanations": [],
            "descriptors": {
                "problem_family": "agents",
                "computation_stage": "planning",
                "intervention_family": "verification",
                "information_source": "trace",
                "timing_class": "pre-action",
                "budget_class": "fixed",
                "evaluation_mode": "counterexample",
            },
            "literature_refs": ["paper-a"],
        },
        now="2026-08-10T00:00:00Z",
    )
    portfolio = add_hypothesis(portfolio, record, knowledge_store=store)
    document = workspace.write_hypotheses(
        portfolio, expected_sha256=None, create_only=True
    )
    before = Path(document.path).read_bytes()
    store.close()

    completed = _run(product, run, "--hypothesis-id", "hypothesis-001")

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["query"]["input_mode"] == "hypothesis"
    assert payload["query"]["input_identity"]["portfolio_sha256"] == document.sha256
    assert Path(document.path).read_bytes() == before


def test_saved_search_is_three_file_atomic_and_reuses_original_utc_idempotently(
    tmp_path: Path,
) -> None:
    product, run, _ = _fixture(tmp_path)
    arguments = (*_explicit_arguments(), "--save-search", "search-001")

    first = _run(product, run, *arguments)
    assert first.returncode == 0, first.stderr
    destination = run / "hypotheses_v001" / "searches" / "search-001"
    before = {path.name: path.read_bytes() for path in destination.iterdir()}
    second = _run(product, run, *arguments)

    assert second.returncode == 0, second.stderr
    first_payload = json.loads(first.stdout)
    second_payload = json.loads(second.stdout)
    first_snapshot = first_payload["persistence"]["snapshot"]
    second_snapshot = second_payload["persistence"]["snapshot"]
    assert first_snapshot["idempotent"] is False
    assert second_snapshot["idempotent"] is True
    assert first_snapshot["created_at_utc"] == second_snapshot["created_at_utc"]
    assert first_payload["persistence"]["full_result_persisted"] is True
    assert first_payload["persistence"]["status"] == "saved_snapshot"
    assert set(first_payload["persistence"]["artifact_paths"]) == {
        "request.json",
        "result.json",
        "report.md",
    }
    assert {path.name: path.read_bytes() for path in destination.iterdir()} == before
    assert set(before) == {"request.json", "result.json", "report.md"}
    report = before["report.md"].decode("utf-8")
    result = json.loads(before["result.json"])
    assert "科研判断由主研究者完成" in report
    assert "紧凑研究地图" in report
    assert "跨路线按 Paper 去重" in report
    assert "完整原始命中保留在 `result.json`" in report
    assert "路线 `paper_card_fts`：1 条" in report
    assert "Card `paper-coordination-card`（paper）" in report
    assert "Evidence `evidence-a`" in report
    assert "路径 `cards/" not in report
    assert sum(
        len(route["hits"])
        for query in result["queries"]
        for route in query["routes"]
    ) == 20
    assert len(before["report.md"]) < len(before["result.json"]) // 10
    assert "最佳候选" not in report


def test_legacy_report_format_remains_canonical_for_existing_snapshots(
    tmp_path: Path,
) -> None:
    product, run, knowledge = _fixture(tmp_path)
    store = KnowledgeStore(knowledge / "knowledge.sqlite", read_only=True)
    bundle = build_research_bundle(
        product,
        knowledge,
        store,
        (ResearchQuery("problem", "coordination", "explicit_query"),),
        input_mode="explicit",
        input_identity={"run_id": run.name, "version": "v001"},
    )
    store.close()
    legacy = dict(bundle.result)
    legacy.pop("report_format")
    metadata = {
        "created_at_utc": "2026-08-10T00:00:00Z",
        "request_fingerprint_sha256": "a" * 64,
        "result_json_sha256": "b" * 64,
        "search_id": "legacy-001",
    }

    report = research_retrieval_module._render_report(legacy, metadata).decode(
        "utf-8"
    )

    assert "### 路线 `paper_card_fts`" in report
    assert "#1 Card `paper-coordination-card`；路径 `" in report
    assert "## 紧凑研究地图" in report


@pytest.mark.parametrize("file_name", ["request.json", "result.json", "report.md"])
def test_any_saved_file_tamper_is_rejected_without_overwrite(
    tmp_path: Path, file_name: str
) -> None:
    product, run, _ = _fixture(tmp_path)
    arguments = (
        "--query",
        "problem=coordination",
        "--save-search",
        "search-002",
    )
    assert _run(product, run, *arguments).returncode == 0
    path = run / "hypotheses_v001" / "searches" / "search-002" / file_name
    path.write_bytes(path.read_bytes() + b"\n")
    tampered = path.read_bytes()

    repeated = _run(product, run, *arguments)

    assert repeated.returncode == 2
    assert "snapshot" in repeated.stderr
    assert path.read_bytes() == tampered


@pytest.mark.parametrize("search_id", ["../escape", "UPPER", "a", "a/b"])
def test_illegal_search_id_is_rejected_without_writes(
    tmp_path: Path, search_id: str
) -> None:
    product, run, _ = _fixture(tmp_path)

    completed = _run(
        product,
        run,
        "--query",
        "problem=coordination",
        "--save-search",
        search_id,
    )

    assert completed.returncode == 2
    assert "SEARCH_ID" in completed.stderr
    assert not (run / "hypotheses_v001" / "searches").exists()


@pytest.mark.windows
def test_cards_directory_junction_to_external_assets_is_rejected(
    tmp_path: Path,
) -> None:
    product, run, knowledge = _fixture(tmp_path)
    outside = tmp_path / "outside-cards"
    (knowledge / "cards").rename(outside)
    make_directory_reparse_point(knowledge / "cards", outside)

    completed = _run(product, run, "--query", "problem=coordination")

    assert completed.returncode == 2
    assert "reparse point" in completed.stderr
