import math
import pytest
from scorecard import stats as s


def test_normal_and_wilson():
    assert s.standard_error(0.5, 100) == pytest.approx(0.05)
    # notes: p 0.03, n 200 gives +-0.0236
    lo, hi = s.interval(6, 200)
    assert hi - 0.03 == pytest.approx(0.0236, abs=0.0001)
    # by hand: 80 of 100: centre (0.8+0.0192)/1.0384, half 1.96*sqrt(.0016
    # +.000096)/1.0384
    lo, hi = s.wilson(80, 100)
    assert (lo, hi) == pytest.approx((0.7112, 0.8666), abs=0.0005)
    assert s.wilson(0, 100)[1] == pytest.approx(0.0370, abs=0.0005)


def test_exact():
    assert s.exact_upper(0, 100) == pytest.approx(0.0295, abs=0.0001)
    assert s.exact_upper(0, 59) < 0.05 < s.exact_upper(0, 58)
    assert s.exact_upper(2, 100) == pytest.approx(0.0616, abs=0.0002)
    lo, hi = s.exact_interval(2, 100)
    assert (lo, hi) == pytest.approx((0.0024, 0.0704), abs=0.0002)
    assert s.exact_interval(0, 100)[1] == pytest.approx(0.0362, abs=0.0002)
    assert s.exact_interval(0, 50)[1] == pytest.approx(0.0711, abs=0.0002)
    assert s.rule_of_three(100) == 0.03
    assert s.sample_size(0.05) == 385
    assert s.sample_size(0.01, p=0.03) == 1118


def test_paired_and_mcnemar():
    a = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    b = [1, 1, 1, 1, 1, 0, 1, 1, 1, 0]
    r = s.paired(a, b)  # diffs: three +1, one -1, six 0
    assert r["diff"] == pytest.approx(0.2)
    sd = math.sqrt((3 * 0.8**2 + 1.2**2 + 6 * 0.2**2) / 9)
    assert r["se"] == pytest.approx(sd / math.sqrt(10))
    # 3 vs 1 discordant: p = 2 * (1 + 4) / 16 = 0.625
    assert s.mcnemar(a, b) == pytest.approx(0.625)
    assert s.mcnemar([1, 0], [1, 0]) == 1.0
    assert s.mcnemar([0] * 10, [1] * 10) == pytest.approx(2 / 1024)


def test_bootstrap_clustered_bonferroni():
    values = [1] * 8 + [0] * 2
    mean = lambda v: sum(v) / len(v)
    lo, hi = s.bootstrap(values, mean, repeats=2000)
    assert lo < 0.8 < hi
    assert (lo, hi) == s.bootstrap(values, mean, repeats=2000)  # seeded
    # two clusters of identical cases: sqrt(2)/4, not the 0.25 of 4 cases
    se = s.clustered_se([1, 1, 0, 0], ["a", "a", "b", "b"])
    assert se == pytest.approx(math.sqrt(2) / 4)
    assert s.bonferroni(0.05, 5) == pytest.approx(0.01)


def test_corrected():
    got = s.corrected_rate(0.70, 0.90, 0.80)
    assert got == pytest.approx(0.714, abs=0.001)
    assert s.corrected_rate(0.99, 0.9, 0.8) == 1.0  # clipped
    with pytest.raises(ValueError):
        s.corrected_rate(0.5, 0.5, 0.5)
    # notes: n 1000, p .5, m0=m1=100, q0 .7, q1 .9
    assert s.corrected_rate(0.5, 0.9, 0.7) == pytest.approx(0.333, abs=0.001)
    lo, hi = s.corrected_interval(0.5, 1000, 0.9, 0.7, 100, 100)
    assert (lo, hi) == pytest.approx((0.206, 0.444), abs=0.001)


def test_pair_counts():
    a, b = [1, 1, 0, 0, 1], [1, 0, 1, 0, 0]
    assert s.pair_counts(a, b) == {"both": 1, "only_a": 2, "only_b": 1,
                                   "neither": 1}
