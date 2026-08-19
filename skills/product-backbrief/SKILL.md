---
name: product-backbrief
description: "Turn an extended product discussion into an operated product story, ASCII system map, explicit assumptions, and alignment questions before commitment."
tier: 2
source: local
template_uses:
  skill-template: "0.4.0"
  skill-qa-checklist: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep
---

# Product Backbrief

## Context

Use this after a substantial product discussion when the operator wants to
check whether the agent understands the intended product before requirements,
tickets, or implementation are committed. It reconstructs the product as a
user-operated story, not as a transcript summary or feature inventory.

This is a read-only alignment workflow. `task-recap` recovers what happened in
a paused task; `product-backbrief` tests what the recovered discussion means
for the product. Accept a task recap as optional input, but do not invoke it for
a live discussion whose product context is already available.

## Skill Signature

```text
product_backbrief(discussion, product_context?, task_recap?, focus?)
  -> proposed_shared_model

state: reads(conversation, accepted decisions, product artifacts?, task recap?);
  writes(none)
owns: one proposed product model for operator correction
gates: product_boundary_bound; decisions_and_inferences_separated;
  operated_story_complete; relationships_legible; human_alignment_pending
routes: direct-answer | task-recap | deep-interview | prd | impl-plan
fails: transcript summary; feature inventory; invented certainty;
  status recap; implementation before alignment; proposed model called approved
```

## Phase Boundary

Use `task-recap` first only when a paused task's authoritative history is
needed. Route unresolved product decisions to `deep-interview`; route an
operator-confirmed model to `prd` or `impl-plan`. Do not externalize those
phases merely to produce the backbrief.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the product and the alignment question from the discussion,
  supplied artifacts, and optional task recap; name a source gap instead of
  inventing missing product history.
- [ ] 2. Separate confirmed decisions, inferred assumptions, contradictions,
  and unresolved choices before constructing a coherent model.
- [ ] 3. State one product promise, then narrate one realistic user journey
  from trigger through system behavior to user value.
- [ ] 4. Show the important objects, states, ownership, or data flow in compact
  ASCII when relationships matter; keep nouns consistent between story and map.
- [ ] 5. State boundaries and non-goals, then end with two to five questions
  that target the highest-risk possible misunderstandings. Label the entire
  result as proposed until the operator confirms or corrects it.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Default response shape:

```text
Product promise
Operated story
System view (ASCII when relationships matter)
Boundaries and non-goals
Confirmed decisions / assumptions / conflicts
Alignment questions
```

Positive example:

```text
Discussion: A content product mixes videos, news, topics, and entities.
Backbrief: "Content stores sources; News groups verified developments; Wiki
tracks durable entities; Topics navigate. Coverage means sources about the
same event." The ASCII flow follows one video from ingest to verified event,
then asks whether Topics should remain a visible destination.
```

## Gotchas

- Do not retell the conversation chronologically; reconstruct the intended
  product from the user's point of view.
- Do not force agreement by smoothing over conflicting decisions or replacing
  uncertainty with polished prose.
- Do not use a generated summary as evidence; link or name source artifacts
  when the proposed model depends on them.
- Do not write a PRD, ticket, or implementation plan until the operator accepts
  the product model or explicitly requests that downstream artifact.

## Reference Map

- [Task Recap](../task-recap/SKILL.md) — use first only when a paused task's
  authoritative state must be recovered before product alignment.
- [Deep Interview](../deep-interview/SKILL.md) — use when the backbrief exposes
  unresolved intent that requires further questioning.
- [PRD](../prd/SKILL.md) — use after the operator confirms a product model that
  needs a durable product requirements artifact.
- [Impl Plan](../impl-plan/SKILL.md) — use after the confirmed model already has
  an implementation-ready scope.

## Output

- `proposed_shared_model`: product promise, operated story, compact system view,
  boundaries, labeled assumptions/conflicts, and focused alignment questions.
