import argparse
import glob
import hashlib
import json
import os
import random
import re
import string
from collections import Counter
from pathlib import Path
from typing import Any


ACTION_RE = re.compile(r"(<search>.*?</search>|<answer>.*?</answer>)", re.DOTALL)


def compact(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def normalize_answer(text: str | None) -> str:
    text = (text or "").lower()
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = "".join(ch if ch not in string.punctuation else " " for ch in text)
    return " ".join(text.split())


def token_f1(prediction: str | None, gold: str | None) -> float:
    pred_tokens = normalize_answer(prediction).split()
    gold_tokens = normalize_answer(gold).split()
    if not pred_tokens or not gold_tokens:
        return 0.0
    common = Counter(pred_tokens) & Counter(gold_tokens)
    same = sum(common.values())
    if same == 0:
        return 0.0
    precision = same / len(pred_tokens)
    recall = same / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def token_overlap(prediction: str | None, gold: str | None) -> float:
    pred_tokens = normalize_answer(prediction).split()
    gold_tokens = normalize_answer(gold).split()
    if not pred_tokens or not gold_tokens:
        return 0.0
    common = Counter(pred_tokens) & Counter(gold_tokens)
    return sum(common.values()) / min(len(pred_tokens), len(gold_tokens))


def is_alias_or_near_match(prediction: str | None, gold: str | None) -> bool:
    pred = normalize_answer(prediction)
    ref = normalize_answer(gold)
    if not pred or not ref:
        return False
    if pred in ref or ref in pred:
        return True
    return token_overlap(pred, ref) >= 0.67


def is_correct(prediction: str | None, golds: list[str], threshold: float) -> bool:
    return max((token_f1(prediction, gold) for gold in golds), default=0.0) >= threshold


def is_usable_wrong_answer(prediction: str | None, golds: list[str], threshold: float) -> bool:
    if is_correct(prediction, golds, threshold):
        return False
    return not any(is_alias_or_near_match(prediction, gold) for gold in golds)


def extract_between(text: str | None, start: str, end: str) -> str | None:
    if not isinstance(text, str):
        return None
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text, re.DOTALL | re.I)
    return m.group(1).strip() if m else None


def extract_all(text: str | None, start: str, end: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return [
        compact(m)
        for m in re.findall(re.escape(start) + r"(.*?)" + re.escape(end), text, re.DOTALL | re.I)
    ]


def answer_kind(answer: str) -> str:
    a = (answer or "").strip()
    if re.fullmatch(r"\d{3,4}([-/]\d{1,2}([-/]\d{1,2})?)?", a):
        return "date/year"
    if re.search(r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b", a, re.I):
        return "date"
    if re.search(r"\b(city|county|province|state|country|island|river|mount|lake|road|street|park)\b", a, re.I):
        return "place/location"
    if re.search(r"\d", a):
        return "number or dated fact"
    if len(a.split()) >= 2 and a[:1].isupper():
        return "named entity"
    return "specific fact"


def mask_gold(text: str, golds: list[str]) -> str:
    out = text
    for gold in sorted((g for g in golds if g), key=len, reverse=True):
        norm_gold = normalize_answer(gold)
        if norm_gold in {"yes", "no"} or len(norm_gold) <= 2:
            continue
        pattern = re.escape(gold)
        if re.fullmatch(r"[\w\s]+", gold):
            pattern = r"\b" + pattern + r"\b"
        out = re.sub(pattern, "[hidden answer]", out, flags=re.I)
    return out


def build_hint(question: str, wrong: str, golds: list[str]) -> str:
    gold = golds[0] if golds else ""
    kind = answer_kind(gold)
    q = compact(question).rstrip("?")
    wrong_norm = normalize_answer(wrong)

    if kind in {"date", "date/year", "number or dated fact"}:
        focus = "the exact time-sensitive value required by the question"
    elif kind == "place/location":
        focus = "the exact place or location relation asked by the question"
    elif kind == "named entity":
        focus = "the exact entity for the requested role or relation"
    else:
        focus = "the exact fact, not a broad or related fact"

    caution = "The current candidate is related but may be outdated, too broad, or the wrong relation."
    if wrong_norm:
        caution += " Do not use the current candidate as a query term."
    hint = (
        f"Need evidence for {focus}. "
        f"Target answer type: {kind}. "
        f"Question focus: {q}. "
        f"{caution}"
    )
    return mask_gold(hint, golds)


def question_from_prompt(prompt: str) -> str:
    if "Question:" not in prompt:
        return ""
    tail = prompt.split("Question:", 1)[1]
    tail = re.split(r"<think>|<search>|<answer>", tail, maxsplit=1)[0]
    return compact(tail)


def parse_step_outputs(prompt: str) -> list[str]:
    question_start = prompt.find("Question:")
    text = prompt[question_start:] if question_start >= 0 else prompt
    thinks = re.findall(r"<think>(.*?)</think>", text, re.DOTALL | re.I)
    actions = ACTION_RE.findall(text)
    outs = []
    for i, action in enumerate(actions):
        think = compact(thinks[i]) if i < len(thinks) else ""
        outs.append(f"<think>{think}</think>\n{compact(action)}")
    return outs


def step_prompt_before(prompt: str, step_output: str | None) -> str:
    if step_output:
        variants = [step_output, step_output.replace("\n", ""), compact(step_output)]
        for variant in variants:
            idx = prompt.find(variant)
            if idx >= 0:
                return prompt[:idx]
    matches = list(re.finditer(r"<think>", prompt))
    return prompt[: matches[-1].start()] if matches else prompt


def text_hash(*parts: str) -> str:
    h = hashlib.md5()
    for part in parts:
        h.update((part or "").encode("utf-8", errors="ignore"))
        h.update(b"\0")
    return h.hexdigest()


def gold_is_in_question(gold: str, question: str) -> bool:
    ng = normalize_answer(gold)
    return bool(ng) and ng in normalize_answer(question)


def contains_norm(text: str, needle: str) -> bool:
    nn = normalize_answer(needle)
    return bool(nn) and nn in normalize_answer(text)


def verifiable_golds(golds: list[str]) -> list[str]:
    usable = []
    for gold in golds:
        ng = normalize_answer(gold)
        if ng and ng not in {"yes", "no"} and len(ng) > 2:
            usable.append(gold)
    return usable


def docs_text(docs: Any) -> str:
    if isinstance(docs, dict):
        docs = [docs]
    if not isinstance(docs, list):
        return ""
    parts = []
    for doc in docs:
        if isinstance(doc, dict):
            for key in ("contents", "content", "text", "title"):
                if doc.get(key):
                    parts.append(str(doc[key]))
        elif isinstance(doc, str):
            parts.append(doc)
    return "\n".join(parts)


def has_gold_evidence(text: str, golds: list[str]) -> bool:
    return any(contains_norm(text, gold) for gold in verifiable_golds(golds))


def too_close_query(query: str, question: str, prev_queries: list[str]) -> bool:
    nq = normalize_answer(query)
    if not nq:
        return True
    qn = normalize_answer(question)
    if nq == qn:
        return True
    for prev in prev_queries:
        if nq == normalize_answer(prev):
            return True
    return False


STOP_QUERY_TOKENS = {
    "what", "who", "when", "where", "which", "why", "how", "is", "are", "was", "were",
    "do", "does", "did", "the", "a", "an", "of", "in", "on", "for", "to", "by", "with",
    "from", "and", "or", "has", "have", "had", "be", "been", "being", "there",
}


def content_tokens(text: str) -> set[str]:
    return {t for t in normalize_answer(text).split() if len(t) > 2 and t not in STOP_QUERY_TOKENS}


def source_allowed(path: str, include_keywords: list[str], exclude_keywords: list[str]) -> bool:
    lower = path.lower()
    if include_keywords and not any(k.lower() in lower for k in include_keywords):
        return False
    if exclude_keywords and any(k.lower() in lower for k in exclude_keywords):
        return False
    return True


def high_wrong_answer_overlap(query: str, wrong: str) -> bool:
    wrong_tokens = content_tokens(wrong)
    if len(wrong_tokens) < 6:
        return False
    query_tokens = content_tokens(query)
    if not query_tokens:
        return True
    return len(query_tokens & wrong_tokens) / len(query_tokens) > 0.45


def query_has_refinement(query: str, question: str) -> bool:
    q_tokens = content_tokens(question)
    query_tokens = content_tokens(query)
    if not query_tokens:
        return False
    added = query_tokens - q_tokens
    evidence_terms = {
        "official", "source", "record", "records", "list", "table", "rank", "ranking",
        "winner", "award", "awards", "episode", "title", "cast", "current", "owner",
        "statistics", "site", "locations", "venue", "venues", "history", "date",
        "year", "season", "total", "number", "largest", "smallest", "highest",
        "lowest", "first", "result", "results", "wiki", "imdb",
    }
    if added:
        return True
    return bool(query_tokens & evidence_terms) and len(query_tokens) < max(len(q_tokens), 1)


def model_prompt(question: str, wrong: str, hint: str, prev_queries: list[str]) -> str:
    prev = "; ".join(prev_queries[-3:]) if prev_queries else "none"
    return (
        "You are a SearchR1-style agent. Continue searching instead of answering.\n"
        "You must output exactly one <think> tag and one <search> tag. Do not output <answer>.\n"
        "Do not reveal hidden clues. Do not use the current wrong answer as a query term.\n"
        "Do not simply copy the whole question. Write a compact web-search query with one added evidence cue, such as official source, ranking/list, episode title, award year, current owner, venue, cast, or record.\n\n"
        f"Question: {question}\n"
        f"Current wrong answer to avoid: {wrong}\n"
        f"Previous queries to avoid repeating: {prev}\n"
        f"Diagnostic hint, not an answer: {hint}\n\n"
        "Output format:\n"
        "<think>state the missing evidence briefly</think>\n"
        "<search>targeted query, 4-12 words</search>"
    )


def canonical_chosen(raw: str) -> tuple[str | None, str | None]:
    if "<answer>" in raw.lower():
        return None, None
    think = extract_between(raw, "<think>", "</think>") or ""
    query = extract_between(raw, "<search>", "</search>")
    if not query:
        return None, None
    think = compact(think) or "I need more specific evidence before answering."
    query = compact(query)
    return f"<think>{think}</think>\n<search>{query}</search>", query


def bad_think_text(chosen: str) -> bool:
    think = extract_between(chosen, "<think>", "</think>") or ""
    lower = think.lower()
    boilerplate = (
        "need evidence for",
        "target answer type",
        "question focus",
        "current candidate",
        "do not use the current",
    )
    return any(term in lower for term in boilerplate)


def bad_query_surface(query: str) -> bool:
    words = query.split()
    if len(words) < 4 or len(words) > 14:
        return True
    if re.search(r"\b\w{1,2}$", query) and not re.search(r"\b\d{4}$", query):
        return True
    return False


def load_candidates(
    paths: list[str],
    f1_threshold: float,
    max_candidates: int,
    seed: int,
    include_source_keywords: list[str],
    exclude_source_keywords: list[str],
) -> tuple[list[dict[str, Any]], Counter]:
    rng = random.Random(seed)
    files = []
    for pat in paths:
        files.extend(glob.glob(pat, recursive=True))
    files = sorted(set(files))
    rng.shuffle(files)
    stats = Counter(files=len(files))
    candidates = []
    for path in files:
        if not source_allowed(path, include_source_keywords, exclude_source_keywords):
            stats["skip_source_filter"] += 1
            continue
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception as exc:
            stats[f"file_error:{type(exc).__name__}"] += 1
            continue
        if not isinstance(data, list):
            continue
        for item_idx, item in enumerate(data):
            output = item.get("output", {}) if isinstance(item, dict) else {}
            prompt = output.get("prompt", "")
            golds = item.get("golden_answers") or item.get("golden_answer") or item.get("answers") or []
            if isinstance(golds, str):
                golds = [golds]
            if not prompt or not golds:
                stats["skip_missing_prompt_gold"] += 1
                continue
            question = item.get("question") or question_from_prompt(prompt)
            step_outputs = parse_step_outputs(prompt)
            simulated = output.get("simulated_outputs") or []
            for step_idx, sim in enumerate(simulated):
                original = sim.get("original_output") if isinstance(sim, dict) else None
                if not original and step_idx < len(step_outputs):
                    original = step_outputs[step_idx]
                answer = extract_between(original, "<answer>", "</answer>")
                if not answer:
                    stats["skip_no_answer_action"] += 1
                    continue
                if not is_usable_wrong_answer(answer, golds, f1_threshold):
                    stats["skip_correct_or_alias_answer"] += 1
                    continue
                step_prompt = step_prompt_before(prompt, original)
                prev_queries = extract_all(step_prompt, "<search>", "</search>")
                hint = build_hint(question, answer, golds)
                if any(contains_norm(hint, g) and not gold_is_in_question(g, question) for g in golds):
                    stats["skip_hint_leaks_gold"] += 1
                    continue
                candidates.append(
                    {
                        "source_file": path,
                        "item_idx": item_idx,
                        "step_idx": step_idx,
                        "question": question,
                        "wrong_answer": compact(answer),
                        "golden_answers": golds,
                        "prompt": step_prompt,
                        "rejected": canonical_rejected(original),
                        "previous_queries": prev_queries,
                        "hint": hint,
                    }
                )
                if max_candidates and len(candidates) >= max_candidates:
                    stats["candidates"] = len(candidates)
                    return candidates, stats
    stats["candidates"] = len(candidates)
    return candidates, stats


def canonical_rejected(original: str | None) -> str:
    think = extract_between(original, "<think>", "</think>") or ""
    answer = extract_between(original, "<answer>", "</answer>") or ""
    return f"<think>{compact(think)}</think>\n<answer>{compact(answer)}</answer>"


def write_samples(path: Path, pairs: list[dict[str, Any]], n: int, seed: int) -> None:
    rng = random.Random(seed)
    sample = rng.sample(pairs, min(n, len(pairs)))
    lines = ["# Under Search Hint-Only Generated Samples", ""]
    for i, pair in enumerate(sample, 1):
        m = pair["metadata"]
        lines += [
            f"## {i}. item={m['item_idx']} step={m['step_idx']}",
            f"- question: {m['question']}",
            f"- wrong: {m['wrong_answer']}",
            f"- gold_for_review: {m['golden_answers']}",
            f"- hint_seen_by_model: {m['hint']}",
            f"- query: {m['query']}",
            f"- chosen: {compact(pair['chosen'])}",
            f"- rejected: {compact(pair['rejected'])}",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def checkpoint_path(out_dir: Path) -> Path:
    return out_dir / "provisional_pairs_checkpoint.json"


def save_checkpoint(
    out_dir: Path,
    pairs: list[dict[str, Any]],
    reject_stats: Counter,
    next_start: int,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "pairs": pairs,
        "reject_stats": dict(reject_stats),
        "next_start": next_start,
    }
    tmp = checkpoint_path(out_dir).with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.replace(checkpoint_path(out_dir))


def load_checkpoint(out_dir: Path) -> tuple[list[dict[str, Any]], Counter, int]:
    path = checkpoint_path(out_dir)
    if not path.exists():
        return [], Counter(), 0
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("pairs", []), Counter(payload.get("reject_stats", {})), int(payload.get("next_start", 0))


def apply_retrieval_gain_filter(pairs: list[dict[str, Any]], args: argparse.Namespace, reject_stats: Counter) -> list[dict[str, Any]]:
    if not args.verify_retrieval_gain or not pairs:
        return pairs[: args.max_items] if args.max_items else pairs

    from flashrag.config import Config
    from flashrag.utils import get_retriever

    config_dict = {
        "disable_save": True,
        "gpu_id": args.retrieval_gpu_id,
        "retrieval_method": args.retrieval_method,
        "retrieval_topk": args.retrieval_topk,
        "retrieval_batch_size": args.retrieval_batch_size,
        "faiss_gpu": args.faiss_gpu,
    }
    if args.corpus_path != "None":
        config_dict["corpus_path"] = args.corpus_path
    if args.index_path != "None":
        config_dict["index_path"] = args.index_path

    retriever = get_retriever(Config("my_config.yaml", config_dict))
    kept = []
    queries = [pair["metadata"]["query"] for pair in pairs]
    for start in range(0, len(queries), args.retrieval_batch_size):
        batch_pairs = pairs[start : start + args.retrieval_batch_size]
        batch_queries = queries[start : start + args.retrieval_batch_size]
        results = retriever.batch_search(batch_queries)
        for pair, docs in zip(batch_pairs, results):
            golds = pair["metadata"]["golden_answers"]
            if not verifiable_golds(golds):
                reject_stats["no_verifiable_gold_for_retrieval"] += 1
                continue
            if has_gold_evidence(pair["prompt"], golds):
                reject_stats["old_context_has_gold"] += 1
                continue
            retrieved_text = docs_text(docs)
            if not has_gold_evidence(retrieved_text, golds):
                reject_stats["no_retrieval_gold_hit"] += 1
                continue
            pair["metadata"]["retrieval_gain_verified"] = True
            pair["metadata"]["retrieved_preview"] = compact(retrieved_text)[:1200]
            kept.append(pair)
            if args.max_items and len(kept) >= args.max_items:
                return kept
    return kept


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_glob", nargs="+", default=["output/**/*intermediate_data.json"])
    ap.add_argument("--include_source_keyword", nargs="*", default=[])
    ap.add_argument("--exclude_source_keyword", nargs="*", default=[])
    ap.add_argument("--out_dir", type=Path, default=Path("dpo_data/under_hint_qwen"))
    ap.add_argument("--model_path", default="./models/SearchR1")
    ap.add_argument("--max_candidates", type=int, default=1000)
    ap.add_argument("--max_items", type=int, default=100)
    ap.add_argument("--batch_size", type=int, default=8)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--f1_threshold", type=float, default=0.8)
    ap.add_argument("--max_model_len", type=int, default=2048)
    ap.add_argument("--max_tokens", type=int, default=96)
    ap.add_argument("--gpu_memory_utilization", type=float, default=0.75)
    ap.add_argument("--temperature", type=float, default=0.6)
    ap.add_argument("--top_p", type=float, default=0.9)
    ap.add_argument("--sample_n", type=int, default=100)
    ap.add_argument("--verify_retrieval_gain", action="store_true")
    ap.add_argument("--retrieval_candidate_multiplier", type=int, default=8)
    ap.add_argument("--retrieval_method", default="e5")
    ap.add_argument("--retrieval_topk", type=int, default=5)
    ap.add_argument("--retrieval_batch_size", type=int, default=128)
    ap.add_argument("--retrieval_gpu_id", default="3")
    ap.add_argument("--faiss_gpu", action="store_true")
    ap.add_argument("--corpus_path", default="None")
    ap.add_argument("--index_path", default="None")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--checkpoint_every_batches", type=int, default=20)
    args = ap.parse_args()

    if (args.out_dir / "generation_report.json").exists():
        print(f"Found completed shard at {args.out_dir}; skipping.")
        return

    candidates, stats = load_candidates(
        args.input_glob,
        args.f1_threshold,
        args.max_candidates,
        args.seed,
        args.include_source_keyword,
        args.exclude_source_keyword,
    )
    random.Random(args.seed).shuffle(candidates)

    from vllm import LLM, SamplingParams

    llm = LLM(
        args.model_path,
        tensor_parallel_size=1,
        gpu_memory_utilization=args.gpu_memory_utilization,
        max_model_len=args.max_model_len,
        max_num_seqs=args.batch_size,
        enforce_eager=True,
    )
    sampling = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        stop=["</search>"],
        skip_special_tokens=False,
    )

    pairs = []
    reject_stats = Counter()
    start_offset = 0
    if args.resume:
        pairs, reject_stats, start_offset = load_checkpoint(args.out_dir)

    seen = {p.get("metadata", {}).get("hash") for p in pairs if p.get("metadata", {}).get("hash")}
    seen_questions = {
        text_hash(
            p.get("metadata", {}).get("question", ""),
            p.get("metadata", {}).get("wrong_answer", ""),
            "||".join(p.get("metadata", {}).get("golden_answers", [])),
        )
        for p in pairs
        if p.get("metadata")
    }
    generation_target = args.max_items
    if args.verify_retrieval_gain and args.max_items:
        generation_target = args.max_items * args.retrieval_candidate_multiplier
    for batch_idx, start in enumerate(range(start_offset, len(candidates), args.batch_size), start=1):
        if generation_target and len(pairs) >= generation_target:
            break
        batch = candidates[start : start + args.batch_size]
        prompts = [
            model_prompt(c["question"], c["wrong_answer"], c["hint"], c["previous_queries"])
            for c in batch
        ]
        outs = llm.generate(prompts, sampling)
        for cand, out in zip(batch, outs):
            raw = (out.outputs[0].text or "").strip()
            if "</search>" not in raw:
                raw += "</search>"
            chosen, query = canonical_chosen(raw)
            if not chosen or not query:
                reject_stats["bad_format"] += 1
                continue
            if bad_query_surface(query):
                reject_stats["bad_query_surface"] += 1
                continue
            if bad_think_text(chosen):
                reject_stats["think_copies_hint"] += 1
                continue
            if not query_has_refinement(query, cand["question"]):
                reject_stats["no_query_refinement"] += 1
                continue
            if contains_norm(query, cand["wrong_answer"]):
                reject_stats["query_contains_wrong"] += 1
                continue
            if high_wrong_answer_overlap(query, cand["wrong_answer"]):
                reject_stats["query_high_wrong_overlap"] += 1
                continue
            if too_close_query(query, cand["question"], cand["previous_queries"]):
                reject_stats["query_too_close"] += 1
                continue
            leak = False
            for gold in cand["golden_answers"]:
                if not gold_is_in_question(gold, cand["question"]) and (
                    contains_norm(chosen, gold) or contains_norm(cand["hint"], gold)
                ):
                    leak = True
            if leak:
                reject_stats["gold_leak"] += 1
                continue
            h = text_hash(cand["prompt"], chosen, cand["rejected"])
            qh = text_hash(cand["question"], cand["wrong_answer"], "||".join(cand["golden_answers"]))
            if qh in seen_questions:
                reject_stats["duplicate_question_wrong"] += 1
                continue
            if h in seen:
                reject_stats["duplicate"] += 1
                continue
            seen.add(h)
            seen_questions.add(qh)
            pair = {
                "system": "",
                "prompt": cand["prompt"],
                "chosen": chosen,
                "rejected": cand["rejected"],
                "metadata": {
                    **{k: cand[k] for k in ("source_file", "item_idx", "step_idx", "question", "wrong_answer", "golden_answers", "hint", "previous_queries")},
                    "query": query,
                    "hash": h,
                    "raw_generation": raw,
                },
            }
            pairs.append(pair)
            if generation_target and len(pairs) >= generation_target:
                break
        if args.checkpoint_every_batches > 0 and batch_idx % args.checkpoint_every_batches == 0:
            save_checkpoint(args.out_dir, pairs, reject_stats, start + args.batch_size)

    save_checkpoint(args.out_dir, pairs, reject_stats, min(len(candidates), start + args.batch_size if "start" in locals() else start_offset))

    pairs = apply_retrieval_gain_filter(pairs, args, reject_stats)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "under_hint_qwen_with_metadata.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=2), encoding="utf-8")
    train = [{k: p[k] for k in ("system", "prompt", "chosen", "rejected")} for p in pairs]
    (args.out_dir / "under_hint_qwen.json").write_text(json.dumps(train, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {"selected": len(pairs), "candidate_stats": dict(stats), "reject_stats": dict(reject_stats), "args": vars(args)}
    (args.out_dir / "generation_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    write_samples(args.out_dir / "samples.md", pairs, args.sample_n, args.seed)
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
