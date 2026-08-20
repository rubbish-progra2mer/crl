from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from evaluation.research_discovery import (
    SYSTEM_TYPES,
    build_evaluation_report,
    build_visible_task_packet,
    canonical_sha256,
    import_system_output,
    load_annotation_batch,
    load_task_manifest,
    render_markdown_report,
    validate_system_output,
    write_report_files,
)
from evaluation.research_discovery.core import validate_annotation_batch, validate_task_manifest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = PROJECT_ROOT / "evaluation" / "research_discovery" / "fixtures" / "synthetic"
MANIFEST_PATH = FIXTURE / "task_manifest.json"
FORMAT_FILES = {
    "bare_llm": "bare_llm.json",
    "passage_rag": "passage_rag.json",
    "card_only": "card_only.json",
    "current_crl": "current_crl.json",
    "crl_scientific_search": "crl_scientific_search.json",
}


def _manifest() -> dict[str, object]:
    return load_task_manifest(MANIFEST_PATH)


def _outputs(manifest: dict[str, object]) -> list[dict[str, object]]:
    return [
        import_system_output(FIXTURE / filename, source_format, manifest)
        for source_format, filename in FORMAT_FILES.items()
    ]


def _annotations(manifest: dict[str, object]) -> list[dict[str, object]]:
    return [
        load_annotation_batch(FIXTURE / "expert_annotations.json", manifest),
        load_annotation_batch(FIXTURE / "llm_auxiliary_annotations.json", manifest),
    ]


def _system(report: dict[str, object], system_id: str) -> dict[str, object]:
    return next(item for item in report["systems"] if item["system_id"] == system_id)


def test_synthetic_fixture_is_explicit_and_all_five_offline_adapters_import() -> None:
    manifest = _manifest()
    assert manifest["synthetic_fixture"] is True
    assert "不代表真实科研能力" in manifest["synthetic_notice"]
    outputs = _outputs(manifest)
    assert {item["system_type"] for item in outputs} == set(SYSTEM_TYPES)
    assert all(len(item["provenance"]["imported_from_sha256"]) == 64 for item in outputs)
    assert all(item["candidate_payload_sha256"] == canonical_sha256(item["candidates"]) for item in outputs)


def test_year_cutoff_never_infers_same_year_order_and_packet_excludes_heldout() -> None:
    manifest = _manifest()
    packet = build_visible_task_packet(manifest)
    visibility = packet["temporal_visibility"]
    assert visibility["visible_paper_ids"] == ["syn-visible-2019", "syn-visible-2020"]
    assert visibility["year_precision_ambiguity"]["paper_ids"] == ["syn-ambiguous-2020"]
    encoded = json.dumps(packet, ensure_ascii=False, sort_keys=True)
    assert "syn-heldout-2020" not in encoded


def test_cutoff_and_heldout_leakage_are_rejected() -> None:
    manifest = _manifest()
    output = import_system_output(FIXTURE / "passage_rag.json", "passage_rag", manifest)
    leaked = copy.deepcopy(output)
    leaked.pop("_source_path")
    leaked["input_trace"]["paper_ids"] = ["syn-heldout-2020"]
    with pytest.raises(ValueError, match="non-visible|held-out"):
        validate_system_output(leaked, manifest)

    unknown_artifact = copy.deepcopy(output)
    unknown_artifact.pop("_source_path")
    unknown_artifact["input_trace"]["artifact_ids"] = ["undeclared-heldout-artifact"]
    with pytest.raises(ValueError, match="non-visible artifact"):
        validate_system_output(unknown_artifact, manifest)

    wrong_packet = copy.deepcopy(output)
    wrong_packet.pop("_source_path")
    wrong_packet["input_trace"]["task_packet_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="does not match visible task packet"):
        validate_system_output(wrong_packet, manifest)

    invalid_manifest = copy.deepcopy({key: value for key, value in manifest.items() if not key.startswith("_")})
    invalid_manifest["temporal_visibility"]["visible_paper_ids"].append("syn-heldout-2020")
    with pytest.raises(ValueError, match="overlap"):
        validate_task_manifest(invalid_manifest)


def test_configuration_mismatch_is_not_silently_accepted() -> None:
    manifest = _manifest()
    output = import_system_output(FIXTURE / "bare_llm.json", "bare_llm", manifest)
    changed = copy.deepcopy(output)
    changed.pop("_source_path")
    changed["system_configuration"]["temperature"] = 1
    changed["configuration_sha256"] = canonical_sha256(changed["system_configuration"])
    with pytest.raises(ValueError, match="does not match TaskManifest profile"):
        validate_system_output(changed, manifest)


def test_collision_rate_uses_only_audited_candidates() -> None:
    manifest = _manifest()
    output = import_system_output(FIXTURE / "bare_llm.json", "bare_llm", manifest)
    mixed = copy.deepcopy(output)
    mixed.pop("_source_path")
    mixed["candidates"][1]["visible_prior_audit"] = {
        "performed": True,
        "audited_visible_paper_ids": ["syn-visible-2019"],
        "collision_visible_paper_ids": ["syn-visible-2019"],
    }
    mixed["candidate_payload_sha256"] = canonical_sha256(mixed["candidates"])
    report = build_evaluation_report(manifest, [mixed])
    exploration = report["systems"][0]["axes"]["exploration"]
    collision = exploration["visible_prior_collision_rate"]
    coverage = exploration["nearest_prior_audit_coverage"]
    assert collision["value"] == 1.0
    assert collision["numerator"] == 1
    assert collision["denominator"] == 1
    assert collision["eligible_count"] == 1
    assert collision["population_count"] == 2
    assert collision["sampling_unit"] == "audited_candidate"
    assert coverage["value"] == 0.5
    assert coverage["denominator"] == 2


def test_all_unaudited_candidates_make_collision_rate_unknown() -> None:
    manifest = _manifest()
    output = import_system_output(FIXTURE / "bare_llm.json", "bare_llm", manifest)
    report = build_evaluation_report(manifest, [output])
    collision = report["systems"][0]["axes"]["exploration"]["visible_prior_collision_rate"]
    assert collision["value"] is None
    assert collision["denominator"] == 0
    assert collision["eligible_count"] == 0
    assert collision["population_count"] == 2


def test_missing_structure_is_not_counted_as_a_duplicate() -> None:
    manifest = _manifest()
    output = import_system_output(FIXTURE / "bare_llm.json", "bare_llm", manifest)
    partial = copy.deepcopy(output)
    partial.pop("_source_path")
    partial["candidates"][1]["descriptors"]["problem_family"] = ""
    partial["candidate_payload_sha256"] = canonical_sha256(partial["candidates"])
    report = build_evaluation_report(manifest, [partial])
    duplicate = report["systems"][0]["axes"]["diversity"]["structure_duplicate_rate"]
    assert duplicate["value"] is None
    assert duplicate["denominator"] == 0
    assert duplicate["eligible_count"] == 0
    assert duplicate["population_count"] == 1


def test_all_observable_metrics_are_decomposed_without_aggregate_score() -> None:
    manifest = _manifest()
    report = build_evaluation_report(
        manifest,
        _outputs(manifest),
        _annotations(manifest),
        bootstrap_replicates=30,
        random_seed=7,
    )
    bare = _system(report, "syn-bare")
    card = _system(report, "syn-card")
    passage = _system(report, "syn-passage")
    current = _system(report, "syn-current")
    search = _system(report, "syn-search")

    assert bare["axes"]["diversity"]["structure_duplicate_rate"]["value"] == 1.0
    assert bare["axes"]["falsifiability"]["changed_computation_completeness"]["value"] == 0.0
    assert card["axes"]["exploration"]["visible_prior_collision_rate"]["value"] == 1.0
    assert passage["axes"]["implementation"]["early_kill_efficiency"]["value"] == 1.0
    assert current["axes"]["implementation"]["implementation_conversion_rate"]["value"] == 1.0
    assert current["axes"]["empirical_survival"]["under_matched_strong_baselines"]["value"] == 1.0
    assert current["axes"]["empirical_survival"]["cost_per_surviving_hypothesis"]["values"]["tokens"] == 500
    assert search["axes"]["empirical_survival"]["under_matched_strong_baselines"]["value"] is None
    def keys(value: object) -> set[str]:
        if isinstance(value, dict):
            return set(value) | set().union(*(keys(item) for item in value.values()))
        if isinstance(value, list):
            return set().union(*(keys(item) for item in value))
        return set()

    report_keys = keys(report)
    for forbidden in ("total_score", "quality_score", "winner_system_id", "ranking"):
        assert forbidden not in report_keys


def test_missing_cost_is_disclosed_and_never_coerced_to_zero() -> None:
    manifest = _manifest()
    output = import_system_output(FIXTURE / "bare_llm.json", "bare_llm", manifest)
    report = build_evaluation_report(manifest, [output])
    cost = report["systems"][0]["axes"]["empirical_survival"]["cost_per_surviving_hypothesis"]
    assert cost["missing_cost"] is True
    assert all(value is None for value in cost["values"].values())


def test_blinded_expert_is_primary_and_llm_judge_remains_auxiliary() -> None:
    manifest = _manifest()
    expert, llm = _annotations(manifest)
    report = build_evaluation_report(
        manifest,
        [import_system_output(FIXTURE / "bare_llm.json", "bare_llm", manifest)],
        [expert, llm],
    )
    assessment = report["systems"][0]["expert_blind_assessment"]
    assert assessment["novelty"]["value"] == 2.0
    assert assessment["llm_judge_auxiliary_annotation_count"] == 1
    assert assessment["llm_judge_policy"].startswith("auxiliary_only")

    unblinded = copy.deepcopy({key: value for key, value in expert.items() if not key.startswith("_")})
    unblinded["blinding"]["system_identity_hidden"] = False
    with pytest.raises(ValueError, match="blinding guarantees"):
        validate_annotation_batch(unblinded, manifest)


def test_heldout_mechanism_rediscovery_is_separate_from_text_similarity() -> None:
    manifest = _manifest()
    current = import_system_output(FIXTURE / "current_crl.json", "current_crl", manifest)
    report = build_evaluation_report(manifest, [current], [_annotations(manifest)[0]])
    heldout = report["systems"][0]["heldout_evaluation"]
    assert heldout["mechanism_rediscovery"]["value"] == 1.0
    assert heldout["simple_text_similarity"]["value"] == 0.2
    assert "separately" in heldout["separation_note"]


def test_bootstrap_discloses_distinct_sampling_units() -> None:
    manifest = _manifest()
    report = build_evaluation_report(
        manifest,
        _outputs(manifest),
        _annotations(manifest),
        bootstrap_replicates=20,
        random_seed=9,
    )
    bare = _system(report, "syn-bare")
    pair_metric = bare["axes"]["diversity"]["structure_duplicate_rate"]
    candidate_metric = bare["axes"]["diversity"]["descriptor_coverage"]
    expert_metric = bare["expert_blind_assessment"]["novelty"]
    assert (
        pair_metric["confidence_interval"]["sampling_unit"]
        == "fully_described_candidate_pair"
    )
    assert candidate_metric["confidence_interval"]["sampling_unit"] == "candidate"
    assert expert_metric["confidence_interval"]["sampling_unit"] == "blinded_expert_annotation"


def test_empty_output_is_a_valid_observable_fact(tmp_path: Path) -> None:
    manifest = _manifest()
    raw = json.loads((FIXTURE / "bare_llm.json").read_text(encoding="utf-8"))
    raw["responses"] = []
    source = tmp_path / "empty.json"
    source.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    output = import_system_output(source, "bare_llm", manifest)
    report = build_evaluation_report(manifest, [output])
    system = report["systems"][0]
    assert system["candidate_count"] == 0
    assert system["axes"]["exploration"]["visible_prior_collision_rate"]["denominator"] == 0
    assert system["axes"]["exploration"]["visible_prior_collision_rate"]["value"] is None


def test_report_is_deterministic_and_saved_without_overwrite(tmp_path: Path) -> None:
    manifest = _manifest()
    kwargs = dict(
        manifest=manifest,
        system_outputs=_outputs(manifest),
        annotation_batches=_annotations(manifest),
        bootstrap_replicates=25,
        confidence_level=0.9,
        random_seed=23,
    )
    first = build_evaluation_report(**kwargs)
    second = build_evaluation_report(**kwargs)
    assert first == second
    assert render_markdown_report(first) == render_markdown_report(second)
    json_path = tmp_path / "report.json"
    markdown_path = tmp_path / "report.md"
    write_report_files(first, json_path, markdown_path)
    assert json_path.read_bytes().startswith(b"{\n")
    assert b"\r" not in markdown_path.read_bytes()
    with pytest.raises(FileExistsError):
        write_report_files(first, json_path, markdown_path)


def test_cli_runs_offline_and_emits_decomposed_report(tmp_path: Path) -> None:
    report_json = tmp_path / "report.json"
    report_markdown = tmp_path / "report.md"
    completed = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "tools" / "evaluate_research_discovery.py"),
            "--manifest",
            str(MANIFEST_PATH),
            "--system-output",
            "bare_llm",
            str(FIXTURE / "bare_llm.json"),
            "--system-output",
            "current_crl",
            str(FIXTURE / "current_crl.json"),
            "--annotation",
            str(FIXTURE / "expert_annotations.json"),
            "--report-json",
            str(report_json),
            "--report-markdown",
            str(report_markdown),
            "--stdout-format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    payload = json.loads(report_json.read_text(encoding="utf-8"))
    assert [item["system_id"] for item in payload["systems"]] == ["syn-bare", "syn-current"]
    assert "总分、排名或冠军" in report_markdown.read_text(encoding="utf-8")


def test_cli_help_is_strict_utf8_with_correct_chinese() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "tools" / "evaluate_research_discovery.py"),
            "--help",
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8")
    help_text = completed.stdout.decode("utf-8", errors="strict")
    assert "离线导入五类研究系统输出" in help_text
    assert "不会调用模型、网络或生产知识库" in help_text


def test_cli_synthetic_markdown_stdout_is_strict_utf8() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "tools" / "evaluate_research_discovery.py"),
            "--manifest",
            str(MANIFEST_PATH),
            "--system-output",
            "bare_llm",
            str(FIXTURE / "bare_llm.json"),
            "--stdout-format",
            "markdown",
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8")
    markdown = completed.stdout.decode("utf-8", errors="strict")
    assert markdown.startswith("# CRL 时间截断研究发现评测")
    assert "完全合成夹具，仅验证评测框架；不代表真实科研能力。" in markdown
    assert "可见先行碰撞率" in markdown


def test_schema_documents_are_valid_json_and_readme_states_limits() -> None:
    schema_dir = PROJECT_ROOT / "evaluation" / "research_discovery" / "schema"
    for path in sorted(schema_dir.glob("*.schema.json")):
        assert json.loads(path.read_text(encoding="utf-8"))["$schema"].endswith("2020-12/schema")
    readme = (PROJECT_ROOT / "evaluation" / "research_discovery" / "README.md").read_text(encoding="utf-8")
    assert "不代表真实科研能力" in readme
    assert "不调用在线模型" in readme
    assert "不访问或写入生产知识库" in readme
