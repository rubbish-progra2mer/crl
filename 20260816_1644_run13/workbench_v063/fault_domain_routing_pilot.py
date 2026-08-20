from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V063_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
RESULT_PATH = Path(__file__).with_name(
    f"fault_domain_routing_{MODEL.replace(':', '_').replace('.', '_')}_r1.json"
)

DOMAINS = (
    "catalog",
    "schedule",
    "inventory",
    "registry",
    "directory",
    "telemetry",
    "archive",
    "pricing",
    "routing",
    "configuration",
    "allocation",
    "status",
)


def tool(name: str, description: str, item_key: str) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "required": [item_key],
                "properties": {item_key: {"type": "string"}},
            },
        },
    }


def build_pair(index: int, domain: str) -> dict[str, Any]:
    shared_a = f"service_group_{domain}_a"
    shared_b = f"service_group_{domain}_b"
    alpha = f"read_{domain}_alpha"
    beta = f"read_{domain}_beta"
    gamma = f"read_{domain}_gamma"
    item_key = f"{domain}_id"
    beta_desc = (
        f"Read the same {domain} record through adapter beta. Cost=1; latency=standard. "
        f"Dependency metadata: adapter=adapter_beta_{domain}; shared_service={shared_a}."
    )
    gamma_desc = (
        f"Read the same {domain} record through adapter gamma. Cost=3; latency=standard. "
        f"Dependency metadata: adapter=adapter_gamma_{domain}; shared_service={shared_b}."
    )
    tools_by_name = {
        beta: tool(beta, beta_desc, item_key),
        gamma: tool(gamma, gamma_desc, item_key),
    }
    order = (beta, gamma) if index % 2 == 0 else (gamma, beta)
    base = {
        "pair_id": f"{index + 1:02d}_{domain}",
        "domain": domain,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "shared_a": shared_a,
        "shared_b": shared_b,
        "tools": [tools_by_name[order[0]], tools_by_name[order[1]]],
        "item_key": item_key,
    }
    common = dict(base)
    common.update(
        {
            "fault_type": "common",
            "correct_tool": gamma,
            "failure": (
                f"Previous call {alpha}({item_key}='{domain}-17') returned "
                f"error_code=UPSTREAM_UNAVAILABLE; failed_component={shared_a}; "
                f"adapter=adapter_alpha_{domain}; adapter_status=healthy."
            ),
            "card": (
                "FAULT-DOMAIN CARD (mechanically compiled from the observed error and dependency metadata):\n"
                f"- fault_scope=SHARED_SERVICE; implicated={shared_a}\n"
                f"- {beta}: depends_on={shared_a}; conditional_availability=LOW; cost=1\n"
                f"- {gamma}: depends_on={shared_b}; conditional_availability=HIGH; cost=3\n"
                f"- best viable fallback={gamma}"
            ),
        }
    )
    local = dict(base)
    local.update(
        {
            "fault_type": "local",
            "correct_tool": beta,
            "failure": (
                f"Previous call {alpha}({item_key}='{domain}-17') returned "
                f"error_code=ADAPTER_PARSE_ERROR; failed_component=adapter_alpha_{domain}; "
                f"shared_service={shared_a}; shared_service_status=healthy."
            ),
            "card": (
                "FAULT-DOMAIN CARD (mechanically compiled from the observed error and dependency metadata):\n"
                f"- fault_scope=LOCAL_ADAPTER; implicated=adapter_alpha_{domain}; {shared_a}=HEALTHY\n"
                f"- {beta}: adapter is independent of failed adapter; depends_on={shared_a}; conditional_availability=HIGH; cost=1\n"
                f"- {gamma}: depends_on={shared_b}; conditional_availability=HIGH; cost=3\n"
                f"- best viable fallback={beta}"
            ),
        }
    )
    return {"common": common, "local": local}


PAIRS = [build_pair(index, domain) for index, domain in enumerate(DOMAINS)]


def chat(task: dict[str, Any], mode: str) -> dict[str, Any]:
    system = (
        "Choose and call exactly one fallback tool that is most likely to return the requested record. "
        "Use the observed failure, tool dependency metadata, cost, and latency. Do not call the failed alpha tool."
    )
    if mode == "principle":
        system += (
            " Distinguish local adapter failures from shared-service failures: avoid an uncalled fallback that depends "
            "on an implicated shared service, but when the shared service is explicitly healthy prefer the lower-cost "
            "viable adapter."
        )
    elif mode == "domain_card":
        system += "\n\n" + task["card"]
    user = (
        f"Retrieve {task['domain']} record {task['domain']}-17 using one fallback now.\n"
        f"{task['failure']}"
    )
    payload = {
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0, "seed": 63, "num_predict": 512},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "tools": task["tools"],
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))
    result["client_elapsed_seconds"] = time.perf_counter() - started
    return result


def selected_tool(response: dict[str, Any]) -> str | None:
    calls = response.get("message", {}).get("tool_calls") or []
    if not calls:
        return None
    name = calls[0].get("function", {}).get("name")
    return name if isinstance(name, str) else None


def summarize(rows: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    common = [row for row in rows if row["fault_type"] == "common"]
    local = [row for row in rows if row["fault_type"] == "local"]
    by_pair: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_pair.setdefault(row["pair_id"], []).append(row)
    paired = sum(
        len(group) == 2 and all(item[mode]["correct"] for item in group)
        for group in by_pair.values()
    )
    return {
        "n": len(rows),
        "paired_n": len(by_pair),
        "paired_correct": paired,
        "common_correct": sum(row[mode]["correct"] for row in common),
        "local_correct": sum(row[mode]["correct"] for row in local),
        "no_call": sum(row[mode]["selected_tool"] is None for row in rows),
        "prompt_tokens": sum(row[mode]["prompt_tokens"] for row in rows),
        "output_tokens": sum(row[mode]["output_tokens"] for row in rows),
        "elapsed_seconds": sum(row[mode]["elapsed_seconds"] for row in rows),
    }


def main() -> None:
    rows: list[dict[str, Any]] = []
    for pair in PAIRS:
        for fault_type in ("common", "local"):
            task = pair[fault_type]
            row: dict[str, Any] = {
                "pair_id": task["pair_id"],
                "fault_type": fault_type,
                "correct_tool": task["correct_tool"],
                "tool_order": [item["function"]["name"] for item in task["tools"]],
            }
            for mode in ("raw", "principle", "domain_card"):
                response = chat(task, mode)
                choice = selected_tool(response)
                row[mode] = {
                    "selected_tool": choice,
                    "correct": choice == task["correct_tool"],
                    "content": response.get("message", {}).get("content", ""),
                    "prompt_tokens": int(response.get("prompt_eval_count", 0)),
                    "output_tokens": int(response.get("eval_count", 0)),
                    "elapsed_seconds": float(response.get("client_elapsed_seconds", 0.0)),
                }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "pair_id": task["pair_id"],
                        "fault_type": fault_type,
                        "correct_tool": task["correct_tool"],
                        "selected": {mode: row[mode]["selected_tool"] for mode in ("raw", "principle", "domain_card")},
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    result = {
        "model": MODEL,
        "endpoint": ENDPOINT,
        "temperature": 0,
        "seed": 63,
        "pair_count": len(PAIRS),
        "task_count": len(rows),
        "summary": {mode: summarize(rows, mode) for mode in ("raw", "principle", "domain_card")},
        "rows": rows,
        "scope_note": "Synthetic benign fallback selection only. No represented fallback tool was executed.",
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
