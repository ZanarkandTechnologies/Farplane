---
template_id: taste-loop-taste-proposal
template_version: "0.1.0"
owner: taste-loop
kind: planning-artifact-template
---

# Taste Proposal

Use this for Taste Loop planning feedback when Kenji needs enough detail to
judge whether an artifact is worth executing. Treat Kenji like a customer or
first buyer whose taste reaction is the signal, and like a founder deciding
whether this bet is worth making, selling, or testing. Do not make him grade an
internal plan. A hook-only card is not enough unless the artifact itself is
only a hook.

```text
TasteProposal:
  task_context:
  customer_or_buyer:
  bigger_problem:
  wedge:
  proposed_solution:
  offer_or_artifact:
  distribution_angle:
  validation_question:
  customer_pitch:
  title:
  one_line_bet:
  audience_or_buyer:
  taste_insight:
  artifact_shape:
  core_angle:
  execution_beats:
    - beat_1:
    - beat_2:
    - beat_3:
    - beat_4:
    - beat_5:
  why_it_could_win:
    - reason_1:
    - reason_2:
    - reason_3:
  what_would_make_it_cringe:
    - risk_1:
    - risk_2:
  references_or_taste_pack:
  feedback_question:
  next_if_approved:
  pivot_trigger_if_rejected:
```

Telegram digest shape:

```text
Review artifact: <artifact type Kenji is judging, e.g. social-thread premise / customer-facing idea>
Skill/workflow: <owner skill and concrete workflow, e.g. social-content -> Twitter/X thread planning>
Product: <product/lane/context, e.g. AGI Toy Shop / Pocket Intern>
Stage: <planning | execution | revision>; <not drafting/posting/building unless explicitly true>
Not judging: <common confusions, e.g. video, product build, final copy, or external posting>

Context: <what we are trying to make and for whom>
Customer: <buyer or user whose reaction matters>
Problem: <the bigger painful or funny customer problem>
Wedge: <why this angle can break through>
Solution: <how this product/artifact solves it>
Distribution angle: <where this would get attention or buyer pull>
What you are judging: <one clear founder decision Kenji should make>

A. <title>
Pitch: Imagine <customer-facing version of the idea in vivid marketing language>
Why it might work: <customer desire, taste insight, or conversion reason>
How it shows up: <3-5 compressed execution beats>
Best moment: <specific line, visual, scene, or mechanic>
Risk: <what could make it cringe>
If approved: <next bet or execution artifact>
If rejected: <what would pivot: customer, problem, wedge, offer, or channel>
```

The first screen should answer "what artifact is this?", "which skill/workflow
is being exercised?", "what product or lane is this for?", and "what am I not
judging?" before the pitch. Then answer "what problem are we solving?" and "why
should I care?" before listing options. The option copy should feel like a
founder/customer pitch someone could get excited about, not a row from a
planning spreadsheet.
