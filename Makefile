.PHONY: doctor check diff test

# Checks your laptop, your settings and your model, then plays a recorded reply.
doctor:
	uv run python scripts/doctor.py

# make check 03.2              runs the lesson's tests on your code in start/
# make check 03.2 SOLUTION=1   runs the same tests on solution/
check:
	uv run python scripts/lesson.py check $(word 2,$(MAKECMDGOALS)) $(if $(SOLUTION),--solution)

# make diff 03.2               shows what solution/ has that start/ does not
diff:
	uv run python scripts/lesson.py diff $(word 2,$(MAKECMDGOALS))

# make test                    every lesson's solution, then the helpdesk and scorecard packages
test:
	uv run python scripts/lesson.py all
	uv run pytest -q helpdesk/tests scorecard/tests

# `make check 03.2` passes the lesson number as a second goal; this rule lets it through quietly.
%:
	@:
