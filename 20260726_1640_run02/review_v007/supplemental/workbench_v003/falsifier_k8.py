"""Workbench decisive falsifier for kernel K8 (run02 v003).

Preregistered defaults (no tuning loop):
  near-duplicate band: cosine > 0.80 between units of DIFFERENT sessions
  with session-date gap >= 1 day; older member score *= 0.5.
  Global-recency comparator: score *= 0.5 ** (age_days / half_life),
  half_life = half the item's history span in days.
  K = 10 units.

Kill conditions (from problem_v003.md):
  (a) arbitration fails to fix the majority of observed stale-over-current
      inversions on W-bucket knowledge-update items, OR
  (b) it breaks non-update evidence hit@10 (statistically visible drop).

W bucket only (physically separated file). Local compute only.
"""
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

W_FILE = Path(r"D:\Desktop\crl\20260726_1640_run02\data_split_commitment_v002\longmemeval_s_WORKBENCH.json")
K = 10
TAU = 0.80
GAMMA = 0.5
MIN_GAP_DAYS = 1

def parse_date(s: str) -> datetime:
    return datetime.strptime(s.split(" (")[0], "%Y/%m/%d")

def main() -> None:
    data = json.loads(W_FILE.read_bytes().decode("utf-8"))
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                device="cuda")
    upd_rows, non_rows = [], []
    for it in data:
        sess_ids = it["haystack_session_ids"]
        dates = {s: parse_date(d) for s, d in
                 zip(sess_ids, it["haystack_dates"])}
        units, unit_sess = [], []
        for sid, sess in zip(sess_ids, it["haystack_sessions"]):
            for turn in sess:
                txt = turn["content"].strip()
                if txt:
                    units.append(txt[:1000])
                    unit_sess.append(sid)
        if not units:
            continue
        emb = model.encode(units, batch_size=256, convert_to_numpy=True,
                           normalize_embeddings=True, show_progress_bar=False)
        qv = model.encode([it["question"]], convert_to_numpy=True,
                          normalize_embeddings=True)[0]
        base = emb @ qv
        n = len(units)
        ages = np.array([(max(dates.values()) - dates[unit_sess[i]]).days
                         for i in range(n)], dtype=np.float32)

        # K8 arm: pairwise arbitration in near-dup cross-session pairs
        k8 = base.copy()
        S = emb @ emb.T
        cand = np.argwhere(S > TAU)
        for i, j in cand:
            if i >= j:
                continue
            si, sj = unit_sess[i], unit_sess[j]
            if si == sj:
                continue
            gap = (dates[si] - dates[sj]).days
            if abs(gap) < MIN_GAP_DAYS:
                continue
            older = i if gap > 0 and False else (i if dates[si] < dates[sj] else j)
            k8[older] = min(k8[older], base[older] * GAMMA)

        # global recency arm
        span = max(1.0, float(ages.max()))
        rec = base * (0.5 ** (ages / (span / 2.0)))

        ev = [s for s in it["answer_session_ids"] if s in dates]

        def best_rank(score, sess):
            order = np.argsort(-score)
            for rank, idx in enumerate(order):
                if unit_sess[idx] == sess:
                    return int(rank)
            return n

        def ev_hits_at_k(score):
            top = np.argsort(-score)[:K]
            return sum(1 for i in top if unit_sess[i] in ev)

        if it["question_type"] == "knowledge-update" and len(ev) >= 2:
            ev_sorted = sorted(ev, key=lambda s: dates[s])
            stale, cur = ev_sorted[0], ev_sorted[-1]
            row = {"qid": it["question_id"]}
            for name, score in (("base", base), ("k8", k8), ("rec", rec)):
                row[name] = {"stale_rank": best_rank(score, stale),
                             "cur_rank": best_rank(score, cur)}
            upd_rows.append(row)
        elif ev:
            row = {"qid": it["question_id"], "type": it["question_type"],
                   "base_hits": ev_hits_at_k(base),
                   "k8_hits": ev_hits_at_k(k8),
                   "rec_hits": ev_hits_at_k(rec)}
            non_rows.append(row)

    def inv(rows, arm):
        return sum(1 for r in rows if r[arm]["stale_rank"] < r[arm]["cur_rank"])

    agg = {
        "update_items": len(upd_rows),
        "inversions_base": inv(upd_rows, "base"),
        "inversions_k8": inv(upd_rows, "k8"),
        "inversions_recency": inv(upd_rows, "rec"),
        "nonupdate_items": len(non_rows),
        "nonupdate_mean_hits_base": float(np.mean([r["base_hits"] for r in non_rows])),
        "nonupdate_mean_hits_k8": float(np.mean([r["k8_hits"] for r in non_rows])),
        "nonupdate_mean_hits_recency": float(np.mean([r["rec_hits"] for r in non_rows])),
        "nonupdate_items_hurt_by_k8": sum(1 for r in non_rows if r["k8_hits"] < r["base_hits"]),
        "nonupdate_items_helped_by_k8": sum(1 for r in non_rows if r["k8_hits"] > r["base_hits"]),
        "nonupdate_items_hurt_by_recency": sum(1 for r in non_rows if r["rec_hits"] < r["base_hits"]),
    }
    out = Path(__file__).parent / "falsifier_k8_results.json"
    out.write_text(json.dumps({"config": {"K": K, "tau": TAU, "gamma": GAMMA,
                                          "min_gap_days": MIN_GAP_DAYS},
                               "aggregate": agg,
                               "update_rows": upd_rows,
                               "nonupdate_rows": non_rows}, indent=2),
                   encoding="utf-8")
    print(json.dumps(agg, indent=2))

if __name__ == "__main__":
    main()
