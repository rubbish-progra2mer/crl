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
    target = run / "experiment_v035" / "artifacts"
    if target.exists():
        raise FileExistsError(f"artifact directory already exists: {target}")
    target.mkdir(parents=True)
    files = {
        "selection_context_v035.md": run / "selection_context_v035.md",
        "problem_v035.md": run / "problem_v035.md",
        "research_map_v035.md": run / "research_map_v035.md",
        "nearest_prior_v035.md": run / "nearest_prior_v035.md",
        "candidate_v035.md": run / "candidate_v035.md",
        "implementation_audit_v035.md": run / "implementation_audit_v035.md",
        "evidence_packet_v035.md": run / "evidence_packet_v035.md",
        "program.py": run / "implementation_v035" / "program.py",
        "audit.py": run / "implementation_v035" / "audit.py",
        "config.json": run / "implementation_v035" / "config.json",
        "test_program.py": run / "implementation_v035" / "test_program.py",
        "acquire_confirmation.py": run
        / "implementation_v035"
        / "acquire_confirmation.py",
        "run_local_experiment.py": run
        / "implementation_v035"
        / "run_local_experiment.py",
        "acquire_prior.py": run / "sources_v035" / "acquire_prior.py",
        "freeze_artifacts.py": Path(__file__).resolve(),
        "prior_source_manifest.json": run
        / "sources_v035"
        / "prior_source_manifest.json",
        "model_manifest.json": run / "sources_v035" / "model_manifest.json",
        "prmbench_GTA.json": run / "sources_v035" / "prmbench_GTA.json",
        "prmbench_bfcl.json": run / "sources_v035" / "prmbench_bfcl.json",
        "prmbench_tooltalk.json": run / "sources_v035" / "prmbench_tooltalk.json",
        "toolprmbench_2601.12294v1.pdf": run
        / "sources_v035"
        / "toolprmbench_2601.12294v1.pdf",
        "toolrm_2510.26167v2.pdf": run
        / "sources_v035"
        / "toolrm_2510.26167v2.pdf",
        "prepair_2025_blackboxnlp_1_5.pdf": run
        / "sources_v035"
        / "prepair_2025_blackboxnlp_1_5.pdf",
        "pairwise_or_pointwise_2504.14716.pdf": run
        / "sources_v035"
        / "pairwise_or_pointwise_2504.14716.pdf",
        "scope_2602.13110.pdf": run / "sources_v035" / "scope_2602.13110.pdf",
        "v034_result.md": run / "experiment_v034" / "result.md",
        "v034_promotion_audit.md": run
        / "experiment_v034"
        / "promotion_audit_v034.md",
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
        "experiment_id": "v035",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "artifact_record_count": len(files),
        "external_model_record_count": len(model_manifest["files"]),
        "record_count": len(records),
        "total_bytes": sum(record["bytes"] for record in records),
        "records": records,
    }
    manifest_path = target / "artifact_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({key: manifest[key] for key in (
        "artifact_record_count",
        "external_model_record_count",
        "record_count",
        "total_bytes",
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
