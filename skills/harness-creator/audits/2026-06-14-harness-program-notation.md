---
skill: harness-creator
date: 2026-06-14
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/harness-creator/templates/project-harness.md
after_ref: skills/harness-creator/templates/project-harness.md
reasoning_basis: advise
proof_artifacts:
  - skills/harness-creator/references/harness-il.md
  - skills/harness-creator/templates/project-harness.md
  - skills/harness-creator/examples/faceless-ai-channel.md
  - docs/specs/program-notation.md
eval_required: no
---

# Skill Audit

## Change

- Before: The project harness template was table-heavy and `HarnessIL` read
  like a second schema beside the output.
- After: The output is a compact fenced `harness-program` block inside
  `project-harness.md`, with Markdown reserved for evidence, assumptions, open
  questions, and review.
- Why: The operator wants to program a business in a compressed notation, not
  fill out a sprawling Markdown plan.
- Tradeoff accepted: The notation is a tiny DSL-like language, but the
  operator-facing name is `Harness Program` to avoid weird IL/DSL branding.

## First-Principles Reasoning

- Objective: Make the harness output compact, grounded, and programmable.
- Placement logic: `SKILL.md` names the behavior, `harness-il.md` defines the
  compact notation, and `project-harness.md` is the filled program artifact.
- Expected behavior delta: Agents should lead with one `harness-program` block
  instead of large tables, and should cite facts through evidence refs.
- Proof needed: Skill-system validators and manual inspection for nested fence
  correctness, source-of-truth clarity, and no hidden runtime claims.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` says the `harness-program` block is the compact source of truth. |
| `reference_load_precision` | pass | `SKILL.md` points to `references/harness-il.md` before writing notation. |
| `missing_context_rate` | pass | Metric honesty, side-effect gates, and Goal Advisor boundaries remain in first load. |
| `noisy_context_rate` | pass | Grammar and examples live outside `SKILL.md`. |
| `duplicated_instruction_count` | pass | The reference owns grammar; the template owns fillable artifact shape. |
| `prompt_size_tokens` | pass | `SKILL.md` remains around the structure-review threshold and keeps only normal-path rules. |
| `task_success_rate` | unknown | Needs pilot. |
| `review_tas_rate` | unknown | No independent reviewer lane run. |
| `maintenance_locality` | pass | Future notation edits belong in `references/harness-il.md`. |
| `composition_clarity` | pass | `project-harness.md` remains the artifact; Goal Advisor compiles frontier only. |

## Proof Artifacts

- Skill-local evals, when needed: not required.
- Structure evals, when needed: standard skill validators.
- Reviewer receipt: local self-check only.
- Validator: final command output belongs in implementation closeout.
- Eval required: no.
- Evidence gaps: one real pilot should test whether the notation is compact
  enough and not too cute.

## Before Behavior

- Agents could produce a verbose Markdown harness where tables became the
  source of truth and the IL reference felt redundant.

## After Behavior

- Agents should produce one compressed Harness Program plus an evidence wrapper.

## Followups

- Pilot the notation on the faceless AI channel.
- After pilots, decide whether to add a lightweight parser or validator for
  required `harness-program` nodes.
