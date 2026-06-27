---
skill: infographic
date: 2026-06-27
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/infographic/examples/workforce-pulse-handdrawn-saas.md
after_ref: skills/infographic/examples/handdrawn-saas-wireframe/example.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/infographic/examples/handdrawn-saas-wireframe/assets/reference.png
  - skills/infographic/examples/handdrawn-saas-wireframe/assets/good-output.png
eval_required: no
---

# Skill Audit

## Change

- Before: The positive example lived in one Markdown file while the reference
  image lived in a separate `assets/examples/` path, and the accepted dense
  output was only available in the TASK-0238 proof artifacts.
- After: The hand-drawn SaaS method has a package-shaped fixture at
  `examples/handdrawn-saas-wireframe/example.md` with local `assets/` for the
  reference image, accepted output PNG, and deterministic SVG source.
- Why: The skill needs qualitative comparison against both a taste reference and
  a known-good dense output to avoid sparse sketch outputs.
- Tradeoff accepted: Keep this as a docs convention and skill-local fixture
  instead of adding registry fields or automated image comparison tooling now.

## First-Principles Reasoning

- Objective: Make the infographic skill usable standalone for the referenced
  dense hand-drawn SaaS style.
- Placement logic: The example is skill-specific and asset-backed, so it
  belongs under the skill package rather than cross-skill docs or eval fixtures.
- Expected behavior delta: Future invocations can load one example file to find
  the style reference, good output, comparison gates, and provenance.
- Proof needed: Final tree inspection plus skill/docs validators.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` links the fixture and method reference. |
| `reference_load_precision` | pass | Detailed style gates remain in `references/handdrawn-saas-wireframe.md` and the example fixture. |
| `missing_context_rate` | pass | Fixture includes reference, good output, gates, and provenance. |
| `noisy_context_rate` | pass | Asset-backed detail is outside first-load prose. |
| `duplicated_instruction_count` | pass | Old split example file and asset path were removed. |
| `prompt_size_tokens` | pass | `SKILL.md` received only a short fixture link. |
| `task_success_rate` | unknown | No new behavioral eval was run; existing eval target remains routing-oriented. |
| `review_tas_rate` | unknown | Self-check only; no independent reviewer for this narrow fixture migration. |
| `maintenance_locality` | pass | Fixture assets live with the owning example. |
| `composition_clarity` | pass | Method reference points at the new fixture asset path. |

## Proof Artifacts

- Skill-local evals, when needed: not changed.
- Structure evals, when needed: `check_skills.py --write`.
- Reviewer receipt: not used for this narrow rollout.
- Validator: `check_doc_refs.py`.
- Eval required: no; structural packaging change.
- Evidence gaps: Automated qualitative comparison remains future work.

## Before Behavior

- Agents could find a positive example and a reference image, but the assets
  were split and the accepted dense output was not part of the skill package.

## After Behavior

- Agents can load `examples/handdrawn-saas-wireframe/example.md` and find the
  input brief, reference asset, accepted output, comparison gates, and
  provenance in one fixture.

## Followups

- Consider a visual comparison runner only after at least two more
  quality-dependent skills adopt the fixture convention.
