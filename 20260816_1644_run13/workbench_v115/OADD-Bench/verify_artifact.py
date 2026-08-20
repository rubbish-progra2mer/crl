#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def codes(value: str) -> set[str]:
    return {item.strip().upper() for item in value.split(";") if item.strip()}


def main() -> None:
    benchmark_path = ROOT / "benchmark" / "OADD-Bench" / "OADD_Bench.csv"
    evidence_path = (
        ROOT / "benchmark" / "OADD-Bench" / "OADD_Bench_evidence.jsonl"
    )
    with benchmark_path.open(newline="", encoding="utf-8") as handle:
        benchmark = list(csv.DictReader(handle))
    evidence = [
        json.loads(line)
        for line in evidence_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(benchmark) != 160 or len(evidence) != 160:
        raise RuntimeError(
            f"Expected 160 benchmark and evidence rows; found {len(benchmark)} and {len(evidence)}"
        )
    benchmark_by_id = {row["record_id"]: row for row in benchmark}
    evidence_by_id = {row["question_id"]: row for row in evidence}
    if set(benchmark_by_id) != set(evidence_by_id):
        raise RuntimeError("Benchmark and evidence record IDs differ")
    for record_id, row in benchmark_by_id.items():
        ledger = evidence_by_id[record_id]
        ledger_codes = {
            str(code).strip().upper()
            for values in ledger["final_column_ids"].values()
            for code in values
        }
        if codes(row["hrs_column_ids"]) != ledger_codes:
            raise RuntimeError(f"Evidence coverage mismatch for {record_id}")
        if not ledger["construction_evidence"]["all_final_columns_accounted_for"]:
            raise RuntimeError(f"Incomplete evidence for {record_id}")
    label_count = sum(len(codes(row["hrs_column_ids"])) for row in benchmark)
    if label_count != 4682:
        raise RuntimeError(f"Expected 4,682 labels; found {label_count:,}")

    raw_manifest = json.loads(
        (ROOT / "benchmark" / "HRS_metadata" / "raw_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    raw_files = list(
        (ROOT / "benchmark" / "HRS_metadata" / "raw_codebooks").glob("*.html")
    )
    if raw_manifest["product_count"] != 169 or len(raw_files) != 2026:
        raise RuntimeError(
            "Raw codebook release does not match its 169-product/2,026-file manifest"
        )
    print(
        json.dumps(
            {
                "questions": len(benchmark),
                "labels": label_count,
                "evidence_rows": len(evidence),
                "hrs_products": raw_manifest["product_count"],
                "raw_codebook_files": len(raw_files),
                "status": "ok",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
