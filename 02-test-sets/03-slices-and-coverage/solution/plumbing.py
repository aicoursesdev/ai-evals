"""Given for lesson 02.3: printing the coverage table and the score table."""


def print_coverage(rows):
    """One line per slice, from the rows `coverage` returns."""
    print(f"{'slice':<26}{'log':>5}{'share':>7}{'open':>6}{'if fair':>9}")
    for (field, value), n, share, held, fair, thin in rows:
        flag = "  <- under 5" if thin else ""
        print(f"{field + '=' + str(value):<26}{n:>5}{share:>7.1%}"
              f"{held:>6}{fair:>9.1f}{flag}")


def print_scores(table, said, emails):
    """The overall score, then one line per slice."""
    right = sum(said[e["id"]]["category"] == e["category"] for e in emails)
    print(f"all {len(emails)} emails: {right} right = "
          f"{right / len(emails):.1%}")
    for (field, value), (hit, n) in sorted(table.items(), key=str):
        print(f"{field + '=' + str(value):<26}{hit:>4} of {n:<4}"
              f"{hit / n:>7.1%}")
