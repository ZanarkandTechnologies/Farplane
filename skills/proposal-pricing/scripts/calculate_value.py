#!/usr/bin/env python3
"""Calculate a conservative annual value and a simple value-based starting price."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_HALF_UP


def positive_decimal(value: str) -> Decimal:
    number = Decimal(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return number


def round_to(value: Decimal, increment: Decimal) -> Decimal:
    return (value / increment).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * increment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--share", type=positive_decimal, default=Decimal("0.15"))
    parser.add_argument("--round-to", type=positive_decimal, default=Decimal("500"))
    subparsers = parser.add_subparsers(dest="anchor", required=True)

    people_time = subparsers.add_parser("people-time")
    people_time.add_argument("--people", type=positive_decimal, required=True)
    people_time.add_argument("--hours", type=positive_decimal, required=True)
    people_time.add_argument("--rate", type=positive_decimal, required=True)
    people_time.add_argument("--periods", type=positive_decimal, required=True)

    consequence = subparsers.add_parser("consequence")
    consequence.add_argument("--incidents", type=positive_decimal, required=True)
    consequence.add_argument("--cost", type=positive_decimal, required=True)
    consequence.add_argument("--periods", type=positive_decimal, required=True)

    annual = subparsers.add_parser("annual")
    annual.add_argument("--amount", type=positive_decimal, required=True)
    return parser


def annual_value(args: argparse.Namespace) -> Decimal:
    if args.anchor == "people-time":
        return args.people * args.hours * args.rate * args.periods
    if args.anchor == "consequence":
        return args.incidents * args.cost * args.periods
    return args.amount


def main() -> int:
    args = build_parser().parse_args()
    if args.share >= 1:
        raise SystemExit("--share must be less than 1")

    value = annual_value(args)
    price = round_to(value * args.share, args.round_to)
    if price <= 0:
        price = args.round_to
    multiple = (value / price).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    result = {
        "anchor": args.anchor,
        "annual_value": str(value.quantize(Decimal("0.01"))),
        "price_share": str(args.share),
        "recommended_price": str(price.quantize(Decimal("0.01"))),
        "client_return_multiple": str(multiple),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
