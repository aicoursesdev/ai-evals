"""Lesson 02.5: find test emails inside the help desk's own prompt files.

Given: it calls your `find_leaks` on the prompt files and the launch set.
From this folder: uv run python find_leaks.py
"""
from leaks import find_leaks
from plumbing import launch_halves, prompt_sources


def main():
    sources = prompt_sources()
    test, dev = launch_halves()
    for name, part in (("test", test), ("dev", dev)):
        print(f"{len(part)} {name} emails against {len(sources)} "
              "prompt files")
        for found in find_leaks(part, sources):
            print("  ", *found)


if __name__ == "__main__":
    main()
