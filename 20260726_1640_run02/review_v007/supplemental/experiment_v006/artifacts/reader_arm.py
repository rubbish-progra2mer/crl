"""K12 Promotion Development, reader stage: answer-level consequences.

argv: <config.json> <d_bucket.json> <out_raw.jsonl>

For each knowledge-update item with both evidence sessions present, runs
three context arms INTERLEAVED per item (drift control): turn_topk,
sentence_topk, oracle_current. Equal context budget via char cap. Raw
API responses appended line-by-line (checkpoint semantics: on restart,
completed (qid, arm) pairs are skipped). API key ONLY from environment
variable DEEPSEEK_API_KEY; never printed; exceptions are redacted.
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
import numpy as np
from sentence_transformers import SentenceTransformer

KEY_PATTERN = re.compile(r"sk-[A-Za-z0-9]+")

def redact(s: str) -> str:
    return KEY_PATTERN.sub("sk-REDACTED", str(s))

def parse_date(s):
    return datetime.strptime(s.split(" (")[0], "%Y/%m/%d")

def sentences(t, min_chars):
    parts = re.split(r"(?<=[.!?])\s+|\n+", t)
    return [p.strip() for p in parts if len(p.strip()) >= min_chars]

def main():
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    data = json.loads(Path(sys.argv[2]).read_bytes().decode("utf-8"))
    out_raw = Path(sys.argv[3])
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("DEEPSEEK_API_KEY not set", file=sys.stderr)
        return 2
    rc = cfg["reader"]
    done = set()
    if out_raw.exists():
        for line in out_raw.read_text(encoding="utf-8").splitlines():
            try:
                j = json.loads(line)
                done.add((j["qid"], j["arm"]))
            except Exception:
                pass
    model = SentenceTransformer(cfg["encoder"], device=cfg["encoder_device"])
    cap = cfg["context_char_cap"]
    K = cfg["k"]

    items = [it for it in data
             if it["question_type"] == "knowledge-update"
             and len([s for s in it["answer_session_ids"]
                      if s in set(it["haystack_session_ids"])]) >= 2]

    with out_raw.open("a", encoding="utf-8") as fout:
        for it in items:
            qid = it["question_id"]
            dates = {s: parse_date(d) for s, d in
                     zip(it["haystack_session_ids"], it["haystack_dates"])}
            ev = [s for s in it["answer_session_ids"] if s in dates]
            cur_sess = max(ev, key=lambda s: dates[s])
            qv = model.encode([it["question"]], convert_to_numpy=True,
                              normalize_embeddings=True)[0]

            def contexts():
                out = {}
                for kind, arm_name in (("turn", "turn_topk"),
                                       ("sentence", "sentence_topk")):
                    units, unit_sess, unit_date = [], [], []
                    for sid, sess in zip(it["haystack_session_ids"],
                                         it["haystack_sessions"]):
                        for turn in sess:
                            txt = turn["content"].strip()
                            if not txt:
                                continue
                            if kind == "turn":
                                units.append(txt[:cfg["turn_char_cap"]])
                                unit_sess.append(sid)
                            else:
                                for s_ in sentences(txt, cfg["sentence_min_chars"]):
                                    units.append(s_[:cfg["sentence_char_cap"]])
                                    unit_sess.append(sid)
                    emb = model.encode(units, batch_size=512,
                                       convert_to_numpy=True,
                                       normalize_embeddings=True,
                                       show_progress_bar=False)
                    sims = emb @ qv
                    top = np.argsort(-sims)[:K]
                    parts = [f"[{it['haystack_dates'][it['haystack_session_ids'].index(unit_sess[i])]}] {units[i]}"
                             for i in top]
                    out[arm_name] = "\n---\n".join(parts)[:cap]
                oracle_parts = []
                for sid, sess in zip(it["haystack_session_ids"],
                                     it["haystack_sessions"]):
                    if sid == cur_sess:
                        d = it["haystack_dates"][
                            it["haystack_session_ids"].index(sid)]
                        for turn in sess:
                            txt = turn["content"].strip()
                            if txt:
                                oracle_parts.append(f"[{d}] {txt[:cfg['turn_char_cap']]}")
                out["oracle_current"] = "\n---\n".join(oracle_parts)[:cap]
                return out

            ctxs = contexts()
            for arm in rc["arms"]:
                if (qid, arm) in done:
                    continue
                prompt = rc["prompt_template"].format(
                    context=ctxs[arm], question_date=it["question_date"],
                    question=it["question"])
                body = {"model": rc["model"],
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": rc["temperature"],
                        "max_tokens": rc["max_tokens"]}
                t0 = time.time()
                try:
                    resp = httpx.post(
                        rc["base_url"],
                        headers={"Authorization": f"Bearer {key}",
                                 "Content-Type": "application/json"},
                        json=body, timeout=120)
                    payload = resp.json()
                    row = {"qid": qid, "arm": arm,
                           "ts_utc": datetime.now(timezone.utc).isoformat(),
                           "latency_s": round(time.time() - t0, 2),
                           "status": resp.status_code,
                           "model_field": payload.get("model"),
                           "usage": payload.get("usage"),
                           "answer": (payload.get("choices") or [{}])[0]
                                     .get("message", {}).get("content"),
                           "gold": it["answer"]}
                except Exception as e:
                    row = {"qid": qid, "arm": arm,
                           "ts_utc": datetime.now(timezone.utc).isoformat(),
                           "error": redact(repr(e))}
                fout.write(json.dumps(row, ensure_ascii=False) + "\n")
                fout.flush()
                time.sleep(0.3)
    print("reader arm complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
