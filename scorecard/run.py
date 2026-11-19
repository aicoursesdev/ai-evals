"""Run cases through a system, grade each output, save and load results."""
import json


def run(cases, system, graders):
    """Call system(case) for each case; apply each named grader.

    graders is {name: grader(output, case) -> bool}. Each row holds the
    case id, the output and one True/False per grader name.
    """
    rows = []
    for case in cases:
        output = system(case)
        row = {"id": case.get("id"), "output": output}
        for name, grader in graders.items():
            row[name] = bool(grader(output, case))
        rows.append(row)
    return rows


def save(results, path):
    """Write result rows as one JSON object per line."""
    with open(path, "w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load(path):
    """Read result rows written by save."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def pass_rate(results, grader):
    """Share of rows where the named grader passed. [T, F] gives 0.5."""
    return sum(row[grader] for row in results) / len(results)
