"""Mechanism-attribution check (v004, workbench): are update (current)
evidence units systematically more elliptical / lexically detached from
the query than the initial (stale) statements?

For each of the 14 W-bucket knowledge-update items, compare the stale
session's best-matching unit vs the current session's best-matching unit:
  - query-cosine gap (already known: stale wins)
  - unit length (chars)
  - lexical overlap with the query (content-word Jaccard)
  - lexical overlap with the STALE best unit (does current depend on the
    old statement's vocabulary?)

Prediction under the ellipsis hypothesis: current best units have LOWER
query lexical overlap and SHORTER length than stale best units in the
inversion cases.
"""
import json
import re
from datetime import datetime
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

W_FILE = Path(r"D:\Desktop\crl\20260726_1640_run02\data_split_commitment_v002\longmemeval_s_WORKBENCH.json")
STOP = set("""a an the is are was were be been being do does did have has had i you he she it we
they my your his her its our their me him them this that these those of in on at to for with
about as by from up down out over under again then once and or but if so not no yes what which
who whom when where why how all any both each few more most other some such only own same than
too very can will just should now""".split())

def words(t: str) -> set:
    return {w for w in re.findall(r"[a-z']+", t.lower()) if w not in STOP}

def parse_date(s: str) -> datetime:
    return datetime.strptime(s.split(" (")[0], "%Y/%m/%d")

def main() -> None:
    data = json.loads(W_FILE.read_bytes().decode("utf-8"))
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                device="cuda")
    rows = []
    for it in data:
        if it["question_type"] != "knowledge-update":
            continue
        sess_ids = it["haystack_session_ids"]
        dates = {s: parse_date(d) for s, d in
                 zip(sess_ids, it["haystack_dates"])}
        ev = [s for s in it["answer_session_ids"] if s in dates]
        if len(ev) < 2:
            continue
        ev_sorted = sorted(ev, key=lambda s: dates[s])
        stale, cur = ev_sorted[0], ev_sorted[-1]
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
        qw = words(it["question"])

        def best_unit(sess):
            idxs = [i for i in range(len(units)) if unit_sess[i] == sess]
            b = max(idxs, key=lambda i: sims[i])
            return b

        bs, bc = best_unit(stale), best_unit(cur)
        sw, cw = words(units[bs]), words(units[bc])
        row = {
            "qid": it["question_id"],
            "inverted": bool(sims[bs] > sims[bc]),
            "sim_stale": round(float(sims[bs]), 4),
            "sim_cur": round(float(sims[bc]), 4),
            "len_stale": len(units[bs]),
            "len_cur": len(units[bc]),
            "q_overlap_stale": round(len(qw & sw) / max(1, len(qw)), 3),
            "q_overlap_cur": round(len(qw & cw) / max(1, len(qw)), 3),
            "cur_vocab_in_stale": round(len(cw & sw) / max(1, len(cw)), 3),
        }
        rows.append(row)

    inv = [r for r in rows if r["inverted"]]
    agg = {
        "items": len(rows),
        "inverted_items": len(inv),
        "mean_len_stale_inv": float(np.mean([r["len_stale"] for r in inv])),
        "mean_len_cur_inv": float(np.mean([r["len_cur"] for r in inv])),
        "mean_q_overlap_stale_inv": float(np.mean([r["q_overlap_stale"] for r in inv])),
        "mean_q_overlap_cur_inv": float(np.mean([r["q_overlap_cur"] for r in inv])),
        "items_cur_shorter": sum(1 for r in inv if r["len_cur"] < r["len_stale"]),
        "items_cur_lower_q_overlap": sum(
            1 for r in inv if r["q_overlap_cur"] < r["q_overlap_stale"]),
    }
    out = Path(__file__).parent / "ellipsis_hypothesis_results.json"
    out.write_text(json.dumps({"aggregate": agg, "rows": rows}, indent=2),
                   encoding="utf-8")
    print(json.dumps(agg, indent=2))
    for r in rows:
        print(r["qid"], "inv" if r["inverted"] else "ok ",
              "sim", r["sim_stale"], r["sim_cur"],
              "len", r["len_stale"], r["len_cur"],
              "qOv", r["q_overlap_stale"], r["q_overlap_cur"])

if __name__ == "__main__":
    main()
