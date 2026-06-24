---
title: "Farplane Project Memory"
status: active
owner: doc-governance
created_at: 2026-03-26
updated_at: 2026-06-23
tags:
  - farplane
  - memory
  - promoted-decisions
refs:
  - docs/archive/memory/memory-ledger-2026-06-23.md
  - docs/specs/filesystem-lifecycle.md
  - skills/knowledge-tidier/SKILL.md
  - docs/HISTORY.md
  - docs/TROUBLES.md
  - docs/LESSONS.md
---

# Farplane Project Memory

This is the live project-level memory file. It is not a second `AGENTS.md`, not
a style guide, and not a ticket log. It keeps only high-value decisions that
future Farplane work is likely to forget and would pay a real cost for getting
wrong.

Exact historical rows through 2026-06-23 are preserved in
`docs/archive/memory/memory-ledger-2026-06-23.md`.

## Admission Rule

Use `knowledge-tidier` before compacting this file:

```text
keep_live = importance >= 2
         && factuality >= 2
         && remembrance >= 2
         && not superseded
```

- `importance`: costly if future agents forget it.
- `recency`: current or recently changed behavior is easier to keep detailed.
- `factuality`: concrete, source-backed, and falsifiable.
- `remembrance`: not already fully owned by `AGENTS.md`, a spec, a skill, a
  validator, a ticket template, or code.

If a true rule belongs in an always-loaded surface, move it there and keep only
a short memory pointer when the project-specific decision history matters.

## Active Memory

### Source, Identity, And Privacy

Source rows: MEM-0001, MEM-0015, MEM-0021, MEM-0047, MEM-0120, MEM-0126,
MEM-0144.

- Reusable harness behavior belongs in the git-backed Farplane source repo;
  installed Codex-home files are deployment targets, not source of truth.
- Tracked artifacts must not contain live auth, secrets, session history, local
  caches, sqlite state, private handles, raw customer data, or machine-local
  `config.toml`.
- Farplane is the active pre-launch identity. Active docs, templates, runtime
  env vars, helpers, skill IDs, registries, and plugin packages should use
  Farplane names. Old names belong in archives, compatibility shims, or
  unmigrated external services.
- Repo-local `.codex/` directories are not Farplane source or runtime state.
  Working eval installs belong under `.farplane/evals`; reusable eval suites
  and templates belong under `skills/eval/`.
- Stale-check note: old row MEM-0121 names
  `/Users/kenjipcx/coding-harness/Farplane` as canonical. Current work in this
  thread is under `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`;
  do not preserve the old absolute path as live truth without confirmation.

### Tickets And Goal Execution

Source rows: MEM-0031, MEM-0044, MEM-0048, MEM-0049, MEM-0061, MEM-0062,
MEM-0064, MEM-0067, MEM-0081, MEM-0082, MEM-0086, MEM-0122, MEM-0147,
MEM-0148.

- The active ticket is the task-local memory and proof contract. Keep scope,
  decisions, state, blockers, proof, and links in ticket files rather than chat.
- Farplane tickets use the compact ticket-as-program shape:
  `Summary`, `Scope`, `Delta`, `Program`, `Map`, `Done / Proof`, `State`,
  `Links`, and sparse `Notes`.
- `Done / Proof` is the scoreboard for done conditions, checks, review gates,
  mechanical metrics, and evidence obligations. Do not revive parallel
  acceptance/proof sections for new tickets.
- Goal-backed work uses a Goal Packet: `ticket.md` owns the task contract,
  `program.md` owns loop configuration, `progress.md` owns append-only observed
  execution, and `artifacts/` owns bulky proof.
- Farplane starts work from explicit invocation or an active Goal Packet, not
  from the mere existence of a ready ticket, board status, or compute target.
- Native Codex Goal mode is the only formal semantic continuation loop.
  Heartbeats, rollouts, feedback loops, and drift checks are visible patterns
  over Goal Packet state, not separate hidden runtimes.
- Treat a coherent ticket as the default execution unit. Split only for a real
  blocker, safety issue, risky migration, external dependency, or reusable
  boundary.

### Runtime, Hooks, And Continuation

Source rows: MEM-0004, MEM-0008, MEM-0009, MEM-0010, MEM-0016, MEM-0017,
MEM-0018, MEM-0020, MEM-0022, MEM-0023, MEM-0025, MEM-0029, MEM-0034,
MEM-0035, MEM-0036, MEM-0056, MEM-0130, MEM-0151.

- Runtime state belongs under `.farplane/`. Tickets may mirror human-facing
  claims, but raw runtime transport identity stays in runtime state.
- Explicit ticket selectors outrank ambient runtime state. Hook `session_id`
  and singleton current-run pointers are fallback context only.
- Stop-hook completion and continuation checks must compare the assistant
  response against the current user request captured at `UserPromptSubmit` when
  available.
- Stop-hook stdout is machine-only JSON. Diagnostics, bells, notifications, and
  fallbacks go to stderr.
- Stop-hook roles are TOML-backed under `agents/*.toml`; runtime code should
  load exact role instructions from those files.
- Same-ticket continuation requires visible Goal Packet state plus a
  session-scoped loop gate and matching runtime claim. Legacy Ralph, `$impl`,
  and `auto_continue` compatibility state must not become activation truth.
- Completion-gate review must judge both evidence quality and whether the saved
  user turn is satisfied.
- Repeated polling, retries, subagent waits, remote checks, and asset-generation
  waits should use adaptive backoff, but backoff does not authorize hidden
  daemons, queues, or always-on watchers.
- Current Farplane framework automations are explicit loops: `pulse-update` for
  frequent one-action idle/actor decisions, plus Daily Interval and Weekly
  Interval automations that call `interval-update` directly. Codex automation
  cadence is the scheduler; do not restore `farplane/steer.config.toml` or
  `.farplane/state/steer-scheduler.json`.

### Review, QA, And Evidence

Source rows: MEM-0006, MEM-0007, MEM-0033, MEM-0034, MEM-0048, MEM-0052,
MEM-0056, MEM-0064, MEM-0067, MEM-0069, MEM-0070, MEM-0115, MEM-0127,
MEM-0129, MEM-0131, MEM-0149, MEM-0150.

- Material implementation, prompt, skill, doc, evidence, and completion claims
  need independent review when a reviewer lane is available. The main model's
  completion claim is candidate-only on completion-like Stop-hook paths.
- Reviewer routing starts from caller-declared rubric families, TAS gates, hard
  gates, and evidence. The reviewer may add obvious missing hard gates with an
  explanation, but the caller/ticket owns the route.
- Review families use modular binary checklist groups and one TAS verdict per
  selected family. Do not average dimensions or invent numeric thresholds.
- Required evidence-quality and integration-readiness gates cannot pass when
  required evidence or integration checks are missing.
- QA and completion proof are artifact-first. Link screenshots, logs, review
  reports, clips, and proof from ticket evidence; keep bulky proof under
  `tickets/TASK-XXXX/artifacts/`.
- Browser/user-visible QA defaults to `qa-tester` or `agent-browser` for direct
  page operation, screenshots, snapshots, console logs, and page errors.
  Playwright is for explicit regression coverage or stable scripted flows.
- Serious adversarial agent testing combines tester evidence, optional captured
  child-agent logs, evidence critique, fix/rerun reconciliation, and final
  proof-bundle review.

### Skills And Harness Surfaces

Source rows: MEM-0037, MEM-0044, MEM-0073, MEM-0098, MEM-0100, MEM-0101,
MEM-0104, MEM-0107, MEM-0117, MEM-0124, MEM-0127, MEM-0128, MEM-0132,
MEM-0133, MEM-0134, MEM-0145, MEM-0146, MEM-0150.

- A workflow is not shipped until a discoverable `skills/<name>/` package exists
  and canonical inventory/docs point to it.
- Skills own reusable workflow contracts. Actor prompts own identity,
  responsibility, delegation boundaries, tool use, durable task loading,
  artifact writeback, and anti-recursion.
- Do not put subagent spawning, caller routing, or actor identity inside a
  reusable skill unless orchestration is the skill's primary job.
- Local Farplane skill packages keep required every-invocation todo items in a
  marker-delimited `## Todo List` section in `SKILL.md`; skill-local
  `todos.md` sidecars are retired.
- Skill-local runtime QA guardrails live as optional
  `skills/<skill-name>/qa_checklist.md` files. `eval_task.json` pressures
  expected behavior; `qa_checklist.md` applies settled guardrails during real
  work.
- Numeric skill tiers are leverage classes, not lifecycle phases. Tier 0 phases
  are inline capabilities; call phase-like skills such as `plan`, `review`, and
  `eval` only when that phase needs its own artifact, budget, handoff,
  independent judgment, or proof surface.
- Skill registries are generated from skill frontmatter and filesystem facts.
  Do not maintain separate hand-authored sequence or skill-feature registries.
- External skills, repos, blogs, and command families are research inputs, not
  live dependencies. Do not directly edit installed or external skill bodies
  unless the operator explicitly requests that specific external edit.

### Docs And Learning Ledgers

Source rows: MEM-0013, MEM-0018, MEM-0019, MEM-0071, MEM-0108, MEM-0109,
MEM-0135, MEM-0136, MEM-0137.

- Root `AGENTS.md` is the project-local map. The shipped global contract lives
  in `templates/global/AGENTS.md`.
- `docs/HISTORY.md` records meaningful project events: shipped milestones,
  migrations, cleanup events, and project-shaping behavior, workflow, API,
  architecture, or governance shifts. Routine code deltas belong in git.
- `docs/MEMORY.md` is the promoted project-level decision log: current,
  factual, important, and worth remembering outside the owner surface.
- `docs/TROUBLES.md` is the raw pain log. `docs/LESSONS.md` is the distilled
  prevention log. Keep them separate.
- Active `docs/specs/` files should map to one current feature, contract, or
  doctrine surface. Completed migration plans and superseded milestone notes
  belong in archives or owning skill surfaces.
- Durable Markdown artifacts should use compact YAML front matter for routing
  metadata while keeping the body focused on the human contract, explanation,
  evidence, or narrative.

### External Tools And Notion

Source rows: MEM-0110, MEM-0111, MEM-0112, MEM-0120, MEM-0123.

- User-specific tool handles, database IDs, private URLs, device names, and
  personal workspace conventions belong in local private context, not tracked
  shared artifacts.
- Notion context wrappers are MCP-only for task, project, goal, and pinned-task
  context. Do not call Notion's public API directly from ad hoc scripts unless
  a new ticket explicitly changes that boundary.
- Prefer a local token-backed MCP server over remote OAuth MCP for unattended
  automation when that local server is available.
- Notion planning automation must read recent pinned task rows through
  row-capable MCP surfaces before task ranking or autonomous selection.
- Feed-scout live Notion task writeback must resolve required Project and Areas
  relations before writing, verify by readback, and fall back to local output
  when routing is missing.

### Retired Or Superseded Paths

Source rows: MEM-0002, MEM-0003, MEM-0005, MEM-0021, MEM-0028, MEM-0032,
MEM-0074, MEM-0105, MEM-0109, MEM-0114.

- Historical Ralph tmux lanes and public Ralph execution surfaces are retired.
  Use Goal-backed `goal-advisor` execution and Goal heartbeat patterns instead.
- Legacy `$impl`, `$ralph`, `$work`, root `todos.md` board-drain, public
  `batch-work`, and old Ralph runtime meanings are superseded by Goal Advisor
  standards unless a compatibility parser explicitly recognizes old text.
- Retired OMX-era instructions belong only in archives or research material.
  Active Farplane skills and docs use current tickets, docs, Goal Packets, and
  `.farplane/` runtime state.
- Skill-local `todos.md` sidecars are no longer active sources. Move useful
  checklist content into `SKILL.md` and delete the sidecar.

## Recent Promoted Log

Keep only recent full rows that pass the admission rule. During a drain, move
older passing rows into `## Active Memory` and keep exact wording in the
archive.

2026-06-12 16:30 +0800 | farplane,goals,loops,tickets,drift,feedback | Native Codex Goal mode is the only formal semantic continuation loop. Material Goal work should create or attach to a ticket-backed Goal Packet: `ticket.md` owns the task contract, `program.md` owns loop configuration, `progress.md` owns append-only observed execution, and `goal-advisor` chooses active Goal, heartbeat, rollout, feedback, skill-improvement, business-loop, or direct-work shape before compiling the native `/goal` prompt. Heartbeats are delayed triggers over the same Goal Packet, rollout is a staged parent/child ticket pattern, `human_feedback` is the abstract feedback provider signal, and `optimize-with-human` is the Telegram-first optimization preset rather than a separate loop runtime. Drift review is read-only and compares ticket, program, progress, and current continuation claim before recommending align, recover, block, or complete-candidate.

2026-06-12 11:16 +0800 | farplane,tickets,programs,proof,planning | Farplane ticket bodies should use the compact ticket-as-program shape: `Summary`, `Scope`, `Delta`, `Program`, `Map`, `Done / Proof`, `State`, `Links`, and sparse `Notes`. `Delta` owns before/after and first-principles basis; `Program` owns variables and operations in `operation(input) -> output` form; `Map` owns touched files, inspected files, callable seams, type sketch, typed flow, and optional diagram; `Done / Proof` collapses old `Acceptance Criteria`, `Verification`, and `Proof Contract` sections into done conditions, checks, review/TAS gates, and evidence obligations. Use `program.md` for long-running Goal/heartbeat/rollout/skill-improvement policy, `progress.md` for append-only logs, and `artifacts/` for bulky proof and review output.

2026-06-13 00:00 +0800 | farplane,skills,qa,evals,checklists | Skill-local runtime QA guardrails should live as optional first-class `skills/<skill-name>/qa_checklist.md` files at the skill package root, not as ordinary `references/` prose. `eval_task.json` discovers and pressures expected behavior; `qa_checklist.md` applies settled reusable guardrails during real work. After editing a skill eval, skill-maintenance should decide whether changed reference points promote into `qa_checklist.md`, `SKILL.md`, a reference, or a validator, and record skipped rare or benchmark-only points in the audit.

2026-06-24 00:00 +0800 | farplane,automations,pulse,intervals | Farplane projects use explicit Codex automation loops for autonomous operation: `pulse-update` for frequent one-action idle/actor decisions, Daily Interval for last-24h reporting and next-24h planning, and Weekly Interval for last-week drift review and next-week planning. Active interval planning lives in `interval-update`; Codex automation records own cadence. Do not restore the old `steer-update`, `farplane/steer.config.toml`, `.farplane/state/steer-scheduler.json`, or cadence compatibility alias packages.

2026-06-23 00:00 +0800 | farplane,knowledge,tidying | Live project memory and other knowledge artifacts should be ranked by importance, recency, factuality, and remembrance value. Keep only important, factual, current-enough knowledge that the target file is the best owner for; route generic policy to `AGENTS.md`, specs, skills, validators, or ticket templates, and preserve exact historical rows in archives before compacting semi-append-only sources.
