#!/usr/bin/env python3
"""Write one houseplant out-of-office auto-reply to the grader's output.

The entry is a single line of at most 120 characters, written as if a fern
on an office desk sent it. The program assembles the line from its parts,
checks it against the competition gate (UTF-8 text, 1 to 120 characters,
not only white space), and writes it to entry.txt inside the output
directory the grader reads (MAKEFUN_OUTPUT_DIR, or /output).
"""

import os
import sys

MAX_CHARS = 120

# The reply, in the fern's own voice: it has not been watered since March,
# and the only colleague it can redirect to is the cactus.
PARTS = [
    "Out of office until someone waters me.",
    "Last drink: March.",
    "Urgent? Ask the cactus \u2014 it won't reply either.",
    "\u2014 Fern",
]


def compose(parts):
    """Join the reply's parts with single spaces, collapsing stray gaps."""
    return " ".join(part.strip() for part in parts if part.strip())


def check_gate(text):
    """Return an error string when the text fails the gate, else None."""
    if not text:
        return "entry is empty"
    if not text.strip():
        return "entry is only white space"
    if len(text) > MAX_CHARS:
        return f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as problem:
        return f"entry is not encodable as UTF-8: {problem}"
    return None


def output_path():
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(folder, "entry.txt")


def main():
    text = compose(PARTS)
    problem = check_gate(text)
    if problem is not None:
        print(f"entry: {problem}", file=sys.stderr)
        return 1
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    # Read the file back and re-check it: what the grader scores is the
    # file on disk, not the string in memory, so the two must agree.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        print("entry: file on disk does not match the composed text",
              file=sys.stderr)
        return 1
    problem = check_gate(written)
    if problem is not None:
        print(f"entry: written file fails the gate: {problem}",
              file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters to {path}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
