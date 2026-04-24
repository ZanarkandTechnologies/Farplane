# QA

Proof-gathering execution phase for one selected ticket.

Use `$qa` to collect evidence under `tickets/artifacts/TASK-XXXX/qa/`, update the ticket `Evidence` section, write `result.json`, and finish with `IMPL_RESULT: status=qa_complete ...`.

When the repo has a visible `qa/` module, read `qa/README.md` and the relevant
`qa/cookbook/*.md` page before driving the browser. Reusable shortcuts, deep
links, fixtures, and test hooks belong there; per-run artifacts still belong
under `tickets/artifacts/TASK-XXXX/qa/`.
