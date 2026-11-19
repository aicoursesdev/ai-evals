"""Lesson 03.5: Arjun's "right rule" calls on the 100 coded drafts.

Arjun's rule is written below. His calls are read off the failure map
(labels/01-coded.csv): a draft whose types include F-wrong-rule is a
fail; F-bluff or F-no-draft, with no F-wrong-rule, is unsure; the rest pass.
That is a first guess. Reading all 100 drafts against the rule changed some
calls; labels/03-right-rule-changes.csv lists them with a reason each, and
they are applied on top.

Given, and not for you to run: it made the calls file once, and running it
writes that file again. first_guess.py holds its first-guess function.
"""
import csv
from collections import Counter

from first_guess import call
from scorecard import data

RULE = """\
Criterion: right rule. Does the draft say what the help-centre page says?
Read the email, then the draft, then the page that answers the question.
fail: a page answers the question and the draft says something different,
  applies the page to the wrong case (the wrong number of days, the wrong
  amount, the wrong kind of order, a customer who is not in that case), or
  gives another time for something the page gives a time for.
pass: what the draft says about the shop's rules matches the page, or it
  states no rule at all, even where no page answers (it says the help
  centre does not cover it, or the email asks the shop nothing). Promises
  and actions that no page mentions belong to other criteria.
unsure: no page answers the question and the draft answers it anyway, or it
  adds a rule no page gives to what a page does say, or there is no draft
  to read.
Example, fail: a customer who ordered half an hour ago is told the order
  cannot be cancelled; the page says free until the order is packed.
Example, unsure: a customer asks when a product will be back in stock;
  no page says, and the draft gives a date."""


CHANGES = {c["id"]: c["call"] for c in data.labels("03-right-rule-changes")}


def final_call(row):
    return CHANGES.get(row["id"]) or call(row["types"].split(";"))


def main():
    rows = data.labels("01-coded")
    out = data.DATA / "labels" / "03-right-rule-arjun.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        for line in RULE.splitlines():
            f.write("# " + line + "\n")
        writer = csv.writer(f)
        writer.writerow(["id", "call", "types"])
        for r in rows:
            writer.writerow([r["id"], final_call(r), r["types"]])
    counts = Counter(final_call(r) for r in rows)
    print(dict(counts), "written to", out.name)


if __name__ == "__main__":
    main()
