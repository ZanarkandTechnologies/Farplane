---
name: pr-runtime
version: 0.1.0
description: "Turn PR follow-up or separate-writer work into an isolated checkout and ticket runtime record."
tier: 3
group: coding
source: local
allowed-tools: Read, Glob, Grep
---

# PR Runtime

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the selected ticket, branch/PR context, compute target, QA needs, and
  any existing `.farplane/state/tickets/*.runtime.json` record.
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
- [ ] Keep runtime state under `.farplane/state/`; do not write live ports or
  transient targets into tracked docs.
- [ ] Record the selected checkout mode, runtime mode, runtime record path, QA
  target, and reason in the owning ticket or handoff.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use when the task is modifying an existing PR branch, when multiple live
writers would otherwise share one filesystem, or when QA needs a declared
ticket-scoped target instead of guessed ports.

This skill is not a git tutorial. It standardizes when isolation is required,
where runtime state lives, how ticket runtime commands are launched, and how QA
reads the target.

## First-Load Contract

### Trigger Conditions

- user asks to address PR comments or update an existing PR branch
- more than one live writer would otherwise share one filesystem
- the task needs a ticket-scoped frontend/backend target for QA

### Workflow

1. Resolve the ticket, PR branch, or working branch.
2. Decide whether the task can stay `shared` or needs `worktree` checkout mode.
3. Decide runtime mode:
   - `shared`
   - `branch-runtime`
   - `branch-compose`
4. Run the helper to create or refresh the runtime record.
5. If isolated checkout is required, create or reuse it through the helper.
6. If QA needs a live target, run `up` with the declared frontend/backend or
   compose command set.
7. Publish live QA targets through the runtime record.
8. Do the work.
9. Hand QA the runtime record instead of telling it to infer local ports.

### Core Decision Branches

- `existing PR branch` -> use isolated checkout by default
- `multiple live writers` -> use isolated checkout
- `single writer, low-risk local work` -> shared checkout is allowed
- `DB or risky integration work` -> prefer `branch-compose`
- `ordinary UI/API work needing ticket-scoped QA` -> prefer `branch-runtime`

### Top 3 Gotchas

1. Treating a branch name as filesystem isolation when two live writers still
   share the same checkout.
2. Storing live ports or runtime targets in tracked repo files instead of
   `.farplane/state/`.
3. Making QA guess the correct target from chat instead of reading the runtime
   record.

### Outcome Contract

When this skill is used, return:

1. `Best:` chosen checkout mode and runtime mode
2. `Runtime record:` path under `.farplane/state/`
3. `QA target:` live frontend/backend target or explicit `none`
4. `Why:` one short line explaining why isolation was or was not required

## Guardrails

- Never allow more than one live writer in the same filesystem.
- Tickets remain the durable task surface; runtime records stay under
  `.farplane/state/`.
- Existing PR branch follow-up should default to isolated checkout.
- Hand QA live frontend/backend targets through the runtime record so
  [qa](../qa/SKILL.md) does not infer ports, processes, or worktrees from chat.
- Keep the runtime helper local-first and minimal; do not expand this skill
  into generic dispatch or cloud orchestration.
- Use the lightest sufficient runtime mode.

## Helper Surface

Use:

- `python3 bin/ticket_runtime.py ensure ...`
- `python3 bin/ticket_runtime.py up ...`
- `python3 bin/ticket_runtime.py status ...`
- `python3 bin/ticket_runtime.py qa ...`
- `python3 bin/ticket_runtime.py down ...`

Runtime records live at:

- `.farplane/state/tickets/TASK-XXXX.runtime.json`

Port reservations live at:

- `.farplane/state/ports.json`

## Minimal Example

```bash
python3 bin/ticket_runtime.py up \
  --ticket TASK-0123 \
  --branch pr-123 \
  --checkout-mode worktree \
  --runtime-mode branch-runtime \
  --create-worktree \
  --reserve frontend \
  --reserve backend \
  --frontend-cmd "npm run dev" \
  --backend-cmd "npm run api" \
  --json

python3 bin/ticket_runtime.py qa --ticket TASK-0123 --json
python3 bin/ticket_runtime.py down --ticket TASK-0123 --json
```
