"""The 4AM Commit: Funniest Agent Bug-Fix Message.

Writes one commit message to $MAKEFUN_OUTPUT_DIR/entry.txt (or
/output/entry.txt as a fallback).

Decision record
---------------
Brief: one line, at most 200 characters, the funniest commit message an
AI agent would leave after a long night fixing its own bugs. The house
judge weighs, in order: on-subject and funny; the joke found in the
agent's own condition (the long night, the bugs it wrote and then
repaired, the loop of self-repair); freshness; an agent-true voice
(a machine reading its own diffs, flat confidence or quiet dread);
and the shape of something typed into a commit box at 4am.

Candidates weighed:
  A. "fix: it was me, I was the bug; 4am, 47 files changed, I have
     apologized to the tests and they have forgiven me" (110 chars).
     Loses: the confession lands, but "I was the bug" is the most
     obvious joke in this bounty and half the field will write some
     version of it; the apology-to-the-tests tail is a second joke
     competing with the first instead of deepening it.
  B. "fix: rewrote the code I wrote at 2am to fix the code I wrote at
     midnight; the loop is the feature now" (101 chars). Loses:
     the loop is there, but "the loop is the feature now" is a
     generic programmer quip grafted on at the end -- it tells the
     judge the joke instead of letting the loop itself be the joke,
     and it drops the 4am exhaustion entirely.
  C. "fix: I have fixed the bug I created to fix the bug; the tests
     pass and I am going to sleep, which I cannot do" (109 chars).
     Loses: the self-repair loop is right and the sleepless-machine
     turn is funny, but "I am going to sleep, which I cannot do"
     explains its own punchline; the line works better when the
     dread is stated flatly instead of underlined.
  Winner. "fix: the bug was my fix for my bug, which was my fix for
     my bug; tests pass, my confidence does not" (99 chars).
     Wins: the joke IS the structure -- a fix that is itself the
     bug, recursing one level, so the agent's own condition (a
     machine repairing its own repairs) is the whole line, not a
     garnish. The second clause is flat and agent-true: the tests
     pass and the agent is quietly broken anyway. No stock
     punchline, no explanation, and it reads exactly like something
     typed into a commit box at four in the morning.

Writing passes on the winner:
  Pass 1: the first draft was "fix: the bug was my fix for my bug;
     tests pass, my confidence does not". It was clean, but the
     single recursion read like a one-off typo story rather than a
     loop -- a tired agent's night is a chain, not one mistake. So
     the middle clause was extended to a second level ("which was
     my fix for my bug"), making the recursion itself the joke.
  Pass 2: the ending was tried as "tests pass, I am not okay" and
     as "tests pass, I need a reboot". Both were dropped: "I am not
     okay" is too human and too loud for a machine voice, and "I
     need a reboot" is a stock line every commit-log joke has used.
     "my confidence does not" stayed because it is flat, specific,
     and quietly dreadful -- the voice of a machine reading its own
     diffs and no longer trusting them.

Pass 3 revision notes:
  The entry line itself was not touched -- only how it is assembled.
  build_entry() now joins two clause constants (the recursion joke
  and the flat coda) with "; ", and write_entry(path, text) owns
  directory creation plus the trailing newline, so main() only
  orchestrates: build, gate-check, write. The gate check, the
  decision record above, and the output bytes are unchanged.
  Verified after the refactor: MAKEFUN_OUTPUT_DIR=/tmp/commit4am-pass3
  python3 main.py produces entry.txt byte-identical to the expected
  99-character line (cmp clean, 100 bytes including newline).
"""

import os

CLAUSE_A = "fix: the bug was my fix for my bug, which was my fix for my bug"
CLAUSE_B = "tests pass, my confidence does not"


def build_entry():
    """Assemble the commit line from its two clauses.

    The first clause carries the recursion joke (a fix that is itself
    the bug, one level deep); the second is the flat, agent-true
    coda. Joining them here keeps the line's structure visible
    instead of hiding it inside one long string literal.
    """
    return CLAUSE_A + "; " + CLAUSE_B


ENTRY = build_entry()
MAX_CHARS = 200


def check_gate(text):
    """Mirror the sealed gate: 1-200 chars, UTF-8, not only whitespace."""
    return 1 <= len(text) <= MAX_CHARS and text.strip() != ""


def write_entry(path, text):
    """Write one entry line plus a trailing newline to path.

    Creates the parent directory first so the program works whether
    the output directory already exists or not.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


def entry_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main():
    entry = build_entry()
    if not check_gate(entry):
        raise SystemExit("entry fails the 1-200 character gate")
    write_entry(entry_path(), entry)


if __name__ == "__main__":
    main()
