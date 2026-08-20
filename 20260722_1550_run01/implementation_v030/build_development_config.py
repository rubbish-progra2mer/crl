from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEVELOPMENT_PRS = (865, 870, 871, 872, 876, 892, 962, 963)
CONFIRMATION_PRS = (1084, 1085, 1086, 1087, 1175, 1177)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def changed_ids(files: list[dict[str, object]]) -> tuple[str, list[str]]:
    data_files = [
        item
        for item in files
        if "/data/" in str(item["filename"]) and "CHANGELOG" not in str(item["filename"])
    ]
    if len(data_files) != 1:
        raise ValueError(f"expected one modified data file, got {len(data_files)}")
    item = data_files[0]
    removed: list[str] = []
    for line in str(item.get("patch", "")).splitlines():
        if line.startswith("-") and not line.startswith("---"):
            try:
                row = json.loads(line[1:])
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                removed.append(row["id"])
    ids = sorted(set(removed))
    if not ids:
        raise ValueError("patch yielded no removed entry IDs")
    return str(item["filename"]), ids


def locate(root: Path, pr: int, tag: str, basename: str) -> Path | None:
    path = root / f"pr_{pr}_{tag}_{basename}"
    return path if path.is_file() else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase", choices=("development", "confirmation"), required=True
    )
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    prs = DEVELOPMENT_PRS if args.phase == "development" else CONFIRMATION_PRS

    records: list[dict[str, object]] = []
    total_changed = 0
    for pr in prs:
        meta_path = args.source_root / f"pr_{pr}_meta.json"
        files_path = args.source_root / f"pr_{pr}_files.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
        files = json.loads(files_path.read_text(encoding="utf-8-sig"))
        if not meta["merged"]:
            raise ValueError(f"PR {pr} is not merged")
        modified_path, labels = changed_ids(files)
        if "/possible_answer/" in modified_path:
            answer_name = Path(modified_path).name
            query_name = answer_name
        else:
            query_name = Path(modified_path).name
            answer_name = query_name
        query = locate(args.source_root, pr, "base_query", query_name)
        answer = locate(args.source_root, pr, "base_answer", answer_name)
        if query is None:
            raise FileNotFoundError(f"missing base query for PR {pr}")
        record: dict[str, object] = {
            "pr": pr,
            "title": meta["title"],
            "base_sha": meta["base"]["sha"],
            "head_sha": meta["head"]["sha"],
            "merge_commit_sha": meta["merge_commit_sha"],
            "modified_repository_path": modified_path,
            "changed_ids": labels,
            "query_file": query.name,
            "query_sha256": sha256(query),
            "query_bytes": query.stat().st_size,
            "answer_file": answer.name if answer else None,
            "answer_sha256": sha256(answer) if answer else None,
            "answer_bytes": answer.stat().st_size if answer else 0,
            "metadata_file": meta_path.name,
            "metadata_sha256": sha256(meta_path),
            "files_file": files_path.name,
            "files_sha256": sha256(files_path),
        }
        records.append(record)
        total_changed += len(labels)

    config = {
        "candidate": "Revision-Grounded Typed Contract Audit",
        "version": "v030",
        "phase": args.phase,
        "evaluation_prs": list(prs),
        "development_prs": list(DEVELOPMENT_PRS),
        "confirmation_prs": list(CONFIRMATION_PRS),
        "weights": {
            "schema_reference": 4.0,
            "path_dependency": 4.0,
            "unit_contract": 4.0,
            "calendar_contract": 4.0,
            "literal_provenance": 2.0,
            "identity_integrity": 4.0,
        },
        "bootstrap_seed": 130030,
        "bootstrap_resamples": 20000,
        "gates": (
            {
                "expected_prs": 8,
                "expected_changed_ids": 9,
                "minimum_mrr": 0.60,
                "minimum_recall_at_10": 8 / 9,
                "minimum_mrr_delta": 0.10,
                "minimum_bootstrap_lower": 0.0,
                "minimum_top10_prs": 6,
            }
            if args.phase == "development"
            else {
                "expected_prs": 6,
                "minimum_mrr": 0.45,
                "minimum_recall_at_10": 0.60,
                "minimum_mrr_delta": 0.05,
                "minimum_bootstrap_lower": 0.0,
                "minimum_top10_prs": 4,
            }
        ),
        "records": records,
        "total_changed_ids": total_changed,
        "source_root_sha_scope": "only files explicitly bound in records",
    }
    args.output.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
