from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import TYPE_CHECKING, Iterable
from uuid import uuid4

if TYPE_CHECKING:
    from crl_v3.decision import DecisionDocument, TerminalDocument
    from crl_v3.experiment import ExperimentArtifact, ExperimentPlanDocument, ExperimentResultDocument
    from crl_v3.hypotheses import HypothesisPortfolio, HypothesisPortfolioDocument
    from crl_v3.knowledge import KnowledgeStore
    from crl_v3.review import ReviewRequestDocument, ReviewerReportDocument


RUN_PATTERN = re.compile(r"^\d{8}_\d{4}_run\d{2,}$")
_VERSION_PATTERN = re.compile(r"^v\d{3,}$")
_CONTROL_FILES = ("RUN_CHARTER.md", "RUN_STATUS.md", "RUN_LEDGER.md")
CURRENT_CONTRACT_VERSION = "3"
SUPPORTED_CONTRACT_VERSIONS = frozenset({"2", "3"})
ALLOWED_STATUSES = {
    "ACTIVE",
    "PAUSED_BY_USER",
    "TERMINATED_BY_USER",
    "CONCLUDED_NO_DELIVERY",
    "DELIVERED",
}
RESUMABLE_STATUSES = {"ACTIVE", "PAUSED_BY_USER"}
PERMANENT_TERMINAL_FILE_STATUS = {
    "TERMINATED_BY_USER.md": "TERMINATED_BY_USER",
}
_DOCUMENT_STEMS = {
    "problem",
    "research_map",
    "nearest_prior",
    "candidate",
    "evidence_packet",
    "selection_context",
    "memory",
    "failure_attribution",
    "seed",
}


@dataclass(frozen=True, slots=True)
class WorkspaceDocument:
    path: str
    content: str
    sha256: str


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    evidence_id: str
    fulltext_is_current: bool
    passage_is_current: bool | None


@dataclass(frozen=True, slots=True)
class ResearchMapDocument:
    path: str
    content: str
    evidence: tuple[EvidenceReference, ...]
    sha256: str


@dataclass(frozen=True, slots=True)
class CandidateDocument:
    path: str
    content: str
    evidence: tuple[EvidenceReference, ...]
    sha256: str


@dataclass(frozen=True, slots=True)
class EvidencePacketDocument:
    path: str
    content: str
    evidence: tuple[EvidenceReference, ...]
    sha256: str


class ResearchWorkspace:
    """File manager bound to one valid direct-child CRL Run and one version."""

    def __init__(
        self,
        workspace_path: str | Path,
        knowledge_store: KnowledgeStore | None = None,
        *,
        version: str = "v001",
        product_root: str | Path | None = None,
    ) -> None:
        product = product_root if product_root is not None else Path(__file__).resolve().parents[2]
        root = bind_run(product, workspace_path)
        run_contract = require_supported_contract(root)
        if not _VERSION_PATTERN.fullmatch(version):
            raise ValueError(f"invalid research version: {version!r}")
        self.product_root = Path(product).resolve()
        self.workspace_path = root
        self.knowledge_store = knowledge_store
        self.version = version
        self.contract_version = run_contract

    @property
    def historical_read_only(self) -> bool:
        return self.contract_version != CURRENT_CONTRACT_VERSION

    @property
    def review_path(self) -> Path:
        return self.workspace_path / f"review_{self.version}"

    @property
    def experiment_path(self) -> Path:
        return self.workspace_path / f"experiment_{self.version}"

    @property
    def implementation_path(self) -> Path:
        return self.workspace_path / f"implementation_{self.version}"

    @property
    def workbench_path(self) -> Path:
        return self.workspace_path / f"workbench_{self.version}"

    @property
    def hypotheses_path(self) -> Path:
        return self.workspace_path / f"hypotheses_{self.version}" / "portfolio.json"

    @property
    def seed_path(self) -> Path:
        return self.workspace_path / f"seed_{self.version}.md"

    def document_path(self, stem: str) -> Path:
        if stem not in _DOCUMENT_STEMS and stem != "decision":
            raise ValueError(f"unsupported Run document stem: {stem!r}")
        return self.workspace_path / f"{stem}_{self.version}.md"

    def write_document(self, stem: str, content: str) -> WorkspaceDocument:
        if stem == "decision":
            raise ValueError("write decisions through write_review_decision()")
        path = self.document_path(stem)
        self._assert_narrative_mutable(path)
        data = _atomic_write_text(path, content, within=self.workspace_path)
        return WorkspaceDocument(str(path), data.decode("utf-8"), _sha256(data))

    def read_document(self, stem: str) -> WorkspaceDocument:
        path = self.document_path(stem)
        data = _required_file(path, within=self.workspace_path)
        return WorkspaceDocument(str(path), data.decode("utf-8"), _sha256(data))

    def write_problem(self, content: str) -> WorkspaceDocument:
        return self.write_document("problem", content)

    def read_problem(self) -> WorkspaceDocument:
        return self.read_document("problem")

    def write_research_map(
        self, content: str, evidence_ids: Iterable[str] = ()
    ) -> ResearchMapDocument:
        references = self._resolve_evidence(evidence_ids)
        body = _render_cited_document(content, tuple(item.evidence_id for item in references))
        written = self.write_document("research_map", body)
        return ResearchMapDocument(written.path, written.content, references, written.sha256)

    def read_research_map(self) -> ResearchMapDocument:
        document = self.read_document("research_map")
        content, evidence_ids = _parse_cited_document(document.content)
        references = self._resolve_evidence(evidence_ids)
        return ResearchMapDocument(document.path, content, references, document.sha256)

    def write_nearest_prior(self, content: str) -> WorkspaceDocument:
        return self.write_document("nearest_prior", content)

    def read_nearest_prior(self) -> WorkspaceDocument:
        return self.read_document("nearest_prior")

    def write_candidate(
        self, content: str, evidence_ids: Iterable[str] = ()
    ) -> CandidateDocument:
        references = self._resolve_evidence(evidence_ids)
        body = _render_cited_document(content, tuple(item.evidence_id for item in references))
        written = self.write_document("candidate", body)
        return CandidateDocument(written.path, written.content, references, written.sha256)

    def read_candidate(self) -> CandidateDocument:
        document = self.read_document("candidate")
        content, evidence_ids = _parse_cited_document(document.content)
        references = self._resolve_evidence(evidence_ids)
        return CandidateDocument(document.path, content, references, document.sha256)

    def write_evidence_packet(
        self, evidence_ids: Iterable[str], *, preface: str = ""
    ) -> EvidencePacketDocument:
        references = self._resolve_evidence(evidence_ids)
        lines = ["# Evidence Summary", ""]
        if preface.strip():
            lines.extend([preface.strip(), ""])
        for reference in references:
            assert self.knowledge_store is not None
            evidence = self.knowledge_store.get_evidence(reference.evidence_id)
            assert evidence is not None
            lines.extend(
                [
                    f"## {evidence.evidence_id}",
                    "",
                    f"- Paper: {evidence.paper_id}",
                    f"- Locator: {evidence.locator}",
                    f"- Section/pages: {evidence.section}, {evidence.page_start}-{evidence.page_end}",
                    f"- Fulltext SHA-256: {evidence.fulltext_sha256}",
                    f"- Current fulltext: {str(evidence.fulltext_is_current).lower()}",
                    "",
                    evidence.source_content,
                    "",
                    f"Codex note: {evidence.codex_note}",
                    "",
                ]
            )
        written = self.write_document("evidence_packet", "\n".join(lines).rstrip() + "\n")
        return EvidencePacketDocument(written.path, written.content, references, written.sha256)

    def read_evidence_packet(self) -> EvidencePacketDocument:
        document = self.read_document("evidence_packet")
        ids = tuple(re.findall(r"^## (\S+)\s*$", document.content, flags=re.MULTILINE))
        references = self._resolve_evidence(ids)
        return EvidencePacketDocument(document.path, document.content, references, document.sha256)

    def write_selection_context(self, content: str) -> WorkspaceDocument:
        return self.write_document("selection_context", content)

    def write_memory(self, content: str) -> WorkspaceDocument:
        return self.write_document("memory", content)

    def write_failure_attribution(self, content: str) -> WorkspaceDocument:
        return self.write_document("failure_attribution", content)

    def write_seed(self, content: str) -> WorkspaceDocument:
        return self.write_document("seed", content)

    def read_seed(self) -> WorkspaceDocument:
        return self.read_document("seed")

    def read_hypotheses(
        self, *, required: bool = True
    ) -> HypothesisPortfolioDocument | None:
        from crl_v3.hypotheses import read_portfolio

        return read_portfolio(self, required=required)

    def write_hypotheses(
        self,
        portfolio: HypothesisPortfolio,
        *,
        expected_sha256: str | None,
        create_only: bool = False,
    ) -> HypothesisPortfolioDocument:
        from crl_v3.hypotheses import write_portfolio

        return write_portfolio(
            self,
            portfolio,
            expected_sha256=expected_sha256,
            create_only=create_only,
        )

    def write_experiment_plan(self, content: str) -> ExperimentPlanDocument:
        from crl_v3.experiment import write_experiment_plan

        return write_experiment_plan(self, content)

    def save_experiment_artifact(
        self,
        source: str | Path,
        relative_path: str,
        *,
        area: str = "experiment",
        replace: bool = False,
    ) -> ExperimentArtifact:
        from crl_v3.experiment import save_experiment_artifact

        return save_experiment_artifact(
            self, source, relative_path, area=area, replace=replace
        )

    def write_experiment_result(self, content: str) -> ExperimentResultDocument:
        from crl_v3.experiment import write_experiment_result

        return write_experiment_result(self, content)

    def write_review_request(
        self, content: str, reading_paths: Iterable[str | Path]
    ) -> ReviewRequestDocument:
        from crl_v3.review import write_review_request

        return write_review_request(self, content, reading_paths)

    def write_reviewer_report(
        self,
        reviewer_number: int,
        reviewer_id: str,
        content: str,
    ) -> ReviewerReportDocument:
        from crl_v3.review import write_reviewer_report

        return write_reviewer_report(self, reviewer_number, reviewer_id, content)

    def list_reviewer_reports(self) -> tuple[ReviewerReportDocument, ...]:
        from crl_v3.review import list_reviewer_reports

        return list_reviewer_reports(self)

    def write_review_decision(
        self, content: str, *, measurement_key: str | None = None
    ) -> DecisionDocument:
        from crl_v3.decision import write_review_decision

        return write_review_decision(
            self, content, measurement_key=measurement_key
        )

    def write_delivery(
        self, *, supporting_attempt_ids: Iterable[str]
    ) -> TerminalDocument:
        from crl_v3.decision import write_delivery

        return write_delivery(self, supporting_attempt_ids=supporting_attempt_ids)

    def write_no_delivery(self, content: str) -> TerminalDocument:
        from crl_v3.decision import write_no_delivery

        return write_no_delivery(self, content)

    def _resolve_evidence(self, evidence_ids: Iterable[str]) -> tuple[EvidenceReference, ...]:
        ids = tuple(dict.fromkeys(str(item).strip() for item in evidence_ids if str(item).strip()))
        if not ids:
            return ()
        if self.knowledge_store is None:
            raise ValueError("a KnowledgeStore is required when evidence ids are supplied")
        references: list[EvidenceReference] = []
        for evidence_id in ids:
            evidence = self.knowledge_store.get_evidence(evidence_id)
            if evidence is None:
                raise KeyError(f"unknown evidence id: {evidence_id}")
            references.append(
                EvidenceReference(
                    evidence_id=evidence_id,
                    fulltext_is_current=evidence.fulltext_is_current,
                    passage_is_current=evidence.passage_is_current,
                )
            )
        return tuple(references)

    def _assert_narrative_mutable(self, path: Path) -> None:
        self.assert_run_writable()
        target = self.assert_write_target(path)
        request_path = self.review_path / "request.md"
        if not request_path.is_file():
            return
        from crl_v3.review import read_review_request

        request = read_review_request(self)
        relative = target.relative_to(self.workspace_path).as_posix()
        relative_key = os.path.normcase(relative)
        locked_keys = {os.path.normcase(item) for item in request.reading_paths}
        if relative_key in locked_keys:
            raise FileExistsError(
                f"reviewed material for {self.version} is locked; create a new version: {path}"
            )

    def assert_run_writable(self) -> None:
        require_current_contract(self.workspace_path)
        for terminal in PERMANENT_TERMINAL_FILE_STATUS:
            if (self.workspace_path / terminal).is_file():
                raise FileExistsError(
                    f"terminal Run is immutable because {terminal} exists"
                )
        status = _status_value(self.workspace_path / "RUN_STATUS.md")
        if status == "DELIVERED":
            raise FileExistsError(
                "delivered Run is read-only until explicitly resumed into a new version"
            )
        if status == "CONCLUDED_NO_DELIVERY":
            raise FileExistsError(
                "no-delivery Run is read-only until explicitly resumed into a new version"
            )
        if status == "TERMINATED_BY_USER":
            raise FileExistsError(f"terminal Run status is immutable: {status}")
        if status == "PAUSED_BY_USER":
            raise PermissionError("paused Run is read-only until explicitly resumed")
        current_version = _current_version(self.workspace_path / "RUN_STATUS.md")
        if self.version != current_version:
            raise ValueError(
                f"writes require CURRENT_VERSION {current_version}, not {self.version}; "
                "advance the Run version explicitly"
            )

    def assert_write_target(self, path: str | Path) -> Path:
        """Return one lexical Run-local target after rejecting reparse-point ancestors."""

        target = Path(path)
        if not target.is_absolute():
            target = self.workspace_path / target
        target = Path(os.path.abspath(target))
        try:
            relative = target.relative_to(self.workspace_path)
        except ValueError as error:
            raise ValueError(f"write target escapes Run root: {target}") from error
        current = self.workspace_path
        for part in relative.parts:
            current = current / part
            if _path_entry_exists(current) and _is_reparse_point(current):
                raise ValueError(f"write target uses a reparse point: {current}")
        resolved_parent = target.parent.resolve()
        try:
            resolved_parent.relative_to(self.workspace_path)
        except ValueError as error:
            raise ValueError(f"write target resolves outside Run root: {target}") from error
        return target

    def assert_read_target(self, path: str | Path) -> Path:
        """Return one existing regular Run file after rejecting every reparse point."""

        return _assert_read_target(Path(path), self.workspace_path)

    def assert_formal_input(self, path: str | Path) -> Path:
        """Bind one Formal input while excluding files owned by sibling CRL Runs."""

        target = Path(path)
        if not target.is_absolute():
            target = self.workspace_path / target
        lexical = Path(os.path.abspath(target))
        try:
            lexical.relative_to(self.workspace_path)
        except ValueError:
            pass
        else:
            return self.assert_read_target(lexical)

        resolved = lexical.resolve(strict=True)
        if not resolved.is_file():
            raise FileNotFoundError(f"formal input is not a regular file: {lexical}")
        try:
            relative = resolved.relative_to(self.product_root)
        except ValueError:
            return resolved
        if len(relative.parts) < 2:
            return resolved
        candidate = self.product_root / relative.parts[0]
        if candidate == self.workspace_path:
            return self.assert_read_target(resolved)
        if RUN_PATTERN.fullmatch(candidate.name) is None:
            return resolved
        try:
            sibling = bind_run(self.product_root, candidate)
        except (FileNotFoundError, OSError, UnicodeError, ValueError):
            return resolved
        raise ValueError(
            "formal input belongs to another CRL Run "
            f"{sibling.name}: {resolved}"
        )


def bind_run(product_root: str | Path, requested: str | Path) -> Path:
    """Bind one real, non-reparse, direct-child CRL Run before reading it."""

    product = Path(product_root).resolve(strict=True)
    if not product.is_dir():
        raise FileNotFoundError(f"product root is not an existing directory: {product}")
    candidate = Path(requested)
    if not candidate.is_absolute():
        candidate = product / candidate
    lexical = Path(os.path.abspath(candidate))
    if lexical.parent != product or RUN_PATTERN.fullmatch(lexical.name) is None:
        raise ValueError(f"Run must be a valid direct child of product root: {lexical}")
    if not _path_entry_exists(lexical):
        raise FileNotFoundError(f"Run root is not an existing directory: {lexical}")
    if _is_reparse_point(lexical):
        raise ValueError(f"Run root must not be a reparse point: {lexical}")
    if not lexical.is_dir():
        raise FileNotFoundError(f"Run root is not an existing directory: {lexical}")
    root = lexical.resolve(strict=True)
    if root.parent != product or root != lexical:
        raise ValueError(f"Run resolves outside its lexical direct-child path: {lexical}")
    for name in _CONTROL_FILES:
        _read_utf8_text(
            root / name,
            f"Run control file {name}",
            within=root,
        )
    run_id = _single_control_field(
        root / "RUN_STATUS.md", "RUN_ID", within=root
    )
    if run_id != root.name:
        raise ValueError(
            f"RUN_STATUS.md RUN_ID does not match Run directory: {run_id!r}"
        )
    charter_run_id = _single_named_field(
        root / "RUN_CHARTER.md",
        "RUN_ID",
        label="RUN_CHARTER.md",
        within=root,
    )
    if charter_run_id != root.name:
        raise ValueError(
            "RUN_CHARTER.md RUN_ID does not match Run directory: "
            f"{charter_run_id!r}"
        )
    status = _status_value(root / "RUN_STATUS.md", within=root)
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"RUN_STATUS.md contains invalid STATUS: {status!r}")
    _current_version(root / "RUN_STATUS.md", within=root)
    return root


def contract_version(run_root: str | Path) -> str | None:
    root = Path(run_root)
    path = root / "RUN_CHARTER.md"
    content = _read_utf8_text(path, "RUN_CHARTER.md", within=root)
    values = [
        line.partition(":")[2].strip()
        for line in content.splitlines()
        if line.startswith("CRL_CONTRACT_VERSION:")
    ]
    if not values:
        return None
    if len(values) != 1 or not values[0]:
        raise ValueError(f"RUN_CHARTER.md has invalid CRL_CONTRACT_VERSION: {path}")
    return values[0]


def require_current_contract(run_root: str | Path) -> None:
    version = contract_version(run_root)
    if version != CURRENT_CONTRACT_VERSION:
        label = "legacy" if version is None else version
        raise ValueError(
            "Run is read-only under the current CRL contract: "
            f"{Path(run_root).name} (contract {label})"
        )


def require_supported_contract(run_root: str | Path) -> str:
    version = contract_version(run_root)
    if version not in SUPPORTED_CONTRACT_VERSIONS:
        label = "legacy" if version is None else version
        raise ValueError(
            "Run contract is not supported by the current CRL reader: "
            f"{Path(run_root).name} (contract {label})"
        )
    return version


def safe_relative_path(value: str | Path) -> Path:
    text = str(value)
    path = Path(text)
    windows = PureWindowsPath(text)
    if (
        path.is_absolute()
        or windows.is_absolute()
        or windows.drive
        or windows.root
        or not path.parts
        or ".." in path.parts
    ):
        raise ValueError(f"path must be a safe relative path: {value!r}")
    if any(part in {"", "."} for part in path.parts):
        raise ValueError(f"path contains an empty or current-directory component: {value!r}")
    return path


def _render_cited_document(content: str, evidence_ids: tuple[str, ...]) -> str:
    body = _required_content(content).rstrip()
    if not evidence_ids:
        return body + "\n"
    return "\n".join(
        [body, "", "<!-- CRL_EVIDENCE_IDS", *evidence_ids, "CRL_EVIDENCE_IDS -->", ""]
    )


def _parse_cited_document(document: str) -> tuple[str, tuple[str, ...]]:
    marker = "<!-- CRL_EVIDENCE_IDS\n"
    if marker not in document:
        return document, ()
    body, tail = document.split(marker, 1)
    ids_text, ending = tail.split("\nCRL_EVIDENCE_IDS -->", 1)
    if ending.strip():
        raise ValueError("unexpected content after CRL evidence metadata")
    ids = tuple(line.strip() for line in ids_text.splitlines() if line.strip())
    return body.rstrip() + "\n", ids


def _normalize_text(content: str) -> str:
    if not isinstance(content, str):
        raise ValueError("document content must be text")
    if content.startswith("\ufeff"):
        raise ValueError("document content must not begin with a UTF-8 BOM marker")
    return content.replace("\r\n", "\n").replace("\r", "\n")


def _required_content(content: str) -> str:
    normalized = _normalize_text(content)
    if not normalized.strip():
        raise ValueError("document content must be non-empty text")
    return normalized if normalized.endswith("\n") else normalized + "\n"


def _required_file(path: Path, *, within: Path | None = None) -> bytes:
    target = _assert_read_target(path, within) if within is not None else path
    if not target.is_file():
        raise FileNotFoundError(target)
    data = target.read_bytes()
    _validate_utf8_lf(data, str(path))
    return data


def _read_utf8_text(
    path: Path, label: str, *, within: Path | None = None
) -> str:
    target = _assert_read_target(path, within) if within is not None else path
    if not target.is_file():
        raise FileNotFoundError(f"missing {label}: {target}")
    data = target.read_bytes()
    _validate_utf8_lf(data, label)
    if not data:
        raise ValueError(f"empty {label}: {path}")
    return data.decode("utf-8")


def _validate_utf8_lf(data: bytes, label: str) -> None:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{label} must be UTF-8 without BOM")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{label} must be valid UTF-8") from error
    if b"\r" in data:
        raise ValueError(f"{label} must use LF newlines")


def _atomic_write_text(
    path: Path, content: str, *, within: Path | None = None
) -> bytes:
    data = _required_content(content).encode("utf-8")
    if within is not None:
        _assert_write_target(path, within)
    path.parent.mkdir(parents=True, exist_ok=True)
    if within is not None:
        _assert_write_target(path, within)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return data


def _publish_once(path: Path, data: bytes, *, within: Path | None = None) -> None:
    _validate_utf8_lf(data, str(path))
    if within is not None:
        _assert_write_target(path, within)
    path.parent.mkdir(parents=True, exist_ok=True)
    if within is not None:
        _assert_write_target(path, within)
    try:
        with path.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        if path.is_file() and path.read_bytes() == data:
            return
        raise


def _status_value(path: Path, *, within: Path | None = None) -> str | None:
    return _single_control_field(path, "STATUS", within=within or path.parent)


def _current_version(path: Path, *, within: Path | None = None) -> str:
    value = _single_control_field(
        path, "CURRENT_VERSION", within=within or path.parent
    )
    if not _VERSION_PATTERN.fullmatch(value):
        raise ValueError(f"RUN_STATUS.md contains invalid CURRENT_VERSION: {value!r}")
    return value


def _single_control_field(
    path: Path, name: str, *, within: Path | None = None
) -> str:
    return _single_named_field(
        path, name, label="RUN_STATUS.md", within=within or path.parent
    )


def _single_named_field(
    path: Path,
    name: str,
    *,
    label: str,
    within: Path | None = None,
) -> str:
    content = _read_utf8_text(path, label, within=within)
    values = [
        line.partition(":")[2].strip()
        for line in content.splitlines()
        if line.startswith(f"{name}:")
    ]
    if len(values) != 1 or not values[0]:
        raise ValueError(f"{label} must contain exactly one {name}: {path}")
    return values[0]


def _assert_write_target(path: Path, run_root: Path) -> None:
    root = run_root.resolve()
    target = Path(os.path.abspath(path))
    try:
        relative = target.relative_to(root)
    except ValueError as error:
        raise ValueError(f"write target escapes Run root: {target}") from error
    current = root
    for part in relative.parts:
        current = current / part
        if _path_entry_exists(current) and _is_reparse_point(current):
            raise ValueError(f"write target uses a reparse point: {current}")
    try:
        target.parent.resolve().relative_to(root)
    except ValueError as error:
        raise ValueError(f"write target resolves outside Run root: {target}") from error


def _assert_read_target(path: Path, run_root: Path) -> Path:
    """Bind one existing regular file to a real Run without following reparses."""

    lexical_root = Path(os.path.abspath(run_root))
    if not _path_entry_exists(lexical_root) or not lexical_root.is_dir():
        raise FileNotFoundError(f"Run root is not an existing directory: {lexical_root}")
    if _is_reparse_point(lexical_root):
        raise ValueError(f"Run root must not be a reparse point: {lexical_root}")
    root = lexical_root.resolve(strict=True)
    target = path if path.is_absolute() else root / path
    target = Path(os.path.abspath(target))
    try:
        relative = target.relative_to(root)
    except ValueError as error:
        raise ValueError(f"read target escapes Run root: {target}") from error
    current = root
    for part in relative.parts:
        current = current / part
        if _path_entry_exists(current) and _is_reparse_point(current):
            raise ValueError(f"read target uses a reparse point: {current}")
    if not _path_entry_exists(target):
        raise FileNotFoundError(target)
    resolved = target.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ValueError(f"read target resolves outside Run root: {target}") from error
    if not resolved.is_file():
        raise FileNotFoundError(f"read target is not a regular file: {target}")
    return target


def _path_entry_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _is_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = os.lstat(path).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
