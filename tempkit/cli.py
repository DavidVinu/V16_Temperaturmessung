"""Command line entry point for :mod:`tempkit`.

Examples
--------
Summarise every CSV file in the ``data`` directory::

    python -m tempkit.cli summary data

Fit Newton's law of cooling to a single run and print the time constant::

    python -m tempkit.cli fit data --run 1
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .analysis import fit_cooling
from .io import load_dataset
from .report import summarise_dataset, summarise_series


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tempkit",
        description="Analyse the V16 Temperaturmessung measurement logs.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    summary = sub.add_parser("summary", help="summarise a dataset directory")
    summary.add_argument("directory", help="directory containing CSV logs")

    fit = sub.add_parser("fit", help="fit Newton cooling to one run")
    fit.add_argument("directory", help="directory containing CSV logs")
    fit.add_argument("--run", type=int, required=True, help="run id to fit")
    fit.add_argument(
        "--min-delta",
        type=float,
        default=0.5,
        help="drop points closer than this to ambient (default: 0.5 C)",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Run the command line interface and return a process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "summary":
        series = load_dataset(args.directory)
        print(summarise_dataset(series))
        return 0

    if args.command == "fit":
        series = load_dataset(args.directory).for_run(args.run)
        if len(series) == 0:
            print(f"no data for run {args.run}", file=sys.stderr)
            return 1
        print(summarise_series(series))
        fit = fit_cooling(series, min_delta_c=args.min_delta)
        print(
            f"tau = {fit.tau_s:.2f} +/- {fit.tau_err_s:.2f} s, "
            f"half-life = {fit.half_life_s():.2f} s, "
            f"delta0 = {fit.delta0_c:.2f} C, "
            f"R^2 = {fit.r_squared:.4f}"
        )
        return 0

    parser.error(f"unknown command {args.command!r}")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
