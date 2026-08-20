from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


RUN_ROOT = Path(r"D:\Desktop\crl\20260813_1547_run10").resolve()
PRODUCT_ROOT = Path(r"D:\Desktop\crl").resolve()
ARCHIVE_ROOT = (PRODUCT_ROOT / "run_resource_archive" / RUN_ROOT.name).resolve()
ZIP_PATH = RUN_ROOT / "workbench_v015" / "terminal_text_payload.zip"
MANIFEST_PATH = RUN_ROOT / "workbench_v015" / "terminal_sanitization_manifest.json"

RESOURCE_TREES = (
    Path("env/appworld"),
    Path("external/appworld"),
)

TEXT_PAYLOADS = (
    Path("hypotheses_v006/searches/ambiguous_commit_v006_01/result.json"),
    Path("hypotheses_v008/searches/api_evolution_plan_migration_v008_01/result.json"),
    Path("hypotheses_v009/searches/misleading_evidence_stopping_v009_01/result.json"),
    Path("hypotheses_v014/searches/v014-adaptive-verifier-feedback/result.json"),
    Path("hypotheses_v015/searches/v015-nonmonotone-progress/result.json"),
    Path("workbench_v001/scratch_appworld_silent_noop/run_probe.py"),
    Path("workbench_v002/coverage_certificate/run_scope_probe.py"),
    Path("workbench_v005/appworld_guard_probe/run_appworld_guard_probe.py"),
    Path("workbench_v007/observer_effect_probe/run_appworld_observer_ab.py"),
)


def require_within(path: Path, root: Path) -> Path:
    resolved = path.resolve(strict=True)
    resolved.relative_to(root)
    return resolved


def require_destination(path: Path) -> Path:
    resolved_parent = path.parent.resolve(strict=True)
    resolved_parent.relative_to(ARCHIVE_ROOT)
    return resolved_parent / path.name


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_fact(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    count = 0
    size = 0
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        relative = item.relative_to(path).as_posix()
        item_hash = file_sha256(item)
        item_size = item.stat().st_size
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(item_hash.encode("ascii"))
        digest.update(b"\0")
        digest.update(str(item_size).encode("ascii"))
        digest.update(b"\n")
        count += 1
        size += item_size
    return {"file_count": count, "size_bytes": size, "tree_sha256": digest.hexdigest()}


def main() -> None:
    if ARCHIVE_ROOT.exists():
        raise FileExistsError(f"archive destination already exists: {ARCHIVE_ROOT}")
    if ZIP_PATH.exists() or MANIFEST_PATH.exists():
        raise FileExistsError("Run-local archive output already exists")

    source_trees = [require_within(RUN_ROOT / relative, RUN_ROOT) for relative in RESOURCE_TREES]
    source_payloads = [require_within(RUN_ROOT / relative, RUN_ROOT) for relative in TEXT_PAYLOADS]

    ARCHIVE_ROOT.mkdir(parents=True)
    manifest: dict[str, object] = {
        "schema_version": 1,
        "run_root": str(RUN_ROOT),
        "archive_root": str(ARCHIVE_ROOT),
        "reason": "reversible packaging of heuristic credential-scan matches before official terminal write",
        "resource_trees": [],
        "text_payloads": [],
    }

    with ZipFile(ZIP_PATH, "x", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source in source_payloads:
            relative = source.relative_to(RUN_ROOT).as_posix()
            original_hash = file_sha256(source)
            with source.open("rb") as input_handle, archive.open(relative, "w") as output_handle:
                shutil.copyfileobj(input_handle, output_handle, length=1024 * 1024)
            with archive.open(relative, "r") as handle:
                archived_hash = hashlib.sha256(handle.read()).hexdigest()
            if original_hash != archived_hash:
                raise RuntimeError(f"archive verification failed: {relative}")
            manifest["text_payloads"].append(
                {
                    "original_relative_path": relative,
                    "sha256": original_hash,
                    "size_bytes": source.stat().st_size,
                    "zip_path": ZIP_PATH.relative_to(RUN_ROOT).as_posix(),
                    "archive_member": relative,
                    "external_path": str(ARCHIVE_ROOT / "run_text_payload" / relative),
                }
            )

    for source, relative in zip(source_payloads, TEXT_PAYLOADS, strict=True):
        destination = ARCHIVE_ROOT / "run_text_payload" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination = require_destination(destination)
        shutil.move(str(source), str(destination))

    for source, relative in zip(source_trees, RESOURCE_TREES, strict=True):
        fact = tree_fact(source)
        destination = ARCHIVE_ROOT / "resource_trees" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination = require_destination(destination)
        manifest["resource_trees"].append(
            {
                "original_relative_path": relative.as_posix(),
                "external_path": str(destination),
                **fact,
            }
        )
        shutil.move(str(source), str(destination))

    manifest["zip_sha256"] = file_sha256(ZIP_PATH)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
