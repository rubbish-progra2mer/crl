from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_EQUAL_KEYS = {
    "card_source_signature",
    "integrity_concerns",
    "per_query",
    "protocol",
    "schema_version",
    "summary",
}
EXPECTED_RELOCATION_KEYS = {
    "created_at",
    "evaluation_id",
    "frozen_inputs",
    "index_status",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def compare_split(root: Path, split: str) -> dict[str, object]:
    before_path = root / "v006" / f"{split}_results.json"
    after_path = root / "v007" / f"{split}_results.json"
    before = json.loads(before_path.read_text(encoding="utf-8"))
    after = json.loads(after_path.read_text(encoding="utf-8"))

    if set(before) != set(after):
        raise ValueError(f"{split}: top-level keys changed")
    equal_keys = {key for key in before if before[key] == after[key]}
    differing_keys = set(before) - equal_keys
    if equal_keys != EXPECTED_EQUAL_KEYS:
        raise ValueError(f"{split}: unexpected equal keys: {sorted(equal_keys)}")
    if differing_keys != EXPECTED_RELOCATION_KEYS:
        raise ValueError(
            f"{split}: unexpected differing keys: {sorted(differing_keys)}"
        )

    before_ids = [item["query_id"] for item in before["per_query"]]
    after_ids = [item["query_id"] for item in after["per_query"]]
    if before_ids != after_ids:
        raise ValueError(f"{split}: query identity/order changed")

    return {
        "split": split,
        "result_v006": {
            "path": before_path.relative_to(root.parent.parent.parent).as_posix(),
            "sha256": sha256(before_path),
        },
        "result_v007": {
            "path": after_path.relative_to(root.parent.parent.parent).as_posix(),
            "sha256": sha256(after_path),
        },
        "query_count": len(before_ids),
        "query_ids": before_ids,
        "per_query_exact_equal": True,
        "per_query_canonical_sha256": canonical_sha256(before["per_query"]),
        "summary_exact_equal": True,
        "summary": before["summary"],
        "summary_canonical_sha256": canonical_sha256(before["summary"]),
        "protocol_exact_equal": True,
        "card_source_signature_exact_equal": True,
        "integrity_concerns_exact_equal": True,
        "expected_relocation_only_top_level_differences": sorted(differing_keys),
        "verdict": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    project_root = arguments.project_root.resolve()
    production_root = (
        project_root / "knowledge_base" / "evaluation" / "production_eval"
    )
    output = arguments.output.resolve()
    if output.exists():
        raise FileExistsError(f"one-shot output already exists: {output}")

    comparisons = [
        compare_split(production_root, split) for split in ("calibration", "blind")
    ]
    relocation_manifest = production_root / "v007" / "relocation_manifest.json"
    document = {
        "schema_version": 1,
        "purpose": (
            "Prove that relocating only papers.fulltext_path changed no retrieval "
            "ranking, hit, source-chain, decision, protocol, integrity concern, or summary."
        ),
        "relocation_manifest": {
            "path": relocation_manifest.relative_to(project_root).as_posix(),
            "sha256": sha256(relocation_manifest),
        },
        "comparisons": comparisons,
        "overall_verdict": "PASS",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(document, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
