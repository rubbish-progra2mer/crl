from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


MACHINE_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = MACHINE_ROOT.parent
BYTECODE_READ_PREFIX = (
    PRODUCT_ROOT
    / "research_workspace"
    / "reward_calibration_v001"
    / "preflight"
    / "runtime"
    / f"unused-pycache-{os.getpid()}"
)
if str(MACHINE_ROOT) not in sys.path:
    sys.path.insert(0, str(MACHINE_ROOT))


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
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    child_arguments = sys.argv[1:] if argv is None else argv
    if (
        sys.flags.utf8_mode == 0
        or not sys.dont_write_bytecode
        or sys.pycache_prefix is None
    ):
        bootstrap_environment = dict(os.environ)
        for name in list(bootstrap_environment):
            upper = name.upper()
            if any(
                marker in upper
                for marker in ("API_KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL")
            ):
                bootstrap_environment.pop(name, None)
        bootstrap_environment["PYTHONUTF8"] = "1"
        bootstrap_environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.call(
            [
                sys.executable,
                "-B",
                "-X",
                "utf8",
                "-X",
                f"pycache_prefix={BYTECODE_READ_PREFIX}",
                str(Path(__file__).resolve()),
                *child_arguments,
            ],
            env=bootstrap_environment,
        )

    from crl_v3.decision import child_process_environment
    from evaluation.research_discovery.calibration_runner import CalibrationWorkspace
    from evaluation.research_discovery.calibration_tau2 import (
        run_tau2_block,
        windows_utf8_subprocess_environment,
    )

    safe_environment, _ = child_process_environment()
    child_environment = windows_utf8_subprocess_environment(
        safe_environment,
        os_name=os.name,
        utf8_mode=sys.flags.utf8_mode,
    )
    environment_was_sanitized = safe_environment != dict(os.environ)
    if child_environment is not None or environment_was_sanitized:
        if child_environment is None:
            child_environment = safe_environment
        return subprocess.call(
            [
                sys.executable,
                "-B",
                "-X",
                "utf8",
                "-X",
                f"pycache_prefix={BYTECODE_READ_PREFIX}",
                str(Path(__file__).resolve()),
                *child_arguments,
            ],
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
