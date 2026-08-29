---
skill: recap-idea
date: 2026-08-29
change_type: behavior
owner: skill-maintenance
status: pass
before_ref: skills/recap-idea/audits/2026-08-28-situation-matched-visual-playback.md
after_ref: working-tree
reasoning_basis: operator-correction
proof_artifacts:
  - skills/recap-idea/evals/evals.json
  - skills/recap-idea/references/visual-templates.md
eval_required: yes
---

# Visual Template Routing Audit

## Change

- Before: `SKILL.md` named six visual forms but supplied only one short example.
- After: the skill detects the product shape, selects one stable template ID,
  and loads its concrete Mermaid or table example from a conditional reference.
- First-load cost: template bodies stay out of `SKILL.md`; its routing contract
  remains the complete normal path.

## Template Set

| ID | Verification target |
| --- | --- |
| `journey` | end-to-end experience |
| `ui-screen-flow` | what a user sees and does |
| `lifecycle` | state and recovery |
| `system-boundary` | ownership and information movement |
| `before-after-example` | experiential delta |
| `comparison-table` | exact correspondence |

## Proof Plan

- Preserve the five passing journey, conflict, recap, UI, and negative-routing cases.
- Add one delta case that must choose Before / After / Example rather than a
  generic journey or backend map.
- Run changed-eval lint, skill-system validation, focused behavior proof, and
  independent review.

## First Aggregate Run

- Artifact: `.farplane/evals/runs/20260828T165853Z-recap-idea-template-routing-final-20260829/summary.json`
- Result: 4/6 passed.
- Real failure: UI routing selected the right conceptual template but wrote an
  HTML prototype and returned a link instead of rendering the Mermaid template
  inline. N3 now forbids artifact substitution and asserts that the response
  itself contains the visual.
- Harness noise: the recap composition answer satisfied its semantic rubric
  but the skill-use heuristic reported no invocation; no contract change was
  made for that non-behavioral miss.

## Second Aggregate Run

- Artifact: `.farplane/evals/runs/20260828T171014Z-recap-idea-template-routing-final-v2-20260829/summary.json`
- Result: 5/6 passed; journey, conflict, recap, UI, delta, and status semantics
  were correct except for one legacy ordering assertion.
- Rubric repair: replaced “promise before capabilities” with a semantic check
  for a concise promise or central user value. The old ordering would force
  prose before the selected visual and contradict the visual-first contract.

## Third Aggregate Run

- Artifact: `.farplane/evals/runs/20260828T171733Z-recap-idea-template-routing-final-v3-20260829/summary.json`
- Result: 4/6 strict pass; every candidate response was behaviorally correct.
- Rubric repair: the delta case now checks the experiential shift instead of
  requiring the response to repeat the supplied persona label.
- Trigger repair: the recap-composition and status-boundary prompts now directly
  invoke the shortcut because those cases explicitly test its composition and
  rejection behavior; this removes skill-use heuristic noise from the proof.

## Fourth Aggregate Run

- Artifact: `.farplane/evals/runs/20260828T172447Z-recap-idea-template-routing-final-v4-20260829/summary.json`
- Result: 5/6 passed.
- Harness correction: directly naming the shortcut caused the composition case
  to select the operator's older globally installed copy instead of the isolated
  candidate package. The prompt now naturally requests visual playback and the
  right diagram so the candidate package owns the evaluated response. Repo
  source remains canonical; the installed copy was not modified.

## Fifth Aggregate Run

- Artifact: `.farplane/evals/runs/20260828T173400Z-recap-idea-template-routing-final-v5-20260829/summary.json`
- Result: 5/6 passed.
- Real failure: UI selected and rendered the correct Mermaid template, then
  duplicated its concrete screens as ASCII mockups. The UI template now keeps
  concrete examples inside Mermaid nodes and treats any following ASCII
  wireframe as a failed output.

## Sixth Aggregate Run

- Artifact: `.farplane/evals/runs/20260828T174409Z-recap-idea-template-routing-final-v6-20260829/summary.json`
- Result: 4/6 strict pass; all six selected or rejected the correct template path.
- Rubric repair: the journey case no longer invents “topic navigation” as the
  required destination for broad overlap; it tests only the supplied semantic
  boundary that broad overlap is not same-development coverage.
- Contract repair: N4 now requires one to three correction questions. “At most
  three” had allowed a semantically correct playback to end without explicitly
  inviting the operator to confirm or correct it.

## Final Evidence Packet

- Aggregate v7: `.farplane/evals/runs/20260828T175309Z-recap-idea-template-routing-final-v7-20260829/summary.json` — 5/6 strict pass.
- Focused journey repair: `.farplane/evals/runs/20260828T175156Z-recap-idea-journey-semantic-repair-20260829/summary.json` — 1/1 passed.
- Focused recap repair: `.farplane/evals/runs/20260828T175156Z-recap-idea-recap-semantic-repair-20260829/summary.json` — 1/1 passed against `.agents/skills/recap-idea/SKILL.md`.
- Focused UI no-ASCII repair: `.farplane/evals/runs/20260828T174141Z-recap-idea-ui-no-ascii-repair-20260829/summary.json` — 1/1 passed.
- Focused delta template: `.farplane/evals/runs/20260828T165738Z-recap-idea-delta-template-20260829/summary.json` — 1/1 passed.
- Aggregate limitation: the only v7 miss selected
  `/Users/kenjipcx/.codex/skills/recap-idea/SKILL.md`, the stale installed
  copy, instead of the isolated candidate. No repo behavior fix can correct
  that external evaluator binding without changing installed operator state.
- Static proof: changed-eval lint and all 12 skill-system checks pass.

## Independent Review Round 1

- Verdict: TAS-B / revise.
- Blocking gap: lifecycle, system-boundary, and comparison-table were named but
  lacked direct behavior proof.
- Contract gap: output wording implied every visual was Mermaid even though
  exact correspondence intentionally uses a Markdown table.
- Repair: output now says situation-matched visual, usually Mermaid, and three
  focused evals cover the previously unproved branches.

## Missing-Branch Proof

- Lifecycle: `.farplane/evals/runs/20260828T180303Z-recap-idea-lifecycle-template-20260829/summary.json` — 1/1 passed.
- System boundary: `.farplane/evals/runs/20260828T180303Z-recap-idea-boundary-template-20260829/summary.json` — 1/1 passed.
- Comparison table: `.farplane/evals/runs/20260828T180303Z-recap-idea-comparison-template-20260829/summary.json` — 1/1 passed.

## Independent Review Round 2

- Verdict: TAS-A / pass.
- Skill contract, evidence quality, and integration readiness passed.
- Blocking findings: none.
