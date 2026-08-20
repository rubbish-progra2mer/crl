from __future__ import annotations

import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    run = Path(__file__).resolve().parents[1]
    implementation = run / "implementation_v040"
    sources = run / "sources_v040"
    v026 = run / "experiment_v026"
    v039 = run / "experiment_v039"
    target = run / "experiment_v040" / "artifacts"
    if target.exists():
        raise FileExistsError(target)
    target.mkdir(parents=True)
    files = {
        "selection_context_v040.md": run / "selection_context_v040.md",
        "problem_v040.md": run / "problem_v040.md",
        "research_map_v040.md": run / "research_map_v040.md",
        "nearest_prior_v040.md": run / "nearest_prior_v040.md",
        "candidate_v040.md": run / "candidate_v040.md",
        "implementation_audit_v040.md": run / "implementation_audit_v040.md",
        "evidence_packet_v040.md": run / "evidence_packet_v040.md",
        "program.py": implementation / "program.py",
        "audit.py": implementation / "audit.py",
        "base_v012.py": implementation / "base_v012.py",
        "config.json": implementation / "config.json",
        "test_gbcd.py": implementation / "test_gbcd.py",
        "run_local_experiment.py": implementation / "run_local_experiment.py",
        "acquire_confirmation.py": implementation / "acquire_confirmation.py",
        "freeze_artifacts.py": Path(__file__).resolve(),
        "source_manifest_v040.json": sources / "source_manifest_v040.json",
        "development_bucket1_dataset.jsonl": sources
        / "development_bucket1_dataset.jsonl",
        "development_bucket1_manifest.json": sources
        / "development_bucket1_manifest.json",
        "development_bucket2_dataset.jsonl": sources
        / "development_bucket2_dataset.jsonl",
        "development_bucket2_manifest.json": sources
        / "development_bucket2_manifest.json",
        "development_bucket3_dataset.jsonl": sources
        / "development_bucket3_dataset.jsonl",
        "development_bucket3_manifest.json": sources
        / "development_bucket3_manifest.json",
        "group_dro_1911.08731.pdf": sources / "group_dro_1911.08731.pdf",
        "terminal_wrench_2604.17596.pdf": sources
        / "terminal_wrench_2604.17596.pdf",
        "cheap_reward_hacking_2606.08893.pdf": sources
        / "cheap_reward_hacking_2606.08893.pdf",
        "trajectory_guard_2601.00516.pdf": sources
        / "trajectory_guard_2601.00516.pdf",
        "v026_candidate.md": v026 / "artifacts" / "candidate_v026.md",
        "v026_nearest_prior.md": v026 / "artifacts" / "nearest_prior_v026.md",
        "v026_promotion_audit.md": v026
        / "artifacts"
        / "promotion_audit_v026.md",
        "v026_raw_predictions.jsonl": v026
        / "dev_output_001"
        / "raw_predictions.jsonl",
        "v026_summary.json": v026 / "dev_output_001" / "summary.json",
        "v026_model.joblib": v026 / "dev_output_001" / "model.joblib",
        "v026_result.md": v026 / "result.md",
        "v039_attempts_manifest.json": v039 / "attempts_manifest_v039.json",
        "v039_promotion_audit.md": v039 / "promotion_audit_v039.md",
        "v039_result.md": v039 / "result.md",
        "v039_summary.json": v039 / "dev_output_001" / "summary.json",
    }
    records = []
    for name in sorted(files):
        source = files[name]
        if not source.is_file():
            raise FileNotFoundError(source)
        destination = target / name
        shutil.copyfile(source, destination)
        records.append(
            {
                "name": name,
                "resolved_path": str(destination.resolve()),
                "bytes": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )
    manifest = {
        "schema_version": 1,
        "experiment_id": "v040",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "record_count": len(records),
        "total_bytes": sum(record["bytes"] for record in records),
        "records": records,
    }
    (target / "artifact_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "record_count": manifest["record_count"],
                "total_bytes": manifest["total_bytes"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
