from __future__ import annotations

import argparse
import re
import sys

import pymupdf


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("pattern")
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--before", type=int, default=450)
    parser.add_argument("--after", type=int, default=800)
    args = parser.parse_args()

    pattern = re.compile(args.pattern, re.IGNORECASE)
    shown = 0
    with pymupdf.open(args.pdf) as document:
        for page_number, page in enumerate(document, start=1):
            text = " ".join(page.get_text("text", sort=True).split())
            for match in pattern.finditer(text):
                start = max(0, match.start() - args.before)
                end = min(len(text), match.end() + args.after)
                print(f"[page {page_number}] {text[start:end]}\n")
                shown += 1
                if shown >= args.limit:
                    return


if __name__ == "__main__":
    main()
