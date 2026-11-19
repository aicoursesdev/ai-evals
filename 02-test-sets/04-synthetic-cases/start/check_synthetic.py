"""Lesson 02.4: what the made-up cases got from the help desk, by code.

From this folder: uv run python check_synthetic.py
Code can check three things: the labels, the script of the reply, and the
bracketed article names. Everything else needs a person to read the draft.
"""
import re

from scorecard import data

REAL = {a["id"] for a in data.articles()}


def in_script(text, language):
    """Is the text in the customer's script? Only for hi, ta and ml."""
    ranges = {"hi": "ऀ-ॿ", "ta": "஀-௿", "ml": "ഀ-ൿ"}
    return bool(re.search(f"[{ranges[language]}]", text))


def invented_ids(draft):
    """Bracketed names in the draft that are not help-centre articles."""
    return [i for i in re.findall(r"\[([^\]]+)\]", draft) if i not in REAL]


def check(case, trace):
    """(category agrees, all three labels agree, reply script) for one case.
    The script is "own", "English", or "-" for en and hi-en emails."""
    got = trace["triage"]
    same = got["category"] == case["category"]
    full = same and all(got[k] == case[k] for k in ("urgency", "needs_human"))
    script = "-"
    if case["language"] in ("hi", "ta", "ml"):
        own = in_script(trace["draft"], case["language"])
        script = "own" if own else "English"
    return same, full, script


def main():
    cases = {c["id"]: c for c in data.testset("synthetic")}
    traces = {t["id"]: t for t in data.run("02-synthetic")["hd-1"]}
    cat = all3 = wrong_script = 0
    print("case  category  all three  reply script  invented article names")
    for id_ in sorted(cases):
        same, full, script = check(cases[id_], traces[id_])
        cat, all3 = cat + same, all3 + full
        wrong_script += script == "English"
        print(f"{id_:<6}{'yes' if same else 'NO':<10}"
              f"{'yes' if full else 'no':<11}{script:<14}"
              f"{invented_ids(traces[id_]['draft'])}")
    print(f"category agrees on {cat} of {len(cases)}, all three on {all3};",
          f"{wrong_script} replies to hi, ta or ml emails are not in that",
          "script")


if __name__ == "__main__":
    main()
