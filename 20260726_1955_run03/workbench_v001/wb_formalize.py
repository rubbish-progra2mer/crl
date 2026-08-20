"""Workbench v001: call DeepSeek to produce the constraint-encoding function.

Secrets: the API key is read ONLY from the process environment variable
DEEPSEEK_API_KEY and never printed; all exception text is passed through
`redact` before reaching stdout/stderr.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import httpx

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
KEY_PATTERN = re.compile(r"sk-[A-Za-z0-9]{8,}")


def redact(text: str) -> str:
    return KEY_PATTERN.sub("[REDACTED_KEY]", text)


def extract_code(content: str) -> str | None:
    match = re.search(r"```(?:python)?\s*\n(.*?)```", content, re.DOTALL)
    if match:
        return match.group(1)
    if "def add_constraints" in content:
        lines = [
            line for line in content.splitlines() if not line.strip().startswith("```")
        ]
        return "\n".join(lines)
    return None


def call_deepseek(messages: list[dict], *, raw_log: Path, request_id: str,
                  max_tokens: int = 4000, temperature: float = 0.0,
                  retries: int = 4) -> dict:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY not present in process environment")
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    last_error = "unknown"
    for attempt in range(retries):
        try:
            response = httpx.post(
                API_URL,
                json=payload,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=300.0,
            )
            if response.status_code == 200:
                body = response.json()
                record = {
                    "request_id": request_id,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "endpoint": API_URL,
                    "requested_model": MODEL,
                    "response_model": body.get("model"),
                    "usage": body.get("usage"),
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "attempt": attempt,
                    "body": body,
                }
                with open(raw_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                return body
            last_error = f"http {response.status_code}: {redact(response.text[:400])}"
        except Exception as error:  # noqa: BLE001 - transport errors retried
            last_error = redact(f"{type(error).__name__}: {error}")
        time.sleep(2 ** attempt)
    raise RuntimeError(f"deepseek call failed after {retries} attempts: {last_error}")


def formalize(query: str, out_dir: Path, raw_log: Path, request_id: str) -> dict:
    from wb_prompt import build_prompt

    messages = build_prompt(query)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "prompt.json").write_text(
        json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    body = call_deepseek(messages, raw_log=raw_log, request_id=request_id)
    content = body["choices"][0]["message"]["content"]
    code = extract_code(content)
    status = "ok" if code else "no_code_block"
    if code:
        (out_dir / "generated_code.py").write_text(code, encoding="utf-8")
    (out_dir / "response_content.md").write_text(content, encoding="utf-8")
    return {
        "status": status,
        "response_model": body.get("model"),
        "usage": body.get("usage"),
    }


if __name__ == "__main__":
    query_path, out_dir, raw_log, request_id = sys.argv[1:5]
    query_text = Path(query_path).read_text(encoding="utf-8")
    result = formalize(query_text, Path(out_dir), Path(raw_log), request_id)
    print(json.dumps(result, ensure_ascii=False))
