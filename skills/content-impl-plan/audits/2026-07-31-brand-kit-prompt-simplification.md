---
title: Brand Kit prompt simplification
date: 2026-07-31
skill: content-impl-plan
mode: refine_skill
verdict: accepted
---

# Brand Kit prompt simplification

## Delta

- Before: a proposed `productionProfile` schema and resolver converted Brand
  Kit advisor choices into structured configuration with separate revisioning.
- After: the proposal is removed. The existing kit-wide prompt carries all
  provider, model, voice, format, and advisor direction as prose and is passed
  intact to selected child advisors.
- Approved Brand Kit `elements[]` and their realization packets are unchanged.

## Ownership

- Brand Kit prompt: kit-wide creative and production direction.
- Child advisors: interpret that direction using agent judgment.
- Skill-local `config.toml`: standalone fallback only.
- Runtime: credentials.

## Proof

- Structured schema, mutation, UI editor, resolver, reference, and tests were
  removed.
- Resource Bank focused tests and root typecheck pass.
- Audio Advisor Fish execution/packet tests pass.
- Eval execution skipped: the correction removes deterministic machinery and
  adds no new variable prompt behavior; focused tests plus independent review
  are the narrower proof surface.
