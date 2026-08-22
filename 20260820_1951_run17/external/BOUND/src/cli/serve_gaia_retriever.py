"""Serve the optional Serper + QwQ GAIA retrieval backend over HTTP."""

from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from gaia import GaiaRetriever, QwQSummarizer, SerperClient, WebPageFetcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8002)
    parser.add_argument(
        "--serper-api-url",
        default=os.getenv("SERPER_API_URL", "https://google.serper.dev/search"),
    )
    parser.add_argument("--summarizer-url", default=os.getenv("GAIA_SUMMARIZER_URL"))
    parser.add_argument(
        "--summarizer-model",
        default=os.getenv("GAIA_SUMMARIZER_MODEL", "qwq-32b"),
    )
    parser.add_argument("--http-proxy", default=os.getenv("GAIA_HTTP_PROXY"))
    parser.add_argument("--fetch-timeout", type=float, default=15.0)
    return parser.parse_args()


def make_handler(retriever: GaiaRetriever) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def _json(self, status: int, value: dict[str, Any]) -> None:
            payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/":
                self._json(404, {"error": "not found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 1_000_000:
                    raise ValueError("invalid request size")
                value = json.loads(self.rfile.read(length).decode("utf-8"))
                query = str(value["query"]).strip()
                top_k = int(value.get("top_k", 5))
                if not query or not 1 <= top_k <= 20:
                    raise ValueError("query must be non-empty and top_k must be between 1 and 20")
                history = value.get("history", [])
                if not isinstance(history, list):
                    raise ValueError("history must be a list")
                documents = retriever.retrieve(
                    query=query,
                    top_k=top_k,
                    question=str(value.get("question", "")),
                    history=history,
                    current_reasoning=str(value.get("reasoning", "")),
                )
                self._json(200, {"documents": documents})
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                self._json(400, {"error": str(exc)})
            except Exception:
                self._json(502, {"error": "retrieval backend failed"})

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def main() -> None:
    args = parse_args()
    serper_api_key = os.getenv("SERPER_API_KEY")
    summarizer_api_key = os.getenv("GAIA_SUMMARIZER_API_KEY", "EMPTY")
    if not serper_api_key:
        raise RuntimeError("set SERPER_API_KEY")
    if not args.summarizer_url:
        raise RuntimeError("set GAIA_SUMMARIZER_URL or pass --summarizer-url")
    search = SerperClient(
        serper_api_key,
        args.serper_api_url,
        proxy=args.http_proxy,
    )
    fetcher = WebPageFetcher(
        timeout=args.fetch_timeout,
        proxy=args.http_proxy,
    )
    summarizer = QwQSummarizer(
        base_url=args.summarizer_url,
        model=args.summarizer_model,
        api_key=summarizer_api_key,
    )
    retriever = GaiaRetriever(search, fetcher, summarizer)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(retriever))
    print(f"GAIA retriever listening on http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
