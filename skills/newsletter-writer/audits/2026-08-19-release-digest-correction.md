---
skill: newsletter-writer
date: 2026-08-19
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: .farplane/evals/runs/20260818-192751-newsletter-writer-release-digest-baseline/summary.json
after_ref: .farplane/evals/runs/20260818-193148-newsletter-writer-release-digest-final/summary.json
reasoning_basis: eval
proof_artifacts:
  - skills/newsletter-writer/examples/weekly-office-showcase/example.md
  - .farplane/evals/runs/20260818-192751-newsletter-writer-release-digest-baseline/summary.json
  - .farplane/evals/runs/20260818-193148-newsletter-writer-release-digest-final/summary.json
  - skills/newsletter-writer/audits/2026-08-19-release-digest-review.json
eval_required: yes
---

# Release-Digest Correction Audit

## Change

- Before: weekly product recaps were forced into one personal story, burying
  the shipped changes and contradicting the requested release-note format.
- After: `release-digest` groups verified changes into two to four impact
  themes and renders each as an indented `Changed / Impact / Evidence` unit.
- Why: the operator wants a fast, high-impact release summary, not a founder
  narrative.
- Tradeoff accepted: release digests optimize scanning over emotional arc;
  story-driven and educational modes remain available for editorial requests.

## First-Principles Reasoning

- Objective: make weekly AI-office progress legible in seconds without losing
  source truth or the human publication gate.
- Placement logic: `reuse_local`; the existing writer owns reader-facing form,
  so no new skill, automation, storage field, or dependency is justified.
- Expected behavior delta: a recap request selects `release-digest`, uses a
  factual opener, groups impact units, avoids invented personal experience, and
  permits zero CTAs.
- Proof needed: a natural regression case, baseline/candidate comparison,
  format-correct preview, skill-system validation, installed-copy match, and
  independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Release branch and structure are executable from `SKILL.md`. |
| `reference_load_precision` | pass | The showcase example is loaded only for Executive Update aggregation. |
| `missing_context_rate` | pass | Format selection, CTA rule, source gate, and output structure remain first-load behavior. |
| `noisy_context_rate` | pass | `SKILL.md` remains at the 200-line envelope. |
| `duplicated_instruction_count` | pass | Writer owns prose; Weekly Interval remains the evidence owner. |
| `prompt_size_tokens` | pass | No new reference is loaded on unrelated newsletter branches. |
| `task_success_rate` | pass | Full suite improved from 1/3 to 3/3 TAS-A. |
| `review_tas_rate` | pass | Independent review rerun returned TAS-A after installed-copy sync. |
| `maintenance_locality` | pass | Skill, QA, eval, example, and audit remain package-local. |
| `composition_clarity` | pass | Release digest inputs, gates, structure, and publication boundary are explicit. |

## Proof Artifacts

- Skill-local evals: final suite 3/3 TAS-A; release-digest case TAS-A.
- Structure evals: standard skill checks pass; `SKILL.md` is 200 lines.
- Reviewer receipt: `audits/2026-08-19-release-digest-review.json`.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Eval required: yes; this changes runtime format selection and output shape.
- Evidence gaps: no live Beehiiv voice examples; release format does not depend
  on a personal voice match.

## Before Behavior

- The unchanged skill scored 1/3 on the revised suite. The release case was
  TAS-B because it did not use indented units or separate change, impact, and
  evidence.

## After Behavior

- The final skill scored 3/3 TAS-A. The release case selected the correct
  format, used three impact groups, four blockquoted units, zero CTAs, explicit
  source gaps, and an unchanged approval gate.

## Followups

- Completed: installed the repo-owned skill and verified the live package has
  no differences from source. No remaining correction blocker.
