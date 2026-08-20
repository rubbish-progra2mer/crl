from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from crl_v3.falsification import PARITY_FIELDS, create_experiment_spec, create_plan
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
)
from crl_v3.workspace import ResearchWorkspace


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNNER = PROJECT_ROOT / "tools" / "run_local_experiment.py"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-real-kb",
        action="store_true",
        default=False,
        help="显式允许读取产品根下的真实知识库资产。",
    )
    parser.addoption(
        "--run-real-pdf",
        action="store_true",
        default=False,
        help="显式允许读取产品根下的真实论文 PDF 资产。",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    skip_windows = pytest.mark.skip(reason="该测试只适用于 Windows")
    skip_real_kb = pytest.mark.skip(
        reason="真实知识库资产未通过 --run-real-kb 显式提供"
    )
    skip_real_pdf = pytest.mark.skip(
        reason="真实论文 PDF 资产未通过 --run-real-pdf 显式提供"
    )
    allow_real_kb = bool(config.getoption("--run-real-kb"))
    allow_real_pdf = bool(config.getoption("--run-real-pdf"))
    for item in items:
        if "windows" in item.keywords and sys.platform != "win32":
            item.add_marker(skip_windows)
        if "real_kb" in item.keywords and not allow_real_kb:
            item.add_marker(skip_real_kb)
        if "real_pdf" in item.keywords and not allow_real_pdf:
            item.add_marker(skip_real_pdf)


def make_run(
    tmp_path: Path,
    *,
    status: str = "ACTIVE",
    contract_version: str = "3",
    mode: str = "AUTONOMOUS",
) -> tuple[Path, Path]:
    product_root = tmp_path / "product"
    product_root.mkdir(parents=True, exist_ok=True)
    run = product_root / "20260731_1200_run01"
    run.mkdir()
    controls = {
        "RUN_CHARTER.md": (
            f"# Run Charter\n\nRUN_ID: {run.name}\n"
            f"CRL_CONTRACT_VERSION: {contract_version}\n"
            "DEFAULT_DOMAIN: TEXT_AND_TOOL_LLM_AGENT\n"
            f"MODE: {mode}\nCURRENT_VERSION: v001\n"
        ),
        "RUN_STATUS.md": (
            f"# Run Status\n\nRUN_ID: {run.name}\nSTATUS: {status}\n"
            f"MODE: {mode}\nCURRENT_VERSION: v001\n"
        ),
        "RUN_LEDGER.md": "# Run Ledger\n\n- EVENT: TEST_RUN_CREATED\n",
    }
    for name, content in controls.items():
        (run / name).write_bytes(content.encode("utf-8"))
    return product_root, run


def set_current_version(run: Path, version: str) -> None:
    status = (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    status = status.replace("CURRENT_VERSION: v001", f"CURRENT_VERSION: {version}")
    (run / "RUN_STATUS.md").write_text(status, encoding="utf-8", newline="\n")


def record_successful_attempt(
    product: Path,
    run: Path,
    version: str,
    source: Path,
    *,
    attempt_id: str = "attempt-001",
) -> subprocess.CompletedProcess[bytes]:
    capture = run / f"experiment_{version}" / "attempts" / attempt_id
    output = capture / "result.txt"
    implementation = run / f"implementation_{version}" / "method.py"
    implementation.parent.mkdir(parents=True, exist_ok=True)
    if not implementation.exists():
        implementation.write_bytes(b"def method():\n    return 'test implementation'\n")
    experiment_id = f"experiment-{attempt_id}"
    spec = prepare_experiment_spec(
        product, run, version, experiment_id=experiment_id
    )
    metrics = capture / "metrics-output.json"
    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; import sys; "
            "Path(sys.argv[1]).write_text('actual output\\n', encoding='utf-8'); "
            "Path(sys.argv[2]).write_text(sys.argv[3], encoding='utf-8', newline='\\n'); "
            "print('completed')"
        ),
        str(output),
        str(metrics),
        metrics_json(experiment_id),
    ]
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--version",
            version,
            "--attempt-id",
            attempt_id,
            "--cwd",
            str(source.parent),
            "--experiment-spec",
            str(spec),
            "--metrics-output",
            str(metrics),
            "--implementation-file",
            str(implementation),
            "--input",
            str(source),
            "--output",
            str(output),
            "--seed-not-set",
            "--",
            *command,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def publish_synthetic_fixed_review(
    workspace: ResearchWorkspace,
    *,
    supporting_attempt_id: str | None = None,
    final_delivery: bool = False,
    score: int = 2,
) -> dict[str, object]:
    """Create one deterministic fixed-review triplet for unit tests only."""

    from crl_v3.reviewer_protocol import (
        DIAGNOSTIC_FIELDS,
        DIMENSION_WEIGHTS,
        ROLES,
        create_evaluation,
        finalize_evaluation,
    )

    if not workspace.implementation_path.is_dir():
        workspace.implementation_path.mkdir(parents=True)
        (workspace.implementation_path / "method.py").write_text(
            "def method():\n    return 'unit-test implementation'\n",
            encoding="utf-8",
            newline="\n",
        )
    sections: dict[int, list[str]] = {}
    if workspace.seed_path.is_file():
        sections[1] = [
            workspace.seed_path.relative_to(workspace.workspace_path).as_posix()
        ]
    if supporting_attempt_id is not None:
        execution = (
            workspace.experiment_path
            / "attempts"
            / supporting_attempt_id
            / "execution.json"
        )
        sections[3] = [execution.relative_to(workspace.workspace_path).as_posix()]
    request = create_evaluation(
        workspace, sections, final_delivery=final_delivery
    )
    root = Path(str(request["path"]))
    request_data = (root / "request.json").read_bytes()
    for role in ROLES:
        output = {
            "review_protocol": "CRL-IR-1.0",
            "reviewer_role": role,
            "evaluator_version": "CRL-EVAL-1.0",
            "model_identity": "gpt-5.6-sol",
            "reasoning_effort": "xhigh",
            "scores": {name: score for name in DIMENSION_WEIGHTS[role]},
            "reasons": {
                name: f"unit-test reason for {name}"
                for name in DIMENSION_WEIGHTS[role]
            },
            "diagnostics": {
                name: f"unit-test diagnostic for {name}"
                for name in DIAGNOSTIC_FIELDS[role]
            },
            "critical_risk": "none",
            "confidence": "medium",
            "free_review": f"unit-test {role} review",
        }
        directory = root / role
        directory.mkdir()
        (directory / "report.json").write_text(
            json.dumps(
                {
                    "request_sha256": hashlib.sha256(request_data).hexdigest(),
                    "packet_key": request["packet_key"],
                    "measurement_key": request["measurement_key"],
                    "runtime": {"codex_version": "codex-cli 0.147.0"},
                    "valid": True,
                    "invalid_reasons": [],
                    "output": output,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finalize_evaluation(workspace, str(request["evaluation_id"]))
    return request


def prepare_experiment_spec(
    product: Path,
    run: Path,
    version: str = "v001",
    *,
    experiment_id: str = "experiment-001",
) -> Path:
    workspace = ResearchWorkspace(run, product_root=product, version=version)
    hypothesis_id = f"hypothesis-{experiment_id}"
    claim_id = f"claim-{experiment_id}"
    plan_id = f"plan-{experiment_id}"
    if not workspace.hypotheses_path.exists():
        document = workspace.write_hypotheses(
            empty_portfolio(run.name, version),
            expected_sha256=None,
            create_only=True,
        )
    else:
        document = workspace.read_hypotheses(required=True)
        assert document is not None
    if hypothesis_id not in {
        item.hypothesis_id for item in document.portfolio.hypotheses
    }:
        text = "测试实验身份"
        hypothesis = create_hypothesis_record(
            {
                "hypothesis_id": hypothesis_id,
                "title": text,
                "parent_ids": [],
                "lineage_note": text,
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
                "alternative_explanations": [text],
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
        )
        portfolio = add_hypothesis(document.portfolio, hypothesis)
        document = workspace.write_hypotheses(
            portfolio, expected_sha256=document.sha256
        )
    plan_path = (
        run / f"hypotheses_{version}" / "falsification" / f"{plan_id}.json"
    )
    if not plan_path.exists():
        create_plan(
            workspace,
            {
                "hypothesis_id": hypothesis_id,
                "plan_id": plan_id,
                "claims": [
                    {
                        "claim_id": claim_id,
                        "claim_text": "测试主张。",
                        "scope": "测试范围。",
                        "observable": "测试指标。",
                        "falsifier": "测试反证条件。",
                        "minimum_effect_or_decision_rule": "由主研究者解释。",
                        "alternative_explanations": [],
                        "killer_experiment_id": experiment_id,
                        "supporting_experiment_ids": [],
                        "status": "proposed",
                        "status_reason": "仅为测试预注册身份。",
                    }
                ],
                "global_confounders": [],
            },
        )
    spec_path = run / f"experiment_{version}" / "specs" / f"{experiment_id}.json"
    if not spec_path.exists():
        create_experiment_spec(
            workspace,
            {
                "experiment_id": experiment_id,
                "hypothesis_id": hypothesis_id,
                "claim_ids": [claim_id],
                "purpose": "independent_claim_validation",
                "research_question": "测试问题？",
                "independent_ground_truth": {
                    "description": "独立测试标签。",
                    "external_evidence_ids": [],
                    "external_card_ids": [],
                    "external_literature_refs": [],
                    "run_local_fact_refs": [],
                },
                "primary_metric": "test_primary_metric",
                "secondary_metrics": [],
                "sampling_unit": "测试样本",
                "dataset": "测试集",
                "model": "测试模型",
                "provider": "本地",
                "revision": "test-r1",
                "baseline_specs": [],
                "parity_dimensions": {
                    name: {"status": "matched", "notes": "测试中显式一致"}
                    for name in PARITY_FIELDS
                },
                "seeds": [1],
                "budget_ceiling": '{"api_calls": 2, "tokens": 100}',
                "expected_signatures": [],
                "falsification_rule": "结果由主研究者解释。",
                "confounders": [],
                "declared_inputs": [],
                "declared_outputs": [],
            },
        )
    return spec_path


def metrics_json(
    experiment_id: str,
    *,
    value: float = 0.5,
    tokens: int | None = 10,
    api_calls: int | None = 1,
) -> str:
    return json.dumps(
        {
            "schema_version": 1,
            "experiment_id": experiment_id,
            "records": [
                {
                    "name": "test_primary_metric",
                    "value": value,
                    "unit": "ratio",
                    "split": "test",
                    "aggregation": "mean",
                    "n": 1,
                }
            ],
            "resource_usage": {
                "tokens": tokens,
                "api_calls": api_calls,
                "wall_time_seconds": 0.01,
                "gpu_time_seconds": "unknown",
                "estimated_cost": "unknown",
            },
            "errors": [],
            "warnings": [],
        },
        ensure_ascii=False,
    ) + "\n"


def make_directory_reparse_point(link: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        pytest.skip("当前 Windows 环境不允许创建 Junction，跳过重解析点专用场景")


def make_file_symlink(link: Path, target: Path) -> None:
    try:
        link.symlink_to(target)
    except OSError:
        pytest.skip("当前环境不允许创建文件符号链接，跳过符号链接专用场景")
