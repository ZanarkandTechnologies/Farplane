---
title: Taste Loop hypothesis cycle validator
owner: taste-loop
status: accepted
date: 2026-06-29
related:
  - skills/taste-loop/SKILL.md
  - skills/taste-loop/scripts/check_progress_hypothesis_cycles.py
  - tickets/TASK-0240/program.md
  - tickets/TASK-0240/progress.md
---

# Taste Loop Hypothesis Cycle Validator

## Trigger

Kenji wanted the autoresearch-style loop enforced mechanically: one workflow
ticket, one `program.md`, and an append-only `progress.md` ledger of hypothesis
cycles. The prior prompt-only contract could still allow workers to create a
fresh `TL-EXP-###` unit for every update.

## Delta

- Added `scripts/check_progress_hypothesis_cycles.py`.
- The validator activates when `program.md` declares
  `progress_unit = hypothesis_cycle`.
- It is tolerant of older historical `TL-EXP` entries, but after the
  correction marker it blocks fresh `TL-EXP` primary work units.
- It validates required fields for any `hypothesis_cycle:` block.
- Taste Loop now requires running the validator before recording waiting or
  terminal state when a ticket opts into hypothesis-cycle progress.

## Proof

```text
python3 skills/taste-loop/scripts/check_progress_hypothesis_cycles.py \
  tickets/TASK-0240/program.md \
  tickets/TASK-0240/progress.md
```

Result:

```text
taste-loop progress hypothesis cycles OK
```
