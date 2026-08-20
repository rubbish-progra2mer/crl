from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


COMMIT = "b43164fbb2cd2963e1906a6fe62a86e7ce05973e"
FILES = {
    "README.md": (
        f"https://raw.githubusercontent.com/David-Li0406/ToolPRMBench/{COMMIT}/data/README.md"
    ),
    "prmbench_GTA.json": (
        f"https://raw.githubusercontent.com/David-Li0406/ToolPRMBench/{COMMIT}/data/prmbench_GTA.json"
    ),
    "prmbench_bfcl.json": (
        f"https://raw.githubusercontent.com/David-Li0406/ToolPRMBench/{COMMIT}/data/prmbench_bfcl.json"
    ),
    "prmbench_tooltalk.json": (
        f"https://raw.githubusercontent.com/David-Li0406/ToolPRMBench/{COMMIT}/data/prmbench_tooltalk.json"
    ),
    "toolprmbench_2601.12294v1.pdf": "https://arxiv.org/pdf/2601.12294v1",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parent
    records = []
    for name, url in FILES.items():
        destination = root / name
        if destination.exists():
            raise FileExistsError(destination)
        request = urllib.request.Request(url, headers={"User-Agent": "CRL-v034-main-codex"})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
            status = response.status
        destination.write_bytes(data)
        records.append(
            {
                "name": name,
                "url": url,
                "http_status": status,
                "bytes": len(data),
                "sha256": sha256(data),
            }
        )

    manifest = {
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": "https://github.com/David-Li0406/ToolPRMBench",
        "commit": COMMIT,
        "development_files": [
            "prmbench_GTA.json",
            "prmbench_bfcl.json",
            "prmbench_tooltalk.json",
        ],
        "conditional_confirmation_file": "prmbench_ToolSandbox.json",
        "confirmation_acquired": False,
        "records": records,
    }
    (root / "development_source_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
