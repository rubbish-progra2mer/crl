from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


MACHINE_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = MACHINE_ROOT.parent
if str(MACHINE_ROOT) not in sys.path:
    sys.path.insert(0, str(MACHINE_ROOT))

from evaluation.research_discovery.calibration_runner import (  # noqa: E402
    CalibrationWorkspace,
    build_calibration_report,
    lock_tau2_preflight_selection,
    repair_evaluator_lock,
    repair_frozen_task_split,
    run_preflight,
    run_temporal_validation,
    summarize_confirmation,
    summarize_pilot,
    summarize_tau2_preflight,
)


DEFAULT_RESEARCH_WORKSPACE = PRODUCT_ROOT / "research_workspace"
DEFAULT_CALIBRATION_WORKSPACE = DEFAULT_RESEARCH_WORKSPACE / "reward_calibration_v001"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "运行 CRL 科研搜索奖励的 Run 外校准；不会改变候选状态、认证新颖性或形成 Delivery。"
        )
    )
    parser.add_argument("--workspace", type=Path, default=DEFAULT_CALIBRATION_WORKSPACE)
    parser.add_argument(
        "--research-workspace-root", type=Path, default=DEFAULT_RESEARCH_WORKSPACE
    )
    subparsers = parser.add_subparsers(dest="phase", required=True)

    preflight = subparsers.add_parser("preflight", help="冻结协议、任务与评价器并检查模型")
    preflight.add_argument("--tau2-root", type=Path, required=True)
    preflight.add_argument("--agent-model", default="qwen3:8b")
    preflight.add_argument("--user-model", default="qwen2.5:7b")
    preflight.add_argument("--reserve-model", default="qwen3:14b")
    preflight.add_argument("--evaluator-model", default="qwen2.5:7b")
    preflight.add_argument("--split-seed", type=int, default=20260819)
    preflight.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    preflight.add_argument("--repair-task-split", action="store_true")
    preflight.add_argument("--repair-evaluator-lock", action="store_true")

    preflight_lock = subparsers.add_parser(
        "preflight-lock", help="在执行前不可变地锁定四个预检角色"
    )
    preflight_lock.add_argument("--selection", type=Path, required=True)

    preflight_results = subparsers.add_parser(
        "preflight-results", help="按显式尝试选择汇总 τ² 预检门槛"
    )
    preflight_results.add_argument("--selection", type=Path, required=True)

    pilot = subparsers.add_parser("pilot", help="记录并汇总两块小试材料")
    pilot.add_argument("--event-json", type=Path, action="append", default=[])

    confirm = subparsers.add_parser("confirm", help="记录并汇总八个新配对块")
    confirm.add_argument("--event-json", type=Path, action="append", default=[])

    temporal = subparsers.add_parser("temporal", help="核验时间洁净材料包")
    temporal.add_argument("--packet", type=Path, required=True)

    subparsers.add_parser("report", help="汇总已有的不可变阶段材料")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = _parser().parse_args(argv)
    workspace = CalibrationWorkspace(args.workspace, args.research_workspace_root)
    if args.phase == "preflight":
        if args.repair_task_split:
            repair_frozen_task_split(
                workspace, tau2_root=args.tau2_root, split_seed=args.split_seed
            )
        if args.repair_evaluator_lock:
            repair_evaluator_lock(workspace, tau2_root=args.tau2_root)
        result = run_preflight(
            workspace,
            tau2_root=args.tau2_root,
            agent_model=args.agent_model,
            user_model=args.user_model,
            reserve_model=args.reserve_model,
            evaluator_model=args.evaluator_model,
            split_seed=args.split_seed,
            ollama_url=args.ollama_url,
        )
    elif args.phase in {"preflight-lock", "preflight-results"}:
        workspace.prepare()
        selection_path = workspace.bind_read_file(args.selection)
        selection_data = selection_path.read_bytes()
        if selection_data.startswith(b"\xef\xbb\xbf") or b"\r" in selection_data:
            raise ValueError(
                "preflight selection JSON must be UTF-8 without BOM and LF-only"
            )
        selection = json.loads(selection_data.decode("utf-8", errors="strict"))
        if not isinstance(selection, dict):
            raise ValueError("preflight selection JSON root must be an object")
        if args.phase == "preflight-lock":
            result = lock_tau2_preflight_selection(workspace, selection)
        else:
            result = summarize_tau2_preflight(workspace, selection)
    elif args.phase == "pilot":
        workspace.prepare()
        if args.event_json:
            raise RuntimeError(
                "pilot event import is disabled until events are derived from immutable tau2 manifests"
            )
        result = summarize_pilot(workspace)
    elif args.phase == "confirm":
        workspace.prepare()
        if args.event_json:
            raise RuntimeError(
                "confirmation event import is disabled until events are derived from immutable tau2 manifests"
            )
        result = summarize_confirmation(workspace)
    elif args.phase == "temporal":
        workspace.prepare()
        result = run_temporal_validation(workspace, args.packet)
    else:
        workspace.prepare()
        result = build_calibration_report(workspace)
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return 0


def _ingest_events(
    workspace: CalibrationWorkspace, phase: str, paths: list[Path]
) -> None:
    for path in paths:
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
            raise ValueError(f"event JSON must be UTF-8 without BOM and LF-only: {path}")
        value = json.loads(data.decode("utf-8", errors="strict"))
        if not isinstance(value, dict):
            raise ValueError(f"event JSON root must be an object: {path}")
        workspace.record_event(phase, value)


if __name__ == "__main__":
    raise SystemExit(main())
