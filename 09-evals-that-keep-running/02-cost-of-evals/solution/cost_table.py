"""Lesson 09.2: what each kind of check costs, from the recorded runs.

Given: the recorded drafts and judge runs, and the lines that print.
You write `time_suite`, `means`, `totals` and `minutes_to_read`.

From this folder: uv run python cost_table.py
The code suite's time is measured on your machine, so yours will differ a
little; every other number is read from a recording.
"""
import time

from plumbing import judge_calls, log_pairs, open_traces
from scorecard.graders import CHECKS

PERSON_SECONDS = 60      # ASSUMED: a person reads one email and draft in 60 s


def time_suite(pairs):
    """Seconds the seven code checks take on every (email, trace) pair."""
    began = time.perf_counter()
    for email, trace in pairs:
        for check, _ in CHECKS.values():
            check(email, trace)
    return time.perf_counter() - began


def means(records, *fields):
    """The mean of each named field over a list of recorded dicts."""
    return [sum(r[f] for r in records) / len(records) for f in fields]


def totals(records, *fields):
    """The sum of each named field over a list of recorded dicts."""
    return [sum(r[f] for r in records) for f in fields]


def minutes_to_read(n, seconds_each):
    """Minutes a person needs to read n drafts at seconds_each."""
    return n * seconds_each / 60


if __name__ == "__main__":
    pairs = log_pairs()
    suite = time_suite(pairs)
    print(f"code suite, {len(pairs)} drafts: {suite:.2f} s "
          f"({suite / len(pairs) * 1000:.2f} ms a draft, no tokens)")
    for folder in ("04-heldout", "09-judge-swap"):
        calls = judge_calls(folder)
        seconds, tokens = means(calls, "seconds", "completion_tokens")
        print(f"judge {calls[0]['model']}: {seconds:.1f} s and {tokens:.0f} "
              f"reply tokens a verdict ({len(calls)} calls)")
    print(f"person (assumed pace): {PERSON_SECONDS} s a draft")

    runs = open_traces()
    prompt, reply, secs = totals(runs, "prompt_tokens", "completion_tokens",
                                 "seconds")
    print(f"\nwriting the {len(runs)} drafts of the open part: {prompt:,} "
          f"prompt + {reply:,} reply tokens, {secs:,.0f} s summed over "
          "emails (several ran at once)")
    judge = judge_calls("04-heldout")
    secs, tokens = totals(judge, "seconds", "completion_tokens")
    print(f"judging {len(judge)} drafts: {secs:.0f} s, "
          f"{tokens:,} reply tokens")
    print(f"a person reading 25 drafts: "
          f"{minutes_to_read(25, PERSON_SECONDS):.0f} minutes")
