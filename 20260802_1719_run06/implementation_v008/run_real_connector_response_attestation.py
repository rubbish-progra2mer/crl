from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from joint_coverage_kernel import (
    Observation,
    Record,
    ScopeCell,
    SourceIdentity,
    canonical_request_payload,
    canonical_response_commitment,
)


@dataclass(frozen=True)
class ConnectorSpec:
    name: str
    url: str
    source: SourceIdentity
    cell: ScopeCell
    production_decoder: Callable[[bytes, ScopeCell], tuple[Record, ...]]
    audit_decoder: Callable[[bytes, ScopeCell], tuple[Record, ...]]
    next_cursor: Callable[[bytes, dict[str, str]], str | None]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fetch(url: str) -> tuple[bytes, dict[str, str], int]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "CRL-Run06-v008-response-attestation",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
        headers = {key.lower(): value for key, value in response.headers.items()}
        return raw, headers, response.status


def _gitlab_production(raw: bytes, cell: ScopeCell) -> tuple[Record, ...]:
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, list):
        raise ValueError("GitLab issues response must be a list")
    return tuple(
        Record(
            str(item["id"]),
            cell,
            bool(item.get("title")),
            isinstance(item.get("iid"), int),
        )
        for item in value
    )


def _gitlab_audit(raw: bytes, cell: ScopeCell) -> tuple[Record, ...]:
    value = json.loads(raw)
    records = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"GitLab row {index} is not an object")
        node_id = item.get("id")
        number = item.get("iid")
        title = item.get("title")
        if not isinstance(node_id, int):
            raise ValueError(f"GitLab row {index} has no stable integer id")
        records.append(
            Record(str(node_id), cell, isinstance(title, str) and bool(title), isinstance(number, int))
        )
    return tuple(records)


def _gitlab_next(_raw: bytes, headers: dict[str, str]) -> str | None:
    next_page = headers.get("x-next-page", "")
    if next_page:
        return next_page
    link = headers.get("link", "")
    for segment in link.split(","):
        if 'rel="next"' in segment:
            return segment.split(";", 1)[0].strip().strip("<>")
    return None


def _crossref_production(raw: bytes, cell: ScopeCell) -> tuple[Record, ...]:
    value = json.loads(raw.decode("utf-8"))
    items = value["message"]["items"]
    return tuple(
        Record(
            str(item["DOI"]),
            cell,
            bool(item.get("title")),
            isinstance(item.get("type"), str),
        )
        for item in items
    )


def _crossref_audit(raw: bytes, cell: ScopeCell) -> tuple[Record, ...]:
    value = json.loads(raw)
    message = value.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("items"), list):
        raise ValueError("Crossref response has no message.items list")
    records = []
    for index, item in enumerate(message["items"]):
        if not isinstance(item, dict):
            raise ValueError(f"Crossref row {index} is not an object")
        doi = item.get("DOI")
        title = item.get("title")
        kind = item.get("type")
        if not isinstance(doi, str) or not doi:
            raise ValueError(f"Crossref row {index} has no DOI")
        records.append(
            Record(
                doi,
                cell,
                isinstance(title, list) and bool(title) and bool(title[0]),
                isinstance(kind, str) and bool(kind),
            )
        )
    return tuple(records)


def _crossref_next(raw: bytes, _headers: dict[str, str]) -> str | None:
    value = json.loads(raw)
    cursor = value["message"].get("next-cursor")
    return cursor if isinstance(cursor, str) and cursor else None


def _specs() -> tuple[ConnectorSpec, ...]:
    common = {
        "authentication_subject": "public-anonymous-view",
        "scope_schema_version": "real-list-scope-v1",
        "adapter_version": "run06-audit-adapter-v1",
        "semantic_normalization_version": "url-parameter-normalization-v1",
        "request_serialization_version": "canonical-json-v1",
    }
    gitlab_source = SourceIdentity(
        "gitlab-rest",
        "GET /projects/gitlab-org%2Fgitlab/issues?state=opened&per_page=5&page=1",
        **common,
    )
    crossref_source = SourceIdentity(
        "crossref-rest",
        "GET /v1/works?query.title=large-language-model&rows=5&select=DOI,title,type",
        **common,
    )
    return (
        ConnectorSpec(
            "gitlab_issues",
            "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/issues?state=opened&per_page=5&page=1",
            gitlab_source,
            ScopeCell("gitlab-org-gitlab", "live-page-1", "open"),
            _gitlab_production,
            _gitlab_audit,
            _gitlab_next,
        ),
        ConnectorSpec(
            "crossref_works",
            "https://api.crossref.org/v1/works?query.title=large%20language%20model&rows=5&select=DOI,title,type",
            crossref_source,
            ScopeCell("works-title-query", "live-page-1", "public"),
            _crossref_production,
            _crossref_audit,
            _crossref_next,
        ),
    )


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    mutation_rows = []
    for spec in _specs():
        raw, headers, status_code = _fetch(spec.url)
        raw_path = args.output_dir / f"{spec.name}.json"
        raw_path.write_bytes(raw)
        production_records = spec.production_decoder(raw, spec.cell)
        audit_records = spec.audit_decoder(raw, spec.cell)
        if production_records != audit_records:
            raise ValueError(f"{spec.name} production/audit record projection differs")
        next_cursor = spec.next_cursor(raw, headers)
        request_payload = canonical_request_payload(
            spec.source, spec.cell, 0, _sha256(raw)
        )
        commitment = canonical_response_commitment(
            request_payload,
            audit_records,
            next_cursor,
            "ok",
            True,
            False,
        )
        observation = Observation(
            observation_id=f"real-{spec.name}",
            connector_id=spec.source.connector_id,
            cell=spec.cell,
            cursor=0,
            next_cursor=next_cursor,
            records=production_records,
            snapshot_id=_sha256(raw),
            query_signature=spec.source.query_signature,
            authentication_subject=spec.source.authentication_subject,
            scope_schema_version=spec.source.scope_schema_version,
            adapter_version=spec.source.adapter_version,
            semantic_normalization_version=spec.source.semantic_normalization_version,
            request_serialization_version=spec.source.request_serialization_version,
            request_payload=request_payload,
            response_commitment=commitment,
        )
        rows.append(
            {
                "connector": spec.name,
                "official_endpoint": spec.url,
                "http_status": status_code,
                "raw_path": raw_path.name,
                "raw_sha256": _sha256(raw),
                "raw_size_bytes": len(raw),
                "production_record_count": len(production_records),
                "audit_record_count": len(audit_records),
                "record_sequence_equal": production_records == audit_records,
                "next_cursor_present": next_cursor is not None,
                "response_commitment": commitment,
                "observation_recomputation_matches": (
                    observation.expected_response_commitment == commitment
                ),
            }
        )

        variants = {
            "omit_first_record": production_records[1:],
            "inject_record": production_records
            + (Record("injected", spec.cell, True, True),),
        }
        for mutation, records in variants.items():
            mutation_rows.append(
                {
                    "connector": spec.name,
                    "mutation": mutation,
                    "commitment_matches": canonical_response_commitment(
                        request_payload,
                        records,
                        next_cursor,
                        "ok",
                        True,
                        False,
                    )
                    == commitment,
                }
            )
        mutation_rows.extend(
            (
                {
                    "connector": spec.name,
                    "mutation": "change_termination",
                    "commitment_matches": canonical_response_commitment(
                        request_payload,
                        production_records,
                        None if next_cursor is not None else "forged-next",
                        "ok",
                        True,
                        False,
                    )
                    == commitment,
                },
                {
                    "connector": spec.name,
                    "mutation": "change_permission",
                    "commitment_matches": canonical_response_commitment(
                        request_payload,
                        production_records,
                        next_cursor,
                        "ok",
                        False,
                        False,
                    )
                    == commitment,
                },
            )
        )

    result = {
        "experiment": "real_connector_raw_response_commitment_v008",
        "schema_version": 1,
        "connector_count": len(rows),
        "all_http_200": all(row["http_status"] == 200 for row in rows),
        "all_record_sequences_equal": all(row["record_sequence_equal"] for row in rows),
        "all_commitments_recompute": all(
            row["observation_recomputation_matches"] for row in rows
        ),
        "mutation_count": len(mutation_rows),
        "mutations_detected": sum(
            not row["commitment_matches"] for row in mutation_rows
        ),
        "trust_boundary": (
            "one TLS fetch per public endpoint; raw bytes retained; production and audit "
            "projections are separate functions in one process, not independent transport "
            "capture, a cryptographic log, or a proof of provider metadata truth"
        ),
        "rows": rows,
        "mutation_rows": mutation_rows,
    }
    output = args.output_dir / "results.json"
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not all(
        (
            result["all_http_200"],
            result["all_record_sequences_equal"],
            result["all_commitments_recompute"],
            result["mutations_detected"] == result["mutation_count"],
        )
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
