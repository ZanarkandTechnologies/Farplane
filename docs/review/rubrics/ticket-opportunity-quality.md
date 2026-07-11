# Ticket Opportunity Quality

Use this family when reviewing AI-generated ticket specs, project bets, or
Pulse refill candidates before worker admission.

## What This Judges

This rubric judges whether a candidate ticket is worth a worker cycle. Valid
metadata is not enough. The ticket must advance a goal or metric, name a clear
ICP or operator audience, a concrete artifact, current relevance or source-gap
honesty, state-of-art/default-workflow pushback, and ticket-owned learning
writeback.

Default posture is reject-first. A reviewer should look for the best reasons
the ticket is boring, low leverage, not ICP-resonant, below the current bar, or
not worth Kenji's review attention before admitting it.

## TAS Guide

- `TAS-A`: candidate is goal- or metric-backed, executable, reviewable, non-boring,
  safely gated, and has clear learning writeback.
- `TAS-B`: promising but needs repair to ICP, artifact ambition, baseline,
  evidence refs, execution rationale, review surface, or learning writeback.
- `TAS-C`: generic, boring-but-valid, unsafe, duplicate without material
  improvement, self-referential planner work, or disconnected from goals and
  metrics.
- `TAS-D`: candidate spec, project context, or evidence refs are missing.

## Required Checks

- `reward_trace`: ticket reward, goal or metric, and output artifact align.
- `capability_fit`: the owning capability skill and workflow are named when
  specialized execution is required.
- `icp_resonance`: ICP/operator audience and why they care now are concrete.
- `relevance`: Feed Scout/source evidence or an explicit source gap is named
  when market-facing.
- `sota_pushback`: reviewer can see the default/current/competitor-like bar and
  why the candidate might still fall short.
- `artifact_ambition`: artifact level matches the intended outcome and is not just
  a note, reminder, receipt, or admin capture.
- `execution_rationale`: worker can start without rediscovering the idea.
- `dedupe`: prior attempts are named or absence is justified.
- `learning_writeback`: the ticket, Goal Packet progress, or report writeback
  target is named.
- `review_surface`: Kenji/reviewer has a concrete artifact to inspect and a
  Telegram-first review path when appropriate.

## Blocker Checks

- Candidate asks the worker to decide what idea is worth doing.
- Candidate's main output is planner, Pulse, generator, metadata, or
  maintenance cleanup that does not directly unblock goal- or metric-backed work.
- Candidate includes final post/publish/spend/deploy/external-contact/account
  mutation/destructive cleanup without human gate.
- Candidate uses fake scalar market or SOTA scoring without evidence.
- Candidate omits ticket-owned learning writeback.

## Evidence Cues

- `farplane/metrics.yaml` optimization contract and current readings
- `farplane/metrics.yaml`
- owning capability skill and workflow references
- ticket-local `program.md`, `progress.md`, or explicit source gap
- recent ticket artifacts and rejection reasons
- Feed Scout/source refs for distribution and market-learning
- `skills/ticket-opportunity-generator/qa_checklist.md`

## Finding Cues

Prioritize findings that prevent bad worker tickets: weak goal/metric trace, weak ICP,
low artifact ambition, no baseline, duplicate idea, unsafe gate, or missing
learning writeback.
