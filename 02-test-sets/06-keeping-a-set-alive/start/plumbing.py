"""Given for lesson 02.6: printing the score table."""


def print_scores(table, said, emails):
    """The overall score, then one line per slice."""
    right = sum(said[e["id"]]["category"] == e["category"] for e in emails)
    print(f"all {len(emails)} emails: {right} right = "
          f"{right / len(emails):.1%}")
    for (field, value), (hit, n) in sorted(table.items(), key=str):
        print(f"{field + '=' + str(value):<26}{hit:>4} of {n:<4}"
              f"{hit / n:>7.1%}")
