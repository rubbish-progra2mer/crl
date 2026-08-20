from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
import urllib.request
from collections import defaultdict
from pathlib import Path


def group(*literals: tuple[str, bool]) -> dict:
    return {"all": [{"field": field, "value": value} for field, value in literals]}


TASKS = [
    {
        "task_id": "refund",
        "fields": {
            "within_30_days": "The request is within 30 days.",
            "has_receipt": "The customer has a receipt.",
            "defective_item": "The item is defective.",
            "within_90_days": "The request is within 90 days.",
            "final_sale": "The item was marked final sale.",
        },
        "policy": "Commit a refund when the request is within 30 days and has a receipt, or when a defective item is returned within 90 days. Never refund a final-sale item.",
        "reference": {
            "allow_any": [group(("within_30_days", True), ("has_receipt", True)), group(("defective_item", True), ("within_90_days", True))],
            "deny_any": [group(("final_sale", True))],
        },
    },
    {
        "task_id": "deployment",
        "fields": {
            "tests_pass": "All required tests passed.",
            "two_approvals": "Two independent approvals are present.",
            "emergency_override": "An emergency override is active.",
            "incident_active": "A production incident is active.",
            "freeze_window": "A deployment freeze is active.",
        },
        "policy": "Deploy when tests pass with two approvals, or when an emergency override is active during a production incident. A deployment freeze always blocks deployment.",
        "reference": {
            "allow_any": [group(("tests_pass", True), ("two_approvals", True)), group(("emergency_override", True), ("incident_active", True))],
            "deny_any": [group(("freeze_window", True))],
        },
    },
    {
        "task_id": "bank_transfer",
        "fields": {
            "owner_verified": "The account owner is verified.",
            "under_limit": "The transfer is within the standard limit.",
            "second_factor": "A second-factor approval is present.",
            "blocked_region": "The destination is in a blocked region.",
            "fraud_hold": "A fraud hold is active.",
        },
        "policy": "Transfer only for a verified owner when the amount is under the standard limit or a second factor is present. Never transfer to a blocked region or while a fraud hold is active.",
        "reference": {
            "allow_any": [group(("owner_verified", True), ("under_limit", True)), group(("owner_verified", True), ("second_factor", True))],
            "deny_any": [group(("blocked_region", True)), group(("fraud_hold", True))],
        },
    },
    {
        "task_id": "report_disclosure",
        "fields": {
            "public_report": "The report is public.",
            "high_clearance": "The requester has high clearance.",
            "audit_purpose": "The request is for an authorized audit.",
            "legal_hold": "A legal hold forbids disclosure.",
            "personal_data": "The report contains protected personal data.",
        },
        "policy": "Disclose a public report, or disclose a nonpublic report to a high-clearance requester for an authorized audit. Never disclose under legal hold or when protected personal data is present.",
        "reference": {
            "allow_any": [group(("public_report", True)), group(("high_clearance", True), ("audit_purpose", True))],
            "deny_any": [group(("legal_hold", True)), group(("personal_data", True))],
        },
    },
    {
        "task_id": "shipment",
        "fields": {
            "in_stock": "The item is in stock.",
            "verified_address": "The delivery address is verified.",
            "store_pickup": "The customer selected store pickup.",
            "fraud_hold": "A fraud hold is active.",
            "embargo": "A shipping embargo applies.",
        },
        "policy": "Ship an in-stock item when the address is verified or store pickup is selected. Never ship while a fraud hold or embargo is active.",
        "reference": {
            "allow_any": [group(("in_stock", True), ("verified_address", True)), group(("in_stock", True), ("store_pickup", True))],
            "deny_any": [group(("fraud_hold", True)), group(("embargo", True))],
        },
    },
    {
        "task_id": "record_deletion",
        "fields": {
            "retention_expired": "The retention period has expired.",
            "owner_request": "The data owner requested deletion.",
            "court_order": "A valid court order requires deletion.",
            "litigation_hold": "A litigation hold is active.",
            "only_backup_copy": "This is the only remaining backup copy.",
        },
        "policy": "Delete after retention expires when the owner requests it or a court order requires it. Never delete during litigation hold or when this is the only remaining backup copy.",
        "reference": {
            "allow_any": [group(("retention_expired", True), ("owner_request", True)), group(("retention_expired", True), ("court_order", True))],
            "deny_any": [group(("litigation_hold", True)), group(("only_backup_copy", True))],
        },
    },
    {
        "task_id": "account_restore",
        "fields": {
            "owner_verified": "The owner is verified.",
            "cooldown_done": "The security cooldown has finished.",
            "support_override": "An authorized support override is present.",
            "abuse_flag": "An abuse flag is active.",
            "legal_lock": "A legal lock is active.",
        },
        "policy": "Restore only for a verified owner after cooldown or with an authorized support override. Never restore while an abuse flag or legal lock is active.",
        "reference": {
            "allow_any": [group(("owner_verified", True), ("cooldown_done", True)), group(("owner_verified", True), ("support_override", True))],
            "deny_any": [group(("abuse_flag", True)), group(("legal_lock", True))],
        },
    },
    {
        "task_id": "travel_booking",
        "fields": {
            "budget_ok": "The trip is within budget.",
            "policy_route": "The route follows travel policy.",
            "executive_exception": "An executive exception is approved.",
            "passport_valid": "The traveler's passport is valid.",
            "travel_ban": "A travel ban applies.",
        },
        "policy": "Book only within budget, using a policy route or an approved executive exception, and with a valid passport. Never book when a travel ban applies.",
        "reference": {
            "allow_any": [group(("budget_ok", True), ("policy_route", True), ("passport_valid", True)), group(("budget_ok", True), ("executive_exception", True), ("passport_valid", True))],
            "deny_any": [group(("travel_ban", True))],
        },
    },
    {
        "task_id": "invoice_payment",
        "fields": {
            "vendor_approved": "The vendor is approved.",
            "under_5000": "The invoice is below 5000.",
            "director_approval": "A director approved the invoice.",
            "duplicate_invoice": "The invoice is a duplicate.",
            "sanctions_hit": "The vendor matches a sanctions record.",
        },
        "policy": "Pay an approved vendor when the invoice is below 5000 or has director approval. Never pay a duplicate invoice or a vendor with a sanctions hit.",
        "reference": {
            "allow_any": [group(("vendor_approved", True), ("under_5000", True)), group(("vendor_approved", True), ("director_approval", True))],
            "deny_any": [group(("duplicate_invoice", True)), group(("sanctions_hit", True))],
        },
    },
    {
        "task_id": "model_release",
        "fields": {
            "evaluation_passed": "The release evaluation passed.",
            "risk_low": "The assessed risk is low.",
            "risk_waiver": "A risk waiver is approved.",
            "license_ok": "All licenses permit release.",
            "active_incident": "An active safety incident exists.",
        },
        "policy": "Release only after evaluation passes, with either low risk or an approved waiver, and when licenses permit release. Never release during an active safety incident.",
        "reference": {
            "allow_any": [group(("evaluation_passed", True), ("risk_low", True), ("license_ok", True)), group(("evaluation_passed", True), ("risk_waiver", True), ("license_ok", True))],
            "deny_any": [group(("active_incident", True))],
        },
    },
    {
        "task_id": "repository_access",
        "fields": {
            "administrator": "The requester is an administrator.",
            "developer": "The requester is a developer.",
            "approved_ticket": "An approved access ticket exists.",
            "revoked": "The requester is revoked.",
            "export_restricted": "Export restrictions prohibit access.",
        },
        "policy": "Grant repository access to an administrator, or to a developer with an approved ticket. Never grant access to a revoked requester or when export restrictions prohibit it.",
        "reference": {
            "allow_any": [group(("administrator", True)), group(("developer", True), ("approved_ticket", True))],
            "deny_any": [group(("revoked", True)), group(("export_restricted", True))],
        },
    },
    {
        "task_id": "procedure_schedule",
        "fields": {
            "consent": "The patient gave consent.",
            "risk_low": "The procedure risk is low.",
            "specialist_present": "A specialist will be present.",
            "labs_current": "Required laboratory results are current.",
            "allergy_conflict": "An unresolved allergy conflict exists.",
        },
        "policy": "Schedule only with consent, when risk is low or a specialist will be present, and when laboratory results are current. Never schedule with an unresolved allergy conflict.",
        "reference": {
            "allow_any": [group(("consent", True), ("risk_low", True), ("labs_current", True)), group(("consent", True), ("specialist_present", True), ("labs_current", True))],
            "deny_any": [group(("allergy_conflict", True))],
        },
    },
]


def evaluate_policy(policy: dict, state: dict[str, bool]) -> bool:
    def matches(item: dict) -> bool:
        return all(state[literal["field"]] is literal["value"] for literal in item["all"])

    allow = any(matches(item) for item in policy["allow_any"])
    deny = any(matches(item) for item in policy["deny_any"])
    return allow and not deny


def validate_candidate(policy: object, field_names: tuple[str, ...]) -> dict:
    if not isinstance(policy, dict) or set(policy) != {"allow_any", "deny_any"}:
        raise ValueError("candidate must contain exactly allow_any and deny_any")
    normalized: dict[str, list[dict]] = {"allow_any": [], "deny_any": []}
    for key in ("allow_any", "deny_any"):
        groups = policy[key]
        if not isinstance(groups, list) or len(groups) > 12:
            raise ValueError(f"{key} must be a list of at most 12 groups")
        if key == "allow_any" and not groups:
            raise ValueError("allow_any must not be empty")
        for item in groups:
            if not isinstance(item, dict) or set(item) != {"all"}:
                raise ValueError(f"{key} group must contain exactly all")
            literals = item["all"]
            if not isinstance(literals, list) or not literals or len(literals) > len(field_names):
                raise ValueError(f"{key} group has invalid literal count")
            seen: set[str] = set()
            normalized_literals = []
            for literal in literals:
                if not isinstance(literal, dict) or set(literal) != {"field", "value"}:
                    raise ValueError("literal must contain exactly field and value")
                field = literal["field"]
                value = literal["value"]
                if field not in field_names or not isinstance(value, bool):
                    raise ValueError("literal has unknown field or non-boolean value")
                if field in seen:
                    raise ValueError("a conjunction cannot repeat a field")
                seen.add(field)
                normalized_literals.append({"field": field, "value": value})
            normalized[key].append({"all": normalized_literals})
    return normalized


def all_states(field_names: tuple[str, ...]) -> list[dict[str, bool]]:
    return [dict(zip(field_names, values, strict=True)) for values in itertools.product((False, True), repeat=len(field_names))]


def state_signature(state: dict[str, bool], field_names: tuple[str, ...]) -> str:
    return "".join("1" if state[field] else "0" for field in field_names)


def reference_design(task: dict, seed: int) -> dict:
    fields = tuple(task["fields"])
    worlds = all_states(fields)
    labels = [evaluate_policy(task["reference"], state) for state in worlds]
    allowed = [state for state, label in zip(worlds, labels, strict=True) if label]
    nominal = max(allowed, key=lambda state: (sum(state.values()), state_signature(state, fields)))

    pairs = []
    for field in fields:
        candidates = []
        for state in worlds:
            if state[field]:
                continue
            other = dict(state)
            other[field] = True
            left = evaluate_policy(task["reference"], state)
            right = evaluate_policy(task["reference"], other)
            if left != right:
                candidates.append((state, other, left, right))
        if not candidates:
            raise ValueError(f"reference field is not decision-relevant: {task['task_id']}:{field}")
        selected = max(
            candidates,
            key=lambda item: (
                sum(item[0].values()) + sum(item[1].values()),
                state_signature(item[0], fields),
            ),
        )
        pairs.append(
            {
                "field": field,
                "false_state": selected[0],
                "true_state": selected[1],
                "false_decision": selected[2],
                "true_decision": selected[3],
            }
        )

    activation_worlds = [pair[name] for pair in pairs for name in ("false_state", "true_state")]
    digest = hashlib.sha256(f"{seed}:{task['task_id']}".encode("utf-8")).digest()
    randomizer = random.Random(int.from_bytes(digest[:8], "big"))
    random_worlds = randomizer.sample(worlds, len(activation_worlds))
    return {
        "fields": fields,
        "worlds": worlds,
        "labels": labels,
        "nominal": nominal,
        "pairs": pairs,
        "activation_worlds": activation_worlds,
        "random_worlds": random_worlds,
    }


def response_schema(field_names: tuple[str, ...]) -> dict:
    literal = {
        "type": "object",
        "properties": {
            "field": {"type": "string", "enum": list(field_names)},
            "value": {"type": "boolean"},
        },
        "required": ["field", "value"],
        "additionalProperties": False,
    }
    conjunction = {
        "type": "object",
        "properties": {"all": {"type": "array", "items": literal, "minItems": 1, "maxItems": len(field_names)}},
        "required": ["all"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "allow_any": {"type": "array", "items": conjunction, "minItems": 1, "maxItems": 12},
            "deny_any": {"type": "array", "items": conjunction, "maxItems": 12},
        },
        "required": ["allow_any", "deny_any"],
        "additionalProperties": False,
    }


def build_messages(task: dict) -> list[dict]:
    system = (
        "Compile a natural-language policy for a privileged tool commit into a boolean decision policy. "
        "allow_any is a disjunction of sufficient groups; every literal inside a group's all list must match. "
        "deny_any is a disjunction of blocking groups and overrides allow_any. "
        "Use only the supplied boolean field identifiers. Preserve every field that can change the decision. "
        "Return only the requested JSON object; do not solve one particular observation."
    )
    user = json.dumps(
        {
            "tool_action": f"commit_{task['task_id']}",
            "observation_fields": task["fields"],
            "policy": task["policy"],
        },
        ensure_ascii=False,
        indent=2,
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def call_ollama(model: str, task: dict, seed: int, timeout: int) -> dict:
    fields = tuple(task["fields"])
    messages = build_messages(task)
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": response_schema(fields),
        "think": False,
        "options": {"temperature": 0.7, "seed": seed, "num_predict": 512},
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    content = body["message"].get("content", "")
    if not content.strip():
        raise ValueError(f"empty content; message keys={sorted(body['message'])}")
    return {
        "raw_policy": json.loads(content),
        "elapsed_seconds": time.time() - started,
        "ollama_created_at": body.get("created_at"),
        "total_duration_ns": body.get("total_duration"),
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "prompt_sha256": hashlib.sha256(json.dumps(messages, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest(),
    }


def accuracy(policy: dict, states: list[dict[str, bool]], reference: dict) -> float:
    return sum(evaluate_policy(policy, state) == evaluate_policy(reference, state) for state in states) / len(states)


def select_record(rows: list[dict], score_name: str) -> dict:
    return max(rows, key=lambda row: (row.get(score_name, -1.0), -row["candidate_index"]))


def summarize(candidate_rows: list[dict], task_count: int) -> dict:
    selection_rows = []
    by_model_task: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in candidate_rows:
        by_model_task[(row["model"], row["task_id"])].append(row)
    for (model, task_id), rows in sorted(by_model_task.items()):
        rows.sort(key=lambda item: item["candidate_index"])
        first = rows[0]
        nominal = select_record(rows, "nominal_score")
        activation = select_record(rows, "activation_accuracy")
        random_pick = select_record(rows, "random_accuracy")
        oracle = select_record(rows, "hidden_accuracy")
        selection_rows.append(
            {
                "model": model,
                "task_id": task_id,
                "first_candidate_index": first["candidate_index"],
                "first_hidden_accuracy": first.get("hidden_accuracy", 0.0),
                "nominal_candidate_index": nominal["candidate_index"],
                "nominal_hidden_accuracy": nominal.get("hidden_accuracy", 0.0),
                "activation_candidate_index": activation["candidate_index"],
                "activation_hidden_accuracy": activation.get("hidden_accuracy", 0.0),
                "random_candidate_index": random_pick["candidate_index"],
                "random_hidden_accuracy": random_pick.get("hidden_accuracy", 0.0),
                "oracle_candidate_index": oracle["candidate_index"],
                "oracle_hidden_accuracy": oracle.get("hidden_accuracy", 0.0),
            }
        )

    scopes: dict[str, list[dict]] = defaultdict(list)
    for row in candidate_rows:
        scopes[row["model"]].append(row)
        scopes["overall"].append(row)
    selection_scopes: dict[str, list[dict]] = defaultdict(list)
    for row in selection_rows:
        selection_scopes[row["model"]].append(row)
        selection_scopes["overall"].append(row)

    aggregates = []
    for scope, rows in sorted(scopes.items()):
        valid = [row for row in rows if row.get("candidate_error") is None and row.get("error") is None]
        nominal_pass = [row for row in valid if row["nominal_correct"]]
        latent_faults = [row for row in nominal_pass if row["hidden_accuracy"] < 1.0]
        activation_caught = sum(row["activation_accuracy"] < 1.0 for row in latent_faults)
        random_caught = sum(row["random_accuracy"] < 1.0 for row in latent_faults)
        picks = selection_scopes[scope]
        activation_selection = sum(row["activation_hidden_accuracy"] for row in picks) / len(picks)
        random_selection = sum(row["random_hidden_accuracy"] for row in picks) / len(picks)
        item = {
            "scope": scope,
            "candidate_count": len(rows),
            "valid_candidate_count": len(valid),
            "nominal_pass_count": len(nominal_pass),
            "latent_fault_count": len(latent_faults),
            "latent_fault_rate_among_nominal_pass": len(latent_faults) / len(nominal_pass) if nominal_pass else 0.0,
            "activation_fault_recall": activation_caught / len(latent_faults) if latent_faults else 0.0,
            "random_fault_recall": random_caught / len(latent_faults) if latent_faults else 0.0,
            "contract_activation_fault_recall_advantage": (activation_caught - random_caught) / len(latent_faults) if latent_faults else 0.0,
            "first_candidate_hidden_accuracy": sum(row["first_hidden_accuracy"] for row in picks) / len(picks),
            "nominal_selection_hidden_accuracy": sum(row["nominal_hidden_accuracy"] for row in picks) / len(picks),
            "activation_selection_hidden_accuracy": activation_selection,
            "random_selection_hidden_accuracy": random_selection,
            "selection_hidden_accuracy_advantage": activation_selection - random_selection,
            "oracle_selection_hidden_accuracy": sum(row["oracle_hidden_accuracy"] for row in picks) / len(picks),
            "task_count": len(picks),
        }
        aggregates.append(item)
    if len(selection_rows) != task_count * len({row["model"] for row in candidate_rows}):
        raise ValueError("selection summary does not cover every model-task pair")
    return {"aggregates": aggregates, "selection": selection_rows}


def main() -> int:
    script_started = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["qwen2.5:7b", "qwen3:8b"])
    parser.add_argument("--seed", type=int, default=20260816)
    parser.add_argument("--candidates-per-task", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--details-output", type=Path, required=True)
    args = parser.parse_args()

    designs = {task["task_id"]: reference_design(task, args.seed) for task in TASKS}
    candidate_rows = []
    api_errors = []
    for model in args.models:
        for task in TASKS:
            design = designs[task["task_id"]]
            for candidate_index in range(args.candidates_per_task):
                call_seed = args.seed + candidate_index
                row = {
                    "model": model,
                    "task_id": task["task_id"],
                    "candidate_index": candidate_index,
                    "seed": call_seed,
                    "error": None,
                    "candidate_error": None,
                }
                try:
                    outcome = call_ollama(model, task, call_seed, args.timeout)
                    row.update(outcome)
                    candidate = validate_candidate(outcome["raw_policy"], design["fields"])
                    row["candidate_policy"] = candidate
                    row["nominal_correct"] = evaluate_policy(candidate, design["nominal"]) == evaluate_policy(task["reference"], design["nominal"])
                    row["nominal_score"] = 1.0 if row["nominal_correct"] else 0.0
                    row["activation_accuracy"] = accuracy(candidate, design["activation_worlds"], task["reference"])
                    row["random_accuracy"] = accuracy(candidate, design["random_worlds"], task["reference"])
                    row["hidden_accuracy"] = accuracy(candidate, design["worlds"], task["reference"])
                    row["latent_fault"] = row["nominal_correct"] and row["hidden_accuracy"] < 1.0
                except (ValueError, KeyError, TypeError) as exc:
                    row["candidate_error"] = f"{type(exc).__name__}: {exc}"
                    row.update({"nominal_score": -1.0, "activation_accuracy": -1.0, "random_accuracy": -1.0, "hidden_accuracy": 0.0})
                except Exception as exc:  # noqa: BLE001 - preserve external model/API failures
                    row["error"] = f"{type(exc).__name__}: {exc}"
                    row.update({"nominal_score": -1.0, "activation_accuracy": -1.0, "random_accuracy": -1.0, "hidden_accuracy": 0.0})
                    api_errors.append(row["error"])
                candidate_rows.append(row)
                print(json.dumps(row, ensure_ascii=False), flush=True)

    summary = summarize(candidate_rows, len(TASKS))
    details = {
        "schema_version": 1,
        "experiment": "contract-activation-probe-v007",
        "models": args.models,
        "seed": args.seed,
        "candidates_per_task": args.candidates_per_task,
        "task_count": len(TASKS),
        "tasks": TASKS,
        "designs": {
            task_id: {
                "nominal": design["nominal"],
                "activation_pairs": design["pairs"],
                "random_worlds": design["random_worlds"],
                "world_count": len(design["worlds"]),
            }
            for task_id, design in designs.items()
        },
        "candidate_records": candidate_rows,
        "summary": summary,
    }

    metric_records = []
    metric_names = (
        "contract_activation_fault_recall_advantage",
        "latent_fault_rate_among_nominal_pass",
        "activation_fault_recall",
        "random_fault_recall",
        "first_candidate_hidden_accuracy",
        "nominal_selection_hidden_accuracy",
        "activation_selection_hidden_accuracy",
        "random_selection_hidden_accuracy",
        "selection_hidden_accuracy_advantage",
        "oracle_selection_hidden_accuracy",
    )
    for item in summary["aggregates"]:
        for name in metric_names:
            n = item["latent_fault_count"] if "fault_recall" in name else item["task_count"]
            if name == "latent_fault_rate_among_nominal_pass":
                n = item["nominal_pass_count"]
            metric_records.append(
                {
                    "name": name,
                    "value": item[name],
                    "unit": "proportion",
                    "split": item["scope"],
                    "aggregation": "micro_over_candidates" if "fault" in name else "mean_over_model_task_groups",
                    "n": n,
                    "seed": args.seed,
                }
            )

    invalid_count = sum(row.get("candidate_error") is not None for row in candidate_rows)
    overall = next(item for item in summary["aggregates"] if item["scope"] == "overall")
    warnings = []
    if invalid_count:
        warnings.append(f"{invalid_count} generated candidates were schema-invalid and treated as failed policies")
    if overall["latent_fault_count"] == 0:
        warnings.append("no nominal-pass latent semantic faults were available for recall estimation")
    metrics = {
        "schema_version": 1,
        "experiment_id": "contract-activation-probe-001",
        "records": metric_records,
        "resource_usage": {
            "tokens": sum((row.get("prompt_eval_count") or 0) + (row.get("eval_count") or 0) for row in candidate_rows),
            "api_calls": len(candidate_rows),
            "wall_time_seconds": time.time() - script_started,
            "gpu_time_seconds": None,
            "estimated_cost": 0,
        },
        "errors": sorted(set(api_errors)),
        "warnings": warnings,
    }
    for path, payload in ((args.details_output, details), (args.metrics_output, metrics)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
