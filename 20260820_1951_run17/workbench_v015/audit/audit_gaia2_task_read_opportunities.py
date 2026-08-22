from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import polars as pl


CONFIGS = ("execution", "search", "adaptability", "time", "ambiguity")

# These high-precision lexical rules were fixed from the local tool contracts before
# inspecting aggregate matches. A match is an opportunity cue, never an observed call.
CUE_RULES = {
    "city_crime_information": {
        "required_classes": {"CityApp"},
        "methods": ["CityApp.get_crime_rate"],
        "patterns": [
            r"\b(?:crime|violent crime|property crime)\b.{0,100}\b(?:rate|statistics?|compare|comparison|safer|safest|dangerous|danger)\b",
            r"\b(?:rate|statistics?|compare|comparison|safer|safest|dangerous|danger)\b.{0,100}\b(?:crime|violent crime|property crime)\b",
        ],
    },
    "cab_quote_information": {
        "required_classes": {"CabApp"},
        "methods": ["CabApp.get_quotation", "CabApp.list_rides"],
        "patterns": [
            r"\b(?:cab|taxi|ride)\b.{0,100}\b(?:quote|quotation|fare|price|cost|cheapest|expensive|estimate)\b",
            r"\b(?:quote|quotation|fare|price|cost|cheapest|expensive|estimate)\b.{0,100}\b(?:cab|taxi|ride)\b",
        ],
    },
    "timed_wait_for_response": {
        "required_classes": {"SystemApp"},
        "methods": ["SystemApp.wait_for_notification"],
        "patterns": [
            r"\b(?:wait|unless|if)\b.{0,140}\b(?:reply|respond|response|notification)\b.{0,100}\b(?:second|seconds|minute|minutes|hour|hours)\b",
            r"\b(?:second|seconds|minute|minutes|hour|hours)\b.{0,100}\b(?:reply|respond|response|notification)\b",
        ],
    },
    "explicit_email_read": {
        "required_classes": {"EmailClientApp", "EmailClientV2", "Mail"},
        "methods": [
            "EmailClientApp.get_email_by_id",
            "EmailClientApp.get_email_by_index",
        ],
        "patterns": [
            r"\b(?:read|open|unread|mark)\b.{0,60}\b(?:email|emails|mail)\b",
            r"\b(?:email|emails|mail)\b.{0,60}\b(?:read|open|unread|mark)\b",
        ],
    },
    "explicit_unread_message": {
        "required_classes": {"AgentUserInterface"},
        "methods": ["AgentUserInterface.get_last_unread_messages"],
        "patterns": [
            r"\bunread\b.{0,60}\b(?:message|messages|reply|response)\b",
            r"\b(?:message|messages|reply|response)\b.{0,60}\bunread\b",
        ],
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def decode_arg_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        return value
    return decoded


def action_args(action: dict[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for item in action.get("args") or []:
        if not isinstance(item, dict) or "name" not in item:
            continue
        output[str(item["name"])] = decode_arg_value(item.get("value"))
    return output


def user_texts(events: list[dict[str, Any]]) -> list[str]:
    output = []
    for event in events:
        if event.get("event_type") != "USER":
            continue
        action = event.get("action") or {}
        args = action_args(action)
        content = args.get("content")
        if isinstance(content, str) and content.strip():
            output.append(content.strip())
    return output


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def app_classes(apps: list[dict[str, Any]]) -> set[str]:
    classes = {
        str(app.get("class_name"))
        for app in apps
        if isinstance(app, dict) and app.get("class_name")
    }
    # The official imported-scenario path adds SystemApp when it is absent from
    # the serialized dataset, so it is an implicit capability of every row.
    classes.add("SystemApp")
    return classes


def oracle_functions(events: list[dict[str, Any]]) -> list[str]:
    functions = set()
    for event in events:
        if event.get("event_type") != "AGENT":
            continue
        action = event.get("action") or {}
        app = action.get("app")
        function = action.get("function")
        if function:
            functions.add(f"{app}.{function}" if app else str(function))
    return sorted(functions)


def match_rules(text: str, classes: set[str]) -> list[str]:
    normalized = normalize_text(text)
    matched = []
    for label, rule in CUE_RULES.items():
        if not (classes & rule["required_classes"]):
            continue
        if any(re.search(pattern, normalized) for pattern in rule["patterns"]):
            matched.append(label)
    return matched


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--dataset-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    file_manifest = []
    config_summaries: dict[str, Any] = {}
    all_matches: list[dict[str, Any]] = []
    overall_rule_counts: Counter[str] = Counter()
    overall_app_presence: Counter[str] = Counter()
    overall_oracle_functions: Counter[str] = Counter()
    total_rows = 0
    total_events = 0
    total_user_events = 0

    compiled_rules = {
        label: {
            "required_classes": sorted(rule["required_classes"]),
            "methods": rule["methods"],
            "patterns": rule["patterns"],
        }
        for label, rule in CUE_RULES.items()
    }

    for config in CONFIGS:
        path = (
            args.source_dir.resolve()
            / f"gaia2_{config}_validation.parquet"
        )
        if not path.is_file():
            raise FileNotFoundError(path)
        file_manifest.append(
            {
                "config": config,
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

        frame = pl.read_parquet(path, columns=["id", "scenario_id", "split", "data"])
        config_rule_counts: Counter[str] = Counter()
        config_app_presence: Counter[str] = Counter()
        config_oracle_functions: Counter[str] = Counter()
        config_events = 0
        config_user_events = 0
        config_match_count = 0

        assert frame.height == 160
        assert set(frame["split"].to_list()) == {"validation"}

        for row in frame.iter_rows(named=True):
            payload = json.loads(row["data"])
            events = payload.get("events") or []
            apps = payload.get("apps") or []
            texts = user_texts(events)
            classes = app_classes(apps)
            initial_text = texts[0] if texts else ""
            combined_text = "\n".join(texts)
            initial_matches = match_rules(initial_text, classes)
            any_user_event_matches = match_rules(combined_text, classes)
            functions = oracle_functions(events)

            config_events += len(events)
            config_user_events += len(texts)
            for label, rule in CUE_RULES.items():
                if classes & rule["required_classes"]:
                    config_app_presence[label] += 1
            for label in any_user_event_matches:
                config_rule_counts[label] += 1
            for function in functions:
                config_oracle_functions[function] += 1

            if any_user_event_matches:
                config_match_count += 1
                identity = (
                    f"{config}\0{row['id']}\0{row['scenario_id']}"
                )
                all_matches.append(
                    {
                        "scenario_identity_sha256": sha256_text(identity),
                        "task_text_sha256": sha256_text(combined_text),
                        "user_event_count": len(texts),
                        "initial_task_cues": initial_matches,
                        "all_user_event_cues": any_user_event_matches,
                        "oracle_write_functions": functions,
                    }
                )

        total_rows += frame.height
        total_events += config_events
        total_user_events += config_user_events
        overall_rule_counts.update(config_rule_counts)
        overall_app_presence.update(config_app_presence)
        overall_oracle_functions.update(config_oracle_functions)
        config_summaries[config] = {
            "rows": frame.height,
            "events": config_events,
            "user_events_with_text": config_user_events,
            "scenarios_with_any_explicit_cue": config_match_count,
            "cue_counts": dict(sorted(config_rule_counts.items())),
            "relevant_app_presence_counts": dict(
                sorted(config_app_presence.items())
            ),
            "oracle_write_function_counts": dict(
                sorted(config_oracle_functions.items())
            ),
        }

    matches_by_oracle_function: dict[str, Counter[str]] = defaultdict(Counter)
    for match in all_matches:
        for function in match["oracle_write_functions"]:
            for label in match["all_user_event_cues"]:
                matches_by_oracle_function[label][function] += 1

    result = {
        "source": {
            "dataset": "meta-agents-research-environments/gaia2",
            "dataset_revision": args.dataset_revision,
            "split": "validation",
            "configs": list(CONFIGS),
            "parquet_files": file_manifest,
            "are_repository": "facebookresearch/meta-agents-research-environments",
            "are_revision": git_revision(args.are_root.resolve()),
            "python": sys.executable,
            "polars": pl.__version__,
        },
        "frozen_cue_contract": compiled_rules,
        "aggregate": {
            "scenario_count": total_rows,
            "event_count": total_events,
            "user_events_with_text": total_user_events,
            "scenarios_with_any_explicit_cue": len(all_matches),
            "scenario_fraction_with_any_explicit_cue": len(all_matches)
            / total_rows,
            "cue_counts": dict(sorted(overall_rule_counts.items())),
            "relevant_app_presence_counts": dict(
                sorted(overall_app_presence.items())
            ),
            "matched_cue_by_oracle_write_function": {
                label: dict(sorted(counter.items()))
                for label, counter in sorted(matches_by_oracle_function.items())
            },
        },
        "by_config": config_summaries,
        "matched_scenarios_without_text": all_matches,
        "interpretation_boundary": (
            "This is an exact denominator over 800 official validation scenarios but "
            "only a conservative lexical opportunity audit. It reports task or later "
            "user-event wording compatible with confirmed effectful READ contracts when "
            "the relevant app class is present. It does not observe model tool calls, "
            "prove that the effectful method is necessary, estimate score-collision "
            "prevalence, or establish ranking impact. Task text is never emitted; only "
            "SHA-256 identities, cue labels, and oracle write function names are retained."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
