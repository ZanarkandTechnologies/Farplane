# `skills/demo-realism/AGENTS.md`

Local rules for the `demo-realism` skill.

- Keep this skill upstream of final design/build. It owns realism synthesis, not execution.
- Prefer believable operating assumptions over generic placeholder examples.
- Treat aggressive inference as allowed, but never phrase the result like verified client truth.
- Every output should connect:
  - operator
  - workflow
  - screen/state
  - data
- If the realism pack is still vague at the workflow level, do not jump to screen-level examples yet.
- If the realism pack is good enough, hand off to `functional-ui`, `frontend-design`, `impl-plan`, or `impl` instead of expanding scope here.
