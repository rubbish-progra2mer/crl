"""Build a variable-level index from the official HRS codebook directory.

The directory mixes modern framed HTML codebooks, legacy standalone HTML
codebooks, and plain-text codebooks.  The crawler preserves the directory
section and study/topic provenance for every extracted variable.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CODEBOOK_DIRECTORY_URL = "https://hrs.isr.umich.edu/documentation/codebooks"
CODEBOOK_ENDPOINTS = {
    "biennial": "https://hrsdata.isr.umich.edu/json/documentation/codebook/biennial",
    "off_year": "https://hrsdata.isr.umich.edu/json/documentation/codebook/off-year",
    "health": "https://hrsdata.isr.umich.edu/json/documentation/codebook/health",
    "xwave": "https://hrsdata.isr.umich.edu/json/documentation/codebook/xwave",
}
BIENNIAL_ENDPOINT = CODEBOOK_ENDPOINTS["biennial"]
USER_AGENT = "OADD-Bench/1.0 (+https://hrs.isr.umich.edu/documentation/codebooks)"
DEFAULT_RAW_DIR = PROJECT_ROOT / "benchmark" / "HRS_metadata" / "raw_codebooks"
DEFAULT_RAW_MANIFEST = PROJECT_ROOT / "benchmark" / "HRS_metadata" / "raw_manifest.json"
DEFAULT_INDEX_PATH = PROJECT_ROOT / "benchmark" / "HRS_metadata" / "metadata.jsonl"

DEFAULT_PRODUCTS = ["all_documentation_page"]


def clean_text(value: str) -> str:
    lines = [" ".join(line.split()) for line in value.splitlines()]
    return "\n".join(line for line in lines if line)


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_") or "untitled"


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def extract_first_link(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find("a", href=True)
    if link is None:
        return "", ""
    return urljoin(CODEBOOK_DIRECTORY_URL, link["href"]), clean_text(link.get_text(" "))


def product_key_from_row(directory_section: str, group: str, title: str) -> str:
    if "tracker" in title.lower():
        if title.lower().strip() == "cross-wave tracker file":
            return "tracker"
    if (
        directory_section == "biennial"
        and group.isdigit()
        and re.fullmatch(rf"{group} HRS Core", title.strip(), flags=re.IGNORECASE)
    ):
        return f"{group}_core"
    return slugify(title)


def infer_year(group: str, title: str) -> str:
    if group.isdigit():
        return group
    years = re.findall(r"\b(?:19|20)\d{2}\b", title)
    return "-".join(dict.fromkeys(years))


def product_family_from_title(title: str, directory_section: str = "biennial", group: str = "") -> str:
    lower = title.lower()
    if "post-exit" in lower or "post exit" in lower:
        return "post_exit"
    if "tracker" in lower:
        return "tracker"
    if "core" in lower and "module" not in lower:
        return "core"
    if "exit" in lower:
        return "exit"
    if directory_section != "biennial":
        return slugify(group)
    return "other_biennial"


def list_directory_products(session: requests.Session, directory_section: str) -> list[dict]:
    endpoint = CODEBOOK_ENDPOINTS[directory_section]
    response = session.get(endpoint, timeout=30)
    response.raise_for_status()
    rows = response.json()

    products: list[dict] = []
    for row in rows:
        product_url, product_title = extract_first_link(row.get("codebooks", ""))
        if not product_url or not product_title:
            continue

        group_field = {
            "biennial": "year",
            "off_year": "study",
            "health": "study",
            "xwave": "topic",
        }[directory_section]
        group = str(row.get(group_field, "")).strip()
        product_key = product_key_from_row(directory_section, group, product_title)
        products.append(
            {
                "target_key": product_key,
                "year": infer_year(group, product_title),
                "product_title": product_title,
                "product_url": product_url,
                "product_family": product_family_from_title(
                    product_title, directory_section, group
                ),
                "documentation_section": directory_section,
                "documentation_group": group,
                "documentation_endpoint": endpoint,
            }
        )

    return products


def list_all_products(session: requests.Session) -> list[dict]:
    products: list[dict] = []
    for directory_section in CODEBOOK_ENDPOINTS:
        products.extend(list_directory_products(session, directory_section))
    return products


def list_biennial_products(session: requests.Session) -> list[dict]:
    """Backward-compatible wrapper used by older callers."""
    return list_directory_products(session, "biennial")


def expand_product_targets(targets: list[str], all_products: list[dict]) -> list[str]:
    expanded: list[str] = []
    for target in targets:
        if target == "recent_core_tracker":
            expanded.extend(["2012_core", "2014_core", "2016_core", "2018_core", "2020_core", "2022_core", "tracker"])
        elif target == "all_core_tracker":
            expanded.extend(
                product["target_key"]
                for product in all_products
                if product["target_key"].endswith("_core") or product["target_key"] == "tracker"
            )
        elif target == "all_core":
            expanded.extend(
                product["target_key"]
                for product in all_products
                if product["target_key"].endswith("_core")
            )
        elif target == "all_documentation_page":
            expanded.extend(product["target_key"] for product in all_products)
        elif target in {"all_biennial", "all_off_year", "all_health", "all_xwave"}:
            section = target.removeprefix("all_")
            expanded.extend(
                product["target_key"]
                for product in all_products
                if product["documentation_section"] == section
            )
        else:
            expanded.append(target)

    seen: set[str] = set()
    deduped: list[str] = []
    for target in expanded:
        if target in seen:
            continue
        seen.add(target)
        deduped.append(target)
    return deduped


def get_selected_products(session: requests.Session, target_keys: list[str]) -> list[dict]:
    all_products = list_all_products(session)
    product_by_key: dict[str, dict] = {}
    duplicate_keys: set[str] = set()
    for product in all_products:
        key = product["target_key"]
        if key in product_by_key:
            duplicate_keys.add(key)
        product_by_key[key] = product
    if duplicate_keys:
        raise RuntimeError(f"Non-unique product keys: {sorted(duplicate_keys)}")
    expanded_targets = expand_product_targets(target_keys, all_products)

    selected: list[dict] = []
    for target_key in expanded_targets:
        if target_key not in product_by_key:
            raise RuntimeError(f"Could not find codebook product key: {target_key}")
        selected.append(product_by_key[target_key])

    return selected


def fetch_text(session: requests.Session, url: str) -> str:
    response = session.get(url, timeout=60)
    response.raise_for_status()
    if response.encoding in {None, "ISO-8859-1"}:
        response.encoding = response.apparent_encoding
    return response.text


def raw_snapshot_path(raw_dir: Path, product_key: str, url: str) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    url_digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    basename = slugify(f"{product_key}_{Path(urlparse(url).path).name}_{url_digest}")
    return raw_dir / f"{basename}.html"


def save_raw_html(raw_dir: Path, product_key: str, url: str, html: str) -> Path:
    path = raw_snapshot_path(raw_dir, product_key, url)
    path.write_text(html, encoding="utf-8")
    return path


def load_or_fetch(
    session: requests.Session,
    raw_dir: Path,
    product_key: str,
    url: str,
    *,
    refresh: bool,
) -> str:
    snapshot = raw_snapshot_path(raw_dir, product_key, url)
    if snapshot.exists() and not refresh:
        return snapshot.read_text(encoding="utf-8")
    content = fetch_text(session, url)
    save_raw_html(raw_dir, product_key, url, content)
    return content


def get_section_frame_urls(index_url: str, index_html: str) -> list[str]:
    soup = BeautifulSoup(index_html, "html.parser")
    urls: list[str] = []
    seen: set[str] = set()

    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        # ``_ri`` is the standard record-layout frame. A few older products
        # use ``_ti``, ``_ji``, ``_ki``, or ``_li``. Do not accept hierarchy
        # (``_hi``), summary (``_si``), universe (``_ui``), or merge-control
        # (``_mci``) frames: those are navigation aids rather than codebooks.
        if not re.search(r"_[rtjkl]i\.html?$", href, flags=re.IGNORECASE):
            continue
        url = urljoin(index_url, href)
        if url not in seen:
            seen.add(url)
            urls.append(url)

    return urls


def get_legacy_section_urls(index_url: str, index_html: str) -> list[str]:
    """Return direct section pages used by the 1992–1994 codebooks."""
    soup = BeautifulSoup(index_html, "html.parser")
    index_path = urlparse(index_url).path
    index_dir = index_path.rsplit("/", 1)[0] + "/"
    urls: list[str] = []
    seen: set[str] = set()

    for link in soup.find_all("a", href=True):
        url = urljoin(index_url, link["href"].strip()).split("#", 1)[0]
        parsed = urlparse(url)
        basename = Path(parsed.path).name
        if parsed.netloc != urlparse(index_url).netloc or parsed.path == index_path:
            continue
        if not parsed.path.startswith(index_dir) or not re.search(r"\.html?$", basename, re.I):
            continue
        is_numbered_section = re.match(r"^\d+_", basename) is not None
        is_ahead_section = basename.lower().startswith("codb-")
        if not (is_numbered_section or is_ahead_section):
            continue
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def get_full_section_url(frame_url: str, frame_html: str) -> str:
    soup = BeautifulSoup(frame_html, "html.parser")

    for frame in soup.find_all(["frame", "iframe"], src=True):
        src = frame["src"].strip()
        if re.search(r"_[rtjkl]\.html?$", src, flags=re.IGNORECASE):
            return urljoin(frame_url, src)

    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        if re.search(r"_[rtjkl]\.html?$", href, flags=re.IGNORECASE):
            return urljoin(frame_url, href)

    raise RuntimeError(f"Could not find full section URL for {frame_url}")


def section_title_from_text(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.upper().startswith("SECTION "):
            return line
    return ""


def parse_metadata_line(line: str) -> dict:
    metadata: dict[str, str] = {}
    for key in ["Section", "File", "Level", "Type", "Width", "Decimals", "Ref"]:
        match = re.search(rf"{key}:\s*(.*?)(?=\s+[A-Z][A-Za-z]+:|$)", line)
        if match:
            metadata[key.lower()] = match.group(1).strip()
    return metadata


def split_variable_block(block: str) -> dict | None:
    lines = [line.rstrip() for line in block.splitlines() if line.strip()]
    if not lines:
        return None

    metadata_hints = [
        index
        for index, line in enumerate(lines)
        if "Type:" in line or "Section:" in line or "File:" in line
    ]
    search_end = min(metadata_hints) if metadata_hints else len(lines)
    candidates: list[tuple[int, str, str, bool]] = []
    for index, line in enumerate(lines[:search_end]):
        standalone_match = re.match(r"^\s*([A-Za-z][A-Za-z0-9_]{1,63})\s*$", line)
        if standalone_match and standalone_match.group(1).upper() not in {
            "ASK",
            "ASSIGN",
            "ELSE",
            "IF",
            "NOTE",
            "SKIP",
        }:
            next_label = lines[index + 1].strip() if index + 1 < search_end else ""
            candidates.append((index, standalone_match.group(1), next_label, True))
            continue
        possible_match = re.match(r"^\s*([A-Za-z][A-Za-z0-9_]{1,63})\s+(.+)$", line)
        if (
            possible_match
            and not possible_match.group(1).upper().startswith("SECTION")
            and possible_match.group(1).upper()
            not in {"ASK", "ASSIGN", "ELSE", "IF", "NOTE", "SKIP"}
        ):
            candidates.append(
                (index, possible_match.group(1), possible_match.group(2), False)
            )

    if not candidates:
        return None

    # Some text codebooks put the physical code on a line by itself and the
    # label on the next line. Prefer that explicit form. Otherwise, control
    # flow may precede a conventional ``CODE LABEL`` title, so use the final
    # candidate immediately before metadata.
    standalone_candidates = [candidate for candidate in candidates if candidate[3]]
    variable_index, variable_code, variable_label, _ = (
        standalone_candidates[0] if standalone_candidates else candidates[-1]
    )
    lines = lines[variable_index:]

    dotted_index = None
    for index, line in enumerate(lines[1:], start=1):
        if re.match(r"^[.\-\s]{20,}$", line):
            dotted_index = index
            break

    metadata_end = dotted_index if dotted_index is not None else min(len(lines), 8)
    metadata_text = " ".join(lines[1:metadata_end])
    metadata = parse_metadata_line(metadata_text)
    metadata_indexes = [
        index
        for index, line in enumerate(lines[1:metadata_end], start=1)
        if any(f"{key}:" in line for key in ["Section", "File", "Level", "Type", "Width", "Decimals", "Ref"])
    ]
    if not metadata_indexes or not metadata:
        return None

    question_start = max(metadata_indexes) + 1
    question_end = dotted_index if dotted_index is not None else len(lines)
    question_lines = lines[question_start:question_end]
    value_lines = lines[dotted_index + 1 :] if dotted_index is not None else []

    record = {
        "variable_code": variable_code,
        "variable_label": variable_label.strip(),
        "section": metadata.get("section", metadata.get("file", "")),
        "level": metadata.get("level", ""),
        "type": metadata.get("type", ""),
        "width": metadata.get("width", ""),
        "decimals": metadata.get("decimals", ""),
        "ref": metadata.get("ref", ""),
        "question_text": clean_text("\n".join(question_lines)),
        "value_labels": clean_text("\n".join(value_lines)),
        "raw_block": clean_text(block),
    }
    anchors = re.findall(r"@@HRS_ANCHOR:([^@]+)@@", block)
    if anchors:
        anchor_code = anchors[-1].strip()
        derived_code = anchor_code
        section_prefix = record["section"]
        if section_prefix and derived_code.upper().startswith(section_prefix.upper()):
            derived_code = derived_code[len(section_prefix) :]
        if derived_code and derived_code[-1].upper() in {"R", "T", "J", "K", "L"}:
            derived_code = derived_code[:-1]
        if (
            derived_code
            and derived_code.lower().startswith(variable_code.lower())
            and derived_code.lower() != variable_code.lower()
        ):
            record["displayed_variable_code"] = variable_code
            record["variable_code"] = derived_code

    # A few older array codebooks truncate the displayed identifier at the
    # index placeholder (``TPT9020_``) or at its first digit
    # (``ST9020_1`` for child 10). The item label exposes the physical array
    # index, which also agrees with the HTML anchor and CAI reference.
    index_match = re.search(r"(?:CHILD|PERSON|PLAN)\s*-?\s*(\d+)\s*$", variable_label, re.I)
    if index_match:
        index = index_match.group(1)
        normalized_code = variable_code
        if variable_code.endswith("_"):
            normalized_code = variable_code + index
        else:
            truncated_match = re.search(r"_(\d)$", variable_code)
            if (
                truncated_match
                and len(index) > 1
                and index.startswith(truncated_match.group(1))
            ):
                normalized_code = variable_code[:-1] + index
        if normalized_code != variable_code:
            record["displayed_variable_code"] = variable_code
            record["variable_code"] = normalized_code
    return record


def parse_modern_variables(text: str) -> list[dict]:
    blocks = re.split(r"\n\s*=+\s*\n", text)
    variables: list[dict] = []
    seen_exact: set[tuple[str, str, str, str, str]] = set()
    source_subproduct = ""
    for block in blocks:
        for line in block.splitlines():
            line = " ".join(line.split())
            if re.match(
                r"^(?:VERSION\s+[A-Z0-9]+|SECTION\s+\S+)\s*:",
                line,
                flags=re.IGNORECASE,
            ):
                source_subproduct = line
        parsed = split_variable_block(block)
        if parsed is not None:
            parsed["source_subproduct"] = source_subproduct
            exact_key = (
                source_subproduct,
                parsed["section"],
                parsed["level"],
                parsed["variable_code"],
                parsed["raw_block"],
            )
            if exact_key in seen_exact:
                continue
            seen_exact.add(exact_key)
            variables.append(parsed)
    return variables


def legacy_block_record(code: str, label: str, block: str, section: str) -> dict:
    return {
        "variable_code": code,
        "variable_label": clean_text(label),
        "section": section,
        "level": "",
        "type": "",
        "width": "",
        "decimals": "",
        "ref": "",
        "question_text": clean_text(block),
        "value_labels": "",
        "raw_block": clean_text(block),
    }


def parse_legacy_variables(text: str) -> list[dict]:
    """Parse the direct HTML layouts used by the 1992–1994 releases."""
    lines = text.splitlines()
    section = section_title_from_text(text)
    headings: list[tuple[int, str, str]] = []

    # 1994 HRS: ``W201 W201 label`` and identifiers such as ``HHID HHID label``.
    repeated_code = re.compile(
        r"^\s{4,}([A-Za-z][A-Za-z0-9_]{1,31})\s+\1\s+(.+?)\s*$"
    )
    # 1993 AHEAD: ``HHID [HH, RESP, ...] HOUSEHOLD IDENTIFIER``.
    ahead_code = re.compile(
        r"^\s*([A-Za-z][A-Za-z0-9_]{1,31})\s+\[[^\]]+\]\s+(.+?)\s*$"
    )
    # 1992 HRS: questionnaire number is represented in the data as V<number>.
    numeric_code = re.compile(r"^\s{4,}(\d{2,5}[A-Z]?)\s+\S+\s+(.+?)\s*$")

    for index, line in enumerate(lines):
        match = repeated_code.match(line) or ahead_code.match(line)
        if match:
            headings.append((index, match.group(1), match.group(2)))
            continue
        if "HRS 1992" in text:
            match = numeric_code.match(line)
            if match:
                headings.append((index, f"V{match.group(1)}", match.group(2)))

    records: list[dict] = []
    seen: set[str] = set()
    for position, (start, code, label) in enumerate(headings):
        if code in seen:
            continue
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        block = "\n".join(lines[start:end])
        records.append(legacy_block_record(code, label, block, section))
        seen.add(code)
    return records


def parse_legacy_html_anchor_variables(section_html: str) -> list[dict]:
    """Use named variable anchors in early standalone HTML codebooks."""
    from bs4.element import NavigableString, Tag

    soup = BeautifulSoup(section_html, "html.parser")
    anchors = soup.find_all("a", attrs={"name": True})
    section = section_title_from_text(soup.get_text("\n"))
    records: list[dict] = []
    seen: set[str] = set()

    for anchor in anchors:
        anchor_code = str(anchor.get("name", "")).strip().upper()
        if not re.fullmatch(r"[A-Z][A-Z0-9_]{1,63}", anchor_code):
            continue
        if anchor_code in {"TOP", "END"}:
            continue

        fragments: list[str] = []
        for element in anchor.next_elements:
            if element is anchor:
                continue
            if isinstance(element, Tag) and element.name == "a" and element.get("name"):
                break
            if isinstance(element, NavigableString):
                fragments.append(str(element))
        raw_block = "".join(fragments)
        lines = [line.strip() for line in raw_block.splitlines() if line.strip()]

        code = anchor_code
        label = ""
        if lines:
            first_line = lines[0]
            code_match = re.match(r"^\s*([A-Za-z][A-Za-z0-9_]{1,63})\s+(.+)$", first_line)
            numeric_match = re.match(r"^\s*\d{1,5}[A-Z]?\s+\S+\s+(.+)$", first_line)
            if code_match:
                code = code_match.group(1)
                label = code_match.group(2)
            elif numeric_match:
                label = numeric_match.group(1)
            else:
                label = first_line

        if code in seen:
            continue
        records.append(legacy_block_record(code, label, raw_block, section))
        seen.add(code)
    return records


def parse_section_variables(section_content: str, *, is_html: bool = True) -> tuple[str, list[dict], str]:
    if is_html:
        soup = BeautifulSoup(section_content, "html.parser")
        for anchor in soup.find_all("a", attrs={"name": True}):
            anchor.insert_after(f"\n@@HRS_ANCHOR:{anchor.get('name')}@@\n")
        for rule in soup.find_all("hr"):
            rule.replace_with("\n" + "=" * 90 + "\n")
        text = soup.get_text("\n")
    else:
        text = section_content
    title = section_title_from_text(text)
    variables = parse_modern_variables(text)
    parser_format = "modern_block"
    if not variables:
        legacy_variables = parse_legacy_variables(text)
        if is_html:
            anchor_variables = parse_legacy_html_anchor_variables(section_content)
            if len(anchor_variables) > len(legacy_variables):
                legacy_variables = anchor_variables
        variables = legacy_variables
        parser_format = "legacy_direct"

    return title, variables, parser_format


def discover_product_sources(product_url: str, product_content: str) -> list[tuple[str, str]]:
    """Return ``(source_url, source_kind)`` pairs for one directory entry."""
    if urlparse(product_url).path.lower().endswith(".txt"):
        return [(product_url, "text")]

    soup = BeautifulSoup(product_content, "html.parser")
    if soup.find(["frame", "iframe"], src=True):
        return [(get_full_section_url(product_url, product_content), "html")]

    frame_urls = get_section_frame_urls(product_url, product_content)
    if frame_urls:
        return [(url, "frame") for url in frame_urls]

    legacy_urls = get_legacy_section_urls(product_url, product_content)
    if legacy_urls:
        return [(url, "html") for url in legacy_urls]

    # A final fallback for a direct, non-framed HTML codebook.
    return [(product_url, "html")]


def fetch_and_parse_source(
    session: requests.Session,
    raw_dir: Path,
    product: dict,
    source_url: str,
    source_kind: str,
    refresh: bool,
) -> tuple[list[dict], dict]:
    first_content = load_or_fetch(
        session, raw_dir, product["target_key"], source_url, refresh=refresh
    )
    resolved_url = source_url
    content = first_content
    if source_kind == "frame":
        resolved_url = get_full_section_url(source_url, first_content)
        content = load_or_fetch(
            session, raw_dir, product["target_key"], resolved_url, refresh=refresh
        )

    is_html = not urlparse(resolved_url).path.lower().endswith(".txt")
    section_title, variables, parser_format = parse_section_variables(
        content, is_html=is_html
    )
    for variable in variables:
        variable.update(
            {
                "product_key": product["target_key"],
                "product_title": product["product_title"],
                "product_family": product["product_family"],
                "year": product["year"],
                "section_title": section_title,
                "source_url": resolved_url,
                "codebook_url": product["product_url"],
                "documentation_section": product["documentation_section"],
                "documentation_group": product["documentation_group"],
                "source_format": parser_format,
            }
        )
    source_report = {
        "source_url": resolved_url,
        "parser_format": parser_format,
        "variable_count": len(variables),
    }
    return variables, source_report


def build_from_raw_manifest(args: argparse.Namespace) -> list[dict]:
    """Build metadata entirely from the versioned raw snapshots.

    The manifest records the original product and source URLs.  These URLs are
    used only to resolve the deterministic snapshot filenames and provenance;
    this path performs no network requests.
    """
    manifest = json.loads(args.raw_manifest.read_text(encoding="utf-8"))
    all_products = manifest["products"]
    selected_keys = set(expand_product_targets(args.products, all_products))
    products = [
        product for product in all_products if product["target_key"] in selected_keys
    ]
    missing_keys = selected_keys - {product["target_key"] for product in products}
    if missing_keys:
        raise RuntimeError(f"Products absent from raw manifest: {sorted(missing_keys)}")

    records: list[dict] = []
    product_reports: list[dict] = []
    for product in products:
        report = {
            **{key: value for key, value in product.items() if key != "sources"},
            "sources": [],
            "variable_count": 0,
            "status": "ok",
            "error": "",
        }
        for source in product.get("sources", []):
            source_url = source["source_url"]
            snapshot = raw_snapshot_path(args.raw_dir, product["target_key"], source_url)
            if not snapshot.exists():
                raise FileNotFoundError(
                    f"Missing raw snapshot for {source_url}: expected {snapshot}"
                )
            content = snapshot.read_text(encoding="utf-8")
            is_html = not urlparse(source_url).path.lower().endswith(".txt")
            section_title, variables, parser_format = parse_section_variables(
                content, is_html=is_html
            )
            for variable in variables:
                variable.update(
                    {
                        "product_key": product["target_key"],
                        "product_title": product["product_title"],
                        "product_family": product["product_family"],
                        "year": product["year"],
                        "section_title": section_title,
                        "source_url": source_url,
                        "codebook_url": product["product_url"],
                        "documentation_section": product["documentation_section"],
                        "documentation_group": product["documentation_group"],
                        "source_format": parser_format,
                    }
                )
            records.extend(variables)
            report["sources"].append(
                {
                    "source_url": source_url,
                    "parser_format": parser_format,
                    "variable_count": len(variables),
                    "status": "ok" if variables else "zero_variables",
                    "error": "",
                }
            )
            report["variable_count"] += len(variables)
        if not report["variable_count"]:
            report["status"] = "zero_variables"
        elif any(source["status"] != "ok" for source in report["sources"]):
            report["status"] = "partial"
        product_reports.append(report)
        print(f"Parsed {product['product_title']}: {report['variable_count']} variables")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest_path = args.manifest or args.output.with_suffix(".manifest.json")
    output_manifest = {
        "source_directory_url": manifest["source_directory_url"],
        "raw_manifest": str(args.raw_manifest),
        "offline": True,
        "requested_products": args.products,
        "product_count": len(products),
        "successful_product_count": sum(
            report["status"] == "ok" for report in product_reports
        ),
        "zero_variable_product_count": sum(
            report["status"] == "zero_variables" for report in product_reports
        ),
        "error_product_count": sum(
            report["status"] == "error" for report in product_reports
        ),
        "variable_record_count": len(records),
        "products": product_reports,
    }
    manifest_path.write_text(
        json.dumps(output_manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(records)} variable records to {args.output}")
    print(f"Wrote coverage manifest to {manifest_path}")
    return records


def crawl_codebooks(args: argparse.Namespace) -> list[dict]:
    session = build_session()
    products = get_selected_products(session, args.products)
    records: list[dict] = []
    product_reports: list[dict] = []

    for product in products:
        print(f"Fetching product: {product['product_title']}")
        report = {
            **product,
            "sources": [],
            "variable_count": 0,
            "status": "ok",
            "error": "",
        }
        try:
            landing_content = load_or_fetch(
                session,
                args.raw_dir,
                product["target_key"],
                product["product_url"],
                refresh=args.refresh,
            )
            sources = discover_product_sources(product["product_url"], landing_content)

            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = [
                    executor.submit(
                        fetch_and_parse_source,
                        session,
                        args.raw_dir,
                        product,
                        source_url,
                        source_kind,
                        args.refresh,
                    )
                    for source_url, source_kind in sources
                ]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        variables, source_report = future.result()
                    except Exception as error:
                        source_report = {
                            "source_url": "",
                            "parser_format": "",
                            "variable_count": 0,
                            "status": "error",
                            "error": f"{type(error).__name__}: {error}",
                        }
                        report["sources"].append(source_report)
                        print(f"  SOURCE ERROR: {source_report['error']}")
                        if args.fail_fast:
                            raise
                        continue
                    source_report["status"] = (
                        "ok" if source_report["variable_count"] else "zero_variables"
                    )
                    source_report["error"] = ""
                    records.extend(variables)
                    report["sources"].append(source_report)
                    report["variable_count"] += len(variables)
                    print(
                        f"  {Path(urlparse(source_report['source_url']).path).name}: "
                        f"{len(variables)} variables"
                    )
                    if args.sleep:
                        time.sleep(args.sleep)
            if report["variable_count"] == 0:
                report["status"] = "zero_variables"
            elif any(source["status"] != "ok" for source in report["sources"]):
                report["status"] = "partial"
        except Exception as error:
            report["status"] = "error"
            report["error"] = f"{type(error).__name__}: {error}"
            print(f"  ERROR: {report['error']}")
            if args.fail_fast:
                raise
        product_reports.append(report)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest_path = args.manifest or args.output.with_suffix(".manifest.json")
    manifest = {
        "source_directory_url": CODEBOOK_DIRECTORY_URL,
        "requested_products": args.products,
        "product_count": len(products),
        "successful_product_count": sum(
            report["status"] == "ok" for report in product_reports
        ),
        "zero_variable_product_count": sum(
            report["status"] == "zero_variables" for report in product_reports
        ),
        "error_product_count": sum(
            report["status"] == "error" for report in product_reports
        ),
        "variable_record_count": len(records),
        "products": product_reports,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} variable records to {args.output}")
    print(f"Wrote coverage manifest to {manifest_path}")
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--products",
        nargs="+",
        default=DEFAULT_PRODUCTS,
        help=(
            "Product keys such as 2016_core, 2018_core, tracker, or groups: "
            "recent_core_tracker, all_core, all_core_tracker, all_biennial, "
            "all_off_year, all_health, all_xwave, all_documentation_page."
        ),
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_INDEX_PATH)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument(
        "--raw-manifest",
        type=Path,
        default=DEFAULT_RAW_MANIFEST,
        help="Versioned source manifest used to parse bundled snapshots offline.",
    )
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--sleep", type=float, default=0.2)
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Redownload sources instead of reusing raw snapshots in --raw-dir.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.raw_manifest.exists() and not args.refresh:
        build_from_raw_manifest(args)
    else:
        crawl_codebooks(args)


if __name__ == "__main__":
    main()
