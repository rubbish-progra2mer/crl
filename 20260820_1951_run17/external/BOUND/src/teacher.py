"""OpenAI-compatible teacher client with strict JSON responses."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable

class Teacher:
    def __init__(self, model: str, base_url: str | None = None, api_key: str | None = None):
        from openai import OpenAI

        kwargs: Dict[str, Any] = {"api_key": api_key or "not-required"}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)
        self.model = model

    def json(self, messages: Iterable[Dict[str, str]]) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=list(messages),
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("teacher returned an empty response")
        value = json.loads(content)
        if not isinstance(value, dict):
            raise ValueError("teacher response must be a JSON object")
        return value
