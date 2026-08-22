import json
import random
import re
from collections import Counter
from pathlib import Path


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def between(text: str, start: str, end: str) -> str:
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def all_between(text: str, start: str, end: str):
    return re.findall(re.escape(start) + r"(.*?)" + re.escape(end), text or "", re.S)


def toks(text: str):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def jaccard(a: str, b: str) -> float:
    a_tokens = toks(a)
    b_tokens = toks(b)
    return len(a_tokens & b_tokens) / max(1, len(a_tokens | b_tokens))


def get_question(prompt: str) -> str:
    match = re.search(r"Question:\s*(.*?)(?:<think>|$)", prompt, re.S)
    return clean(match.group(1)) if match else clean(prompt[:500])


def last_searches(prompt: str):
    return [clean(x) for x in all_between(prompt, "<search>", "</search>")]


def features(item: dict) -> dict:
    question = get_question(item["prompt"])
    query = clean(between(item["chosen"], "<search>", "</search>"))
    rejected = clean(between(item["rejected"], "<answer>", "</answer>"))
    searches = last_searches(item["prompt"])
    prev_search = searches[-1] if searches else ""

    sim_question = jaccard(query, question)
    sim_prev = jaccard(query, prev_search)
    sim_rejected = jaccard(query, rejected)

    flags = []
    if len(query) < 8:
        flags.append("too_short")
    if len(query) > 180:
        flags.append("too_long")
    if sim_question > 0.72:
        flags.append("repeats_question")
    if prev_search and sim_prev > 0.72:
        flags.append("repeats_last_search")
    if rejected and sim_rejected > 0.55:
        flags.append("searches_rejected_answer")
    if re.search(r"\b(current|today|now|this season|latest|specific dates?)\b", query, re.I):
        flags.append("time_sensitive_or_vague")
    if re.search(r"\bnot mentioned|not found|unknown|various|specific\b", query, re.I):
        flags.append("low_confidence_reasoning")
    if query.lower().startswith(("what is ", "who is ", "when is ", "where is ", "how much is ")) and sim_question > 0.45:
        flags.append("generic_question_restated")
    if "<|endoftext|>" in item["chosen"] or "<|endoftext|>" in item["rejected"]:
        flags.append("eos_junk")

    return {
        "question": question,
        "query": query,
        "rejected": rejected,
        "prev_search": prev_search,
        "sim_question": sim_question,
        "sim_prev": sim_prev,
        "sim_rejected": sim_rejected,
        "flags": flags,
    }


def add_section(md: list[str], title: str, rows: list[tuple], rng: random.Random, limit: int):
    md.extend(["", f"## {title}", ""])
    if len(rows) > limit:
        rows = rng.sample(rows, limit)
    for rank, (idx, item, f) in enumerate(rows, 1):
        flags = ",".join(f["flags"]) if f["flags"] else "none"
        md.append(f"### {rank}. idx={idx} flags={flags}")
        md.append(f"- question: {f['question'][:1000]}")
        md.append(f"- previous_search: {f['prev_search'][:600]}")
        md.append(f"- chosen_query: {f['query'][:600]}")
        md.append(f"- rejected_answer: {f['rejected'][:600]}")
        md.append(
            f"- sim_question={f['sim_question']:.2f}, "
            f"sim_prev_search={f['sim_prev']:.2f}, sim_rejected={f['sim_rejected']:.2f}"
        )
        md.append(f"- prompt_tail: {clean(item['prompt'])[-1200:]}")
        md.append("")


def main():
    base = Path("dpo_data/curated_main_5k_5k_clean")
    data = json.load(open(base / "under_search_5k.json", encoding="utf-8"))
    rng = random.Random(123)

    rows = []
    flag_counts = Counter()
    combos = Counter()
    for idx, item in enumerate(data):
        f = features(item)
        rows.append((idx, item, f))
        if not f["flags"]:
            flag_counts["no_rule_flag"] += 1
        for flag in f["flags"]:
            flag_counts[flag] += 1
        combos[tuple(sorted(f["flags"]))] += 1

    print("TOTAL", len(data))
    print("FLAG_COUNTS")
    for flag, count in flag_counts.most_common():
        print(count, flag)
    print("\nTOP_COMBOS")
    for combo, count in combos.most_common(20):
        print(count, combo)

    md = ["# Under-search Query Quality Review", "", f"Total under samples: {len(data)}", "", "## Flag Counts", ""]
    for flag, count in flag_counts.most_common():
        md.append(f"- {flag}: {count}")

    for flag in [
        "repeats_question",
        "repeats_last_search",
        "searches_rejected_answer",
        "low_confidence_reasoning",
        "time_sensitive_or_vague",
        "too_long",
    ]:
        add_section(md, flag, [r for r in rows if flag in r[2]["flags"]], rng, 12)

    add_section(md, "no_rule_flag_random", [r for r in rows if not r[2]["flags"]], rng, 20)
    add_section(md, "overall_random", rows, rng, 30)

    output = base / "under_query_quality_review.md"
    output.write_text("\n".join(md), encoding="utf-8")
    print("WROTE", output)


if __name__ == "__main__":
    main()
