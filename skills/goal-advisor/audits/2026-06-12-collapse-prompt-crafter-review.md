---
date: 2026-06-12
change: collapse-prompt-crafter-review
skill: goal-advisor
---

# Collapse Goal Crafter Review

## First Principles

Objective: make Goal loops usable for material auto-improvement work without
splitting one decision across tiny prompt-template skills.

The useful function is:

```text
advise_goal_use(intent, state?, constraints?, budget?)
  -> goal_architecture
   + goal_packet
   + native_goal_prompt?
   + next_action
```

The old split had `goal-advisor` choose the architecture and the separate prompt-crafting skill
fill the final prompt. That added a handoff without adding a new judgment
surface. Goal prompt wording depends on the same choices as architecture:
trigger mode, metric provider, drift policy, state surfaces, and stop
conditions. Keeping them together reduces inconsistent prompts.

## Review Findings

| Check | Verdict | Notes |
| --- | --- | --- |
| Single loop owner | pass | Native Goal remains the continuation engine; Goal Packet files are visible state. |
| Human feedback boundary | pass | `with-human` is a provider, not a loop runtime. |
| Prompt/state coherence | pass | `goal-advisor` now owns both Goal architecture and prompt compilation. |
| File write capability | fixed | Added `Write` to `goal-advisor` and `with-human` allowed tools because both may create packet or feedback files. |
| Drift control | pass | `goal-drift-reviewer` is read-only and compares ticket, program, progress, and current continuation claim. |
| Auto-improve content use case | pass with pilot needed | Added a skill-local eval task for content-skill improvement with human feedback; still needs a live pilot ticket before claiming runtime reliability. |
| Heartbeat automation | known limit | Heartbeat is documented as a trigger pattern, not an implemented scheduler. |
| Feedback ingestion | known limit | Human feedback is file/Telegram-request based; no automatic Telegram reply ingest is shipped here. |

## Expected Working Path

1. `goal-advisor` creates or points to a ticket-backed Goal Packet.
2. `program.md` names the loop mode, metric provider, feedback policy, drift
   policy, budget, and stop condition.
3. `progress.md` receives one compact entry per turn.
4. `with-human` creates `feedback-request.md` and a `feedback.json` schema when
   Kenji is the quality signal.
5. Native `/goal` runs from the generated prompt and resumes from the largest
   unresolved acceptance, evidence, blocker, or feedback gap.
6. Drift review is inline for small loops and `goal-drift-reviewer` for
   strategic, long-running, or self-approval-prone loops.

## Residual Risk

This is a contract and skill-system migration, not a live Goal runtime test.
The first production use should be a small content-skill pilot with one ticket,
one `program.md`, one `progress.md`, one `feedback-request.md`, and one drift
review sample before scaling to multiple traps.
