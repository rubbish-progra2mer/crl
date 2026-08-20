from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.data.exists() or args.manifest.exists():
        raise FileExistsError("confirmation output already exists")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if config["experiment_id"] != "v035":
        raise ValueError("wrong experiment")
    commit = config["repository_commit"]
    file_name = config["conditional_confirmation"]["file_name"]
    url = (
        "https://raw.githubusercontent.com/David-Li0406/ToolPRMBench/"
        f"{commit}/data/{file_name}"
    )
    request = Request(url, headers={"User-Agent": "CRL-v035-confirmation-acquisition"})
    with urlopen(request, timeout=120) as response:
        data = response.read()
        status = response.status
    parsed = json.loads(data.decode("utf-8"))
    expected_rows = config["conditional_confirmation"]["rows"]
    if status != 200 or not isinstance(parsed, list) or len(parsed) != expected_rows:
        raise ValueError("unexpected confirmation response")
    args.data.write_bytes(data)
    manifest = {
        "acquired_at_utc": datetime.now(UTC).isoformat(),
        "commit": commit,
        "file_name": file_name,
        "url": url,
        "http_status": status,
        "rows": len(parsed),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    args.manifest.write_bytes(
        (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
