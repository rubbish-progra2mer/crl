import json
import re
import string
from pathlib import Path


SRCS = [
    "dpo_data/under_hint_qwen_gpu3_gain_multihop50_s1/under_hint_qwen_with_metadata.json",
    "dpo_data/under_hint_qwen_gpu3_gain_multihop50_s2/under_hint_qwen_with_metadata.json",
    "dpo_data/under_hint_qwen_gpu3_gain_multihop50_s3/under_hint_qwen_with_metadata.json",
]
OUT = Path("dpo_data/under_hint_qwen_gain_multihop100_reviewed")

STOP = set(
    "the a an of in on for to and or by with from is are was were be been being "
    "what who which when where how did does do had has have as it its this that "
    "current candidate related exact need evidence answer type target question focus".split()
)


def norm(text: str | None) -> str:
    text = (text or "").lower()
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = "".join(ch if ch not in string.punctuation else " " for ch in text)
    return " ".join(text.split())


def toks(text: str | None) -> list[str]:
    return [t for t in norm(text).split() if len(t) > 2 and t not in STOP]


def aliasish(a: str, b: str) -> bool:
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return False
    if na in nb or nb in na:
        return True
    if na.replace(" ", "") in nb.replace(" ", "") or nb.replace(" ", "") in na.replace(" ", ""):
        return True
    ta, tb = set(toks(a)), set(toks(b))
    if not ta or not tb:
        return False
    return len(ta & tb) / max(1, min(len(ta), len(tb))) >= 0.75


def high_wrong_overlap(query: str, wrong: str) -> bool:
    qt, wt = set(toks(query)), set(toks(wrong))
    return len(wt) >= 6 and bool(qt) and len(qt & wt) / len(qt) > 0.45


def compact(text: str) -> str:
    return " ".join((text or "").split())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_items = []
    for src in SRCS:
        path = Path(src)
        if path.exists():
            all_items.extend(json.loads(path.read_text(encoding="utf-8")))

    seen = set()
    kept = []
    reject = {}

    def rej(key: str) -> None:
        reject[key] = reject.get(key, 0) + 1

    for item in all_items:
        meta = item["metadata"]
        question = meta["question"]
        wrong = meta["wrong_answer"]
        golds = meta["golden_answers"]
        query = meta["query"]
        if any(aliasish(wrong, gold) for gold in golds):
            rej("aliasish_wrong_gold")
            continue
        if high_wrong_overlap(query, wrong):
            rej("high_wrong_overlap")
            continue
        key = (norm(question), norm(wrong), "|".join(norm(g) for g in golds))
        if key in seen:
            rej("duplicate_qwg")
            continue
        seen.add(key)
        kept.append(item)
        if len(kept) >= 100:
            break

    train = [{k: item[k] for k in ("system", "prompt", "chosen", "rejected")} for item in kept]
    (OUT / "under_hint_qwen_with_metadata.json").write_text(
        json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "under_hint_qwen.json").write_text(
        json.dumps(train, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report = {"raw": len(all_items), "kept": len(kept), "reject": reject, "sources": SRCS}
    (OUT / "merge_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Reviewed Multihop Under-Search Samples", ""]
    for i, item in enumerate(kept, 1):
        meta = item["metadata"]
        lines.extend(
            [
                f"## {i}",
                f"- q: {meta['question']}",
                f"- wrong: {meta['wrong_answer']}",
                f"- gold: {meta['golden_answers']}",
                f"- query: {meta['query']}",
                f"- chosen: {compact(item['chosen'])}",
                "",
            ]
        )
    (OUT / "samples_100.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
