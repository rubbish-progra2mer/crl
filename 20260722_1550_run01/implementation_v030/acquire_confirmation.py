from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path


CONFIRMATION_PRS = (1084, 1085, 1086, 1087, 1175, 1177)
API = "https://api.github.com/repos/ShishirPatil/gorilla"


def download(url: str, path: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "CRL-commissioning-main-codex",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        path.write_bytes(response.read())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir()
    for pr in CONFIRMATION_PRS:
        meta_path = args.output_dir / f"pr_{pr}_meta.json"
        files_path = args.output_dir / f"pr_{pr}_files.json"
        download(f"{API}/pulls/{pr}", meta_path)
        download(f"{API}/pulls/{pr}/files?per_page=100", files_path)
        meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
        files = json.loads(files_path.read_text(encoding="utf-8-sig"))
        if not meta["merged"]:
            raise ValueError(f"PR {pr} is not merged")
        for item in files:
            repository_path = str(item["filename"])
            if "/data/" not in repository_path or "CHANGELOG" in repository_path:
                continue
            if "/possible_answer/" in repository_path:
                query_path = repository_path.replace("/possible_answer/", "/")
                answer_path = repository_path
            else:
                query_path = repository_path
                answer_path = repository_path.replace("/data/", "/data/possible_answer/")
            for tag, ref, path in (
                ("base_query", meta["base"]["sha"], query_path),
                ("head_query", meta["head"]["sha"], query_path),
                ("base_answer", meta["base"]["sha"], answer_path),
                ("head_answer", meta["head"]["sha"], answer_path),
            ):
                url = f"https://raw.githubusercontent.com/ShishirPatil/gorilla/{ref}/{path}"
                output = args.output_dir / f"pr_{pr}_{tag}_{Path(path).name}"
                try:
                    download(url, output)
                except urllib.error.HTTPError as exc:
                    if exc.code != 404:
                        raise
                    (args.output_dir / f"pr_{pr}_{tag}_HTTP_404.json").write_text(
                        json.dumps({"url": url, "status": 404}, indent=2) + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
