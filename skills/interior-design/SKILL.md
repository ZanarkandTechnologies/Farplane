---
name: interior-design
version: 0.1.0
description: "Turn an existing room, office, or navigable interior plus activities and taste into an evidence-backed composition brief, blockout, and operator review gate."
tier: 3
group: frontend
source: local
template_uses:
  skill-template: "0.3.8"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Grep, Glob
---

# Interior Design

## Context

Use this skill for the spatial design of virtual or conceptual interiors:
offices, rooms, studios, shops, control rooms, isometric environments, and
other navigable indoor scenes. It owns the interior program, adjacency,
circulation, furniture and landmark scale, occupied mass, negative space,
material and furniture grammar, lighting composition, and review blockout.

`visual-design` owns interface typography, UI hierarchy, component styling,
and screen-level color systems. `functional-ui` owns interaction workflow.
Implementation remains with the owning frontend or scene module after the
interior direction is accepted.

If the request concerns only a screen, dashboard, page, chart, component, or
interface and has no navigable room or interior, route immediately to
`visual-design` and stop. Do not produce an interior program, circulation plan,
furniture grammar, or blockout for screen-level work.

For that boundary case, the response must begin with the explicit handoff:
`This is interface visual design, so route it to visual-design.` It may then
briefly name relevant UI concerns, but it must not continue the interior-design
workflow.

This skill may shape a conceptual physical room, but it does not certify
architecture, structure, fire safety, accessibility, egress, or building-code
compliance. Route real construction decisions to qualified local professionals.
For any compliance or construction-approval request, the response must begin:
`This skill provides conceptual or virtual interior direction, not licensed
professional approval.` Preserve that wording even under schedule pressure,
then name the qualified local reviewers and authorities required.

## Skill Signature

```text
interior_design(existing_scene, activities, operator_taste, constraints, reference?)
  -> evidence_inventory
   + interior_program
   + composition_options
   + blockout_hypotheses
   + review_artifact
   + accepted_direction
state: reads(scene screenshots/files, room shell, current assets/themes, activity needs, prior feedback); writes(design brief or ticket-local interior section when authorized)
gates: observed_vs_unknown_separated; circulation_preserved; review_artifact_exists; operator_accepts_before_broad_implementation
routes: visual-design | frontend-craft | review | qualified-building-professional
fails: local prop tuning before whole-room diagnosis; invented scene audit; palette-only reference matching; engineering metrics used as aesthetic proof
```

```text
InteriorDesignBudget = {
  grounding?: "scene-only" | "reference-led" | "precedent-led",
  fidelity?: "diagram" | "greybox" | "annotated-render",
  finish_gate?: "self-check" | "review" | "human-feedback"
}
```

Resolve missing inputs from current files, screenshots, tickets, and theme or
layout state. When the scene or reference needed for judgment is unavailable,
state verbatim that the unavailable image cannot be honestly audited from the
prompt alone, require the actual image before locking direction, and keep all
directions provisional; do not invent an audit. For reference-led work, always
complete a comparison matrix covering `composition`, `silhouette`, `value`,
`material family`, `lighting`, `density`, and `repetition`, marking every
dimension observed, user-stated, or unknown before mapping traits to `adopt`,
`adapt`, `preserve`, or `reject`. The transfer must use each of those four
decisions explicitly at least once, or state that no honest decision is yet
possible for a category.

## Phase Contract

```text
interior_design_phase(task, bound_inputs, state)
  -> evidence_status
   + interior_program
   + current_scene_audit
   + composition_decision
   + reviewable_blockout
   + guard_metrics
   + operator_verdict
   + implementation_handoff
```

## Phase Boundary

Follow Tier 0 phases inline. Use `review` for independent judgment of a
material brief or proof bundle. Use `visual-design` only after the spatial
composition is accepted and UI or presentation styling remains. Do not call a
phase-like skill recursively at the same scope.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the interior-design inputs and read `qa_checklist.md` as
  preflight guardrails.
  - [ ] If no navigable interior exists, route to `visual-design` and stop the
    interior workflow. Begin the response with the required explicit handoff:
    `This is interface visual design, so route it to visual-design.`
  - [ ] If a real physical project requests compliance or construction
    approval, begin the response with `This skill provides conceptual or
    virtual interior direction, not licensed professional approval.` Then route
    code, fire, accessibility, egress, and structural verification to qualified
    local professionals and authorities.
  - [ ] Before proposing a final direction, produce an evidence-status matrix
    that marks each item observed or missing: default-camera screenshot/current
    view, shell, camera/crop, furniture/scale, circulation, materials, and
    lighting.
- [ ] 2. Establish the interior program.
  - [ ] Name occupants or agents, activities, zones, adjacencies, focal anchors,
    storage or equipment needs, arrival points, circulation, camera/read
    conditions, and hard functional constraints.
- [ ] 3. Audit the complete current interior before local polish.
  - [ ] Inspect shell and boundaries, camera and crop, occupied visual mass,
    purposeful circulation versus accidental dead space versus decorative
    clutter, circulation and occlusion, furniture scale and silhouette,
    material/value/color family, lighting and shadows, repeated forms, and what
    reads as one world versus pasted-on scenery.
- [ ] 4. Choose the interior branch.
  - [ ] 1. For a new interior, define two or three whole-room composition
    models before selecting furniture details.
  - [ ] 2. After strong negative feedback or repeated local fixes, reset the
    composition model rather than tuning room size, prop scale, or palette.
  - [ ] 3. For reference-led work, compare composition, silhouette, value,
    material family, lighting, density, and repetition in an explicit matrix,
    mark each dimension observed, user-stated, or unknown, then map traits to
    `adopt`, `adapt`, `preserve`, or `reject`, using all four decisions
    explicitly at least once or stating why a decision is not yet honest. If
    either image is unavailable,
    state that it cannot be honestly audited from the prompt alone and require
    the actual image before locking direction.
- [ ] 5. Shape and recommend the composition.
  - [ ] Present two or three materially different spatial options, recommend
    one, name the accepted tradeoff, and define at least three measurable but
    provisional scene-relative targets. Include occupied mass or viewport
    fill, maximum dead patch relative to a workstation or zone, primary and
    secondary path widths in occupant units, object-to-occupant scale,
    adjacency distance, or default-camera framing. These are blockout tests,
    not universal standards.
- [ ] 6. Produce a reviewable interior artifact before broad implementation.
  - [ ] Use an annotated screenshot, top-down or ASCII plan, greybox, isometric
    overlay, or side-by-side study that shows shell, zones, primary masses,
    circulation, dead space, camera crop, and material/furniture grammar.
  - [ ] Require the operator to accept or reject this artifact; walkability,
    collision, compile, console, and occupancy checks remain guard metrics.
- [ ] 7. Write the interior brief and complete the finish gate.
  - [ ] Apply `qa_checklist.md` again, keep the direction reproducible from
    files, use independent review for material changes, then hand accepted
    spatial constraints to the scene implementer and remaining UI styling to
    [visual-design](../visual-design/SKILL.md).
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- Use [interior design brief](templates/interior-design-brief.md) for durable
  ticket/spec handoff.
- Use [isometric office reset](examples/isometric-office-reset/example.md) as
  the positive example for repeated local-fix failures.
- Skill behavior is covered by `evals/evals.json`.

## Gotchas

- Do not equate empty floor with elegance or fully walkable floor with good
  composition; distinguish intentional circulation from accidental voids.
- Do not enlarge furniture to make an oversized shell feel occupied. Fix the
  shell, camera, zoning, adjacency, or massing model first.
- Do not give every room or activity station a separate visual universe. Use a
  shared architectural, furniture, material, scale, and lighting grammar.
- Do not lock dimensions from generic ratios. Treat numbers as hypotheses to
  test in the actual blockout and default camera.

## Reference Map

- [interior composition](references/interior-composition.md) - read when
  auditing, repairing, or comparing a navigable interior.
- [interior design brief](templates/interior-design-brief.md) - use when the
  direction must survive into a ticket, delegation, or implementation pass.
- [isometric office reset](examples/isometric-office-reset/example.md) - read
  when repeated size, scale, palette, or room-placement changes failed.
- [runtime QA checklist](qa_checklist.md) - read at invocation and apply again
  before accepting the interior direction.

## Output

- `Evidence status matrix`: current view, shell, camera/crop, furniture/scale,
  circulation, materials, and lighting marked observed or missing
- `Interior program`: never omit occupants, activities, zones, anchors,
  adjacency, circulation, massing, object-to-occupant scale, and shared grammar
- `Current-scene audit`
- `Space classification`: explicitly distinguish purposeful circulation,
  accidental dead floor, and decorative clutter
- `Composition options`
- `Recommended direction and tradeoff`
- `Blockout hypotheses`
- `Reference transfer` when applicable
- `Review artifact`
- `Operator acceptance gate`
- `Engineering guard metrics`
- `Implementation handoff`
