---
title: Character fallback approval hardening review
owner: reviewer
status: passed
kind: skill-review
created_at: 2026-07-17
context_ref: skills/video-production/audits/2026-07-17-character-fallback-approval.md
overall_tas: TAS-A
verdict: pass
rerun_required: false
---

# Character Fallback Approval Hardening Review

## Review Contract

- `work_type`: material skill, prompt, eval, and integration review
- `search_scope`: the caller-listed `video-production` and `storyboard` skill
  files; the character manifest and identity sheet; the TASK-0378 identity
  correction and actual generation inputs; the two cited eval run artifacts;
  skill-system validators; neighboring packet terminology in
  `ai-video-advisor`
- `rubrics_used`: `skill-contract`, `prompt-quality`, `eval-quality`,
  `integration-readiness`, and `evidence-quality`
- `required_tas`: `TAS-A` for every selected family
- `overall_tas`: `TAS-A`
- `verdict`: `pass`
- `rerun_required`: `false`

These families were selected from the actual changed surfaces because the
caller did not supply named rubric families. `integration-readiness` and
`evidence-quality` are hard gates for the cross-skill behavioral claim.

## Adversarial Rejection Attempts

1. Searched for a path where a provider-safe fallback could inherit approval.
   The first-load gates now reject that path and explicitly return affected
   assets to human review.
2. Traced the canonical character from manifest to storyboard packet to the
   live Seedance JSON. The repaired approval and generation envelope now joins
   the exact path/hash evidence to the reduced provider API input.
3. Inspected both the initial and replacement targeted eval runs instead of
   trusting the audit summary. The initial semantic judges rejected the
   answers with verdict `C`; both replacement semantic judges return `A`.
4. Checked JSON parsing, local links, character hash integrity, and the full
   skill-system validator. Those mechanical checks pass.
5. Looked for harmful first-load duplication. The short gates in the two
   skills and their QA checklists are justified; detailed procedure remains in
   `scene-grid-production.md` and the style references.

## Rereview Result

The two original hard-gate failures are resolved:

- The audit now reports the initial semantic failures and the replacement
  semantic runs separately. Both replacement runs return verdict `A`, pass rate
  `1.0`, and behavior-trace pass.
- Scene packets, `approved.json`, shot-planner output, and the local generation
  envelope now use `canonical_character_path` and
  `canonical_character_sha256`. Versioned approved variants have explicit
  path/hash fields. The preflight receipt checks approval state, canonical and
  effective hashes, grid hashes, and the effective character's presence in the
  exact provider `reference_images` before reducing the envelope to the
  Seedance API schema.

## Hard-Gate Failures

None.

## Failed Checks

None.

## Finding Log

### F1 — Initial cited evals rejected the claimed behavior

- `status`: resolved
- `severity`: none
- `confidence`: high
- `rubric`: `evidence-quality`, `eval-quality`, `skill-contract`
- `file_refs`:
  - `skills/video-production/audits/2026-07-17-character-fallback-approval.md:49`
  - `.farplane/evals/runs/20260716-173338-character-fallback-reapproval-20260717/summary.json`
  - `.farplane/evals/runs/20260716-173516-character-fallback-reapproval-video-20260717/summary.json`
- `evidence`: both summaries report `pass_rate: 0.0` and semantic verdict `C`.
  The storyboard answer changes the canonical path/hash instead of preserving
  the original, does not require a versioned provider-safe sibling, and does
  not lock unaffected scenes. The video-production answers omit some or all of
  proof-only status, exact clean/annotated grid review, and canonical path/hash
  binding. `behavior_verdict: pass` means the Codex run completed; it is not a
  semantic task pass.
- `resolution`: first-load contracts now require canonical preservation,
  versioned siblings, affected clean/annotated-grid review, and unaffected
  scene locking. Replacement semantic runs pass:
  - `.farplane/evals/runs/20260716-175348-character-fallback-storyboard-rerun-20260717/`
  - `.farplane/evals/runs/20260716-175516-character-fallback-video-rerun-20260717/`

### F2 — Character identity lacked one checkable provider-call contract

- `status`: resolved
- `severity`: none
- `confidence`: high
- `rubric`: `integration-readiness`, `prompt-quality`, `skill-contract`
- `file_refs`:
  - `skills/video-production/references/scene-grid-production.md:59`
  - `skills/video-production/references/scene-grid-production.md:128`
  - `skills/video-production/references/explainer-styles/retro-low-poly-consequence/prompts.md:8`
  - `skills/video-production/references/explainer-styles/retro-low-poly-consequence/prompts.md:111`
  - `skills/video-production/references/explainer-styles/retro-low-poly-consequence/prompts.md:204`
- `initial_evidence`: the scene schema used `character_profile_ref` and
  `character_reference_sha256`; the style packet uses `character_bible_path`
  and `character_bible_sha256`; the shot-planner output carries the path but
  omits the hash; and the live provider JSON contains only reference paths.
  The prose says to compare hashes, but does not define the local generation
  envelope/preflight receipt that performs the comparison before producing the
  provider API JSON. The sample folder names `approved.json`, while the schema
  does not define its required identity and approval fields.
- `resolution`: `scene-grid-production.md` now defines the stable canonical and
  approved-variant field pairs, structured approval record, local generation
  envelope, exact nested provider input, and all-pass preflight receipt. The
  provider receives only its supported API object while the local envelope
  retains approval and digest evidence.

### F3 — The canonical card is identity-correct but visually cleaner than the profile lock

- `severity`: low
- `confidence`: high
- `rubric`: `prompt-quality`
- `file_refs`:
  - `skills/video-production/references/explainer-styles/retro-low-poly-consequence/characters/late-90s-everyperson/identity-sheet.png`
  - `skills/video-production/references/explainer-styles/retro-low-poly-consequence/profile.md:111`
- `evidence`: the card matches the original hair, face, teal shirt, ochre
  trousers, and silhouette, but its clean light background and smooth,
  contemporary low-poly presentation do not themselves demonstrate the dirty
  PS1 surface lock. The profile correctly makes the overview/grid the rendering
  authority, so this is not a blocker.
- `next_action`: label the card explicitly as identity/wardrobe authority only,
  with scene grids/profile as render-surface authority, so a provider is less
  likely to modernize the accepted look.

## Rubric Sections

### Skill Contract — TAS-A

The owning surfaces and human-review gate are correctly placed, the first-load
rules are compact, and detailed procedure is progressively disclosed. Both
targeted semantic reruns now preserve the canonical asset, version the
fallback, invalidate only affected approvals, return the correct visual packet,
and keep unaffected scenes locked.

### Prompt Quality — TAS-A

The generation prompts clearly forbid fallback promotion and describe the
visual review gate. Cross-stage inputs, shot-planner output, approval records,
and the generation envelope now preserve one stable canonical identity/hash
vocabulary through the handoff.

### Eval Quality — TAS-A

The new fixtures are realistic, use observable reference points, run the real
Codex harness, and correctly exposed the original missing behavior. They are
good regression tests. The repaired contracts now pass both semantic reruns.

### Integration Readiness — TAS-A

All references resolve, JSON parses, the manifest hash matches the actual
identity sheet, and `check_skills.py` passes. The explicit approval record,
generation envelope, and preflight receipt make the provider-call boundary
auditable without adding unsupported fields to the provider API object.

### Evidence Quality — TAS-A

Mechanical evidence is strong and auditable. The audit accurately distinguishes
the initial failures from the replacement semantic passes, and both rerun
summaries map the complete behavior claim to verdict `A` evidence.

## Would This Have Prevented TASK-0378?

Yes. The new first-load rule stops the exact SC01 promotion: the mannequin is
proof-only, visible identity change invalidates affected approval, the
canonical asset stays unchanged, the fallback becomes a versioned sibling, the
affected character card and clean/annotated grids return to the operator, and
unaffected scenes remain locked. The generation envelope then blocks spend
unless approved path/hash evidence matches the exact provider inputs. Both
targeted semantic reruns demonstrate this behavior.

## Blocking Findings

None.

## Next Action

Advance the scoped skill changes to modular commit. The low-severity F3 note may
be handled later by labeling the character card as identity/wardrobe authority
only; it does not weaken the current approval-invalidation contract.

## Verification Performed

```text
jq empty skills/video-production/evals/evals.json skills/storyboard/evals/evals.json
shasum -a 256 .../characters/late-90s-everyperson/identity-sheet.png
python3 skills/skill-maintenance/scripts/check_skills.py
```

- Both eval JSON files parse.
- Identity sheet digest matches the manifest:
  `8ce13c3aff557aac962cfca88bf1b85a58ec80821731c5f580771469e1b94d8a`.
- Skill-system validator passes, including registry, config, eval-query, link,
  capability, and surface-budget checks.
- Storyboard semantic rerun: verdict `A`, pass rate `1.0`.
- Video-production semantic rerun: verdict `A`, pass rate `1.0`.
