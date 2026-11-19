"""Lesson 08.3: the upper limit after zero failures, by hand.

From this folder: uv run python by_hand.py
"""

def upper_limit(n):
    """The p where a clean run of n has chance 0.05: (1 - p) ** n = 0.05."""
    raise NotImplementedError(
        "TODO 08.3: return 1 - 0.05 ** (1 / n), the p where (1 - p) ** "
        "n = 0.05, see the lesson's 'The rule of three' section")

for n in (10, 30, 59, 100, 300, 1000):
    print(f"{n:5} clean trials: exact {upper_limit(n):.4f}"
          f"   3/n = {3 / n:.4f}")

# The smallest clean run whose limit is under 5%: try n = 1, 2, 3 ...
n = 1
while upper_limit(n) >= 0.05:
    n += 1
print("smallest n with limit under 5%:", n)
