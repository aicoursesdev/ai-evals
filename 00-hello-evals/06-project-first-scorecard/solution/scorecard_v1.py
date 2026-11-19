"""Lesson 00.6, project: a first scorecard for the help desk: triage accuracy
on Kiran's test emails and on week 1, the gap, and the spread in week 1.

From this folder: uv run python scorecard_v1.py
"""

from scorecard import data, run


def triage_score(emails, traces):
    """Run the recorded help desk over the emails; return the rows."""
    said = {t["id"]: t["triage"]["category"] for t in traces}
    return run.run(
        emails,
        system=lambda case: said[case["id"]],
        graders={"category": lambda output, case: output == case["category"]},
    )


def main():
    test = [e for e in data.emails(launch=True) if e["split"] == "test"]
    test_rows = triage_score(test, data.traces("hd-1", launch=True))
    week_rows = triage_score(data.emails(week=1), data.traces("hd-1", week=1))
    run.save(test_rows, "kiran-test.jsonl")
    run.save(week_rows, "week-1.jsonl")

    a = run.pass_rate(test_rows, "category")
    b = run.pass_rate(week_rows, "category")
    n_a = sum(r["category"] for r in test_rows)
    n_b = sum(r["category"] for r in week_rows)
    print("Triage accuracy (category), help desk hd-1")
    print(f"  Kiran's test split : {n_a} of {len(test_rows)} = {a:.1%}")
    print(f"  Week 1 of the log  : {n_b} of {len(week_rows)} = {b:.1%}")
    print(f"  Gap (week 1 minus test): {100 * (b - a):+.1f} points")

    slices = [sum(r["category"] for r in week_rows[i:i + 50])
              for i in (0, 50, 100)]
    print("  Week 1 in three slices of 50:", ", ".join(map(str, slices)),
          "right")


if __name__ == "__main__":
    main()
