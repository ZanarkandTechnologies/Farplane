---
skill: recap-idea
date: 2026-08-28
change_type: behavior
owner: skill-maintenance
status: pass
before_ref: skills/recap-idea/SKILL.md@0.4.0
after_ref: working-tree
reasoning_basis: operator-correction
proof_artifacts:
  - skills/recap-idea/evals/evals.json
eval_required: yes
---

# Situation-Matched Visual Playback Audit

## Change

- Before: the skill prescribed an operated story, compact ASCII map, and six
  fixed response sections regardless of the operator's alignment question.
- After: the skill selects one fenced Mermaid view from the question,
  including Before/After/Example for deltas and user-visible screen-state flows
  for UI or design discussions.
- Preserved: proposed status, separation of decisions from assumptions and
  conflicts, recap-task boundary, and the ban on premature planning.

## Refinement Pass

| Unit | Decision | Reason |
| --- | --- | --- |
| Fixed six-section template | delete | Encouraged report-shaped output instead of question-shaped playback. |
| Operated story | merge | User operation is encoded in the selected journey or screen-state view. |
| ASCII default | rewrite | A fenced Mermaid diagram is the relationship default; tables remain valid for exact mappings. |
| Boundaries and uncertainty | keep | These expose semantic disagreement. |
| Alignment questions | keep | Human correction remains the finish gate. |

## Proof Plan

- Preserve the four existing routing and semantic cases.
- Update visual assertions from ASCII to situation-matched Mermaid.
- Add a UI case that rejects backend architecture and requires what the end
  user sees, does, and sees next.
- Run changed-eval lint, skill-system validation, focused behavior proof, and
  independent contract review.

## First Behavior Run

- Artifact: `.farplane/evals/runs/20260828T154909Z-recap-idea-visual-routing-20260828/summary.json`
- Result: 3/5 candidate cases passed.
- Useful failure: the UI case added ASCII screen simulations after its Mermaid
  flow; the skill now forbids that redundant supplement.
- Rubric repair: Promptfoo judges fenced Markdown source rather than the Codex
  app's rendered view, so assertions now test a fenced Mermaid diagram instead
  of claiming the grader can observe app-side rendering.
- Preservation repair: the conflict case now tests a representative visual
  user path and explicit affected boundary rather than requiring the deleted
  fixed prose sections.

## Focused Repair Runs

- Conflict: `.farplane/evals/runs/20260828T155719Z-recap-idea-conflict-rerun-20260828/summary.json` — 1/1 passed.
- UI flow: `.farplane/evals/runs/20260828T155719Z-recap-idea-ui-rerun-20260828/summary.json` — 1/1 passed.

## First Aggregate Rerun

- Artifact: `.farplane/evals/runs/20260828T164134Z-recap-idea-final-aggregate-20260829/summary.json`
- Result: 4/5 passed.
- Useful failure: compaction had removed the explicit `recap-task` route, so a
  status-only request borrowed unrelated local history. N1 now exits through
  `recap-task` or requests the authoritative task reference without resuming.

## Final Aggregate Proof

- Focused status repair: `.farplane/evals/runs/20260828T164738Z-recap-idea-status-route-repair-20260829/summary.json` — 1/1 passed.
- Final suite: `.farplane/evals/runs/20260828T164904Z-recap-idea-final-aggregate-v2-20260829/summary.json` — 5/5 passed, `candidate_gate_passed: true`.
- Static proof: changed-eval lint passed; skill registry, frontmatter,
  checklists, references, capabilities, surface budget, and template registry
  passed through `check_skills.py --write`.

## Independent Review

- Verdict: TAS-A / pass.
- Scope: skill contract, eval quality, evidence quality, and integration readiness.
- Blocking findings: none.
