"""K12 Promotion Development, local stage: stale-bias decomposition on
the untouched D bucket.

argv: <config.json> <d_bucket.json> <out_raw.jsonl> <out_summary.json>

Computes, per knowledge-update item (both evidence sessions present):
  for each unit kind (turn, sentence) and scoring arm (direct, ppr,
  recency): stale/current best ranks, margin, inversion flag; plus
  lexical-overlap stats for the isomorphism share.
Per non-update item: evidence hits@k under direct vs recency (harm
replication).

Deterministic; local encoder only; loads ONLY the D-bucket file given.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

STOP = set("""a an the is are was were be been being do does did have has had i you he she it we
they my your his her its our their me him them this that these those of in on at to for with
about as by from up down out over under again then once and or but if so not no yes what which
who whom when where why how all any both each few more most other some such only own same than
too very can will just should now""".split())

def words(t):
    return {w for w in re.findall(r"[a-z']+", t.lower()) if w not in STOP}

def parse_date(s):
    return datetime.strptime(s.split(" (")[0], "%Y/%m/%d")

def sentences(t, min_chars):
    parts = re.split(r"(?<=[.!?])\s+|\n+", t)
    return [p.strip() for p in parts if len(p.strip()) >= min_chars]

def main():
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    data = json.loads(Path(sys.argv[2]).read_bytes().decode("utf-8"))
    out_raw = Path(sys.argv[3])
    out_sum = Path(sys.argv[4])
    model = SentenceTransformer(cfg["encoder"], device=cfg["encoder_device"])
    K = cfg["k"]
    rows = []

    def build_units(it, kind):
        units, unit_sess = [], []
        for sid, sess in zip(it["haystack_session_ids"], it["haystack_sessions"]):
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
        return units, unit_sess

    def arms(base, emb, ages, span):
        p = cfg["ppr"]
        n = len(base)
        S = emb @ emb.T
        np.fill_diagonal(S, -1.0)
        W = np.zeros((n, n), dtype=np.float32)
        for i in range(n):
            nb = np.argpartition(-S[i], min(p["knn"], n - 1))[:p["knn"]]
            W[i, nb] = np.maximum(S[i, nb], 0.0)
        W = np.maximum(W, W.T)
        deg = W.sum(1, keepdims=True); deg[deg == 0] = 1.0
        P = W / deg
        p0 = np.exp(base / p["softmax_temp"]); p0 /= p0.sum()
        r = p0.copy()
        for _ in range(p["iterations"]):
            r = (1 - p["damping"]) * p0 + p["damping"] * (P.T @ r)
        rec = base * (0.5 ** (ages / max(1.0, span * cfg["recency_half_life_fraction"])))
        return {"direct": base, "ppr": r, "recency": rec}

    for it in data:
        dates = {s: parse_date(d) for s, d in
                 zip(it["haystack_session_ids"], it["haystack_dates"])}
        ev = [s for s in it["answer_session_ids"] if s in dates]
        is_update = it["question_type"] == "knowledge-update" and len(ev) >= 2
        qv = model.encode([it["question"]], convert_to_numpy=True,
                          normalize_embeddings=True)[0]
        item_row = {"qid": it["question_id"], "type": it["question_type"],
                    "is_update_pair": is_update, "arms": {}}
        for kind in cfg["unit_kinds"]:
            units, unit_sess = build_units(it, kind)
            if not units:
                continue
            emb = model.encode(units, batch_size=512, convert_to_numpy=True,
                               normalize_embeddings=True,
                               show_progress_bar=False)
            base = emb @ qv
            ages = np.array([(max(dates.values()) - dates[s]).days
                             for s in unit_sess], dtype=np.float32)
            span = float(ages.max()) if len(ages) else 1.0
            arm_scores = arms(base, emb, ages, span)
            for arm, score in arm_scores.items():
                key = f"{kind}/{arm}"
                entry = {}
                if is_update:
                    ev_sorted = sorted(ev, key=lambda s: dates[s])
                    stale, cur = ev_sorted[0], ev_sorted[-1]
                    order = np.argsort(-score)
                    def brank(sess):
                        for rank, idx in enumerate(order):
                            if unit_sess[idx] == sess:
                                return int(rank)
                        return len(units)
                    rs, rc = brank(stale), brank(cur)
                    def bsim(sess):
                        idxs = [i for i in range(len(units))
                                if unit_sess[i] == sess]
                        return max(float(base[i]) for i in idxs)
                    entry = {"stale_rank": rs, "cur_rank": rc,
                             "inverted": rs < rc,
                             "margin": round(bsim(cur) - bsim(stale), 4)}
                    if kind == "turn" and arm == "direct":
                        qw = words(it["question"])
                        sidx = max((i for i in range(len(units))
                                    if unit_sess[i] == stale),
                                   key=lambda i: base[i])
                        entry["q_overlap_stale"] = round(
                            len(qw & words(units[sidx])) / max(1, len(qw)), 3)
                else:
                    top = np.argsort(-score)[:K]
                    entry = {"ev_hits": int(sum(1 for i in top
                                                if unit_sess[i] in ev))}
                item_row["arms"][key] = entry
        rows.append(item_row)

    upd = [r for r in rows if r["is_update_pair"]]
    non = [r for r in rows if not r["is_update_pair"] and r["arms"]]
    def inv_rate(kind, arm):
        xs = [r["arms"].get(f"{kind}/{arm}") for r in upd]
        xs = [x for x in xs if x]
        return sum(1 for x in xs if x["inverted"]), len(xs)
    def mean_margin(kind, arm):
        xs = [r["arms"][f"{kind}/{arm}"]["margin"] for r in upd
              if f"{kind}/{arm}" in r["arms"]]
        return float(np.mean(xs)) if xs else None
    def mean_hits(kind, arm):
        xs = [r["arms"][f"{kind}/{arm}"]["ev_hits"] for r in non
              if f"{kind}/{arm}" in r["arms"]]
        return float(np.mean(xs)) if xs else None

    summary = {"n_items": len(rows), "n_update_pairs": len(upd),
               "n_non_update_scored": len(non)}
    for kind in cfg["unit_kinds"]:
        for arm in ("direct", "ppr", "recency"):
            i, n = inv_rate(kind, arm)
            summary[f"inv_{kind}_{arm}"] = f"{i}/{n}"
            summary[f"margin_{kind}_{arm}"] = mean_margin(kind, arm)
            summary[f"hits_{kind}_{arm}"] = mean_hits(kind, arm)

    with out_raw.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    out_sum.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
