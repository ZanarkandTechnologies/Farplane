---
title: Advise change-preview hardening
status: complete
owner: advise
date: 2026-08-23
kind: skill-audit
---

# Advise Change-Preview Hardening

## Behavior delta

> **Before:** `advise` could recommend a behavior change without making the
> current gap or expected effect inspectable. The ticket `Delta` described
> generic current and intended behavior without requiring evidence or a causal
> link.
>
> **After:** Behavior-changing advice includes a source-backed Change preview;
> ticket Deltas ask for the observed gap, the smallest intended change, and its
> expected effect.
>
> **Example:** Rather than “add preview guidance,” the recommendation says that
> `advise` has no preview field, adds one concise requirement, and makes the
> resulting decision comparison inspectable before editing.

## Ownership and proof

- Primary owner: `skills/advise/SKILL.md` owns reusable advice output.
- Secondary owner: `tickets/templates/ticket.md` owns durable implementation
  deltas.
- Rejected: `templates/global/AGENTS.md` already requires Before/After/Example
  previews for policy, prompt, workflow, UX, and architecture changes.
- Scope: concurrent changes to `advise` deliberation/reference routing and the
  ticket template's structural sections predated this hardening. They are
  excluded from this audit and are not evidence for the Change preview delta.
- Validation passed: `git diff --check`,
  `python3 skills/skill-maintenance/scripts/check_skills.py`, and
  `python3 -m unittest bin.validators.test_harness_invariants`.
- Review passed: independent scoped contract review returned `TAS-A` on
  2026-08-23.
