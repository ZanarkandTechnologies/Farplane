---
ticket_id: TASK-0091
title: add qa cookbook and browser automation policy
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-04-24T18:35:00Z
updated_at: 2026-04-24T18:42:00Z
next_action: archived; use `qa/README.md` plus `qa/cookbook/*.md` for future browser-QA slices
last_verification: `python3 tickets/scripts/check_ticket_metadata.py` and `git diff --check`
linked_docs:
  - docs/specs/agent-testability-surfaces.md
  - skills/testing/references/testing-strategy-decision-tree.md
  - skills/agent-browser/references/qa-workflows.md
---

# TASK-0091: add qa cookbook and browser automation policy

## Summary
Codexter already has the right raw ingredients for browser QA, but the operator-facing workflow is still scattered across skills and agent prompts. This ticket adds one visible `qa/` surface for reusable runbooks and makes the default split explicit: stable UX regression belongs in Playwright, while `agent-browser` is the fast lane for discovery, artifact capture, and debugging when a scripted flow is still being proven or has started failing.

## Scope
- In:
  - add a repo-level `qa/` module with a cookbook surface for deterministic app-entry guidance
  - document the recommended Playwright-versus-`agent-browser` workflow
  - update existing QA/testability docs so the new surface is discoverable
- Out:
  - adding Playwright packages, CI jobs, or runnable app-specific tests
  - changing the execution runtime or Stop-hook logic

## Plan
- `Change:` add `qa/README.md`, `qa/AGENTS.md`, and a cookbook template; update the existing testing, agent-browser, and qa-tester guidance to point at the new surface and prefer Playwright for stable browser regression
- `Why:` the current guidance implies the split, but it does not give operators one place to store route shortcuts, deep links, seeded states, or test-only helpers that make browser QA fast and repeatable
- `Before -> After:`
  - `Before:` browser QA policy is distributed across skills and agent prompts, and there is no repo-owned cookbook for deterministic app entry
  - `After:` the repo exposes one explicit QA module with a reusable cookbook shape and a clear default workflow for Playwright plus `agent-browser`
- `Touch:` `qa/`, `agents/qa-tester.toml`, `skills/testing/references/testing-strategy-decision-tree.md`, `skills/testing/references/agentic-testing-instrumentation.md`, `skills/agent-browser/references/qa-workflows.md`, `skills/qa/README.md`, `README.md`, `docs/MEMORY.md`, `docs/HISTORY.md`
- `Inspect:` `agents/qa-tester.toml`, `skills/testing/SKILL.md`, `skills/agent-browser/SKILL.md`, `docs/specs/agent-testability-surfaces.md`, `tickets/README.md`
- `Signature delta:` none
- `Type Sketch:` none
- `Typed flow example:` none
- `Recommendation:` codify a Playwright-first regression policy and treat `agent-browser` as the proof-of-work plus debugging lane, with repo-level QA cookbooks capturing the shortcuts and instrumentation needed to make both fast
- `Blast radius:` QA guidance, skill discoverability, and future ticket plans that need deterministic browser proof
- `Risks:` over-documenting without improving discoverability; introducing a QA folder that duplicates ticket artifact storage instead of complementing it

## Gap Analysis
- `Current state:` the repo already distinguishes QA operation from visual judgment and already mentions Playwright, `agent-browser`, and testability instrumentation, but the guidance is spread across multiple skills and there is no canonical place for reusable app-entry guides
- `Production expectation:` a credible browser-automation workflow keeps regression proof in code, keeps exploratory browser driving available for debugging, and preserves deterministic shortcuts/hooks in one visible cookbook so tests do not depend on rediscovering the UI manually
- `Missing gaps:` explicit policy for which browser tool to reach for first, a canonical repo-owned place to store deep links and shortcuts, and a template that turns missing determinism into planned instrumentation instead of QA improvisation
- `Comparable implementations:` local Codexter QA/testing/agent-browser surfaces only; this ticket is codifying the repo's existing direction rather than importing a new external framework
- `Recommendation:` ship the cookbook and policy now, and leave actual app-specific Playwright suites or instrumentation helpers to later feature tickets

## Acceptance Criteria
- [x] AC-1: the repo contains a visible `qa/` module with `README.md`, `AGENTS.md`, and a reusable cookbook template for deterministic browser-entry guidance
- [x] AC-2: the canonical QA/testing docs state that Playwright is the default tool for stable end-to-end UX regression, while `agent-browser` is the fast discovery and debugging lane
- [x] AC-3: `qa-tester` guidance tells QA to read the repo-level QA cookbook when present before driving the browser

## Verification
- `Tests:` `python3 tickets/scripts/check_ticket_metadata.py`; `git diff --check`
- `Manual checks:` read the new `qa/` docs plus updated QA/testing surfaces and confirm the workflow is consistent
- `Evidence required:` linked ticket plus doc diffs showing the new QA surface and the policy updates
- `Artifacts path:` `tickets/artifacts/TASK-0091/`

## Evidence
- `Artifacts:`
  - [review.md](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0091/review/2026-04-24_194200_policy-review/review.md)
  - [review.json](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0091/review/2026-04-24_194200_policy-review/review.json)
- `Commands:`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Result summary:` added a repo-owned `qa/` cookbook surface, aligned QA guidance around a Playwright-first regression policy, and passed a final review with no blocking findings

## Blockers
- none
