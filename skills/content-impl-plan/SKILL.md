---
name: content-impl-plan
description: "Compile content intent into a canonical ticket's action graph, dependencies, gates, and proof for a real deliverable."
tier: 3
group: content-production
source: local
template_uses:
  skill-template: "0.4.0"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["storyboard", "asset-advisor", "editing-advisor", "remotion", "review"]
allowed-tools: Read, Grep, Glob, Bash
---

# Content Impl Plan

## Context

Use this skill when an idea, proof point, offer, or Tasty Pack/reference needs
an executable content-production ticket. It is the content analogue to
`impl-plan`: it resolves creative intent into the canonical
`tickets/TASK-XXXX/ticket.md`, with a complete production action graph in its
`Change Plan`, concrete proof in `Done` and `QA Strategy`, and child artifacts
linked rather than copied.

This skill owns the ticket's parent direction and action graph, not a separate
plan file or schema. It does not author a storyboard, asset manifest, provider
prompt, edit recipe, rendered file, or readiness verdict.
Storyboard owns narrative/scene design, Asset Advisor owns asset resolution,
Editing Advisor owns timed edit direction, Remotion owns implementation and
rendering, and QA/review own judgment.

### Production owner contract

For every production sequence, emit each applicable sibling as its own action;
name its sole primary output, acceptance/blocker state, and next handoff. Do
not compress these rows into a generic “production” or “asset” phase.

| Sole owner | Primary output | Parent behavior |
| --- | --- | --- |
| `storyboard` | accepted narrative, beats, and scene map | order it and aggregate its output by reference |
| `asset-advisor` | accepted media bundles, provenance/rights receipts, and the selected image/video/avatar/audio realization-child route | order the returned specialist action; never reselect it |
| `editing-advisor` | accepted frame- or time-addressed edit direction covering applicable pacing, cuts, captions, transitions, and compositing | pass the accepted recipe downstream; never assign it to Asset Advisor or Remotion |
| `remotion` | implemented deterministic timeline, encoded deliverable, and render proof | invoke only after required media and edit direction are accepted |
| `review` / `qa` | independent evidence and readiness verdict | record the verdict; never let a production owner self-approve |

An omitted applicable row is an incomplete action list. Asset Advisor may
select a realization child, but Editing Advisor and Remotion are always sibling
lanes rather than Asset Advisor children.

```text
ActionRow {
  owner
  accepted_inputs
  primary_output
  acceptance_or_blocker
  next_handoff
}
```

Emit all five fields in the ticket's `Change Plan` for every applicable row,
including when inputs are already accepted. Never turn an accepted upstream
input back into a blocker. Grouped owner rows and a Remotion handoff without
accepted storyboard, media, and edit receipts are incomplete.

## Skill Signature

```text
content_impl_plan(ticket_or_intent, creative_context?, production_constraints?)
  -> canonical_ticket + next_owner | blocked_report

state:
  reads(user brief, optional approved Brand Kit snapshot, optional complete
        Tasty Pack captures, proof/examples/swipes, canonical ticket?,
        qa_checklist.md)
  writes(canonical ticket.md)

owns: parent creative direction, ordered child-action graph, dependency and
      proof contract

gates: target_and_audience_bound; creative-context decision recorded;
       every applicable action has one owner/output/handoff;
       child dependencies and terminal proof ordered; no child artifact
       impersonated by the parent

routes:
  storyboard | asset-advisor | editing-advisor |
  remotion | social-content | review | qa

fails: second-authoring a child output; grouped/ownerless action; provider
       selection duplicated after Asset Advisor; renderer before accepted
       dependencies; review treated as implementation
```

## Ticket Addition

Start with [tickets/templates/ticket.md](../../tickets/templates/ticket.md).
Do not create a content ticket template, plan file, or program schema. Add only
this block under its existing `Change Plan`:

```md
### Content Production

- Target / audience / platform:
- Creative hypothesis / accepted references:
- Constraints / timing assumption:

| Order | Owner | Accepted inputs | Primary output | Gate or blocker | Next handoff |
| ---: | --- | --- | --- | --- | --- |
```

Put required receipts in the ticket's existing `Done` and `QA Strategy`, and
child artifacts in `Links`. Omit fields that do not affect the selected
deliverable; child skills own their detailed packets.

## Production Contract

After binding the brief, load
[production contract](references/production-contract.md) before compiling the
ticket. It owns visual-direction composition, Resource Bank readiness,
`creative_lock`, and deliberate scene-packet approval.
For narrative, persuasive, editorial, documentary, explainer, or launch work,
also load [storytelling, asset evidence, and persona review](references/storytelling-asset-persona.md).
It owns the resolved ICP, causal/viewer-state beat contract, evidence-ranked
asset decisions, thumbnail/animatic passes, and blocking persona-review receipt.
For every visual production scene, also load
[scene asset bundles](references/scene-asset-bundles.md). It owns the mandatory
background/main-topic/foreground manifest, genuine-asset rule, readiness
states, and representative layered-frame gate.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the canonical ticket and content target.
  - [ ] Read or create the ticket; record audience, promise, platform, target
    deliverable, constraints, proof need, Brand Kit/Tasty Pack decisions, and
    exact blockers without inventing a third style source.
- [ ] 2. Resolve plan-owned creative direction.
  - [ ] Record the hypothesis, high-level story or format intent, accepted
    references, timing/topology assumptions, and falsifier in `Change Plan`.
    Load detailed production references only for the selected content type.
- [ ] 3. Populate the content action graph in `Change Plan`.
  - [ ] Add every applicable action with its sole owner, accepted inputs,
    primary output, acceptance/blocker, and next handoff. Schedule
    [Storyboard](../storyboard/SKILL.md) before
    [Asset Advisor](../asset-advisor/SKILL.md); schedule Asset Advisor before
    its selected realization children; keep
    [Editing Advisor](../editing-advisor/SKILL.md) and
    [Remotion](../remotion/SKILL.md) as sibling lanes.
- [ ] 4. Make the ticket executable without child impersonation.
  - [ ] Put dependency unlocks and terminal receipts in `Done` and `QA Strategy`;
    link accepted child work. Provider choice remains with Asset Advisor;
    `review` judges a material plan and `qa` judges a produced artifact.
- [ ] 5. Return the ticket and next executable owner.
  - [ ] Return `plan_ready` with the canonical ticket and first unblocked action,
    or an exact action-level blocker. Do not create a duplicate plan artifact.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Do not make `storyboard` carry the whole implementation plan. Storyboard owns
  narrative and scene design; this skill owns the parent ticket and production
  action list. Returning the accepted storyboard ref does not make this skill a
  second storyboard author.
- Do not choose an asset realization route twice. Asset Advisor owns the
  `reuse | source | inspired_generation | original_generation | capture |
  compose` decision; this skill orders the returned specialist action.
- Do not reintroduce `style_profile` as an alias, fallback, or third
  composition source. A saved capture may be compiled by
  `ingest-content:compile-style-profile`, but an active content ticket still
  uses only its Brand Kit and optional Tasty Pack.
- Do not let a child consume only an element title or description. Selected
  work is conditioned on its resolved golden example and golden recipe, with a
  receipt mapping the realized output back to the element ID.
- Do not send editing elements directly from the leverage map to Remotion.
  `editing-advisor` owns compatibility and the ordered edit recipe; Remotion
  owns deterministic implementation and rendered proof.
- Do not let “original,” “rights-safe,” “deterministic,” or “local-only” become
  permission to skip asset discovery and draw the content as custom SVG/JSX.
  Those constraints change source selection; they do not remove the
  `asset-advisor` search gate.

## Reference Map

- `references/production-contract.md` - load after brief binding and before
  ticket compilation for Resource Bank readiness, creative lock detail, scene
  approval, and selected production requirements.
- `references/storytelling-asset-persona.md` - load for narrative/persuasive
  work; owns ICP resolution, causal beats, asset evidence, story passes, and
  persona review.
- `references/scene-asset-bundles.md` - load for every visual production scene;
  owns concrete background/main-topic/foreground bundles, readiness states,
  and the representative frame gate.
- `references/newsprint-treatment.md` - load for newspaper/newsprint visual
  direction; owns source-honest texture classification, raster paper sourcing,
  compositing handoff, Brand Kit placement, and final-resolution proof.
- `qa_checklist.md` - read at start and finish for content implementation plan
  QA.
- `../storyboard/SKILL.md` - narrative, script, beat sheet, and scene map.
- `../asset-advisor/SKILL.md` - asset inventory, recreation plan, and owner
  routes.
- `../avatar-advisor/SKILL.md` - child avatar realization contract used only
  after Asset Advisor selects that route.
- `../audio-advisor/SKILL.md` - child audio realization contract used only
  after Asset Advisor selects that route.
- `../ingest-content/references/compile-style-profile.md` - load only for an
  explicit saved-capture-to-profile request outside the current ticket's
  Brand Kit plus Tasty Pack composition.
- `../storyboard/references/scene-grid-production.md` - load for
  deliberate-scene-break model-native video; owns per-scene grids, approval,
  reuse locking, and Remotion assembly handoff.
- `../ai-image-advisor/SKILL.md` - child image realization contract used only
  after Asset Advisor selects that route.
- `../ai-video-advisor/SKILL.md` - child model-native video contract used only
  after Asset Advisor selects that route.
- `../editing-advisor/SKILL.md` - editing-technique retrieval, compatibility,
  method selection, ordered edit recipe, and renderer handoff.
- `../remotion/SKILL.md` - React composition, stitching, captions, audio
  placement, and local render proof.
- `../remotion/references/documentary-reel.md` - load for a voice-led
  documentary/editorial reel using layered stills, prepared overlays, shared
  treatment, and frame-addressed motion.

## Output

- `canonical_ticket`: one ticket using `tickets/templates/ticket.md`, with a
  Content action graph in `Change Plan`, proof in `Done` and `QA
  Strategy`, and links to accepted child outputs.
- `blocked_report`: exact incomplete action, missing accepted input, and the
  owner that must resolve it. It never pretends a child delivery is complete.
