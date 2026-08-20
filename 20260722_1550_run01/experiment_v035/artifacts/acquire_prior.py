from __future__ import annotations

import hashlib
import json
import shutil
import urllib.request
from pathlib import Path


SOURCES = {
    "prepair_2025_blackboxnlp_1_5.pdf": "https://aclanthology.org/2025.blackboxnlp-1.5.pdf",
    "pairwise_or_pointwise_2504.14716.pdf": "https://arxiv.org/pdf/2504.14716",
    "scope_2602.13110.pdf": "https://arxiv.org/pdf/2602.13110",
}

LOCAL_SOURCES = {
    "toolprmbench_2601.12294v1.pdf": Path(__file__).resolve().parents[1]
    / "sources_v034"
    / "toolprmbench_2601.12294v1.pdf",
    "toolrm_2510.26167v2.pdf": Path(__file__).resolve().parents[1]
    / "sources_v034"
    / "toolrm_2510.26167v2.pdf",
    "prmbench_GTA.json": Path(__file__).resolve().parents[1]
    / "sources_v034"
    / "prmbench_GTA.json",
    "prmbench_bfcl.json": Path(__file__).resolve().parents[1]
    / "sources_v034"
    / "prmbench_bfcl.json",
    "prmbench_tooltalk.json": Path(__file__).resolve().parents[1]
    / "sources_v034"
    / "prmbench_tooltalk.json",
    "model_manifest.json": Path(__file__).resolve().parents[1]
    / "sources_v034"
    / "model_manifest.json",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    target = Path(__file__).resolve().parent
    records = []
    for name, url in SOURCES.items():
        path = target / name
        request = urllib.request.Request(url, headers={"User-Agent": "CRL-v035/1.0"})
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
        path.write_bytes(payload)
        records.append(
            {
                "name": name,
                "url": url,
                "bytes": len(payload),
                "sha256": sha256(path),
            }
        )
    for name, source in LOCAL_SOURCES.items():
        path = target / name
        shutil.copyfile(source, path)
        records.append(
            {
                "name": name,
                "source_path": str(source),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = target / "prior_source_manifest.json"
    manifest.write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
