# Best Of Worlds Workflow

Date: 2026-05-03

## Goal

Add a reusable workflow for comparing multiple projects, repos, blogs, or
implementations and turning the best transferable features into a concrete local
design.

Farplane skills are stable local contracts. External skills, repos, blogs, and
command families are research inputs, not live dependencies. This workflow is
the import gate for reviewed `adopt`, `adapt`, `reject`, or `defer` decisions.
See `MEM-0073`.

## Context

The autoresearch skill-suite work exposed a repeatable failure mode: even after
reading strong external examples, an agent can capture the headline idea while
missing concrete operational techniques. `best-of-worlds` fixes that by forcing
source inventory, feature extraction, metric discovery, and
adopt/adapt/reject/defer decisions before implementation.

## Contract

A best-of-worlds pass produces:

- source inventory with credibility notes
- feature ledger with evidence
- metric card or judgement-call questions
- decision matrix with `adopt`, `adapt`, `reject`, or `defer`
- implementation handoff

## Metric Discovery

When the optimization metric is unknown, the workflow asks:

- What user-visible behavior should improve?
- What artifact changes?
- What primary metric can be measured mechanically?
- What guard metric prevents gaming?
- What anti-metric catches regressions?
- What minimum delta is worth keeping?
- Which remaining choice needs `advise`?

## Skill Judgement Questions

New or updated skills should include judgement questions when they require
material choices. These questions tell agents when to use `advise` instead of
pretending an ambiguous product, architecture, metric, or adoption choice is
deterministic.

## Boundaries

- Use `research:parity` for broad category research.
- Use `best-of-worlds` for synthesis from known sources.
- Use `research:gap` for local missing-scope analysis.
- Use `impl-plan` after the synthesis becomes a concrete ticket plan.
- Do not auto-sync external skill behavior into Farplane skills.
