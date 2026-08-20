"""Workbench decisive falsifier for kernel K11 (run02 v004).

K11: query-anchored competitive-band temporal arbitration.
Detection signal is NOT store-side unit-unit similarity (K8, refuted) but
co-presence in the query's competitive relevance band: units scoring
within MARGIN of the top score, from different sessions with >= 1 day
gap, are treated as candidate versions of the same contested slot; band
members not from the newest banded session are attenuated by GAMMA.
Units outside the band are never touched (this is the predicted fix for
global recency's 29/79 collateral harm).

Preregistered defaults, no tuning loop:
  MARGIN = 0.05 (cosine), GAMMA = 0.5, MIN_GAP_DAYS = 1, K = 10.

Preregistered kill conditions:
  (a) repairs fewer than 5 of the 9 base inversions on W-bucket
      knowledge-update items (i.e. fails to approach the recency arm's
      7/9 repair), OR
  (b) harms non-update items at the same order as global recency
      (>= 10 of 79 items with reduced evidence hits).

W bucket only (physically separated file). Local compute only.
"""
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

W_FILE = Path(r"D:\Desktop\crl\20260726_1640_run02\data_split_commitment_v002\longmemeval_s_WORKBENCH.json")
K = 10
MARGIN = 0.05
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

        # K11 arm: competitive-band temporal arbitration
        k11 = base.copy()
        top = float(base.max())
        band = np.where(base >= top - MARGIN)[0]
        band_sessions = {unit_sess[i] for i in band}
        if len(band_sessions) > 1:
            band_dates = {s: dates[s] for s in band_sessions}
            newest = max(band_dates.values())
            eligible = {s for s, d in band_dates.items()
                        if (newest - d).days >= MIN_GAP_DAYS}
            if eligible and any((newest - d).days >= MIN_GAP_DAYS
                                for d in band_dates.values()):
                for i in band:
                    if (newest - dates[unit_sess[i]]).days >= MIN_GAP_DAYS:
                        k11[i] = base[i] * GAMMA

        ev = [s for s in it["answer_session_ids"] if s in dates]

        def best_rank(score, sess):
            order = np.argsort(-score)
            for rank, idx in enumerate(order):
                if unit_sess[idx] == sess:
                    return int(rank)
            return n

        def ev_hits_at_k(score):
            topk = np.argsort(-score)[:K]
            return sum(1 for i in topk if unit_sess[i] in ev)

        if it["question_type"] == "knowledge-update" and len(ev) >= 2:
            ev_sorted = sorted(ev, key=lambda s: dates[s])
            stale, cur = ev_sorted[0], ev_sorted[-1]
            row = {"qid": it["question_id"],
                   "band_size": int(len(band)),
                   "band_sessions": len(band_sessions)}
            for name, score in (("base", base), ("k11", k11)):
                row[name] = {"stale_rank": best_rank(score, stale),
                             "cur_rank": best_rank(score, cur)}
            upd_rows.append(row)
        elif ev:
            non_rows.append({"qid": it["question_id"],
                             "type": it["question_type"],
                             "base_hits": ev_hits_at_k(base),
                             "k11_hits": ev_hits_at_k(k11)})

    def inv(rows, arm):
        return sum(1 for r in rows if r[arm]["stale_rank"] < r[arm]["cur_rank"])

    agg = {
        "update_items": len(upd_rows),
        "inversions_base": inv(upd_rows, "base"),
        "inversions_k11": inv(upd_rows, "k11"),
        "nonupdate_items": len(non_rows),
        "nonupdate_mean_hits_base": float(np.mean([r["base_hits"] for r in non_rows])),
        "nonupdate_mean_hits_k11": float(np.mean([r["k11_hits"] for r in non_rows])),
        "nonupdate_items_hurt_by_k11": sum(
            1 for r in non_rows if r["k11_hits"] < r["base_hits"]),
        "nonupdate_items_helped_by_k11": sum(
            1 for r in non_rows if r["k11_hits"] > r["base_hits"]),
    }
    out = Path(__file__).parent / "falsifier_k11_results.json"
    out.write_text(json.dumps({"config": {"K": K, "margin": MARGIN,
                                          "gamma": GAMMA,
                                          "min_gap_days": MIN_GAP_DAYS},
                               "aggregate": agg,
                               "update_rows": upd_rows,
                               "nonupdate_rows": non_rows}, indent=2),
                   encoding="utf-8")
    print(json.dumps(agg, indent=2))

if __name__ == "__main__":
    main()
