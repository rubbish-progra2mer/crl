from __future__ import annotations

import copy
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V033_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
RESULT_PATH = Path(__file__).with_name(
    f"language_typed_argument_controls_{MODEL.replace(':', '_').replace('.', '_')}.json"
)

TOOL = {
    "type": "function",
    "function": {
        "name": "send_message",
        "description": "Send a message.",
        "parameters": {
            "type": "object",
            "required": ["recipient_id", "body", "priority"],
            "properties": {
                "recipient_id": {"type": "string"},
                "body": {"type": "string"},
                "priority": {
                    "type": "string",
                    "enum": ["low", "normal", "high"],
                },
            },
        },
    },
}

TYPED_TOOL = copy.deepcopy(TOOL)
TYPED_PROPERTIES = TYPED_TOOL["function"]["parameters"]["properties"]
TYPED_PROPERTIES["recipient_id"]["description"] = (
    "Language contract COPY_SOURCE: copy the identifier exactly from the request; never translate or normalize it."
)
TYPED_PROPERTIES["body"]["description"] = (
    "Language contract REQUESTED_LANGUAGE: write the message in the language explicitly requested by the user."
)
TYPED_PROPERTIES["priority"]["description"] = (
    "Language contract CANONICAL: return exactly one schema enum token: low, normal, or high."
)

TASKS = [
    {
        "id": "zh_fr",
        "prompt": "请给联系人 Mélanie 发送一条法语消息：“会议改到下午三点”，优先级设为高。",
        "recipient_id": "Mélanie",
        "priority": "high",
        "target_language": "French",
        "keyword_groups": [["réunion"], ["15", "quinze"]],
    },
    {
        "id": "en_de",
        "prompt": "Send contact Zoë-42 a German message saying that the package will arrive tomorrow morning. Use normal priority.",
        "recipient_id": "Zoë-42",
        "priority": "normal",
        "target_language": "German",
        "keyword_groups": [["paket"], ["morgen"]],
    },
    {
        "id": "es_it",
        "prompt": "Envía al contacto João_7 un mensaje en italiano que diga que la llamada se ha movido al lunes. Prioridad baja.",
        "recipient_id": "João_7",
        "priority": "low",
        "target_language": "Italian",
        "keyword_groups": [["chiamata"], ["lunedì", "lunedi"]],
    },
    {
        "id": "fr_en",
        "prompt": "Envoyez au contact 李雷 un message en anglais indiquant que la facture a déjà été payée. Priorité normale.",
        "recipient_id": "李雷",
        "priority": "normal",
        "target_language": "English",
        "keyword_groups": [["invoice"], ["paid"]],
    },
    {
        "id": "de_es",
        "prompt": "Sende dem Kontakt Andrés-9 eine spanische Nachricht: Der Termin ist morgen um neun Uhr. Priorität hoch.",
        "recipient_id": "Andrés-9",
        "priority": "high",
        "target_language": "Spanish",
        "keyword_groups": [["cita"], ["mañana", "manana"], ["nueve", "9"]],
    },
    {
        "id": "ja_ko",
        "prompt": "連絡先 민수-9 に、会議は金曜日にオンラインで行われるという韓国語のメッセージを通常優先度で送ってください。",
        "recipient_id": "민수-9",
        "priority": "normal",
        "target_language": "Korean",
        "keyword_groups": [["회의"], ["금요일"], ["온라인"]],
    },
    {
        "id": "ko_ja",
        "prompt": "연락처 佐藤_3에게 회의실은 3층이라는 일본어 메시지를 낮은 우선순위로 보내세요.",
        "recipient_id": "佐藤_3",
        "priority": "low",
        "target_language": "Japanese",
        "keyword_groups": [["会議室"], ["三階", "3階"]],
    },
    {
        "id": "ar_fr",
        "prompt": "أرسل إلى جهة الاتصال René#5 رسالة بالفرنسية تفيد بأن الموعد قد أُلغي، وبأولوية عالية.",
        "recipient_id": "René#5",
        "priority": "high",
        "target_language": "French",
        "keyword_groups": [["rendez-vous"], ["annulé", "annule"]],
    },
    {
        "id": "ru_en",
        "prompt": "Отправьте контакту Олег-2 сообщение на английском о том, что крайний срок — следующий вторник. Обычный приоритет.",
        "recipient_id": "Олег-2",
        "priority": "normal",
        "target_language": "English",
        "keyword_groups": [["deadline"], ["tuesday"]],
    },
    {
        "id": "pt_de",
        "prompt": "Envie ao contato Müller_8 uma mensagem em alemão dizendo que a senha foi redefinida. Prioridade baixa.",
        "recipient_id": "Müller_8",
        "priority": "low",
        "target_language": "German",
        "keyword_groups": [["passwort"], ["zurückgesetzt", "zuruckgesetzt", "neu definiert"]],
    },
    {
        "id": "zh_it",
        "prompt": "请给联系人 Giulia-六 发送意大利语消息，说明文件已经准备好签字，使用普通优先级。",
        "recipient_id": "Giulia-六",
        "priority": "normal",
        "target_language": "Italian",
        "keyword_groups": [["documento"], ["firma"]],
    },
    {
        "id": "en_ja",
        "prompt": "Send contact 配送係-4 a Japanese message saying that the delivery address has changed. Use high priority.",
        "recipient_id": "配送係-4",
        "priority": "high",
        "target_language": "Japanese",
        "keyword_groups": [["配送先", "配達先"], ["変更"]],
    },
]


def chat(messages: list[dict[str, str]], tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0, "seed": 7, "num_predict": 1024},
        "messages": messages,
    }
    if tools is not None:
        payload["tools"] = tools
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))
    result["client_elapsed_seconds"] = time.perf_counter() - started
    return result


def first_tool_arguments(response: dict[str, Any]) -> dict[str, str] | None:
    calls = response.get("message", {}).get("tool_calls") or []
    if not calls:
        return None
    arguments = calls[0].get("function", {}).get("arguments")
    return arguments if isinstance(arguments, dict) else None


def typed_prompt_call(task: dict[str, Any]) -> tuple[dict[str, str] | None, dict[str, Any]]:
    response = chat(
        [
            {
                "role": "system",
                "content": (
                    "Obey each tool field's language contract independently. COPY_SOURCE fields must remain byte-for-byte "
                    "unchanged, CANONICAL fields must use schema tokens, and REQUESTED_LANGUAGE fields must use the "
                    "language explicitly requested by the user."
                ),
            },
            {"role": "user", "content": task["prompt"]},
        ],
        [TYPED_TOOL],
    )
    return first_tool_arguments(response), response


def pretranslate_call(task: dict[str, Any]) -> tuple[dict[str, str] | None, list[dict[str, Any]], str]:
    translation_response = chat(
        [
            {
                "role": "system",
                "content": (
                    "Translate the request into English. Preserve every contact identifier exactly and preserve the "
                    "instruction that the message body must be written in the explicitly requested target language. "
                    "Return only the translated request."
                ),
            },
            {"role": "user", "content": task["prompt"]},
        ]
    )
    translated = translation_response.get("message", {}).get("content", "").strip()
    tool_response = chat([{"role": "user", "content": translated}], [TOOL])
    return first_tool_arguments(tool_response), [translation_response, tool_response], translated


def parse_json_object(text: str) -> dict[str, str] | None:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        cleaned = "\n".join(lines[1:-1]).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        parsed = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def render_body(task: dict[str, Any], draft: dict[str, str]) -> tuple[dict[str, str] | None, dict[str, Any]]:
    response = chat(
        [
            {
                "role": "system",
                "content": (
                    f"Render only the value of the tool field body in {task['target_language']}. "
                    "Preserve the requested meaning. Return only the field value, without quotes, JSON, labels, or explanation."
                ),
            },
            {
                "role": "user",
                "content": f"Original request:\n{task['prompt']}\n\nDraft body:\n{draft.get('body', '')}",
            },
        ]
    )
    body = response.get("message", {}).get("content", "").strip()
    if not body:
        return None, response
    compiled = dict(draft)
    compiled["body"] = body
    return compiled, response


def refine_whole_call(task: dict[str, Any], draft: dict[str, str]) -> tuple[dict[str, str] | None, dict[str, Any]]:
    response = chat(
        [
            {
                "role": "system",
                "content": (
                    "Correct only the body in the draft tool arguments. The current recipient_id and priority values are "
                    "already correct and immutable: copy their exact draft values into the output. Do not replace a value "
                    "with a contract label. The body must be written in "
                    f"{task['target_language']} while preserving the requested meaning. "
                    "Return only one strict JSON object with recipient_id, body, and priority."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original request:\n{task['prompt']}\n\n"
                    f"Draft arguments:\n{json.dumps(draft, ensure_ascii=False)}"
                ),
            },
        ]
    )
    content = response.get("message", {}).get("content", "")
    return parse_json_object(content), response


def score(task: dict[str, Any], arguments: dict[str, str] | None) -> dict[str, Any]:
    if arguments is None:
        return {
            "parse_ok": False,
            "recipient_ok": False,
            "priority_ok": False,
            "body_ok": False,
            "all_ok": False,
        }
    body = str(arguments.get("body", ""))
    body_folded = body.casefold()
    groups = task["keyword_groups"]
    keyword_hits = [any(keyword.casefold() in body_folded for keyword in group) for group in groups]
    result = {
        "parse_ok": True,
        "recipient_ok": arguments.get("recipient_id") == task["recipient_id"],
        "priority_ok": arguments.get("priority") == task["priority"],
        "body_ok": all(keyword_hits),
        "keyword_hits": keyword_hits,
    }
    result["all_ok"] = all(result[key] for key in ("recipient_ok", "priority_ok", "body_ok"))
    return result


def usage(response: dict[str, Any]) -> dict[str, float | int]:
    return {
        "prompt_tokens": int(response.get("prompt_eval_count", 0)),
        "output_tokens": int(response.get("eval_count", 0)),
        "elapsed_seconds": float(response.get("client_elapsed_seconds", 0.0)),
    }


def combined_usage(responses: list[dict[str, Any]]) -> dict[str, float | int]:
    parts = [usage(response) for response in responses]
    return {
        "prompt_tokens": sum(int(part["prompt_tokens"]) for part in parts),
        "output_tokens": sum(int(part["output_tokens"]) for part in parts),
        "elapsed_seconds": sum(float(part["elapsed_seconds"]) for part in parts),
    }


def summarize(rows: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    scores = [row[mode]["score"] for row in rows]
    usages = [row[mode]["usage"] for row in rows]
    return {
        "n": len(rows),
        "parse_ok": sum(item["parse_ok"] for item in scores),
        "recipient_ok": sum(item["recipient_ok"] for item in scores),
        "priority_ok": sum(item["priority_ok"] for item in scores),
        "body_ok": sum(item["body_ok"] for item in scores),
        "all_ok": sum(item["all_ok"] for item in scores),
        "prompt_tokens": sum(item["prompt_tokens"] for item in usages),
        "output_tokens": sum(item["output_tokens"] for item in usages),
        "elapsed_seconds": sum(item["elapsed_seconds"] for item in usages),
    }


def main() -> None:
    rows: list[dict[str, Any]] = []
    for task in TASKS:
        baseline_response = chat([{"role": "user", "content": task["prompt"]}], [TOOL])
        baseline_arguments = first_tool_arguments(baseline_response)
        typed_arguments, typed_response = typed_prompt_call(task)
        pretranslated_arguments, pretranslated_responses, translated_request = pretranslate_call(task)
        row: dict[str, Any] = {
            "task_id": task["id"],
            "target_language": task["target_language"],
            "baseline": {
                "arguments": baseline_arguments,
                "score": score(task, baseline_arguments),
                "usage": usage(baseline_response),
            },
            "typed_prompt": {
                "arguments": typed_arguments,
                "score": score(task, typed_arguments),
                "usage": usage(typed_response),
            },
            "pretranslate": {
                "arguments": pretranslated_arguments,
                "translated_request": translated_request,
                "score": score(task, pretranslated_arguments),
                "usage": combined_usage(pretranslated_responses),
            },
        }
        if baseline_arguments is None:
            row["whole_refine"] = {
                "arguments": None,
                "score": score(task, None),
                "usage": usage(baseline_response),
                "note": "baseline tool call missing",
            }
            row["field_render"] = {
                "arguments": None,
                "score": score(task, None),
                "usage": usage(baseline_response),
                "note": "baseline tool call missing",
            }
        else:
            refined_arguments, refined_response = refine_whole_call(task, baseline_arguments)
            rendered_arguments, rendered_response = render_body(task, baseline_arguments)
            base_usage = usage(baseline_response)
            refine_usage = usage(refined_response)
            render_usage = usage(rendered_response)
            row["whole_refine"] = {
                "arguments": refined_arguments,
                "score": score(task, refined_arguments),
                "usage": {
                    key: base_usage[key] + refine_usage[key]
                    for key in base_usage
                },
            }
            row["field_render"] = {
                "arguments": rendered_arguments,
                "score": score(task, rendered_arguments),
                "usage": {
                    key: base_usage[key] + render_usage[key]
                    for key in base_usage
                },
            }
        rows.append(row)
        print(
            json.dumps(
                {
                    "task_id": task["id"],
                    "scores": {
                        mode: row[mode]["score"]
                        for mode in ("baseline", "typed_prompt", "pretranslate", "whole_refine", "field_render")
                    },
                },
                ensure_ascii=False,
            )
        )

    result = {
        "model": MODEL,
        "endpoint": ENDPOINT,
        "temperature": 0,
        "seed": 7,
        "task_count": len(TASKS),
        "field_contract": {
            "recipient_id": "COPY_SOURCE",
            "body": "REQUESTED_LANGUAGE",
            "priority": "CANONICAL",
        },
        "summary": {
            mode: summarize(rows, mode)
            for mode in ("baseline", "typed_prompt", "pretranslate", "whole_refine", "field_render")
        },
        "rows": rows,
        "scope_note": (
            "Synthetic fixed-template control experiment. Keyword scoring is deterministic but incomplete; "
            "it measures these authored messages, not deployment prevalence or general multilingual tool use."
        ),
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
