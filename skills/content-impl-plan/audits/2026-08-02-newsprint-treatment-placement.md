---
title: Newsprint-treatment placement and source boundary
status: accepted
owner: content-impl-plan
kind: skill-audit
created_at: 2026-08-02
source_refs:
  - .farplane/learn-from-video/DZdCD2YNk4d/evidence/source-02s.jpg
  - .farplane/learn-from-video/DZdCD2YNk4d/evidence/contact-sheet.jpg
changed_files:
  - skills/content-impl-plan/SKILL.md
  - skills/content-impl-plan/qa_checklist.md
  - skills/content-impl-plan/evals/evals.json
  - skills/content-impl-plan/references/scene-asset-bundles.md
  - skills/content-impl-plan/references/newsprint-treatment.md
  - skills/content-impl-plan/scripts/verify_scene_direction.py
  - skills/content-impl-plan/scripts/test_verify_scene_direction.py
---

# Newsprint-treatment placement

## Grounding note

```text
claim:
  The supplied tutorial does not demonstrate a separate Vox grain-filter recipe.
source_class:
  operator-provided selected frames + local reconstruction evidence + live Brand Kit inventory
evidence:
  The finished frame contains texture already present in a scanned New York
  Times page and photograph. Visible After Effects controls demonstrate Trim
  Paths, Roughen Edges, Turbulent Displace, time-varying Random Seed, and a
  duplicated displacement layer for annotations—not page grain. The live Brand
  Kit query for “vox” returned no records.
confidence:
  high for what the retained frames demonstrate; unknown for Vox's undocumented
  internal finishing stack
local_impact:
  Preserve the source uncertainty, use a clean-room raster newsprint method,
  and do not create a third-party-named Brand Kit from one reference.
```

## Placement decision

| Option | Fit | Decision |
| --- | --- | --- |
| Vox Brand Kit | Strong only for an operator-approved recurring identity with a stable example and recipe | Reject now: no such live kit exists, and one third-party reference is not approved local identity |
| `content-impl-plan` reference | Strong for reusable source classification, asset ownership, production handoff, and proof | Primary owner |
| Root/global prompt or new skill | High context/duplication cost; existing content owner already gates newsprint | Reject |

Secondary owners remain `asset-advisor` for raster discovery, the selected image
owner for subject print preparation, and Remotion for deterministic compositing.

> **Before:** “Add grain” could collapse baked scan texture, paper surface,
> subject halftone, and global noise into one vague filter.
> **After:** Evidence is classified first; paper and subject treatment receive
> separate owners and final-resolution proof.
> **Example:** A rights-cleared raster paper plate moves with the page beneath
> type, while the photograph receives its own grayscale/halftone treatment.

## Proof plan

- Extend the existing clean-newsprint eval without weakening its frozen intent.
- Require classification, raster asset, page/object registration, and
  full-frame/close proof refs, inspectable final-resolution halftone scale, and
  independent style-review receipt in the mechanical scene-direction verifier.
- Validate links, JSON, registry generation, and query-spoiler checks.
- Independent reviewer applies both skill QA checklists and the placement claim.

Focused behavior evidence progressed from the under-specified round-two B to a
final TAS-A without weakening the assertions:
`.farplane/evals/runs/20260801-181837-20260802-scope-newsprint-round6/summary.json`.
The accepted response now distinguishes all three evidence classes; records
rights, page registration, final-size subject/background proofs, halftone
scale, Remotion compositing, and independent review; and keeps unresolved
packets blocked.

The package-wide surface-budget validator currently reports a pre-existing
19-item QA/eval surface against its configured limit of 5. This change neither
adds a QA item nor a content-impl-plan task; focused JSON, query, link, verifier,
and reviewer evidence own acceptance here. Surface compaction remains separate
maintenance work because deleting unrelated coverage would broaden this repair.

Independent reviewer verdict: TAS-A, no hard gates or blocking findings. The
reviewer accepted the pre-existing surface-budget warning as separate
maintenance debt for this scoped repair.
