"""Serper search, webpage extraction, and frozen QwQ summarization for GAIA."""

from __future__ import annotations

import hashlib
import html
import ipaddress
import re
import time
from typing import Any, Iterable
from urllib.parse import urlsplit


_NOISY_TAGS = ("script", "style", "meta", "noscript", "nav", "header", "footer")
_FINAL_MARKERS = (
    "**Final Answer:**",
    "**Final Information**",
    "**Extracted Facts",
    "Here are the verified facts:",
    "The relevant facts are:",
    "Based on the webpage:",
    "Facts extracted:",
)


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def _set_f1(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    common = len(left & right)
    if common == 0:
        return 0.0
    precision = common / len(right)
    recall = common / len(left)
    return 2 * precision * recall / (precision + recall)


def extract_snippet_with_context(
    full_text: str,
    snippet: str,
    context_chars: int = 2000,
) -> tuple[bool, str]:
    """Return context around the sentence with greatest snippet word overlap."""

    text = full_text[:50_000]
    snippet_words = _words(snippet)
    best_sentence = ""
    best_f1 = 0.15
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        score = _set_f1(snippet_words, _words(sentence))
        if score > best_f1:
            best_sentence = sentence
            best_f1 = score
    if best_sentence:
        position = text.find(best_sentence)
        if position >= 0:
            start = max(0, position - context_chars)
            end = min(len(text), position + len(best_sentence) + context_chars)
            return True, text[start:end]
    return False, text[: context_chars * 2]


def strip_qwq_thinking(text: str) -> str:
    """Remove an explicit QwQ thinking prefix and keep its factual response."""

    value = text.strip()
    if "</think>" in value:
        value = value.rsplit("</think>", 1)[1].strip()
    for marker in _FINAL_MARKERS:
        position = value.find(marker)
        if position >= 0:
            return value[position:].strip()
    if len(value) > 800:
        paragraphs = value.split("\n\n")
        if len(paragraphs) > 3:
            return "\n\n".join(paragraphs[-max(1, len(paragraphs) // 3) :]).strip()
    return value


def _html_to_text(source: str) -> str:
    value = source
    for tag in _NOISY_TAGS:
        value = re.sub(
            rf"<{tag}\b[^>]*>.*?</{tag}>",
            " ",
            value,
            flags=re.IGNORECASE | re.DOTALL,
        )
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(value).split())


def _public_http_url(url: str) -> bool:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    if parsed.hostname.casefold() in {"localhost", "localhost.localdomain"}:
        return False
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        return True
    return not (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
    )


class SerperClient:
    """Minimal client for the Serper Google Search endpoint."""

    def __init__(
        self,
        api_key: str,
        api_url: str = "https://google.serper.dev/search",
        timeout: float = 30.0,
        proxy: str | None = None,
    ):
        if not api_key:
            raise ValueError("Serper API key is required")
        import requests

        self.api_key = api_key
        self.api_url = api_url
        self.timeout = timeout
        self.session = requests.Session()
        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})

    def search(self, query: str, count: int) -> list[dict[str, Any]]:
        response = self.session.post(
            self.api_url,
            headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
            json={"q": query, "num": count},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        organic = payload.get("organic", [])
        if not isinstance(organic, list):
            return []
        results = []
        for rank, item in enumerate(organic, 1):
            if not isinstance(item, dict):
                continue
            url = str(item.get("link", "")).strip()
            if not _public_http_url(url):
                continue
            results.append(
                {
                    "rank": rank,
                    "title": str(item.get("title", "")).strip(),
                    "url": url,
                    "snippet": str(item.get("snippet", "")).strip(),
                }
            )
        return results[:count]


class WebPageFetcher:
    """Fetch HTML pages and keep text near the search-engine snippet."""

    def __init__(
        self,
        timeout: float = 15.0,
        retries: int = 3,
        proxy: str | None = None,
    ):
        import requests

        self.requests = requests
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )
        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})

    def fetch(self, url: str, snippet: str = "") -> str:
        if not _public_http_url(url):
            return ""
        for attempt in range(self.retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code != 200:
                    return ""
                content_type = response.headers.get("Content-Type", "")
                if "pdf" in content_type.casefold():
                    return ""
                text = _html_to_text(response.text)
                if snippet:
                    matched, context = extract_snippet_with_context(text, snippet)
                    if matched:
                        return context
                if len(text) > 5000:
                    return text[:3500] + "\n...\n" + text[-1500:]
                return text
            except self.requests.exceptions.Timeout:
                if attempt + 1 < self.retries:
                    time.sleep(2**attempt)
            except self.requests.exceptions.RequestException:
                return ""
        return ""


class QwQSummarizer:
    """Extract question-relevant facts with a frozen OpenAI-compatible QwQ model."""

    def __init__(
        self,
        base_url: str,
        model: str = "qwq-32b",
        api_key: str = "EMPTY",
        retries: int = 2,
    ):
        if not base_url:
            raise ValueError("summarizer base URL is required")
        from openai import OpenAI

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key or "EMPTY",
            timeout=120.0,
            max_retries=1,
        )
        self.model = model
        self.retries = retries

    def summarize(
        self,
        question: str,
        query: str,
        url: str,
        content: str,
        domain: str,
        previous_reasoning: str = "",
    ) -> dict[str, Any] | None:
        if not content or len(content) < 60:
            return None
        previous = previous_reasoning.strip() or f"Question: {question[:300]}"
        prompt = f"""Extract only facts from the supplied webpage that help answer the question.
Do not use outside knowledge. If the webpage contains no relevant facts, output SKIP.

Question:
{question}

Previous reasoning:
{previous}

Current search query:
{query}

Webpage URL:
{url}

Webpage content:
{content}

Return concise factual notes and preserve important names, dates, and relations."""
        for attempt in range(self.retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2048,
                    temperature=0.6,
                    top_p=0.95,
                    timeout=600,
                )
                raw = (response.choices[0].message.content or "").strip()
                extracted = strip_qwq_thinking(raw)
                if not extracted or "SKIP" in extracted[:20].upper():
                    return None
                return {
                    "title": f"QwQ-Extract: {domain}",
                    "text": extracted,
                    "url": url,
                    "source_query": query,
                    "is_enriched": True,
                }
            except Exception:
                if attempt + 1 < self.retries:
                    time.sleep(2**attempt)
        return None


def _previous_reasoning(
    question: str,
    history: Iterable[dict[str, Any]],
    current_reasoning: str,
) -> str:
    lines = [f"Question: {question}"]
    entries = list(history)[-6:]
    if entries:
        lines.append("Previous search actions:")
        for entry in entries:
            lines.append(
                f"- {entry.get('action', '')}: {entry.get('parameter', '')}"
            )
    if current_reasoning.strip():
        lines.append(f"Current decision rationale: {current_reasoning.strip()}")
    return "\n".join(lines)


class GaiaRetriever:
    """Compose Serper, webpage fetching, and QwQ extraction."""

    def __init__(self, search: SerperClient, fetcher: WebPageFetcher, summarizer: QwQSummarizer):
        self.search = search
        self.fetcher = fetcher
        self.summarizer = summarizer

    def retrieve(
        self,
        query: str,
        top_k: int,
        question: str = "",
        history: Iterable[dict[str, Any]] = (),
        current_reasoning: str = "",
    ) -> list[dict[str, Any]]:
        original_question = question.strip() or query
        previous = _previous_reasoning(original_question, history, current_reasoning)
        search_results = self.search.search(query, max(top_k * 2, top_k))
        documents = []
        for result in search_results:
            content = self.fetcher.fetch(result["url"], result.get("snippet", ""))
            if len(content) < 60:
                content = result.get("snippet", "")
            domain = urlsplit(result["url"]).netloc
            document = self.summarizer.summarize(
                original_question,
                query,
                result["url"],
                content,
                domain,
                previous,
            )
            if document is None:
                continue
            document["doc_id"] = hashlib.sha1(result["url"].encode("utf-8")).hexdigest()
            document["search_rank"] = result["rank"]
            documents.append(document)
            if len(documents) == top_k:
                break
        return documents
