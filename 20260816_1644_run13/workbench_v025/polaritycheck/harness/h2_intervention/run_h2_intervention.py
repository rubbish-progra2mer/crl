"""H2 intervention demo (the §7 repair study) — pre-registered before the run.

Selection/evaluation separation: every parameter (I1's cosine threshold, I2/I3's logistic
weights, feature standardization) is fit ONLY on the factorial-pilot corpus, frozen, then
applied ONCE to the guard-stack corpora. Nothing is refit after a guard-stack number exists.

Arms (bars and predictions live in the pre-registration, not here):
  I1  mxbai, cosine-only "fire if cosine < c"          (predicted to FAIL: P1)
  I2  mxbai, logistic on (cosine, token_jaccard)       (primary; predicted to pass: P2)
  I3  production nomic MRL-256, same rule as I2        (descriptive robustness leg: P3)

Deterministic: no RNG anywhere (logistic is fit by full-batch Newton on a convex loss).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
sys.path.insert(0, str(REPO_ROOT))

from harness.factorial_pilot.lexical import token_jaccard  # noqa: E402
from harness.factorial_pilot.encoders import REGISTRY  # noqa: E402

PILOT_CORPUS = [
    REPO_ROOT / "corpus/distinctness_2x2.jsonl",
    REPO_ROOT / "corpus/constraint_2x2.jsonl",
]
GUARD_IN = REPO_ROOT / "results/guard_stack/guard_stack_corpus_2026-07-26.json"
GUARD_OUT = REPO_ROOT / "results/guard_stack/guard_stack_heldout_2026-07-26.json"
RESULTS = REPO_ROOT / "results" / "h2_intervention" / (
    "h2_intervention_rerun_" + datetime.now(timezone.utc).strftime("%Y-%m-%d") + ".json")

POSITIVE = {"OPPOSITE", "VIOLATION"}  # gate SHOULD fire (meaning changed)


def load_pilot() -> list[dict]:
    rows = []
    for path in PILOT_CORPUS:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    assert len(rows) == 80, f"pilot corpus expected 80 rows, got {len(rows)}"
    return rows


def load_guard(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["rows"]


def pick_encoder(substr: str):
    for enc in REGISTRY:
        if substr in enc.name:
            ok, why = enc.available()
            if not ok:
                raise SystemExit(f"encoder {enc.name} unavailable: {why}")
            return enc
    raise SystemExit(f"no encoder matching {substr!r} in registry")


def balanced_accuracy(fire: np.ndarray, positive: np.ndarray) -> float:
    tpr = float(fire[positive].mean()) if positive.any() else float("nan")
    tnr = float((~fire[~positive]).mean()) if (~positive).any() else float("nan")
    return 0.5 * (tpr + tnr)


def fit_i1_threshold(cos: np.ndarray, positive: np.ndarray) -> float:
    """Best-BA threshold for rule `fire if cosine < c`, grid = midpoints of sorted cosines."""
    order = np.sort(np.unique(cos))
    grid = [(order[i] + order[i + 1]) / 2 for i in range(len(order) - 1)]
    grid = [order[0] - 1e-6, *grid, order[-1] + 1e-6]
    best_c, best_ba = grid[0], -1.0
    for c in grid:
        ba = balanced_accuracy(cos < c, positive)
        if ba > best_ba:
            best_ba, best_c = ba, c
    return float(best_c)


def fit_logistic(X: np.ndarray, y: np.ndarray, iters: int = 200) -> np.ndarray:
    """Plain-numpy Newton's method on unregularized logistic loss. Convex, deterministic."""
    Xb = np.hstack([np.ones((len(X), 1)), X])
    w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-Xb @ w))
        grad = Xb.T @ (p - y)
        W = p * (1 - p)
        H = Xb.T @ (Xb * W[:, None]) + 1e-9 * np.eye(Xb.shape[1])
        step = np.linalg.solve(H, grad)
        w -= step
        if float(np.abs(step).max()) < 1e-10:
            break
    return w


def logistic_p(w: np.ndarray, X: np.ndarray) -> np.ndarray:
    Xb = np.hstack([np.ones((len(X), 1)), X])
    return 1.0 / (1.0 + np.exp(-Xb @ w))


def evaluate(fire: np.ndarray, positive: np.ndarray, classes: list[str]) -> dict:
    per_class: dict[str, dict] = {}
    for cls in sorted(set(classes)):
        idx = np.array([c == cls for c in classes])
        per_class[cls] = {
            "n": int(idx.sum()),
            "fired": int(fire[idx].sum()),
            "rate": round(float(fire[idx].mean()), 4),
        }
    return {
        "n_positive": int(positive.sum()),
        "n_control": int((~positive).sum()),
        "catch_rate": round(float(fire[positive].mean()), 4),
        "false_positive_rate": round(float(fire[~positive].mean()), 4),
        "balanced_accuracy": round(balanced_accuracy(fire, positive), 4),
        "per_class_fire_rate": per_class,
    }


def main() -> None:
    pilot = load_pilot()
    guard_in, guard_out = load_guard(GUARD_IN), load_guard(GUARD_OUT)

    pilot_pairs = [(r["text_a"], r["text_b"]) for r in pilot]
    pilot_pos = np.array([r["decision"] in POSITIVE for r in pilot])
    pilot_jac = np.array([token_jaccard(a, b) for a, b in pilot_pairs])

    sets = {}
    for name, rows in (("in_sample", guard_in), ("held_out", guard_out)):
        pairs = [(r["root"], r["mutated"]) for r in rows]
        sets[name] = {
            "rows": rows,
            "pairs": pairs,
            "positive": np.array([r["mutation_class"] != "faithful_control" for r in rows]),
            "classes": [r["mutation_class"] for r in rows],
            "jaccard": np.array([token_jaccard(a, b) for a, b in pairs]),
        }

    # Baseline sanity check against the frozen per-row production cosines: threshold 0.4 on
    # drift = 1 - cosine never fires (the 0-of-56 result the demo starts from).
    baseline = {}
    for name, s in sets.items():
        drift_fire = np.array([1.0 - r["cosine"]["similarity"] > 0.4 for r in s["rows"]])
        baseline[name] = evaluate(drift_fire, s["positive"], s["classes"])

    out = {
        "experiment": "H2 intervention demo (pre-registered)",
        "preregistration": "committed before the run; bars and predictions in the paper (§7)",
        "date": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "fit_corpus": "factorial_pilot 80 pairs (both tasks); guard-stack never touched during fit",
        "baseline_production_drift_gate_threshold_0.4": baseline,
        "arms": {},
    }

    arm_specs = [
        ("I1_mxbai_cosine_only", "mxbai", "cosine_threshold"),
        ("I2_mxbai_confound_aware", "mxbai", "logistic_cos_jaccard"),
        ("I3_production_confound_aware", "PRODUCTION", "logistic_cos_jaccard"),
    ]
    enc_cache: dict[str, dict] = {}
    for arm_name, enc_key, rule in arm_specs:
        enc = pick_encoder(enc_key)
        if enc_key not in enc_cache:
            enc_cache[enc_key] = {
                "pilot": np.array(enc.cosines(pilot_pairs)),
                **{n: np.array(enc.cosines(s["pairs"])) for n, s in sets.items()},
            }
        cos = enc_cache[enc_key]
        arm: dict = {"encoder": enc.name, "rule": rule}

        if rule == "cosine_threshold":
            c = fit_i1_threshold(cos["pilot"], pilot_pos)
            arm["frozen_threshold"] = round(c, 6)
            arm["fit_balanced_accuracy_on_pilot"] = round(
                balanced_accuracy(cos["pilot"] < c, pilot_pos), 4)
            for name, s in sets.items():
                arm[name] = evaluate(cos[name] < c, s["positive"], s["classes"])
                arm[name]["sensitivity_pm_0.05"] = {
                    f"{c + d:+.3f}": round(balanced_accuracy(cos[name] < c + d, s["positive"]), 4)
                    for d in (-0.05, 0.05)
                }
        else:
            Xp = np.column_stack([cos["pilot"], pilot_jac])
            mu, sd = Xp.mean(axis=0), Xp.std(axis=0)
            w = fit_logistic((Xp - mu) / sd, pilot_pos.astype(float))
            arm["frozen_standardization"] = {"mean": mu.round(6).tolist(), "std": sd.round(6).tolist()}
            arm["frozen_weights_bias_cos_jac"] = w.round(6).tolist()
            arm["fit_balanced_accuracy_on_pilot"] = round(
                balanced_accuracy(logistic_p(w, (Xp - mu) / sd) >= 0.5, pilot_pos), 4)
            for name, s in sets.items():
                X = (np.column_stack([cos[name], s["jaccard"]]) - mu) / sd
                p = logistic_p(w, X)
                arm[name] = evaluate(p >= 0.5, s["positive"], s["classes"])
                arm[name]["sensitivity_p_cut"] = {
                    f"{cut:.2f}": round(balanced_accuracy(p >= cut, s["positive"]), 4)
                    for cut in (0.45, 0.55)
                }
        out["arms"][arm_name] = arm
        print(f"{arm_name}: in_sample BA {arm['in_sample']['balanced_accuracy']}"
              f" | held_out BA {arm['held_out']['balanced_accuracy']}")

    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"frozen -> {RESULTS}")


if __name__ == "__main__":
    main()
