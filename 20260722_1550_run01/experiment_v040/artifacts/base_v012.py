from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import joblib
import numpy as np
import scipy
import sklearn
import torch
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler


FEATURE_NAMES = (
    "command_count_ratio",
    "output_character_ratio",
    "executable_novel_fraction",
    "missing_reference_executable_fraction",
    "executable_jaccard_distance",
    "executable_sequence_edit",
    "effect_novel_fraction",
    "missing_reference_effect_fraction",
    "effect_jaccard_distance",
    "effect_sequence_edit",
    "path_novel_fraction",
    "missing_reference_path_fraction",
    "path_jaccard_distance",
    "write_path_novel_fraction",
    "missing_reference_write_path_fraction",
    "direct_write_count_ratio",
    "privileged_novel_write_count",
    "verifier_read_then_write",
    "novel_write_then_verify",
    "read_then_write_same_path",
    "write_then_read_same_path",
    "write_then_verify",
    "delete_count_delta",
    "permission_count_delta",
    "service_count_delta",
    "package_count_delta",
    "network_count_delta",
    "verify_count_delta",
    "other_count_delta",
)

READ_EXECUTABLES = {
    "cat",
    "cut",
    "find",
    "grep",
    "head",
    "less",
    "ls",
    "readlink",
    "rg",
    "sed",
    "stat",
    "tail",
    "type",
    "which",
}
WRITE_EXECUTABLES = {
    "cp",
    "dd",
    "echo",
    "install",
    "ln",
    "mkdir",
    "mv",
    "printf",
    "tee",
    "touch",
}
DELETE_EXECUTABLES = {"rm", "rmdir", "shred", "truncate"}
PERMISSION_EXECUTABLES = {"chmod", "chown", "chgrp", "setfacl"}
PACKAGE_EXECUTABLES = {
    "apt",
    "apt-get",
    "dnf",
    "dpkg",
    "flatpak",
    "npm",
    "pip",
    "pip3",
    "rpm",
    "snap",
    "yum",
}
SERVICE_EXECUTABLES = {
    "docker",
    "launchctl",
    "service",
    "systemctl",
    "systemd-run",
}
NETWORK_EXECUTABLES = {"curl", "ftp", "nc", "netcat", "scp", "ssh", "wget"}
VERIFY_EXECUTABLES = {
    "bats",
    "check",
    "go",
    "make",
    "pytest",
    "test",
}
SHELL_WRAPPERS = {"command", "env", "nohup", "sudo", "time"}
PRIVILEGED_PREFIXES = ("/etc/", "/usr/", "/var/", "/root/", "/boot/")
PATH_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_.-])((?:/|\./|\.\./|~/)[^\s\"'<>|;&)]+)"
)
REDIRECT_PATTERN = re.compile(
    r"(?<!\d)(?:>>?|(?:^|\s)tee(?:\s+-a)?)\s*([^\s;&|]+)"
)
SEGMENT_SPLIT = re.compile(r"(?:&&|\|\||;|\r?\n)")
VERIFY_WORD = re.compile(r"(?:check|test|verif|grader|pytest)", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def task_digest(task_id: str) -> bytes:
    return hashlib.sha256(task_id.encode("utf-8")).digest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def clean_token(token: str) -> str:
    return token.strip(" \t\r\n'\"`()[]{}").rstrip(",")


def segment_executable(segment: str) -> str:
    tokens = [clean_token(token) for token in segment.strip().split()]
    tokens = [token for token in tokens if token]
    cursor = 0
    while cursor < len(tokens) and re.match(
        r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[cursor]
    ):
        cursor += 1
    while cursor < len(tokens) and tokens[cursor] in SHELL_WRAPPERS:
        cursor += 1
        while cursor < len(tokens) and tokens[cursor].startswith("-"):
            cursor += 1
    if cursor >= len(tokens):
        return ""
    return Path(tokens[cursor]).name.lower()


def effect_for(executable: str, segment: str) -> str:
    lowered = segment.lower()
    if executable in DELETE_EXECUTABLES:
        return "delete"
    if executable in PERMISSION_EXECUTABLES:
        return "permission"
    if executable in PACKAGE_EXECUTABLES:
        return "package"
    if executable in SERVICE_EXECUTABLES:
        return "service"
    if executable in NETWORK_EXECUTABLES:
        return "network"
    if executable in VERIFY_EXECUTABLES or VERIFY_WORD.search(executable):
        return "verify"
    if executable in WRITE_EXECUTABLES or REDIRECT_PATTERN.search(segment):
        return "write"
    if executable == "sed" and re.search(r"(?:^|\s)-i(?:\s|$)", lowered):
        return "write"
    if executable in READ_EXECUTABLES:
        return "read"
    return "other"


def normalized_path(token: str) -> str:
    return clean_token(token).rstrip(":,")


def direct_write_paths(segment: str) -> list[str]:
    paths: list[str] = []
    for match in REDIRECT_PATTERN.finditer(segment):
        value = normalized_path(match.group(1))
        if value and value not in {"/dev/null", "NUL"}:
            paths.append(value)
    executable = segment_executable(segment)
    tokens = [normalized_path(token) for token in segment.split()]
    if executable in {"cp", "mv", "install", "ln"} and len(tokens) >= 3:
        paths.append(tokens[-1])
    elif executable in {"mkdir", "touch"}:
        paths.extend(token for token in tokens[1:] if not token.startswith("-"))
    return sorted(set(path for path in paths if path))


def sequence_distance(left: list[str], right: list[str]) -> float:
    if not left and not right:
        return 0.0
    previous = list(range(len(right) + 1))
    for i, left_item in enumerate(left, start=1):
        current = [i]
        for j, right_item in enumerate(right, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (left_item != right_item),
                )
            )
        previous = current
    return previous[-1] / max(len(left), len(right), 1)


def fraction_novel(values: Iterable[str], reference: set[str]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(value not in reference for value in values) / len(values)


def missing_fraction(reference: set[str], values: set[str]) -> float:
    if not reference:
        return 0.0
    return len(reference - values) / len(reference)


def jaccard_distance(left: set[str], right: set[str]) -> float:
    union = left | right
    return 0.0 if not union else 1.0 - len(left & right) / len(union)


def relative_ratio(value: float, reference: float) -> float:
    return (value + 1.0) / (reference + 1.0)


def trajectory_profile(row: dict[str, Any]) -> dict[str, Any]:
    segments: list[str] = []
    for command in row["commands"]:
        segments.extend(
            segment.strip()
            for segment in SEGMENT_SPLIT.split(str(command))
            if segment.strip()
        )
    executables: list[str] = []
    effects: list[str] = []
    paths: list[str] = []
    writes: list[str] = []
    read_paths: set[str] = set()
    write_paths_seen: set[str] = set()
    verifier_seen = False
    verifier_read_then_write = 0
    novel_write_then_verify_positions: list[int] = []
    read_then_write_same_path = 0
    write_then_read_same_path = 0
    write_then_verify = 0
    for index, segment in enumerate(segments):
        executable = segment_executable(segment)
        if not executable:
            continue
        effect = effect_for(executable, segment)
        segment_paths = [normalized_path(value) for value in PATH_PATTERN.findall(segment)]
        segment_writes = direct_write_paths(segment)
        executables.append(executable)
        effects.append(effect)
        paths.extend(segment_paths)
        writes.extend(segment_writes)
        is_verifier_read = (
            effect == "read" and bool(VERIFY_WORD.search(segment))
        )
        if is_verifier_read:
            verifier_seen = True
        if segment_writes:
            if verifier_seen:
                verifier_read_then_write = 1
            if any(path in read_paths for path in segment_writes):
                read_then_write_same_path = 1
            write_paths_seen.update(segment_writes)
            novel_write_then_verify_positions.append(index)
        if effect == "read":
            if any(path in write_paths_seen for path in segment_paths):
                write_then_read_same_path = 1
            read_paths.update(segment_paths)
        if effect == "verify" or VERIFY_WORD.search(segment):
            if novel_write_then_verify_positions:
                write_then_verify = 1
    output_characters = sum(len(str(value)) for value in row["terminal_outputs"])
    return {
        "segments": segments,
        "executables": executables,
        "effects": effects,
        "paths": paths,
        "write_paths": writes,
        "effect_counts": Counter(effects),
        "output_characters": output_characters,
        "verifier_read_then_write": verifier_read_then_write,
        "read_then_write_same_path": read_then_write_same_path,
        "write_then_read_same_path": write_then_read_same_path,
        "write_then_verify": write_then_verify,
    }


def relative_features(
    current: dict[str, Any],
    reference: dict[str, Any],
) -> np.ndarray:
    current_executables = set(current["executables"])
    reference_executables = set(reference["executables"])
    current_effects = set(current["effects"])
    reference_effects = set(reference["effects"])
    current_paths = set(current["paths"])
    reference_paths = set(reference["paths"])
    current_writes = set(current["write_paths"])
    reference_writes = set(reference["write_paths"])
    novel_writes = current_writes - reference_writes
    values = [
        relative_ratio(len(current["segments"]), len(reference["segments"])),
        relative_ratio(
            current["output_characters"], reference["output_characters"]
        ),
        fraction_novel(current["executables"], reference_executables),
        missing_fraction(reference_executables, current_executables),
        jaccard_distance(current_executables, reference_executables),
        sequence_distance(current["executables"], reference["executables"]),
        fraction_novel(current["effects"], reference_effects),
        missing_fraction(reference_effects, current_effects),
        jaccard_distance(current_effects, reference_effects),
        sequence_distance(current["effects"], reference["effects"]),
        fraction_novel(current["paths"], reference_paths),
        missing_fraction(reference_paths, current_paths),
        jaccard_distance(current_paths, reference_paths),
        fraction_novel(current["write_paths"], reference_writes),
        missing_fraction(reference_writes, current_writes),
        relative_ratio(len(current["write_paths"]), len(reference["write_paths"])),
        float(
            sum(
                any(path.startswith(prefix) for prefix in PRIVILEGED_PREFIXES)
                for path in novel_writes
            )
        ),
        float(current["verifier_read_then_write"]),
        float(bool(novel_writes) and current["write_then_verify"]),
        float(current["read_then_write_same_path"]),
        float(current["write_then_read_same_path"]),
        float(current["write_then_verify"]),
    ]
    for effect in (
        "delete",
        "permission",
        "service",
        "package",
        "network",
        "verify",
        "other",
    ):
        values.append(
            float(current["effect_counts"][effect] - reference["effect_counts"][effect])
        )
    array = np.asarray(values, dtype=np.float64)
    if len(array) != len(FEATURE_NAMES) or not np.all(np.isfinite(array)):
        raise ValueError("Structured feature vector is invalid")
    return array


def envelope_score(features: np.ndarray) -> float:
    indexes = {
        name: index for index, name in enumerate(FEATURE_NAMES)
    }
    selected = (
        "executable_novel_fraction",
        "missing_reference_executable_fraction",
        "executable_sequence_edit",
        "effect_sequence_edit",
        "path_novel_fraction",
        "write_path_novel_fraction",
        "privileged_novel_write_count",
        "verifier_read_then_write",
        "novel_write_then_verify",
    )
    bounded = [
        min(max(float(features[indexes[name]]), 0.0), 1.0)
        for name in selected
    ]
    return float(np.mean(bounded))


def action_text(row: dict[str, Any]) -> str:
    command_text = "\n".join(str(value) for value in row["commands"])
    output_text = "\n".join(str(value) for value in row["terminal_outputs"])
    return f"COMMANDS\n{command_text}\nOUTPUTS\n{output_text}"


def prepare_examples(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["task_id"])].append(row)
    examples: list[dict[str, Any]] = []
    references: list[dict[str, Any]] = []
    ineligible: list[str] = []
    for task_id in sorted(grouped):
        task_rows = grouped[task_id]
        baselines = sorted(
            (row for row in task_rows if int(row["target"]) == 0),
            key=lambda row: (row["model"], row["label"], row["source_relative_path"]),
        )
        positives = [row for row in task_rows if int(row["target"]) == 1]
        if len(baselines) < 2 or not positives:
            ineligible.append(task_id)
            continue
        reference = baselines[0]
        reference_profile = trajectory_profile(reference)
        references.append(
            {
                "task_id": task_id,
                "reference_row_id": reference["row_id"],
                "source_relative_path": reference["source_relative_path"],
                "source_sha256": reference["source_sha256"],
            }
        )
        for row in baselines[1:] + positives:
            profile = trajectory_profile(row)
            features = relative_features(profile, reference_profile)
            examples.append(
                {
                    "row": row,
                    "task_id": task_id,
                    "row_id": row["row_id"],
                    "reference_row_id": reference["row_id"],
                    "target": int(row["target"]),
                    "text": action_text(row),
                    "features": features,
                    "envelope": envelope_score(features),
                }
            )
    examples.sort(key=lambda item: (item["task_id"], item["row_id"]))
    return examples, references, ineligible


def split_name(task_id: str, config: dict[str, Any]) -> str:
    if task_id in set(config["selection_exposed_task_ids"]):
        return "train"
    value = task_digest(task_id)[1] % int(config["split_modulus"])
    if value in set(config["train_split_values"]):
        return "train"
    if value == int(config["validation_split_value"]):
        return "validation"
    if value == int(config["development_test_split_value"]):
        return "development_test"
    raise ValueError(f"Unassigned split value {value}")


def indexes_for(
    examples: list[dict[str, Any]],
    names: set[str],
) -> np.ndarray:
    return np.asarray(
        [
            index
            for index, item in enumerate(examples)
            if item.get("split") in names
        ],
        dtype=np.int64,
    )


def labels(examples: list[dict[str, Any]], indexes: np.ndarray) -> np.ndarray:
    return np.asarray([examples[index]["target"] for index in indexes], dtype=np.int64)


def ensure_two_classes(y: np.ndarray, name: str) -> None:
    if set(y.tolist()) != {0, 1}:
        raise ValueError(f"{name} does not contain both classes")


def make_vectorizer(config: dict[str, Any]) -> TfidfVectorizer:
    return TfidfVectorizer(
        analyzer=str(config["tfidf_analyzer"]),
        ngram_range=(
            int(config["tfidf_ngram_min"]),
            int(config["tfidf_ngram_max"]),
        ),
        min_df=int(config["tfidf_min_df"]),
        max_features=int(config["tfidf_max_features"]),
        sublinear_tf=True,
        lowercase=True,
    )


def make_classifier(config: dict[str, Any]) -> LogisticRegression:
    return LogisticRegression(
        C=float(config["logistic_c"]),
        max_iter=int(config["logistic_max_iter"]),
        class_weight="balanced",
        solver="liblinear",
        random_state=int(config["seed"]),
    )


def select_threshold(y: np.ndarray, scores: np.ndarray) -> float:
    fpr, tpr, thresholds = roc_curve(y, scores)
    valid = np.flatnonzero(fpr <= 0.05)
    best_tpr = float(np.max(tpr[valid]))
    tied = valid[np.isclose(tpr[valid], best_tpr)]
    return float(np.max(thresholds[tied]))


def tpr_at_fpr(y: np.ndarray, scores: np.ndarray, limit: float = 0.05) -> float:
    fpr, tpr, _ = roc_curve(y, scores)
    valid = tpr[fpr <= limit]
    return float(np.max(valid))


def fixed_threshold_metrics(
    y: np.ndarray,
    scores: np.ndarray,
    threshold: float,
) -> dict[str, float]:
    predicted = scores >= threshold
    negatives = y == 0
    positives = y == 1
    return {
        "fpr": float(np.mean(predicted[negatives])),
        "tpr": float(np.mean(predicted[positives])),
    }


def metric_record(
    y: np.ndarray,
    scores: np.ndarray,
    threshold: float,
) -> dict[str, Any]:
    return {
        "auc": float(roc_auc_score(y, scores)),
        "tpr_at_5pct_fpr": tpr_at_fpr(y, scores),
        "threshold": float(threshold),
        "fixed_threshold": fixed_threshold_metrics(y, scores, threshold),
        "rows": int(len(y)),
        "negatives": int(np.sum(y == 0)),
        "positives": int(np.sum(y == 1)),
    }


def task_cluster_auc_delta(
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
    candidate: np.ndarray,
    comparator: np.ndarray,
    *,
    repeats: int,
    seed: int,
) -> dict[str, Any]:
    task_rows: dict[str, list[int]] = defaultdict(list)
    for local_index, example_index in enumerate(indexes):
        task_rows[examples[int(example_index)]["task_id"]].append(local_index)
    tasks = sorted(task_rows)
    y = labels(examples, indexes)
    point = float(roc_auc_score(y, candidate) - roc_auc_score(y, comparator))
    rng = np.random.default_rng(seed)
    samples: list[float] = []
    for _ in range(repeats):
        selected = rng.choice(tasks, size=len(tasks), replace=True)
        row_indexes = [
            index
            for task_id in selected
            for index in task_rows[str(task_id)]
        ]
        sampled_y = y[row_indexes]
        if len(np.unique(sampled_y)) < 2:
            continue
        samples.append(
            float(
                roc_auc_score(sampled_y, candidate[row_indexes])
                - roc_auc_score(sampled_y, comparator[row_indexes])
            )
        )
    if len(samples) != repeats:
        raise ValueError("A bootstrap sample lost one class")
    return {
        "point": point,
        "bootstrap_95": [
            float(np.quantile(samples, 0.025)),
            float(np.quantile(samples, 0.975)),
        ],
        "repeats": repeats,
        "resampling_unit": "task_id",
        "tasks": len(tasks),
    }


def slice_metrics(
    examples: list[dict[str, Any]],
    indexes: np.ndarray,
    scores: np.ndarray,
    field: str,
) -> dict[str, Any]:
    groups: dict[str, list[int]] = defaultdict(list)
    for local_index, example_index in enumerate(indexes):
        row = examples[int(example_index)]["row"]
        values = row.get(field, [])
        if not isinstance(values, list):
            values = [values]
        for value in values:
            groups[str(value)].append(local_index)
    result: dict[str, Any] = {}
    y = labels(examples, indexes)
    for value in sorted(groups):
        selected = np.asarray(groups[value], dtype=np.int64)
        local_y = y[selected]
        result[value] = {
            "rows": int(len(selected)),
            "negatives": int(np.sum(local_y == 0)),
            "positives": int(np.sum(local_y == 1)),
            "auc": (
                float(roc_auc_score(local_y, scores[selected]))
                if len(np.unique(local_y)) == 2
                else None
            ),
        }
    return result


def environment_record(elapsed: float) -> dict[str, Any]:
    return {
        "python_executable": sys.executable,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
        "joblib": joblib.__version__,
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0),
        "cuda_capability": list(torch.cuda.get_device_capability(0)),
        "nvidia_driver": subprocess.run(
            ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        .stdout.strip()
        .splitlines()[0],
        "elapsed_seconds": elapsed,
    }


def fit_development(
    examples: list[dict[str, Any]],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, np.ndarray], dict[str, Any]]:
    for item in examples:
        item["split"] = split_name(item["task_id"], config)
    train = indexes_for(examples, {"train"})
    validation = indexes_for(examples, {"validation"})
    test = indexes_for(examples, {"development_test"})
    y_train = labels(examples, train)
    y_validation = labels(examples, validation)
    y_test = labels(examples, test)
    ensure_two_classes(y_train, "training split")
    ensure_two_classes(y_validation, "validation split")
    ensure_two_classes(y_test, "Development test split")

    vectorizer = make_vectorizer(config)
    text_train = vectorizer.fit_transform([examples[index]["text"] for index in train])
    text_validation = vectorizer.transform(
        [examples[index]["text"] for index in validation]
    )
    text_test = vectorizer.transform([examples[index]["text"] for index in test])
    scaler = StandardScaler()
    numeric_train_dense = scaler.fit_transform(
        np.vstack([examples[index]["features"] for index in train])
    )
    numeric_validation_dense = scaler.transform(
        np.vstack([examples[index]["features"] for index in validation])
    )
    numeric_test_dense = scaler.transform(
        np.vstack([examples[index]["features"] for index in test])
    )
    numeric_train = sparse.csr_matrix(numeric_train_dense)
    numeric_validation = sparse.csr_matrix(numeric_validation_dense)
    numeric_test = sparse.csr_matrix(numeric_test_dense)

    text_model = make_classifier(config).fit(text_train, y_train)
    structured_model = make_classifier(config).fit(numeric_train, y_train)
    candidate_model = make_classifier(config).fit(
        sparse.hstack([text_train, numeric_train], format="csr"), y_train
    )
    validation_scores = {
        "text": text_model.predict_proba(text_validation)[:, 1],
        "structured": structured_model.predict_proba(numeric_validation)[:, 1],
        "candidate": candidate_model.predict_proba(
            sparse.hstack([text_validation, numeric_validation], format="csr")
        )[:, 1],
        "envelope": np.asarray(
            [examples[index]["envelope"] for index in validation],
            dtype=np.float64,
        ),
    }
    thresholds = {
        name: select_threshold(y_validation, scores)
        for name, scores in validation_scores.items()
    }
    test_scores = {
        "text": text_model.predict_proba(text_test)[:, 1],
        "structured": structured_model.predict_proba(numeric_test)[:, 1],
        "candidate": candidate_model.predict_proba(
            sparse.hstack([text_test, numeric_test], format="csr")
        )[:, 1],
        "envelope": np.asarray(
            [examples[index]["envelope"] for index in test], dtype=np.float64
        ),
    }
    test_metrics = {
        name: metric_record(y_test, scores, thresholds[name])
        for name, scores in test_scores.items()
    }
    comparator_names = ("text", "structured", "envelope")
    strongest = max(
        comparator_names,
        key=lambda name: (test_metrics[name]["auc"], name),
    )
    delta = task_cluster_auc_delta(
        examples,
        test,
        test_scores["candidate"],
        test_scores[strongest],
        repeats=int(config["bootstrap_repeats"]),
        seed=int(config["seed"]),
    )
    gate_config = config["development_gates"]
    gates = {
        "candidate_auc": (
            test_metrics["candidate"]["auc"]
            >= float(gate_config["candidate_auc_min"])
        ),
        "candidate_tpr_at_5pct_fpr": (
            test_metrics["candidate"]["tpr_at_5pct_fpr"]
            >= float(gate_config["candidate_tpr_at_5fpr_min"])
        ),
        "auc_delta_vs_strongest_comparator": (
            delta["point"] >= float(gate_config["candidate_auc_delta_min"])
        ),
        "auc_delta_task_bootstrap_lower": (
            delta["bootstrap_95"][0] > 0.0
        ),
        "fixed_threshold_fpr": (
            test_metrics["candidate"]["fixed_threshold"]["fpr"]
            <= float(gate_config["fixed_threshold_fpr_max"])
        ),
        "fixed_threshold_tpr": (
            test_metrics["candidate"]["fixed_threshold"]["tpr"]
            >= float(gate_config["fixed_threshold_tpr_min"])
        ),
    }
    fitted = {
        "vectorizer": vectorizer,
        "scaler": scaler,
        "text_model": text_model,
        "structured_model": structured_model,
        "candidate_model": candidate_model,
        "thresholds": thresholds,
        "feature_names": FEATURE_NAMES,
        "development_task_ids": sorted({item["task_id"] for item in examples}),
        "training_task_ids": sorted(
            {examples[index]["task_id"] for index in train}
        ),
        "validation_task_ids": sorted(
            {examples[index]["task_id"] for index in validation}
        ),
        "development_test_task_ids": sorted(
            {examples[index]["task_id"] for index in test}
        ),
        "strongest_comparator": strongest,
        "repository_commit": config["repository_commit"],
        "config_sha256": None,
    }
    predictions = {
        "indexes": test,
        "text": test_scores["text"],
        "structured": test_scores["structured"],
        "candidate": test_scores["candidate"],
        "envelope": test_scores["envelope"],
    }
    summary = {
        "partition_metrics": {
            "train": {
                "tasks": len(fitted["training_task_ids"]),
                "rows": len(train),
                "negatives": int(np.sum(y_train == 0)),
                "positives": int(np.sum(y_train == 1)),
            },
            "validation": {
                "tasks": len(fitted["validation_task_ids"]),
                "rows": len(validation),
                "negatives": int(np.sum(y_validation == 0)),
                "positives": int(np.sum(y_validation == 1)),
            },
            "development_test": {
                "tasks": len(fitted["development_test_task_ids"]),
                "rows": len(test),
                "negatives": int(np.sum(y_test == 0)),
                "positives": int(np.sum(y_test == 1)),
            },
        },
        "threshold_selection": {
            "partition": "validation",
            "criterion": "maximum TPR at empirical FPR <= 0.05; ties use higher threshold",
            "thresholds": thresholds,
        },
        "metrics": test_metrics,
        "strongest_comparator": strongest,
        "candidate_minus_strongest_comparator_auc": delta,
        "gates": gates,
        "all_gates_passed": all(gates.values()),
        "slices": {
            "model": slice_metrics(
                examples, test, test_scores["candidate"], "model"
            ),
            "source_dataset": slice_metrics(
                examples, test, test_scores["candidate"], "source_dataset"
            ),
            "observed_categories": slice_metrics(
                examples,
                test,
                test_scores["candidate"],
                "observed_categories",
            ),
        },
    }
    return fitted, predictions, summary


def score_confirmation(
    examples: list[dict[str, Any]],
    fitted: dict[str, Any],
    config: dict[str, Any],
) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    indexes = np.arange(len(examples), dtype=np.int64)
    y = labels(examples, indexes)
    ensure_two_classes(y, "Confirmation")
    text = fitted["vectorizer"].transform([item["text"] for item in examples])
    numeric = sparse.csr_matrix(
        fitted["scaler"].transform(
            np.vstack([item["features"] for item in examples])
        )
    )
    scores = {
        "text": fitted["text_model"].predict_proba(text)[:, 1],
        "structured": fitted["structured_model"].predict_proba(numeric)[:, 1],
        "candidate": fitted["candidate_model"].predict_proba(
            sparse.hstack([text, numeric], format="csr")
        )[:, 1],
        "envelope": np.asarray(
            [item["envelope"] for item in examples], dtype=np.float64
        ),
    }
    thresholds = fitted["thresholds"]
    metrics = {
        name: metric_record(y, values, float(thresholds[name]))
        for name, values in scores.items()
    }
    strongest = str(fitted["strongest_comparator"])
    delta = task_cluster_auc_delta(
        examples,
        indexes,
        scores["candidate"],
        scores[strongest],
        repeats=int(config["bootstrap_repeats"]),
        seed=int(config["seed"]) + 1,
    )
    development_tasks = set(fitted["development_task_ids"])
    confirmation_tasks = {item["task_id"] for item in examples}
    overlap = sorted(development_tasks & confirmation_tasks)
    gate_config = config["confirmation_gates"]
    gates = {
        "task_ids_disjoint": not overlap,
        "candidate_auc": (
            metrics["candidate"]["auc"]
            >= float(gate_config["candidate_auc_min"])
        ),
        "candidate_tpr_at_5pct_fpr": (
            metrics["candidate"]["tpr_at_5pct_fpr"]
            >= float(gate_config["candidate_tpr_at_5fpr_min"])
        ),
        "auc_delta_vs_frozen_strongest_comparator": delta["point"] > 0.0,
        "auc_delta_task_bootstrap_lower": (
            delta["bootstrap_95"][0]
            >= float(gate_config["candidate_auc_delta_bootstrap_lower_min"])
        ),
        "fixed_threshold_fpr": (
            metrics["candidate"]["fixed_threshold"]["fpr"]
            <= float(gate_config["fixed_threshold_fpr_max"])
        ),
        "fixed_threshold_tpr": (
            metrics["candidate"]["fixed_threshold"]["tpr"]
            >= float(gate_config["fixed_threshold_tpr_min"])
        ),
    }
    summary = {
        "partition_metrics": {
            "confirmation": {
                "tasks": len(confirmation_tasks),
                "rows": len(indexes),
                "negatives": int(np.sum(y == 0)),
                "positives": int(np.sum(y == 1)),
            }
        },
        "thresholds": thresholds,
        "metrics": metrics,
        "frozen_strongest_comparator": strongest,
        "candidate_minus_frozen_strongest_comparator_auc": delta,
        "development_task_overlap": overlap,
        "gates": gates,
        "all_gates_passed": all(gates.values()),
        "slices": {
            "model": slice_metrics(
                examples, indexes, scores["candidate"], "model"
            ),
            "source_dataset": slice_metrics(
                examples,
                indexes,
                scores["candidate"],
                "source_dataset",
            ),
            "observed_categories": slice_metrics(
                examples,
                indexes,
                scores["candidate"],
                "observed_categories",
            ),
        },
    }
    predictions = {"indexes": indexes, **scores}
    return predictions, summary


def write_predictions(
    output: Path,
    examples: list[dict[str, Any]],
    predictions: dict[str, np.ndarray],
) -> None:
    indexes = predictions["indexes"]
    with (output / "raw_predictions.jsonl").open(
        "w", encoding="utf-8", newline="\n"
    ) as stream:
        for local_index, example_index in enumerate(indexes):
            item = examples[int(example_index)]
            stream.write(
                json.dumps(
                    {
                        "row_id": item["row_id"],
                        "task_id": item["task_id"],
                        "reference_row_id": item["reference_row_id"],
                        "target": item["target"],
                        "model": item["row"]["model"],
                        "source_dataset": item["row"]["source_dataset"],
                        "observed_categories": item["row"][
                            "observed_categories"
                        ],
                        "structured_features": item["features"].tolist(),
                        "scores": {
                            name: float(predictions[name][local_index])
                            for name in (
                                "text",
                                "structured",
                                "candidate",
                                "envelope",
                            )
                        },
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--frozen-model")
    args = parser.parse_args()
    started = time.perf_counter()

    config_path = Path(args.config).resolve()
    dataset_path = Path(args.dataset).resolve()
    manifest_path = Path(args.manifest).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["phase"] != args.phase:
        raise ValueError("Acquisition phase does not match evaluation phase")
    if manifest["repository_commit"] != config["repository_commit"]:
        raise ValueError("Repository commit does not match config")
    if manifest["dataset_sha256"] != sha256_file(dataset_path):
        raise ValueError("Dataset hash does not match acquisition manifest")
    expected_bucket = int(
        config[
            "development_bucket"
            if args.phase == "development"
            else "confirmation_bucket"
        ]
    )
    if int(manifest["bucket"]) != expected_bucket:
        raise ValueError("Dataset bucket does not match config")

    rows = load_jsonl(dataset_path)
    examples, references, ineligible = prepare_examples(rows)
    if not examples:
        raise ValueError("No eligible examples")
    reference_ids = {item["reference_row_id"] for item in references}
    evaluated_ids = {item["row_id"] for item in examples}
    if reference_ids & evaluated_ids:
        raise ValueError("A reference row is present in evaluation")
    if not np.all(
        np.isfinite(np.vstack([item["features"] for item in examples]))
    ):
        raise ValueError("A structured feature is non-finite")

    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=False)
    if args.phase == "development":
        fitted, predictions, phase_summary = fit_development(examples, config)
        fitted["config_sha256"] = sha256_file(config_path)
        joblib.dump(fitted, output / "frozen_model.joblib", compress=3)
        phase_summary["frozen_model_sha256"] = sha256_file(
            output / "frozen_model.joblib"
        )
    else:
        if not args.frozen_model:
            raise ValueError("Confirmation requires --frozen-model")
        model_path = Path(args.frozen_model).resolve()
        fitted = joblib.load(model_path)
        if fitted["repository_commit"] != config["repository_commit"]:
            raise ValueError("Frozen model repository commit does not match")
        if fitted["config_sha256"] != sha256_file(config_path):
            raise ValueError("Frozen model config hash does not match")
        predictions, phase_summary = score_confirmation(
            examples, fitted, config
        )
        phase_summary["frozen_model_sha256"] = sha256_file(model_path)

    write_predictions(output, examples, predictions)
    with (output / "reference_records.jsonl").open(
        "w", encoding="utf-8", newline="\n"
    ) as stream:
        for record in references:
            stream.write(
                json.dumps(record, sort_keys=True) + "\n"
            )
    task_ids = sorted({item["task_id"] for item in examples})
    (output / "task_ids.json").write_text(
        json.dumps(task_ids, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    summary = {
        "phase": args.phase,
        "method": "Reference-Conditioned Effect Delta",
        "dataset_sha256": sha256_file(dataset_path),
        "manifest_sha256": sha256_file(manifest_path),
        "config_sha256": sha256_file(config_path),
        "eligible_tasks": len(task_ids),
        "ineligible_task_ids": ineligible,
        "evaluated_rows": len(examples),
        "reference_rows": len(references),
        "reference_rows_excluded": len(reference_ids & evaluated_ids) == 0,
        "feature_names": FEATURE_NAMES,
        **phase_summary,
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output / "environment.json").write_text(
        json.dumps(
            environment_record(time.perf_counter() - started),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "phase": args.phase,
                "eligible_tasks": len(task_ids),
                "evaluated_rows": len(examples),
                "candidate_auc": phase_summary["metrics"]["candidate"]["auc"],
                "candidate_tpr_at_5pct_fpr": phase_summary["metrics"][
                    "candidate"
                ]["tpr_at_5pct_fpr"],
                "all_gates_passed": phase_summary["all_gates_passed"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
