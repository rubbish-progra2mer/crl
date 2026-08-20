from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.research_discovery import (  # noqa: E402
    SYSTEM_TYPES,
    build_evaluation_report,
    import_system_output,
    load_annotation_batch,
    load_task_manifest,
    render_markdown_report,
    write_report_files,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "离线导入五类研究系统输出并生成无总分的时间截断分解报告；"
            "不会调用模型、网络或生产知识库。"
        )
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument(
        "--system-output",
        action="append",
        nargs=2,
        metavar=("FORMAT", "PATH"),
        required=True,
        help=f"可重复；FORMAT 为 {', '.join(SYSTEM_TYPES)}",
    )
    parser.add_argument("--annotation", action="append", default=[], type=Path)
    parser.add_argument("--bootstrap-replicates", type=int, default=0)
    parser.add_argument("--confidence-level", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--report-json", type=Path)
    parser.add_argument("--report-markdown", type=Path)
    parser.add_argument(
        "--stdout-format", choices=("json", "markdown"), default="markdown"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = _parser().parse_args(argv)
    if (args.report_json is None) != (args.report_markdown is None):
        raise ValueError("--report-json and --report-markdown must be supplied together")
    manifest = load_task_manifest(args.manifest)
    outputs = [
        import_system_output(path, source_format, manifest)
        for source_format, path in args.system_output
    ]
    annotations = [load_annotation_batch(path, manifest) for path in args.annotation]
    report = build_evaluation_report(
        manifest,
        outputs,
        annotations,
        bootstrap_replicates=args.bootstrap_replicates,
        confidence_level=args.confidence_level,
        random_seed=args.seed,
    )
    if args.report_json is not None:
        write_report_files(report, args.report_json, args.report_markdown)
    if args.stdout_format == "json":
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    else:
        sys.stdout.write(render_markdown_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
