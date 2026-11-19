# AI Evals: the course repo

Code and data for the AI Evals course on [aicourses.dev](https://aicourses.dev). Over the course you measure one product: the AI help desk of **Tidewater Goods**, an imaginary shop in Kochi that sells rain and outdoor gear. The shop, its staff, customers, orders and emails are all invented. Every answer the help desk gives in this repo is real model output, recorded once and kept, so the numbers in the lessons are the numbers you get.

## Set up

You need [uv](https://docs.astral.sh/uv/) (it installs Python for you) and git.

```sh
git clone https://github.com/aicoursesdev/ai-evals.git
cd ai-evals
uv sync          # installs Python packages into .venv
make doctor      # checks your laptop and settings, then plays a recorded reply
```

**You do not need a model to take the course.** Every run a lesson uses is recorded under `data/`: the help desk's reply to each of 750 emails, the judge's verdicts, the repeats, the attacks. The lessons' scripts and tests replay those recordings, with no network.

To rerun anything yourself, install [Ollama](https://ollama.com), then `ollama pull qwen3.5:4b` and `ollama pull qwen3-embedding:0.6b`, and copy `.env.example` to `.env`. To use another provider, put its `LLM_BASE_URL`, `LLM_API_KEY` and `LLM_MODEL` in `.env`; your scores will then differ from the lessons', which is the point of an eval. `.env` holds your keys. It is in `.gitignore`: never commit it.

## What is here

- `helpdesk/`: the system under test. It labels an email (triage), finds help-centre pages, drafts a reply, and has a small refund agent. Its versions are folders of prompts and settings under `helpdesk/versions/`; the course compares `hd-1` with `hd-2`.
- `scorecard/`: the eval library the course builds, one module at a time: loading data, code checks, a model judge, statistics, retrieval and agent metrics, a gate and a report. It ships finished, so any lesson runs even if you skipped an earlier one. See `scorecard/README.md`.
- `data/`: the shop's help centre, four weeks of logged emails with labels, the recorded runs, people's calls on the drafts, and the test set. `data/README.md` describes every file and how it was recorded.
- `scripts/doctor.py` is the setup check behind `make doctor`; `scripts/lesson.py` is the lesson runner behind `make check`, `make diff` and `make test`; `scripts/record.py` re-records any run; `scripts/check_data.py` checks that every data file agrees with the others.
- One folder per module (`03-graders/`), and in it one folder per lesson with code (`02-code-graders/`).

## Work through a lesson

A lesson folder holds two folders: `start/`, your working copy, with the lesson's part left as `TODO`s, and `solution/`, the same files finished. The lesson's tests sit in both, the same.

1. Go into the lesson's `start/` folder, for example `cd 03-graders/02-code-graders/start`, write the TODOs, and run your files there with `uv run python hand_checks.py`.
2. Back in the repo's top folder (`cd ../../..`), `make check 03.2` runs the lesson's tests with no model and no network. A failing test names the TODO to do next, and when all pass it prints `all tests pass. Done.`
3. Stuck? `make diff 03.2` shows only what `solution/` has that your `start/` does not; or open `solution/` and read.

On Windows, where there is no `make`, type the long form: `uv run python scripts/lesson.py check 03.2` (add `--solution` to run the tests on `solution/`) and `uv run python scripts/lesson.py diff 03.2`. `uv run python scripts/lesson.py list` shows every lesson folder and what is in it. `make test` runs every solution's tests and the two packages' own, as the repo's checks on GitHub do.

## The sealed test set

`data/testsets/v1/` holds the test set the course builds in Module 02: an open part of 100 emails you may read, a made-up part of 20, and a **sealed part of 50** that is scored once, in Module 10. In Modules 00 to 09 nothing reads what the help desk wrote for a sealed email: the loader `scorecard.graders.logged` skips those lines without parsing them, the recorder refuses them, and the lessons' tests fail if a script opens one.

The course's own opening is recorded in `data/runs/10-sealed/`, with the plan that was written before it. If you want that final score to mean something for you, leave that folder and the sealed traces alone until Module 10 tells you to open them. Module 02 explains why a peek spends the test.
