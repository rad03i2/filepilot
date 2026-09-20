from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from .core import apply_plan, build_plan, file_sha256, undo


def _size(value: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{value} B"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="filepilot", description="Safely organize files by type with preview and undo.")
    p.add_argument("--version", action="version", version="FilePilot 1.0.0 — Radwan Abdulhadi Ahmed (@rad03i2)")
    sub = p.add_subparsers(dest="command", required=True)

    for name in ("plan", "organize"):
        cmd = sub.add_parser(name, help=f"{name.title()} file organization")
        cmd.add_argument("source", type=Path)
        cmd.add_argument("--destination", "-d", type=Path)
        cmd.add_argument("--recursive", "-r", action="store_true")
        cmd.add_argument("--include-hidden", action="store_true")
        if name == "organize":
            cmd.add_argument("--manifest", type=Path, default=Path("filepilot-manifest.json"))
            cmd.add_argument("--yes", action="store_true", help="Apply without interactive confirmation")

    u = sub.add_parser("undo", help="Restore files using a FilePilot manifest")
    u.add_argument("manifest", type=Path)
    h = sub.add_parser("hash", help="Print a file SHA-256 digest")
    h.add_argument("file", type=Path)
    return p


def _print_plan(moves) -> None:
    if not moves:
        print("Nothing to organize.")
        return
    counts = Counter(m.category for m in moves)
    total = sum(m.size for m in moves)
    print(f"Planned moves: {len(moves)} ({_size(total)})")
    print("Categories: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for m in moves:
        print(f"  [{m.category}] {m.source} -> {m.destination}")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "hash":
            if not args.file.is_file():
                raise FileNotFoundError(args.file)
            print(file_sha256(args.file))
            return 0
        if args.command == "undo":
            print(f"Restored {undo(args.manifest)} file(s).")
            return 0

        moves = build_plan(args.source, args.destination, recursive=args.recursive,
                           include_hidden=args.include_hidden)
        _print_plan(moves)
        if args.command == "plan" or not moves:
            return 0
        if not args.yes:
            answer = input("Apply this plan? [y/N] ").strip().lower()
            if answer not in {"y", "yes"}:
                print("Cancelled; no files were changed.")
                return 0
        payload = apply_plan(moves, args.manifest)
        print(f"Moved {len(payload['moves'])} file(s). Undo manifest: {args.manifest}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
