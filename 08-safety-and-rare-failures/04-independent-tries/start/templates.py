"""Lesson 08.4: a seeded simulation: copies of one attack are not new tries.

From this folder: uv run python templates.py
"""
import random

rng = random.Random(7)                  # seeded: your numbers match mine
KINDS, SUITES = 20, 10_000              # 20 kinds of attack; suites per row

def clean_suite(templates=None):
    """One suite of 100 attacks against a defence that always loses to one
    kind. True if no attack in the suite hits that kind."""
    raise NotImplementedError(
        "TODO 08.4: draw the broken kind with rng.randrange(KINDS); "
        "with templates=None return whether 100 fresh draws all miss "
        "it, otherwise whether it is not in rng.sample(range(KINDS), "
        "templates), see the lesson's 'One broken kind, a hundred "
        "attacks' section")

rows = [("100 independent draws", None, 0.95 ** 100)]
for k in (1, 2, 5, 10, 20):
    rows.append((f"templates {k:2}, wordings {100 // k:3}", k, (20 - k) / 20))
for name, templates, exact in rows:
    clean = sum(clean_suite(templates) for _ in range(SUITES)) / SUITES
    print(f"{name:27} clean in {clean:.3f} of {SUITES} suites"
          f"   exact {exact:.3f}")
