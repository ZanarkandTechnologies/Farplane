---
title: Agent Skills eval comparison metrics
created_at: 2026-06-30
target: Farplane skill system compared with Agent Skills eval and authoring practices
status: draft
---

# Metrics: Farplane skill system compared with Agent Skills eval and authoring practices

## Metric Card

- Target user: Farplane skill author, maintainer, and reviewer.
- Job-to-be-done: know whether a skill is worth loading, triggers correctly, and improves outputs enough to justify its context cost.
- Artifact being improved: `skills/*/SKILL.md`, skill-local eval/QA files, `docs/skills/*`, and `skills/eval` or `skill-maintenance` runner behavior.
- Primary behavior to improve: measurable skill value and selection accuracy.
- Primary metric: validated skill delta, combining output pass-rate delta and trigger validation pass rate for material skill changes.
- Direction: higher output delta and trigger validation pass rate, lower unjustified token/time overhead.
- Guard metric: first-load surface budget and false-trigger rate.
- Anti-metric: higher eval pass rate achieved by keyword overfitting, brittle assertions, or hiding broad routing text in descriptions.
- Minimum meaningful delta: for a material skill hardening pass, at least one real failure becomes a passing assertion or trigger case without increasing false triggers or first-load bloat.
- Measurement method: run skill-local output evals against baseline or previous version; run labeled trigger evals with repeated invocations; record evidence, tokens, duration, and reviewer judgment.

## Judgement Questions

- Is this skill trying to improve output quality, routing/selection, or both?
- Would a no-skill or previous-version baseline already pass the task?
- Which should-trigger prompts are non-obvious enough to prove the description helps?
- Which near-miss prompts are close enough to prove the description is precise?
- Are assertions observable and useful, or are they brittle/always-passing?
- Did the skill buy enough quality to justify extra context, time, and maintenance?
- Did trace review reveal instructions that should be cut, promoted to gotchas, moved to references, or turned into scripts?
