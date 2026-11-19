"""Lesson 10.3: the planned measures on the open part (read before the
sealed part is opened).

From this folder: uv run python open_scores.py
"""
from plumbing import RUNS, judge_pass, line, measures, open_part

if __name__ == "__main__":
    mail, seen = open_part()
    for name, (hits, n) in measures(mail, seen).items():
        print(line(name, hits, n))
    hits, n = judge_pass(RUNS / "04-dev" / "v4.jsonl")
    print(line("judge: clear PASS (v4)", hits, n))
