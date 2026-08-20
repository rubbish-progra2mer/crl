from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import urllib.request
from pathlib import Path
from typing import Any


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def parse_jsonl(value: bytes) -> list[dict[str, Any]]:
    text = value.decode("utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    source = config["confirmation_source"]
    commit = str(source["commit"])
    repository = str(source["repository"])
    base = f"https://raw.githubusercontent.com/{repository}/{commit}/"
    question_url = base + str(source["questions_path"])
    gold_url = base + str(source["gold_path"])
    args.output_dir.mkdir(parents=True, exist_ok=False)
    with urllib.request.urlopen(question_url, timeout=120) as response:
        question_bytes = response.read()
    with urllib.request.urlopen(gold_url, timeout=120) as response:
        gold_bytes = response.read()
    questions = parse_jsonl(question_bytes)
    gold = parse_jsonl(gold_bytes)
    question_ids = [str(row["id"]) for row in questions]
    gold_ids = [str(row["id"]) for row in gold]
    if len(question_ids) != len(set(question_ids)) or len(gold_ids) != len(set(gold_ids)):
        raise ValueError("duplicate Confirmation query IDs")
    if set(question_ids) != set(gold_ids):
        raise ValueError("Confirmation query/gold ID sets differ")
    question_path = args.output_dir / "BFCL_v4_live_multiple.json"
    gold_path = args.output_dir / "BFCL_v4_live_multiple_possible_answer.json"
    question_path.write_bytes(question_bytes)
    gold_path.write_bytes(gold_bytes)
    manifest = {
        "schema_version": 1,
        "phase": "confirmation",
        "repository": repository,
        "commit": commit,
        "questions_path": source["questions_path"],
        "gold_path": source["gold_path"],
        "questions_url": question_url,
        "gold_url": gold_url,
        "questions_bytes": len(question_bytes),
        "gold_bytes": len(gold_bytes),
        "questions_sha256": sha256_bytes(question_bytes),
        "gold_sha256": sha256_bytes(gold_bytes),
        "queries": len(questions),
        "config_sha256": sha256_path(args.config),
        "python_executable": sys.executable,
        "python": platform.python_version(),
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "phase": "confirmation",
                "queries": len(questions),
                "questions_sha256": manifest["questions_sha256"],
                "gold_sha256": manifest["gold_sha256"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
