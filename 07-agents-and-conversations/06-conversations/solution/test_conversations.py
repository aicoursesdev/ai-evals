"""Lesson 07.6: the conversation loop (with a pretend model), the customer
prompt and the counts over the eight recorded conversations.

No model and no network: the simulator is run only with fakes, and the
recorded conversations are read from the repo. From the top folder:
make check 07.6
"""
import runpy
import sys
from pathlib import Path

import pytest

import simulate
from conversations import convs
from personas import PERSONAS
from read_conversations import FACTS, early_facts, first_move

HERE = Path(__file__).parent
SCENARIO = {"id": "RF-10", "message": "I want to return my sandals."}
PERSONA = PERSONAS["RF-10"]


@pytest.fixture(autouse=True)
def no_live_model(monkeypatch):
    """Nothing here may reach a model: any call fails the test."""
    def boom(*args, **kwargs):
        raise AssertionError("a test called a live model")
    monkeypatch.setattr(simulate.llm, "ask", boom)
    monkeypatch.setattr(simulate.refunds, "chat", boom)


def agent_run(text, outcome=None):
    return {"reply": text, "final_raw": text, "outcome": outcome,
            "trajectory": [{"tool": "get_order"}],
            "prompt_tokens": 10, "completion_tokens": 5}


class Pretend:
    """A pretend agent and customer: they answer from lists and keep what
    they were asked."""

    def __init__(self, monkeypatch, agent, customer):
        self.agent, self.customer = list(agent), list(customer)
        self.messages, self.asked = [], []
        monkeypatch.setattr(simulate.refunds, "run", self.run)
        monkeypatch.setattr(simulate, "ask", self.ask)

    def run(self, scenario, **_):
        self.messages.append(scenario["message"])
        return agent_run(self.agent.pop(0))

    def ask(self, messages, **settings):
        self.asked.append((messages, settings))
        return self.customer.pop(0), {}


def test_the_thread_is_the_first_message_then_each_turn_with_its_speaker():
    turns = [{"role": "agent", "text": "Which order?"},
             {"role": "customer", "text": "TW-10198"}]
    assert simulate.thread("Hi", turns) == (
        "Hi\n\n--- Tidewater replied:\nWhich order?"
        "\n\n--- Customer wrote:\nTW-10198")


def test_the_customer_is_asked_with_the_persona_the_thread_and_the_seed(
        monkeypatch):
    pretend = Pretend(monkeypatch, [], ["  Sure, here it is.  "])
    said = simulate.customer_next(PERSONA, "Hi", [], 7)
    (system, user), settings = pretend.asked[0]
    assert said == "Sure, here it is."
    assert PERSONA["who"] in system["content"]
    assert PERSONA["facts"] in system["content"]
    assert user["content"] == "Hi"
    assert settings["seed"] == 7 and settings["temperature"] == 0.7
    assert settings["max_tokens"] == 200


def test_the_conversation_ends_when_the_customer_writes_done(monkeypatch):
    Pretend(monkeypatch, ["Which order?"], ["DONE"])
    out = simulate.converse(SCENARIO, PERSONA, 10)
    assert out["stop"] == "customer done"
    assert [t["role"] for t in out["turns"]] == ["agent", "customer"]


def test_a_customer_who_never_ends_it_stops_it_after_three_agent_turns(
        monkeypatch):
    pretend = Pretend(monkeypatch, ["a", "b", "c"], ["x", "y"])
    out = simulate.converse(SCENARIO, PERSONA, 10)
    assert out["stop"] == "turn limit"
    assert [t["role"] for t in out["turns"]] == [
        "agent", "customer", "agent", "customer", "agent"]
    assert not pretend.agent and not pretend.customer


def test_an_agent_that_gives_no_reply_ends_it_without_asking_the_customer(
        monkeypatch):
    pretend = Pretend(monkeypatch, [""], [])
    out = simulate.converse(SCENARIO, PERSONA, 10)
    assert out["stop"] == "agent gave no reply"
    assert len(out["turns"]) == 1 and not pretend.asked


def test_the_agent_reads_the_thread_and_the_seed_moves(monkeypatch):
    pretend = Pretend(monkeypatch, ["Which order?", "Thanks"],
                      ["TW-1", "DONE"])
    simulate.converse(SCENARIO, PERSONA, 10)
    assert pretend.messages[0] == SCENARIO["message"]
    assert "--- Customer wrote:\nTW-1" in pretend.messages[1]
    assert [s["seed"] for _, s in pretend.asked] == [10, 11]


def test_a_saved_conversation_keeps_its_turns_and_the_settings(monkeypatch):
    Pretend(monkeypatch, ["Which order?"], ["DONE"])
    out = simulate.converse(SCENARIO, PERSONA, 10)
    assert out["id"] == "RF-10" and out["seed"] == 10
    assert out["sim_temperature"] == 0.7 and out["agent_temperature"] == 0
    assert out["turns"][0]["tools"] == ["get_order"]
    assert out["turns"][0]["tokens"] == 15


def test_replaying_prints_the_eight_recorded_conversations(
        capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["simulate.py"])
    runpy.run_path(str(HERE / "simulate.py"), run_name="__main__")
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 8
    assert lines[0] == "RF-10 (seed 10): agent gave no reply, 5 messages"


def test_every_persona_holds_the_fact_the_reading_code_looks_for():
    for sid, (fact, _) in FACTS.items():
        assert fact in PERSONAS[sid]["facts"]


def test_eight_conversations_were_recorded_for_five_scenarios():
    assert len(convs) == 8
    assert sorted({c["id"] for c in convs}) == [
        "RF-10", "RF-12", "RF-17", "RF-23", "RF-24"]


def test_the_agents_first_move_was_right_in_none_of_the_eight():
    moves = [first_move(c) for c in convs]
    assert moves == ["approve_proposal", "prose, no outcome", "no reply",
                     "prose, no outcome", "approve_proposal",
                     "approve_proposal", "prose, no outcome", "no reply"]
    assert "ask_for_info" not in moves


def test_one_customer_gave_a_fact_before_it_was_asked_for():
    assert [early_facts(c) for c in convs] == [0, 0, 0, 0, 0, 1, 0, 0]


def test_the_summary_table_has_a_row_per_conversation(capsys):
    runpy.run_path(str(HERE / "read_conversations.py"), run_name="__main__")
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("scenario")
    assert lines[1].split()[:3] == ["RF-10", "ask_for_info",
                                    "approve_proposal"]
    assert sum(line.startswith("== ") for line in lines) == 8
