from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from run_gaia2_local_effect_trace_panel import (
    CONFIGS,
    CUE_ORDER,
    git_revision,
    ollama_model_digest,
    run_one,
    select_panel,
    sha256_file,
)


def select_independent_panel(
    source_dir: Path,
    development_panel: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    candidates, manifest = select_panel(source_dir, per_cue=2)
    by_stratum: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in candidates:
        by_stratum[item["panel_stratum"]].append(item)
    selected = []
    for stratum in CUE_ORDER:
        items = by_stratum[stratum]
        if len(items) != 2:
            raise ValueError(f"Expected two frozen candidates for {stratum}, got {len(items)}")
        selected.append(items[1])

    prior = json.loads(development_panel.read_text(encoding="utf-8"))
    development_identities = {
        item["scenario_identity_sha256"] for item in prior.get("results") or []
    }
    selected_identities = {item["identity_sha256"] for item in selected}
    overlap = development_identities & selected_identities
    if overlap:
        raise ValueError(f"Admission panel overlaps development identities: {sorted(overlap)}")
    return selected, manifest, sha256_file(development_panel)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--development-panel", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen2.5:7b")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--max-iterations", type=int, default=8)
    parser.add_argument("--invalid-format-retries", type=int, default=1)
    parser.add_argument("--num-predict", type=int, default=768)
    parser.add_argument("--num-ctx", type=int, default=16384)
    parser.add_argument("--seed", type=int, default=20260831)
    parser.add_argument("--request-timeout", type=float, default=300.0)
    args = parser.parse_args()

    if not args.development_panel.is_file():
        raise FileNotFoundError(args.development_panel)
    for key in ("HF_HUB_OFFLINE", "HF_DATASETS_OFFLINE", "TRANSFORMERS_OFFLINE"):
        os.environ[key] = "1"
    logging.getLogger().setLevel(logging.ERROR)

    panel, manifest, development_sha256 = select_independent_panel(
        args.source_dir.resolve(), args.development_panel.resolve()
    )
    results = []
    for index, item in enumerate(panel):
        results.append(
            run_one(
                item,
                model=args.model,
                endpoint=args.endpoint,
                seed=args.seed + index,
                num_predict=args.num_predict,
                num_ctx=args.num_ctx,
                timeout=args.request_timeout,
                max_iterations=args.max_iterations,
                invalid_format_retries=args.invalid_format_retries,
            )
        )

    aggregate = Counter()
    for result in results:
        aggregate.update(result["counts"])
    aggregate["scenarios"] = len(results)
    aggregate["scenarios_with_effectful_read"] = sum(
        result["counts"]["effectful_read_calls"] > 0 for result in results
    )
    aggregate["scenarios_with_any_declared_read"] = sum(
        result["counts"]["declared_read_calls"] > 0 for result in results
    )

    script_path = Path(__file__).resolve()
    base_script = Path(sys.modules["run_gaia2_local_effect_trace_panel"].__file__).resolve()
    output = {
        "source": {
            "repository": "facebookresearch/meta-agents-research-environments",
            "are_revision": git_revision(args.are_root.resolve()),
            "dataset": "meta-agents-research-environments/gaia2",
            "dataset_revision": "78ea3bdbdeec2bdcd6afa5420915d8a22f23ed99",
            "split": "validation",
            "configs": list(CONFIGS),
            "parquet_files": manifest,
            "python": sys.executable,
            "script": str(script_path),
            "script_sha256": sha256_file(script_path),
            "shared_runner_script": str(base_script),
            "shared_runner_script_sha256": sha256_file(base_script),
            "development_panel": str(args.development_panel.resolve()),
            "development_panel_sha256": development_sha256,
        },
        "independent_panel_contract": {
            "selection": (
                "For every cue stratum, take the second lexicographically smallest "
                "SHA-256 scenario identity from the pre-model two-item selection."
            ),
            "cue_order": list(CUE_ORDER),
            "selected_scenarios": len(panel),
            "development_identity_overlap": 0,
            "different_model_from_development": args.model != "qwen3.5:9b",
            "task_text_emitted": False,
        },
        "model": {
            "runtime": "Ollama loopback HTTP API",
            "model": args.model,
            "digest": ollama_model_digest(args.endpoint, args.model, args.request_timeout),
            "temperature": 0,
            "seed_base": args.seed,
            "seed_schedule": "seed_base + scenario_index + model_call_index",
            "num_predict": args.num_predict,
            "num_ctx": args.num_ctx,
            "think": False,
        },
        "execution_contract": {
            "agent": "official ARE default ReAct JSON agent and tool descriptions",
            "judge": "disabled; independent trace screening only",
            "max_iterations_per_turn": args.max_iterations,
            "invalid_format_retries": args.invalid_format_retries,
            "simulated_generation_time_mode": "measured",
            "effect_closure_projection": (
                "curated app state plus TimeManager offset and pause_offset; real clock "
                "bookkeeping, callbacks, registries and instrumentation flags are excluded"
            ),
            "external_network_offline_flags": True,
            "filesystem_app_dependency_available_in_venv": False,
            "cache_or_export_invoked": False,
        },
        "results": results,
        "aggregate": dict(sorted(aggregate.items())),
        "interpretation_boundary": (
            "This panel is task-identity-disjoint from the development panel and uses a "
            "different installed local model, so it is an independent low-fidelity screening "
            "check of natural declared-READ calls and the frozen effect projection. It still "
            "uses no official judge, caps the agent loop, omits the unavailable filesystem app, "
            "and cannot establish official submitted-model prevalence, score corrections, "
            "rank changes, representative detector accuracy, or paper-level admission."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
