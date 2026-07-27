---
artifact_type: skill-maintenance-audit
date: 2026-07-27
mode: harden_skill
owner_skill: content-impl-plan
affected_skills:
  - content-impl-plan
  - asset-advisor
  - storyboard
  - remotion
status: accepted
---

# Asset discovery and custom SVG hardening

## Behavior delta

```text
expected_behavior:
  missing visual -> Asset Advisor candidate discovery
  discovery -> links/IDs + rights/fit decisions + accepted file | searched_no_fit
  searched_no_fit -> raster/video generation owner when needed
  accepted media -> Remotion animation/compositing

current_behavior_observed:
  rights-safe originality was treated as permission to skip discovery
  missing scene visuals were drawn as custom SVG assets
  Remotion received locally authored asset substitutes instead of sourced media

forbidden:
  custom-created SVG animation assets
  SVG/JSX/programmatic vector scene substitutes
  generation or Remotion before a discovery receipt

allowed:
  user-supplied, brand-owned, licensed, or discovered SVG as static source media
  deterministic Remotion transforms, masks, crops, treatment, and sequencing
  raster/video generation after evidenced searched_no_fit or explicit generation need
```

## Evidence

The TASK-0073 documentary-reel proof used nine locally authored SVG scene
assets without an Asset Advisor candidate-search receipt. The user explicitly
rejected that production shortcut and requested a ban across content
implementation planning.

## Owner-local changes

- `content-impl-plan`: makes discovery receipts and the no-custom-SVG rule
  creative-lock gates.
- `asset-advisor`: owns candidate searching, rights/fit decisions, selected
  files, and evidenced `searched_no_fit`.
- `storyboard`: emits searchable asset briefs and cannot prescribe SVG/JSX
  substitutes.
- `remotion`: animates accepted media and returns missing visuals to Asset
  Advisor instead of drawing them.
- `documentary-reel.md`: applies the same boundary to backgrounds, subjects,
  foregrounds, and overlay media.

## Inspectable delta

> **Before:** Missing visual → draw a rights-safe local SVG → animate it.
>
> **After:** Missing visual → search and compare candidates → accept a sourced
> file or record `searched_no_fit` → route raster/video generation if needed →
> animate accepted media.
>
> **Example:** A documentary reel needs a microphone. Asset Advisor searches
> supplied/Resource Bank assets and suitable licensed photo, cutout, archive,
> and illustration sources; it records candidates and rights. Remotion receives
> the selected file. It does not draw a microphone SVG.

## Proof plan

- JSON parse for all changed eval suites.
- Eval query spoiler check.
- Scoped documentation-reference validation.
- Skill validator with inherited unrelated blockers named separately.
- Four candidate behavior cases:
  - content plan refuses an SVG-built three-layer bundle;
  - Asset Advisor searches before generation;
  - Storyboard routes missing visuals through discovery;
  - Remotion refuses SVG/JSX asset substitutes.
- Independent review of first-load sufficiency, ownership, and loopholes.

## Baseline and candidate

```text
baseline_artifact:
  TASK-0073 documentary-reel render and asset directory
baseline_result:
  failed user expectation; no Asset Advisor discovery receipt; custom SVG scene assets
candidate_artifact:
  changed skills and regression rows listed above
comparison:
  candidate run 3 judges confirmed all four core guardrails:
    - custom SVG/JSX scene substitutes rejected
    - Asset Advisor discovery precedes generation and Remotion
    - searched_no_fit requires evidence
    - Remotion remains blocked until accepted files
  overall task grades remained B/C because of unrelated audio completeness,
  scene-row completeness, readiness wording, and recital-only SVG-exception
  assertions; the focused eval rows were corrected after inspection
promotion_decision:
  accepted after independent TAS-A contract review
```

## Validation receipt

- `jq empty` on all four changed eval suites: passed.
- `skills/eval/scripts/check_eval_queries.py --root .`: passed.
- `bin/validators/check_doc_refs.py`: passed, 1,957 references checked.
- Scoped `git diff --check`: passed.
- Registry, template, todo, and Tier 0 checks: passed.
- Full skill checker remains non-zero only for inherited
  `content-impl-plan` surface-budget debt: 14 QA items and 19 eval tasks
  against the five-item limit.
- Candidate behavior evidence:
  `.farplane/evals/runs/20260727-133620-asset-discovery-svg-ban-candidate-3/summary.json`.
  Overall task pass rate was 0 because the judges applied additional
  completeness/recital assertions, but their per-reference receipts mark the
  core correction behaviors met in all four lanes. No pass-rate improvement is
  claimed.
- Independent final review: TAS-A, no blocking findings, no rerun required.
