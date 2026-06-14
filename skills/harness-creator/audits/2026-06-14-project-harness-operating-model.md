---
skill: harness-creator
date: 2026-06-14
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/harness-creator/SKILL.md
after_ref: skills/harness-creator/SKILL.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - docs/specs/program-notation.md
  - skills/harness-creator/references/harness-il.md
  - skills/harness-creator/templates/project-harness.md
eval_required: no
---

# Skill Audit

## Change

- Before: `harness-creator` produced a generic harness portfolio plus optional
  capability, missing-primitive, and Goal Advisor handoff sidecars.
- After: `harness-creator` now defaults to one `project-harness.md` operating
  file that carries values, goal weights, strategy axes, KPIs, metric-provider
  honesty, Scrum-style heartbeats, skill gaps, missing systems, and the current
  Goal Advisor frontier.
- Why: The operator clarified that the useful primitive is not a business-only
  scheduler, but a values-first project harness that uses standard systems
  where known and delegates leaf execution to Goal Advisor.
- Tradeoff accepted: The first-load skill grew slightly to prevent drift on
  metric honesty, board-drain priority, Deep Init Project boundaries, and
  hidden-automation gates.

## First-Principles Reasoning

- Objective: Make a high-level project or business idea immediately
  convertible into a visible operating harness.
- Placement logic: Put normal-path routing and gates in `SKILL.md`; put the
  detailed IL in `references/harness-il.md`; put the operator-facing config in
  `templates/project-harness.md`.
- Expected behavior delta: Agents should emit a compact one-file harness before
  spawning Goal work, drain proceedable tickets before proactive gaps, and mark
  absent metrics as `missing_instrumentation`.
- Proof needed: Skill structure checks, doc refs, registry sync, and manual
  inspection for hidden autonomy or fake metrics.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names signature, gates, routes, heartbeats, output contract, and gotchas. |
| `reference_load_precision` | pass | `SKILL.md` names when to load `harness-il.md`, `project-harness.md`, sidecar templates, Goal Advisor, Deep Init Project, and weekly strategy analysis. |
| `missing_context_rate` | pass | Metric honesty, board-drain priority, missing systems, and side-effect gates remain in first load. |
| `noisy_context_rate` | pass | Detailed axis semantics and one-file config rows live in reference/template files. |
| `duplicated_instruction_count` | pass | `SKILL.md` owns routing; `harness-il.md` owns semantics; `project-harness.md` owns artifact shape. |
| `prompt_size_tokens` | pass | First load remains a single skill contract with references for detail. |
| `task_success_rate` | unknown | No post-change pilot run yet. |
| `review_tas_rate` | unknown | No independent reviewer lane run in this pass. |
| `maintenance_locality` | pass | Future edits have clear owners: skill routing, IL semantics, or template rows. |
| `composition_clarity` | pass | `deep-init-project` and `goal-advisor` are explicit subfunction routes. |

## Proof Artifacts

- Skill-local evals, when needed: not needed for this structure-only update.
- Structure evals, when needed: standard validators.
- Reviewer receipt: not run; self-check used for this approved local update.
- Validator: pending at audit creation; final command output belongs in the
  implementation closeout.
- Eval required: no.
- Evidence gaps: pilot proof still needed across channel, mission/academy/lab,
  and profit/ecommerce or internal-ops cases before canonicalizing the model.

## Before Behavior

- A harness run could still read like generic domain discovery plus several
  sidecars, with automation previews and KPIs less tightly tied to values,
  strategy, and existing tickets.

## After Behavior

- A harness run starts from values, goal weights, mode presets, strategy axes,
  KPIs, metric providers, missing systems, Scrum heartbeats, and one current
  frontier. Parent coordination remains heartbeat/manual; leaf execution
  belongs to Goal Advisor.

## Followups

- Pilot `project-harness.md` on the faceless AI channel.
- After at least two pilots, decide whether a validator should check required
  project-harness sections.
