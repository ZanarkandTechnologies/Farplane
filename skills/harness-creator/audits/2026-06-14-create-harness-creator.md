---
skill: harness-creator
date: 2026-06-14
change_type: structure
owner: skill-creator
status: draft
review_route: self_check
before_ref: skills/business-harness/SKILL.md
after_ref: skills/harness-creator/SKILL.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - .farplane/automation/decisions/2026-06-13-harness-creator/decision.md
  - tickets/TASK-0201/ticket.md
  - skills/harness-creator/SKILL.md
  - skills/harness-creator/references/harness-il.md
  - farplane/goals.md
eval_required: no
---

# Skill Audit

## Change

- Before: A scratch `business-harness` skill framed the problem as business
  launch only.
- After: `harness-creator` frames the reusable primitive as high-level goal to
  task-specific harness, with HarnessIL as durable intermediate language and
  `goal-advisor` as downstream leaf compiler.
- Why: The operator clarified that both a template intra-language and a skill
  for choosing each harness parameter are needed.
- Tradeoff accepted: The skill is experimental and pilot-gated rather than
  claiming broad autonomous domain bootstrapping immediately.

## First-Principles Reasoning

- Objective: Let Farplane design a harness around a high-level goal before
  execution.
- Placement logic: Repeated procedure belongs in a Tier 3 skill; durable
  filled state belongs in Markdown templates/artifacts; Goal execution remains
  with `goal-advisor`.
- Expected behavior delta: Agents should fill HarnessIL, map capabilities,
  decide missing primitive actions, and hand one selected frontier to
  `goal-advisor`.
- Proof needed: Skill validators, structure QA, and a pilot against the
  faceless AI/harness engineering channel.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes trigger, signature, todo path, gates, routes, gotchas, output. |
| `reference_load_precision` | pass | Every reference/template has a read/copy condition in the todo or Reference Map. |
| `missing_context_rate` | pass | HarnessIL fields, side-effect gates, skill inventory, lever choice, and handoff are first-load obligations. |
| `noisy_context_rate` | pass | Field detail and long schemas live in `references/` and `templates/`. |
| `duplicated_instruction_count` | pass | `harness-creator` designs harnesses; `goal-advisor` compiles leaves; `harness-advisor` handles placement. |
| `prompt_size_tokens` | pass | First-load file remains below the rough 250-line threshold. |
| `task_success_rate` | unknown | Needs pilot. |
| `review_tas_rate` | unknown | Needs review before non-experimental promotion. |
| `maintenance_locality` | pass | New package owns the skill, IL reference, templates, example, and audit. |
| `composition_clarity` | pass | Signature names inputs, outputs, state, gates, routes, and failures. |

## Proof Artifacts

- Skill-local evals, when needed: defer until pilot exposes stable hardcases.
- Structure evals, when needed: none.
- Reviewer receipt: TAS-A finish-readiness review for TASK-0201 returned no
  blocking findings.
- Validator: `check_skills.py --write`,
  `check_skill_todo_tiers.py --allow-peer-tier3`, and
  `sync_skill_registry.py --check` passed on 2026-06-14.
- Eval required: not for first scaffold; likely after pilot.
- Evidence gaps: pilot has not yet run.

## Before Behavior

- Agents had to manually connect high-level goals to research, skill inventory,
  missing primitive planning, portfolio state, and Goal Advisor handoff.

## After Behavior

- `harness-creator` owns that design procedure and writes the result into a
  visible harness portfolio / HarnessIL packet.

## Followups

- Run TASK-0201 pilot handoff for the faceless AI/harness engineering channel.
- Add an eval row after the pilot identifies concrete pass/fail behavior.
