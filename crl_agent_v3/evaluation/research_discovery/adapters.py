from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .core import (
    SYSTEM_TYPES,
    canonical_sha256,
    load_json_file,
    validate_system_output,
)


def import_system_output(
    path: str | Path,
    source_format: str,
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    """Import one offline result file; this function never invokes a model or network."""

    if source_format not in SYSTEM_TYPES:
        raise ValueError(f"unsupported system import format: {source_format!r}")
    raw, source_sha256 = load_json_file(path)
    if source_format == "bare_llm":
        candidates = _array(raw.get("responses"), "responses")
        paper_ids: list[str] = []
        artifact_ids = _text_array(raw.get("prompt_artifact_ids", []), "prompt_artifact_ids")
    elif source_format == "passage_rag":
        candidates = _array(raw.get("hypotheses"), "hypotheses")
        retrieval = _object(raw.get("retrieval"), "retrieval")
        paper_ids = _text_array(retrieval.get("paper_ids"), "retrieval.paper_ids")
        artifact_ids = _text_array(retrieval.get("passage_ids"), "retrieval.passage_ids")
    elif source_format == "card_only":
        candidates = _array(raw.get("ideas"), "ideas")
        cards = _array(raw.get("cards"), "cards")
        paper_ids = [
            _text(_object(item, "card").get("paper_id"), "card.paper_id")
            for item in cards
        ]
        artifact_ids = [
            _text(_object(item, "card").get("card_id"), "card.card_id")
            for item in cards
        ]
    elif source_format == "current_crl":
        portfolio = _object(raw.get("portfolio"), "portfolio")
        candidates = _portfolio_candidates(portfolio, raw.get("candidate_facts", {}))
        paper_ids = _text_array(raw.get("visible_paper_ids", []), "visible_paper_ids")
        artifact_ids = _text_array(raw.get("run_local_artifact_ids", []), "run_local_artifact_ids")
    else:
        portfolio = _object(raw.get("portfolio"), "portfolio")
        candidates = _portfolio_candidates(portfolio, raw.get("candidate_facts", {}))
        search = _object(raw.get("scientific_search"), "scientific_search")
        paper_ids = _text_array(search.get("visible_paper_ids"), "scientific_search.visible_paper_ids")
        artifact_ids = _text_array(search.get("artifact_ids"), "scientific_search.artifact_ids")

    configuration = _object(raw.get("system_configuration"), "system_configuration")
    provenance = _object(raw.get("provenance"), "provenance")
    output = {
        "schema_version": 1,
        "task_id": _text(raw.get("task_id"), "task_id"),
        "system_id": _text(raw.get("system_id"), "system_id"),
        "system_type": source_format,
        "system_configuration": configuration,
        "configuration_sha256": canonical_sha256(configuration),
        "random_seed": raw.get("random_seed"),
        "input_trace": {
            "paper_ids": sorted(set(paper_ids)),
            "artifact_ids": sorted(set(artifact_ids)),
            "task_packet_sha256": _text(
                raw.get("task_packet_sha256"), "task_packet_sha256"
            ),
        },
        "provenance": {
            "source_format": source_format,
            "generated_at_utc": _text(
                provenance.get("generated_at_utc"), "provenance.generated_at_utc"
            ),
            "model": _text(provenance.get("model"), "provenance.model"),
            "provider": _text(provenance.get("provider"), "provenance.provider"),
            "prompt_revision": _text(
                provenance.get("prompt_revision"), "provenance.prompt_revision"
            ),
            "imported_from_sha256": source_sha256,
        },
        "cost": raw.get("cost"),
        "candidates": candidates,
        "candidate_payload_sha256": canonical_sha256(candidates),
    }
    validated = validate_system_output(output, manifest)
    validated["_source_path"] = str(Path(path))
    return validated


def _portfolio_candidates(portfolio: Mapping[str, Any], facts_value: object) -> list[dict[str, Any]]:
    hypotheses = _array(portfolio.get("hypotheses"), "portfolio.hypotheses")
    facts = _object(facts_value, "candidate_facts")
    result: list[dict[str, Any]] = []
    for raw in hypotheses:
        hypothesis = _object(raw, "portfolio hypothesis")
        candidate_id = _text(hypothesis.get("hypothesis_id"), "hypothesis_id")
        extra = _object(facts.get(candidate_id, {}), f"candidate_facts.{candidate_id}")
        result.append(
            {
                "candidate_id": candidate_id,
                "title": hypothesis.get("title", ""),
                "problem": hypothesis.get("problem", ""),
                "mechanism_claim": hypothesis.get("mechanism_claim", ""),
                "descriptors": hypothesis.get("descriptors", _empty_descriptors()),
                "changed_computation": hypothesis.get(
                    "changed_computation", _empty_changed_computation()
                ),
                "falsifier": extra.get(
                    "falsifier",
                    {
                        "statement": hypothesis.get("falsifier", ""),
                        "observable": "",
                        "decision_rule": "",
                    },
                ),
                "killer_experiment": extra.get(
                    "killer_experiment",
                    {
                        "experiment_id": "",
                        "research_question": hypothesis.get(
                            "minimal_killer_experiment", ""
                        ),
                        "independent_ground_truth": "",
                        "primary_metric": "",
                        "sampling_unit": "",
                        "baseline_ids": [],
                    },
                ),
                "visible_prior_audit": extra.get(
                    "visible_prior_audit",
                    {
                        "performed": False,
                        "audited_visible_paper_ids": [],
                        "collision_visible_paper_ids": [],
                    },
                ),
                "implementation": extra.get(
                    "implementation",
                    {"status": "not_started", "artifact_sha256s": []},
                ),
                "outcome": extra.get(
                    "outcome",
                    {
                        "status": "unresolved",
                        "decision_stage": "none",
                        "decision_reason": "",
                    },
                ),
                "empirical_evaluations": extra.get("empirical_evaluations", []),
            }
        )
    return result


def _empty_descriptors() -> dict[str, str]:
    return {
        "problem_family": "",
        "computation_stage": "",
        "intervention_family": "",
        "information_source": "",
        "timing_class": "",
        "budget_class": "",
        "evaluation_mode": "",
    }


def _empty_changed_computation() -> dict[str, str]:
    return {
        "baseline": "",
        "intervention": "",
        "information_available": "",
        "timing": "",
        "budget_effect": "",
    }


def _object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return dict(value)


def _array(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def _text_array(value: object, label: str) -> list[str]:
    items = _array(value, label)
    return [_text(item, label) for item in items]


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be non-empty text")
    return value
