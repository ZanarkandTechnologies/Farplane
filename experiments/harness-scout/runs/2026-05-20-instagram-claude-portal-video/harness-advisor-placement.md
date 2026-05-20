# Harness Advisor Placement Decision

## Decision

Place the capability as a `harness-scout` video reconstruction method first,
with an optional future dedicated Tier 3 skill only if repeated runs show it
deserves a standalone package.

The concrete capability gap is: Codexter can ingest videos as source evidence,
but it does not yet have a repeatable method for extracting representative
frames, inferring a visual build workflow, converting that into a skill
proposal, and handing implementation to the right owner.

## Current Evidence

- `FEAT-0011` covers source ingestion through `harness-scout`, but known limits
  say it is manual and scorecard-based.
- `FEAT-0014` covers frontend skill parity, so this source should not trigger a
  broad frontend skill rewrite.
- `video-production`, `video-generation`, and `remotion` own video creation,
  not external video understanding.
- `frontend-craft`, `landing-page`, and `visual-qa` are the right downstream
  owners if the operator later wants the portal page rebuilt.
- `docs/specs/harness-engineering-doctrine.md` says to prefer the smallest
  surface that fixes the failure and use skills for procedural consistency.

## Existing Feature/Skill Match

Partial match:

- `harness-scout`: source ingestion, dedupe, scoring, decisions.
- `harness-advisor`: placement decision.
- `skill-creator`: skill package quality contract.
- `frontend-craft`/`visual-qa`: downstream implementation and visual proof.

No exact match for "video frames -> reconstruction storyboard -> skill proposal
-> optional remake brief."

## Options

1. Extend `harness-scout` with a method `harness-scout:video-reconstruction`.
   Pros: smallest owner, uses existing source registry/run artifact model,
   keeps video evidence untrusted, easy to validate with this run. Cons: can
   make `harness-scout` broader unless the method stays compact.

2. Create a new Tier 3 skill `video-reconstruction-scout`.
   Pros: clear trigger, focused workflow, can own frame extraction scripts and
   templates. Cons: risks duplicate source-ingestion behavior already owned by
   `harness-scout`; premature until multiple runs prove demand.

3. Put rules into root `AGENTS.md` or `templates/global/AGENTS.md`.
   Pros: agents see the rule early. Cons: wrong primary surface; this is a
   repeatable workflow, not a global invariant, and root policy would bloat.

## Recommendation

Choose option 1 now: add a compact `harness-scout:video-reconstruction` method
that can call `skill-creator` for the proposed skill shape and downstream
`frontend-craft`/`visual-qa` for actual remakes.

## Tradeoff Accepted

This keeps the first implementation small and avoids over-promoting one
Instagram test into a standalone skill before the workflow has repeated
evidence.

## Primary Owner

`skills/harness-scout`

## Secondary Sync Points

- `skills/skill-creator` for the first-load skill contract.
- `skills/video-production` only for production/storyboard terminology.
- `skills/frontend-craft`, `skills/landing-page`, and `skills/visual-qa` for
  implementation handoff when the operator asks to rebuild the visible artifact.
- `docs/features/registry.jsonl` only after the method ships as durable feature
  knowledge.

## Validation

- Run the method on this Instagram source and one local MP4 fixture.
- Require a contact sheet, selected frames, storyboard, event timeline,
  confidence notes, and a skill proposal.
- Review against `evidence-quality`, `user-intent-satisfaction`, and
  `integration-readiness`.

## Next Ticket

`TASK-video-reconstruction-scout-method`: Add
`harness-scout:video-reconstruction` with frame extraction guidance, source-run
templates, selected-frame evidence rules, and a skill-proposal handoff section.
