---
title: QA and Browser System Guide
status: active
owner: qa
updated_at: 2026-10-12
refs:
  - skills/qa/SKILL.md
  - agents/qa-tester.toml
  - skills/qa/references/runbooks.md
---

# QA and Browser System Guide

Farplane QA turns one ticket claim into inspectable evidence, independent
judgment when required, a canonical receipt, and selective reusable learning.
The ticket owns what must be proved; this guide explains how to run that proof.

```text
qa_journey(ticket, runtime_target?, proof_policy_override?)
  -> choose -> capture -> reconcile -> judge -> receipt -> learn
```

Per-run evidence belongs under `.farplane/qa/<issue>/<run>/`, and the verdict
with its strongest evidence is posted on the GitHub issue. Reusable
entry paths, shortcuts, selectors, seeds, and observability belong in the
project's `AGENTS.md` Agent QA section, or `docs/qa/<flow>.md` for a long flow
(see [runbooks.md](runbooks.md)).


## Rules for QA runbooks

- use project QA runbooks for reusable guidance, not per-run evidence
- keep screenshots, logs, traces, and one-off reports under
  `.farplane/qa/<issue>/<run>/`; attach the strongest to the issue comment
- treat `skills/qa/SKILL.md` as the execution and receipt contract; this guide
  owns readable guidance and reusable runbooks
- prefer the Codex in-app Browser for browser proof: page operation, snapshots,
  screenshots, console/network inspection, and page-error capture
- use Playwright only when stable UX regression coverage is explicitly needed,
  when an existing suite is the acceptance surface, or when a settled flow is
  ready to graduate into scripted coverage
- when a workflow is hard to automate, document the missing shortcut,
  deterministic setup, or instrumentation helper here so later tickets can land
  the fix intentionally
- after each run classify learning as `ticket_only`, `cookbook_update`, or
  `instrumentation_ticket`; do not force a cookbook edit for one-off facts

## Start Here

1. **Choose proof.** Read the issue's `Done / Proof`, `QA Strategy`, optional `Agent
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
   completion judgment; visual and adversarial modes run as their own lane.
7. **Write the receipt.** Produce `report.md` and validated `result.json`, then
   post the verdict and strongest evidence with `gh issue comment`.
8. **Learn selectively.** Decide whether the run stays ticket-local, updates a
   cookbook page, or needs an instrumentation follow-up.

## Choose the Proof Route

| Work under test | Normal proof | Owner |
| --- | --- | --- |
| CLI, script, validator, or generated artifact | command output, logs, files, focused tests | `qa` / implementing lane |
| API or integration | bound runtime, responses, logs, traces | `qa-tester` when operated capture helps |
| New or exploratory UI workflow | snapshots, screenshots, console, errors, storyboard | `qa-tester` using the Codex in-app Browser |
| User-visible quality | already captured images plus design/taste baseline | `qa` visual mode ([visual.md](visual.md)) |
| Explicit adversarial agent claim | tester evidence plus independent evidence review | `qa` adversarial mode ([adversarial.md](adversarial.md)) |
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
  -> connector_or_cli | codex_browser | chrome | playwright | hyperframes_renderer
```

| Surface | Use for | State and lifecycle |
| --- | --- | --- |
| Connector, API, or CLI | Semantic reads/writes, feeds, repository operations, media download | First choice; no browser process |
| Codex in-app Browser | Public or dynamic pages, local app QA, screenshots, DOM/console/network inspection | Own browser state; reuse one binding and tabs across sequential work |
| `@Chrome` | UI work requiring the operator's existing Chrome login, tabs, or extensions | Uses the real Chrome profile; verify the active account before acting |
| Playwright | Stable repeatable regressions, CI, clean-state tests, multi-user flows | Reuse one browser with isolated contexts/pages inside a test run; close after the run |
| HyperFrames renderer | Video composition rendering | Dedicated renderer process; launch only for rendering and close afterward |

Do not create a fresh browser because a new task started. Open another tab when
the browser identity and controller are unchanged. Use separate state only for
different authenticated identities, concurrent independent controllers, clean
test isolation, or incompatible browser configuration. External coding
delegates do not launch browsers; they return the launch command and URL to the
coordinating Codex QA lane.

### Skill Index

| Route | Skills and owners |
| --- | --- |
| Connector/API/CLI first | [`feed-scout`](../../feed-scout/SKILL.md), [`intelligest`](../../intelligest/SKILL.md) |
| Codex in-app Browser | [`qa`](../../qa/SKILL.md), [`eval`](../../eval/SKILL.md), [`impl-plan`](../../impl-plan/SKILL.md), [`visual-design`](../../visual-design/SKILL.md), [`landing-page`](../../landing-page/SKILL.md), [`prospect`](../../prospect/SKILL.md), [`prd`](../../prd/SKILL.md), [`optimize-harness`](../../optimize-harness/SKILL.md), [`feed-scout`](../../feed-scout/SKILL.md), [`social-content`](../../social-content/SKILL.md) |
| `@Chrome` | [`feed-scout`](../../feed-scout/SKILL.md) only for explicitly authorized logged-in inspection |
| Playwright | [`qa`](../../qa/SKILL.md), [`landing-page`](../../landing-page/SKILL.md), [`impl-plan`](../../impl-plan/SKILL.md) |
| HyperFrames renderer | external `hyperframes` skill (`/hyperframes`), fed by [`storyboard`](../../storyboard/SKILL.md) |

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
- `qa-tester` owns operated runtime/browser capture and posts the receipt back
  to the issue.
- The Codex in-app Browser supplies page operation, snapshots, screenshots,
  console/network inspection, page errors, and traces.
- Visual mode judges captured UI evidence; it does not drive the browser.
- Adversarial mode is only for explicit adversarial agent/workflow claims; its
  tester lane cannot self-approve.
- The closeout demo ([closeout-demo.md](closeout-demo.md)) runs only after a pass.
- `reviewer` judges whether material evidence is sufficient for completion.

The tester may perform one skeptical failure check during ordinary QA. That
does not turn ordinary QA into the separate adversarial protocol.

## Issue Writeback

- Store run artifacts under `.farplane/qa/<issue>/<run>/`; never create
  `tickets/` folders for an issue-backed project.
- Post one `gh issue comment <n> --body-file <file>` per executed run with the
  verdict, receipt summary, strongest evidence attached or linked (a local path
  alone is not shared), blockers, and residual risk.
- For Goal-backed runs, the comment is the append-only progress entry; update
  the issue body's `## Current Goal state` only when the checkpoint changed.
- Issues carry engineering facts only; keep client names and private data out.

## Receipt Invariants

`scripts/validate_qa_result.py` enforces these on `result.json`:

- `ticket_id` is `owner/repo#N`, `#N`, or a legacy `TASK-NNNN`; `phase` is
  `qa`; `proof_type` is `cli | api | browser | ui | artifact | agent`; all five
  gates (`contract`, `mechanism`, `journey`, `adversarial`, `receipt`) exist
  with `pass | fail | blocked`.
- `artifacts` is non-empty; a concrete `best_evidence` also appears there.
- A pass has every gate passing, concrete best evidence, and no blockers. A
  non-pass has at least one blocker and may use `best_evidence: null` when the
  required artifact does not exist.
- Browser/UI passes require a bound runtime, image best evidence, and a
  completed `design.md` comparison; API proof requires a bound runtime.
- `ticket_only` uses `learning.ref: null`; `cookbook_update` and
  `instrumentation_ticket` require a non-empty ref.
- A passing policy naming `visual`, `adversarial`, or `reviewer` requires a
  `judgment_receipts` path containing `visual`, `adversarial`, or `review`.

## Learning After Every Run

Make the decision every time; do not edit shared documentation every time.

```text
classify_qa_learning(run)
  -> ticket_only | cookbook_update | instrumentation_ticket
```

- `ticket_only`: one-off workaround, transient failure, or task-specific fact.
  Keep it in the report and the issue comment.
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
wandering. See [the runbook template](runbook-template.md).

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
