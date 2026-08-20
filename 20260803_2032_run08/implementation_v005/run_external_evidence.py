#!/usr/bin/env python3
"""先运行上游原始单元测试，再运行 v005 不同源持留评价。"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    test_paths = [
        ROOT / "upstream_evidence" / "tests" / "tools" / name
        for name in (
            "contact_test.py",
            "messaging_test.py",
            "reminder_test.py",
            "setting_test.py",
        )
    ]
    environment = dict(os.environ)
    prior = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = str(ROOT / "vendor") + (
        os.pathsep + prior if prior else ""
    )
    test_process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            *map(str, test_paths),
        ],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    test_output = test_process.stdout.decode("utf-8", errors="strict")
    (args.output_dir / "upstream_pytest.txt").write_text(
        test_output, encoding="utf-8"
    )
    if test_process.returncode != 0:
        print(test_output, file=sys.stderr)
        return test_process.returncode

    holdout_process = subprocess.run(
        [
            sys.executable,
            str(ROOT / "external_holdout.py"),
            "--output-dir",
            str(args.output_dir),
        ],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if holdout_process.returncode != 0:
        sys.stdout.buffer.write(holdout_process.stdout)
        sys.stderr.buffer.write(holdout_process.stderr)
        return holdout_process.returncode

    summary = json.loads((args.output_dir / "summary.json").read_text(encoding="utf-8"))
    evidence = {
        "upstream_tests": {
            "exit_code": test_process.returncode,
            "summary_line": next(
                (
                    line
                    for line in reversed(test_output.splitlines())
                    if "passed" in line
                ),
                "",
            ),
            "files": [str(path.relative_to(ROOT)) for path in test_paths],
        },
        "holdout": summary,
    }
    (args.output_dir / "evidence_summary.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
