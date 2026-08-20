from __future__ import annotations

import json
from pathlib import Path

from conftest import make_run, record_successful_attempt
from tools.compare_attempts import main


def test_cli_accepts_multiple_baselines_and_publishes_fixed_pair(
    tmp_path: Path, capsys
) -> None:
    product, run = make_run(tmp_path)
    source = run / "workbench_v001" / "source.py"
    source.parent.mkdir()
    source.write_bytes(b"print('fixture')\n")
    for attempt_id in ("candidate", "baseline-a", "baseline-b"):
        completed = record_successful_attempt(
            product, run, "v001", source, attempt_id=attempt_id
        )
        assert completed.returncode == 0
    result = main(
        [
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--version",
            "v001",
            "--comparison-id",
            "cli-comparison",
            "--candidate-attempt",
            "candidate",
            "--baseline-attempt",
            "baseline-a",
            "--baseline-attempt",
            "baseline-b",
        ]
    )
    assert result == 0
    output = json.loads(capsys.readouterr().out)
    assert output["baseline_attempt_ids"] == ["baseline-a", "baseline-b"]
    path = Path(output["path"])
    assert sorted(item.name for item in path.iterdir()) == [
        "comparison.json",
        "report.md",
    ]
