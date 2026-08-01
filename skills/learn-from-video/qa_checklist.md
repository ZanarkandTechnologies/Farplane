---
title: Learn From Video QA Checklist
owner: learn-from-video
status: active
kind: qa-checklist
created_at: 2026-07-28
updated_at: 2026-08-02
---

# Learn From Video QA Checklist

Apply before reconstruction and again before completion.

## Scope

- [ ] A concrete operator learning goal is recorded before the eval is frozen.
- [ ] When the initial request is broad and the source supports multiple
  plausible targets, the operator was shown two to four total source-grounded
  choices, with `full_system` occupying one choice when appropriate, and could
  select multiple targets.
- [ ] A follow-up was skipped only because the operator's prompt already named
  concrete elements precise enough to determine `must_match`.
- [ ] No candidate generation began while scope status was
  `clarification_required`.

## Evidence

- [ ] Canonical source and prior ingest/run artifacts were deduped.
- [ ] Transcript-backed facts, frame-backed evidence, creator claims,
  inference, candidate observations, and confidence limits are separate.
- [ ] Evidence classes use distinct ledger sections; shared timestamps do not
  collapse transcript facts and frame observations into one mixed row.
- [ ] The demonstrated final output or intermediate state is visible enough to
  judge; otherwise the result is blocked.
- [ ] Source anchors include timestamps/frame refs for every must-match check.

## Eval

- [ ] The source-output eval was frozen before candidate generation.
- [ ] Checks grade a produced artifact or observable state, not tutorial recall
  or summary wording.
- [ ] The user-facing eval prompt does not name the target skill, checklist,
  expected owner, or exact answer.
- [ ] Must-match, may-vary, and reject criteria are distinct.
- [ ] Failed checks remain failed; the rubric was not weakened after output.

## Candidate

- [ ] Any prior generic/failed candidate and its proof refs remain retained as
  the replayable regression baseline.
- [ ] Candidate uses real files/parameters/timing and the narrowest faithful
  production route.
- [ ] Rights-safe substitutions name protected source expression, replacement,
  and provenance while preserving the taught mechanism rather than reducing it
  to generic style.
- [ ] Technical render integrity is reported separately from source-match
  quality.
- [ ] Representative frames, probes, manifests, and comparison artifacts exist.
- [ ] Reconstruction rounds stay within budget.

## Handoff

- [ ] Existing owner versus new skill placement is explicit and registry-backed.
- [ ] `learn-from-video` did not mutate the target skill.
- [ ] Handoff includes frozen eval, failed observations, evidence anchors,
  smallest repair, and rerun rule.
- [ ] Each failure row contains check id, source anchor, expected observation,
  candidate observation, evidence ref, owner, smallest repair, and rerun rule.
- [ ] Missing candidate/evidence gates also have failure rows, using explicit
  observations such as `not generated` instead of omitting the schema.
- [ ] Both placement branches are explicit: existing owner routes to
  maintenance/self-improve; no stable owner routes to skill-creator.
- [ ] Returned skill candidates are judged by rerunning the same frozen eval.
- [ ] Final verdict is `pass` or an evidence-backed `blocked`, never “learned”
  from analysis/storage alone.

## Rights

- [ ] No source logos, scripts, prompts, frames, music, voices, likenesses,
  proprietary assets, or affiliation claims enter the candidate.
- [ ] Stored evidence is minimal, attributed, rights-limited, and excludes raw
  media unless explicitly authorized.
- [ ] A private-source blocker offers redacted excerpts, local paths, or
  timestamped operator descriptions as privacy-preserving resume options.
- [ ] The private-source minimum bundle jointly connects at least one
  instruction/operation sequence to a judgeable output state; it does not claim
  that any isolated partial item is sufficient.
