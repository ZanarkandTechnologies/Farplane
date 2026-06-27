---
title: "Decision: Project Harness Overlay"
status: implemented
owner: codex
created_at: 2026-06-24T00:00:00+0800
updated_at: 2026-06-24T00:00:00+0800
tags:
  - farplane
  - deliberative-advice
  - harness
  - rollout
refs:
  - context.md
  - ../../../docs/farplane-framework/graph-contract.md
  - ../../../skills/skill-maintenance/graph/README.md
  - ../../../tickets/TASK-0216/ticket.md
  - ../../../bin/core/farplane_adoption.py
---

# Decision: Project Harness Overlay

## Decision

Build a small **Project Harness Overlay** feature, but start as a falsifiable
manifest-and-metrics pilot rather than a broad platform or Office-heavy UI
feature.

The implemented v1 is the narrower **Farplane Adoption Tracker CLI** in
`bin/core/farplane_adoption.py` and `farplane adoption scan`.

## Scope Revision

After follow-up discussion, narrow v1 to a **Farplane Adoption Tracker**:

```text
farplane_adoption_tracker(
  global_farplane_manifest,
  project_manifest_pins[],
  feature_registry,
  template_registry,
  optional_project_skill_dirs
) -> adoption_graph + rollout_status + drift_report
```

There is one global Farplane standard. Forward-facing company projects can
adopt that standard first, then other projects declare adoption through
manifest pins. In this repo, the `farplane/` directory is treated as the
forward-facing company harness.

Local project skills are simple:

- if a project has `skills/`, include local skills in that project's skill
  graph;
- otherwise use global skills;
- global skill standards are frontiered by the main forward-facing company
  harness before broader rollout.

## Stakes

Farplane needs a way to let local and team skills mature inside real projects
without copying global harness machinery into every repo. The feature should
support local experimentation, cross-project rollout, promotion to global
skills, and harness performance tracking while keeping small projects light.

## Grounding

- `docs/farplane-framework/graph-contract.md` defines generated graph surfaces
  as projections over GraphIR.
- `skills/skill-maintenance/graph/README.md` documents shared GraphIR and
  named projection profiles.
- `tickets/TASK-0216/ticket.md` records the decision that lifecycle, harness,
  and skill graphs are sibling projections, not parent/child graphs.

## Perspectives

- `Operator value:` favors a Project Harness Overlay rendered in Office as
  Global / Team / Project panels, with local-to-team-to-global skill promotion.
- `Engineering risk:` favors the same direction, but only with a boring v1:
  small manifest, explicit precedence, separate harness and skill versioning,
  fixtures before UI.
- `Evidence skeptic:` dissents against a broad feature now; first prove the
  pain across 2-3 real projects with metrics.
- `Systems fit:` says the declarative source of truth should be
  `farplane/manifest.json`; GraphIR is derived, `skill-maintenance` generates,
  `deep-init` scaffolds, Office consumes, validators check.

## Options

1. `Global-only manifest and graph`
   Keep one Farplane standard and render all projects through global defaults.
   This is simple but does not solve local skill experimentation or rollout.

2. `Per-project copied harness`
   Let each project vendor skill-maintenance and standards. This maximizes
   portability but creates drift and maintenance overhead.

3. `Standard manifest plus project/team overlays`
   Keep Farplane core global, then let projects and teams declare local skill
   sources, version pins, overlays, metrics refs, and promotion refs.

## Recommendation

Choose option 3, but scope v1 as a **Farplane Adoption Tracker** rather than a
general overlay platform:

```text
track_farplane_adoption(
  projects[],
  global_manifest,
  feature_registry,
  template_registry
) -> project_pin_matrix + feature_adoption_graph + rollout_lag_report
```

Do not copy `skill-maintenance` into each project. Keep it as the shared
generator owner that can read project/team/global sources.

## Manifest V1 Shape

```json
{
  "schema_version": "0.1.0",
  "project_id": "example",
  "harness_standard_version": "0.2.0",
  "template_uses": {
    "farplane-framework": "1.3.0"
  },
  "feature_pins": {
    "FEAT-0060": "adopted"
  },
  "skill_policy": {
    "local_skills": "use-if-present",
    "fallback": "global"
  }
}
```

## Dissent

The strongest dissent is timing: GraphIR proves we can map project harnesses,
but it does not yet prove repeated cross-project rollout pain. A broad Office
feature before project evidence could create ceremony and a second config plane
before the need is real.

## Tradeoff Accepted

Accept one small declarative config surface now to make local/team/global
precedence visible. Reject a daemon, copied skill-maintenance bundle, database,
or Office-first implementation until pilot evidence exists.

## Confidence

Medium-high on the direction. Medium on timing. The right first move is a
prototype with falsifiable project evidence.

## Next Owner

Create an implementation ticket for a Farplane Adoption Tracker.

Owner surfaces:

- `docs/features/`: adoption tracker and manifest pin contract.
- `farplane/manifest.json`: global/forward-facing manifest source.
- `docs/features/registry.jsonl`: feature adoption dimension.
- `docs/templates/registry.jsonl`: template version adoption dimension.
- project `farplane/manifest.json`: per-project pins.
- `skills/skill-maintenance/`: load project/team/global skill sources and emit
  adoption-aware projections.
- validators: check manifest pins, stale versions, unknown feature refs, and
  local skill source existence.
- Office UI: consumer of the adoption graph.

## Proof / Evidence Gap

Pilot across 2-3 projects before expanding:

- measure time-to-init,
- copied-file count,
- local skill count,
- skill promotion attempts,
- skill version conflicts,
- feature adoption lag,
- template version drift,
- QA/review pass rate,
- operator interruptions caused by harness ambiguity.

If those projects run cleanly with current `deep-init-project`, existing docs,
tickets, and manual promotion notes, stop and defer the feature.
