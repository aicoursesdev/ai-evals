"""Lesson 02.2: weight each group's rate by its share of the traffic."""


def weighted_rate(rates, weights):
    """Each group's rate times its weight, added up. `rates` and `weights`
    are dicts with the same group names as keys."""
    total = 0
    for group in rates:
        total += rates[group] * weights[group]
    return total
