from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


FILES = {
    "rrd_2602.05125v1.pdf": "https://arxiv.org/pdf/2602.05125v1",
    "toolrm_2510.26167v2.pdf": "https://arxiv.org/pdf/2510.26167v2",
    "tool_verifier_2026_findings_acl_1647.pdf": (
        "https://aclanthology.org/2026.findings-acl.1647.pdf"
    ),
}


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
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )

    manifest = {
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "v034 nearest-prior direct reading",
        "records": records,
    }
    (root / "prior_source_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
