"""Given for lesson 01.4: reading the two files and printing the result."""
import csv
import re


def defined_types(path):
    """The type names in a definitions file: lines that start '## F-...'."""
    with open(path, encoding="utf-8") as f:
        return set(re.findall(r"^## (F-[\w-]+)", f.read(), re.M))


def coded_rows(path):
    """Rows of the coded file, skipping comment lines that start with #."""
    with open(path, encoding="utf-8", newline="") as f:
        lines = [line for line in f if not line.startswith("#")]
    return list(csv.DictReader(lines))


def print_report(rows, bad):
    """How many rows were read, how many problems, then each problem."""
    print(len(rows), "rows;", len(bad), "problems")
    for line in bad:
        print(" ", line)
