from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the independent oracle before the budget-matched control."
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--oracle-output", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", required=True, type=Path)
    parser.add_argument("--metrics-output", required=True, type=Path)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--prompt-regimes", nargs="+", required=True)
    parser.add_argument("--seeds", nargs="+", type=int, required=True)
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent
    subprocess.run(
        [
            sys.executable,
            str(root / "independent_oracle.py"),
            "--cases",
            str(args.cases),
            "--output",
            str(args.oracle_output),
        ],
        check=True,
    )
    command = [
        sys.executable,
        str(root / "budget_matched_control.py"),
        "--cases",
        str(args.cases),
        "--output",
        str(args.output),
        "--report-output",
        str(args.report_output),
        "--metrics-output",
        str(args.metrics_output),
        "--experiment-id",
        args.experiment_id,
        "--models",
        *args.models,
        "--prompt-regimes",
        *args.prompt_regimes,
        "--seeds",
        *(str(seed) for seed in args.seeds),
        "--ollama-url",
        args.ollama_url,
        "--temperature",
        str(args.temperature),
        "--timeout-seconds",
        str(args.timeout_seconds),
    ]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
