#!/usr/bin/env python3
"""Audit a direct operational-semantics pair judge on PolarityCheck factorial pairs."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SYSTEM = """You are a strict operational-semantics judge. Compare a reference policy and a candidate policy. Answer SAME only if required, prohibited, and permitted actions, conditions, scope, exceptions, modality, quantities or units, ordering, and timing all agree. Otherwise answer DIFFERENT. Do not use wording similarity as the criterion.
Return only: {\"decision\":\"SAME\" or \"DIFFERENT\",\"reason\":\"brief concrete reason\"}"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def atomic_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(temporary, path)


def call(url: str, model: str, text_a: str, text_b: str) -> dict[str, Any]:
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "format": "json",
        "keep_alive": "30m",
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": "REFERENCE POLICY:\n" + text_a + "\n\nCANDIDATE POLICY:\n" + text_b},
        ],
        "options": {"temperature": 0, "seed": 20260816, "num_ctx": 4096, "num_predict": 300},
    }
    request = urllib.request.Request(
        url.rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
        raw = body.get("message", {}).get("content", "")
        parsed = json.loads(raw)
        decision = parsed.get("decision")
        if isinstance(decision, str):
            decision = decision.strip().upper()
        return {
            "ok": decision in {"SAME", "DIFFERENT"},
            "decision": decision,
            "parsed": parsed,
            "raw": raw,
            "wall_seconds": round(time.perf_counter() - started, 4),
            "prompt_eval_count": body.get("prompt_eval_count"),
            "eval_count": body.get("eval_count"),
        }
    except Exception as error:
        return {"ok": False, "error": f"{type(error).__name__}: {error}", "wall_seconds": round(time.perf_counter() - started, 4)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--url", default="http://127.0.0.1:11434")
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.corpus.read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.output.exists():
        result = json.loads(args.output.read_text(encoding="utf-8"))
    else:
        result = {"schema_version": 1, "model": args.model, "created_at_utc": utc_now(), "rows": []}
    completed = {row["id"] for row in result["rows"]}
    for index, row in enumerate(rows, start=1):
        if row["id"] in completed:
            continue
        print(f"[{index}/{len(rows)}] {row['id']}", flush=True)
        response = call(args.url, args.model, row["text_a"], row["text_b"])
        gold = "DIFFERENT" if row["decision"] == "VIOLATION" else "SAME"
        result["rows"].append({
            "id": row["id"],
            "cell": row["cell"],
            "subclass": row["subclass"],
            "lexical": row["lexical"],
            "gold": gold,
            "response": response,
        })
        result["updated_at_utc"] = utc_now()
        atomic_write(args.output, result)
    print(f"completed={len(result['rows'])}", flush=True)


if __name__ == "__main__":
    main()
