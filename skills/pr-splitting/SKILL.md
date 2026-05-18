---
name: pr-splitting
description: Use when a finished working branch needs to be broken into smaller non-stacked pull requests, preferring feature-first slices and falling back to layer-based buckets when feature seams are too entangled.
tier: 3
group: coding
allowed-tools: Read, Glob, Grep, Bash
---

# PR Splitting

Use this after the code already works.

This skill is not for stacked PRs, speculative pre-planning, or hunk surgery. It
is for turning one large finished diff into a smaller set of honest,
reviewer-friendly PR plans.

## Job

1. Inspect the final diff against a chosen base branch.
2. Prefer feature-first PR buckets when they can merge cleanly against base.
3. Fall back to layer-based buckets only when feature seams are too entangled.
4. Avoid hunk-based splitting as the default move.
5. Refuse fake decomposition when the work is too coupled for honest
   non-stacked PRs.
6. Return a concrete PR split plan with exact file lists and branch steps.

## Use When

- the branch is already working end to end
- the diff is too large for comfortable review or CI throughput
- the operator wants non-stacked PRs rather than stacked dependencies
- the main question is how to carve the final state into reviewer-friendly
  slices

## Do Not Use When

- the work is still being implemented
- stacked PRs are acceptable or preferred
- the operator wants to reconstruct a perfect semantic commit history
- the only way to split is invasive hunk cherry-picking across the same files
- the diff is already small enough to review honestly as one PR

## First-Load Checklist

Ensure an agent can execute the core path after only reading this file.

- Trigger conditions:
  - finished branch, oversized diff
  - non-stacked review workflow
  - need for a concrete PR split artifact rather than generic advice
- Workflow:
  1. choose the base branch and inspect the diff
  2. try feature-first grouping
  3. test each group for clean mergeability against base
  4. if feature-first fails, try layer-based grouping
  5. apply size thresholds and shared-file checks
  6. refuse hunk-based fake independence
  7. emit the PR plan with exact file lists and blocker notes
- Core decision branches:
  - coherent feature seams exist -> feature-first PRs
  - feature seams are too entangled -> layer fallback
  - every split depends on another split -> recommend fewer PRs or one PR
- Top gotchas:
  - do not optimize for line-count symmetry over reviewer clarity
  - do not hide shared files in a vague misc bucket
  - do not pretend a PR is independent if it cannot merge or run cleanly
- Outcome contract:
  - each proposed PR has one reviewer story
  - each proposed PR lists exact files
  - the skill says when not to split

## Documentation Index

- Decision rules: [`references/decision-rules.md`](references/decision-rules.md)
- Output template: [`references/output-template.md`](references/output-template.md)

## Default Policy

- prefer feature-first PRs when they can merge cleanly and tell one coherent
  reviewer story
- fall back to layer-based buckets such as `frontend`, `backend`, `schema`,
  `infra`, `tooling`, `docs`, or `tests` when feature-first grouping becomes
  too entangled
- target under `5k` changed lines per PR when feasible
- warn or refuse above `10k` changed lines per PR unless the work is truly
  inseparable
- avoid hunk-based splitting by default; only tolerate it for narrow mechanical
  cases where review clarity is still obvious

## Workflow

1. Choose the comparison base:
   - usually `main`, `master`, or the branch intended for merge
   - if the operator has a different merge target, use that explicitly
2. Inspect the final diff:
   - changed files
   - rough added/removed line counts
   - files shared across multiple candidate stories
   - contract-touching files such as schema, API, shared types, config, and
     routing
3. Try a feature-first pass:
   - identify end-to-end user-facing or operator-facing capabilities
   - keep backend, frontend, tests, and docs together when they form one honest
     feature slice
   - reject a feature bucket if it cannot merge cleanly against base on its own
4. If feature-first is too entangled, try a layer-based pass:
   - frontend
   - backend
   - schema/data
   - infra/tooling
   - docs
   - tests when they are clearly separable
5. Apply the decision rules from
   [`references/decision-rules.md`](references/decision-rules.md):
   - mergeability first
   - coherent reviewer story second
   - ownership clarity third
   - size pressure after honesty
6. Check for blockers:
   - shared files needed by multiple buckets
   - contract changes that require paired consumers
   - generated files with ambiguous ownership
   - broad refactors that only make sense with the behavior change
7. Produce a PR plan using
   [`references/output-template.md`](references/output-template.md).

## Decision Branches

- **Branch A: feature-first works**
  - keep each PR end to end
  - let tests and docs travel with the feature
  - avoid artificial backend/frontend separation
- **Branch B: feature-first is too expensive or dishonest**
  - switch to layer buckets
  - keep each bucket mergeable against base
  - explain why feature-first was rejected
- **Branch C: refactor plus behavior are tangled**
  - either isolate a narrow mechanical prep PR
  - or keep the refactor attached to the behavior bucket it explains
- **Branch D: non-stacked split is not honest**
  - recommend fewer PRs or one PR
  - state the exact blockers instead of forcing decomposition

## Output Contract

Return one compact PR split note with:

- `Base branch`
- `Split strategy`: `feature-first` or `layer-fallback`
- `Why this strategy won`
- `PR buckets`
- `Blockers or refusal reason`
- `Branch steps`

For each PR bucket include:

- `PR name`
- `Reviewer story`
- `Why independent`
- `Exact files`
- `Approx size`
- `Risk notes`

If refusing to split, return:

- `Why non-stacked split is dishonest`
- `Which files or contracts create the coupling`
- `Best fallback`: fewer PRs, one PR, or revisit the implementation before
  splitting

## Guardrails

- do not default to hunk cherry-picking across the same file
- do not force perfect size equality across PRs
- do not separate contract changes from non-backward-compatible consumers
- do not create a cleanup bucket that exists only to hide uncertainty
- generated files, lockfiles, and snapshots should stay with their owning source
- colocated tests should stay with the behavior they validate
- docs should travel with the code change unless they are independently
  reviewable

## Minimal Example

```text
Base branch: main
Split strategy: feature-first
Why this strategy won: the diff contains two mergeable user stories plus one
small shared tooling update

PR 1: client intake flow
- Reviewer story: add the intake wizard end to end
- Why independent: backend routes, UI screens, and tests merge cleanly against base
- Exact files:
  - app/intake/*
  - api/intake.ts
  - tests/intake.test.ts
- Approx size: 3.8k changed lines

PR 2: invoice generation
- Reviewer story: add invoice generation end to end
- Why independent: invoice flow does not depend on the intake feature bucket
- Exact files:
  - app/invoices/*
  - api/invoices.ts
  - tests/invoices.test.ts
- Approx size: 4.6k changed lines

PR 3: shared tooling
- Reviewer story: upgrade build config needed by both features
- Why independent: config change merges cleanly and does not depend on feature code
- Exact files:
  - package.json
  - pnpm-lock.yaml
  - vite.config.ts
- Approx size: 0.4k changed lines
```
