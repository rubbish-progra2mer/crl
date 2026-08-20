"""Windows-compatible evaluator for Heuresis' BBOB probe.

This preserves the released problem suite, budget wrapper, seeds, and score
formula.  It omits the POSIX-only per-tuple SIGALRM; the calling probe enforces
one subprocess timeout for the complete suite instead.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from problems import BudgetedF, BudgetExhausted, make_problem  # noqa: E402


def _run_one(func_id, instance_id, seed, dim, budget, optimize_fn):
    f_raw, f_opt, bounds = make_problem(func_id, dim, instance_id)
    wrapped = BudgetedF(f_raw, budget=budget, bounds=bounds)
    rng_seed = func_id * 1_000_000 + instance_id * 1_000 + seed
    status = "ok"
    t0 = time.monotonic()
    try:
        optimize_fn(wrapped, dim, bounds, budget, rng_seed)
    except BudgetExhausted:
        status = "budget_exhausted"
    except Exception as exc:
        status = f"error:{type(exc).__name__}"
    duration_s = time.monotonic() - t0
    best_y = wrapped.best_y if np.isfinite(wrapped.best_y) else float("inf")
    return {
        "func_id": func_id,
        "instance_id": instance_id,
        "seed": seed,
        "best_y": best_y,
        "f_opt": f_opt,
        "gap": best_y - f_opt,
        "n_fevals": wrapped.calls,
        "duration_s": duration_s,
        "status": status,
    }


def main():
    root = Path(__file__).resolve().parent
    spec = json.loads((root / "problem_spec.json").read_text(encoding="utf-8"))
    from optimizer import optimize as optimize_fn

    records = []
    total_t0 = time.monotonic()
    for func_id in spec["functions"]:
        for instance_id in spec["instances"]:
            for seed in spec["seeds"]:
                rec = _run_one(
                    int(func_id),
                    int(instance_id),
                    int(seed),
                    int(spec["dim"]),
                    int(spec["budget"]),
                    optimize_fn,
                )
                records.append(rec)
                print(
                    f"func_id={rec['func_id']} instance_id={rec['instance_id']} "
                    f"seed={rec['seed']} best_y={rec['best_y']:.6f} "
                    f"f_opt={rec['f_opt']:.6f} gap={rec['gap']:.6f} "
                    f"n_fevals={rec['n_fevals']} duration_s={rec['duration_s']:.3f} "
                    f"status={rec['status']}",
                    flush=True,
                )

    gaps = np.array([max(rec["gap"], 1e-12) for rec in records])
    log_gaps = np.log10(gaps)
    print("\n---")
    print(f"mean_log_gap: {float(np.mean(log_gaps)):.6f}")
    print(f"median_log_gap: {float(np.median(log_gaps)):.6f}")
    print(f"n_tuples: {len(records)}")
    print(
        "n_errors: "
        f"{sum(rec['status'].startswith('error') for rec in records)}"
    )
    for func_id in sorted({rec["func_id"] for rec in records}):
        mask = np.array([rec["func_id"] == func_id for rec in records])
        print(f"f{func_id}_mean_log_gap: {float(np.mean(log_gaps[mask])):.6f}")
    print(f"total_duration_s: {time.monotonic() - total_t0:.3f}")


if __name__ == "__main__":
    main()
