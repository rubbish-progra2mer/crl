"""Optional GAIA web-search retrieval backend."""

from .retriever import (
    GaiaRetriever,
    QwQSummarizer,
    SerperClient,
    WebPageFetcher,
    extract_snippet_with_context,
    strip_qwq_thinking,
)

__all__ = [
    "GaiaRetriever",
    "QwQSummarizer",
    "SerperClient",
    "WebPageFetcher",
    "extract_snippet_with_context",
    "strip_qwq_thinking",
]
