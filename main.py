#!/usr/bin/env python3
"""The Meeting That Should Have Been an Email — make.fun entry.

Writes one line (at most 200 chars) to /output/entry.txt: a joke about
a meeting that should have been an email. Stdlib only.

The line is picked by a small candidate tournament scored 1-5 on
specificity / surprise / freshness, mirroring the judge's brief:
on-subject first, then the laugh landing on its own, then surprise
(not the obvious complaint about how long it ran), then economy.
"""

import os
import sys

# (line, specificity, surprise, freshness)
# Tournament result (scored 1-5 specificity / surprise / freshness):
#   winner: "I declined a meeting about the meeting..." — 4/5/4 = 13.
#   runner-up: "I took 14 pages of notes..." — 5/4/4 = 13, loses the
#   tie-break on surprise: the escalation to a third meeting about
#   your absence is the fresher turn, and its punch lands on the
#   last word, which is what the judge weighs second.
# Killed: the follow-up-meeting line (3/2/2, only relatable) and the
# two length-complaint lines (the judge explicitly warns against
# the obvious "it ran long" angle).
CANDIDATES = [
    (
        "The meeting ended with a follow-up meeting to decide what "
        "the first meeting was about.",
        3, 2, 2,
    ),
    (
        "Forty-five minutes in, someone finally asked what the meeting "
        "was for. Nobody knew. We scheduled another one to find out.",
        4, 3, 3,
    ),
    (
        "I took 14 pages of notes in a meeting that could have been one "
        "sentence: 'The launch moved to Thursday.'",
        5, 4, 4,
    ),
    (
        "The agenda had one item: 'sync.' Ninety minutes later we were "
        "still syncing about what sync means.",
        4, 4, 4,
    ),
    (
        "I declined a meeting about the meeting and got invited to a "
        "third meeting to discuss my absence.",
        4, 5, 4,
    ),
    (
        "We spent an hour debating the meeting invite's title, then ran "
        "out of time to discuss the actual topic.",
        4, 3, 3,
    ),
]

# Gate from RULES.txt: 1 to 200 UTF-8 characters, single line.
MIN_CHARS = 1
MAX_CHARS = 200


def tournament_winner():
    """Highest total score; ties break to the higher surprise score,
    then to the shorter line."""
    best = None
    for line, spec, surp, fresh in CANDIDATES:
        total = spec + surp + fresh
        key = (total, surp, -len(line))
        if best is None or key > best[0]:
            best = (key, line)
    return best[1]


def check(line):
    """Validate the gate: 1-200 chars, single line, non-blank."""
    if not line or not line.strip():
        return "entry is blank"
    if "\n" in line or "\r" in line:
        return "entry must be a single line"
    n = len(line.encode("utf-8"))
    if n < MIN_CHARS or n > MAX_CHARS:
        return f"entry is {n} chars, gate is {MIN_CHARS}-{MAX_CHARS}"
    return None


def main():
    out_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    line = tournament_winner()
    problem = check(line)
    if problem:
        print(f"gate FAIL: {problem}", file=sys.stderr)
        return 1
    if "--check" in sys.argv:
        print(f"gate OK: {len(line)} chars, {len(line.encode('utf-8'))} bytes")
        print(line)
        return 0
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(line)
    # Verify the round-trip: what we wrote is exactly what we meant.
    with open(out_path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != line:
        print("round-trip FAIL: file differs from entry", file=sys.stderr)
        return 1
    print(f"wrote {len(line)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
