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
    prior = run / "experiment_v035" / "artifacts"
    target = run / "experiment_v036" / "artifacts"
    if target.exists():
        raise FileExistsError(target)
    target.mkdir(parents=True)
    files = {
        "selection_context_v036.md": run / "selection_context_v036.md",
        "problem_v036.md": run / "problem_v036.md",
        "research_map_v036.md": run / "research_map_v036.md",
        "nearest_prior_v036.md": run / "nearest_prior_v036.md",
        "candidate_v036.md": run / "candidate_v036.md",
        "implementation_audit_v036.md": run / "implementation_audit_v036.md",
        "evidence_packet_v036.md": run / "evidence_packet_v036.md",
        "program.py": run / "implementation_v036" / "program.py",
        "audit.py": run / "implementation_v036" / "audit.py",
        "config.json": run / "implementation_v036" / "config.json",
        "test_program.py": run / "implementation_v036" / "test_program.py",
        "acquire_confirmation.py": run
        / "implementation_v036"
        / "acquire_confirmation.py",
        "run_local_experiment.py": run
        / "implementation_v036"
        / "run_local_experiment.py",
        "freeze_artifacts.py": Path(__file__).resolve(),
        "v035_candidate.md": prior / "candidate_v035.md",
        "v035_problem.md": prior / "problem_v035.md",
        "v035_research_map.md": prior / "research_map_v035.md",
        "v035_nearest_prior.md": prior / "nearest_prior_v035.md",
        "v035_selection_context.md": prior / "selection_context_v035.md",
        "v035_evidence_packet.md": prior / "evidence_packet_v035.md",
        "v035_artifact_manifest.json": prior / "artifact_manifest.json",
        "v035_plan.md": run / "experiment_v035" / "plan.md",
        "v035_execution.json": run
        / "experiment_v035"
        / "captures"
        / "dev_001"
        / "execution.json",
        "v035_stdout.bin": run
        / "experiment_v035"
        / "captures"
        / "dev_001"
        / "stdout.bin",
        "v035_stderr.bin": run
        / "experiment_v035"
        / "captures"
        / "dev_001"
        / "stderr.bin",
        "v035_attempts_manifest.json": run
        / "experiment_v035"
        / "attempts_manifest_v035.json",
        "v035_result.md": run / "experiment_v035" / "result.md",
        "prior_source_manifest.json": prior / "prior_source_manifest.json",
        "model_manifest.json": prior / "model_manifest.json",
        "prmbench_GTA.json": prior / "prmbench_GTA.json",
        "prmbench_bfcl.json": prior / "prmbench_bfcl.json",
        "prmbench_tooltalk.json": prior / "prmbench_tooltalk.json",
        "toolprmbench_2601.12294v1.pdf": prior
        / "toolprmbench_2601.12294v1.pdf",
        "toolrm_2510.26167v2.pdf": prior / "toolrm_2510.26167v2.pdf",
        "prepair_2025_blackboxnlp_1_5.pdf": prior
        / "prepair_2025_blackboxnlp_1_5.pdf",
        "pairwise_or_pointwise_2504.14716.pdf": prior
        / "pairwise_or_pointwise_2504.14716.pdf",
        "scope_2602.13110.pdf": prior / "scope_2602.13110.pdf",
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
                "kind": "artifact",
                "resolved_path": str(destination.resolve()),
                "bytes": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )
    model_manifest = json.loads((target / "model_manifest.json").read_text(encoding="utf-8"))
    for model_file in model_manifest["files"]:
        path = Path(model_file["resolved_path"])
        if path.stat().st_size != model_file["bytes"] or sha256(path) != model_file["sha256"]:
            raise ValueError(f"external model mismatch: {path}")
        records.append(
            {
                "name": f"model/{model_file['name']}",
                "kind": "external_frozen_model",
                "resolved_path": str(path.resolve()),
                "bytes": model_file["bytes"],
                "sha256": model_file["sha256"],
            }
        )
    manifest = {
        "schema_version": 1,
        "experiment_id": "v036",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "artifact_record_count": len(files),
        "external_model_record_count": len(model_manifest["files"]),
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
                key: manifest[key]
                for key in (
                    "artifact_record_count",
                    "external_model_record_count",
                    "record_count",
                    "total_bytes",
                )
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
