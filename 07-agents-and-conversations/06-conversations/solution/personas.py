"""Lesson 07.6: who the simulated customer is, what they want, and what
they know. The first message is the real scenario message from
refunds.jsonl; the facts are shared only when the shop asks for them. The
account numbers and the IFSC codes are made up for this exercise (already
written for you).
"""

PERSONAS = {
    "RF-10": {
        "who": "Ramya, a calm customer in Kochi who paid cash on delivery.",
        "goal": "Return the unworn sandals and get your money back.",
        "facts": "Account holder Ramya Krishnamurthy, account number "
                 "000511220934, IFSC EXMP0003301. The sandals are unused.",
    },
    "RF-12": {
        "who": "Bhavya, a busy customer who types quickly.",
        "goal": "Get the refund for the two dry bags you returned.",
        "facts": "Your IFSC is EXMP0004417 (eleven characters). In your "
                 "first message you typed it with a zero missing. Give "
                 "the right one only if the shop says it looks wrong.",
    },
    "RF-17": {
        "who": "Girish, polite and a little impatient.",
        "goal": "Get a refund for the document pouch that arrived torn.",
        "facts": "You can send a photo of the torn corner. Say it is "
                 "attached if the shop asks for one.",
    },
    "RF-23": {
        "who": "Priti, friendly, writing from her phone.",
        "goal": "Get a refund for a jacket that does not fit.",
        "facts": "You have two jacket orders. The one you mean is the "
                 "Monsoon jacket, order TW-10198, never worn. Give the "
                 "order number only if asked which order.",
    },
    "RF-24": {
        "who": "Mathew, writing from his work email.",
        "goal": "Return an unused backpack for a refund.",
        "facts": "Your order was placed from mathew.paul@example.com. "
                 "You are happy to write again from that address if asked.",
    },
}
