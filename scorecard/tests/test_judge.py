import pytest
from scorecard import judge


def test_verdict_live_and_replay():
    ask = lambda p: "Reasoning...\nPASS"
    assert judge.verdict("Is {x} ok?", {"id": "a", "x": 1}, ask) is True
    never = lambda p: 1 / 0
    replay = {"a": "FAIL"}
    assert judge.verdict("{x}", {"id": "a"}, never, replay) is False
    with pytest.raises(ValueError):
        judge.verdict("{x}", {"id": "a", "x": 1}, lambda p: "unsure")


def test_verdict_unsure():
    reply = lambda p: "No page says.\nUNSURE"
    case = {"id": "a", "x": 1}
    assert judge.verdict("{x}", case, reply, unsure=True) is None
    with pytest.raises(ValueError):
        judge.verdict("{x}", case, reply)  # UNSURE is not a verdict here


def table(tp, fp, fn, tn):
    human = [True] * (tp + fn) + [False] * (fp + tn)
    judged = [True] * tp + [False] * fn + [True] * fp + [False] * tn
    return human, judged


def test_confusion_rates():
    h, j = table(45, 10, 10, 35)
    assert judge.confusion(h, j) == {"tp": 45, "fp": 10, "fn": 10, "tn": 35}
    assert judge.rates(h, j) == (45 / 55, 35 / 45)
    assert judge.agreement(h, j) == 0.8


def test_kappa_examples():
    h, j = table(45, 10, 10, 35)  # notes: kappa 0.596
    assert judge.kappa(h, j) == pytest.approx(0.596, abs=0.001)
    h, j = table(94, 2, 2, 2)  # 96% agreement, kappa 0.479
    assert judge.agreement(h, j) == 0.96
    assert judge.kappa(h, j) == pytest.approx(0.479, abs=0.001)
    assert judge.rates(h, j)[1] == 0.5


def test_reading_and_unsure_counts_as_not_pass():
    assert [judge.reading(r) for r in ("x\nPASS", "x\nFAIL", "x\nUNSURE",
                                       "so it is a PASS")] == [
        "pass", "fail", "unsure", "none"]
    c = judge.confusion([True, False, True], [True, None, None])
    assert c == {"tp": 1, "fp": 0, "fn": 1, "tn": 1}
