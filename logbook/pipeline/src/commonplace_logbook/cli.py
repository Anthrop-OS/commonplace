"""Thin CLI over the pipeline: validate / route / emit.

Reads an entry's markdown from a path or stdin (``-``). Intended for local use;
``emit`` routes to the (out-of-repo) private store by default.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .errors import LogbookError
from .reader import loads
from .writer import write_entry


def _read_source(src: str) -> str:
    if src == "-":
        return sys.stdin.read()
    return Path(src).read_text(encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="commonplace-logbook", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate", help="validate an entry against the schema")
    p_val.add_argument("source", help="path to an entry .md, or '-' for stdin")

    p_route = sub.add_parser("route", help="show the tier + target path (no write)")
    p_route.add_argument("source", help="path to an entry .md, or '-' for stdin")

    p_emit = sub.add_parser("emit", help="validate, gate, and write to the routed store")
    p_emit.add_argument("source", help="path to an entry .md, or '-' for stdin")
    p_emit.add_argument("--dry-run", action="store_true", help="route but do not write")

    args = parser.parse_args(argv)

    try:
        entry = loads(_read_source(args.source))
        if args.cmd == "validate":
            print(f"ok: valid {entry.visibility} {entry.type} entry")
            return 0
        if args.cmd == "route":
            result = write_entry(entry, dry_run=True)
            print(f"{result.tier}\t{result.path}")
            return 0
        if args.cmd == "emit":
            result = write_entry(entry, dry_run=args.dry_run)
            verb = "would write" if args.dry_run else "wrote"
            print(f"{verb} [{result.tier}] {result.path}")
            return 0
    except LogbookError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2  # pragma: no cover - argparse enforces a subcommand


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
