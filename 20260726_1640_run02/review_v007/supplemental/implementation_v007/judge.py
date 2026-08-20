"""Frozen judge for the v006 reader raw data (v007 record repair).

argv: <reader_raw.jsonl> <out_verdict_table.jsonl>

Deterministic: auto-scorer (normalized substring + 0.8 content-word
overlap) plus the EXPLICIT manual-equivalence correction list adjudicated
by the Main Codex and independently re-adjudicated by Reviewers 1 and 3
(review_v006). Incorporates the decision_v006 correction: 031748ae_abs /
turn_topk does NOT abstain and is scored INCORRECT (turn total 29/37,
not 30/37; 11 manual verdicts changed, not 12).
"""
import json
import re
import sys
from pathlib import Path

STOPS = {"the", "a", "an", "of", "to", "in", "per", "each", "week",
         "times", "time", "or"}

# (qid, arm) pairs adjudicated CORRECT by manual equivalence review.
MANUAL_CORRECT = {
    ("6a1eabeb", "turn_topk"), ("6a1eabeb", "sentence_topk"), ("6a1eabeb", "oracle_current"),
    ("89941a93", "turn_topk"), ("89941a93", "sentence_topk"), ("89941a93", "oracle_current"),
    ("a1eacc2a", "turn_topk"), ("a1eacc2a", "sentence_topk"), ("a1eacc2a", "oracle_current"),
    ("e493bb7c", "turn_topk"), ("e493bb7c", "sentence_topk"), ("e493bb7c", "oracle_current"),
    ("5c40ec5b", "turn_topk"), ("5c40ec5b", "sentence_topk"), ("5c40ec5b", "oracle_current"),
    ("8fb83627", "sentence_topk"),
    ("07741c45", "oracle_current"),
    # Abstention items: correct information-not-available responses.
    # 031748ae_abs turn_topk EXCLUDED per decision_v006 (it answered
    # substantively about the wrong role; incorrect).
    ("031748ae_abs", "sentence_topk"), ("031748ae_abs", "oracle_current"),
    ("2698e78f_abs", "turn_topk"), ("2698e78f_abs", "sentence_topk"), ("2698e78f_abs", "oracle_current"),
    ("0ddfec37_abs", "turn_topk"), ("0ddfec37_abs", "sentence_topk"), ("0ddfec37_abs", "oracle_current"),
    ("f685340e_abs", "turn_topk"), ("f685340e_abs", "sentence_topk"), ("f685340e_abs", "oracle_current"),
}

def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", str(s).lower()).split()

def auto_match(ans, gold):
    if not ans:
        return False
    a, g = " ".join(norm(ans)), " ".join(norm(gold))
    if g in a:
        return True
    gw = set(norm(gold)) - STOPS
    aw = set(norm(ans))
    return bool(gw) and len(gw & aw) / len(gw) >= 0.8

def main():
    rows = [json.loads(l) for l in
            Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
    out = Path(sys.argv[2])
    table, totals = [], {}
    for r in rows:
        auto = auto_match((r.get("answer") or "").strip(), r["gold"])
        manual = (r["qid"], r["arm"]) in MANUAL_CORRECT
        final = auto or manual
        table.append({"qid": r["qid"], "arm": r["arm"], "auto": auto,
                      "manual_correction": manual and not auto,
                      "final": final, "gold": r["gold"],
                      "answer": r.get("answer")})
        totals.setdefault(r["arm"], [0, 0])
        totals[r["arm"]][1] += 1
        if final:
            totals[r["arm"]][0] += 1
    with out.open("w", encoding="utf-8") as f:
        for t in table:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    print(json.dumps({k: f"{v[0]}/{v[1]}" for k, v in totals.items()},
                     indent=2))

if __name__ == "__main__":
    main()
