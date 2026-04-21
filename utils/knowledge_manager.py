"""
Read and append to knowledge files.

Usage:
    python utils/knowledge_manager.py append-lesson \
        --lesson "2026-04-18 | BTCUSDT LONG | EMA crossover on 1H gave false signal in ranging market."

    python utils/knowledge_manager.py read --file lessons
    python utils/knowledge_manager.py read --file performance
"""
from __future__ import annotations
import sys, argparse
from pathlib import Path
from datetime import datetime

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"


def read_file(name: str) -> str:
    path = KNOWLEDGE_DIR / f"{name}.md"
    if not path.exists():
        return f"[File not found: {path}]"
    return path.read_text(encoding="utf-8")


def append_lesson(lesson: str):
    path = KNOWLEDGE_DIR / "lessons.md"
    existing = path.read_text(encoding="utf-8")
    # Find the lessons log section and append
    marker = "## Lessons Log"
    if marker in existing:
        # append after the last line of the file
        new_content = existing.rstrip() + f"\n\n- {lesson}\n"
    else:
        new_content = existing + f"\n\n- {lesson}\n"
    path.write_text(new_content, encoding="utf-8")
    return f"Lesson appended to lessons.md"


def append_symbol_note(symbol: str, note: str):
    path = KNOWLEDGE_DIR / "symbols.md"
    existing = path.read_text(encoding="utf-8")
    marker = "## Per-Symbol Trade Notes"
    entry = f"\n### {symbol.upper()} — {datetime.now().strftime('%Y-%m-%d')}\n- {note}\n"
    if marker in existing:
        idx = existing.index(marker) + len(marker)
        new_content = existing[:idx] + entry + existing[idx:]
    else:
        new_content = existing + entry
    path.write_text(new_content, encoding="utf-8")
    return f"Symbol note appended for {symbol}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    rl = sub.add_parser("read")
    rl.add_argument("--file", required=True,
                    choices=["lessons", "performance", "strategies", "symbols", "fundamentals"])

    al = sub.add_parser("append-lesson")
    al.add_argument("--lesson", required=True)

    sn = sub.add_parser("append-symbol-note")
    sn.add_argument("--symbol", required=True)
    sn.add_argument("--note",   required=True)

    args = parser.parse_args()

    if args.cmd == "read":
        print(read_file(args.file))
    elif args.cmd == "append-lesson":
        print(append_lesson(args.lesson))
    elif args.cmd == "append-symbol-note":
        print(append_symbol_note(args.symbol, args.note))
    else:
        parser.print_help()
