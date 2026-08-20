from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score


OLLAMA_URL = "http://127.0.0.1:11434"
EMBED_MODEL = "bge-m3:latest"
PARSER_MODEL = "qwen3:8b"


@dataclass(frozen=True)
class DomainSpec:
    key: str
    base: dict[str, Any]
    alternatives: dict[str, list[Any]]
    binding_slots: tuple[str, ...]
    inert_slot: str
    manual_key_slots: tuple[str, ...]
    template: str
    base_steps: tuple[str, ...]
    step_rules: tuple[tuple[str, Any, str, int], ...]
    interaction: tuple[str, Any, str, Any, str, int]

    @property
    def ordered_slots(self) -> tuple[str, ...]:
        return tuple(self.base)

    def render(self, slots: dict[str, Any]) -> str:
        values = {key: verbalize(value) for key, value in slots.items()}
        return self.template.format(**values)

    def trace(self, slots: dict[str, Any]) -> list[dict[str, Any]]:
        steps = [{"tool": tool, "args": {}} for tool in self.base_steps]
        for slot, value, tool, position in self.step_rules:
            if slots[slot] == value:
                if tool.startswith("replace:"):
                    _, old_tool, new_tool = tool.split(":", maxsplit=2)
                    old_index = next(index for index, step in enumerate(steps) if step["tool"] == old_tool)
                    steps[old_index] = {"tool": new_tool, "args": {"trigger": slot}}
                else:
                    steps.insert(position, {"tool": tool, "args": {"trigger": slot}})
        left_slot, left_value, right_slot, right_value, tool, position = self.interaction
        if slots[left_slot] == left_value and slots[right_slot] == right_value:
            steps.insert(position, {"tool": tool, "args": {"trigger": f"{left_slot}&{right_slot}"}})
        binding_values = {slot: slots[slot] for slot in self.binding_slots}
        for step in steps:
            step["args"].update(binding_values)
        return steps


def verbalize(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return str(value)


def build_specs() -> list[DomainSpec]:
    return [
        DomainSpec(
            key="flight_booking",
            base={"trip_type": "one-way", "traveler": "adult", "refundable": False,
                  "origin": "Boston", "destination": "Chicago", "date": "September 12",
                  "tone": "Please handle this normally.", "cross_border": False, "high_value": False},
            alternatives={"trip_type": ["round-trip"], "traveler": ["infant"], "refundable": [True],
                          "origin": ["Seattle", "Austin"], "destination": ["Denver", "Miami"],
                          "date": ["October 3", "November 18"],
                          "tone": ["Thanks in advance.", "This is not urgent."],
                          "cross_border": [True], "high_value": [True]},
            binding_slots=("origin", "destination", "date"), inert_slot="tone",
            manual_key_slots=("trip_type", "refundable"),
            template=("Book a {trip_type} flight for an {traveler} from {origin} to {destination} on {date}. "
                      "Refundable fare: {refundable}. Cross-border itinerary: {cross_border}. "
                      "High-value transaction: {high_value}. {tone}"),
            base_steps=("search_flights", "book_flight"),
            step_rules=(("trip_type", "round-trip", "search_return_flights", 1),
                        ("traveler", "infant", "check_infant_eligibility", 0),
                        ("refundable", True, "read_refund_policy", 1)),
            interaction=("cross_border", True, "high_value", True, "run_travel_compliance", 0),
        ),
        DomainSpec(
            key="calendar_meeting",
            base={"recurrence": "once", "audience": "internal", "private": False,
                  "title": "design review", "time": "Tuesday 10 AM", "duration": "45 minutes",
                  "tone": "No rush.", "external_domain": False, "sensitive_topic": False},
            alternatives={"recurrence": ["weekly"], "audience": ["external"], "private": [True],
                          "title": ["budget review", "roadmap sync"], "time": ["Friday 2 PM", "Monday 9 AM"],
                          "duration": ["30 minutes", "60 minutes"],
                          "tone": ["Please do this soon.", "Thank you."],
                          "external_domain": [True], "sensitive_topic": [True]},
            binding_slots=("title", "time", "duration"), inert_slot="tone",
            manual_key_slots=("recurrence", "audience"),
            template=("Schedule the {title} at {time} for {duration}, occurring {recurrence}, with an {audience} "
                      "audience. Private event: {private}. External email domain: {external_domain}. "
                      "Sensitive topic: {sensitive_topic}. {tone}"),
            base_steps=("check_calendar", "create_event"),
            step_rules=(("recurrence", "weekly", "create_recurrence_rule", 1),
                        ("audience", "external", "send_external_invites", 2),
                        ("private", True, "apply_private_visibility", 2)),
            interaction=("external_domain", True, "sensitive_topic", True, "request_compliance_approval", 1),
        ),
        DomainSpec(
            key="retail_return",
            base={"resolution": "refund", "receipt": "present", "opened": False,
                  "order": "ORD-1042", "item": "headphones", "reason": "arrived late",
                  "tone": "Please process it.", "hazardous": False, "international": False},
            alternatives={"resolution": ["exchange"], "receipt": ["missing"], "opened": [True],
                          "order": ["ORD-2051", "ORD-7740"], "item": ["keyboard", "speaker"],
                          "reason": ["has the wrong color", "has a damaged box"],
                          "tone": ["I would appreciate help.", "This can wait."],
                          "hazardous": [True], "international": [True]},
            binding_slots=("order", "item", "reason"), inert_slot="tone",
            manual_key_slots=("resolution", "receipt"),
            template=("For order {order}, return the {item} because it {reason}. Requested resolution: {resolution}. "
                      "Receipt: {receipt}. Package opened: {opened}. Hazardous item: {hazardous}. "
                      "International order: {international}. {tone}"),
            base_steps=("get_order", "issue_refund"),
            step_rules=(("resolution", "exchange", "replace:issue_refund:create_replacement_order", 1),
                        ("receipt", "missing", "verify_purchase_history", 1),
                        ("opened", True, "inspect_opened_item_policy", 1)),
            interaction=("hazardous", True, "international", True, "route_special_return", 1),
        ),
        DomainSpec(
            key="bank_transfer",
            base={"timing": "immediate", "recipient_type": "saved", "notify": False,
                  "recipient": "Alex", "amount": "$240", "memo": "utilities",
                  "tone": "Please proceed.", "cross_border": False, "new_device": False},
            alternatives={"timing": ["scheduled"], "recipient_type": ["new"], "notify": [True],
                          "recipient": ["Morgan", "Taylor"], "amount": ["$315", "$480"],
                          "memo": ["rent", "invoice"], "tone": ["Thank you.", "It is not urgent."],
                          "cross_border": [True], "new_device": [True]},
            binding_slots=("recipient", "amount", "memo"), inert_slot="tone",
            manual_key_slots=("timing", "recipient_type"),
            template=("Make an {timing} transfer of {amount} to {recipient}, a {recipient_type} recipient, "
                      "with memo {memo}. Send notification: {notify}. Cross-border: {cross_border}. "
                      "New device session: {new_device}. {tone}"),
            base_steps=("get_recipient", "submit_transfer"),
            step_rules=(("timing", "scheduled", "replace:submit_transfer:create_transfer_schedule", 1),
                        ("recipient_type", "new", "verify_new_recipient", 1),
                        ("notify", True, "send_transfer_notification", 3)),
            interaction=("cross_border", True, "new_device", True, "step_up_authentication", 1),
        ),
        DomainSpec(
            key="email_cleanup",
            base={"action": "archive", "scope": "single-folder", "dry_run": False,
                  "folder": "Newsletters", "before": "January 1", "sender": "updates@example.com",
                  "tone": "Please clean this up.", "legal_hold": False, "shared_mailbox": False},
            alternatives={"action": ["delete"], "scope": ["all-folders"], "dry_run": [True],
                          "folder": ["Receipts", "Alerts"], "before": ["March 1", "June 30"],
                          "sender": ["offers@example.com", "digest@example.com"],
                          "tone": ["No hurry.", "Thanks."], "legal_hold": [True], "shared_mailbox": [True]},
            binding_slots=("folder", "before", "sender"), inert_slot="tone",
            manual_key_slots=("action", "dry_run"),
            template=("{action} messages in {folder} from {sender} dated before {before}. Scope: {scope}. "
                      "Dry run only: {dry_run}. Legal hold applies: {legal_hold}. "
                      "Shared mailbox: {shared_mailbox}. {tone}"),
            base_steps=("search_messages", "archive_messages"),
            step_rules=(("action", "delete", "replace:archive_messages:delete_messages", 1),
                        ("scope", "all-folders", "enumerate_folders", 0),
                        ("dry_run", True, "replace:archive_messages:preview_changes", 1)),
            interaction=("legal_hold", True, "shared_mailbox", True, "request_records_approval", 1),
        ),
        DomainSpec(
            key="cloud_deploy",
            base={"environment": "staging", "strategy": "rolling", "rollback": False,
                  "service": "billing-api", "version": "v2.4.1", "region": "us-east",
                  "tone": "Deploy when ready.", "schema_change": False, "traffic_peak": False},
            alternatives={"environment": ["production"], "strategy": ["blue-green"], "rollback": [True],
                          "service": ["search-api", "auth-api"], "version": ["v3.0.0", "v2.5.2"],
                          "region": ["eu-west", "ap-south"], "tone": ["No rush.", "Please proceed carefully."],
                          "schema_change": [True], "traffic_peak": [True]},
            binding_slots=("service", "version", "region"), inert_slot="tone",
            manual_key_slots=("environment", "strategy"),
            template=("Deploy {service} version {version} to {environment} in {region} using {strategy}. "
                      "Prepare rollback: {rollback}. Database schema change: {schema_change}. "
                      "Peak traffic window: {traffic_peak}. {tone}"),
            base_steps=("run_prechecks", "deploy_service", "verify_health"),
            step_rules=(("environment", "production", "request_change_approval", 1),
                        ("strategy", "blue-green", "switch_traffic", 2),
                        ("rollback", True, "create_rollback_snapshot", 1)),
            interaction=("schema_change", True, "traffic_peak", True, "schedule_maintenance_window", 1),
        ),
        DomainSpec(
            key="data_report",
            base={"analysis": "snapshot", "format": "dashboard", "restricted": False,
                  "metric": "monthly revenue", "period": "Q2", "segment": "North America",
                  "tone": "Please prepare it.", "personal_data": False, "external_share": False},
            alternatives={"analysis": ["comparison"], "format": ["csv"], "restricted": [True],
                          "metric": ["active users", "churn rate"], "period": ["Q1", "July"],
                          "segment": ["Europe", "Enterprise"], "tone": ["Thanks.", "This can wait."],
                          "personal_data": [True], "external_share": [True]},
            binding_slots=("metric", "period", "segment"), inert_slot="tone",
            manual_key_slots=("analysis", "format"),
            template=("Prepare a {analysis} report for {metric} during {period}, segment {segment}, in {format} "
                      "format. Restricted dataset: {restricted}. Contains personal data: {personal_data}. "
                      "Share externally: {external_share}. {tone}"),
            base_steps=("query_warehouse", "build_dashboard"),
            step_rules=(("analysis", "comparison", "query_comparison_period", 1),
                        ("format", "csv", "replace:build_dashboard:export_csv", 2),
                        ("restricted", True, "check_data_entitlement", 0)),
            interaction=("personal_data", True, "external_share", True, "run_privacy_review", 1),
        ),
        DomainSpec(
            key="support_ticket",
            base={"operation": "resolve", "priority": "normal", "customer_contact": False,
                  "ticket": "TCK-441", "product": "mobile app", "issue": "login loop",
                  "tone": "Please take care of it.", "security_signal": False, "production_outage": False},
            alternatives={"operation": ["escalate"], "priority": ["urgent"], "customer_contact": [True],
                          "ticket": ["TCK-992", "TCK-317"], "product": ["web portal", "desktop client"],
                          "issue": ["sync failure", "blank screen"], "tone": ["Thank you.", "No rush."],
                          "security_signal": [True], "production_outage": [True]},
            binding_slots=("ticket", "product", "issue"), inert_slot="tone",
            manual_key_slots=("operation", "priority"),
            template=("{operation} ticket {ticket} about a {issue} in the {product}. Priority: {priority}. "
                      "Contact customer: {customer_contact}. Security signal: {security_signal}. "
                      "Production outage: {production_outage}. {tone}"),
            base_steps=("get_ticket", "apply_resolution"),
            step_rules=(("operation", "escalate", "replace:apply_resolution:assign_specialist", 1),
                        ("priority", "urgent", "page_on_call", 1),
                        ("customer_contact", True, "send_customer_update", 2)),
            interaction=("security_signal", True, "production_outage", True, "activate_incident_response", 1),
        ),
    ]


def skeleton(trace: list[dict[str, Any]]) -> tuple[str, ...]:
    return tuple(step["tool"] for step in trace)


def mutate(base: dict[str, Any], **changes: Any) -> dict[str, Any]:
    result = dict(base)
    result.update(changes)
    return result


def generate_cases(specs: list[DomainSpec], seed: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rng = random.Random(seed)
    caches: list[dict[str, Any]] = []
    cases: list[dict[str, Any]] = []
    for spec in specs:
        base_trace = spec.trace(spec.base)
        cache = {
            "domain": spec.key,
            "request": spec.render(spec.base),
            "slots": dict(spec.base),
            "trace": base_trace,
            "skeleton": list(skeleton(base_trace)),
        }
        caches.append(cache)
        variants: list[tuple[str, dict[str, Any]]] = []
        # Eight safe variants: binding changes, inert changes, and paraphrase-equivalent combinations.
        for slot in spec.binding_slots:
            for value in spec.alternatives[slot][:2]:
                variants.append((f"binding:{slot}", mutate(spec.base, **{slot: value})))
        for value in spec.alternatives[spec.inert_slot][:2]:
            variants.append((f"inert:{spec.inert_slot}", mutate(spec.base, **{spec.inert_slot: value})))
        # Unsafe single-factor changes for all non-binding/non-inert factors that affect the trace.
        risk_left, risk_left_value, risk_right, risk_right_value, _, _ = spec.interaction
        single_unsafe_slots = []
        base_skeleton = skeleton(base_trace)
        for slot, values in spec.alternatives.items():
            if slot in spec.binding_slots or slot == spec.inert_slot or slot in (risk_left, risk_right):
                continue
            if skeleton(spec.trace(mutate(spec.base, **{slot: values[0]}))) != base_skeleton:
                single_unsafe_slots.append(slot)
                variants.append((f"single:{slot}", mutate(spec.base, **{slot: values[0]})))
        # Pair interaction is invisible to all single-factor probes.
        variants.append(("interaction", mutate(spec.base, **{risk_left: risk_left_value, risk_right: risk_right_value})))
        # Add structural+binding near-neighbors until every domain contributes 16 cases.
        cursor = 0
        while len(variants) < 16:
            structural_slot = single_unsafe_slots[cursor % len(single_unsafe_slots)]
            bind_slot = spec.binding_slots[cursor % len(spec.binding_slots)]
            variants.append((
                f"combined:{structural_slot}+{bind_slot}",
                mutate(spec.base, **{
                    structural_slot: spec.alternatives[structural_slot][0],
                    bind_slot: spec.alternatives[bind_slot][cursor % len(spec.alternatives[bind_slot])],
                }),
            ))
            cursor += 1
        rng.shuffle(variants)
        for index, (kind, slots) in enumerate(variants):
            trace = spec.trace(slots)
            compatible = skeleton(trace) == base_skeleton
            cases.append({
                "id": f"{spec.key}-{index:02d}",
                "domain": spec.key,
                "kind": kind,
                "request": spec.render(slots),
                "slots": slots,
                "gold_trace": trace,
                "gold_skeleton": list(skeleton(trace)),
                "compatible": compatible,
                "split": "calibration" if index % 4 == 0 else "test",
            })
    return caches, cases


def http_json(path: str, payload: dict[str, Any], timeout: int = 600) -> dict[str, Any]:
    request = urllib.request.Request(
        OLLAMA_URL + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:2000]
        raise RuntimeError(f"Ollama request failed for {path}: HTTP {exc.code}: {body}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Ollama request failed for {path}: {type(exc).__name__}: {exc}") from exc


def ollama_embeddings(texts: list[str]) -> tuple[np.ndarray, dict[str, Any]]:
    batch_size = 32
    rows: list[list[float]] = []
    responses: list[dict[str, Any]] = []
    for start in range(0, len(texts), batch_size):
        response = http_json(
            "/api/embed",
            {"model": EMBED_MODEL, "input": texts[start:start + batch_size], "truncate": True},
        )
        rows.extend(response["embeddings"])
        responses.append({key: response.get(key) for key in (
            "model", "total_duration", "load_duration", "prompt_eval_count",
        )})
    vectors = np.asarray(rows, dtype=np.float32)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    vectors = vectors / np.maximum(norms, 1e-12)
    meta = {"model": EMBED_MODEL, "batch_size": batch_size, "calls": len(responses), "responses": responses}
    return vectors, meta


def json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("model response contains no JSON object")
    value = json.loads(match.group(0))
    if not isinstance(value, dict):
        raise ValueError("model JSON is not an object")
    return value


def ollama_json(prompt: str) -> tuple[dict[str, Any], dict[str, Any]]:
    response = http_json("/api/chat", {
        "model": PARSER_MODEL,
        "messages": [
            {"role": "system", "content": "Return only valid JSON. Do not explain."},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "format": "json",
        "think": False,
        "options": {"temperature": 0, "seed": 20260802, "num_ctx": 16384},
    })
    content = response["message"]["content"]
    parsed = json_object(content)
    meta = {key: response.get(key) for key in (
        "model", "created_at", "done_reason", "total_duration", "load_duration",
        "prompt_eval_count", "eval_count",
    )}
    return parsed, meta


def parse_slots_with_qwen(specs: list[DomainSpec], cases: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    parsed_by_id: dict[str, dict[str, Any]] = {}
    calls: list[dict[str, Any]] = []
    for spec in specs:
        domain_cases = [case for case in cases if case["domain"] == spec.key]
        allowed = {slot: [spec.base[slot], *spec.alternatives[slot]] for slot in spec.ordered_slots}
        payload = [{"id": case["id"], "request": case["request"]} for case in domain_cases]
        prompt = (
            "Extract every slot for each request. Use exactly the listed slot names and one of the listed allowed values. "
            "Boolean values must be JSON true/false. Return {\"items\":[{\"id\":...,\"slots\":{...}}]}.\n"
            f"Domain: {spec.key}\nAllowed schema: {json.dumps(allowed, ensure_ascii=False)}\n"
            f"Requests: {json.dumps(payload, ensure_ascii=False)}"
        )
        started = time.time()
        try:
            result, meta = ollama_json(prompt)
            items = result.get("items", [])
            if not isinstance(items, list):
                items = []
            for item in items:
                if isinstance(item, dict) and isinstance(item.get("id"), str) and isinstance(item.get("slots"), dict):
                    parsed_by_id[item["id"]] = item["slots"]
            calls.append({"domain": spec.key, "ok": True, "elapsed_seconds": time.time() - started,
                          "returned_items": len(items), "meta": meta})
        except Exception as exc:  # Preserve failure as evidence; downstream treats missing parse as reject.
            calls.append({"domain": spec.key, "ok": False, "elapsed_seconds": time.time() - started,
                          "error": f"{type(exc).__name__}: {exc}"})
    return parsed_by_id, calls


def qwen_reuse_judgments(specs: list[DomainSpec], caches: list[dict[str, Any]], cases: list[dict[str, Any]]) -> tuple[dict[str, bool], list[dict[str, Any]]]:
    judgments: dict[str, bool] = {}
    calls: list[dict[str, Any]] = []
    cache_by_domain = {cache["domain"]: cache for cache in caches}
    for spec in specs:
        cache = cache_by_domain[spec.key]
        domain_cases = [case for case in cases if case["domain"] == spec.key]
        prompt = (
            "Decide whether the cached tool plan can handle each new request by changing argument values only. "
            "Return reuse=false if any tool step must be added, removed, replaced, or reordered, including checks, "
            "approvals, policy reads, or safety actions. Return {\"items\":[{\"id\":...,\"reuse\":true/false}]}.\n"
            f"Cached request: {cache['request']}\nCached tool plan: {json.dumps(cache['skeleton'])}\n"
            f"New requests: {json.dumps([{'id': c['id'], 'request': c['request']} for c in domain_cases], ensure_ascii=False)}"
        )
        started = time.time()
        try:
            result, meta = ollama_json(prompt)
            items = result.get("items", [])
            if not isinstance(items, list):
                items = []
            for item in items:
                if isinstance(item, dict) and isinstance(item.get("id"), str) and isinstance(item.get("reuse"), bool):
                    judgments[item["id"]] = item["reuse"]
            calls.append({"domain": spec.key, "ok": True, "elapsed_seconds": time.time() - started,
                          "returned_items": len(items), "meta": meta})
        except Exception as exc:
            calls.append({"domain": spec.key, "ok": False, "elapsed_seconds": time.time() - started,
                          "error": f"{type(exc).__name__}: {exc}"})
    return judgments, calls


def infer_signature(spec: DomainSpec, pairwise: bool) -> dict[str, Any]:
    base_skeleton = skeleton(spec.trace(spec.base))
    sensitive: dict[str, list[Any]] = {}
    single_probe_count = 0
    for slot, alternatives in spec.alternatives.items():
        changed = []
        for value in alternatives:
            single_probe_count += 1
            if skeleton(spec.trace(mutate(spec.base, **{slot: value}))) != base_skeleton:
                changed.append(value)
        if changed:
            sensitive[slot] = changed
    interactions: list[dict[str, Any]] = []
    pairwise_probe_count = 0
    if pairwise:
        slots = list(spec.alternatives)
        for left, right in combinations(slots, 2):
            for left_value in spec.alternatives[left]:
                for right_value in spec.alternatives[right]:
                    left_skeleton = skeleton(spec.trace(mutate(spec.base, **{left: left_value})))
                    right_skeleton = skeleton(spec.trace(mutate(spec.base, **{right: right_value})))
                    if left_skeleton != base_skeleton or right_skeleton != base_skeleton:
                        continue
                    pairwise_probe_count += 1
                    both_skeleton = skeleton(spec.trace(mutate(spec.base, **{left: left_value, right: right_value})))
                    if both_skeleton != base_skeleton:
                        interactions.append({"left": left, "left_value": left_value,
                                             "right": right, "right_value": right_value})
    return {
        "sensitive": sensitive,
        "interactions": interactions,
        "conceptual_probe_count": 1 + single_probe_count + pairwise_probe_count,
        "single_probe_count": single_probe_count,
        "pairwise_probe_count": pairwise_probe_count,
    }


def signature_accepts(spec: DomainSpec, signature: dict[str, Any], slots: dict[str, Any] | None) -> bool:
    if slots is None:
        return False
    # Missing, unknown, or out-of-schema values make the matcher conservatively reject.
    for slot in spec.ordered_slots:
        if slot not in slots:
            return False
        allowed = [spec.base[slot], *spec.alternatives[slot]]
        if slots[slot] not in allowed:
            return False
    for slot, values in signature["sensitive"].items():
        if slots[slot] in values:
            return False
    for relation in signature["interactions"]:
        if (slots[relation["left"]] == relation["left_value"] and
                slots[relation["right"]] == relation["right_value"]):
            return False
    return True


def cosine_scores_tfidf(caches: list[dict[str, Any]], cases: list[dict[str, Any]]) -> dict[str, float]:
    cache_by_domain = {cache["domain"]: cache for cache in caches}
    documents = [cache_by_domain[case["domain"]]["request"] for case in cases] + [case["request"] for case in cases]
    matrix = TfidfVectorizer(ngram_range=(1, 2), lowercase=True).fit_transform(documents)
    count = len(cases)
    return {case["id"]: float(matrix[index].multiply(matrix[index + count]).sum())
            for index, case in enumerate(cases)}


def cosine_scores_bge(caches: list[dict[str, Any]], cases: list[dict[str, Any]]) -> tuple[dict[str, float], dict[str, Any]]:
    cache_by_domain = {cache["domain"]: cache for cache in caches}
    texts = [cache_by_domain[case["domain"]]["request"] for case in cases] + [case["request"] for case in cases]
    vectors, meta = ollama_embeddings(texts)
    count = len(cases)
    scores = {case["id"]: float(np.dot(vectors[index], vectors[index + count]))
              for index, case in enumerate(cases)}
    return scores, meta


def choose_threshold(scores: dict[str, float], cases: list[dict[str, Any]]) -> float:
    calibration = [case for case in cases if case["split"] == "calibration"]
    candidates = sorted({scores[case["id"]] for case in calibration})
    candidates = [min(candidates) - 1e-6, *candidates, max(candidates) + 1e-6]
    best: tuple[float, float, float] | None = None
    for threshold in candidates:
        predictions = {case["id"]: scores[case["id"]] >= threshold for case in calibration}
        metrics = binary_metrics(calibration, predictions)
        # Wrong reuse is three times costlier than a missed reuse.
        utility = metrics["safe_recall"] - 3.0 * metrics["unsafe_accept_rate"]
        candidate = (utility, metrics["safe_recall"], threshold)
        if best is None or candidate > best:
            best = candidate
    assert best is not None
    return best[2]


def binary_metrics(cases: list[dict[str, Any]], predictions: dict[str, bool]) -> dict[str, Any]:
    tp = fp = tn = fn = missing = 0
    for case in cases:
        prediction = predictions.get(case["id"])
        if prediction is None:
            missing += 1
            prediction = False
        gold = bool(case["compatible"])
        if prediction and gold:
            tp += 1
        elif prediction and not gold:
            fp += 1
        elif not prediction and not gold:
            tn += 1
        else:
            fn += 1
    safe_total = tp + fn
    unsafe_total = fp + tn
    accepted = tp + fp
    return {
        "n": len(cases), "tp_safe_accept": tp, "fp_wrong_accept": fp,
        "tn_unsafe_reject": tn, "fn_safe_reject": fn, "missing_predictions": missing,
        "safe_recall": tp / safe_total if safe_total else 0.0,
        "unsafe_accept_rate": fp / unsafe_total if unsafe_total else 0.0,
        "wrong_per_100_accepts": 100.0 * fp / accepted if accepted else 0.0,
        "balanced_accuracy": 0.5 * ((tp / safe_total if safe_total else 0.0) +
                                    (tn / unsafe_total if unsafe_total else 0.0)),
        "accepted": accepted,
    }


def extraction_metrics(specs: list[DomainSpec], cases: list[dict[str, Any]], parsed: dict[str, dict[str, Any]]) -> dict[str, Any]:
    total_slots = correct_slots = exact_cases = 0
    by_slot: dict[str, list[int]] = {}
    for case in cases:
        spec = next(item for item in specs if item.key == case["domain"])
        candidate = parsed.get(case["id"], {})
        exact = True
        for slot in spec.ordered_slots:
            total_slots += 1
            correct = int(candidate.get(slot) == case["slots"][slot])
            correct_slots += correct
            by_slot.setdefault(slot, []).append(correct)
            exact = exact and bool(correct)
        exact_cases += int(exact)
    return {
        "case_count": len(cases), "parsed_case_count": len(parsed),
        "slot_accuracy": correct_slots / total_slots,
        "exact_case_accuracy": exact_cases / len(cases),
        "per_slot_accuracy": {slot: sum(values) / len(values) for slot, values in sorted(by_slot.items())},
    }


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()

    started = time.time()
    specs = build_specs()
    caches, cases = generate_cases(specs, args.seed)
    test_cases = [case for case in cases if case["split"] == "test"]

    tfidf_scores = cosine_scores_tfidf(caches, cases)
    tfidf_threshold = choose_threshold(tfidf_scores, cases)
    bge_scores, bge_meta = cosine_scores_bge(caches, cases)
    bge_threshold = choose_threshold(bge_scores, cases)

    parsed_slots, parser_calls = parse_slots_with_qwen(specs, cases)
    qwen_judgments, judge_calls = qwen_reuse_judgments(specs, caches, cases)

    signatures_1 = {spec.key: infer_signature(spec, pairwise=False) for spec in specs}
    signatures_2 = {spec.key: infer_signature(spec, pairwise=True) for spec in specs}
    spec_by_domain = {spec.key: spec for spec in specs}

    predictions: dict[str, dict[str, bool]] = {
        "keyword_intent": {case["id"]: True for case in cases},
        "tfidf": {case["id"]: tfidf_scores[case["id"]] >= tfidf_threshold for case in cases},
        "bge_m3": {case["id"]: bge_scores[case["id"]] >= bge_threshold for case in cases},
        "manual_partial_key": {},
        "exact_all_noninert_slots": {},
        "ecpc_single_gold_slots": {},
        "ecpc_pairwise_gold_slots": {},
        "ecpc_pairwise_qwen_slots": {},
        "qwen_direct_judge": qwen_judgments,
    }
    for case in cases:
        spec = spec_by_domain[case["domain"]]
        slots = case["slots"]
        predictions["manual_partial_key"][case["id"]] = all(
            slots[slot] == spec.base[slot] for slot in spec.manual_key_slots
        )
        predictions["exact_all_noninert_slots"][case["id"]] = all(
            slot == spec.inert_slot or slots[slot] == spec.base[slot] for slot in spec.ordered_slots
        )
        predictions["ecpc_single_gold_slots"][case["id"]] = signature_accepts(
            spec, signatures_1[spec.key], slots
        )
        predictions["ecpc_pairwise_gold_slots"][case["id"]] = signature_accepts(
            spec, signatures_2[spec.key], slots
        )
        predictions["ecpc_pairwise_qwen_slots"][case["id"]] = signature_accepts(
            spec, signatures_2[spec.key], parsed_slots.get(case["id"])
        )

    metrics = {method: binary_metrics(test_cases, values) for method, values in predictions.items()}
    metrics_by_domain = {
        method: {
            spec.key: binary_metrics([case for case in test_cases if case["domain"] == spec.key], values)
            for spec in specs
        }
        for method, values in predictions.items()
    }
    labels = [int(case["compatible"]) for case in test_cases]
    score_diagnostics = {}
    for name, scores in (("tfidf", tfidf_scores), ("bge_m3", bge_scores)):
        test_scores = [scores[case["id"]] for case in test_cases]
        score_diagnostics[name] = {
            "threshold": tfidf_threshold if name == "tfidf" else bge_threshold,
            "roc_auc": float(roc_auc_score(labels, test_scores)),
            "mean_safe": float(np.mean([scores[c["id"]] for c in test_cases if c["compatible"]])),
            "mean_unsafe": float(np.mean([scores[c["id"]] for c in test_cases if not c["compatible"]])),
        }

    result = {
        "schema_version": 1,
        "experiment": "execution-counterfactual plan-cache controlled probe",
        "seed": args.seed,
        "scope": {
            "domains": len(specs), "cases_total": len(cases), "cases_test": len(test_cases),
            "safe_test": sum(int(c["compatible"]) for c in test_cases),
            "unsafe_test": sum(int(not c["compatible"]) for c in test_cases),
            "note": "Controlled synthetic workflows with deterministic reference traces; not a real-world benchmark.",
        },
        "models": {
            "embedding": EMBED_MODEL, "parser_and_direct_judge": PARSER_MODEL,
            "ollama_url": OLLAMA_URL, "embedding_response": bge_meta,
        },
        "metrics_test": metrics,
        "metrics_test_by_domain": metrics_by_domain,
        "score_diagnostics": score_diagnostics,
        "slot_extraction": extraction_metrics(specs, cases, parsed_slots),
        "signatures": {"single": signatures_1, "pairwise": signatures_2},
        "model_calls": {"parser": parser_calls, "direct_judge": judge_calls},
        "dataset_sha256": stable_hash({"caches": caches, "cases": cases}),
        "predictions_sha256": stable_hash(predictions),
        "elapsed_seconds": time.time() - started,
        "cases": cases,
        "predictions": predictions,
        "parsed_slots": parsed_slots,
        "continuous_scores": {"tfidf": tfidf_scores, "bge_m3": bge_scores},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    compact = {
        "output": str(args.output), "dataset_sha256": result["dataset_sha256"],
        "elapsed_seconds": result["elapsed_seconds"], "scope": result["scope"],
        "metrics_test": metrics, "slot_extraction": result["slot_extraction"],
        "score_diagnostics": score_diagnostics,
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
