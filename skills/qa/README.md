# QA

The one Delivery proof skill. `$qa` proves a GitHub issue's `Done / Proof` and
`QA Strategy` in one of three modes and, after a pass, records the closeout
demo:

- `functional` (default): claim-matched evidence through the real mechanism;
  browser operation is delegated to `qa-tester`.
- `visual`: four-part judgment of captured UI against `design.md`
  ([references/visual.md](references/visual.md)).
- `adversarial`: separate tester and evidence-review lanes attack a claim
  ([references/adversarial.md](references/adversarial.md)).
- `closeout: demo`: the Before/After/Example MP4 that leads the closing proof
  comment ([references/closeout-demo.md](references/closeout-demo.md)).

Per-run artifacts go under `.farplane/qa/<issue>/<run>/`; the verdict and
strongest evidence go on the issue with `gh issue comment`. Every run writes a
canonical `result.json` checked by `scripts/validate_qa_result.py` and ends
with `QA_RESULT: verdict=... evidence=... reason=...`.

Read [references/guide.md](references/guide.md), the project's `AGENTS.md`
Agent QA section, and any matching `docs/qa/*.md` page before driving the
browser. Reusable shortcuts, deep links, fixtures, and test hooks belong there.

Test: `.venv/bin/python -m unittest discover -s skills/qa/scripts -p "test_*.py"`.
