"""Given: the 100 coded drafts with the week of each email, and the file of
simulated actions."""
from scorecard import data
from scorecard.graders import logged

ACTIONS = data.DATA / "feedback" / "actions.jsonl"


def coded():
    """The 100 drafts of the failure map: {id: (week, fine)}, where fine is
    True when Module 01's reading found nothing wrong."""
    weeks = {e["id"]: w for w in (1, 2, 3, 4)
             for e in logged("emails", w)}
    return {r["id"]: (weeks[r["id"]], r["ok"] == "yes")
            for r in data.labels("01-coded")}


def actions():
    """{id: "sent" | "edited" | "rewritten"} from the simulated file."""
    return {r["id"]: r["action"] for r in data.read_jsonl(ACTIONS)}
