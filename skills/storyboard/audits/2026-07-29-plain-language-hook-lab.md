---
skill: storyboard
date: 2026-07-29
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: .farplane/evals/runs/20260728-175059-storyboard-hook-heldout-baseline-2026-07-29
after_ref: .farplane/evals/runs/20260728-174915-storyboard-hook-heldout-r3-2026-07-29
reasoning_basis: eval
proof_artifacts:
  - .farplane/evals/runs/20260728-173220-storyboard-hook-baseline-2026-07-29/summary.json
  - .farplane/evals/runs/20260728-174114-storyboard-hook-candidate-r7-2026-07-29/summary.json
  - .farplane/evals/runs/20260728-175059-storyboard-hook-heldout-baseline-2026-07-29/summary.json
  - .farplane/evals/runs/20260728-174915-storyboard-hook-heldout-r3-2026-07-29/summary.json
eval_required: yes
---

# Plain-Language Hook Lab Hardening

## Change

- Before: Storyboard required one `Hook:` narrative signature but did not
  generate alternatives, compare the source title, translate jargon, or prove
  the first three seconds.
- After: Short-form, latest-news, title-led, and retention-sensitive work runs
  a mandatory hook lab with ten candidates across six causal lenses, three
  finalists, a source-title contest, a child-simple winner, and an executable
  first-three-second packet.
- Why: A latest-news reel produced an accurate but abstract opening whose
  financial language had to be decoded before the viewer could feel curiosity.
- Tradeoff accepted: Applicable Storyboard plans are longer because they expose
  the candidate and comparison work instead of silently choosing one line.

## First-Principles Reasoning

- Objective: Make the opening understandable, interesting, visual, and
  evidence-safe before the rest of the script is allowed to lock.
- Placement logic: Hook selection is narrative and scene design, so Storyboard
  owns the first-load route, QA gate, conditional rubric, and regression eval.
- Expected behavior delta: One abstract opening becomes a compared set whose
  winner uses a recognizable actor, concrete action, familiar consequence,
  short display language, and an uncertainty-safe first frame.
- Proof needed: The same realistic latest-news case must move from failure to
  TAS-A without leaking the desired winning line into the eval prompt.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` owns the trigger, hard gates, compact rubric, template, and reference load condition. |
| `reference_load_precision` | pass | `plain-language-hook-lab.md` loads only for short-form, latest-news, title-led, or retention-sensitive work. |
| `missing_context_rate` | pass | Candidate count, lens diversity, blocked language, title comparison, and first-three-second fields remain visible in first load. |
| `noisy_context_rate` | pass | Longer translation examples and the full comparison method live in one conditional reference. |
| `duplicated_instruction_count` | pass | `SKILL.md` selects and gates; the reference expands the method; QA verifies evidence. |
| `prompt_size_tokens` | unknown | Token count was not measured separately. |
| `task_success_rate` | pass | Exact held-out mower-policy eval moved from C/0% against the pre-change skill to A/100% against the candidate. The original Nvidia case also moved C -> A. |
| `review_tas_rate` | pass | Initial TAS-B findings were repaired; independent rerun returned TAS-A with no blockers. |
| `maintenance_locality` | pass | All behavior, proof, QA, reference, and audit changes remain under `skills/storyboard/`. |
| `composition_clarity` | pass | `hook_lab(...)` exposes inputs, candidate/finalist outputs, winner, rejection reasons, and first-three-second proof. |

## Proof Artifacts

- Skill-local eval: `storyboard_latest_news_plain_language_hook_01`.
- Original correction case: Nvidia C -> A, with winner
  `Nvidia may help OpenAI buy Nvidia chips`.
- Held-out domain baseline: California mower-policy case scored C against the
  pre-change Storyboard skill: one long hook, no candidate lab, no title
  contest, and no exact first-three-second packet.
- Held-out domain candidate: the identical prompt and assertions scored A
  against the changed skill, with winner
  `California May Restrict New Gas Mowers`.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passes Storyboard's registry, todo, template, and five-item surface checks.
  The repo-wide command still reports unrelated pre-existing
  `content-impl-plan` QA/eval surface-budget warnings.
- Eval query smoke check:
  `python3 skills/eval/scripts/check_eval_queries.py --root .`.
- Reviewer receipt: initial TAS-B identified close-domain proof and blocked
  jargon in raw candidates. The canonical eval now uses an unrelated
  mower-policy domain, displayed candidates are post-jargon-cleanup, weak
  candidates require visible rejection reasons, and an exact pre-change
  baseline/candidate pair exists. Independent rerun verdict: TAS-A, pass, no
  hard-gate failures, no further rerun required.

## Before Behavior

```text
Hook:
  "Nvidia may not just sell the chips behind AI..."
result:
  accurate but abstract
  no alternatives
  no title contest
  no plain-language gate
```

## After Behavior

```text
hook_lab(latest_news, proof, general_viewer, source_title)
  -> 10 cross-lens candidates
   -> 3 compared finalists
   -> "California May Restrict New Gas Mowers"
   -> exact on-screen copy + VO + visual action + evidence qualifier
```

## Followups

- Re-run the focused eval when Storyboard's narrative or short-form contracts
  change.
- Treat future operator corrections as new cases only when they expose a
  distinct failure mode rather than another wording preference.
