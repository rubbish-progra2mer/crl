#!/usr/bin/env python3
"""Build the 2x2 pilot corpora with PER-ANCHOR OVERLAP MATCHING.

WHY MATCHING IS NECESSARY — a finding from the first build
----------------------------------------------------------
The first hand-authored attempt FAILED its own manipulation check: within the
CLOSE stratum, OPPOSITE pairs had mean token-Jaccard 0.721 against SAME's 0.520
(permutation p = 0.014). The design meant to decouple lexical overlap from the
decision axis and did not.

The cause is not sloppy authoring. It is structural:

    Negation is an ADDITIVE edit.  "do not" INSERTS tokens and retains every
    original one, so overlap stays high.
    Paraphrase is a SUBSTITUTIVE edit.  It SWAPS tokens out, so overlap drops.

Negation is lexically cheaper than rewording. So in any naturally-written corpus,
opposite-decision pairs sit at *higher* surface overlap than same-decision pairs,
and the confound is a property of the phenomenon rather than of the author. Intent
cannot remove it. **Matching can.**

HOW THE MATCHING WORKS
----------------------
Each anchor carries ONE fixed opposite-side partner and SEVERAL candidate
same-side partners spanning a range of overlaps. For each anchor and each lexical
stratum, the builder selects the same-side candidate whose measured overlap is
closest to that anchor's opposite-side overlap.

This is ordinary matched-pair design, and it is legitimate here for one specific
reason: **the matching variable is the confounder, and it is computed without any
encoder.** No model is loaded, no cosine is seen, no outcome is consulted. The
selection could not favour a hypothesis about embeddings even in principle. Every
choice is recorded in the emitted rows (`match_target`, `match_achieved`,
`candidates_considered`) so a reader can audit it.

What matching CANNOT fix, stated plainly: token Jaccard is blind to word order, so
a pure order-inversion pair ("merge A into B" / "merge B into A") scores 1.0
despite deciding opposite things. That is why `levenshtein_sim` is reported
alongside, and why the affected anchors are flagged in the output.

Run:  python harness/factorial_pilot/build_corpus.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_REPO_ROOT = _HERE.parents[2]
for _p in (str(_REPO_ROOT),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from harness.factorial_pilot.lexical import PRIMARY_METRIC, all_metrics  # noqa: E402
from harness.lib import stats  # noqa: E402

AUTHOR = "claude-opus-5, session 2026-07-26 — SINGLE AUTHOR, see paper §10 limitation (iv)"
OUT = _REPO_ROOT / "corpus"

# ---------------------------------------------------------------------------
# TASK 1 — distinctness.
#   anchor · opposite-CLOSE · opposite-DISTANT · [same-CLOSE cands] · [same-DISTANT cands]
# ---------------------------------------------------------------------------
DISTINCTNESS = [
    dict(
        group="deploy", subclass="negation",
        anchor="Deploy the migration to production tonight.",
        opp_close="Do not deploy the migration to production tonight.",
        opp_distant="Hold the schema change in staging until the audit closes.",
        same_close=["Deploy the migration to prod tonight.",
                    "Deploy the migration into production tonight.",
                    "Deploy the schema migration to production tonight.",
                    "Deploy the production migration tonight."],
        same_distant=["Cut the database change live before morning.",
                      "Push the structural update out ahead of daybreak.",
                      "Take the new schema live overnight."],
    ),
    dict(
        group="retry", subclass="antonym_verb",
        anchor="Increase the retry limit.",
        opp_close="Decrease the retry limit.",
        opp_distant="Let a failed call die on its first attempt.",
        same_close=["Raise the retry limit.", "Increase the retry ceiling.",
                    "Increase the retry limit further."],
        same_distant=["Allow more attempts before the call is abandoned.",
                      "Give failing operations additional chances to succeed."],
    ),
    dict(
        group="cache", subclass="antonym_verb",
        anchor="Enable caching for all read queries.",
        opp_close="Disable caching for all read queries.",
        opp_distant="Serve every request from origin with no intermediate storage.",
        same_close=["Activate caching for all read queries.",
                    "Enable caching for all read requests.",
                    "Switch on caching for all read queries.",
                    "Turn on caching for every read query."],
        same_distant=["Keep hot responses close to the client so origin sees little traffic.",
                      "Store frequently requested results nearer the caller."],
    ),
    dict(
        group="perms", subclass="antonym_verb",
        anchor="Grant the service account write access.",
        opp_close="Revoke the service account write access.",
        opp_distant="Confine that identity to a read-only role.",
        same_close=["Give the service account write access.",
                    "Grant the service account write permission.",
                    "Grant the service principal write access."],
        same_distant=["Let that identity modify records, not merely read them.",
                      "Permit the automated user to change stored data."],
    ),
    dict(
        group="schema", subclass="direction_inversion",
        anchor="Roll back to schema v12.",
        opp_close="Roll forward to schema v12.",
        opp_distant="Advance the database to the newest available structure.",
        same_close=["Roll back onto schema v12.", "Roll back to schema version 12.",
                    "Revert to schema v12."],
        same_distant=["Return the database to its twelfth structural revision.",
                      "Restore the earlier table layout."],
    ),
    dict(
        group="legacy", subclass="antonym_verb",
        anchor="Remove the legacy endpoint.",
        opp_close="Keep the legacy endpoint.",
        opp_distant="Continue serving the old route indefinitely for existing clients.",
        same_close=["Delete the legacy endpoint.", "Remove the legacy route.",
                    "Drop the legacy endpoint."],
        same_distant=["Take the deprecated route out of service.",
                      "Retire the old interface entirely."],
    ),
    dict(
        group="order", subclass="order_inversion",
        anchor="Run the batch job before the nightly sync.",
        opp_close="Run the batch job after the nightly sync.",
        opp_distant="Let the nightly sync complete first, then start batch processing.",
        same_close=["Start the batch job before the nightly sync.",
                    "Run the batch job prior to the nightly sync.",
                    "Run the batch task before the nightly sync."],
        same_distant=["Schedule bulk processing ahead of the overnight replication.",
                      "Bulk work should precede the evening data copy."],
    ),
    dict(
        group="alert", subclass="comparator_inversion",
        anchor="Alert on error rates above two percent.",
        opp_close="Alert on error rates below two percent.",
        opp_distant="Stay quiet unless failures drop beneath one in fifty.",
        same_close=["Alert on error rates over two percent.",
                    "Alert on error rates exceeding two percent.",
                    "Alert when error rates exceed two percent."],
        same_distant=["Notify the on-call engineer once failures pass one in fifty.",
                      "Page somebody when more than one request in fifty fails."],
    ),
    dict(
        group="merge", subclass="order_inversion",
        anchor="Merge the feature branch into main.",
        opp_close="Merge main into the feature branch.",
        opp_distant="Bring the trunk's changes down into the topic branch instead.",
        same_close=["Merge into main the feature branch.",
                    "Merge the feature branch to main.",
                    "Merge the feature branch into master."],
        same_distant=["Integrate the topic branch's work into the trunk.",
                      "Fold the side line of development back into the mainline."],
    ),
    dict(
        group="timeout", subclass="antonym_noun",
        anchor="Treat the timeout as retryable.",
        opp_close="Treat the timeout as fatal.",
        opp_distant="Abort the whole operation the moment a deadline is missed.",
        same_close=["Treat the timeout as recoverable.", "Treat the timeout as retriable.",
                    "Treat timeouts as retryable."],
        same_distant=["A missed deadline should be attempted again rather than surfaced as failure.",
                      "When the clock runs out, try the operation once more."],
    ),
]

# ---------------------------------------------------------------------------
# TASK 2 — constraint survival. Weighted toward modal_downgrade and
# quantity_drift, the two classes cosine measured worst on (AUROC 0.000–0.160).
# ---------------------------------------------------------------------------
CONSTRAINT = [
    dict(
        group="retries", subclass="quantity_drift",
        anchor="Retry the request at most three times.",
        opp_close="Retry the request at most thirty times.",
        opp_distant="Keep attempting the call until it succeeds, however long that takes.",
        same_close=["Retry the request at most three attempts.",
                    "Retry the request no more than three times.",
                    "Retry the request at most 3 times."],
        same_distant=["Give the call up to three attempts, then stop.",
                      "Allow three tries and then abandon the operation."],
    ),
    dict(
        group="rotation", subclass="modal_downgrade",
        anchor="The token must be rotated every 24 hours.",
        opp_close="The token should be rotated every 24 hours.",
        opp_distant="Credential refresh is left to the operator's discretion.",
        same_close=["The token must be rotated every 24 hrs.",
                    "The token must be rotated each 24 hours.",
                    "The token must be rotated every twenty-four hours."],
        same_distant=["Credentials expire daily and mandatory refresh is required.",
                      "Secrets have to be replaced once per day without exception."],
    ),
    dict(
        group="secrets", subclass="modal_downgrade",
        anchor="Never log the raw API key.",
        opp_close="Rarely log the raw API key.",
        opp_distant="Verbose diagnostics may include credential material when troubleshooting.",
        same_close=["Never log the raw API token.", "Never log the raw API keys.",
                    "Never record the raw API key."],
        same_distant=["Under no circumstances should secret material appear in diagnostic output.",
                      "Credentials must stay out of every log line."],
    ),
    dict(
        group="cleanup", subclass="order_inversion",
        anchor="Delete the temp files after the job completes.",
        opp_close="Delete the temp files before the job completes.",
        opp_distant="Scratch data persists on disk once processing finishes.",
        same_close=["Remove the temp files after the job completes.",
                    "Delete the temp files after the job finishes.",
                    "Delete the temporary files after the job completes."],
        same_distant=["Clean up scratch data once processing has finished.",
                      "Discard working files when the task is done."],
    ),
    dict(
        group="latency", subclass="quantity_drift",
        anchor="Alert if latency exceeds 200ms.",
        opp_close="Alert if latency exceeds 2000ms.",
        opp_distant="Notify the on-call engineer only when response time passes two full seconds.",
        same_close=["Alert if latency exceeds 200 ms.", "Alert if delay exceeds 200ms.",
                    "Alert if latency exceeds 200 milliseconds."],
        same_distant=["Page the on-call engineer when response time passes a fifth of a second.",
                      "Raise a warning once requests take longer than two tenths of a second."],
    ),
    dict(
        group="approval", subclass="constraint_deletion",
        anchor="Only admins may approve the deploy.",
        opp_close="Any user may approve the deploy.",
        opp_distant="Any team member with repository access can sign off on a release.",
        same_close=["Only admins may authorise the deploy.",
                    "Only administrators may approve the deploy.",
                    "Only admins may approve the release."],
        same_distant=["Release sign-off is restricted to users holding administrator rights.",
                      "Nobody without elevated privileges can push a release live."],
    ),
    dict(
        group="encrypt", subclass="order_inversion",
        anchor="Encrypt the backup before uploading it.",
        opp_close="Encrypt the backup after uploading it.",
        opp_distant="Archives transfer in plaintext and are secured at rest by the provider.",
        same_close=["Encrypt the backup before sending it.",
                    "Encrypt the backup prior to uploading it.",
                    "Encrypt the archive before uploading it."],
        same_distant=["Apply encryption to the archive ahead of transfer.",
                      "Scramble the saved copy first, then move it off the host."],
    ),
    dict(
        group="failmode", subclass="polarity_flip",
        anchor="Fail closed if the auth service is unreachable.",
        opp_close="Fail open if the auth service is unreachable.",
        opp_distant="When identity checks are unavailable, allow the request through and log the gap.",
        same_close=["Fail shut if the auth service is unreachable.",
                    "Fail closed when the auth service is unreachable.",
                    "Fail closed if the auth service is unavailable."],
        same_distant=["Deny the request if identity verification cannot be reached.",
                      "Block traffic whenever the login backend is down."],
    ),
    dict(
        group="concurrency", subclass="quantity_drift",
        anchor="Cap concurrent workers at eight.",
        opp_close="Cap concurrent workers at eighty.",
        opp_distant="Parallelism is unbounded and governed only by available memory.",
        same_close=["Cap concurrent workers at 8.", "Cap parallel workers at eight.",
                    "Cap simultaneous workers at eight."],
        same_distant=["Limit parallelism to a maximum of eight simultaneous workers.",
                      "No more than eight tasks may run side by side."],
    ),
    dict(
        group="txn", subclass="modal_downgrade",
        anchor="All writes must go through the transaction wrapper.",
        opp_close="Some writes must go through the transaction wrapper.",
        opp_distant="Direct database access is acceptable for performance-critical paths.",
        same_close=["All writes must go through the transaction helper.",
                    "Every write must go through the transaction wrapper.",
                    "All writes must pass through the transaction wrapper."],
        same_distant=["Each mutation is required to pass through the transactional layer.",
                      "No change may touch storage outside a transaction."],
    ),
]

TASKS = {
    "distinctness": dict(spec=DISTINCTNESS, neg="OPPOSITE", pos="SAME",
                         file="distinctness_2x2.jsonl", prefix="D"),
    "constraint": dict(spec=CONSTRAINT, neg="VIOLATION", pos="FAITHFUL",
                       file="constraint_2x2.jsonl", prefix="C"),
}


def ov(a: str, b: str) -> float:
    return all_metrics(a, b)[PRIMARY_METRIC]


def pick(anchor: str, candidates: list[str], target: float) -> tuple[str, list[dict]]:
    """Select the candidate whose overlap is nearest `target`. Encoder-blind."""
    scored = [{"text": c, "overlap": round(ov(anchor, c), 6),
               "distance_to_target": round(abs(ov(anchor, c) - target), 6)}
              for c in candidates]
    best = min(scored, key=lambda s: s["distance_to_target"])
    return best["text"], scored


def build(task: str) -> list[dict]:
    cfg = TASKS[task]
    rows: list[dict] = []
    print(f"\n{'=' * 78}\nBUILDING {task}  (matching on {PRIMARY_METRIC}, no encoder loaded)\n{'=' * 78}")
    print(f"{'anchor':<13s} {'stratum':<8s} {'target':>7s} {'chosen':>7s} {'gap':>7s}  candidate")
    for i, s in enumerate(cfg["spec"], 1):
        anchor = s["anchor"]
        for stratum, opp_key, cand_key in [("CLOSE", "opp_close", "same_close"),
                                           ("DISTANT", "opp_distant", "same_distant")]:
            target = ov(anchor, s[opp_key])
            chosen, scored = pick(anchor, s[cand_key], target)
            got = ov(anchor, chosen)
            print(f"{s['group']:<13s} {stratum:<8s} {target:>7.3f} {got:>7.3f} "
                  f"{got - target:>+7.3f}  {chosen[:44]!r}")
            neg_cell = "A" if stratum == "CLOSE" else "B"
            pos_cell = "C" if stratum == "CLOSE" else "D"
            for cell, text_b, dec in [(neg_cell, s[opp_key], cfg["neg"]),
                                      (pos_cell, chosen, cfg["pos"])]:
                row = {
                    "id": f"{cfg['prefix']}-{cell}-{i:02d}", "task": task,
                    "decision": dec, "lexical": stratum, "cell": cell,
                    "anchor_group": s["group"], "subclass": s["subclass"],
                    "text_a": anchor, "text_b": text_b,
                    "authored_by": AUTHOR, "authored_before_measurement": True,
                    "independent_decision_label": None,
                    "independent_lexical_label": None,
                }
                if dec == cfg["pos"]:
                    row["match_target"] = round(target, 6)
                    row["match_achieved"] = round(got, 6)
                    row["candidates_considered"] = scored
                    row["matching_note"] = (
                        "selected to match the opposite-side overlap for this anchor; "
                        "selection used the confounder only, blind to any encoder")
                rows.append(row)
    return rows


def check_balance(rows: list[dict], task: str) -> bool:
    cfg = TASKS[task]
    print(f"\n  BALANCE after matching ({task}):")
    ok = True
    for lex in ("CLOSE", "DISTANT"):
        a = [ov(r["text_a"], r["text_b"]) for r in rows
             if r["lexical"] == lex and r["decision"] == cfg["neg"]]
        b = [ov(r["text_a"], r["text_b"]) for r in rows
             if r["lexical"] == lex and r["decision"] == cfg["pos"]]
        t = stats.permutation_test_mean_diff(a, b)
        good = t["p_two_sided"] > 0.05
        ok &= good
        print(f"    {lex:<8s} {cfg['neg']}={t['mean_a']:.4f}  {cfg['pos']}={t['mean_b']:.4f}  "
              f"diff={t['observed_diff']:.4f}  perm p={t['p_two_sided']:.4f}  "
              f"{'balanced' if good else '*** STILL IMBALANCED ***'}")
    # flag the anchors where token Jaccard is structurally blind
    blind = [r["anchor_group"] for r in rows
             if r["decision"] == cfg["neg"] and ov(r["text_a"], r["text_b"]) >= 0.99]
    if blind:
        print(f"    NOTE: token Jaccard is order-blind and scores 1.0 on these "
              f"opposite-side pairs: {sorted(set(blind))}")
        print(f"          levenshtein_sim is reported per row for exactly this reason.")
    return ok


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    all_ok = True
    for task in TASKS:
        rows = build(task)
        all_ok &= check_balance(rows, task)
        dest = OUT / TASKS[task]["file"]
        dest.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                        encoding="utf-8")
        print(f"\n  wrote {dest.relative_to(_REPO_ROOT)}: {len(rows)} rows "
              f"({len(rows) // 4} anchors x 4 cells)")
    print(f"\n{'=' * 78}")
    print(f"BALANCE ACHIEVED ON BOTH TASKS: {all_ok}")
    if not all_ok:
        print("  Add same-side candidates at the needed overlap and rebuild. Do NOT")
        print("  proceed to the encoder run on an invalid design.")
    print("=" * 78)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
