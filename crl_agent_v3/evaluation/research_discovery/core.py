from __future__ import annotations

import hashlib
import json
import math
import random
import re
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = 1
SYSTEM_TYPES = (
    "bare_llm",
    "passage_rag",
    "card_only",
    "current_crl",
    "crl_scientific_search",
)
DESCRIPTOR_FIELDS = (
    "problem_family",
    "computation_stage",
    "intervention_family",
    "information_source",
    "timing_class",
    "budget_class",
    "evaluation_mode",
)
CHANGED_COMPUTATION_FIELDS = (
    "baseline",
    "intervention",
    "information_available",
    "timing",
    "budget_effect",
)
FALSIFIER_FIELDS = ("statement", "observable", "decision_rule")
KILLER_EXPERIMENT_FIELDS = (
    "experiment_id",
    "research_question",
    "independent_ground_truth",
    "primary_metric",
    "sampling_unit",
    "baseline_ids",
)
COST_FIELDS = (
    "tokens",
    "api_calls",
    "wall_time_seconds",
    "gpu_time_seconds",
    "estimated_cost_usd",
)
EARLY_KILL_STAGES = {"proposal", "prior_audit", "falsification_design"}
LATE_KILL_STAGES = {"implementation", "matched_baseline"}
OUTCOME_STATUSES = {"survived", "early_killed", "late_killed", "unresolved"}
IMPLEMENTATION_STATUSES = {"not_started", "attempted_failed", "implemented"}
PARITY_STATUSES = {"matched", "mismatched", "unknown", "not_applicable"}
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def canonical_sha256(value: object) -> str:
    data = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json_file(path: str | Path) -> tuple[dict[str, Any], str]:
    source = Path(path)
    data = source.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"JSON must be UTF-8 without BOM: {source}")
    if b"\r" in data:
        raise ValueError(f"JSON must use LF newlines: {source}")
    try:
        text = data.decode("utf-8", errors="strict")
        value = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid UTF-8 JSON: {source}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {source}")
    return value, hashlib.sha256(data).hexdigest()


def load_task_manifest(path: str | Path) -> dict[str, Any]:
    value, source_sha256 = load_json_file(path)
    manifest = validate_task_manifest(value)
    manifest["_source_sha256"] = source_sha256
    return manifest


def validate_task_manifest(value: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version",
        "task_id",
        "agent_subfield",
        "research_question",
        "temporal_visibility",
        "heldout_paper_ids",
        "paper_timeline",
        "resource_budget",
        "known_strong_baselines",
        "blinding",
        "human_annotation_instructions",
        "system_profiles",
        "synthetic_fixture",
        "synthetic_notice",
    }
    mapping = _mapping(value, "TaskManifest")
    _exact_fields(mapping, required, "TaskManifest")
    _schema_one(mapping, "TaskManifest")
    task_id = _identifier(mapping["task_id"], "task_id")
    _required_text(mapping["agent_subfield"], "agent_subfield")
    _required_text(mapping["research_question"], "research_question")

    visibility = _mapping(mapping["temporal_visibility"], "temporal_visibility")
    _exact_fields(
        visibility,
        {"cutoff", "visible_paper_ids", "visible_artifact_ids"},
        "temporal_visibility",
    )
    visible_ids = _unique_identifiers(
        visibility["visible_paper_ids"], "visible_paper_ids"
    )
    _text_list(visibility["visible_artifact_ids"], "visible_artifact_ids")
    cutoff = visibility["cutoff"]
    if cutoff is not None:
        cutoff_mapping = _mapping(cutoff, "temporal_visibility.cutoff")
        _exact_fields(cutoff_mapping, {"precision", "value"}, "cutoff")
        precision = cutoff_mapping["precision"]
        if precision == "day":
            _date_value(cutoff_mapping["value"], "cutoff.value")
        elif precision == "year":
            _year_value(cutoff_mapping["value"], "cutoff.value")
        else:
            raise ValueError("cutoff.precision must be 'day' or 'year'")
    if cutoff is None and not visible_ids:
        raise ValueError("TaskManifest requires a cutoff or explicit visible_paper_ids")

    heldout_ids = _unique_identifiers(mapping["heldout_paper_ids"], "heldout_paper_ids")
    overlap = set(visible_ids) & set(heldout_ids)
    if overlap:
        raise ValueError(f"visible and held-out paper IDs overlap: {sorted(overlap)}")

    timeline = _paper_timeline(mapping["paper_timeline"])
    timeline_ids = {item["paper_id"] for item in timeline}
    missing_timeline = (set(visible_ids) | set(heldout_ids)) - timeline_ids
    if missing_timeline:
        raise ValueError(f"paper_timeline is missing paper IDs: {sorted(missing_timeline)}")
    _validate_temporal_membership(cutoff, visible_ids, heldout_ids, timeline)

    _resource_budget(mapping["resource_budget"])
    baselines = _list(mapping["known_strong_baselines"], "known_strong_baselines")
    baseline_ids: list[str] = []
    for index, item in enumerate(baselines):
        baseline = _mapping(item, f"known_strong_baselines[{index}]")
        _exact_fields(baseline, {"baseline_id", "description"}, "strong baseline")
        baseline_ids.append(_identifier(baseline["baseline_id"], "baseline_id"))
        _required_text(baseline["description"], "baseline description")
    _require_unique(baseline_ids, "baseline IDs")

    blinding = _mapping(mapping["blinding"], "blinding")
    _exact_fields(
        blinding,
        {
            "system_identity_hidden_from_experts",
            "candidate_order_randomized",
            "heldout_not_in_system_input",
        },
        "blinding",
    )
    for name, flag in blinding.items():
        if type(flag) is not bool:
            raise ValueError(f"blinding.{name} must be boolean")
    if not all(blinding.values()):
        raise ValueError("all TaskManifest blinding guarantees must be true")
    _required_text(
        mapping["human_annotation_instructions"], "human_annotation_instructions"
    )

    profiles = _list(mapping["system_profiles"], "system_profiles")
    profile_ids: list[str] = []
    for index, item in enumerate(profiles):
        profile = _mapping(item, f"system_profiles[{index}]")
        _exact_fields(
            profile,
            {"system_id", "system_type", "configuration_sha256"},
            "system profile",
        )
        profile_ids.append(_identifier(profile["system_id"], "system_id"))
        if profile["system_type"] not in SYSTEM_TYPES:
            raise ValueError(f"invalid system_type: {profile['system_type']!r}")
        _sha256_value(profile["configuration_sha256"], "configuration_sha256")
    _require_unique(profile_ids, "system profile IDs")

    if type(mapping["synthetic_fixture"]) is not bool:
        raise ValueError("synthetic_fixture must be boolean")
    notice = mapping["synthetic_notice"]
    if mapping["synthetic_fixture"]:
        _required_text(notice, "synthetic_notice")
        if "不代表真实科研能力" not in notice:
            raise ValueError("synthetic fixture notice must state 不代表真实科研能力")
    elif not isinstance(notice, str):
        raise ValueError("synthetic_notice must be text")

    normalized = dict(mapping)
    normalized["task_id"] = task_id
    return normalized


def build_visible_task_packet(manifest: Mapping[str, Any]) -> dict[str, Any]:
    validated = validate_task_manifest(_without_internal_fields(manifest))
    visible_ids, ambiguity = derive_visible_paper_ids(validated)
    packet = {
        "schema_version": 1,
        "task_id": validated["task_id"],
        "agent_subfield": validated["agent_subfield"],
        "research_question": validated["research_question"],
        "temporal_visibility": {
            "cutoff": validated["temporal_visibility"]["cutoff"],
            "visible_paper_ids": visible_ids,
            "visible_artifact_ids": sorted(
                set(validated["temporal_visibility"]["visible_artifact_ids"])
            ),
            "year_precision_ambiguity": ambiguity,
        },
        "resource_budget": validated["resource_budget"],
        "known_strong_baselines": validated["known_strong_baselines"],
    }
    _assert_no_heldout_leak(packet, validated["heldout_paper_ids"], "task packet")
    return packet


def derive_visible_paper_ids(
    manifest: Mapping[str, Any],
) -> tuple[list[str], dict[str, Any]]:
    visibility = manifest["temporal_visibility"]
    explicit = set(visibility["visible_paper_ids"])
    cutoff = visibility["cutoff"]
    derived: set[str] = set()
    ambiguous: set[str] = set()
    if cutoff is not None:
        precision = cutoff["precision"]
        cutoff_year = int(str(cutoff["value"])[:4])
        cutoff_day = str(cutoff["value"]) if precision == "day" else None
        for item in manifest["paper_timeline"]:
            paper_id = item["paper_id"]
            if paper_id in manifest["heldout_paper_ids"]:
                continue
            publication_date = item["publication_date"]
            publication_year = item["publication_year"]
            if publication_date is not None and cutoff_day is not None:
                if publication_date <= cutoff_day:
                    derived.add(paper_id)
                continue
            year = int(publication_date[:4]) if publication_date else publication_year
            if year is None:
                continue
            if year < cutoff_year:
                derived.add(paper_id)
            elif year == cutoff_year:
                ambiguous.add(paper_id)
    visible = sorted((derived | explicit) - set(manifest["heldout_paper_ids"]))
    return visible, {
        "paper_ids": sorted(ambiguous - explicit),
        "policy": (
            "Papers known only to share the cutoff year are not ordered or made "
            "visible unless explicitly listed."
        ),
    }


def validate_system_output(
    value: Mapping[str, Any], manifest: Mapping[str, Any]
) -> dict[str, Any]:
    required = {
        "schema_version",
        "task_id",
        "system_id",
        "system_type",
        "system_configuration",
        "configuration_sha256",
        "random_seed",
        "input_trace",
        "provenance",
        "cost",
        "candidates",
        "candidate_payload_sha256",
    }
    mapping = _mapping(value, "SystemOutput")
    _exact_fields(mapping, required, "SystemOutput")
    _schema_one(mapping, "SystemOutput")
    if mapping["task_id"] != manifest["task_id"]:
        raise ValueError("SystemOutput task_id does not match TaskManifest")
    system_id = _identifier(mapping["system_id"], "system_id")
    if mapping["system_type"] not in SYSTEM_TYPES:
        raise ValueError(f"invalid system_type: {mapping['system_type']!r}")
    configuration = _mapping(mapping["system_configuration"], "system_configuration")
    actual_config_sha = canonical_sha256(configuration)
    if mapping["configuration_sha256"] != actual_config_sha:
        raise ValueError("SystemOutput configuration_sha256 does not match configuration")
    profiles = {item["system_id"]: item for item in manifest["system_profiles"]}
    if system_id not in profiles:
        raise ValueError(f"SystemOutput system_id is not declared: {system_id!r}")
    expected = profiles[system_id]
    if expected["system_type"] != mapping["system_type"]:
        raise ValueError("SystemOutput system_type does not match TaskManifest profile")
    if expected["configuration_sha256"] != actual_config_sha:
        raise ValueError("SystemOutput configuration does not match TaskManifest profile")
    if type(mapping["random_seed"]) is not int:
        raise ValueError("random_seed must be an integer")

    trace = _mapping(mapping["input_trace"], "input_trace")
    _exact_fields(
        trace, {"paper_ids", "artifact_ids", "task_packet_sha256"}, "input_trace"
    )
    paper_ids = _unique_identifiers(trace["paper_ids"], "input_trace.paper_ids")
    artifact_ids = _text_list(trace["artifact_ids"], "input_trace.artifact_ids")
    unknown_artifacts = set(artifact_ids) - set(
        manifest["temporal_visibility"]["visible_artifact_ids"]
    )
    if unknown_artifacts:
        raise ValueError(
            f"system input contains non-visible artifact IDs: {sorted(unknown_artifacts)}"
        )
    _sha256_value(trace["task_packet_sha256"], "task_packet_sha256")
    expected_task_packet_sha = canonical_sha256(build_visible_task_packet(manifest))
    if trace["task_packet_sha256"] != expected_task_packet_sha:
        raise ValueError("SystemOutput task_packet_sha256 does not match visible task packet")
    allowed_visible, _ = derive_visible_paper_ids(manifest)
    not_visible = set(paper_ids) - set(allowed_visible)
    if not_visible:
        raise ValueError(f"system input contains non-visible paper IDs: {sorted(not_visible)}")

    provenance = _mapping(mapping["provenance"], "provenance")
    _exact_fields(
        provenance,
        {
            "source_format",
            "generated_at_utc",
            "model",
            "provider",
            "prompt_revision",
            "imported_from_sha256",
        },
        "provenance",
    )
    for name in ("source_format", "generated_at_utc", "model", "provider", "prompt_revision"):
        _required_text(provenance[name], f"provenance.{name}")
    _sha256_value(provenance["imported_from_sha256"], "imported_from_sha256")
    if mapping["cost"] is not None:
        _cost(mapping["cost"])

    candidates = _list(mapping["candidates"], "candidates")
    candidate_ids: list[str] = []
    for index, item in enumerate(candidates):
        candidate = _validate_candidate(item, f"candidates[{index}]", manifest)
        candidate_ids.append(candidate["candidate_id"])
    _require_unique(candidate_ids, "candidate IDs")
    if mapping["candidate_payload_sha256"] != canonical_sha256(candidates):
        raise ValueError("candidate_payload_sha256 does not match candidates")

    _assert_no_heldout_leak(mapping, manifest["heldout_paper_ids"], "SystemOutput")
    return dict(mapping)


def load_annotation_batch(path: str | Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    value, source_sha256 = load_json_file(path)
    batch = validate_annotation_batch(value, manifest)
    batch["_source_sha256"] = source_sha256
    return batch


def validate_annotation_batch(
    value: Mapping[str, Any], manifest: Mapping[str, Any]
) -> dict[str, Any]:
    required = {
        "schema_version",
        "task_id",
        "annotation_batch_id",
        "annotation_source",
        "authority",
        "used_for_primary_conclusions",
        "annotator_id_hash",
        "blinding",
        "sampling_unit",
        "annotations",
        "unblinding_map",
        "heldout_mechanism_assessments",
    }
    mapping = _mapping(value, "ExpertAnnotationBatch")
    _exact_fields(mapping, required, "ExpertAnnotationBatch")
    _schema_one(mapping, "ExpertAnnotationBatch")
    if mapping["task_id"] != manifest["task_id"]:
        raise ValueError("annotation task_id does not match TaskManifest")
    _identifier(mapping["annotation_batch_id"], "annotation_batch_id")
    source = mapping["annotation_source"]
    if source not in {"blinded_expert", "llm_auxiliary"}:
        raise ValueError("annotation_source must be blinded_expert or llm_auxiliary")
    if source == "blinded_expert":
        if mapping["authority"] != "primary_allowed":
            raise ValueError("blinded expert annotation authority must be primary_allowed")
        if mapping["used_for_primary_conclusions"] is not True:
            raise ValueError("blinded expert annotations must explicitly allow primary use")
    else:
        if mapping["authority"] != "auxiliary_only":
            raise ValueError("LLM judge authority must be auxiliary_only")
        if mapping["used_for_primary_conclusions"] is not False:
            raise ValueError("LLM judge cannot be used for primary conclusions")
    _sha256_value(mapping["annotator_id_hash"], "annotator_id_hash")
    if mapping["sampling_unit"] != "candidate_annotation":
        raise ValueError("annotation sampling_unit must be candidate_annotation")

    blinding = _mapping(mapping["blinding"], "annotation blinding")
    _exact_fields(
        blinding,
        {
            "system_identity_hidden",
            "candidate_order_randomized",
            "annotation_collected_before_unblinding",
            "packet_sha256",
        },
        "annotation blinding",
    )
    for name in (
        "system_identity_hidden",
        "candidate_order_randomized",
        "annotation_collected_before_unblinding",
    ):
        if type(blinding[name]) is not bool:
            raise ValueError(f"annotation blinding.{name} must be boolean")
    _sha256_value(blinding["packet_sha256"], "packet_sha256")
    if source == "blinded_expert" and not all(
        blinding[name]
        for name in (
            "system_identity_hidden",
            "candidate_order_randomized",
            "annotation_collected_before_unblinding",
        )
    ):
        raise ValueError("primary expert annotations must preserve all blinding guarantees")

    annotations = _list(mapping["annotations"], "annotations")
    annotation_refs: list[str] = []
    for index, item in enumerate(annotations):
        annotation = _mapping(item, f"annotations[{index}]")
        _exact_fields(
            annotation,
            {
                "blinded_candidate_id",
                "novelty",
                "significance",
                "technical_correctness",
                "overall_notes",
            },
            "expert annotation",
        )
        annotation_refs.append(
            _identifier(annotation["blinded_candidate_id"], "blinded_candidate_id")
        )
        for dimension in ("novelty", "significance", "technical_correctness"):
            _score(annotation[dimension], dimension)
        if not isinstance(annotation["overall_notes"], str):
            raise ValueError("overall_notes must be text")
    _require_unique(annotation_refs, "annotated blinded candidate IDs")

    mappings = _list(mapping["unblinding_map"], "unblinding_map")
    by_ref: dict[str, tuple[str, str]] = {}
    for index, item in enumerate(mappings):
        unblind = _mapping(item, f"unblinding_map[{index}]")
        _exact_fields(
            unblind,
            {"blinded_candidate_id", "system_id", "candidate_id"},
            "unblinding map item",
        )
        ref = _identifier(unblind["blinded_candidate_id"], "blinded_candidate_id")
        if ref in by_ref:
            raise ValueError(f"duplicate unblinding reference: {ref!r}")
        by_ref[ref] = (
            _identifier(unblind["system_id"], "system_id"),
            _identifier(unblind["candidate_id"], "candidate_id"),
        )
    if set(annotation_refs) - set(by_ref):
        raise ValueError("every annotation requires an unblinding map entry")

    assessments = _list(
        mapping["heldout_mechanism_assessments"], "heldout_mechanism_assessments"
    )
    heldout = set(manifest["heldout_paper_ids"])
    for index, item in enumerate(assessments):
        assessment = _mapping(item, f"heldout_mechanism_assessments[{index}]")
        _exact_fields(
            assessment,
            {
                "blinded_candidate_id",
                "heldout_paper_id",
                "mechanism_rediscovered",
                "mechanism_rationale",
                "simple_text_similarity",
            },
            "heldout mechanism assessment",
        )
        ref = _identifier(assessment["blinded_candidate_id"], "blinded_candidate_id")
        if ref not in by_ref:
            raise ValueError(f"unknown blinded candidate ID in held-out assessment: {ref!r}")
        paper_id = _identifier(assessment["heldout_paper_id"], "heldout_paper_id")
        if paper_id not in heldout:
            raise ValueError(f"assessment paper is not held out: {paper_id!r}")
        if type(assessment["mechanism_rediscovered"]) is not bool:
            raise ValueError("mechanism_rediscovered must be boolean")
        _required_text(assessment["mechanism_rationale"], "mechanism_rationale")
        similarity = assessment["simple_text_similarity"]
        if similarity is not None:
            _bounded_number(similarity, "simple_text_similarity", 0.0, 1.0)
    return dict(mapping)


def build_evaluation_report(
    manifest: Mapping[str, Any],
    system_outputs: Sequence[Mapping[str, Any]],
    annotation_batches: Sequence[Mapping[str, Any]] = (),
    *,
    bootstrap_replicates: int = 0,
    confidence_level: float = 0.95,
    random_seed: int = 0,
) -> dict[str, Any]:
    clean_manifest = validate_task_manifest(_without_internal_fields(manifest))
    if type(bootstrap_replicates) is not int or bootstrap_replicates < 0:
        raise ValueError("bootstrap_replicates must be a non-negative integer")
    _bounded_number(confidence_level, "confidence_level", 0.0, 1.0, strict=True)
    if type(random_seed) is not int:
        raise ValueError("evaluation random_seed must be an integer")
    outputs = [
        validate_system_output(_without_internal_fields(item), clean_manifest)
        for item in system_outputs
    ]
    system_ids = [item["system_id"] for item in outputs]
    _require_unique(system_ids, "evaluated system IDs")
    batches = [
        validate_annotation_batch(_without_internal_fields(item), clean_manifest)
        for item in annotation_batches
    ]
    known_candidates = {
        (output["system_id"], candidate["candidate_id"])
        for output in outputs
        for candidate in output["candidates"]
    }
    declared_system_ids = {
        item["system_id"] for item in clean_manifest["system_profiles"]
    }
    for batch in batches:
        for item in batch["unblinding_map"]:
            key = (item["system_id"], item["candidate_id"])
            if item["system_id"] not in declared_system_ids:
                raise ValueError(f"annotation maps to undeclared system: {item['system_id']!r}")
            if item["system_id"] in system_ids and key not in known_candidates:
                raise ValueError(f"annotation maps to unknown candidate: {key!r}")

    systems = [
        _evaluate_system(
            clean_manifest,
            output,
            batches,
            bootstrap_replicates=bootstrap_replicates,
            confidence_level=confidence_level,
            random_seed=random_seed,
        )
        for output in sorted(outputs, key=lambda item: item["system_id"])
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "task": {
            "task_id": clean_manifest["task_id"],
            "agent_subfield": clean_manifest["agent_subfield"],
            "research_question": clean_manifest["research_question"],
            "synthetic_fixture": clean_manifest["synthetic_fixture"],
            "synthetic_notice": clean_manifest["synthetic_notice"],
        },
        "evaluation_configuration": {
            "random_seed": random_seed,
            "bootstrap_replicates": bootstrap_replicates,
            "confidence_level": confidence_level,
            "bootstrap_method": (
                "nonparametric percentile bootstrap" if bootstrap_replicates else None
            ),
            "sampling_unit_policy": (
                "Each metric declares its own observable sampling unit; units are not pooled."
            ),
        },
        "provenance": {
            "manifest_sha256": manifest.get("_source_sha256"),
            "system_source_sha256s": {
                item["system_id"]: item["provenance"]["imported_from_sha256"]
                for item in sorted(outputs, key=lambda row: row["system_id"])
            },
            "annotation_source_sha256s": sorted(
                item.get("_source_sha256")
                for item in annotation_batches
                if item.get("_source_sha256") is not None
            ),
        },
        "interpretation_boundaries": [
            "Automatic metrics describe observable records only.",
            (
                "Novelty, significance, and technical correctness come only from "
                "blinded expert annotations in primary assessment fields."
            ),
            "LLM judge annotations are auxiliary only and never enter primary conclusions.",
            (
                "Held-out mechanism rediscovery is an expert judgment and is reported "
                "separately from simple text similarity."
            ),
            "No aggregate score, ranking, champion, or automatic research verdict is produced.",
        ],
        "systems": systems,
    }


def _evaluate_system(
    manifest: Mapping[str, Any],
    output: Mapping[str, Any],
    batches: Sequence[Mapping[str, Any]],
    *,
    bootstrap_replicates: int,
    confidence_level: float,
    random_seed: int,
) -> dict[str, Any]:
    candidates = output["candidates"]
    strong_baselines = {
        item["baseline_id"] for item in manifest["known_strong_baselines"]
    }

    audited_candidates = [
        item for item in candidates if item["visible_prior_audit"]["performed"]
    ]
    collision_values = [
        bool(item["visible_prior_audit"]["collision_visible_paper_ids"])
        for item in audited_candidates
    ]
    audit_values = [item["visible_prior_audit"]["performed"] for item in candidates]
    structurally_eligible = [item for item in candidates if _has_complete_structure(item)]
    pair_values = [
        _structure_signature(left) == _structure_signature(right)
        for index, left in enumerate(structurally_eligible)
        for right in structurally_eligible[index + 1 :]
    ]
    descriptor_values = [
        sum(_is_complete_text(item["descriptors"][field]) for field in DESCRIPTOR_FIELDS)
        / len(DESCRIPTOR_FIELDS)
        for item in candidates
    ]
    changed_values = [
        sum(
            _is_complete_text(item["changed_computation"][field])
            for field in CHANGED_COMPUTATION_FIELDS
        )
        / len(CHANGED_COMPUTATION_FIELDS)
        for item in candidates
    ]
    falsifier_values = [
        all(_is_complete_text(item["falsifier"][field]) for field in FALSIFIER_FIELDS)
        for item in candidates
    ]
    killer_values = [
        all(_complete_field(item["killer_experiment"][field]) for field in KILLER_EXPERIMENT_FIELDS)
        for item in candidates
    ]
    implementation_values = [
        item["implementation"]["status"] == "implemented"
        and bool(item["implementation"]["artifact_sha256s"])
        for item in candidates
    ]
    killed = [item for item in candidates if item["outcome"]["status"] in {"early_killed", "late_killed"}]
    early_values = [item["outcome"]["decision_stage"] in EARLY_KILL_STAGES for item in killed]

    matched_evaluations: list[tuple[str, bool]] = []
    per_candidate_matched: dict[str, list[bool]] = {}
    for candidate in candidates:
        for evaluation in candidate["empirical_evaluations"]:
            if (
                evaluation["baseline_id"] in strong_baselines
                and evaluation["parity_status"] == "matched"
                and evaluation["survived"] is not None
            ):
                survived = bool(evaluation["survived"])
                matched_evaluations.append((candidate["candidate_id"], survived))
                per_candidate_matched.setdefault(candidate["candidate_id"], []).append(survived)
    surviving_candidate_ids = sorted(
        candidate_id
        for candidate_id, values in per_candidate_matched.items()
        if values and all(values)
    )

    expert_scores: dict[str, list[float]] = {
        "novelty": [],
        "significance": [],
        "technical_correctness": [],
    }
    rediscovery_values: list[bool] = []
    similarity_values: list[float] = []
    auxiliary_annotation_count = 0
    for batch in batches:
        unblind = {
            item["blinded_candidate_id"]: (item["system_id"], item["candidate_id"])
            for item in batch["unblinding_map"]
        }
        if batch["annotation_source"] == "llm_auxiliary":
            auxiliary_annotation_count += sum(
                1
                for item in batch["annotations"]
                if unblind[item["blinded_candidate_id"]][0] == output["system_id"]
            )
            continue
        for item in batch["annotations"]:
            if unblind[item["blinded_candidate_id"]][0] != output["system_id"]:
                continue
            for dimension in expert_scores:
                expert_scores[dimension].append(float(item[dimension]["value"]))
        for item in batch["heldout_mechanism_assessments"]:
            if unblind[item["blinded_candidate_id"]][0] != output["system_id"]:
                continue
            rediscovery_values.append(bool(item["mechanism_rediscovered"]))
            if item["simple_text_similarity"] is not None:
                similarity_values.append(float(item["simple_text_similarity"]))

    metric = lambda name, values, unit: _mean_metric(
        name,
        values,
        unit,
        bootstrap_replicates=bootstrap_replicates,
        confidence_level=confidence_level,
        random_seed=_derived_seed(random_seed, output["system_id"], name),
    )
    cost_per_survivor = {
        "surviving_hypothesis_count": len(surviving_candidate_ids),
        "surviving_hypothesis_ids": surviving_candidate_ids,
        "sampling_unit": "system_output",
        "values": {},
        "missing_cost": output["cost"] is None,
    }
    for field in COST_FIELDS:
        raw = None if output["cost"] is None else output["cost"][field]
        cost_per_survivor["values"][field] = (
            None
            if raw is None or not surviving_candidate_ids
            else raw / len(surviving_candidate_ids)
        )

    collision_metric = metric(
        "visible_prior_collision_rate", collision_values, "audited_candidate"
    )
    collision_metric.update(
        {
            "eligible_count": len(audited_candidates),
            "population_count": len(candidates),
            "eligibility_rule": "visible_prior_audit.performed == true",
        }
    )
    structure_duplicate_metric = metric(
        "structure_duplicate_rate",
        pair_values,
        "fully_described_candidate_pair",
    )
    structure_duplicate_metric.update(
        {
            "eligible_count": len(pair_values),
            "population_count": len(candidates) * (len(candidates) - 1) // 2,
            "eligibility_rule": (
                "both candidates have all seven structure descriptor fields observed"
            ),
        }
    )

    return {
        "system_id": output["system_id"],
        "system_type": output["system_type"],
        "system_configuration_sha256": output["configuration_sha256"],
        "random_seed": output["random_seed"],
        "candidate_payload_sha256": output["candidate_payload_sha256"],
        "candidate_count": len(candidates),
        "cost": output["cost"],
        "axes": {
            "exploration": {
                "visible_prior_collision_rate": collision_metric,
                "nearest_prior_audit_coverage": metric(
                    "nearest_prior_audit_coverage", audit_values, "candidate"
                ),
            },
            "diversity": {
                "structure_duplicate_rate": structure_duplicate_metric,
                "descriptor_coverage": metric(
                    "descriptor_coverage", descriptor_values, "candidate"
                ),
                "descriptor_distributions": _descriptor_distributions(candidates),
            },
            "falsifiability": {
                "changed_computation_completeness": metric(
                    "changed_computation_completeness", changed_values, "candidate"
                ),
                "falsifier_completeness": metric(
                    "falsifier_completeness", falsifier_values, "candidate"
                ),
                "killer_experiment_completeness": metric(
                    "killer_experiment_completeness", killer_values, "candidate"
                ),
            },
            "implementation": {
                "implementation_conversion_rate": metric(
                    "implementation_conversion_rate", implementation_values, "candidate"
                ),
                "early_kill_efficiency": metric(
                    "early_kill_efficiency", early_values, "killed_candidate"
                ),
                "definition": (
                    "A killed candidate is early only when its recorded decision stage is "
                    "proposal, prior_audit, or falsification_design."
                ),
            },
            "empirical_survival": {
                "under_matched_strong_baselines": metric(
                    "empirical_survival_under_matched_baselines",
                    [value for _, value in matched_evaluations],
                    "strong_matched_baseline_comparison",
                ),
                "matched_comparison_count": len(matched_evaluations),
                "cost_per_surviving_hypothesis": cost_per_survivor,
                "survivor_definition": (
                    "At least one matched comparison against a manifest-declared strong "
                    "baseline and survival in every such recorded comparison."
                ),
            },
        },
        "heldout_evaluation": {
            "mechanism_rediscovery": metric(
                "heldout_mechanism_rediscovery",
                rediscovery_values,
                "expert_annotated_candidate_heldout_pair",
            ),
            "simple_text_similarity": metric(
                "heldout_simple_text_similarity",
                similarity_values,
                "annotated_candidate_heldout_pair",
            ),
            "separation_note": (
                "Mechanism rediscovery is a blinded expert label; simple text similarity "
                "is reported separately and never defines rediscovery."
            ),
        },
        "expert_blind_assessment": {
            "primary_source": "blinded_expert_only",
            "novelty": metric(
                "expert_novelty", expert_scores["novelty"], "blinded_expert_annotation"
            ),
            "significance": metric(
                "expert_significance",
                expert_scores["significance"],
                "blinded_expert_annotation",
            ),
            "technical_correctness": metric(
                "expert_technical_correctness",
                expert_scores["technical_correctness"],
                "blinded_expert_annotation",
            ),
            "llm_judge_auxiliary_annotation_count": auxiliary_annotation_count,
            "llm_judge_policy": "auxiliary_only; excluded from primary conclusions",
        },
    }


def _mean_metric(
    name: str,
    values: Sequence[bool | float],
    sampling_unit: str,
    *,
    bootstrap_replicates: int,
    confidence_level: float,
    random_seed: int,
) -> dict[str, Any]:
    numeric = [float(value) for value in values]
    result: dict[str, Any] = {
        "metric": name,
        "numerator": sum(numeric) if numeric else 0,
        "denominator": len(numeric),
        "value": sum(numeric) / len(numeric) if numeric else None,
        "sampling_unit": sampling_unit,
        "confidence_interval": None,
    }
    if bootstrap_replicates and numeric:
        rng = random.Random(random_seed)
        samples = []
        for _ in range(bootstrap_replicates):
            draw = [numeric[rng.randrange(len(numeric))] for _ in numeric]
            samples.append(sum(draw) / len(draw))
        samples.sort()
        alpha = (1.0 - confidence_level) / 2.0
        result["confidence_interval"] = {
            "method": "nonparametric percentile bootstrap",
            "confidence_level": confidence_level,
            "replicates": bootstrap_replicates,
            "sampling_unit": sampling_unit,
            "lower": _percentile(samples, alpha),
            "upper": _percentile(samples, 1.0 - alpha),
        }
    return result


def _percentile(sorted_values: Sequence[float], probability: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = probability * (len(sorted_values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return sorted_values[lower] * (1.0 - fraction) + sorted_values[upper] * fraction


def _validate_candidate(
    value: object, label: str, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    required = {
        "candidate_id",
        "title",
        "problem",
        "mechanism_claim",
        "descriptors",
        "changed_computation",
        "falsifier",
        "killer_experiment",
        "visible_prior_audit",
        "implementation",
        "outcome",
        "empirical_evaluations",
    }
    item = _mapping(value, label)
    _exact_fields(item, required, label)
    _identifier(item["candidate_id"], f"{label}.candidate_id")
    for name in ("title", "problem", "mechanism_claim"):
        if not isinstance(item[name], str):
            raise ValueError(f"{label}.{name} must be text")
    descriptors = _mapping(item["descriptors"], f"{label}.descriptors")
    _exact_fields(descriptors, set(DESCRIPTOR_FIELDS), f"{label}.descriptors")
    changed = _mapping(item["changed_computation"], f"{label}.changed_computation")
    _exact_fields(changed, set(CHANGED_COMPUTATION_FIELDS), f"{label}.changed_computation")
    for name, field_value in (*descriptors.items(), *changed.items()):
        if not isinstance(field_value, str):
            raise ValueError(f"{label}.{name} must be text")
    falsifier = _mapping(item["falsifier"], f"{label}.falsifier")
    _exact_fields(falsifier, set(FALSIFIER_FIELDS), f"{label}.falsifier")
    for name in FALSIFIER_FIELDS:
        if not isinstance(falsifier[name], str):
            raise ValueError(f"{label}.falsifier.{name} must be text")
    killer = _mapping(item["killer_experiment"], f"{label}.killer_experiment")
    _exact_fields(killer, set(KILLER_EXPERIMENT_FIELDS), f"{label}.killer_experiment")
    for name in KILLER_EXPERIMENT_FIELDS[:-1]:
        if not isinstance(killer[name], str):
            raise ValueError(f"{label}.killer_experiment.{name} must be text")
    _text_list(killer["baseline_ids"], f"{label}.killer_experiment.baseline_ids")

    prior = _mapping(item["visible_prior_audit"], f"{label}.visible_prior_audit")
    _exact_fields(
        prior,
        {"performed", "audited_visible_paper_ids", "collision_visible_paper_ids"},
        f"{label}.visible_prior_audit",
    )
    if type(prior["performed"]) is not bool:
        raise ValueError(f"{label}.visible_prior_audit.performed must be boolean")
    audited = _unique_identifiers(
        prior["audited_visible_paper_ids"], f"{label}.audited_visible_paper_ids"
    )
    collisions = _unique_identifiers(
        prior["collision_visible_paper_ids"], f"{label}.collision_visible_paper_ids"
    )
    visible, _ = derive_visible_paper_ids(manifest)
    if set(audited) - set(visible) or set(collisions) - set(visible):
        raise ValueError(f"{label} prior audit references a non-visible paper")
    if set(collisions) - set(audited):
        raise ValueError(f"{label} collision papers must be included in audited papers")
    if not prior["performed"] and (audited or collisions):
        raise ValueError(f"{label} unperformed prior audit cannot contain paper IDs")

    implementation = _mapping(item["implementation"], f"{label}.implementation")
    _exact_fields(
        implementation, {"status", "artifact_sha256s"}, f"{label}.implementation"
    )
    if implementation["status"] not in IMPLEMENTATION_STATUSES:
        raise ValueError(f"{label} has invalid implementation status")
    hashes = _text_list(
        implementation["artifact_sha256s"], f"{label}.implementation.artifact_sha256s"
    )
    for digest in hashes:
        _sha256_value(digest, "implementation artifact hash")
    if implementation["status"] == "implemented" and not hashes:
        raise ValueError(f"{label} implemented candidate requires an artifact hash")

    outcome = _mapping(item["outcome"], f"{label}.outcome")
    _exact_fields(outcome, {"status", "decision_stage", "decision_reason"}, f"{label}.outcome")
    if outcome["status"] not in OUTCOME_STATUSES:
        raise ValueError(f"{label} has invalid outcome status")
    stage = outcome["decision_stage"]
    if stage not in EARLY_KILL_STAGES | LATE_KILL_STAGES | {"none"}:
        raise ValueError(f"{label} has invalid decision_stage")
    if not isinstance(outcome["decision_reason"], str):
        raise ValueError(f"{label}.decision_reason must be text")
    if outcome["status"] == "early_killed" and stage not in EARLY_KILL_STAGES:
        raise ValueError(f"{label} early_killed outcome has a late decision stage")
    if outcome["status"] == "late_killed" and stage not in LATE_KILL_STAGES:
        raise ValueError(f"{label} late_killed outcome has an early decision stage")

    evaluations = _list(item["empirical_evaluations"], f"{label}.empirical_evaluations")
    comparison_ids: list[str] = []
    for index, raw in enumerate(evaluations):
        evaluation = _mapping(raw, f"{label}.empirical_evaluations[{index}]")
        _exact_fields(
            evaluation,
            {
                "comparison_id",
                "baseline_id",
                "parity_status",
                "survived",
                "decision_rule",
                "metric_name",
                "sampling_unit",
            },
            "empirical evaluation",
        )
        comparison_ids.append(_identifier(evaluation["comparison_id"], "comparison_id"))
        _identifier(evaluation["baseline_id"], "baseline_id")
        if evaluation["parity_status"] not in PARITY_STATUSES:
            raise ValueError("invalid empirical parity_status")
        if evaluation["survived"] is not None and type(evaluation["survived"]) is not bool:
            raise ValueError("empirical survived must be boolean or null")
        for name in ("decision_rule", "metric_name", "sampling_unit"):
            if not isinstance(evaluation[name], str):
                raise ValueError(f"empirical {name} must be text")
    _require_unique(comparison_ids, f"{label} comparison IDs")
    return dict(item)


def _paper_timeline(value: object) -> list[dict[str, Any]]:
    items = _list(value, "paper_timeline")
    result: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw in enumerate(items):
        item = _mapping(raw, f"paper_timeline[{index}]")
        _exact_fields(
            item,
            {"paper_id", "publication_date", "publication_year"},
            "paper timeline entry",
        )
        paper_id = _identifier(item["paper_id"], "paper_id")
        ids.append(paper_id)
        date = item["publication_date"]
        year = item["publication_year"]
        if date is not None:
            _date_value(date, "publication_date")
        if year is not None:
            _year_value(year, "publication_year")
        if date is None and year is None:
            raise ValueError("paper timeline entry requires a date or year")
        if date is not None and year is not None and int(date[:4]) != year:
            raise ValueError("publication_date and publication_year disagree")
        result.append(dict(item))
    _require_unique(ids, "paper timeline IDs")
    return result


def _validate_temporal_membership(
    cutoff: object,
    visible_ids: Sequence[str],
    heldout_ids: Sequence[str],
    timeline: Sequence[Mapping[str, Any]],
) -> None:
    if cutoff is None:
        return
    by_id = {item["paper_id"]: item for item in timeline}
    precision = cutoff["precision"]
    cutoff_year = int(str(cutoff["value"])[:4])
    cutoff_day = str(cutoff["value"]) if precision == "day" else None
    for paper_id in visible_ids:
        item = by_id[paper_id]
        date = item["publication_date"]
        year = int(date[:4]) if date else item["publication_year"]
        if date is not None and cutoff_day is not None and date > cutoff_day:
            raise ValueError(f"visible paper is after exact cutoff: {paper_id}")
        if year is not None and year > cutoff_year:
            raise ValueError(f"visible paper is after cutoff year: {paper_id}")
    for paper_id in heldout_ids:
        item = by_id[paper_id]
        date = item["publication_date"]
        year = int(date[:4]) if date else item["publication_year"]
        if date is not None and cutoff_day is not None and date <= cutoff_day:
            raise ValueError(f"held-out paper is not after exact cutoff: {paper_id}")
        if year is not None and year < cutoff_year:
            raise ValueError(f"held-out paper predates cutoff year: {paper_id}")


def _resource_budget(value: object) -> None:
    mapping = _mapping(value, "resource_budget")
    _exact_fields(mapping, set(COST_FIELDS), "resource_budget")
    for name, item in mapping.items():
        if item is not None:
            _nonnegative_number(item, f"resource_budget.{name}")


def _cost(value: object) -> None:
    mapping = _mapping(value, "cost")
    _exact_fields(mapping, set(COST_FIELDS), "cost")
    for name, item in mapping.items():
        if item is not None:
            _nonnegative_number(item, f"cost.{name}")


def _score(value: object, label: str) -> None:
    mapping = _mapping(value, label)
    _exact_fields(mapping, {"value", "confidence", "rationale"}, label)
    if type(mapping["value"]) is not int or not 1 <= mapping["value"] <= 5:
        raise ValueError(f"{label}.value must be an integer from 1 to 5")
    _bounded_number(mapping["confidence"], f"{label}.confidence", 0.0, 1.0)
    _required_text(mapping["rationale"], f"{label}.rationale")


def _descriptor_distributions(candidates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field in DESCRIPTOR_FIELDS:
        counts: dict[str, int] = {}
        for candidate in candidates:
            value = candidate["descriptors"][field].strip() or "(missing)"
            counts[value] = counts.get(value, 0) + 1
        result[field] = dict(sorted(counts.items()))
    return result


def _structure_signature(candidate: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(candidate["descriptors"][field].strip() for field in DESCRIPTOR_FIELDS)


def _has_complete_structure(candidate: Mapping[str, Any]) -> bool:
    return all(
        _is_complete_text(candidate["descriptors"][field])
        for field in DESCRIPTOR_FIELDS
    )


def _assert_no_heldout_leak(value: object, heldout_ids: Iterable[str], label: str) -> None:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    leaked = sorted(paper_id for paper_id in heldout_ids if paper_id in serialized)
    if leaked:
        raise ValueError(f"held-out paper ID leaked into {label}: {leaked}")


def _derived_seed(seed: int, system_id: str, metric: str) -> int:
    digest = hashlib.sha256(f"{seed}\0{system_id}\0{metric}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def _without_internal_fields(value: Mapping[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if not key.startswith("_")}


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return dict(value)


def _list(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def _exact_fields(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{label} fields mismatch; missing={sorted(expected-actual)}, extra={sorted(actual-expected)}"
        )


def _schema_one(value: Mapping[str, Any], label: str) -> None:
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError(f"{label} schema_version must be integer 1")


def _identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise ValueError(f"invalid {label}: {value!r}")
    return value


def _required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty text")
    return value


def _text_list(value: object, label: str) -> list[str]:
    items = _list(value, label)
    if any(not isinstance(item, str) for item in items):
        raise ValueError(f"{label} must contain only text")
    return items


def _unique_identifiers(value: object, label: str) -> list[str]:
    items = [_identifier(item, label) for item in _list(value, label)]
    _require_unique(items, label)
    return items


def _require_unique(values: Sequence[str], label: str) -> None:
    if len(set(values)) != len(values):
        raise ValueError(f"{label} must be unique")


def _sha256_value(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase SHA-256")
    return value


def _year_value(value: object, label: str) -> int:
    if type(value) is not int or not 1000 <= value <= 9999:
        raise ValueError(f"{label} must be a four-digit integer year")
    return value


def _date_value(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be YYYY-MM-DD")
    match = _DATE.fullmatch(value)
    if match is None:
        raise ValueError(f"{label} must be YYYY-MM-DD")
    year, month, day = map(int, match.groups())
    try:
        __import__("datetime").date(year, month, day)
    except ValueError as error:
        raise ValueError(f"{label} is not a valid date") from error
    return value


def _nonnegative_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a non-negative finite number")
    numeric = float(value)
    if not math.isfinite(numeric) or numeric < 0:
        raise ValueError(f"{label} must be a non-negative finite number")
    return numeric


def _bounded_number(
    value: object,
    label: str,
    lower: float,
    upper: float,
    *,
    strict: bool = False,
) -> float:
    numeric = _nonnegative_number(value, label)
    valid = lower < numeric < upper if strict else lower <= numeric <= upper
    if not valid:
        bracket = "strictly between" if strict else "between"
        raise ValueError(f"{label} must be {bracket} {lower} and {upper}")
    return numeric


def _is_complete_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _complete_field(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    return value is not None
