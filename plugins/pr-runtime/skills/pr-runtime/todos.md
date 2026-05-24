# Todos

- [ ] Read the selected ticket, branch/PR context, compute target, QA needs, and
  any existing `.harness/state/tickets/*.runtime.json` record.
- [ ] Use [plan](../plan/SKILL.md) when checkout mode, runtime mode, or compute
  target is a real decision.
- [ ] Decide checkout mode: shared checkout, isolated worktree, or existing
  branch/runtime workspace.
- [ ] Decide runtime mode: `shared`, `branch-runtime`, or `branch-compose`.
- [ ] Use the lightest sufficient helper command:
  `python3 bin/ticket_runtime.py ensure|up|status|qa|down`.
- [ ] If QA needs a live frontend/backend target, publish it through the runtime
  record instead of chat-only port notes.
- [ ] Hand the runtime record to [qa](../qa/SKILL.md) so browser/API evidence
  runs against the declared target.
- [ ] Keep runtime state under `.harness/state/`; do not write live ports or
  transient targets into tracked docs.
- [ ] Record the selected checkout mode, runtime mode, runtime record path, QA
  target, and reason in the owning ticket or handoff.
