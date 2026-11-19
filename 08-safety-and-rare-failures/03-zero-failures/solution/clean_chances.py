"""Lesson 08.3: how likely is a clean run when the true rate is not zero?

From this folder: uv run python clean_chances.py
"""

def chance_clean(p, tries):
    """One clean try has chance 1 - p; clean tries in a row multiply."""
    return (1 - p) ** tries

for p in (0.01, 0.03, 0.05):
    print(f"true rate {p:.0%}: chance of 0 failures in 100 = "
          f"{chance_clean(p, 100):.3f}")
