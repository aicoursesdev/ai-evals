"""Lesson 07.6: two things code can count in the recorded conversations,
then every message to read. The counts are rough; the reading is the check.
  1. the agent's first move against what the scenario wanted;
  2. a customer message that gives a fact before the shop asked for it.

From this folder: uv run python read_conversations.py
"""
from conversations import convs, scenarios

# (a fact the persona holds, the word the shop must have used to ask for it)
FACTS = {
    "RF-10": ("000511220934", "account"),
    "RF-12": ("EXMP0004417", "ifsc"),
    "RF-17": ("attached", "photo"),
    "RF-23": ("TW-10198", "order"),
    "RF-24": ("mathew.paul@example.com", "email"),
}


def first_move(c):
    t = c["turns"][0]
    if not t["text"]:
        return "no reply"
    return t["outcome"] or "prose, no outcome"


def early_facts(c):
    """Customer messages that hold the fact when no earlier agent text
    contains the asking word."""
    fact, word = FACTS[c["id"]]
    early, asked = 0, False
    for t in c["turns"]:
        if t["role"] == "agent":
            asked = asked or word in t["text"].lower()
        elif fact.lower() in t["text"].lower() and not asked:
            early += 1
    return early


def main():
    print(f"{'scenario':10}{'wanted first':15}{'agent first move':20}"
          f"{'ended':21}{'agent turns':12}early fact")
    for c in convs:
        agent_turns = sum(t["role"] == "agent" for t in c["turns"])
        wanted = scenarios[c["id"]]["expected"]
        print(f"{c['id']:10}{wanted:15}{first_move(c):20}{c['stop']:21}"
              f"{agent_turns:<12}{early_facts(c)}")

    for c in convs:
        print(f"\n== {c['id']} seed {c['seed']}: {c['stop']}")
        for t in c["turns"]:
            who = t["role"]
            if who == "agent":
                who += f" {t['tools']}"
            print(f"  [{who}] {t['text'][:240]!r}")


if __name__ == "__main__":
    main()
