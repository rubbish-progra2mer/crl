from __future__ import annotations

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


QUERY = "cat:cs.AI OR cat:cs.CL"
MAX_RESULTS = 800
URL = (
    "https://export.arxiv.org/api/query?"
    + urllib.parse.urlencode(
        {
            "search_query": QUERY,
            "start": 0,
            "max_results": MAX_RESULTS,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
)


def clean(text: str | None) -> str:
    return " ".join((text or "").split())


def main() -> None:
    request = urllib.request.Request(URL, headers={"User-Agent": "CRL-research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    root = ET.fromstring(payload)
    atom = {"a": "http://www.w3.org/2005/Atom"}
    entries = []
    for entry in root.findall("a:entry", atom):
        entries.append(
            {
                "id": clean(entry.findtext("a:id", namespaces=atom)),
                "published": clean(entry.findtext("a:published", namespaces=atom)),
                "updated": clean(entry.findtext("a:updated", namespaces=atom)),
                "title": clean(entry.findtext("a:title", namespaces=atom)),
                "summary": clean(entry.findtext("a:summary", namespaces=atom)),
                "authors": [clean(a.findtext("a:name", namespaces=atom)) for a in entry.findall("a:author", atom)],
                "categories": [c.attrib.get("term") for c in entry.findall("a:category", atom)],
            }
        )
    out = Path(__file__).with_name("latest_arxiv_800.json")
    out.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"url": URL, "count": len(entries), "first": entries[0]["id"] if entries else None}))


if __name__ == "__main__":
    main()
