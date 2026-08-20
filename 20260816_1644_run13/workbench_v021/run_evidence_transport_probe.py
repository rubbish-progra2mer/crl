import argparse
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


ALLOWED_PERMISSIONS = {"allowed", "blocked"}
POLICY_TO_PERMISSION = {
    "continue": "allowed",
    "show_progress": "allowed",
    "ask_clarification": "blocked",
    "request_approval": "blocked",
    "escalate": "blocked",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3:4b")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--timeout", type=float, default=180.0)
    return parser.parse_args()


def atomic_write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temp_name = handle.name
    os.replace(temp_name, path)


def extract_json_object(text):
    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return None
    try:
        value = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def permission_from_response(text):
    parsed = extract_json_object(text)
    if parsed is None:
        return None, None
    permission = parsed.get("commit_permission")
    if permission in ALLOWED_PERMISSIONS:
        return permission, parsed
    action = parsed.get("policy_action")
    return POLICY_TO_PERMISSION.get(action), parsed


def call_ollama(base_url, model, system_prompt, scenario_id, model_input, timeout):
    body = {
        "model": model,
        "stream": False,
        "think": False,
        "format": "json",
        "keep_alive": "30m",
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"scenario_id: {scenario_id}\n\n{model_input}",
            },
        ],
        "options": {
            "temperature": 0,
            "seed": 20260816,
            "num_ctx": 8192,
            "num_predict": 384,
        },
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/chat",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "status": "infrastructure_error",
            "error": f"{type(exc).__name__}: {exc}",
            "elapsed_seconds": time.perf_counter() - started,
        }

    text = payload.get("message", {}).get("content", "")
    permission, parsed = permission_from_response(text)
    return {
        "status": "ok" if permission is not None else "parse_error",
        "permission": permission,
        "parsed": parsed,
        "response_text": text,
        "elapsed_seconds": time.perf_counter() - started,
        "prompt_eval_count": payload.get("prompt_eval_count"),
        "eval_count": payload.get("eval_count"),
    }


def main():
    args = parse_args()
    inputs = json.loads(args.inputs.read_text(encoding="utf-8"))
    artifact = {
        "schema_version": "crl.evidence_transport_probe_results.v1",
        "model": args.model,
        "temperature": 0,
        "seed": 20260816,
        "source_inputs": str(args.inputs.resolve()),
        "results": [],
    }

    if args.output.exists():
        artifact = json.loads(args.output.read_text(encoding="utf-8"))
    completed = {
        (row["scenario_id"], row["condition"])
        for row in artifact.get("results", [])
        if row.get("status") in {"ok", "parse_error"}
    }

    total = len(inputs["cases"]) * 2
    for case in inputs["cases"]:
        for condition, field in (
            ("canonical", "canonical_input"),
            ("payload_preserving", "payload_preserving_input"),
        ):
            key = (case["id"], condition)
            if key in completed:
                continue
            result = call_ollama(
                args.base_url,
                args.model,
                inputs["system_prompt"],
                case["id"],
                case[field],
                args.timeout,
            )
            row = {
                "scenario_id": case["id"],
                "condition": condition,
                "expected_permission": case["expected_permission"],
                "taxonomy_direction": case["taxonomy_direction"],
                **result,
            }
            artifact["results"].append(row)
            atomic_write_json(args.output, artifact)
            print(
                f"[{len(artifact['results'])}/{total}] {case['id']} "
                f"{condition}: {row.get('permission')} ({row['status']})",
                flush=True,
            )


if __name__ == "__main__":
    main()
