# PRD: Codexter Aikage Telemetry Sync

## Problem / Context

Codexter now has generated skill registries, tier checks, graph views, runtime
hooks, and a skill-opportunity learning loop, but the operator cannot easily
see whether those surfaces are actually being used. The current hook telemetry
path can POST a small lifecycle payload when `CODEXTER_TELEMETRY_API_URL` is
set, and Aikage already stores agent activity pings in Convex, but there is no
local-first Codexter event ledger, no skill usage diagnostics, and no Aikage
view for hook health, skill routing, or self-improvement outcomes.

This creates a trust gap: unused skills cannot be pruned confidently, learning
hooks may silently skip, and cloud telemetry cannot be audited against local
truth.

## Audience

- Primary: the Codexter operator managing skills, hooks, tickets, and Aikage.
- Secondary: future agents maintaining Codexter runtime hooks and skill
  registry health.
- Tertiary: Aikage dashboard users who want project/machine/session level
  agent activity without reading local JSONL files.

## JTBD

When Codexter runs turns, hooks, skills, tickets, validators, and learning
loops, I want a local-first event ledger that can optionally sync to Aikage, so
I can see what actually happened, debug missing feedback, and decide which
skills or hooks deserve maintenance.

## SLC Slice (Next Release)

Ship a local-first Codexter telemetry event ledger plus optional Aikage Convex
sync and a compact Aikage dashboard panel. The first slice tracks lifecycle,
skill request/routing, hook result, ticket transition, validator, and
self-improvement events. It must not require Aikage to be available for
Codexter to work.

## Goals

- Codexter writes deterministic local JSONL events under `.harness/events/`.
- Existing hook telemetry calls reuse the local event writer before attempting
  network sync.
- Aikage accepts a richer `codexter_event` ingest shape through Convex HTTP.
- Aikage dashboard shows Codexter event health using the existing visual
  system: square panels, JetBrains Mono headings, bento layout, dark/light
  theme variables, compact diagnostics.
- The operator can run one local status command to see hook health,
  skill-request counts, learning-review skips/launches, and cloud-sync status.

## Metric Candidates

- Primary candidate: event ledger parse pass.
- Direction: pass/fail.
- Verification idea: parse every `.harness/events/*.jsonl` event emitted by
  tests and validate required fields.
- Guard idea: existing hook tests plus new runtime telemetry tests pass.

Secondary candidates:

- Aikage ingest smoke pass: POST fixture event to local/Convex endpoint and
  query it back.
- Skill visibility pass: a fixture `$impl-plan` prompt produces a
  `skill_requested` or `control_surface_detected` event.
- Learning-hook visibility pass: a forced due/not-due fixture writes
  `learning_review_skipped` or `learning_review_launched`.

## Non-Goals

- Do not build a background Codexter daemon.
- Do not make Aikage required for local Codexter operation.
- Do not sync raw transcripts, secrets, full prompts, raw assistant outputs, or
  repo file contents to Aikage.
- Do not infer "skill actually loaded" when only prompt/request routing is
  observable. Track `skill_requested`, `skill_routed`, and
  `control_surface_detected` honestly.
- Do not implement automatic skill deprecation in this slice.
- Do not mutate Notion, Linear, GitHub, or external boards.
- Do not add hosted queues, retries, or remote execution control.

## User Stories

### US-001: Local Event Ledger

**Description:** As the operator, I want Codexter hooks to write local event
JSONL before any cloud sync, so local proof exists even when Aikage is offline.

**Acceptance Criteria:**

- [ ] `bin/runtime_telemetry.py` exposes a local event writer with schema
      validation.
- [ ] `capture_user_turn.py` and `stop_hook.py` write local events before
      attempting network telemetry.
- [ ] Local telemetry writes do not include raw transcripts or full prompts by
      default.
- [ ] Tests cover valid events, redaction, and network-disabled behavior.

### US-002: Skill And Hook Usage Diagnostics

**Description:** As the operator, I want a local command that summarizes skill
requests, hook runs, validator runs, self-improvement windows, and Aikage sync
status, so I can see whether the harness is alive.

**Acceptance Criteria:**

- [ ] A CLI such as `bin/codexter_telemetry_status.py` reads local event JSONL.
- [ ] The CLI prints counts by event type, skill, hook, ticket, project, and
      sync result.
- [ ] The CLI reports self-improvement window counts and application report
      counts.
- [ ] The CLI flags zero learning application runs when windows exist.

### US-003: Aikage Codexter Event Ingest

**Description:** As the operator, I want Aikage to accept Codexter event
envelopes through its existing private ingest key model, so local agents can
sync richer telemetry without a new auth system.

**Acceptance Criteria:**

- [ ] Aikage Convex schema stores Codexter events separately from existing
      activity pings.
- [ ] HTTP ingest accepts a bounded event payload with the existing key lookup.
- [ ] Sensitive fields are bounded, truncated, or omitted.
- [ ] Queries can return dashboard-safe aggregate event counts without raw
      prompt contents.

### US-004: Aikage Dashboard Integration

**Description:** As the operator, I want Codexter telemetry to appear in the
Aikage dashboard using the existing bento visual language, so it feels like
part of the same product rather than a bolted-on log table.

**Acceptance Criteria:**

- [ ] Dashboard adds a Codexter telemetry panel using existing
      `BentoGrid`, `BentoItem`, `Panel`, `MetricTile`, and theme variables.
- [ ] Panel shows event volume, hook health, top skills/control surfaces,
      learning-loop status, and recent failed syncs or skipped reviews.
- [ ] Raw event detail is collapsed or paginated.
- [ ] Existing agent-hours dashboard remains primary; telemetry is secondary
      diagnostics.

### US-005: Prune Candidate Report

**Description:** As the operator, I want a report that compares skill registry
topology with actual local usage, so I can decide which skills are dead,
duplicative, or worth turning into methods.

**Acceptance Criteria:**

- [ ] Report reads `docs/skills/registry.jsonl` plus local event JSONL.
- [ ] Report distinguishes static references from actual observed usage.
- [ ] Report produces candidate categories: unobserved, frequently requested,
      routed but failing, external locked, merge candidate, keep.
- [ ] Report does not delete or deprecate skills automatically.

## Functional Requirements

- FR-1: Define a versioned `CodexterEvent` envelope with required fields:
  `schema_version`, `event_id`, `event_type`, `timestamp`, `source`,
  `project_root`, `session_id`, and optional ticket/skill/hook/sync fields.
- FR-2: Store local events under `.harness/events/YYYY-MM-DD.jsonl`.
- FR-3: Emit local events from user-turn capture, stop-hook completion,
  self-improvement review decisions, telemetry sync attempts, and validators
  where practical.
- FR-4: Keep cloud sync best-effort and non-blocking.
- FR-5: Reuse existing `CODEXTER_TELEMETRY_API_URL`,
  `CODEXTER_TELEMETRY_API_TOKEN`, and timeout env vars unless a new endpoint
  path is required.
- FR-6: Add Aikage Convex table and HTTP route for Codexter event ingest.
- FR-7: Add Aikage dashboard-safe aggregate query fields.
- FR-8: Add dashboard UI consistent with Aikage current design system.
- FR-9: Add local status/prune-report commands.

## Constraints

- Security/privacy: do not sync raw transcript paths, full prompts, assistant
  responses, secrets, env vars, local config, or repo file contents.
- Performance: hook writes must be fast and must not block turn completion on
  network calls.
- Platform: Codexter side must remain Python standard-library first. Aikage
  side uses Convex, React, Vite, TypeScript, Tailwind, and existing shadcn
  primitives.
- Budget/time: first implementation should be a small set of proofable tickets,
  not a hosted orchestration platform.

## Autonomy Readiness

- Human inputs/assets needed:
  - Aikage branch name and whether implementation should happen in that branch.
  - Aikage ingest key for live smoke, if live cloud sync is tested.
- Credentials / external services:
  - Convex dev/prod deployment configured for Aikage.
  - Optional `CODEXTER_TELEMETRY_API_URL` and token.
- Compute or runtime needs:
  - Local Python tests in Codexter.
  - Aikage `pnpm lint`, `pnpm exec tsc -b`, `pnpm build`, and Convex tests or
    local dev smoke where available.
- Tooling or testability gaps:
  - Current telemetry helper has no local event log.
  - Current Aikage table models only coarse activity pings and posts.
- Hard-to-QA surfaces:
  - Hook events are easy to miss unless fixture runners simulate payloads.
  - Cloud sync failures should be visible without failing local hooks.
- Human gates:
  - Plan approval: required before implementation.
  - QA approval: required for Aikage UI screenshots.
  - Deploy/publish: explicit user approval only.
  - Spend/billing: none expected.
  - Destructive/migration actions: no destructive migrations; Convex schema
    additions only.
- Agent decision boundaries:
  - The agent may add local files, tests, schema additions, and dashboard UI.
  - The agent must not deploy Aikage or mutate production Convex without
    explicit approval.

## Risks / Unknowns

- Aikage work is on another branch; implementation must verify the active
  branch before editing.
- Codex hook payloads may not expose reliable skill-load events. The first
  version must track observable requested/routed events rather than claiming
  true runtime skill usage.
- Existing unrelated dirty Codexter files are present; implementation must
  stage only this feature's files.
- Convex schema changes may need generated types refreshed in Aikage.

## Backpressure / Evidence to Ship

- Tests:
  - Codexter Python telemetry unit tests.
  - Codexter hook fixture tests.
  - Aikage TypeScript/lint/build.
- QA:
  - Local CLI summary output.
  - Aikage dashboard screenshot with Codexter telemetry panel.
- Perf checks:
  - Hook telemetry emits local event and returns without network configured.
  - Network timeout remains bounded.
