---
name: demo
description: "Turn passing feature QA into a concise Before/After/Example MP4 that leads the GitHub closeout, with evidence and independent review."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.3.9"
  skill-surface-budget: "0.1.0"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.1"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["close-ticket"]
allowed-tools: Read, Glob, Grep, Bash
---

# Demo

## Context

`demo` is the terminal presentation phase for a material implementation Goal.
It turns already-passing ticket evidence into one concise narrated MP4 for a
lead engineer who needs the problem, decision, result, proof, and remaining
risk without rereading the full ticket.

The default applies to material feature implementation Goals and explicit `$demo`
calls. Direct non-Goal fixes, heartbeats, feedback checks, and planning-only
work do not require a recap. The MP4 explains existing proof; it never replaces
QA or creates new product claims. Default duration is 45–90 seconds. The recap
is optimized for an operator who will watch the video instead of reading the
ticket: `Before`, `After`, one concrete `Example`, and the few `Key decisions`
needed to understand the result. Proof and residual risk stay compact.

## Skill Signature

```text
demo(ticket, passed_qa, brand_kit?) -> narrated_mp4 + evidence_map + result_json + review_receipts
state: reads(ticket, diagrams, progress, QA/test/review evidence, optional brand kit);
       writes(ticket-scoped demo artifacts, ticket Links, progress)
gates: selected_ticket; QA_pass; verified_sources; recap_plan; media_probe;
       independent_demo_video_evidence_review_TAS_A
routes: content-impl-plan | storyboard | audio-advisor | remotion | reviewer
fails: invents evidence; runs before QA passes; emits PPTX instead of MP4;
       generates unsupported visuals; spends without authorization; self-certifies
```

Resolve missing evidence from the selected ticket and its artifact tree. If QA
has not passed or a claim cannot be sourced, return a blocker instead of
guessing.

## Phase Contract

```text
demo(ticket, evidence)
  -> evidence inventory
   + ticket-scoped content plan
   + storyboard and narration
   + deterministic Remotion composition
   + MP4/media verification
   + independent review
   + ticket/progress writeback
```

The content plan is a child artifact of this ticket, not a second content
ticket. Externalized skills specialize production; they do not reopen the
feature scope.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the selected ticket, passing QA result, audience, and optional
  Brand Kit; read `qa_checklist.md` as preflight.
- [ ] 2. Inventory only verified ticket sources: problem/scope, diagrams,
  progress, test output, QA captures, review receipts, and residual risks.
- [ ] 3. Create
  `tickets/TASK-XXXX/artifacts/demo/<timestamp>-<slug>/`, then load
  [the lead-engineer recap recipe](references/lead-engineer-recap.md).
- [ ] 4. Use [content-impl-plan](../content-impl-plan/SKILL.md) in
  ticket-scoped artifact mode to write the recap plan and evidence map; do not
  create another ticket or add per-ticket demo configuration.
- [ ] 5. Route beats and narration to
  [storyboard](../storyboard/SKILL.md), using the default sequence and duration
  from the recipe. Use the visible narrative spine `Before -> After -> Example
  -> Key decisions -> Proof`; every spoken or visible claim must name its
  evidence source.
- [ ] 6. Route authorized narration to
  [audio-advisor](../audio-advisor/SKILL.md) and deterministic assembly to
  [remotion](../remotion/SKILL.md). Reuse verified screenshots, diagrams, logs,
  and text; generated visuals are forbidden by default. If narration approval
  blocks production, preserve the spend-free content plan, evidence map, and
  script before returning the blocker.
- [ ] 7. Render `final.mp4`; verify video, frames, duration, and audible
  narration with `ffprobe` plus representative frame/audio inspection. Write
  `media-probe.json`, `evidence-map.json`, and compatible `result.json`.
- [ ] 8. Send the MP4, evidence map, source artifacts, and `qa_checklist.md` to
  the independent `reviewer` using demo, video, and evidence rubrics. Require
  TAS-A, then link the reviewed artifacts from the ticket and `progress.md`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Do not produce a PowerPoint, slide deck, generic evidence montage, or
  marketing trailer. The default deliverable is one narrated MP4.
- Do not recapture or reinterpret failed behavior to make the story cleaner.
  Return to QA when proof is missing or weak.
- Do not hide provider spend, generated assets, or unsupported facts inside a
  production child route.
- A passing `result.json` means the reviewed recap is present and technically
  playable; it does not weaken the Goal's completion review.

## Output

Write the package under
`tickets/TASK-XXXX/artifacts/demo/<timestamp>-<slug>/`. Every plan or success
summary must name the 45–90 second MP4, glanceable narrative spine, ticket-scoped
path, `evidence-map.json`, deterministic Remotion route, media probe, and TAS-A
review gate.

Finish with:

```text
EXECUTION_RESULT: status=demo_complete next=completion_review reason=<brief>
```

On missing proof, authorization, failed media verification, or sub-TAS-A
review, preserve every spend-free plan/map/script already possible, write a
blocked/revise `result.json` at the ticket-scoped path, and return the exact
recovery owner.
