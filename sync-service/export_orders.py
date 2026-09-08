#!/usr/bin/env python3
"""CLI utility to export queued orders to import_staging.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.exporter import OrderExporter


def main() -> int:
    parser = argparse.ArgumentParser(description="Export queued orders to FoxPro staging JSON")
    parser.add_argument(
        "--output",
        "-o",
        default="import_staging.json",
        help="Path to output staging JSON file (default: import_staging.json)",
    )
    parser.add_argument(
        "--user",
        "-u",
        default="RAM",
        help="Operator username for FoxPro billing (default: RAM)",
    )
    parser.add_argument(
        "--salesman",
        "-s",
        default="SELF",
        help="Salesman code (default: SELF)",
    )
    parser.add_argument(
        "--order-ids",
        nargs="*",
        help="Optional specific order IDs to export",
    )
    args = parser.parse_args()

    exporter = OrderExporter()
    payload, count = exporter.export_queued_orders(
        output_file=args.output,
        order_ids=args.order_ids,
        operator_user=args.user,
        salesman_code=args.salesman,
    )

    print(f"Successfully exported {count} order(s) to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
