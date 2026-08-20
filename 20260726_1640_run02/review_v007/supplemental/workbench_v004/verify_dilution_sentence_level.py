"""Dilution-mechanism verification (v004 workbench): does sentence-level
indexing remove the stale-over-current inversion that turn-level
indexing exhibits?

Same 14 W-bucket knowledge-update items; same encoder; only the unit
changes: sentences (regex split, min 15 chars) instead of turns.
Prediction under the dilution mechanism: inversions drop substantially
(current's update sentence, no longer averaged with surrounding content,
matches the query); under the ellipsis/vocabulary account they stay.
"""
import json
import re
from datetime import datetime
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

W_FILE = Path(r"D:\Desktop\crl\20260726_1640_run02\data_split_commitment_v002\longmemeval_s_WORKBENCH.json")

def parse_date(s: str) -> datetime:
    return datetime.strptime(s.split(" (")[0], "%Y/%m/%d")

def sentences(t: str):
    parts = re.split(r"(?<=[.!?])\s+|\n+", t)
    return [p.strip() for p in parts if len(p.strip()) >= 15]

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

        for unit_kind in ("turn", "sentence"):
            units, unit_sess = [], []
            for sid, sess in zip(sess_ids, it["haystack_sessions"]):
                for turn in sess:
                    txt = turn["content"].strip()
                    if not txt:
                        continue
                    if unit_kind == "turn":
                        units.append(txt[:1000]); unit_sess.append(sid)
                    else:
                        for s_ in sentences(txt):
                            units.append(s_[:300]); unit_sess.append(sid)
            emb = model.encode(units, batch_size=512, convert_to_numpy=True,
                               normalize_embeddings=True,
                               show_progress_bar=False)
            qv = model.encode([it["question"]], convert_to_numpy=True,
                              normalize_embeddings=True)[0]
            sims = emb @ qv

            def best(sess):
                idxs = [i for i in range(len(units)) if unit_sess[i] == sess]
                return max(float(sims[i]) for i in idxs)

            s_sim, c_sim = best(stale), best(cur)
            rows.append({"qid": it["question_id"], "unit": unit_kind,
                         "n_units": len(units),
                         "sim_stale": round(s_sim, 4),
                         "sim_cur": round(c_sim, 4),
                         "inverted": bool(s_sim > c_sim)})

    by_kind = {}
    for kind in ("turn", "sentence"):
        ks = [r for r in rows if r["unit"] == kind]
        by_kind[kind] = {
            "items": len(ks),
            "inversions": sum(1 for r in ks if r["inverted"]),
            "mean_margin_cur_minus_stale": float(np.mean(
                [r["sim_cur"] - r["sim_stale"] for r in ks])),
        }
    out = Path(__file__).parent / "dilution_sentence_results.json"
    out.write_text(json.dumps({"aggregate": by_kind, "rows": rows}, indent=2),
                   encoding="utf-8")
    print(json.dumps(by_kind, indent=2))
    for r in rows:
        if r["unit"] == "sentence":
            print(r["qid"], "sent-level sim stale/cur:",
                  r["sim_stale"], r["sim_cur"],
                  "INVERTED" if r["inverted"] else "fixed-or-ok")

if __name__ == "__main__":
    main()
