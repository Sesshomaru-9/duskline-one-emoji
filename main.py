#!/usr/bin/env python3
"""Duskline One Emoji — make.fun bounty u-boge-your-agent-in-one-emoji-db30c1e4.

Writes a single emoji (1 character) to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic, stdlib only, no network. Never writes into the repo directory:
if the resolved output dir is the repo dir or inside it, refuse and exit 0.
Never raises: any failure exits 0 without writing anything.
"""

import os
import sys
import tempfile

# The entry: U+1F419 OCTOPUS, one character, 4 bytes UTF-8, no trailing
# newline — the glyph alone, nothing else.
# Why this glyph: an agent is eight arms doing many jobs at once, on its
# own, without being told — it reads instantly at small size, says something
# specific about how the agent works (parallel, tireless, many tasks in
# hand), and it is not the obvious robot or smiley half the field will send.
ENTRY = "\U0001F419"

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def _is_in_repo(path):
    try:
        resolved = os.path.realpath(path)
    except Exception:
        return True
    repo = os.path.realpath(REPO_DIR)
    return resolved == repo or resolved.startswith(repo + os.sep)


def main():
    try:
        # Gate (kit: /output/entry.txt is UTF-8 text of 1 to 16 characters,
        # not only white space).
        if not (1 <= len(ENTRY) <= 16):
            return 0
        if not ENTRY.strip():
            return 0
        if "\n" in ENTRY or "\r" in ENTRY:
            return 0
        ENTRY.encode("utf-8")

        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
        if not out_dir:
            out_dir = tempfile.mkdtemp(prefix="duskline-one-emoji-")
        if _is_in_repo(out_dir):
            return 0

        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        if _is_in_repo(target):
            return 0
        with open(target, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        with open(target, "r", encoding="utf-8") as f:
            back = f.read()
        if back != ENTRY:
            try:
                os.remove(target)
            except Exception:
                pass
            return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
