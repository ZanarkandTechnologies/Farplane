---
skill: solution-shaping
date: 2026-07-06
change_type: structure
owner: skill-creator
status: pass
review_route: self_check
before_ref: none
after_ref: skills/solution-shaping/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/solution-shaping/eval_task.json
  - skills/solution-shaping/examples/static-calculator-solution-brief/example.md
eval_required: yes
---

# Skill Audit

## Change

- Before: No parent skill owned agency-style complaint or outreach target to
  realistic MVP brief and handoff.
- After: `solution-shaping` owns the product-level synthesis from reported or
  inferred problem to MVP brief, proof model, and downstream route.
- Why: Existing skills handle brainstorming, PRD, system design, demo realism,
  and implementation planning, but not the whole complaint-to-reviewable-MVP
  product workflow.
- Tradeoff accepted: Adds one Tier 3 product workflow while keeping reusable
  problem framing in the Tier 2 `problem-framing` skill.

## First-Principles Reasoning

- Objective: let an autonomous agency team turn problem reports or outreach
  signals into realistic MVP proposals without overbuilding or inventing facts.
- Placement logic: Tier 3 because this is a concrete product/agency workflow
  that composes Tier 2 framing and research with downstream PRD/ticket owners.
- Expected behavior delta: agents produce reviewable MVP briefs with proof and
  routing instead of raw feature pitches.
- Proof needed: skill-local eval cases for complaint, outreach, and system-heavy
  MVP routing.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes context, signature, todo path, templates, routes, and gotchas. |
| `reference_load_precision` | pass | Only example reference is linked as a quality reference. |
| `missing_context_rate` | pass | Problem frame, grounding, MVP boundary, proof, and handoff gates are first-load. |
| `noisy_context_rate` | pass | Detailed example is in fixture rather than first load. |
| `duplicated_instruction_count` | pass | The skill composes but does not duplicate `problem-framing`, `prd`, or `impl-plan`. |
| `prompt_size_tokens` | pass | First load is below the review pressure threshold. |
| `task_success_rate` | unknown | Eval cases added; runner not executed in this audit. |
| `review_tas_rate` | unknown | No independent reviewer lane run. |
| `maintenance_locality` | pass | Product-level solution-shaping synthesis has one package owner. |
| `composition_clarity` | pass | Signature names outputs, gates, routes, and fails. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/solution-shaping/eval_task.json`
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Reviewer receipt: not run; self-check only for initial package creation.
- Validator: registry/skill validation command noted above.
- Eval required: yes.
- Evidence gaps: no live agent-behavior test yet.

## Before Behavior

- Agents had to improvise across `brainstorm`, `prd`, `demo-realism`,
  `functional-ui`, and `impl-plan` when the real output was an agency MVP
  brief.

## After Behavior

- Agents can call `solution-shaping` to frame the problem, ground the
  opportunity, choose a realistic MVP, name proof, and route to PRD, design,
  implementation, or Goal execution.

## Followups

- Run behavior evals or a clean-room `agent-behavior-test` after registry
  validation.
