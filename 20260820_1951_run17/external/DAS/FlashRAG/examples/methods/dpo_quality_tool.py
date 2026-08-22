import argparse
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path


ACTION_RE = re.compile(r"(<search>.*?</search>|<answer>.*?</answer>)", re.DOTALL)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} is not a JSON list")
    return data


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def text_hash(*parts: str) -> str:
    h = hashlib.md5()
    for part in parts:
        h.update((part or "").encode("utf-8", errors="ignore"))
        h.update(b"\0")
    return h.hexdigest()


def compact(text: str, limit: int = 700) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[:limit] + " ..."


def infer_kind(path: Path, item: dict | None = None) -> str:
    name = path.name.lower()
    parent = path.parent.name.lower()
    joined = f"{parent}/{name}"
    if "over" in joined:
        return "over"
    if "under" in joined:
        return "under"
    if item:
        chosen = item.get("chosen", "")
        rejected = item.get("rejected", "")
        if "<answer>" in chosen and "<search>" in rejected:
            return "over"
        if "<search>" in chosen and "<answer>" in rejected:
            return "under"
    return "unknown"


def action_type(text: str) -> str:
    has_search = "<search>" in text and "</search>" in text
    has_answer = "<answer>" in text and "</answer>" in text
    if has_search and has_answer:
        return "mixed"
    if has_search:
        return "search"
    if has_answer:
        return "answer"
    return "none"


def count_action_tags(text: str) -> int:
    return len(ACTION_RE.findall(text or ""))


def has_balanced_think(text: str) -> bool:
    return (text or "").count("<think>") == (text or "").count("</think>")


def final_action_content(text: str, tag: str) -> str:
    start = f"<{tag}>"
    end = f"</{tag}>"
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def normalize_item(raw: dict) -> dict:
    return {
        "system": raw.get("system", ""),
        "prompt": raw.get("prompt", ""),
        "chosen": raw.get("chosen", ""),
        "rejected": raw.get("rejected", ""),
    }


def quality_check(raw: dict, kind: str, max_chars: int) -> tuple[bool, list[str], dict]:
    reasons = []
    if not isinstance(raw, dict):
        return False, ["not_dict"], {}

    missing = [key for key in ("prompt", "chosen", "rejected") if key not in raw]
    if missing:
        reasons.append("missing_" + "_".join(missing))

    item = normalize_item(raw)
    prompt = item["prompt"]
    chosen = item["chosen"]
    rejected = item["rejected"]

    for key, value in item.items():
        if not isinstance(value, str):
            reasons.append(f"{key}_not_string")

    if not prompt.strip():
        reasons.append("empty_prompt")
    if not chosen.strip():
        reasons.append("empty_chosen")
    if not rejected.strip():
        reasons.append("empty_rejected")
    if chosen.strip() == rejected.strip():
        reasons.append("chosen_equals_rejected")

    chosen_type = action_type(chosen)
    rejected_type = action_type(rejected)

    if kind == "over":
        if chosen_type != "answer":
            reasons.append(f"over_chosen_not_answer:{chosen_type}")
        if rejected_type != "search":
            reasons.append(f"over_rejected_not_search:{rejected_type}")
        if not final_action_content(chosen, "answer"):
            reasons.append("empty_chosen_answer")
        if not final_action_content(rejected, "search"):
            reasons.append("empty_rejected_search")
    elif kind == "under":
        if chosen_type != "search":
            reasons.append(f"under_chosen_not_search:{chosen_type}")
        if rejected_type != "answer":
            reasons.append(f"under_rejected_not_answer:{rejected_type}")
        if not final_action_content(chosen, "search"):
            reasons.append("empty_chosen_search")
        if not final_action_content(rejected, "answer"):
            reasons.append("empty_rejected_answer")
    else:
        reasons.append("unknown_kind")

    if not has_balanced_think(chosen):
        reasons.append("chosen_unbalanced_think")
    if not has_balanced_think(rejected):
        reasons.append("rejected_unbalanced_think")

    total_chars = len(prompt) + len(chosen) + len(rejected)
    if total_chars > max_chars:
        reasons.append("too_long")

    # The DPO item should usually train one local decision, not multiple complete actions.
    if count_action_tags(chosen) != 1:
        reasons.append(f"chosen_action_count:{count_action_tags(chosen)}")
    if count_action_tags(rejected) != 1:
        reasons.append(f"rejected_action_count:{count_action_tags(rejected)}")

    info = {
        "kind": kind,
        "chars": total_chars,
        "prompt_chars": len(prompt),
        "chosen_chars": len(chosen),
        "rejected_chars": len(rejected),
        "chosen_type": chosen_type,
        "rejected_type": rejected_type,
        "hash": text_hash(prompt, chosen, rejected),
    }
    return not reasons, reasons, info


def discover_files(dpo_dir: Path) -> list[Path]:
    skip_names = {
        "all_dpo_data.json",
        "dpo_pairs.json",
        "curated_10k.json",
        "quality_samples.json",
        "quality_samples.md",
    }
    files = []
    for path in dpo_dir.rglob("*.json"):
        if path.name in skip_names:
            continue
        files.append(path)
    return sorted(files)


def collect(dpo_dir: Path, max_chars: int):
    records = []
    file_summaries = []
    duplicate_seen = set()

    for path in discover_files(dpo_dir):
        try:
            data = load_json(path)
        except Exception as exc:
            file_summaries.append({"file": str(path), "error": str(exc)})
            continue

        counts = Counter()
        reason_counts = Counter()
        for idx, raw in enumerate(data):
            kind = infer_kind(path, raw if isinstance(raw, dict) else None)
            ok, reasons, info = quality_check(raw, kind, max_chars)
            item = normalize_item(raw) if isinstance(raw, dict) else {}
            dup = info.get("hash") in duplicate_seen if info else False
            if ok and dup:
                ok = False
                reasons = ["duplicate"]
            if ok:
                duplicate_seen.add(info["hash"])

            counts[f"{kind}_total"] += 1
            counts[f"{kind}_ok" if ok else f"{kind}_bad"] += 1
            for reason in reasons:
                reason_counts[reason] += 1

            records.append(
                {
                    "source": str(path),
                    "index": idx,
                    "kind": kind,
                    "ok": ok,
                    "reasons": reasons,
                    "info": info,
                    "item": item,
                }
            )

        file_summaries.append(
            {
                "file": str(path),
                "items": len(data),
                "counts": dict(counts),
                "top_bad_reasons": reason_counts.most_common(12),
            }
        )

    return records, file_summaries


def choose(records, kind: str, n: int, seed: int) -> list[dict]:
    candidates = [r for r in records if r["ok"] and r["kind"] == kind]
    rng = random.Random(seed)
    rng.shuffle(candidates)

    # Prefer concise single-decision samples, then keep source diversity through shuffling.
    candidates.sort(key=lambda r: r["info"]["chars"])
    selected = candidates[:n]
    rng.shuffle(selected)
    return [r["item"] for r in selected]


def sample_records(records, kind: str, ok: bool, n: int, seed: int):
    pool = [r for r in records if r["kind"] == kind and r["ok"] == ok]
    rng = random.Random(seed)
    return rng.sample(pool, min(n, len(pool)))


def write_samples(out_dir: Path, samples: list[dict]):
    json_path = out_dir / "quality_samples.json"
    md_path = out_dir / "quality_samples.md"
    write_json(json_path, samples)

    lines = ["# DPO Quality Samples", ""]
    for i, r in enumerate(samples, 1):
        lines.append(f"## {i}. {r['kind']} | ok={r['ok']} | {Path(r['source']).name}#{r['index']}")
        if r["reasons"]:
            lines.append(f"- reasons: {', '.join(r['reasons'])}")
        lines.append(f"- prompt: {compact(r['item'].get('prompt', ''))}")
        lines.append(f"- chosen: {compact(r['item'].get('chosen', ''))}")
        lines.append(f"- rejected: {compact(r['item'].get('rejected', ''))}")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Audit and curate DPO decision-boundary data.")
    parser.add_argument("--dpo_dir", type=Path, default=Path("dpo_data"))
    parser.add_argument("--out_dir", type=Path, default=Path("dpo_data/curated_main_5k_5k"))
    parser.add_argument("--over_n", type=int, default=5000)
    parser.add_argument("--under_n", type=int, default=5000)
    parser.add_argument("--max_chars", type=int, default=60000)
    parser.add_argument("--sample_n", type=int, default=25)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    records, file_summaries = collect(args.dpo_dir, args.max_chars)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    totals = Counter()
    bad_reasons = Counter()
    source_counts = defaultdict(Counter)
    for r in records:
        totals[f"{r['kind']}_total"] += 1
        totals[f"{r['kind']}_ok" if r["ok"] else f"{r['kind']}_bad"] += 1
        source_counts[r["kind"]][r["source"]] += int(r["ok"])
        for reason in r["reasons"]:
            bad_reasons[f"{r['kind']}:{reason}"] += 1

    over = choose(records, "over", args.over_n, args.seed)
    under = choose(records, "under", args.under_n, args.seed + 1)
    merged = over + under
    random.Random(args.seed + 2).shuffle(merged)

    write_json(args.out_dir / "over_search_5k.json", over)
    write_json(args.out_dir / "under_search_5k.json", under)
    write_json(args.out_dir / "all_dpo_10k.json", merged)

    samples = []
    for kind in ("over", "under"):
        samples.extend(sample_records(records, kind, True, args.sample_n, args.seed))
        samples.extend(sample_records(records, kind, False, args.sample_n, args.seed))
    write_samples(args.out_dir, samples)

    report = {
        "dpo_dir": str(args.dpo_dir),
        "out_dir": str(args.out_dir),
        "totals": dict(totals),
        "selected": {"over": len(over), "under": len(under), "merged": len(merged)},
        "top_bad_reasons": bad_reasons.most_common(40),
        "ok_by_source": {k: v.most_common() for k, v in source_counts.items()},
        "files": file_summaries,
    }
    write_json(args.out_dir / "quality_report.json", report)

    print(json.dumps(report["totals"], ensure_ascii=False, indent=2))
    print(json.dumps(report["selected"], ensure_ascii=False, indent=2))
    print("Top bad reasons:")
    for reason, count in report["top_bad_reasons"][:20]:
        print(f"  {reason}: {count}")
    print(f"\nWrote: {args.out_dir / 'quality_report.json'}")
    print(f"Wrote: {args.out_dir / 'quality_samples.md'}")
    print(f"Wrote: {args.out_dir / 'all_dpo_10k.json'}")


if __name__ == "__main__":
    main()
