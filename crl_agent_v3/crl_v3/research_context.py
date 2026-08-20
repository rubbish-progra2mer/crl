from __future__ import annotations

import json
import math
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from crl_v3.comparison import (
    _build_payload as build_comparison_payload,
    _load_closed_attempt as load_closed_attempt,
    render_comparison_report,
)
from crl_v3.experiment import (
    formal_attempt_integrity_execution_sha256,
    supporting_attempt_execution_sha256,
)
from crl_v3.falsification import (
    experiment_spec_from_mapping,
    validate_experiment_spec,
    plan_from_mapping,
    validate_plan,
)
from crl_v3.hypotheses import (
    hypothesis_record_to_dict,
    portfolio_from_mapping,
    validate_portfolio,
)
from crl_v3.prior_audit import load_prior_audit
from crl_v3.research_retrieval import verify_existing_search
from crl_v3.workspace import (
    ResearchWorkspace,
    _current_version,
    _required_file,
    _sha256,
    _validate_utf8_lf,
)


AUTHORITY_CLASSES = (
    "EXTERNAL_EVIDENCE",
    "CARD_SYNTHESIS",
    "RUN_HYPOTHESIS",
    "RUN_EXPERIMENT_FACT",
    "RESEARCHER_INTERPRETATION",
)
PRIORITY_MINIMUM_CHARS = 256
FAIR_ROUND_CHARS = 256
APPROX_TOKEN_CHARS = 4

_MARKDOWN_STEMS = (
    "problem",
    "research_map",
    "nearest_prior",
    "candidate",
    "evidence_packet",
    "selection_context",
    "memory",
    "failure_attribution",
    "seed",
    "decision",
)


@dataclass(frozen=True, slots=True)
class ResearchContextFragment:
    source_path: str
    source_sha256: str
    authority_class: str
    fragment_id: str
    content: str
    priority: str | None = None


class _Collector:
    def __init__(self, workspace: ResearchWorkspace) -> None:
        self.workspace = workspace
        self.sources: dict[str, str] = {}
        self.fragments: list[ResearchContextFragment] = []

    def read(self, path: Path) -> tuple[str, bytes, str]:
        data = _required_file(path, within=self.workspace.workspace_path)
        if not data:
            raise ValueError(f"empty research context source: {path}")
        relative = path.relative_to(self.workspace.workspace_path).as_posix()
        digest = _sha256(data)
        previous = self.sources.setdefault(relative, digest)
        if previous != digest:
            raise ValueError(f"research context source changed while read: {relative}")
        return relative, data, digest

    def add(
        self,
        path: Path,
        authority_class: str,
        fragment_id: str,
        content: str,
        *,
        priority: str | None = None,
    ) -> None:
        if authority_class not in AUTHORITY_CLASSES:
            raise ValueError(f"invalid authority class: {authority_class}")
        relative, _, digest = self.read(path)
        normalized = content.replace("\r\n", "\n").replace("\r", "\n")
        if not normalized.strip():
            return
        if not normalized.endswith("\n"):
            normalized += "\n"
        self.fragments.append(
            ResearchContextFragment(
                relative,
                digest,
                authority_class,
                fragment_id,
                normalized,
                priority,
            )
        )

    def verify_unchanged(self) -> None:
        for relative, expected in sorted(self.sources.items()):
            data = _required_file(
                self.workspace.workspace_path / relative,
                within=self.workspace.workspace_path,
            )
            if _sha256(data) != expected:
                raise ValueError(
                    f"research context source changed while rendering: {relative}"
                )


def render_research_context(
    workspace: ResearchWorkspace,
    *,
    hypothesis_ids: Iterable[str] = (),
    search_ids: Iterable[str] = (),
    max_characters: int | None = None,
    max_approx_tokens: int | None = None,
    include_charter: bool = True,
    include_portfolio: bool = True,
    include_research_bundle: bool = True,
    include_prior_audit: bool = True,
    include_falsification: bool = True,
    include_experiments: bool = True,
    include_markdown: bool = True,
) -> bytes:
    """Render one deterministic, non-authoritative, Run-local context view."""

    current_version = _current_version(
        workspace.workspace_path / "RUN_STATUS.md", within=workspace.workspace_path
    )
    if workspace.version != current_version:
        raise ValueError(
            f"research context requires CURRENT_VERSION {current_version}, "
            f"not {workspace.version}"
        )
    selected_ids = tuple(sorted(set(_identifier(item, "hypothesis ID") for item in hypothesis_ids)))
    requested_search_ids = tuple(
        sorted(set(_identifier(item, "search ID") for item in search_ids))
    )
    budget, budget_kind = _effective_budget(max_characters, max_approx_tokens)
    collector = _Collector(workspace)

    portfolio, portfolio_path, portfolio_data = _read_run_local_portfolio(workspace)
    hypothesis_index = (
        {item.hypothesis_id: item for item in portfolio.hypotheses}
        if portfolio is not None
        else {}
    )
    unknown = sorted(set(selected_ids) - set(hypothesis_index))
    if unknown:
        raise KeyError(f"unknown hypothesis ids: {unknown}")

    if include_charter:
        charter = workspace.workspace_path / "RUN_CHARTER.md"
        _, data, _ = collector.read(charter)
        collector.add(
            charter,
            "RESEARCHER_INTERPRETATION",
            "run-charter-direction-boundary",
            data.decode("utf-8"),
        )

    if include_portfolio and portfolio is not None:
        assert portfolio_path is not None and portfolio_data is not None
        envelope = {
            "schema_version": portfolio.schema_version,
            "run_id": portfolio.run_id,
            "version": portfolio.version,
            "revision": portfolio.revision,
            "created_at_utc": portfolio.created_at_utc,
            "updated_at_utc": portfolio.updated_at_utc,
            "hypothesis_count": len(portfolio.hypotheses),
        }
        collector.add(
            portfolio_path,
            "RUN_HYPOTHESIS",
            "portfolio-envelope",
            _json_text(envelope),
        )
        for record in portfolio.hypotheses:
            if selected_ids and record.hypothesis_id not in selected_ids:
                continue
            collector.add(
                portfolio_path,
                "RUN_HYPOTHESIS",
                f"hypothesis:{record.hypothesis_id}",
                _json_text(hypothesis_record_to_dict(record)),
                priority=(
                    "active-candidate"
                    if record.status in {"active", "escalated"}
                    else None
                ),
            )

    if include_research_bundle:
        _collect_searches(
            collector,
            selected_ids=set(selected_ids),
            requested_search_ids=requested_search_ids,
        )
    if include_prior_audit:
        _collect_prior_audits(collector, selected_ids=set(selected_ids))
    if include_falsification:
        _collect_falsification(
            collector,
            hypothesis_index=hypothesis_index,
            selected_ids=set(selected_ids),
        )
    included_attempt_ids: set[str] = set()
    if include_experiments:
        included_attempt_ids = _collect_experiments(
            collector, selected_ids=set(selected_ids)
        )
        _collect_comparisons(
            collector,
            selected_ids=set(selected_ids),
            included_attempt_ids=included_attempt_ids,
        )
    if include_markdown:
        _collect_markdown(collector)

    fragments = tuple(
        sorted(
            collector.fragments,
            key=lambda item: (
                item.source_path,
                item.fragment_id,
                item.authority_class,
            ),
        )
    )
    rendered = _render_budgeted(
        workspace,
        fragments,
        budget=budget,
        budget_kind=budget_kind,
    )
    collector.verify_unchanged()
    return rendered.encode("utf-8")


def _read_run_local_portfolio(
    workspace: ResearchWorkspace,
) -> tuple[object | None, Path | None, bytes | None]:
    path = workspace.hypotheses_path
    try:
        data = _required_file(path, within=workspace.workspace_path)
    except FileNotFoundError:
        return None, None, None
    if not data:
        raise ValueError(f"empty hypothesis portfolio: {path}")
    value = _json_object(data, "hypothesis portfolio")
    portfolio = portfolio_from_mapping(value)
    scrubbed = replace(
        portfolio,
        hypotheses=tuple(
            replace(
                record,
                target_failure=replace(record.target_failure, evidence_ids=()),
            )
            for record in portfolio.hypotheses
        ),
    )
    validate_portfolio(
        scrubbed,
        expected_run_id=workspace.workspace_path.name,
        expected_version=workspace.version,
    )
    return portfolio, path, data


def _collect_searches(
    collector: _Collector,
    *,
    selected_ids: set[str],
    requested_search_ids: Sequence[str],
) -> None:
    workspace = collector.workspace
    root = workspace.workspace_path / f"hypotheses_{workspace.version}" / "searches"
    workspace.assert_write_target(root)
    if requested_search_ids:
        identifiers = requested_search_ids
    elif not root.exists():
        return
    else:
        if not root.is_dir():
            raise ValueError(f"research search root is not a directory: {root}")
        identifiers = tuple(
            path.name
            for path in sorted(root.iterdir(), key=lambda item: item.name)
            if not path.name.startswith(".")
        )

    snapshots = []
    for identifier in identifiers:
        snapshot = verify_existing_search(workspace, identifier)
        if snapshot is None:
            raise FileNotFoundError(f"missing research search snapshot: {identifier}")
        files = dict(snapshot.files)
        request = _json_object(files["request.json"], "research request")
        identity = request.get("input_identity")
        if not isinstance(identity, dict):
            raise ValueError("research request input_identity is invalid")
        if identity.get("run_id") != workspace.workspace_path.name:
            raise ValueError("research search is bound to a different Run")
        if identity.get("version") != workspace.version:
            raise ValueError("research search is bound to a different version")
        hypothesis_id = identity.get("hypothesis_id")
        if selected_ids and hypothesis_id not in selected_ids:
            continue
        snapshots.append((snapshot.created_at_utc, identifier, files))
    if not requested_search_ids and snapshots:
        snapshots = [max(snapshots, key=lambda item: (item[0], item[1]))]

    for _, identifier, files in snapshots:
        directory = root / identifier
        for name, data in files.items():
            collector.read(directory / name)
        collector.add(
            directory / "request.json",
            "RUN_HYPOTHESIS",
            f"research-bundle:{identifier}:request",
            files["request.json"].decode("utf-8"),
        )
        result = _json_object(files["result.json"], "research result")
        queries = result.get("queries")
        if not isinstance(queries, list):
            raise ValueError("research result queries are invalid")
        for query_index, query in enumerate(queries):
            if not isinstance(query, dict) or not isinstance(query.get("routes"), list):
                raise ValueError("research result query routes are invalid")
            query_id = str(query.get("query_id", f"q{query_index + 1:03d}"))
            for route_index, route in enumerate(query["routes"]):
                if not isinstance(route, dict):
                    raise ValueError("research result route is invalid")
                route_name = str(route.get("route", f"route-{route_index + 1}"))
                authority = (
                    "EXTERNAL_EVIDENCE"
                    if route_name == "passage_hybrid"
                    else "CARD_SYNTHESIS"
                )
                collector.add(
                    directory / "result.json",
                    authority,
                    f"research-bundle:{identifier}:{query_id}:{route_name}",
                    _json_text(
                        {
                            "query_id": query_id,
                            "purpose": query.get("purpose"),
                            "route": route,
                        }
                    ),
                )
        diagnostics = result.get("diagnostics")
        if diagnostics is not None:
            collector.add(
                directory / "result.json",
                "CARD_SYNTHESIS",
                f"research-bundle:{identifier}:diagnostics",
                _json_text(diagnostics),
            )


def _collect_prior_audits(
    collector: _Collector, *, selected_ids: set[str]
) -> None:
    workspace = collector.workspace
    root = workspace.workspace_path / f"hypotheses_{workspace.version}" / "priors"
    workspace.assert_write_target(root)
    if not root.exists():
        return
    if not root.is_dir():
        raise ValueError(f"prior audit root is not a directory: {root}")
    for directory in sorted(root.iterdir(), key=lambda item: item.name):
        if directory.name.startswith("."):
            continue
        snapshot = load_prior_audit(workspace, directory.name)
        request = snapshot.request
        if request.get("run_id") != workspace.workspace_path.name:
            raise ValueError("prior audit is bound to a different Run")
        if request.get("version") != workspace.version:
            raise ValueError("prior audit is bound to a different version")
        hypothesis = request.get("hypothesis")
        if not isinstance(hypothesis, dict):
            raise ValueError("prior audit hypothesis identity is invalid")
        hypothesis_id = hypothesis.get("hypothesis_id")
        if selected_ids and hypothesis_id not in selected_ids:
            continue
        request_path = directory / "request.json"
        candidates_path = directory / "candidates.json"
        report_path = directory / "report.md"
        for path in (request_path, candidates_path, report_path):
            collector.read(path)
        collector.add(
            request_path,
            "RUN_HYPOTHESIS",
            f"prior-audit:{directory.name}:request",
            _required_file(request_path, within=workspace.workspace_path).decode("utf-8"),
        )
        candidates = snapshot.candidates.get("candidates")
        if not isinstance(candidates, list):
            raise ValueError("prior audit candidates are invalid")
        for index, candidate in enumerate(candidates):
            collector.add(
                candidates_path,
                "CARD_SYNTHESIS",
                f"prior-audit:{directory.name}:candidate:{index + 1:04d}",
                _json_text(candidate),
            )
        report_schema = request.get("schema_version", 1)
        collector.add(
            report_path,
            "RUN_HYPOTHESIS" if report_schema == 3 else "RESEARCHER_INTERPRETATION",
            (
                f"prior-audit:{directory.name}:machine-report"
                if report_schema == 3
                else f"prior-audit:{directory.name}:legacy-manual-report"
            ),
            _required_file(report_path, within=workspace.workspace_path).decode("utf-8"),
        )
        assessment_warning = ""
        if snapshot.assessment_warnings:
            assessment_warning = (
                "PRIOR_ASSESSMENT_WARNING: 该解释未通过轻量解析/绑定检查，"
                "不得无提示地当作正常、正确绑定的科研解释。\n"
                f"ASSESSMENT_PATH: hypotheses_{workspace.version}/priors/"
                f"{directory.name}/assessment.md\n"
                + "\n".join(
                    f"- {warning}" for warning in snapshot.assessment_warnings
                )
                + "\n\n"
            )
        if snapshot.assessment is not None:
            assessment_path = directory / "assessment.md"
            collector.read(assessment_path)
            collector.add(
                assessment_path,
                "RESEARCHER_INTERPRETATION",
                (
                    f"prior-audit:{directory.name}:assessment-with-warnings"
                    if snapshot.assessment_warnings
                    else f"prior-audit:{directory.name}:assessment"
                ),
                assessment_warning + snapshot.assessment,
            )
        elif snapshot.assessment_warnings:
            collector.add(
                request_path,
                "RESEARCHER_INTERPRETATION",
                f"prior-audit:{directory.name}:assessment-warning",
                assessment_warning,
            )


def _collect_falsification(
    collector: _Collector,
    *,
    hypothesis_index: Mapping[str, object],
    selected_ids: set[str],
) -> None:
    workspace = collector.workspace
    plan_root = (
        workspace.workspace_path
        / f"hypotheses_{workspace.version}"
        / "falsification"
    )
    workspace.assert_write_target(plan_root)
    if plan_root.exists():
        if not plan_root.is_dir():
            raise ValueError(f"falsification root is not a directory: {plan_root}")
        for path in sorted(plan_root.iterdir(), key=lambda item: item.name):
            if path.name.startswith("."):
                continue
            if path.suffix != ".json":
                raise ValueError(f"unexpected falsification file: {path}")
            _, data, _ = collector.read(path)
            plan = plan_from_mapping(_json_object(data, "falsification plan"))
            validate_plan(
                plan,
                expected_run_id=workspace.workspace_path.name,
                expected_version=workspace.version,
            )
            if plan.plan_id != path.stem or plan.hypothesis_id not in hypothesis_index:
                raise ValueError("falsification plan identity mismatch")
            if selected_ids and plan.hypothesis_id not in selected_ids:
                continue
            collector.add(
                path,
                "RUN_HYPOTHESIS",
                f"falsification-plan:{plan.plan_id}",
                data.decode("utf-8"),
                priority="explicit-falsification",
            )

    spec_root = workspace.experiment_path / "specs"
    workspace.assert_write_target(spec_root)
    if spec_root.exists():
        if not spec_root.is_dir():
            raise ValueError(f"experiment spec root is not a directory: {spec_root}")
        for path in sorted(spec_root.iterdir(), key=lambda item: item.name):
            if path.name.startswith("."):
                continue
            if path.suffix != ".json":
                raise ValueError(f"unexpected experiment spec file: {path}")
            _, data, _ = collector.read(path)
            spec = experiment_spec_from_mapping(_json_object(data, "experiment spec"))
            validate_experiment_spec(
                spec,
                expected_run_id=workspace.workspace_path.name,
                expected_version=workspace.version,
            )
            if spec.experiment_id != path.stem or spec.hypothesis_id not in hypothesis_index:
                raise ValueError("experiment spec identity mismatch")
            if selected_ids and spec.hypothesis_id not in selected_ids:
                continue
            collector.add(
                path,
                "RUN_HYPOTHESIS",
                f"experiment-spec:{spec.experiment_id}",
                data.decode("utf-8"),
                priority="explicit-falsification",
            )


def _collect_experiments(
    collector: _Collector, *, selected_ids: set[str]
) -> set[str]:
    workspace = collector.workspace
    root = workspace.experiment_path / "attempts"
    workspace.assert_write_target(root)
    included: set[str] = set()
    if not root.exists():
        return included
    if not root.is_dir():
        raise ValueError(f"attempt root is not a directory: {root}")
    for directory in sorted(root.iterdir(), key=lambda item: item.name):
        if directory.name.startswith("."):
            continue
        execution_path = directory / "execution.json"
        _, execution_data, execution_sha = collector.read(execution_path)
        execution = _json_object(execution_data, "attempt execution")
        schema = execution.get("schema_version")
        if schema in {7, 8}:
            verified_sha = formal_attempt_integrity_execution_sha256(
                workspace, directory.name
            )
        elif schema in {5, 6}:
            verified_sha = supporting_attempt_execution_sha256(workspace, directory.name)
        else:
            raise ValueError(f"unsupported attempt schema: {directory.name}")
        if verified_sha != execution_sha:
            raise ValueError(f"attempt execution changed while read: {directory.name}")

        spec_path = directory / "spec.json"
        hypothesis_id = None
        spec_data = None
        if spec_path.exists():
            _, spec_data, _ = collector.read(spec_path)
            spec = experiment_spec_from_mapping(_json_object(spec_data, "attempt spec"))
            validate_experiment_spec(
                spec,
                expected_run_id=workspace.workspace_path.name,
                expected_version=workspace.version,
            )
            hypothesis_id = spec.hypothesis_id
        if selected_ids and hypothesis_id not in selected_ids:
            continue
        included.add(directory.name)
        collector.add(
            execution_path,
            "RUN_EXPERIMENT_FACT",
            f"attempt:{directory.name}:execution",
            execution_data.decode("utf-8"),
        )
        if spec_data is not None:
            collector.add(
                spec_path,
                "RUN_HYPOTHESIS",
                f"attempt:{directory.name}:registered-spec",
                spec_data.decode("utf-8"),
            )
        metrics_path = directory / "metrics.json"
        if metrics_path.exists():
            _, metrics_data, _ = collector.read(metrics_path)
            collector.add(
                metrics_path,
                "RUN_EXPERIMENT_FACT",
                f"attempt:{directory.name}:metrics",
                metrics_data.decode("utf-8"),
            )
    return included


def _collect_comparisons(
    collector: _Collector,
    *,
    selected_ids: set[str],
    included_attempt_ids: set[str],
) -> None:
    workspace = collector.workspace
    root = workspace.experiment_path / "comparisons"
    workspace.assert_write_target(root)
    if not root.exists():
        return
    if not root.is_dir():
        raise ValueError(f"comparison root is not a directory: {root}")
    for directory in sorted(root.iterdir(), key=lambda item: item.name):
        if directory.name.startswith("."):
            continue
        names = tuple(sorted(path.name for path in directory.iterdir()))
        if names != ("comparison.json", "report.md"):
            raise ValueError(f"comparison artifacts are incomplete: {directory}")
        json_path = directory / "comparison.json"
        report_path = directory / "report.md"
        _, json_data, _ = collector.read(json_path)
        _, report_data, _ = collector.read(report_path)
        payload = _json_object(json_data, "comparison")
        if (
            payload.get("schema_version") not in {1, 2}
            or payload.get("artifact_kind") != "attempt_fact_comparison"
            or payload.get("comparison_id") != directory.name
            or payload.get("run_id") != workspace.workspace_path.name
            or payload.get("version") != workspace.version
        ):
            raise ValueError("comparison identity mismatch")
        candidate_summary = payload.get("candidate_attempt")
        baselines = payload.get("baseline_attempts")
        if (
            not isinstance(candidate_summary, dict)
            or not isinstance(candidate_summary.get("attempt_id"), str)
            or not isinstance(baselines, list)
            or not all(
                isinstance(item, dict) and isinstance(item.get("attempt_id"), str)
                for item in baselines
            )
        ):
            raise ValueError("comparison attempt summaries are invalid")
        candidate = load_closed_attempt(workspace, candidate_summary["attempt_id"])
        baseline_attempts = tuple(
            load_closed_attempt(workspace, item["attempt_id"]) for item in baselines
        )
        expected_payload = build_comparison_payload(
            workspace,
            directory.name,
            candidate,
            baseline_attempts,
            schema_version=int(payload["schema_version"]),
        )
        if _json_text(payload) != _json_text(expected_payload):
            raise ValueError("comparison facts do not match their attempt sources")
        attempt_ids = {
            candidate.attempt_id,
            *(item.attempt_id for item in baseline_attempts),
        }
        expected_report = render_comparison_report(payload).encode("utf-8")
        if report_data != expected_report:
            raise ValueError("comparison report bytes do not match comparison facts")
        if selected_ids and not (attempt_ids & included_attempt_ids):
            continue
        collector.add(
            json_path,
            "RUN_EXPERIMENT_FACT",
            f"comparison:{directory.name}",
            json_data.decode("utf-8"),
        )


def _collect_markdown(collector: _Collector) -> None:
    workspace = collector.workspace
    mappings = [
        (workspace.document_path(stem), "RESEARCHER_INTERPRETATION", stem)
        for stem in _MARKDOWN_STEMS
    ]
    mappings.extend(
        (
            (workspace.experiment_path / "plan.md", "RUN_HYPOTHESIS", "experiment-plan"),
            (
                workspace.experiment_path / "result.md",
                "RESEARCHER_INTERPRETATION",
                "experiment-result-interpretation",
            ),
        )
    )
    for path, authority, fragment_id in mappings:
        if not path.exists():
            continue
        _, data, _ = collector.read(path)
        collector.add(path, authority, f"markdown:{fragment_id}", data.decode("utf-8"))


def _effective_budget(
    max_characters: int | None, max_approx_tokens: int | None
) -> tuple[int | None, str]:
    if max_characters is not None and max_approx_tokens is not None:
        raise ValueError("choose max_characters or max_approx_tokens, not both")
    if max_characters is not None:
        if type(max_characters) is not int or max_characters <= 0:
            raise ValueError("max_characters must be a positive integer")
        return max_characters, f"characters={max_characters}"
    if max_approx_tokens is not None:
        if type(max_approx_tokens) is not int or max_approx_tokens <= 0:
            raise ValueError("max_approx_tokens must be a positive integer")
        return (
            max_approx_tokens * APPROX_TOKEN_CHARS,
            f"approx_tokens={max_approx_tokens};1_token={APPROX_TOKEN_CHARS}_characters",
        )
    return None, "unbounded"


def _render_budgeted(
    workspace: ResearchWorkspace,
    fragments: Sequence[ResearchContextFragment],
    *,
    budget: int | None,
    budget_kind: str,
) -> str:
    allocations = [len(item.content) for item in fragments]
    if budget is None:
        return _render_allocations(workspace, fragments, allocations, budget_kind)
    full = _render_allocations(workspace, fragments, allocations, budget_kind)
    if len(full) <= budget:
        return full

    allocations = [0] * len(fragments)
    baseline = _render_allocations(workspace, fragments, allocations, budget_kind)
    if len(baseline) > budget:
        raise ValueError(
            "research context budget is too small for the complete omission inventory; "
            f"requires at least {len(baseline)} characters"
        )
    for index, fragment in enumerate(fragments):
        if fragment.priority is not None:
            allocations[index] = min(PRIORITY_MINIMUM_CHARS, len(fragment.content))
    minimum = _render_allocations(workspace, fragments, allocations, budget_kind)
    if len(minimum) > budget:
        raise ValueError(
            "research context budget is too small for active/falsification minimum quotas; "
            f"requires at least {len(minimum)} characters"
        )

    while True:
        progressed = False
        for index, fragment in enumerate(fragments):
            remaining = len(fragment.content) - allocations[index]
            if remaining <= 0:
                continue
            maximum = min(FAIR_ROUND_CHARS, remaining)
            increment = _largest_fitting_increment(
                workspace,
                fragments,
                allocations,
                index,
                maximum,
                budget,
                budget_kind,
            )
            if increment:
                allocations[index] += increment
                progressed = True
        if not progressed:
            break
    return _render_allocations(workspace, fragments, allocations, budget_kind)


def _largest_fitting_increment(
    workspace: ResearchWorkspace,
    fragments: Sequence[ResearchContextFragment],
    allocations: list[int],
    index: int,
    maximum: int,
    budget: int,
    budget_kind: str,
) -> int:
    original = allocations[index]
    allocations[index] = original + maximum
    if len(_render_allocations(workspace, fragments, allocations, budget_kind)) <= budget:
        allocations[index] = original
        return maximum
    allocations[index] = original
    low, high = 1, maximum - 1
    best = 0
    while low <= high:
        middle = (low + high) // 2
        allocations[index] = original + middle
        fits = len(
            _render_allocations(workspace, fragments, allocations, budget_kind)
        ) <= budget
        allocations[index] = original
        if fits:
            best = middle
            low = middle + 1
        else:
            high = middle - 1
    return best


def _render_allocations(
    workspace: ResearchWorkspace,
    fragments: Sequence[ResearchContextFragment],
    allocations: Sequence[int],
    budget_kind: str,
) -> str:
    lines = [
        "# CRL Research Context View",
        "",
        "> NON_AUTHORITATIVE_READ_ONLY_VIEW；不写回、不冻结、不评分、不作科研决策，也不替代 Review render-input。",
        "",
        f"- RUN_ID: `{workspace.workspace_path.name}`",
        f"- VERSION: `{workspace.version}`",
        f"- BUDGET: `{budget_kind}`",
        f"- AUTHORITY_CLASSES: `{', '.join(AUTHORITY_CLASSES)}`",
        (
            "- TRUNCATION_POLICY: active-candidate 与 explicit-falsification 各片段"
            f"最低 {PRIORITY_MINIMUM_CHARS} 字符；其后全部片段按来源路径/片段标识排序，"
            f"每轮各分配至多 {FAIR_ROUND_CHARS} 字符；不读取或使用分数。"
        ),
        "",
        "## Fragments",
        "",
    ]
    included = 0
    for index, (fragment, count) in enumerate(zip(fragments, allocations), start=1):
        if count <= 0:
            continue
        included += 1
        lines.extend(
            (
                f"### Fragment {index:04d}: `{fragment.fragment_id}`",
                "",
                f"- SOURCE_PATH: `{fragment.source_path}`",
                f"- SOURCE_SHA256: `{fragment.source_sha256}`",
                f"- AUTHORITY_CLASS: `{fragment.authority_class}`",
                f"- PRIORITY: `{fragment.priority or 'none'}`",
                f"- INCLUDED_CHARACTERS: `{count}/{len(fragment.content)}`",
                "",
                "----- BEGIN FRAGMENT CONTENT -----",
                fragment.content[:count].rstrip("\n"),
                "----- END FRAGMENT CONTENT -----",
                "",
            )
        )
    if included == 0:
        lines.extend(("- （无已纳入片段）", ""))

    lines.extend(("## Omitted Content Inventory", ""))
    omitted = 0
    for fragment, count in zip(fragments, allocations):
        if count >= len(fragment.content):
            continue
        omitted += 1
        lines.append(
            "- "
            f"SOURCE_PATH=`{fragment.source_path}`; "
            f"SOURCE_SHA256=`{fragment.source_sha256}`; "
            f"AUTHORITY_CLASS=`{fragment.authority_class}`; "
            f"FRAGMENT_ID=`{fragment.fragment_id}`; "
            f"INCLUDED_CHARACTERS={count}; "
            f"OMITTED_CHARACTERS={len(fragment.content) - count}; "
            "REASON=deterministic_budget_truncation"
        )
    if omitted == 0:
        lines.append("- （无省略内容）")
    return "\n".join(lines).rstrip() + "\n"


def _json_object(data: bytes, label: str) -> dict[str, object]:
    _validate_utf8_lf(data, label)
    try:
        value = json.loads(data.decode("utf-8"), parse_constant=_reject_json_constant)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid {label} JSON") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} JSON must contain an object")
    return value


def _json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _identifier(value: object, label: str) -> str:
    text = str(value).strip()
    if not text or any(character in text for character in "\\/\r\n") or text in {".", ".."}:
        raise ValueError(f"{label} must be one non-empty safe path component")
    return text


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def approximate_token_count(text: str) -> int:
    return math.ceil(len(text) / APPROX_TOKEN_CHARS)
