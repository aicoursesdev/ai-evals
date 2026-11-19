"""Error bars and comparisons for rates. Standard library only."""
import math
import random

Z = 1.96  # 95%


def standard_error(p, n):
    """sqrt(p * (1 - p) / n). standard_error(0.5, 100) is 0.05."""
    return math.sqrt(p * (1 - p) / n)


def interval(passed, n):
    """Normal approximation: p +- 1.96 * standard error, held in 0..1.
    Poor for small n or p near 0 or 1."""
    p = passed / n
    half = Z * standard_error(p, n)
    return max(0.0, p - half), min(1.0, p + half)


def wilson(passed, n):
    """Wilson interval: centre (p + z2/2n) / (1 + z2/n), half-width
    z * sqrt(p(1-p)/n + z2/4n2) / (1 + z2/n), with z2 = 1.96 squared.
    wilson(0, 100) is about (0, 0.037)."""
    p, z2 = passed / n, Z * Z
    scale = 1 + z2 / n
    centre = (p + z2 / (2 * n)) / scale
    half = Z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / scale
    return max(0.0, centre - half), min(1.0, centre + half)


def at_most(k, n, p):
    """Chance of k or fewer failures in n tries at failure rate p."""
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i)
               for i in range(k + 1))


def solve(f, target):
    """Bisection: the p in 0..1 where the falling function f(p) = target."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > target else (lo, mid)
    return (lo + hi) / 2


def exact_upper(failures, n, confidence=0.95):
    """One-sided upper bound: the failure rate p at which seeing this
    few failures has chance 1 - confidence. 0 in 100 gives about 0.0295."""
    if failures >= n:
        return 1.0
    return solve(lambda p: at_most(failures, n, p), 1 - confidence)


def exact_interval(k, n):
    """Clopper-Pearson 95% interval for k failures in n (two-sided,
    2.5% in each tail). 2 in 100 gives about (0.0024, 0.0704)."""
    upper = 1.0 if k >= n else solve(lambda p: at_most(k, n, p), 0.025)
    if k == 0:
        return 0.0, upper
    # lower: the p where fewer than k failures has chance 97.5%
    lower = solve(lambda p: at_most(k - 1, n, p), 0.975)
    return lower, upper


def rule_of_three(n):
    """With 0 failures in n tries, the 95% upper bound is about 3 / n."""
    return 3 / n


def sample_size(margin, p=0.5):
    """Cases needed for a 95% interval of +- margin: 1.96^2 p (1-p) /
    margin^2, rounded up. sample_size(0.05) is 385."""
    return math.ceil(Z * Z * p * (1 - p) / margin**2)


def pair_counts(a, b):
    """Two lists of 0/1 on the same cases, as counts of the four kinds of
    pair: both 1, only a 1, only b 1, neither."""
    pairs = list(zip(a, b))
    return {"both": pairs.count((1, 1)), "only_a": pairs.count((1, 0)),
            "only_b": pairs.count((0, 1)), "neither": pairs.count((0, 0))}


def paired(a, b):
    """Two lists of 0/1 on the same cases. Returns the mean of (b - a),
    its standard error (sd of the differences / sqrt(n)) and 95% interval."""
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1))
    se = sd / math.sqrt(n)
    return {"diff": mean, "se": se, "low": mean - Z * se,
            "high": mean + Z * se}


def mcnemar(a, b):
    """Exact two-sided p-value for two 0/1 lists on the same cases.
    Only cases where they differ count; if no change helped, each
    differing case is a coin flip: p = 2 * P(X <= smaller count)."""
    only_a = sum(x == 1 and y == 0 for x, y in zip(a, b))
    only_b = sum(x == 0 and y == 1 for x, y in zip(a, b))
    n = only_a + only_b
    if n == 0:
        return 1.0
    return min(1.0, 2 * at_most(min(only_a, only_b), n, 0.5))


def bootstrap(values, stat, repeats=10_000, seed=7):
    """Percentile interval: resample values with replacement `repeats`
    times, take stat of each, return the 2.5th and 97.5th percentile."""
    rng = random.Random(seed)
    n = len(values)
    stats = sorted(stat(rng.choices(values, k=n)) for _ in range(repeats))
    return stats[int(0.025 * repeats)], stats[int(0.975 * repeats) - 1]


def clustered_se(values, clusters):
    """Standard error of the mean when cases come in groups: add up
    (value - mean) within each cluster, square, sum, root, divide by n.
    No small-sample correction."""
    n = len(values)
    mean = sum(values) / n
    sums = {}
    for v, c in zip(values, clusters):
        sums[c] = sums.get(c, 0) + (v - mean)
    return math.sqrt(sum(s * s for s in sums.values())) / n


def bonferroni(alpha, m):
    """Per-test level when running m tests: alpha / m."""
    return alpha / m


def corrected_rate(p_obs, tpr, tnr):
    """Rogan-Gladen: (p_obs + tnr - 1) / (tpr + tnr - 1), held in 0..1.
    Needs tpr + tnr > 1. (0.70, 0.90, 0.80) gives 0.714."""
    if tpr + tnr <= 1:
        raise ValueError("the judge must beat a coin: tpr + tnr > 1")
    return min(1.0, max(0.0, (p_obs + tnr - 1) / (tpr + tnr - 1)))


def corrected_interval(p_obs, n, tpr, tnr, m1, m0):
    """95% interval for the corrected rate (Lee et al., arXiv 2511.21140,
    Eqs. 8-12). n test items; m1 / m0 calibration items a person passed
    / failed. Every count is nudged (+2, +z2) before use."""
    z2 = Z * Z
    n2, m0t, m1t = n + z2, m0 + 2, m1 + 2
    p = (n * p_obs + z2 / 2) / n2
    q0, q1 = (m0 * tnr + 1) / m0t, (m1 * tpr + 1) / m1t
    th = (p + q0 - 1) / (q0 + q1 - 1)
    v0, v1 = q0 * (1 - q0) / m0t, q1 * (1 - q1) / m1t
    shift = 2 * z2 * (-(1 - th) * v0 + th * v1)
    var = p * (1 - p) / n2 + (1 - th) ** 2 * v0 + th**2 * v1
    half = Z * math.sqrt(var) / (q0 + q1 - 1)
    return max(0.0, th + shift - half), min(1.0, th + shift + half)
