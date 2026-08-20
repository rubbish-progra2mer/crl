from __future__ import annotations

import argparse
import sys

from .audit import audit
from .logs import from_csv, from_jsonl
from .metrics import (
    bits_over_random,
    bor_ceiling,
    collapse_lambda,
    random_success_at_least_m,
    random_success_at_least_one,
)


def main() -> None:
    argv = sys.argv[1:]
    if argv and argv[0] == "audit":
        _audit_main(argv[1:])
        return
    _calc_main(argv)


def _calc_main(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(
        prog="bor",
        description=(
            "Compute random baselines and Bits-over-Random. "
            "Use 'bor audit <log>' to audit a retrieval log."
        ),
    )
    parser.add_argument("--N", type=int, required=True, help="Corpus size.")
    parser.add_argument("--R", type=int, required=True, help="Relevant items in corpus.")
    parser.add_argument("--K", type=int, required=True, help="Items retrieved.")
    parser.add_argument(
        "--observed",
        type=float,
        required=True,
        help="Observed success rate, e.g. 0.82.",
    )
    parser.add_argument(
        "--m",
        type=int,
        default=1,
        help="Success threshold. Default is at least one relevant item.",
    )

    args = parser.parse_args(argv)

    if args.m == 1:
        p_rand = random_success_at_least_one(args.N, args.R, args.K)
    else:
        p_rand = random_success_at_least_m(args.N, args.R, args.K, args.m)

    bor = bits_over_random(args.observed, p_rand)
    ceiling = bor_ceiling(p_rand)
    lam = collapse_lambda(args.N, args.R, args.K)

    print(f"N: {args.N}")
    print(f"R: {args.R}")
    print(f"K: {args.K}")
    print(f"Observed success: {args.observed:.4f}")
    print(f"Random baseline: {p_rand:.4f}")
    print(f"Bits-over-Random: {bor:.4f}")
    print(f"BoR ceiling: {ceiling:.4f}")
    print(f"lambda: {lam:.4f}")

    if p_rand >= 0.95:
        print("warning: random baseline is already near 1.0")
    if lam >= 3:
        print("warning: lambda is in the collapse zone")


def _audit_main(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(
        prog="bor audit",
        description=(
            "Audit a retrieval log (JSONL or CSV) against blind-draw "
            "baselines. Read-only and local; nothing leaves the machine."
        ),
    )
    parser.add_argument("log", help="Path to the log file.")
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Parse the log as CSV instead of JSONL.",
    )
    parser.add_argument(
        "--map",
        default=None,
        help=(
            "Explicit field mapping, e.g. "
            "'N=pool_size,K=top_k,hit=found,R=num_relevant'."
        ),
    )
    parser.add_argument(
        "--default-R",
        type=int,
        default=None,
        help="Use this relevant count for every row lacking an R field.",
    )
    parser.add_argument(
        "--R-frac",
        type=float,
        default=None,
        help=(
            "Estimate R as round(frac * N) for rows lacking an R field. "
            "Reported as an estimate."
        ),
    )
    parser.add_argument(
        "--bootstrap",
        type=int,
        default=2000,
        help="Bootstrap resamples for the confidence interval.",
    )
    parser.add_argument("--seed", type=int, default=0, help="Bootstrap seed.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on rows with missing fields instead of skipping them.",
    )

    args = parser.parse_args(argv)

    mapping = None
    if args.map:
        mapping = dict(pair.split("=", 1) for pair in args.map.split(","))

    loader = from_csv if args.csv else from_jsonl
    try:
        records = loader(
            args.log,
            mapping=mapping,
            default_R=args.default_R,
            R_frac=args.R_frac,
            strict=args.strict,
        )
    except FileNotFoundError:
        parser.error(f"log file not found: {args.log}")
    except ValueError as e:
        parser.error(str(e))
    result = audit(records, n_bootstrap=args.bootstrap, seed=args.seed)
    print(result.summary())
    if args.R_frac is not None:
        print(
            f"note: R estimated as round({args.R_frac} * N) per row; "
            f"treat BoR as an estimate."
        )


if __name__ == "__main__":
    main()
