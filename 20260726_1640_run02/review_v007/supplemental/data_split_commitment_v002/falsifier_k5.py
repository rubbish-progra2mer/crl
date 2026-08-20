"""Workbench decisive falsifier for kernel K5 (run02 v002).

Question: does time-symmetric similarity-graph propagation (PPR) amplify
STALE versions of updated facts into top-k, relative to direct retrieval,
on W-bucket knowledge-update items of LongMemEval-s?

Kill condition: if symmetric PPR does NOT increase stale presence/rank
relative to direct retrieval, kernel K5 dies.

Workbench only: reads W-bucket items exclusively. Local compute only.
Fixed default hyperparameters, no tuning loop.
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

DATA = Path(r"C:\Users\g\.cache\huggingface\hub\datasets--xiaowu0162--longmemeval\snapshots\2ec2a557f339b6c0369619b1ed5793734cc87533\longmemeval_s")
K = 10          # retrieval depth (units)
M = 10          # kNN edges per node
DAMP = 0.5      # PPR damping (HippoRAG-style)
ITERS = 30      # power iterations

def bucket_of(qid: str) -> str:
    m = hashlib.sha256(qid.encode()).digest()[0] % 5
    return "W" if m == 0 else ("D" if m in (1, 2) else "C")

def parse_date(s: str) -> datetime:
    return datetime.strptime(s.split(" (")[0], "%Y/%m/%d")

def main() -> None:
    data = json.loads(DATA.read_bytes().decode("utf-8"))
    items = [
        x for x in data
        if bucket_of(str(x["question_id"])) == "W"
        and x["question_type"] == "knowledge-update"
    ]
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                device="cuda")
    rows = []
    for it in items:
        qid = it["question_id"]
        sess_ids = it["haystack_session_ids"]
        dates = {sid: parse_date(d) for sid, d in
                 zip(sess_ids, it["haystack_dates"])}
        ev_ids = [s for s in it["answer_session_ids"] if s in dates]
        if len(ev_ids) < 2:
            rows.append({"qid": qid, "skip": f"evidence in haystack={len(ev_ids)}"})
            continue
        ev_sorted = sorted(ev_ids, key=lambda s: dates[s])
        stale_sess, current_sess = ev_sorted[0], ev_sorted[-1]

        units, unit_sess = [], []
        for sid, sess in zip(sess_ids, it["haystack_sessions"]):
            for turn in sess:
                txt = turn["content"].strip()
                if txt:
                    units.append(txt[:1000])
                    unit_sess.append(sid)
        emb = model.encode(units, batch_size=256, convert_to_numpy=True,
                           normalize_embeddings=True, show_progress_bar=False)
        qv = model.encode([it["question"]], convert_to_numpy=True,
                          normalize_embeddings=True)[0]
        sims = emb @ qv
        n = len(units)

        # direct arm
        direct_top = np.argsort(-sims)[:K]

        # symmetric kNN graph + PPR arm
        S = emb @ emb.T
        np.fill_diagonal(S, -1.0)
        W = np.zeros((n, n), dtype=np.float32)
        for i in range(n):
            nb = np.argpartition(-S[i], M)[:M]
            W[i, nb] = np.maximum(S[i, nb], 0.0)
        W = np.maximum(W, W.T)                       # symmetric edges
        deg = W.sum(1, keepdims=True); deg[deg == 0] = 1.0
        P = W / deg
        p0 = np.exp(sims / 0.1); p0 /= p0.sum()      # personalization
        r = p0.copy()
        for _ in range(ITERS):
            r = (1 - DAMP) * p0 + DAMP * (P.T @ r)
        ppr_top = np.argsort(-r)[:K]

        def metrics(top):
            cs = [unit_sess[i] for i in top]
            stale_cnt = sum(1 for s in cs if s == stale_sess)
            cur_cnt = sum(1 for s in cs if s == current_sess)
            def best_rank(order, sess):
                for rank, i in enumerate(np.argsort(-order)):
                    if unit_sess[i] == sess:
                        return rank
                return n
            return stale_cnt, cur_cnt

        d_stale, d_cur = metrics(direct_top)
        p_stale, p_cur = metrics(ppr_top)

        def best_rank(score, sess):
            for rank, i in enumerate(np.argsort(-score)):
                if unit_sess[i] == sess:
                    return int(rank)
            return n
        row = {
            "qid": qid, "n_units": n,
            "direct": {"stale@k": d_stale, "cur@k": d_cur,
                       "stale_rank": best_rank(sims, stale_sess),
                       "cur_rank": best_rank(sims, current_sess)},
            "ppr": {"stale@k": p_stale, "cur@k": p_cur,
                    "stale_rank": best_rank(r, stale_sess),
                    "cur_rank": best_rank(r, current_sess)},
        }
        rows.append(row)

    ok = [r for r in rows if "skip" not in r]
    agg = {
        "n_items": len(ok),
        "skipped": [r for r in rows if "skip" in r],
        "direct_mean_stale@k": float(np.mean([r["direct"]["stale@k"] for r in ok])),
        "ppr_mean_stale@k": float(np.mean([r["ppr"]["stale@k"] for r in ok])),
        "direct_mean_cur@k": float(np.mean([r["direct"]["cur@k"] for r in ok])),
        "ppr_mean_cur@k": float(np.mean([r["ppr"]["cur@k"] for r in ok])),
        "items_ppr_stale_above_cur": sum(
            1 for r in ok if r["ppr"]["stale_rank"] < r["ppr"]["cur_rank"]),
        "items_direct_stale_above_cur": sum(
            1 for r in ok if r["direct"]["stale_rank"] < r["direct"]["cur_rank"]),
        "items_ppr_more_stale_than_direct": sum(
            1 for r in ok if r["ppr"]["stale@k"] > r["direct"]["stale@k"]),
        "items_ppr_less_stale_than_direct": sum(
            1 for r in ok if r["ppr"]["stale@k"] < r["direct"]["stale@k"]),
    }
    out = Path(__file__).parent / "falsifier_k5_results.json"
    out.write_text(json.dumps({"config": {"K": K, "M": M, "damp": DAMP,
                                          "iters": ITERS},
                               "aggregate": agg, "rows": rows},
                              indent=2), encoding="utf-8")
    print(json.dumps(agg, indent=2))

if __name__ == "__main__":
    main()
