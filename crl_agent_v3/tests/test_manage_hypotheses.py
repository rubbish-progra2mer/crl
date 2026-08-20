from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from conftest import make_run


TOOL = Path(__file__).resolve().parents[1] / "tools" / "manage_hypotheses.py"


def _payload(hypothesis_id: str, *, complete: bool = False) -> dict[str, object]:
    text = "完整字段" if complete else ""
    return {
        "hypothesis_id": hypothesis_id,
        "title": text,
        "parent_ids": [],
        "lineage_note": "根候选",
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
        "alternative_explanations": [],
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


def _run(product: Path, run: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [
            sys.executable,
            str(TOOL),
            *arguments,
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--version",
            "v001",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_cli_init_add_update_transition_show_list_validate_and_render(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    created = _run(product, run, "init")
    assert created.returncode == 0, created.stderr.decode("utf-8")
    assert json.loads(created.stdout)["record_count"] == 0

    source = tmp_path / "hypothesis.json"
    source.write_text(
        json.dumps(_payload("h-001"), ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    added = _run(product, run, "add", "--from-json", str(source))
    assert added.returncode == 0, added.stderr.decode("utf-8")
    assert json.loads(added.stdout)["record_count"] == 1

    patch = _payload("ignored", complete=True)
    patch.pop("hypothesis_id")
    patch_path = tmp_path / "patch.json"
    patch_path.write_text(
        json.dumps(patch, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    updated = _run(
        product, run, "update", "h-001", "--patch-json", str(patch_path)
    )
    assert updated.returncode == 0, updated.stderr.decode("utf-8")

    transitioned = _run(
        product,
        run,
        "transition",
        "h-001",
        "--status",
        "active",
        "--reason",
        "主研究者显式采纳",
    )
    assert transitioned.returncode == 0, transitioned.stderr.decode("utf-8")
    assert json.loads(transitioned.stdout)["status"] == "active"

    shown = _run(product, run, "show", "h-001")
    assert shown.returncode == 0
    assert json.loads(shown.stdout)["hypothesis"]["status"] == "active"

    listed = _run(product, run, "list")
    assert listed.returncode == 0
    assert json.loads(listed.stdout)["hypotheses"][0]["hypothesis_id"] == "h-001"

    validated = _run(product, run, "validate")
    assert validated.returncode == 0
    facts = json.loads(validated.stdout)
    assert facts["schema_version"] == 2
    assert facts["record_count"] == 1
    assert "quality" not in validated.stdout.decode("utf-8").lower()

    first = _run(product, run, "render")
    second = _run(product, run, "render")
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert b"h-001" in first.stdout
    assert not (run / "seed_v001.md").exists()


def test_cli_update_rejects_status_and_init_does_not_overwrite(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    assert _run(product, run, "init").returncode == 0
    again = _run(product, run, "init")
    assert again.returncode == 1
    before = (run / "hypotheses_v001" / "portfolio.json").read_bytes()

    source = tmp_path / "draft.json"
    source.write_text(
        json.dumps(_payload("h-002"), ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    assert _run(product, run, "add", "--from-json", str(source)).returncode == 0
    status_patch = tmp_path / "status-patch.json"
    status_patch.write_text(
        '{"status":"falsified"}\n', encoding="utf-8", newline="\n"
    )
    rejected = _run(
        product, run, "update", "h-002", "--patch-json", str(status_patch)
    )
    assert rejected.returncode == 1
    assert b"use transition" in rejected.stderr
    assert (run / "hypotheses_v001" / "portfolio.json").read_bytes() != before


def test_cli_uses_only_the_fixed_product_knowledge_base_path(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    rejected = _run(
        product,
        run,
        "init",
        "--knowledge-root",
        str(tmp_path / "alternate-knowledge"),
    )
    assert rejected.returncode == 2
    assert b"unrecognized arguments: --knowledge-root" in rejected.stderr
    assert not (run / "hypotheses_v001" / "portfolio.json").exists()
