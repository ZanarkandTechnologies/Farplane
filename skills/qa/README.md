# QA

Proof-gathering execution phase for one selected ticket.

Use `$qa` to collect evidence under `tickets/TASK-XXXX/artifacts/qa/`, update
the ticket `Links` or `State` section, write `result.json`, and finish with
`IMPL_RESULT: status=qa_complete ...`.

When `$qa` is invoked from a live `$impl` coordinator lane, keep browser driving delegated to `qa-tester` instead of using `agent-browser` directly from the coordinator session.

When the repo has a visible `qa/` module, read `qa/README.md` and the relevant
`qa/cookbook/*.md` page before driving the browser. Reusable shortcuts, deep
links, fixtures, and test hooks belong there; per-run artifacts still belong
under `tickets/TASK-XXXX/artifacts/qa/`.
