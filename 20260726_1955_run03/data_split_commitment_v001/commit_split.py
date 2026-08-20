"""Commit-reveal data split for run03 (v001).

Downloads the TravelPlanner validation split (queries CSV + sole-planning
reference info JSONL) from the HuggingFace dataset repo, then deterministically
partitions rows into three PHYSICALLY SEPARATE bucket files before any
instance content or outcome is read by the research flow:

    bucket(i) = int(sha256(f"run03_tp_val_{i:03d}").hexdigest(), 16) % 5
    {0, 1} -> W  (WORKBENCH)
    {2, 3} -> D  (PROMOTION_DEVELOPMENT)
    {4}    -> C  (CONFIRMATION, reserved untouched)

i is the 0-based data-row index in the original validation.csv row order
(header excluded). The JSONL is split by the same line index under the
assumption of aligned ordering; alignment is verified later using W rows only.

This script is mechanical: it never parses instance semantics, never prints
row contents, and evaluates no outcome. Receivers can re-run it to verify the
split. Outputs and their SHA-256 go to MANIFEST.json in this directory.
"""

import csv
import hashlib
import io
import json
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download

COMMIT_DIR = Path(__file__).resolve().parent
REPO = "osunlp/TravelPlanner"
CSV_NAME = "validation.csv"
JSONL_NAME = "validation_ref_info.jsonl"
SALT = "run03_tp_val"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bucket_of(index: int) -> str:
    digest = hashlib.sha256(f"{SALT}_{index:03d}".encode("utf-8")).hexdigest()
    value = int(digest, 16) % 5
    if value in (0, 1):
        return "W"
    if value in (2, 3):
        return "D"
    return "C"


def main() -> int:
    csv_path = Path(
        hf_hub_download(REPO, CSV_NAME, repo_type="dataset", revision="main")
    )
    jsonl_path = Path(
        hf_hub_download(REPO, JSONL_NAME, repo_type="dataset", revision="main")
    )

    raw_csv = csv_path.read_bytes()
    raw_jsonl = jsonl_path.read_bytes()

    (COMMIT_DIR / "raw_validation.csv").write_bytes(raw_csv)
    (COMMIT_DIR / "raw_validation_ref_info.jsonl").write_bytes(raw_jsonl)

    # Mechanical row split (csv module handles embedded newlines; contents
    # are passed through untouched and never inspected).
    text_stream = io.StringIO(raw_csv.decode("utf-8"))
    reader = csv.reader(text_stream)
    rows = list(reader)
    header, data_rows = rows[0], rows[1:]

    jsonl_lines = raw_jsonl.decode("utf-8").splitlines()

    if len(data_rows) != len(jsonl_lines):
        print(
            json.dumps(
                {
                    "error": "row count mismatch",
                    "csv_rows": len(data_rows),
                    "jsonl_lines": len(jsonl_lines),
                }
            )
        )
        return 1

    assignments: dict[str, list[int]] = {"W": [], "D": [], "C": []}
    for index in range(len(data_rows)):
        assignments[bucket_of(index)].append(index)

    outputs: dict[str, str] = {}
    for bucket_name in ("W", "D", "C"):
        indices = assignments[bucket_name]

        out_csv = COMMIT_DIR / f"bucket_{bucket_name}.csv"
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["orig_index"] + header)
        for i in indices:
            writer.writerow([str(i)] + data_rows[i])
        out_csv.write_text(buffer.getvalue(), encoding="utf-8", newline="")

        out_jsonl = COMMIT_DIR / f"bucket_{bucket_name}_ref_info.jsonl"
        lines = [
            json.dumps({"orig_index": i, "raw": jsonl_lines[i]}, ensure_ascii=False)
            for i in indices
        ]
        out_jsonl.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")

        outputs[out_csv.name] = sha256_bytes(out_csv.read_bytes())
        outputs[out_jsonl.name] = sha256_bytes(out_jsonl.read_bytes())

    manifest = {
        "commit_rule": (
            f"bucket(i) = int(sha256('{SALT}_' + format(i, '03d')).hexdigest(), 16) % 5; "
            "{0,1}=W (WORKBENCH), {2,3}=D (PROMOTION_DEVELOPMENT), {4}=C (CONFIRMATION reserved untouched); "
            "i = 0-based data-row index of original validation.csv"
        ),
        "source_repo": REPO,
        "source_files": {
            "validation.csv": sha256_bytes(raw_csv),
            "validation_ref_info.jsonl": sha256_bytes(raw_jsonl),
        },
        "row_count": len(data_rows),
        "bucket_sizes": {k: len(v) for k, v in assignments.items()},
        "bucket_indices": assignments,
        "bucket_files": outputs,
        "committed_before_any_instance_content_or_outcome_was_read": True,
        "script_sha256_self": None,
    }
    manifest["script_sha256_self"] = sha256_bytes(
        (COMMIT_DIR / "commit_split.py").read_bytes()
    )
    manifest_path = COMMIT_DIR / "MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
                "bucket_sizes": manifest["bucket_sizes"],
                "row_count": len(data_rows),
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
