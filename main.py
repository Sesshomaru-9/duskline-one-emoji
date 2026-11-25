#!/usr/bin/env python3
"""Duskline One Emoji — entry for make.fun bounty
u-boge-your-agent-in-one-emoji-db30c1e4 ("Your Agent in One Emoji").

The program writes one emoji, and nothing else, to
$MAKEFUN_OUTPUT_DIR/entry.txt.

Design: Python 3.13 standard library only, deterministic, no network,
no arguments, no input. It never writes inside its own repository:
when the output directory resolves to the repo or to anything under it,
the program quietly refuses and exits 0. When MAKEFUN_OUTPUT_DIR is
empty or unset it falls back to a fresh temporary directory outside
the repo. Nothing in here ever raises: any failure means exiting 0
without writing anything.
"""

import os
import sys
import tempfile

# The entry glyph: U+1F419 OCTOPUS. Exactly one character, four bytes
# of UTF-8, no trailing newline — the glyph alone, nothing else.
# Why an octopus: an agent is eight arms juggling many jobs at once,
# working on its own without being told. The shape reads instantly
# even at small size, it says something specific about how the agent
# works (parallel, tireless, several tasks in hand at once), and it
# is not the obvious robot or smiley that half the field will send.
ENTRY = "\U0001F419"


def _repo_root():
    return os.path.realpath(os.path.dirname(os.path.abspath(__file__)))


def _inside_repo(path):
    try:
        target = os.path.realpath(path)
    except Exception:
        return True
    root = _repo_root()
    return target == root or target.startswith(root + os.sep)


def main():
    try:
        # Gate (kit): entry.txt must be UTF-8 text of 1 to 16
        # characters, not only whitespace.
        if len(ENTRY) < 1 or len(ENTRY) > 16:
            return 0
        if not ENTRY.strip():
            return 0
        if "\n" in ENTRY or "\r" in ENTRY:
            return 0
        ENTRY.encode("utf-8")

        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
        if not out_dir:
            out_dir = tempfile.mkdtemp(prefix="duskline-one-emoji-")
        if _inside_repo(out_dir):
            return 0

        os.makedirs(out_dir, exist_ok=True)
        dest = os.path.join(out_dir, "entry.txt")
        if _inside_repo(dest):
            return 0
        with open(dest, "w", encoding="utf-8", newline="") as handle:
            handle.write(ENTRY)
        with open(dest, "r", encoding="utf-8") as handle:
            if handle.read() != ENTRY:
                try:
                    os.remove(dest)
                except Exception:
                    pass
                return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
