---
template_id: taste-loop-taste-proposal
template_version: "0.1.0"
owner: taste-loop
kind: planning-artifact-template
---

# Taste Proposal

Use this for Taste Loop planning feedback when Kenji needs enough detail to
judge whether an artifact is worth executing. Treat Kenji like a customer or
first buyer whose taste reaction is the signal, not like an internal reviewer
grading a plan. A hook-only card is not enough unless the artifact itself is
only a hook.

```text
TasteProposal:
  task_context:
  bigger_problem:
  proposed_solution:
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
```

Telegram digest shape:

```text
Context: <what we are trying to make and for whom>
Problem: <the bigger painful or funny customer problem>
Solution: <how this product/artifact solves it>
What you are judging: <one clear decision Kenji should make>

A. <title>
Pitch: Imagine <customer-facing version of the idea in vivid marketing language>
Why it might work: <customer desire, taste insight, or conversion reason>
How it shows up: <3-5 compressed execution beats>
Best moment: <specific line, visual, scene, or mechanic>
Risk: <what could make it cringe>
If approved: <next execution artifact>
```

The first screen should answer "what are we making?", "what problem are we
solving?", and "why should I care?" before listing options. The option copy
should feel like a pitch someone could get excited about, not a row from a
planning spreadsheet.
