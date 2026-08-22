import argparse
import glob
import hashlib
import json
import os
import random
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any


ACTION_RE = re.compile(r"(<search>.*?</search>|<answer>.*?</answer>)", re.DOTALL)


def extract_between(text: str | None, start_token: str, end_token: str) -> str | None:
    if not isinstance(text, str):
        return None
    try:
        start = text.index(start_token) + len(start_token)
        end = text.index(end_token, start)
        return text[start:end]
    except ValueError:
        return None


def extract_between_all(text: str | None, start_token: str, end_token: str) -> list[str]:
    if not isinstance(text, str):
        return []
    pattern = re.escape(start_token) + r"(.*?)" + re.escape(end_token)
    return [m.strip() for m in re.findall(pattern, text, flags=re.DOTALL)]


def normalize_answer(text: str | None) -> str:
    text = (text or "").lower()
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def token_f1(prediction: str | None, gold: str | None) -> float:
    pred_tokens = normalize_answer(prediction).split()
    gold_tokens = normalize_answer(gold).split()
    if not pred_tokens or not gold_tokens:
        return 0.0
    common = Counter(pred_tokens) & Counter(gold_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0
    precision = num_same / len(pred_tokens)
    recall = num_same / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def is_correct(prediction: str | None, golden_answers: list[str], threshold: float) -> bool:
    return max((token_f1(prediction, gold) for gold in golden_answers), default=0.0) >= threshold


def extract_answer(output: str | None) -> str | None:
    answer = extract_between(output, "<answer>", "</answer>")
    return answer.strip() if answer else None


def extract_search(output: str | None) -> str | None:
    query = extract_between(output, "<search>", "</search>")
    return query.strip() if query else None


def is_answer_output(output: str | None) -> bool:
    return extract_answer(output) is not None


def is_search_output(output: str | None) -> bool:
    return extract_search(output) is not None


def merge_think_tags(output: str | None) -> str:
    if not isinstance(output, str):
        return ""
    think_parts = re.findall(r"<think>(.*?)</think>", output, flags=re.DOTALL)
    if not think_parts:
        return output.strip()
    merged = " ".join(part.strip() for part in think_parts if part.strip())
    think_end = output.rfind("</think>") + len("</think>")
    action = output[think_end:].strip()
    return f"<think>{merged}</think>\n{action}".strip()


def parse_prompt_segments(prompt: str | None) -> tuple[list[str], list[str]]:
    if not isinstance(prompt, str):
        return [], []
    question_start = prompt.find("Question:")
    agent_content = prompt[question_start:] if question_start != -1 else prompt
    thinks = re.findall(r"<think>(.*?)</think>", agent_content, flags=re.DOTALL)
    actions = ACTION_RE.findall(agent_content)
    outputs = []
    for idx, action in enumerate(actions):
        think = thinks[idx].strip() if idx < len(thinks) else ""
        outputs.append(f"<think>{think}</think>\n{action.strip()}")
    return outputs, [a.strip() for a in actions]


def get_step_prompt(prompt: str, original_step_output: str | None) -> str:
    if original_step_output:
        compact = original_step_output.replace("\n", "")
        variants = [original_step_output, compact, original_step_output.replace("\n", "\n\n")]
        for variant in variants:
            start = prompt.find(variant)
            if start != -1:
                return prompt[:start]
    matches = list(re.finditer(r"<think>", prompt))
    if matches:
        return prompt[: matches[-1].start()]
    return prompt


def text_hash(*parts: str) -> str:
    h = hashlib.md5()
    for part in parts:
        h.update((part or "").encode("utf-8", errors="ignore"))
        h.update(b"\0")
    return h.hexdigest()


def compact_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def question_from_prompt(prompt: str) -> str:
    marker = "Question:"
    if marker not in prompt:
        return ""
    tail = prompt.split(marker, 1)[1]
    tail = re.split(r"<think>|<search>|<answer>", tail, maxsplit=1)[0]
    return compact_space(tail)


def answer_kind(answer: str) -> str:
    text = answer.strip()
    if re.fullmatch(r"\d{3,4}([-/]\d{1,2}([-/]\d{1,2})?)?", text):
        return "date or year"
    if re.search(r"\b(city|county|province|state|country|island|river|mount|lake)\b", text, re.I):
        return "location"
    if len(text.split()) >= 2 and text[:1].isupper():
        return "named entity"
    if re.search(r"\d", text):
        return "number"
    return "specific fact"


def heuristic_hint_and_query(question: str, gold: str, wrong: str | None) -> tuple[str, str]:
    kind = answer_kind(gold)
    hint = f"Verify the {kind} that distinguishes the correct answer from the current guess."
    query = question
    if wrong:
        query = re.sub(re.escape(wrong), "", query, flags=re.I)
    query = compact_space(query)
    query = re.sub(r"\?$", "", query).strip()
    if len(query.split()) < 4:
        query = f"{query} correct {kind}".strip()
    else:
        query = f"{query} {kind}".strip()
    return hint, query


def llm_hint_and_query(
    question: str,
    gold_answers: list[str],
    wrong_answer: str,
    model: str,
    base_url: str | None,
    api_key: str | None,
    temperature: float,
    retries: int,
) -> tuple[str, str]:
    try:
        from openai import OpenAI
    except Exception as exc:
        raise RuntimeError("openai package is required for --mode llm") from exc

    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"), base_url=base_url or os.getenv("OPENAI_BASE_URL"))
    gold = "; ".join(gold_answers)
    prompt = f"""You are generating one DPO chosen action for a search agent.

Question: {question}
Wrong answer the agent was about to give: {wrong_answer}
Gold answer, visible only to you: {gold}

Return JSON with:
- hint: a short clue about what evidence is missing. Do not reveal the gold answer verbatim.
- query: a concise web/wiki search query likely to retrieve evidence for the gold answer. Do not search the wrong answer. Avoid copying the whole question.

The query may include entities from the question, but should not be only the gold answer.
"""
    last_error = None
    for attempt in range(retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Return only valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
            )
            content = resp.choices[0].message.content or "{}"
            content = content.strip().strip("`")
            if content.startswith("json"):
                content = content[4:].strip()
            obj = json.loads(content)
            return compact_space(obj.get("hint", "")), compact_space(obj.get("query", ""))
        except Exception as exc:
            last_error = exc
            time.sleep(min(2**attempt, 8))
    raise RuntimeError(f"LLM hint generation failed: {last_error}")


def contains_normalized(haystack: str, needle: str) -> bool:
    norm_haystack = normalize_answer(haystack)
    norm_needle = normalize_answer(needle)
    return bool(norm_needle) and norm_needle in norm_haystack


def good_query(
    query: str,
    hint: str,
    gold_answers: list[str],
    wrong_answer: str | None,
    previous_queries: list[str],
    allow_gold_in_query: bool,
) -> tuple[bool, str]:
    if not query or len(query.split()) < 3:
        return False, "query_too_short"
    if len(query) > 220:
        return False, "query_too_long"
    if wrong_answer and contains_normalized(query, wrong_answer):
        return False, "query_contains_wrong_answer"
    for prev in previous_queries:
        if normalize_answer(prev) == normalize_answer(query):
            return False, "query_repeats_previous"
    if not hint or len(hint.split()) < 4:
        return False, "hint_too_short"
    if not allow_gold_in_query:
        for gold in gold_answers:
            if contains_normalized(query, gold):
                return False, "query_contains_gold"
    return True, "ok"


def make_chosen(hint: str, query: str) -> str:
    think = (
        "The current evidence is not enough to answer reliably. "
        f"I should verify the missing clue: {hint}"
    )
    return f"<think>{think}</think>\n<search>{query}</search>"


def iter_input_files(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        expanded = glob.glob(pattern, recursive=True)
        paths.extend(Path(p) for p in expanded)
    return sorted(set(paths))


def generate_from_file(path: Path, args: argparse.Namespace) -> tuple[list[dict[str, Any]], Counter]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} is not a list")

    pairs: list[dict[str, Any]] = []
    stats: Counter = Counter(items=len(data))
    for item_idx, item in enumerate(data):
        output = item.get("output", {}) if isinstance(item, dict) else {}
        prompt = output.get("prompt", "")
        golden_answers = item.get("golden_answers") or item.get("golden_answer") or []
        if isinstance(golden_answers, str):
            golden_answers = [golden_answers]
        if not prompt or not golden_answers:
            stats["skip_missing_prompt_or_gold"] += 1
            continue

        question = item.get("question") or question_from_prompt(prompt)
        simulated_outputs = output.get("simulated_outputs", [])
        original_outputs, action_patterns = parse_prompt_segments(prompt)
        if not simulated_outputs:
            stats["skip_no_simulated_outputs"] += 1
            continue

        for step_idx, sim_step in enumerate(simulated_outputs):
            original_step_output = sim_step.get("original_output") if isinstance(sim_step, dict) else None
            if not original_step_output and step_idx < len(original_outputs):
                original_step_output = original_outputs[step_idx]
            original_action = action_patterns[step_idx] if step_idx < len(action_patterns) else original_step_output
            if not is_answer_output(original_action):
                stats["skip_original_not_answer"] += 1
                continue

            wrong_answer = extract_answer(original_action)
            if is_correct(wrong_answer, golden_answers, args.f1_threshold):
                stats["skip_original_correct"] += 1
                continue
            original_think = extract_between(original_step_output, "<think>", "</think>") or ""
            if wrong_answer and contains_normalized(original_think, wrong_answer):
                stats["skip_answer_in_think"] += 1
                continue

            step_prompt = get_step_prompt(prompt, original_step_output)
            previous_queries = extract_between_all(step_prompt, "<search>", "</search>")
            gold_for_hint = golden_answers[0]
            try:
                if args.mode == "llm":
                    hint, query = llm_hint_and_query(
                        question=question,
                        gold_answers=golden_answers,
                        wrong_answer=wrong_answer or "",
                        model=args.model,
                        base_url=args.base_url,
                        api_key=args.api_key,
                        temperature=args.temperature,
                        retries=args.retries,
                    )
                else:
                    hint, query = heuristic_hint_and_query(question, gold_for_hint, wrong_answer)
            except Exception as exc:
                stats[f"skip_generation_error:{type(exc).__name__}"] += 1
                message = compact_space(str(exc))[:220] or "empty_error_message"
                stats[f"generation_error_message:{message}"] += 1
                continue

            ok, reason = good_query(
                query=query,
                hint=hint,
                gold_answers=golden_answers,
                wrong_answer=wrong_answer,
                previous_queries=previous_queries,
                allow_gold_in_query=args.allow_gold_in_query,
            )
            if not ok:
                stats[f"skip_{reason}"] += 1
                continue

            chosen = make_chosen(hint, query)
            rejected = merge_think_tags(original_step_output)
            pair = {
                "system": "",
                "prompt": step_prompt,
                "chosen": chosen,
                "rejected": rejected,
                "metadata": {
                    "kind": "under_hint_opd",
                    "source_file": str(path),
                    "item_idx": item_idx,
                    "step_idx": step_idx,
                    "question": question,
                    "golden_answers": golden_answers,
                    "wrong_answer": wrong_answer,
                    "hint": hint,
                    "query": query,
                    "previous_queries": previous_queries,
                    "hash": text_hash(step_prompt, chosen, rejected),
                },
            }
            pairs.append(pair)
            stats["kept"] += 1
            if args.max_items and len(pairs) >= args.max_items:
                return pairs, stats
    return pairs, stats


def strip_metadata(pair: dict[str, Any]) -> dict[str, str]:
    return {
        "system": pair.get("system", ""),
        "prompt": pair.get("prompt", ""),
        "chosen": pair.get("chosen", ""),
        "rejected": pair.get("rejected", ""),
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def write_samples(path: Path, pairs: list[dict[str, Any]], n: int, seed: int) -> None:
    rng = random.Random(seed)
    sample = rng.sample(pairs, min(n, len(pairs)))
    lines = ["# Under-Search Hint OPD Samples", ""]
    for idx, pair in enumerate(sample, 1):
        meta = pair["metadata"]
        lines.extend(
            [
                f"## {idx}. {Path(meta['source_file']).name} item={meta['item_idx']} step={meta['step_idx']}",
                f"- question: {meta['question']}",
                f"- gold: {meta['golden_answers']}",
                f"- wrong: {meta['wrong_answer']}",
                f"- hint: {meta['hint']}",
                f"- query: {meta['query']}",
                f"- chosen: {compact_space(pair['chosen'])}",
                f"- rejected: {compact_space(pair['rejected'])}",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate under-search OPD DPO pairs with gold-derived hints.")
    parser.add_argument("--input_glob", nargs="+", default=["output/**/*intermediate_data.json"])
    parser.add_argument("--out_dir", type=Path, default=Path("dpo_data/under_hint_opd"))
    parser.add_argument("--max_items", type=int, default=5000)
    parser.add_argument("--per_file_limit", type=int, default=0)
    parser.add_argument("--f1_threshold", type=float, default=0.8)
    parser.add_argument("--mode", choices=["heuristic", "llm"], default="heuristic")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("--base_url", default=os.getenv("OPENAI_BASE_URL"))
    parser.add_argument("--api_key", default=os.getenv("OPENAI_API_KEY"))
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--allow_gold_in_query", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--sample_n", type=int, default=30)
    args = parser.parse_args()

    input_files = iter_input_files(args.input_glob)
    rng = random.Random(args.seed)
    rng.shuffle(input_files)

    all_pairs: list[dict[str, Any]] = []
    file_reports = []
    seen_hashes = set()
    totals: Counter = Counter(files=len(input_files))
    for path in input_files:
        if args.max_items and len(all_pairs) >= args.max_items:
            break
        file_args = argparse.Namespace(**vars(args))
        remaining = args.max_items - len(all_pairs) if args.max_items else 0
        limits = [x for x in (args.per_file_limit, remaining) if x]
        file_args.max_items = min(limits) if limits else 0
        try:
            pairs, stats = generate_from_file(path, file_args)
        except Exception as exc:
            stats = Counter({f"file_error:{type(exc).__name__}": 1})
            pairs = []
        unique_pairs = []
        for pair in pairs:
            h = pair["metadata"]["hash"]
            if h in seen_hashes:
                stats["skip_duplicate"] += 1
                continue
            seen_hashes.add(h)
            unique_pairs.append(pair)
        all_pairs.extend(unique_pairs)
        totals.update(stats)
        file_reports.append({"file": str(path), "stats": dict(stats), "kept_unique": len(unique_pairs)})

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with_meta_path = args.out_dir / "under_hint_opd_with_metadata.json"
    train_path = args.out_dir / "under_hint_opd.json"
    report_path = args.out_dir / "generation_report.json"
    samples_path = args.out_dir / "samples.md"

    write_json(with_meta_path, all_pairs)
    write_json(train_path, [strip_metadata(p) for p in all_pairs])
    write_json(
        report_path,
        {
            "args": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
            "totals": dict(totals),
            "selected": len(all_pairs),
            "files": file_reports,
        },
    )
    write_samples(samples_path, all_pairs, args.sample_n, args.seed)

    print(json.dumps({"selected": len(all_pairs), "totals": dict(totals)}, ensure_ascii=False, indent=2))
    print(f"Wrote: {train_path}")
    print(f"Wrote: {with_meta_path}")
    print(f"Wrote: {report_path}")
    print(f"Wrote: {samples_path}")


if __name__ == "__main__":
    main()
