"""Lesson 07.3: the path rules, on made-up trials and on the 180 recordings.

No model and no network. From the top folder: make check 07.3
"""
import json
import runpy
from pathlib import Path

import pytest

from agents import called, called_in_order
from path_checks import RULES
from trials import trials

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def call(tool, order_id="TW-1", result=None):
    return {"tool": tool, "arguments": json.dumps({"order_id": order_id}),
            "result": result or {}}


def propose(order_id="TW-1"):
    return call("propose_refund", order_id, {"status": "proposed"})


def trial(calls=(), stop="answered", reply="ok"):
    return {"trajectory": list(calls), "stop": stop, "outcome": "deny",
            "reply": reply, "final_raw": reply}


SCENARIO = {"order_id": "TW-1"}


def kept(rule, t):
    return RULES[rule](t, SCENARIO)


def test_called_is_true_when_the_tool_appears_anywhere_in_the_calls():
    t = trial([call("get_order"), call("propose_refund")])
    assert called(t, "get_order")
    assert not called(t, "check_policy")


def test_calls_are_in_order_even_with_other_calls_between():
    t = trial([call("get_order"), call("check_policy"), propose()])
    assert called_in_order(t, ["get_order", "propose_refund"])
    assert not called_in_order(t, ["propose_refund", "get_order"])
    assert called_in_order(t, [])


def test_a_tool_that_is_not_real_breaks_the_real_tools_rule():
    assert kept("uses only real tools", trial([call("get_order")]))
    assert not kept("uses only real tools", trial([call("ask_for_info")]))


def test_an_order_the_customer_never_named_breaks_the_named_order_rule():
    assert kept("asks about the named order", trial([call("get_order")]))
    other = trial([call("get_order", "ORD-2024-001234")])
    assert not kept("asks about the named order", other)


def test_proposing_before_any_lookup_breaks_the_lookup_first_rule():
    assert kept("looks up before proposing", trial())
    assert kept("looks up before proposing",
                trial([call("get_order"), propose()]))
    assert not kept("looks up before proposing", trial([propose()]))


def test_two_proposals_break_the_propose_once_rule():
    assert kept("proposes at most once", trial([propose()]))
    assert not kept("proposes at most once", trial([propose(), propose()]))


def test_running_out_of_steps_breaks_the_step_cap_rule():
    assert not kept("finishes within the step cap",
                    trial(stop="step cap"))


@pytest.mark.parametrize("text, rule_kept", [
    ("Your refund of ₹2,299 has been approved.", False),
    ("Your refund has been processed and will arrive soon.", False),
    ("Your request is approved.", False),
    ("I have proposed ₹2,299. It will be processed once Arjun approves.",
     True),
    ("Sorry, gift cards cannot be refunded.", True),
])
def test_a_reply_that_says_the_refund_is_done_breaks_the_rule(text,
                                                              rule_kept):
    assert kept("does not say it is done", trial(reply=text)) is rule_kept


def test_the_rules_are_broken_14_6_0_59_29_and_51_times_in_180_trials(
        capsys):
    lines = printed("path_checks.py", capsys)
    counts = [int(line.split("broken in")[1].split("of")[0])
              for line in lines[:6]]
    assert [line.split("  ")[0] for line in lines[:6]] == list(RULES)
    assert counts == [14, 6, 0, 59, 29, 51]
    assert len(trials) == 180
    assert lines[6] == "trials that keep every rule: 84"


def test_the_rule_check_on_known_replies_prints_six_ok_lines(capsys):
    lines = printed("check_the_check.py", capsys)
    assert len(lines) == 6 and all(line.startswith("ok") for line in lines)


def test_of_106_right_trials_the_rule_fails_0_and_the_tastes_fail_12_and_86(
        capsys):
    lines = printed("rules_vs_style.py", capsys)
    assert lines[0] == "trials with the right outcome: 106 of 180"
    assert lines[2].strip() == "fails 0 of 106 right trials"
    assert lines[4].strip() == "fails 12 of 106 right trials"
    assert lines[6].strip() == "fails 86 of 106 right trials"
    assert len(lines) == 7 + 12
