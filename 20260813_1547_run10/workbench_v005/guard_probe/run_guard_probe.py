from __future__ import annotations

import itertools
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "guard_probe_results.json"
PREDICATES = (
    "authenticated",
    "resource_exists",
    "destination_empty",
    "owner_matches",
    "network_online",
    "schema_current",
)
STATE_COUNT = 1 << len(PREDICATES)
BUDGETS = (4, 6, 8, 10)
RANDOM_TRIALS = 500
SEED = 20260813


Literal = tuple[int, bool]
Term = tuple[Literal, ...]
Formula = tuple[Term, ...]


@dataclass(frozen=True)
class Candidate:
    formula: Formula
    truth_mask: int
    literal_count: int
    term_count: int
    text: str


def state_tuple(index: int) -> tuple[bool, ...]:
    return tuple(bool((index >> bit) & 1) for bit in range(len(PREDICATES)))


STATES = tuple(state_tuple(index) for index in range(STATE_COUNT))


def eval_term(term: Term, state: tuple[bool, ...]) -> bool:
    return all(state[var] is value for var, value in term)


def eval_formula(formula: Formula, state: tuple[bool, ...]) -> bool:
    return any(eval_term(term, state) for term in formula)


def literal_text(literal: Literal) -> str:
    variable, value = literal
    name = PREDICATES[variable]
    return name if value else f"not {name}"


def formula_text(formula: Formula) -> str:
    return " OR ".join("(" + " AND ".join(literal_text(lit) for lit in term) + ")" for term in formula)


def truth_mask(formula: Formula) -> int:
    mask = 0
    for index, state in enumerate(STATES):
        if eval_formula(formula, state):
            mask |= 1 << index
    return mask


def canonical_term(literals: Iterable[Literal]) -> Term | None:
    by_var: dict[int, bool] = {}
    for variable, value in literals:
        if variable in by_var and by_var[variable] is not value:
            return None
        by_var[variable] = value
    return tuple(sorted(by_var.items()))


def build_candidates() -> list[Candidate]:
    literals = [(variable, value) for variable in range(len(PREDICATES)) for value in (False, True)]
    terms: set[Term] = set()
    for size in (1, 2):
        for items in itertools.combinations(literals, size):
            term = canonical_term(items)
            if term is not None:
                terms.add(term)
    ordered_terms = sorted(terms)
    best_by_mask: dict[int, Candidate] = {}
    for term_count in (1, 2):
        for selected in itertools.combinations(ordered_terms, term_count):
            formula = tuple(sorted(selected))
            mask = truth_mask(formula)
            candidate = Candidate(
                formula=formula,
                truth_mask=mask,
                literal_count=sum(len(term) for term in formula),
                term_count=len(formula),
                text=formula_text(formula),
            )
            incumbent = best_by_mask.get(mask)
            key = (candidate.literal_count, candidate.term_count, candidate.text)
            if incumbent is None or key < (incumbent.literal_count, incumbent.term_count, incumbent.text):
                best_by_mask[mask] = candidate
    return sorted(best_by_mask.values(), key=lambda item: (item.literal_count, item.term_count, item.text))


CANDIDATES = build_candidates()
CANDIDATE_BY_MASK = {candidate.truth_mask: candidate for candidate in CANDIDATES}


def lit(name: str) -> Literal:
    value = not name.startswith("not_")
    base = name[4:] if not value else name
    return PREDICATES.index(base), value


def term(*names: str) -> Term:
    result = canonical_term(lit(name) for name in names)
    if result is None:
        raise ValueError(names)
    return result


GROUND_TRUTHS: tuple[tuple[str, Formula], ...] = (
    ("direct_export", (term("authenticated", "destination_empty"),)),
    ("owner_update", (term("authenticated", "owner_matches"),)),
    ("live_sync", (term("network_online", "schema_current"),)),
    ("safe_archive", (term("resource_exists", "destination_empty"),)),
    ("delegated_export", (term("authenticated", "owner_matches"), term("authenticated", "destination_empty"))),
    ("cached_sync", (term("network_online", "schema_current"), term("resource_exists", "schema_current"))),
    ("owner_or_schema_patch", (term("authenticated", "owner_matches"), term("resource_exists", "schema_current"))),
    ("online_or_empty_publish", (term("authenticated", "network_online"), term("authenticated", "destination_empty"))),
    ("recover_or_replace", (term("resource_exists", "owner_matches"), term("destination_empty", "schema_current"))),
    ("trusted_or_fresh_import", (term("authenticated", "schema_current"), term("owner_matches", "network_online"))),
    ("local_or_remote_commit", (term("owner_matches", "destination_empty"), term("network_online", "schema_current"))),
    ("existing_or_authorized_move", (term("resource_exists", "destination_empty"), term("authenticated", "owner_matches"))),
)


def labels_for(mask: int, queries: list[int]) -> list[bool]:
    return [bool((mask >> index) & 1) for index in queries]


def consistent_candidates(queries: list[int], labels: list[bool]) -> list[Candidate]:
    return [
        candidate
        for candidate in CANDIDATES
        if all(bool((candidate.truth_mask >> index) & 1) is label for index, label in zip(queries, labels))
    ]


def choose_simplest(version_space: list[Candidate]) -> Candidate:
    return min(version_space, key=lambda item: (item.literal_count, item.term_count, item.text))


def conservative_mask(version_space: list[Candidate]) -> int:
    mask = (1 << STATE_COUNT) - 1
    for candidate in version_space:
        mask &= candidate.truth_mask
    return mask


def active_queries(target_mask: int, source: int, budget: int) -> tuple[list[int], list[bool], list[int]]:
    queries = [source]
    labels = [True]
    version_sizes = [len(consistent_candidates(queries, labels))]
    while len(queries) - 1 < budget:
        version_space = consistent_candidates(queries, labels)
        remaining = [index for index in range(STATE_COUNT) if index not in queries]
        best_index = max(
            remaining,
            key=lambda index: (
                min(
                    sum(bool((candidate.truth_mask >> index) & 1) for candidate in version_space),
                    sum(not bool((candidate.truth_mask >> index) & 1) for candidate in version_space),
                ),
                -abs(sum(bool((candidate.truth_mask >> index) & 1) for candidate in version_space) - len(version_space) / 2),
                -index,
            ),
        )
        queries.append(best_index)
        labels.append(bool((target_mask >> best_index) & 1))
        version_sizes.append(len(consistent_candidates(queries, labels)))
    return queries, labels, version_sizes


def random_queries(target_mask: int, source: int, budget: int, rng: random.Random) -> tuple[list[int], list[bool]]:
    remaining = [index for index in range(STATE_COUNT) if index != source]
    selected = rng.sample(remaining, budget)
    queries = [source, *selected]
    return queries, labels_for(target_mask, queries)


def neighbor_queries(target_mask: int, source: int, budget: int, rng: random.Random) -> tuple[list[int], list[bool]]:
    neighbors = [source ^ (1 << bit) for bit in range(len(PREDICATES))]
    remaining = [index for index in range(STATE_COUNT) if index != source and index not in neighbors]
    selected = neighbors[:budget]
    if len(selected) < budget:
        selected.extend(rng.sample(remaining, budget - len(selected)))
    queries = [source, *selected]
    return queries, labels_for(target_mask, queries)


def local_then_active_queries(target_mask: int, source: int, budget: int) -> tuple[list[int], list[bool], list[int]]:
    queries = [source]
    labels = [True]
    version_sizes = [len(consistent_candidates(queries, labels))]
    for bit in range(min(budget, len(PREDICATES))):
        index = source ^ (1 << bit)
        queries.append(index)
        labels.append(bool((target_mask >> index) & 1))
        version_sizes.append(len(consistent_candidates(queries, labels)))
    while len(queries) - 1 < budget:
        version_space = consistent_candidates(queries, labels)
        remaining = [index for index in range(STATE_COUNT) if index not in queries]
        best_index = max(
            remaining,
            key=lambda index: (
                min(
                    sum(bool((candidate.truth_mask >> index) & 1) for candidate in version_space),
                    sum(not bool((candidate.truth_mask >> index) & 1) for candidate in version_space),
                ),
                -abs(sum(bool((candidate.truth_mask >> index) & 1) for candidate in version_space) - len(version_space) / 2),
                -index,
            ),
        )
        queries.append(best_index)
        labels.append(bool((target_mask >> best_index) & 1))
        version_sizes.append(len(consistent_candidates(queries, labels)))
    return queries, labels, version_sizes


def metrics(target_mask: int, predicted_mask: int) -> dict[str, float | int | bool]:
    tp = fp = fn = tn = 0
    total_cost = 0
    successes = 0
    for index in range(STATE_COUNT):
        actual = bool((target_mask >> index) & 1)
        predicted = bool((predicted_mask >> index) & 1)
        if predicted and actual:
            tp += 1
            successes += 1
            total_cost += 1
        elif predicted and not actual:
            fp += 1
            total_cost += 1
        elif not predicted and actual:
            fn += 1
            successes += 1
            total_cost += 4
        else:
            tn += 1
            successes += 1
            total_cost += 4
    return {
        "exact_function": target_mask == predicted_mask,
        "true_positive": tp,
        "false_admission": fp,
        "false_rejection": fn,
        "true_negative": tn,
        "admission_precision": tp / (tp + fp) if tp + fp else 1.0,
        "applicable_coverage": tp / (tp + fn) if tp + fn else 1.0,
        "terminal_success_rate": successes / STATE_COUNT,
        "mean_execution_cost": total_cost / STATE_COUNT,
    }


def aggregate(records: list[dict[str, float | int | bool]]) -> dict[str, float]:
    keys = (
        "exact_function",
        "false_admission",
        "false_rejection",
        "admission_precision",
        "applicable_coverage",
        "terminal_success_rate",
        "mean_execution_cost",
    )
    return {key: sum(float(record[key]) for record in records) / len(records) for key in keys}


def main() -> None:
    rng = random.Random(SEED)
    task_records: list[dict[str, object]] = []
    summaries: dict[str, object] = {}
    for budget in BUDGETS:
        active_simplest_metrics: list[dict[str, float | int | bool]] = []
        active_conservative_metrics: list[dict[str, float | int | bool]] = []
        local_active_simplest_metrics: list[dict[str, float | int | bool]] = []
        local_active_conservative_metrics: list[dict[str, float | int | bool]] = []
        neighbor_simplest_metrics: list[dict[str, float | int | bool]] = []
        neighbor_conservative_metrics: list[dict[str, float | int | bool]] = []
        random_simplest_metrics_all: list[dict[str, float | int | bool]] = []
        random_conservative_metrics_all: list[dict[str, float | int | bool]] = []
        always_reject_metrics: list[dict[str, float | int | bool]] = []
        for task_name, formula in GROUND_TRUTHS:
            target_mask = truth_mask(formula)
            always_reject_metrics.append(metrics(target_mask, 0))
            source = next(index for index in range(STATE_COUNT) if (target_mask >> index) & 1)
            active_q, active_y, version_sizes = active_queries(target_mask, source, budget)
            active_version = consistent_candidates(active_q, active_y)
            active_prediction = choose_simplest(active_version)
            active_simplest_score = metrics(target_mask, active_prediction.truth_mask)
            active_conservative_score = metrics(target_mask, conservative_mask(active_version))
            active_simplest_metrics.append(active_simplest_score)
            active_conservative_metrics.append(active_conservative_score)

            local_active_q, local_active_y, local_active_version_sizes = local_then_active_queries(target_mask, source, budget)
            local_active_version = consistent_candidates(local_active_q, local_active_y)
            local_active_prediction = choose_simplest(local_active_version)
            local_active_simplest_score = metrics(target_mask, local_active_prediction.truth_mask)
            local_active_conservative_score = metrics(target_mask, conservative_mask(local_active_version))
            local_active_simplest_metrics.append(local_active_simplest_score)
            local_active_conservative_metrics.append(local_active_conservative_score)

            neighbor_q, neighbor_y = neighbor_queries(target_mask, source, budget, rng)
            neighbor_version = consistent_candidates(neighbor_q, neighbor_y)
            neighbor_prediction = choose_simplest(neighbor_version)
            neighbor_simplest_score = metrics(target_mask, neighbor_prediction.truth_mask)
            neighbor_conservative_score = metrics(target_mask, conservative_mask(neighbor_version))
            neighbor_simplest_metrics.append(neighbor_simplest_score)
            neighbor_conservative_metrics.append(neighbor_conservative_score)

            random_task_simplest_metrics: list[dict[str, float | int | bool]] = []
            random_task_conservative_metrics: list[dict[str, float | int | bool]] = []
            for _ in range(RANDOM_TRIALS):
                random_q, random_y = random_queries(target_mask, source, budget, rng)
                random_version = consistent_candidates(random_q, random_y)
                random_prediction = choose_simplest(random_version)
                random_simplest_score = metrics(target_mask, random_prediction.truth_mask)
                random_conservative_score = metrics(target_mask, conservative_mask(random_version))
                random_task_simplest_metrics.append(random_simplest_score)
                random_task_conservative_metrics.append(random_conservative_score)
                random_simplest_metrics_all.append(random_simplest_score)
                random_conservative_metrics_all.append(random_conservative_score)

            task_records.append(
                {
                    "task": task_name,
                    "ground_truth": formula_text(formula),
                    "positive_states": target_mask.bit_count(),
                    "budget": budget,
                    "source_state": {PREDICATES[i]: value for i, value in enumerate(STATES[source])},
                    "active": {
                        "queries": active_q,
                        "labels": active_y,
                        "version_space_sizes": version_sizes,
                        "simplest_consistent_prediction": active_prediction.text,
                        "simplest_consistent_metrics": active_simplest_score,
                        "unanimous_conservative_metrics": active_conservative_score,
                    },
                    "local_then_active": {
                        "queries": local_active_q,
                        "labels": local_active_y,
                        "version_space_sizes": local_active_version_sizes,
                        "simplest_consistent_prediction": local_active_prediction.text,
                        "simplest_consistent_metrics": local_active_simplest_score,
                        "unanimous_conservative_metrics": local_active_conservative_score,
                    },
                    "single_flip_then_random": {
                        "queries": neighbor_q,
                        "labels": neighbor_y,
                        "simplest_consistent_prediction": neighbor_prediction.text,
                        "simplest_consistent_metrics": neighbor_simplest_score,
                        "unanimous_conservative_metrics": neighbor_conservative_score,
                    },
                    "random_same_budget": {
                        "simplest_consistent": aggregate(random_task_simplest_metrics),
                        "unanimous_conservative": aggregate(random_task_conservative_metrics),
                    },
                }
            )
        summaries[str(budget)] = {
            "active_version_space": {
                "simplest_consistent": aggregate(active_simplest_metrics),
                "unanimous_conservative": aggregate(active_conservative_metrics),
            },
            "local_then_active": {
                "simplest_consistent": aggregate(local_active_simplest_metrics),
                "unanimous_conservative": aggregate(local_active_conservative_metrics),
            },
            "single_flip_then_random": {
                "simplest_consistent": aggregate(neighbor_simplest_metrics),
                "unanimous_conservative": aggregate(neighbor_conservative_metrics),
            },
            "random_same_budget": {
                "simplest_consistent": aggregate(random_simplest_metrics_all),
                "unanimous_conservative": aggregate(random_conservative_metrics_all),
            },
            "always_reject": aggregate(always_reject_metrics),
        }

    document = {
        "schema_version": 1,
        "seed": SEED,
        "predicate_names": list(PREDICATES),
        "state_count_per_task": STATE_COUNT,
        "hypothesis_space_unique_functions": len(CANDIDATES),
        "ground_truth_tasks": len(GROUND_TRUTHS),
        "random_trials_per_task_budget": RANDOM_TRIALS,
        "budgets_excluding_known_positive_source": list(BUDGETS),
        "cost_model": {"admitted_fast_skill": 1, "rejected_safe_fallback": 4, "false_admission": "terminal_failure"},
        "summary": summaries,
        "tasks": task_records,
    }
    OUTPUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
