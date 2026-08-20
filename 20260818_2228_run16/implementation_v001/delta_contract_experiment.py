from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CONDITIONS = ("latest", "diff_prompt", "reflection", "obligation")


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    family: str
    task: str
    old_plan: tuple[dict[str, Any], ...]
    new_tools: tuple[dict[str, Any], ...]
    diff: tuple[str, ...]
    expected_plan: tuple[dict[str, Any], ...]
    near_miss: tuple[dict[str, Any], ...]
    affected_index: int = 0


def tool(name: str, description: str, required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "input_schema": {"type": "object", "required": required, "properties": properties},
    }


def step(name: str, **arguments: str) -> dict[str, Any]:
    return {"tool": name, "arguments": arguments}


def build_scenarios() -> list[Scenario]:
    scenarios: list[Scenario] = []
    rename_rows = [
        ("mail", "给 alice@example.com 发送内容为 budget-ready 的邮件", "alice@example.com", "budget-ready"),
        ("sms", "给 +8613800000000 发送短信 code-731", "+8613800000000", "code-731"),
        ("ticket", "为用户 u-17 创建主题 login-failed 的工单", "u-17", "login-failed"),
        ("note", "在项目 p-9 写入备注 review-tomorrow", "p-9", "review-tomorrow"),
    ]
    for prefix, task_text, target, payload in rename_rows:
        old_name = f"{prefix}_send"
        new_name = old_name
        new_tool = tool(
            new_name,
            "Send one payload to one target.",
            ["destination", "content"],
            {"destination": {"type": "string"}, "content": {"type": "string"}},
        )
        expected = (step(new_name, destination=target, content=payload),)
        scenarios.append(
            Scenario(
                f"rename-{prefix}",
                "parameter_rename",
                task_text,
                (step(old_name, recipient=target, body=payload),),
                (new_tool,),
                ("recipient renamed to destination", "body renamed to content"),
                expected,
                (step(new_name, destination=payload, content=target),),
            )
        )

    required_rows = [
        ("trip", "预订 2026-09-03 从 Beijing 到 Shanghai 的行程", "Beijing", "Shanghai", "2026-09-03"),
        ("meeting", "为 team-red 安排 2026-09-04 的会议", "team-red", "planning", "2026-09-04"),
        ("report", "为 sales 生成截至 2026-08-31 的 monthly 报告", "sales", "monthly", "2026-08-31"),
        ("shipment", "从 WH-2 向 C-11 发货，日期 2026-09-05", "WH-2", "C-11", "2026-09-05"),
    ]
    for prefix, task_text, first, second, date in required_rows:
        name = f"{prefix}_create"
        new_tool = tool(
            name,
            "Create the requested object on an explicit effective date.",
            ["source", "target", "effective_date"],
            {
                "source": {"type": "string"},
                "target": {"type": "string"},
                "effective_date": {"type": "string"},
            },
        )
        expected = (step(name, source=first, target=second, effective_date=date),)
        scenarios.append(
            Scenario(
                f"required-{prefix}",
                "required_parameter",
                task_text,
                (step(name, source=first, target=second),),
                (new_tool,),
                ("effective_date is newly required and must be copied from the task date",),
                expected,
                (step(name, source=first, target=second, effective_date="2026-01-01"),),
            )
        )

    enum_rows = [
        ("incident", "把事件 INC-8 标记为 urgent", "INC-8"),
        ("case", "把案件 CASE-4 标记为 urgent", "CASE-4"),
        ("alert", "把告警 ALT-3 标记为 urgent", "ALT-3"),
        ("request", "把请求 REQ-6 标记为 urgent", "REQ-6"),
    ]
    for prefix, task_text, item_id in enum_rows:
        name = f"{prefix}_prioritize"
        new_tool = tool(
            name,
            "Set priority. P1 is the replacement for legacy urgent; P2 replaces normal.",
            ["item_id", "priority"],
            {
                "item_id": {"type": "string"},
                "priority": {"type": "string", "enum": ["P1", "P2"]},
            },
        )
        expected = (step(name, item_id=item_id, priority="P1"),)
        scenarios.append(
            Scenario(
                f"enum-{prefix}",
                "enum_semantics",
                task_text,
                (step(name, item_id=item_id, priority="urgent"),),
                (new_tool,),
                ("legacy urgent maps to P1; legacy normal maps to P2",),
                expected,
                (step(name, item_id=item_id, priority="P2"),),
            )
        )

    replace_rows = [
        ("customer", "用 alice@example.com 解析客户账户", "alice@example.com"),
        ("device", "用 SN-44 解析设备实体", "SN-44"),
        ("paper", "用 doi:10.1/x 解析论文记录", "doi:10.1/x"),
        ("order", "用 ORD-81 解析订单对象", "ORD-81"),
    ]
    for prefix, task_text, key in replace_rows:
        old_name = f"lookup_{prefix}"
        new_name = f"resolve_{prefix}"
        fallback = f"search_{prefix}s"
        tools = (
            tool(new_name, f"Exact replacement for {old_name}; resolve one stable key.", ["stable_key"], {"stable_key": {"type": "string"}}),
            tool(fallback, "Fuzzy search; not an exact resolver.", ["query"], {"query": {"type": "string"}}),
        )
        expected = (step(new_name, stable_key=key),)
        scenarios.append(
            Scenario(
                f"replace-{prefix}",
                "tool_replacement",
                task_text,
                (step(old_name, key=key),),
                tools,
                (f"{old_name} removed and exactly replaced by {new_name}", "key renamed to stable_key"),
                expected,
                (step(fallback, query=key),),
            )
        )

    prereq_rows = [
        ("invoice", "提交客户 C-7 金额 91 的发票", "C-7", "91"),
        ("refund", "提交订单 O-3 金额 42 的退款", "O-3", "42"),
        ("transfer", "提交账户 A-5 金额 13 的转账", "A-5", "13"),
        ("deployment", "提交服务 S-2 版本 4.1 的部署", "S-2", "4.1"),
    ]
    for prefix, task_text, entity, value in prereq_rows:
        authorize = f"authorize_{prefix}"
        submit = f"submit_{prefix}"
        value_key = "version" if prefix == "deployment" else "amount"
        tools = (
            tool(authorize, "Authorize this exact operation and return authorization_token.", ["entity", value_key], {"entity": {"type": "string"}, value_key: {"type": "string"}}),
            tool(submit, "Submit only with token returned by authorize step for same entity and value.", ["entity", value_key, "authorization_token"], {"entity": {"type": "string"}, value_key: {"type": "string"}, "authorization_token": {"type": "string"}}),
        )
        auth_args = {"entity": entity, value_key: value}
        submit_args = {"entity": entity, value_key: value, "authorization_token": "$step1.authorization_token"}
        expected = (step(authorize, **auth_args), step(submit, **submit_args))
        scenarios.append(
            Scenario(
                f"prerequisite-{prefix}",
                "new_prerequisite",
                task_text,
                (step(submit, **{"entity": entity, value_key: value}),),
                tools,
                (f"{submit} now requires authorization_token produced by {authorize} for the same entity and {value_key}",),
                expected,
                (step(submit, **{"entity": entity, value_key: value, "authorization_token": "STATIC-TOKEN"}),),
            )
        )

    description_rows = [
        ("record", "软归档记录 R-8，必须可恢复", "R-8"),
        ("project", "软归档项目 P-4，必须可恢复", "P-4"),
        ("thread", "软归档会话 T-2，必须可恢复", "T-2"),
        ("dataset", "软归档数据集 D-6，必须可恢复", "D-6"),
    ]
    for prefix, task_text, item_id in description_rows:
        old_name = f"archive_{prefix}"
        soft_name = f"soft_archive_{prefix}"
        tools = (
            tool(old_name, "Permanently delete; irreversible. Do not use for recoverable archive.", ["id"], {"id": {"type": "string"}}),
            tool(soft_name, "Recoverable soft archive; preserves restore capability.", ["id"], {"id": {"type": "string"}}),
        )
        expected = (step(soft_name, id=item_id),)
        scenarios.append(
            Scenario(
                f"description-{prefix}",
                "description_semantics",
                task_text,
                (step(old_name, id=item_id),),
                tools,
                (f"{old_name} changed from recoverable archive to irreversible deletion", f"new {soft_name} provides legacy recoverable behavior"),
                expected,
                (step(old_name, id=item_id),),
            )
        )
    return scenarios


def call_model(endpoint: str, model: str, messages: list[dict[str, str]], seed: int, timeout: float) -> tuple[str, dict[str, int]]:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {"temperature": 0, "seed": seed, "num_ctx": 6144},
    }
    request = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = json.loads(response.read().decode("utf-8"))
    message = raw.get("message")
    if not isinstance(message, dict):
        raise ValueError("model response lacks message")
    return str(message.get("content", "")), {"prompt": int(raw.get("prompt_eval_count", 0) or 0), "completion": int(raw.get("eval_count", 0) or 0)}


def parse_object(content: str) -> dict[str, Any]:
    try:
        value = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.DOTALL)
        if match is None:
            return {}
        try:
            value = json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}
    return value if isinstance(value, dict) else {}


def normalize_plan(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    plan: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get("tool"), str) or not isinstance(item.get("arguments"), dict):
            return []
        plan.append({"tool": item["tool"], "arguments": {str(k): str(v) for k, v in item["arguments"].items()}})
    return plan


def schema_valid(plan: list[dict[str, Any]], tools: tuple[dict[str, Any], ...]) -> bool:
    index = {item["name"]: item for item in tools}
    for call in plan:
        spec = index.get(call["tool"])
        if spec is None:
            return False
        schema = spec["input_schema"]
        args = call["arguments"]
        if any(name not in args for name in schema["required"]):
            return False
        if any(name not in schema["properties"] for name in args):
            return False
        for name, value in args.items():
            allowed = schema["properties"][name].get("enum")
            if allowed is not None and value not in allowed:
                return False
    return True


def exact_success(plan: list[dict[str, Any]], expected: tuple[dict[str, Any], ...]) -> bool:
    return plan == list(expected)


def build_prompt(scenario: Scenario, condition: str) -> list[dict[str, str]]:
    system = (
        "You migrate executable tool plans. Use only listed tools and exact argument names. "
        "Return JSON only. Preserve task values exactly; never invent tokens."
    )
    payload: dict[str, Any] = {
        "task": scenario.task,
        "old_successful_plan": list(scenario.old_plan),
        "new_tools": list(scenario.new_tools),
    }
    if condition != "latest":
        payload["structured_interface_diff"] = list(scenario.diff)
    if condition == "obligation":
        payload["migration_obligation"] = {
            "affected_old_step_index": scenario.affected_index,
            "instruction": "Return only the replacement sequence for this affected old step. It may contain one or more calls. Unaffected steps are merged deterministically.",
        }
        output = '{"replacement":[{"tool":"...","arguments":{}}]}'
    else:
        payload["instruction"] = "Return the complete executable plan under the new tools."
        output = '{"plan":[{"tool":"...","arguments":{}}]}'
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(payload, ensure_ascii=False) + "\nOUTPUT_SCHEMA=" + output}]


def run_episode(scenario: Scenario, condition: str, endpoint: str, model: str, seed: int, timeout: float) -> dict[str, Any]:
    started = time.perf_counter()
    messages = build_prompt(scenario, condition)
    content, usage = call_model(endpoint, model, messages, seed, timeout)
    parsed = parse_object(content)
    if condition == "obligation":
        replacement = normalize_plan(parsed.get("replacement"))
        plan = list(scenario.old_plan[: scenario.affected_index]) + replacement + list(scenario.old_plan[scenario.affected_index + 1 :])
    else:
        plan = normalize_plan(parsed.get("plan"))
    first_valid = schema_valid(plan, scenario.new_tools)
    first_success = exact_success(plan, scenario.expected_plan)
    calls = 1
    total_usage = dict(usage)
    if condition == "reflection" and not first_success:
        feedback = {
            "schema_valid": first_valid,
            "semantic_failure": "The proposed plan does not exactly satisfy the task under the interface diff.",
            "instruction": "Repair once. Return the complete plan as {\"plan\":[...]}",
        }
        messages.extend([{"role": "assistant", "content": content}, {"role": "user", "content": json.dumps(feedback)}])
        content2, usage2 = call_model(endpoint, model, messages, seed + 10000, timeout)
        parsed2 = parse_object(content2)
        plan = normalize_plan(parsed2.get("plan"))
        calls = 2
        total_usage = {"prompt": usage["prompt"] + usage2["prompt"], "completion": usage["completion"] + usage2["completion"]}
    valid = schema_valid(plan, scenario.new_tools)
    success = exact_success(plan, scenario.expected_plan)
    near_miss = list(scenario.near_miss)
    return {
        "scenario_id": scenario.scenario_id,
        "family": scenario.family,
        "condition": condition,
        "plan": plan,
        "expected_plan": list(scenario.expected_plan),
        "schema_valid": valid,
        "task_success": success,
        "first_attempt_success": first_success,
        "model_calls": calls,
        "tokens": total_usage,
        "near_miss_schema_valid": schema_valid(near_miss, scenario.new_tools),
        "near_miss_rejected": schema_valid(near_miss, scenario.new_tools) and not exact_success(near_miss, scenario.expected_plan),
        "elapsed_seconds": round(time.perf_counter() - started, 4),
    }


def metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {"scenario_count": len({item["scenario_id"] for item in results}), "conditions": {}}
    for condition in CONDITIONS:
        rows = [item for item in results if item["condition"] == condition]
        n = len(rows)
        family: dict[str, Any] = {}
        for name in sorted({item["family"] for item in rows}):
            subset = [item for item in rows if item["family"] == name]
            family[name] = {"n": len(subset), "task_success_rate": sum(item["task_success"] for item in subset) / len(subset)}
        output["conditions"][condition] = {
            "n": n,
            "task_success_rate": sum(item["task_success"] for item in rows) / n,
            "schema_valid_rate": sum(item["schema_valid"] for item in rows) / n,
            "first_attempt_success_rate": sum(item["first_attempt_success"] for item in rows) / n,
            "mean_model_calls": sum(item["model_calls"] for item in rows) / n,
            "mean_tokens": sum(item["tokens"]["prompt"] + item["tokens"]["completion"] for item in rows) / n,
            "near_miss_rejection_rate": sum(item["near_miss_rejected"] for item in rows) / n,
            "by_family": family,
        }
    obligation = output["conditions"]["obligation"]
    diff_prompt = output["conditions"]["diff_prompt"]
    reflection = output["conditions"]["reflection"]
    output["falsification"] = {
        "obligation_minus_diff_prompt_success": obligation["task_success_rate"] - diff_prompt["task_success_rate"],
        "obligation_minus_reflection_success": obligation["task_success_rate"] - reflection["task_success_rate"],
        "obligation_survives_screen": bool(
            obligation["task_success_rate"] >= 0.75
            and obligation["task_success_rate"] - diff_prompt["task_success_rate"] >= 0.15
            and obligation["near_miss_rejection_rate"] >= 0.95
        ),
    }
    return output


def main() -> int:
    overall_started = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--model", default="qwen2.5:7b")
    parser.add_argument("--seed", type=int, default=16003)
    parser.add_argument("--experiment-id", default="delta-contract-screening-v001")
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--limit", type=int)
    arguments = parser.parse_args()
    output_dir = Path(arguments.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    scenarios = build_scenarios()
    if arguments.limit is not None:
        scenarios = scenarios[: arguments.limit]
    results: list[dict[str, Any]] = []
    for scenario_index, scenario in enumerate(scenarios):
        for condition_index, condition in enumerate(CONDITIONS):
            result = run_episode(scenario, condition, arguments.endpoint, arguments.model, arguments.seed + scenario_index * 10 + condition_index, arguments.timeout)
            results.append(result)
            print(json.dumps({"scenario": scenario.scenario_id, "condition": condition, "success": result["task_success"], "valid": result["schema_valid"]}, ensure_ascii=False), flush=True)
    metric_value = metrics(results)
    records: list[dict[str, Any]] = []
    for condition in CONDITIONS:
        condition_metrics = metric_value["conditions"][condition]
        for name, unit in (
            ("task_success_rate", "ratio"),
            ("schema_valid_rate", "ratio"),
            ("first_attempt_success_rate", "ratio"),
            ("mean_model_calls", "calls_per_episode"),
            ("mean_tokens", "tokens_per_episode"),
            ("near_miss_rejection_rate", "ratio"),
        ):
            record_name = "task_success_rate_by_condition" if name == "task_success_rate" else name
            records.append({"name": record_name, "value": condition_metrics[name], "unit": unit, "aggregation": "mean", "split": condition, "n": condition_metrics["n"]})
        for family, family_metrics in condition_metrics["by_family"].items():
            records.append({"name": "task_success_rate", "value": family_metrics["task_success_rate"], "unit": "ratio", "aggregation": "mean", "split": f"{condition}:{family}", "n": family_metrics["n"]})
    records.extend(
        [
            {"name": "obligation_minus_diff_prompt_success", "value": metric_value["falsification"]["obligation_minus_diff_prompt_success"], "unit": "ratio_difference", "aggregation": "difference", "split": "overall", "n": len(scenarios)},
            {"name": "obligation_minus_reflection_success", "value": metric_value["falsification"]["obligation_minus_reflection_success"], "unit": "ratio_difference", "aggregation": "difference", "split": "overall", "n": len(scenarios)},
            {"name": "obligation_survives_screen", "value": 1.0 if metric_value["falsification"]["obligation_survives_screen"] else 0.0, "unit": "boolean", "aggregation": "decision_rule", "split": "overall", "n": len(scenarios)},
        ]
    )
    formal_metrics = {
        "schema_version": 1,
        "experiment_id": arguments.experiment_id,
        "records": records,
        "resource_usage": {
            "api_calls": sum(item["model_calls"] for item in results),
            "tokens": sum(item["tokens"]["prompt"] + item["tokens"]["completion"] for item in results),
            "wall_time_seconds": time.perf_counter() - overall_started,
            "gpu_time_seconds": "unknown",
            "estimated_cost": 0.0,
        },
        "warnings": [],
        "errors": [],
    }
    (output_dir / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (output_dir / "metrics-output.json").write_text(json.dumps(formal_metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(metric_value, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
