"""Lesson 00.3: run cases through a system, grade, save and load.

The course's own finished version is scorecard/run.py.
"""
import json


def run(cases, system, graders):
    rows = []
    for case in cases:
        output = system(case)
        row = {"id": case.get("id"), "output": output}
        for name, grader in graders.items():
            row[name] = bool(grader(output, case))
        rows.append(row)
    return rows


def save(results, path):
    with open(path, "w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def pass_rate(results, grader):
    return sum(row[grader] for row in results) / len(results)
