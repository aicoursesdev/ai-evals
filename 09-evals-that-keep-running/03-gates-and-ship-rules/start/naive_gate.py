"""Lesson 09.3: a gate that runs once, on an unchanged system.

Given: the recorded reruns and the lines that print. You write
`naive_fails`.

From this folder: uv run python naive_gate.py
The "change" is hd-1 asked again (temperature 0.7, a new seed each time),
so nothing changed and a fair gate should pass every time.
"""
from plumbing import repeats


def naive_fails(baseline, scores):
    """How many reruns score below the baseline: the naive gate fails
    anything lower."""
    raise NotImplementedError(
        "TODO 09.3: return how many reruns score below the baseline, see "
        "the lesson's 'A gate that runs once cries wolf' section")


if __name__ == "__main__":
    (base_triage, base_clean), triage_runs, check_runs = repeats()
    for name, base, runs in (("triage right", base_triage, triage_runs),
                             ("no check fires", base_clean, check_runs)):
        scores = [sum(r) for r in runs]          # of 100 emails each
        fails = naive_fails(sum(base), scores)
        print(f"{name}: baseline {sum(base)}, {len(runs)} unchanged reruns "
              f"scored {min(scores)} to {max(scores)}; the naive gate "
              f"failed {fails}")
