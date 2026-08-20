from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


MACHINE_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = MACHINE_ROOT.parent
if str(MACHINE_ROOT) not in sys.path:
    sys.path.insert(0, str(MACHINE_ROOT))

from evaluation.research_discovery.calibration_runner import CalibrationWorkspace  # noqa: E402
from evaluation.research_discovery.calibration_tau2 import (  # noqa: E402
    run_tau2_block,
    windows_utf8_subprocess_environment,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="在冻结评价器上顺序执行声明式 τ² Agent scaffold。"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=PRODUCT_ROOT / "research_workspace" / "reward_calibration_v001",
    )
    parser.add_argument(
        "--research-workspace-root",
        type=Path,
        default=PRODUCT_ROOT / "research_workspace",
    )
    parser.add_argument("--tau2-root", type=Path, required=True)
    parser.add_argument("--phase", choices=("preflight", "pilot", "confirm"), required=True)
    parser.add_argument(
        "--fidelity", choices=("smoke", "low_fidelity", "high_fidelity"), required=True
    )
    parser.add_argument("--block-id", required=True)
    parser.add_argument("--attempt-id", default="attempt-001")
    parser.add_argument("--scaffold", type=Path, required=True)
    parser.add_argument("--agent-model", default="qwen3:8b")
    parser.add_argument("--user-model", default="qwen2.5:7b")
    parser.add_argument("--evaluator-model", default="qwen2.5:7b")
    parser.add_argument("--domain", action="append", dest="domains")
    parser.add_argument("--repetitions", type=int)
    parser.add_argument("--seed", type=int, default=20260819)
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--max-steps", type=int, default=30)
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    child_environment = windows_utf8_subprocess_environment(
        os.environ,
        os_name=os.name,
        utf8_mode=sys.flags.utf8_mode,
    )
    if child_environment is not None:
        child_arguments = sys.argv[1:] if argv is None else argv
        return subprocess.call(
            [sys.executable, str(Path(__file__).resolve()), *child_arguments],
            env=child_environment,
        )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = _parser().parse_args(argv)
    workspace = CalibrationWorkspace(args.workspace, args.research_workspace_root)
    workspace.prepare()
    result = run_tau2_block(
        workspace,
        tau2_root=args.tau2_root,
        phase=args.phase,
        fidelity=args.fidelity,
        block_id=args.block_id,
        attempt_id=args.attempt_id,
        scaffold_path=args.scaffold,
        agent_model=args.agent_model,
        user_model=args.user_model,
        evaluator_model=args.evaluator_model,
        domains=args.domains,
        repetitions=args.repetitions,
        base_seed=args.seed,
        ollama_url=args.ollama_url,
        max_steps=args.max_steps,
        timeout_seconds=args.timeout_seconds,
    )
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
