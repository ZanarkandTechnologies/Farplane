---
title: QA and Browser System Guide
status: active
owner: qa
updated_at: 2026-08-03
refs:
  - skills/qa/SKILL.md
  - agents/qa-tester.toml
  - qa/cookbook/README.md
---

# QA and Browser System Guide

Farplane QA turns one ticket claim into inspectable evidence, independent
judgment when required, a canonical receipt, and selective reusable learning.
The ticket owns what must be proved; this guide explains how to run that proof.

```text
qa_journey(ticket, runtime_target?, proof_policy_override?)
  -> choose -> capture -> reconcile -> judge -> receipt -> learn
```

Per-run evidence belongs under `tickets/TASK-XXXX/artifacts/qa/`. Reusable
entry paths, shortcuts, selectors, seeds, and observability belong in
`qa/cookbook/`.

## Start Here

1. **Choose proof.** Read ticket `Done`, `QA Strategy`, optional `Agent
   Contract`, linked specs, and any explicit proof-policy override. Together
   they form the effective proof policy.
2. **Bind the runtime.** Use the ticket/runtime handoff. If an app or API target
   is ambiguous, block instead of guessing a port, URL, session, or account.
3. **Use deterministic entry.** Read the matching cookbook page before manual
   exploration. Prefer a documented route, deep link, seed, reset, shortcut,
   debug control, or test hook.
4. **Capture the real mechanism.** Exercise the implementation that owns the
   result and collect evidence appropriate to the proof type.
5. **Reconcile the claim.** Mark each `Done` and `QA Strategy` obligation
   `PASS`, `FAIL`, or `not_provable` with an artifact path.
6. **Judge separately when required.** Browser operation is not visual or
   completion judgment.
7. **Write the receipt.** Produce `report.md` and validated `result.json`, then
   link the strongest evidence from ticket `Links`.
8. **Learn selectively.** Decide whether the run stays ticket-local, updates a
   cookbook page, or needs an instrumentation follow-up.

## Choose the Proof Route

| Work under test | Normal proof | Owner |
| --- | --- | --- |
| CLI, script, validator, or generated artifact | command output, logs, files, focused tests | `qa` / implementing lane |
| API or integration | bound runtime, responses, logs, traces | `qa-tester` when operated capture helps |
| New or exploratory UI workflow | snapshots, screenshots, console, errors, storyboard | `qa-tester` using the Codex in-app Browser |
| User-visible quality | already captured images plus design/taste baseline | `visual-qa` |
| Explicit adversarial agent claim | tester evidence plus independent evidence review | `agent-qa-test` |
| Stable repeated UX regression | scripted assertions | Playwright |
| Material completion sufficiency | complete proof bundle | `reviewer` |

The Codex in-app Browser is the browser tool, not the QA owner. In material or
Goal-backed runs, `qa-tester` owns browser operation and artifact capture.
Reuse one browser binding and tabs across sequential checks. Use `@Chrome` only
when the operator's existing authenticated state is required. Playwright is the
graduation path for stable, repeatedly valuable regressions; it is not the
default response to an unsettled selector or workflow.

## Browser System

Choose the browser surface by state and proof needs, never by task identity.

```text
browser_route(operation, auth_state, repeatability, concurrency)
  -> connector_or_cli | codex_browser | chrome | playwright | remotion_renderer
```

| Surface | Use for | State and lifecycle |
| --- | --- | --- |
| Connector, API, or CLI | Semantic reads/writes, feeds, repository operations, media download | First choice; no browser process |
| Codex in-app Browser | Public or dynamic pages, local app QA, screenshots, DOM/console/network inspection | Own browser state; reuse one binding and tabs across sequential work |
| `@Chrome` | UI work requiring the operator's existing Chrome login, tabs, or extensions | Uses the real Chrome profile; verify the active account before acting |
| Playwright | Stable repeatable regressions, CI, clean-state tests, multi-user flows | Reuse one browser with isolated contexts/pages inside a test run; close after the run |
| Remotion Chromium | Video composition rendering | Dedicated renderer process; launch only for rendering and close afterward |

Do not create a fresh browser because a new task started. Open another tab when
the browser identity and controller are unchanged. Use separate state only for
different authenticated identities, concurrent independent controllers, clean
test isolation, or incompatible browser configuration. External coding
delegates do not launch browsers; they return the launch command and URL to the
coordinating Codex QA lane.

### Skill Index

| Route | Skills and owners |
| --- | --- |
| Connector/API/CLI first | [`feed-scout`](../skills/feed-scout/SKILL.md), [`media-ingest`](../skills/media-ingest/SKILL.md), [`ingest-content`](../skills/ingest-content/SKILL.md), [`close-ticket`](../skills/close-ticket/SKILL.md) |
| Codex in-app Browser | [`qa`](../skills/qa/SKILL.md), [`visual-qa`](../skills/visual-qa/SKILL.md), [`testing`](../skills/testing/SKILL.md), [`functional-ui`](../skills/functional-ui/SKILL.md), [`customer-research`](../skills/customer-research/SKILL.md), [`ingest-content`](../skills/ingest-content/SKILL.md), [`frontend-craft`](../skills/frontend-craft/SKILL.md), [`frontend-design`](../skills/frontend-design/SKILL.md), [`react-flow`](../skills/react-flow/SKILL.md), [`prd`](../skills/prd/SKILL.md), [`optimize-harness`](../skills/optimize-harness/SKILL.md), [`convex`](../skills/convex/SKILL.md), [`feed-scout`](../skills/feed-scout/SKILL.md), [`social-content`](../skills/social-content/SKILL.md) |
| `@Chrome` | [`close-ticket`](../skills/close-ticket/SKILL.md); [`feed-scout`](../skills/feed-scout/SKILL.md) only for explicitly authorized logged-in inspection |
| Playwright | [`testing`](../skills/testing/SKILL.md), [`qa`](../skills/qa/SKILL.md), [`visual-qa`](../skills/visual-qa/SKILL.md), [`landing-page`](../skills/landing-page/SKILL.md), [`convex`](../skills/convex/SKILL.md), [`data-viz`](../skills/data-viz/SKILL.md), [`frontend-design`](../skills/frontend-design/SKILL.md), [`react-flow`](../skills/react-flow/SKILL.md) |
| Remotion Chromium | [`remotion`](../skills/remotion/SKILL.md), [`remotion-render`](../skills/remotion-render/SKILL.md) |
| Browser deferred to coordinator | [`delegate-cli`](../skills/delegate-cli/SKILL.md), [`delegate-frontend`](../skills/delegate-frontend/SKILL.md) |

When a skill changes browser ownership, update this index and the skill-local
route together. Do not add another standalone browser runtime without an
accepted ticket proving a capability gap in these surfaces.

## Evidence by Proof Type

- CLI/artifact: exact commands, exit status, logs, generated files, and the
  strongest non-image artifact as `best_evidence`.
- API: bound runtime target, request/response evidence, service logs, and
  relevant traces.
- Browser/UI: runtime target, pre-interaction snapshot, important-state
  screenshots, console logs, page errors, and ordered frames when the journey
  matters. A pass requires image `best_evidence`; an honest non-pass may use
  `best_evidence: null` and name the missing capture in `blockers`.
- Failure: capture the strongest available evidence and name the missing or
  falsifying evidence in `blockers`; do not manufacture a pass.

Screenshots are required for browser/UI proof, not for every QA run.

## Ownership Boundaries

- `qa` owns the effective proof policy, five-gate journey, canonical receipt,
  ticket reconciliation, and learning decision.
- `qa-tester` owns operated runtime/browser capture and writes the receipt back
  to the ticket.
- The Codex in-app Browser supplies page operation, snapshots, screenshots,
  console/network inspection, page errors, and traces.
- `visual-qa` judges captured UI evidence; it does not drive the browser.
- `agent-qa-test` is only for explicit adversarial agent/workflow claims.
- `reviewer` judges whether material evidence is sufficient for completion.

The tester may perform one skeptical failure check during ordinary QA. That
does not turn ordinary QA into the separate `agent-qa-test` protocol.

## Ticket Writeback

- Always store run artifacts under `tickets/TASK-XXXX/artifacts/qa/<run>/`.
- Always link `report.md`, `result.json`, the verdict, and strongest evidence
  from ticket `Links`.
- Append `progress.md` only when it already exists, the run is Goal-backed, or
  blocker/review state needs an append-only entry. Do not create `progress.md`
  for every QA run.
- Never write to retired ticket `State` or `Evidence` sections.

## Learning After Every Run

Make the decision every time; do not edit shared documentation every time.

```text
classify_qa_learning(run)
  -> ticket_only | cookbook_update | instrumentation_ticket
```

- `ticket_only`: one-off workaround, transient failure, or task-specific fact.
  Keep it in the report and ticket links.
- `cookbook_update`: verified reusable route, shortcut, selector, seed/reset,
  debug control, observability method, or stable regression path. Update the
  existing workflow page and cite the verifying receipt.
- `instrumentation_ticket`: missing shortcut, deterministic state control,
  selector, runtime handoff, log, or debug surface requires implementation.
  Create a linked follow-up only when it is genuinely required work.

## Shortcuts and Test Controls

A QA shortcut is any deterministic accelerator: keyboard command, deep link,
debug button, quick-open panel, seed/reset command, test-only toggle, pause,
step, or state mirror. It is not a universal QA mode.

Every documented shortcut states:

- exact trigger or command
- supported environment and safety guard
- prerequisites
- expected visible and internal state
- reset or cleanup
- verification and evidence to capture
- source ticket and last verified receipt

If QA needs repeated wandering, improve testability instead of normalizing the
wandering. See [the cookbook template](cookbook/TEMPLATE.md).

## Browser Loop Limits

- Refresh element references after navigation or state-changing interactions.
- Try the same DOM intent at most twice.
- After three interaction cycles without reaching a new declared state, stop,
  capture the failure bundle, and return `FAIL` or `not_provable` with one
  concrete testability request.

## Regression Graduation

Graduate a browser path to Playwright when the flow and selectors are stable,
the regression is important enough to rerun, or an existing Playwright suite
is already the acceptance surface. Reuse the same cookbook entry, setup,
selectors, and expected observations.
