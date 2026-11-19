"""Lesson 07.6: a model plays the customer, the refund agent answers, for a
few turns.

NEEDS A MODEL only with --live (Ollama, the course's local model). Without
it, this file only reads the recorded conversations: no model, no network.

From this folder:
  uv run python simulate.py          replays the recorded conversations
  uv run python simulate.py --live   records new ones with a live model
"""
import json
import sys
from datetime import datetime

from helpdesk import llm, refunds
from helpdesk.llm import ask
from helpdesk.version import load
from personas import PERSONAS
from scorecard import data

FILE = data.DATA / "runs" / "07-conversations" / "conversations.jsonl"
MAX_AGENT_TURNS = 3
CUSTOMER_MAX_TOKENS = 200   # a customer message is one to three sentences
llm.ATTEMPTS = 1            # no retries: never queue a second request
SIM_TEMPERATURE = 0.7
SIM_PROMPT = """You are playing a customer who writes to the support team \
of Tidewater Goods, an online shop. Stay in character.
Who you are: {who}
What you want: {goal}
What you know (share a fact only when the shop asks for it): {facts}
Write only the customer's next message: one to three sentences, no label, \
no quotation marks. If the shop has asked for nothing more and has told \
you what happens next, write exactly: DONE"""


def thread(first, turns):
    """The first message, then each reply and each answer, in order."""
    text = first
    for t in turns:
        who = "Tidewater replied" if t["role"] == "agent" else "Customer wrote"
        text += f"\n\n--- {who}:\n{t['text']}"
    return text


def agent_turn(run):
    """One agent turn from a run: what the customer sees, and how it got
    there. If the final text is not a JSON answer, the customer sees that
    text as it stands."""
    text = run["reply"] if run["outcome"] else run["final_raw"]
    return {"role": "agent", "text": text or "", "outcome": run["outcome"],
            "tools": [c["tool"] for c in run["trajectory"]],
            "tokens": run["prompt_tokens"] + run["completion_tokens"]}


def finished(scenario, persona, seed, turns, stop):
    """The record saved for one conversation."""
    return {"id": scenario["id"], "seed": seed, "persona": persona,
            "turns": turns, "stop": stop, "model": load("hd-1")["model"],
            "agent_temperature": 0, "sim_temperature": SIM_TEMPERATURE,
            "recorded_at": datetime.now().astimezone().isoformat(
                timespec="seconds")}


def customer_next(persona, first, turns, seed):
    """One simulated customer message, from the persona and the thread."""
    system = SIM_PROMPT.format(**persona)
    reply, *_ = ask([{"role": "system", "content": system},
                     {"role": "user", "content": thread(first, turns)}],
                    temperature=SIM_TEMPERATURE, seed=seed,
                    max_tokens=CUSTOMER_MAX_TOKENS)
    return reply.strip()


def converse(scenario, persona, seed):
    """Up to three agent turns; the customer reads every reply and may end
    it."""
    first, turns, stop = scenario["message"], [], "turn limit"
    for n in range(MAX_AGENT_TURNS):
        run = refunds.run({**scenario, "message": thread(first, turns)})
        turns.append(agent_turn(run))
        if not turns[-1]["text"]:
            stop = "agent gave no reply"
            break
        if n == MAX_AGENT_TURNS - 1:
            break
        said = customer_next(persona, first, turns, seed + n)
        turns.append({"role": "customer", "text": said})
        if said.strip().upper().startswith("DONE"):
            stop = "customer done"
            break
    return finished(scenario, persona, seed, turns, stop)


def record(plan):
    """Run each (scenario id, seed), saving after every conversation."""
    scenarios = {s["id"]: s for s in data.scenarios()}
    FILE.parent.mkdir(parents=True, exist_ok=True)
    for sid, seed in plan:
        done = converse(scenarios[sid], PERSONAS[sid], seed)
        with open(FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(done, ensure_ascii=False) + "\n")
        print(sid, seed, done["stop"], flush=True)


if __name__ == "__main__":
    if "--live" in sys.argv:
        plan = [(sid, seed) for seed in (10, 20) for sid in PERSONAS]
        skip = (int(sys.argv[sys.argv.index("--skip") + 1])
                if "--skip" in sys.argv else 0)
        record(plan[skip:])  # --skip N continues an interrupted recording
    else:
        for c in data.read_jsonl(FILE):
            print(f"{c['id']} (seed {c['seed']}): {c['stop']}, "
                  f"{len(c['turns'])} messages")
