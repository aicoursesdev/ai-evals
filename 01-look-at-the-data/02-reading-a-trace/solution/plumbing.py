"""Given for lesson 01.2: the printing for view.py.

`wrap` fits text to 78 columns; `show` prints one trace in the order the help
desk worked: email, labels, pages, draft, citations.
"""
import textwrap


def wrap(text):
    """Wrap each line to 78 columns, keeping line breaks and blank lines."""
    return "\n".join(textwrap.fill(line, 78) for line in text.split("\n"))


def show(email, trace, chunks=False):
    print(f"{email['id']}  week {email['week']}  {email['language']}  "
          f"from {email['from_name']}")
    print(f"Subject: {email['subject']}\n")
    print(wrap(email["body"]))
    print("\nArjun's labels :", {k: email[k] for k in
                                  ("category", "urgency", "needs_human")})
    print("Help desk said :", trace["triage"])
    print("\nPages it fetched:")
    for hit in trace["retrieved"]:
        title = hit["chunk"].split("\n")[0].lstrip("# ")
        print(f"  {hit['article_id']:<22} {hit['score']:.2f}  {title}")
        if chunks:
            print(textwrap.indent(wrap(hit["chunk"]), "      "))
    print("\nThe draft:\n")
    print(wrap(trace["draft"]))
    print("\nCited:", trace["citations"] or "nothing")
    if trace.get("error"):
        print("\nError:", wrap(trace["error"]))
