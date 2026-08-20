from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from conftest import make_run
from crl_v3.falsification import PARITY_FIELDS
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
)
from crl_v3.workspace import ResearchWorkspace


TOOL = Path(__file__).resolve().parents[1] / "tools" / "manage_falsification.py"


def _hypothesis_payload() -> dict[str, object]:
    text = "完整字段"
    return {
        "hypothesis_id": "h-001",
        "title": "候选 h-001",
        "parent_ids": [],
        "lineage_note": "根候选",
        "problem": text,
        "target_failure": {
            "summary": text,
            "card_ids": [],
            "evidence_ids": [],
        },
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
        "literature_refs": ["paper-001"],
    }


def _claim() -> dict[str, object]:
    return {
        "claim_id": "claim-001",
        "claim_text": "候选降低错误。",
        "scope": "固定范围",
        "observable": "错误率",
        "falsifier": "错误率不降。",
        "minimum_effect_or_decision_rule": "至少改善 0.05。",
        "alternative_explanations": ["随机波动"],
        "killer_experiment_id": "experiment-001",
        "supporting_experiment_ids": [],
        "status": "proposed",
        "status_reason": "主研究者显式提出。",
    }


def _plan() -> dict[str, object]:
    return {
        "hypothesis_id": "h-001",
        "plan_id": "plan-001",
        "claims": [],
        "global_confounders": ["任务难度"],
    }


def _spec() -> dict[str, object]:
    return {
        "experiment_id": "experiment-001",
        "hypothesis_id": "h-001",
        "claim_ids": ["claim-001"],
        "purpose": "independent_claim_validation",
        "research_question": "是否支持 Claim？",
        "independent_ground_truth": {
            "description": "独立人工标签",
            "external_evidence_ids": [],
            "external_card_ids": [],
            "external_literature_refs": ["paper-001"],
            "run_local_fact_refs": ["workbench_v001/labels.json"],
        },
        "primary_metric": "错误率",
        "secondary_metrics": [],
        "sampling_unit": "任务",
        "dataset": "固定集",
        "model": "模型",
        "provider": "本地",
        "revision": "r1",
        "baseline_specs": ["同预算基线"],
        "parity_dimensions": {
            name: {"status": "matched", "notes": "显式声明一致"}
            for name in PARITY_FIELDS
        },
        "seeds": [1],
        "budget_ceiling": "100 次调用",
        "expected_signatures": ["改善至少 0.05"],
        "falsification_rule": "改善不足 0.05。",
        "confounders": [],
        "declared_inputs": ["workbench_v001/labels.json"],
        "declared_outputs": ["experiment_v001/metrics.json"],
    }


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


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


def _setup(tmp_path: Path) -> tuple[Path, Path]:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product, version="v001")
    document = workspace.write_hypotheses(
        empty_portfolio(run.name, "v001"),
        expected_sha256=None,
        create_only=True,
    )
    portfolio = add_hypothesis(
        document.portfolio,
        create_hypothesis_record(_hypothesis_payload()),
    )
    workspace.write_hypotheses(portfolio, expected_sha256=document.sha256)
    return product, run


def test_cli_all_p5_actions_and_deterministic_render(tmp_path: Path) -> None:
    product, run = _setup(tmp_path)
    plan_path = tmp_path / "plan.json"
    claim_path = tmp_path / "claim.json"
    patch_path = tmp_path / "patch.json"
    spec_path = tmp_path / "spec.json"
    _write_json(plan_path, _plan())
    _write_json(claim_path, _claim())
    _write_json(
        patch_path,
        {"status": "testing", "status_reason": "显式开始测试。"},
    )
    _write_json(spec_path, _spec())

    created = _run(product, run, "create-plan", "--from-json", str(plan_path))
    assert created.returncode == 0, created.stderr.decode("utf-8")
    assert json.loads(created.stdout)["plan_id"] == "plan-001"

    added = _run(
        product,
        run,
        "add-claim",
        "plan-001",
        "--from-json",
        str(claim_path),
    )
    assert added.returncode == 0, added.stderr.decode("utf-8")
    assert json.loads(added.stdout)["claim_count"] == 1

    updated = _run(
        product,
        run,
        "update-claim",
        "plan-001",
        "claim-001",
        "--patch-json",
        str(patch_path),
    )
    assert updated.returncode == 0, updated.stderr.decode("utf-8")
    assert json.loads(updated.stdout)["status"] == "testing"

    spec = _run(
        product,
        run,
        "create-experiment-spec",
        "--from-json",
        str(spec_path),
    )
    assert spec.returncode == 0, spec.stderr.decode("utf-8")
    assert json.loads(spec.stdout)["purpose"] == "independent_claim_validation"

    validated = _run(product, run, "validate")
    assert validated.returncode == 0, validated.stderr.decode("utf-8")
    facts = json.loads(validated.stdout)
    assert facts["claim_count"] == 1
    assert facts["experiment_spec_count"] == 1
    assert "score" not in validated.stdout.decode("utf-8").lower()

    first = _run(product, run, "render", "plan-001")
    second = _run(product, run, "render", "plan-001")
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert "什么结果会杀死该 Claim" in first.stdout.decode("utf-8")
    assert not (run / "seed_v001.md").exists()


def test_cli_requires_json_files_for_scientific_bodies_and_does_not_overwrite(
    tmp_path: Path,
) -> None:
    product, run = _setup(tmp_path)
    plan_path = tmp_path / "plan.json"
    _write_json(plan_path, _plan())
    first = _run(product, run, "create-plan", "--from-json", str(plan_path))
    assert first.returncode == 0
    before = (run / "hypotheses_v001" / "falsification" / "plan-001.json").read_bytes()
    again = _run(product, run, "create-plan", "--from-json", str(plan_path))
    assert again.returncode == 1
    assert b"already exists" in again.stderr
    assert (run / "hypotheses_v001" / "falsification" / "plan-001.json").read_bytes() == before

    rejected = _run(
        product,
        run,
        "add-claim",
        "plan-001",
        "--claim-text",
        "不得从命令行自由文本注入科研正文",
    )
    assert rejected.returncode == 2
    assert b"--from-json" in rejected.stderr
