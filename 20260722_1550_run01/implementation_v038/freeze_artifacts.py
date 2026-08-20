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
    implementation = run / "implementation_v038"
    sources = run / "sources_v038"
    previous = run / "experiment_v037"
    target = run / "experiment_v038" / "artifacts"
    if target.exists():
        raise FileExistsError(target)
    target.mkdir(parents=True)
    files = {
        "selection_context_v038.md": run / "selection_context_v038.md",
        "problem_v038.md": run / "problem_v038.md",
        "research_map_v038.md": run / "research_map_v038.md",
        "nearest_prior_v038.md": run / "nearest_prior_v038.md",
        "candidate_v038.md": run / "candidate_v038.md",
        "implementation_audit_v038.md": run / "implementation_audit_v038.md",
        "evidence_packet_v038.md": run / "evidence_packet_v038.md",
        "program.py": implementation / "program.py",
        "audit.py": implementation / "audit.py",
        "config.json": implementation / "config.json",
        "test_program.py": implementation / "test_program.py",
        "acquire_confirmation.py": implementation / "acquire_confirmation.py",
        "run_local_experiment.py": implementation / "run_local_experiment.py",
        "freeze_artifacts.py": Path(__file__).resolve(),
        "model_manifest.json": sources / "model_manifest.json",
        "prmbench_GTA.json": sources / "prmbench_GTA.json",
        "prmbench_bfcl.json": sources / "prmbench_bfcl.json",
        "prmbench_tooltalk.json": sources / "prmbench_tooltalk.json",
        "prior_source_manifest.json": sources / "prior_source_manifest.json",
        "toolformer_P082.pdf": sources / "toolformer_P082.pdf",
        "toolprmbench_2601.12294v1.pdf": sources
        / "toolprmbench_2601.12294v1.pdf",
        "toolrm_2510.26167v2.pdf": sources / "toolrm_2510.26167v2.pdf",
        "v037_artifact_manifest.json": previous
        / "artifacts"
        / "artifact_manifest.json",
        "v037_attempts_manifest.json": previous / "attempts_manifest_v037.json",
        "v037_result.md": previous / "result.md",
        "v037_plan.md": previous / "plan.md",
        "v037_invocation_failure.md": previous
        / "development_invocation_failure.md",
        "v037_candidate.md": previous / "artifacts" / "candidate_v037.md",
        "v037_evidence_packet.md": previous
        / "artifacts"
        / "evidence_packet_v037.md",
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
    model_manifest = json.loads(
        (target / "model_manifest.json").read_text(encoding="utf-8")
    )
    for model_file in model_manifest["files"]:
        path = Path(model_file["resolved_path"])
        if (
            path.stat().st_size != model_file["bytes"]
            or sha256(path) != model_file["sha256"]
        ):
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
        "experiment_id": "v038",
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
