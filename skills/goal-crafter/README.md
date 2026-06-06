# goal-crafter

## Purpose

`goal-crafter` turns fuzzy operator intent into a paste-ready native Codex
`/goal` command with an outcome, proof surface, constraints, boundaries,
iteration policy, and blocked-stop condition.

It can draft Goal contracts for `$work`, `$ralph`, `batch-work`, metric loops,
and figure-it-out unblock runs.

When a ticket, plan, or Proof Contract already exists, it should compile the
known fields into `GoalPrepState` and ask only missing execution-safety
questions. It should not restart product discovery.

## Public API

- `SKILL.md`: the loaded skill contract.
- `SKILL.md` Todo List: the todo list used while drafting a goal.
- `fixtures/goal-prep-cases.md`: expected behavior examples for ticket-backed
  state, proxy rejection, quantified issue hunts, and tiny direct asks.

## Minimal Example

Ask for a goal when the desired outcome is clear enough to pursue, but the
stopping rule is still soft:

```text
Use goal-crafter to turn "make this demo work even if I am away" into a
paste-ready /goal.
```

Ticket-backed prep:

```text
Use goal-crafter on tickets/TASK-1234/ticket.md and preserve the Proof Contract
as GoalPrepState.
```

## How to Test

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
```
