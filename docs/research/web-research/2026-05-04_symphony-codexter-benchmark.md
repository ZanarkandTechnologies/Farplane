# Research: Symphony vs Codexter Board-Orchestration Benchmark

Date: 2026-05-04

## Scope

This memo benchmarks the provided Symphony Service Specification against
Codexter's current ticket-first harness. It is not an implementation plan and
does not assume Codexter should clone Symphony. The goal is to identify:

1. what Symphony does better,
2. what Codexter already does better,
3. what should be adapted into Codexter's next runtime direction, and
4. how Symphony's prompt/workflow contract differs from Codexter's prompt
   surfaces.

## Sources

- User-provided Symphony Service Specification, draft v1, pasted in chat.
- Codexter current local surfaces:
  - [README.md](/Users/kenjipcx/coding-harness/Codexter/README.md)
  - [ARCHITECTURE.md](/Users/kenjipcx/coding-harness/Codexter/ARCHITECTURE.md)
  - [tickets/README.md](/Users/kenjipcx/coding-harness/Codexter/tickets/README.md)
  - [tickets/templates/ticket.md](/Users/kenjipcx/coding-harness/Codexter/tickets/templates/ticket.md)
  - [docs/specs/spec-first-execution-loop.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/spec-first-execution-loop.md)
  - [docs/specs/runtime-surface.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/runtime-surface.md)
  - [docs/specs/orchestrator-subagent-loop.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/orchestrator-subagent-loop.md)
  - [docs/specs/review-gates.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/review-gates.md)
  - [docs/specs/harness-techniques.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/harness-techniques.md)
  - [skills/ralph/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/ralph/SKILL.md)
  - [skills/impl/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/impl/SKILL.md)
  - [skills/impl-plan/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/impl-plan/SKILL.md)
  - [skills/ralph/scripts/select_next_ticket.py](/Users/kenjipcx/coding-harness/Codexter/skills/ralph/scripts/select_next_ticket.py)
  - [templates/global/AGENTS.md](/Users/kenjipcx/coding-harness/Codexter/templates/global/AGENTS.md)
- Prior local comparison:
  - [docs/research/web-research/2026-04-02_codexter-vs-omx-gap-analysis.md](/Users/kenjipcx/coding-harness/Codexter/docs/research/web-research/2026-04-02_codexter-vs-omx-gap-analysis.md)
- Official Codex docs checked on 2026-05-04:
  - [Codex App Server](https://developers.openai.com/codex/app-server)
  - [Use Codex in Linear](https://developers.openai.com/codex/integrations/linear)
  - [Codex automations](https://developers.openai.com/codex/app/automations)
  - [Codex worktrees](https://developers.openai.com/codex/app/worktrees)
  - [Codex local environments](https://developers.openai.com/codex/app/local-environments)
  - [Codex SDK](https://developers.openai.com/codex/sdk)
  - [Codex skills](https://developers.openai.com/codex/skills)
  - [Codex subagents](https://developers.openai.com/codex/subagents)

## Short Answer

Codexter should not copy Symphony as a daemon right now. Codexter should adapt
Symphony's orchestration primitives behind a Codexter-native board runtime
profile and adapter boundary.

Best path:

- keep local Markdown tickets as the first-class durable work object,
- keep `impl-plan`, `$impl`, QA, review, Stop-hook, and artifact gates as the
  quality system,
- add a normalized `WorkItemAdapter` layer so filesystem tickets, Linear,
  GitHub, Notion, or other boards can map into the same execution shape,
- add a small board runtime profile that declares dispatch policy, active and
  terminal states, workspace/worktree strategy, prompt template, retry rules,
  and observability settings,
- delay a full daemon until serial `$ralph`, ticket-runtime, and selective
  branch/worktree runtime prove the shape locally.

The product bet is:

> Symphony is ahead on scheduler mechanics. Codexter is ahead on work-quality
> mechanics. Codexter should steal the scheduler spine, not replace its ticket
> and review system.

## Capability + Parity Lens

Capability:

- autonomous coding-agent work execution from a visible board.

Parity lens:

- issue intake,
- dispatch eligibility,
- runtime isolation,
- agent session control,
- retry/reconciliation,
- observability,
- prompt/workflow authoring,
- tracker portability,
- proof and completion trust.

Primary operator:

- a maintainer who wants to hand a prepared board to agents without losing
  control over quality, workspace isolation, or human review.

## Local Baseline

Codexter today is strongest as a visible-artifact harness:

- tickets are the durable task memory and board card;
- `impl-plan` owns detailed per-ticket planning;
- `$impl` owns one selected ticket's build/review/QA loop;
- `$ralph` drains prepared filesystem tickets serially;
- `qa-tester`, `visual-qa`, `review`, and Stop hook split evidence gathering,
  judgment, and completion routing;
- `Autonomy Readiness`, `Agent Contract`, and `Evidence Checklist` make
  unattended and hard-to-QA work explicit;
- `docs/HISTORY.md`, `docs/MEMORY.md`, and `docs/TROUBLES.md` preserve durable
  lessons;
- `pr-runtime` and `ticket-runtime` create the beginning of a selective local
  runtime and QA target story.

Codexter is intentionally not yet:

- a long-running daemon,
- a parallel N-agent dispatcher,
- a Linear-first service,
- a generic distributed job scheduler,
- a complete app-server protocol client,
- a hosted runtime dashboard.

That local restraint is mostly good. It has avoided building a hidden
orchestration plane before the work-quality loop is trustworthy.

## Comparable Implementations

### 1. Symphony specification

Symphony is a long-running scheduler/runner that polls Linear, claims issues,
creates per-issue workspaces, launches Codex app-server sessions, retries with
backoff, reconciles active issue state, exposes structured logs and optional
HTTP state, and keeps repo-owned runtime policy in `WORKFLOW.md`.

Why it matters:

- it is a clean service contract for the exact future boundary Codexter has
  been deferring: board-driven agent execution.

Limit:

- it mostly treats quality, proof, planning, and handoff as workflow prompt
  responsibilities rather than first-class review gates.

### 2. Official Codex app primitives

Official Codex docs already provide several primitives that reduce the need for
Codexter to own every runtime detail:

- Codex Linear integration can delegate issues to Codex and post results back
  into Linear.
- Codex automations can run background recurring tasks, optionally on
  worktrees, and can combine with skills.
- Codex worktrees isolate parallel tasks and support handoff back to local.
- Codex local environments provide setup scripts and common actions for
  worktrees.
- Codex SDK and app-server can programmatically start/resume threads and run
  prompts.
- Codex skills and subagents already provide progressive disclosure and bounded
  specialist execution.

Why it matters:

- Codexter should own the board/work-quality policy, not rebuild all hosting,
  worktree, Linear, and app-server ergonomics from scratch unless the platform
  primitives are insufficient.

### 3. Codexter current repo

Codexter already contains a strong local board and proof model:

- canonical ticket shape;
- serial selector;
- clear ready/approval/blocker/claim rules;
- role split between builder, QA, reviewer, and Stop hook;
- review rubrics and evidence gates;
- selective runtime and isolated checkout early work.

Why it matters:

- Symphony has a scheduler. Codexter has a stronger answer to "what counts as
  done and who is allowed to say so?"

### 4. Prior OMX comparison

The 2026-04-02 Codexter-vs-OMX gap memo reached a similar structural
conclusion:

- Codexter has better workflow discipline;
- OMX had more runtime machinery;
- the gap was runtime/persistence/control-plane support around Codexter's
  stronger ticket/proof system.

Symphony is another confirmation of that same gap, but with a cleaner
language-agnostic scheduler spec than the older OMX runtime.

## Parity Table

| Surface | Symphony | Codexter today | Verdict |
| --- | --- | --- | --- |
| Board source | Linear issue tracker, active/terminal states, blockers, priority sorting | Filesystem tickets with frontmatter, ready/approval/blockers/depends_on, serial selector | Symphony ahead on external tracker adapter; Codexter ahead on human-readable work card depth |
| Scheduler | Long-running poll loop, claimed/running/retry state, reconciliation, stall timeout | `$ralph` read-only serial selector plus phase handoff; no daemon, no retries | Symphony ahead |
| Workspace isolation | Deterministic per-issue workspace under sanitized root; optional hooks | `pr-runtime` and worktree/branch runtime direction; no per-ticket workspace policy in `$ralph` yet | Symphony ahead in spec clarity; Codexter direction is compatible |
| Compute placement | Local process by default, optional SSH worker extension | Local shared checkout today, selective branch/worktree runtime planned, cloud boundary explicit but deferred | Tie in vision; Symphony ahead on worker-extension shape |
| Prompt workflow | One `WORKFLOW.md` with YAML config and strict prompt template over `issue` and `attempt` | Root AGENTS, skills, subagent prompts, ticket bodies, review rubrics, QA docs | Codexter ahead on quality prompts; Symphony ahead on one self-contained runtime prompt |
| Strict templating | Unknown variables/filters fail rendering | No equivalent board-run prompt renderer; instructions are procedural Markdown | Symphony ahead |
| Agent protocol | App-server subprocess contract, session/turn telemetry, max turns, continuation turns | Native app session plus local tools/subagents; no repo-owned app-server client | Symphony ahead if Codexter wants daemon mode |
| Retry/backoff | Exponential retry queue and 1s continuation retry | Stop-hook same-ticket re-entry and `$loop`, but no generic retry queue | Symphony ahead for unattended scheduler |
| Reconciliation | Running issue state refresh stops terminal/non-active runs | Ticket frontmatter and Stop hook route phases; no active external state poll | Symphony ahead for tracker-driven runs |
| Observability | Structured logs, runtime snapshot, optional HTTP dashboard | Ticket evidence, artifacts, stop-hook logs, partial telemetry ticket | Codexter ahead on proof artifacts; Symphony ahead on live ops dashboard |
| QA and review | Mostly delegated to workflow prompt and agent tooling | Explicit QA lane, visual QA, reviewer lane, review rubrics, completion receipts | Codexter far ahead |
| Safety | Strong workspace path invariants, secret handling, documented trust posture | Strong git/destructive-command policy, approval rules, artifact-first completion, but no per-workspace root invariant for board runs | Split: Symphony ahead on workspace safety; Codexter ahead on completion safety |
| Adapter portability | Linear-compatible adapter now, TODO for more | Filesystem tickets now; external adapters explicitly future | Symphony ahead on Linear; Codexter should generalize earlier |
| Conformance tests | Detailed matrix for loader, workspace, tracker, orchestrator, app-server, observability | Validators for ticket metadata, doc parity, harness invariants; tests for runtime hooks/selectors | Symphony ahead on service conformance breadth |

## Where Codexter Is Better

### 1. Work quality is first-class

Symphony says successful work may end at a workflow-defined handoff state, but
the spec does not define a rich review/proof gate. Codexter does:

- QA gathers evidence.
- Reviewer scores against anchored rubrics.
- Stop hook checks phase, evidence, freshness, traceability, and completion
  receipt mechanics.
- Tickets store durable evidence.

This is not cosmetic. It is the difference between "the agent ran" and "the
result is defensible."

### 2. Tickets are richer than normalized issues

Symphony's normalized issue model is excellent for scheduling. It is too thin
as the primary work object. Codexter tickets carry:

- plan,
- acceptance criteria,
- verification,
- evidence,
- blockers,
- autonomy readiness,
- agent/testability contracts,
- typed flow examples,
- signature deltas.

Codexter should preserve that richness even when the source board is Linear.
The adapter should project Linear into a Codexter work package, not demote
Codexter tickets into Linear issue summaries.

### 3. Prompting is more modular and role-aware

Symphony has one workflow prompt body. Codexter has:

- root policy,
- reusable skills,
- role-specific subagents,
- ticket-local proof surfaces,
- review rubrics,
- QA cookbook surfaces.

This is heavier, but it is also more aligned with how complex engineering work
actually fails. Different stages need different prompts.

### 4. Human gates and autonomy readiness are clearer

Symphony documents trust posture, but Codexter asks each unattended ticket to
name missing inputs, credentials, compute, QA risk, and human gates. That is a
stronger operator-trust primitive.

### 5. The system resists hidden orchestration

Codexter's instinct to keep tickets/docs visible is good. Symphony's scheduler
is clean, but a daemon can become a black box quickly unless it inherits
Codexter's artifact-first proof model.

## Where Symphony Is Better

### 1. It has a real scheduler state machine

Symphony names:

- unclaimed,
- claimed,
- running,
- retry queued,
- released,
- worker attempt phases,
- stall timeout,
- retry timer behavior,
- continuation retries.

Codexter has selector rules and Stop-hook continuation, but no unified queue
runtime state machine.

### 2. It separates tracker adapters from orchestration

Symphony's tracker reader contract is clean:

- fetch candidate issues,
- fetch terminal issues,
- refresh active issue states,
- normalize to a stable model.

Codexter needs this if it wants filesystem tickets, Linear, GitHub, Notion, or
other boards to be interchangeable.

### 3. It has deterministic workspace safety rules

Symphony's workspace invariants are simple and important:

- agent cwd must equal per-issue workspace path,
- workspace path must stay under workspace root,
- workspace key must be sanitized.

Codexter's git/worktree safety instincts are good, but the future board runner
should copy this level of mechanical workspace invariant.

### 4. Its config/reload story is cleaner

`WORKFLOW.md` front matter gives Symphony one typed runtime policy source:

- tracker,
- polling,
- workspace,
- hooks,
- agent,
- codex.

Codexter has many richer surfaces, but no single board-run policy profile.

### 5. It treats observability as an operator surface

Symphony's runtime snapshot shape is exactly the kind of "what is running,
retrying, stuck, and burning tokens?" surface Codexter lacks today.

### 6. It has a conformance mindset

The Symphony test matrix is unusually useful. Codexter has validators, but a
future board runtime needs Symphony-style conformance tests before it becomes
trusted.

## Prompt and Workflow Comparison

### Symphony prompt model

Symphony uses `WORKFLOW.md` as a combined policy and prompt file:

- YAML front matter defines runtime settings.
- Markdown body is the per-issue prompt template.
- Template variables are strict: `issue` and `attempt`.
- Unknown variables and filters fail.
- The prompt is rendered once per issue/attempt.
- The worker can send shorter continuation guidance on later turns.

Strengths:

- one self-contained repo-owned workflow contract,
- easy to hot-reload,
- easy to test,
- easy to port across languages,
- strict template failure prevents quiet prompt drift.

Weaknesses:

- one prompt body can become overloaded,
- little role separation by default,
- proof/review expectations live in prose unless the implementation adds
  stronger gates,
- quality system depends on what the prompt remembers to demand.

### Codexter prompt model

Codexter spreads prompting across:

- repo/global `AGENTS.md`,
- `skills/*/SKILL.md`,
- skill `todos.md`,
- subagent TOML prompts,
- ticket templates and ticket bodies,
- QA cookbook,
- review rubrics,
- Stop-hook prompts.

Strengths:

- excellent progressive disclosure,
- role-specific workflows,
- rich review and QA gates,
- better durability across long work,
- better human-readable planning artifacts,
- better correction and memory loops.

Weaknesses:

- no single board-run profile,
- no strict prompt-template renderer,
- harder to lint as one runtime contract,
- harder to adapt to Linear/GitHub/Notion without a normalized work-item
  interface,
- some instructions can become scattered or duplicated.

### What Codexter should learn from Symphony's prompt style

Codexter should add a small board-runtime profile, not replace skills with one
large workflow prompt.

Recommended shape:

```yaml
---
board:
  kind: filesystem
  active_states: ["review", "building", "documenting"]
  terminal_states: ["done", "failed"]
dispatch:
  mode: serial
  max_concurrent: 1
  retry_backoff_ms: 300000
workspace:
  strategy: local|worktree|codex_app_worktree|cloud|ssh
  root: .harness/workspaces
prompts:
  run_template: .codexter/prompts/ticket-run.md
  continuation_template: .codexter/prompts/ticket-continue.md
quality:
  requires_qa: from_ticket
  requires_review: true
  completion_receipt: true
---
```

This profile should feed the dispatcher. It should not replace:

- `AGENTS.md`,
- `impl-plan`,
- `$impl`,
- QA,
- review,
- ticket evidence.

## Gap Analysis

### Capability + user

Capability:

- adapter-ready board execution where local tickets are the first adapter, and
  Linear/GitHub/Notion/cloud workers can come later.

User:

- operator who wants Codexter to run prepared work safely across local and
  future remote compute.

### Current state

Codexter has:

- strong filesystem ticket contract,
- serial selector,
- single-ticket build loop,
- rich QA/review/proof gates,
- partial local runtime records,
- planned selective branch runtime,
- partial hosted telemetry work.

Codexter lacks:

- normalized `WorkItem` adapter contract,
- board runtime profile,
- persistent scheduler state,
- retry queue,
- active reconciliation,
- per-ticket workspace invariant,
- app-server or SDK runner layer,
- live runtime snapshot,
- adapter-specific writeback contracts,
- conformance matrix for board execution.

### Production expectation

A credible production-grade board runner should include:

- normalized work item model independent of source board,
- adapter operations for candidate fetch, state refresh, terminal cleanup, and
  optional writeback,
- dispatch eligibility and sorting rules,
- claim/lease model,
- isolated workspace/worktree selection,
- retry and stale-run handling,
- observable runtime state,
- failure categories,
- prompt rendering validation,
- clear trust/sandbox policy,
- conformance tests.

Codexter should add those while preserving:

- ticket depth,
- planning discipline,
- QA/review separation,
- artifact-first evidence,
- completion receipts.

### Missing gaps

1. `WorkItemAdapter` abstraction:
   - current filesystem tickets should become Adapter 1,
   - Linear/GitHub/Notion should become later adapters,
   - adapter must normalize `id`, `identifier`, `title`, `state`, `priority`,
     `labels`, `blocked_by`, `url`, and source-specific metadata.

2. Board runtime profile:
   - one self-contained config/prompt surface for a board run,
   - typed enough to validate and lint,
   - narrow enough not to duplicate the whole harness.

3. Claim and lease policy:
   - current `claimed_by` is human-facing and useful,
   - parallel work needs machine-safe leases, timestamps, owner identity, stale
     detection, and safe release behavior.

4. Workspace and compute selector:
   - local shared checkout,
   - local worktree,
   - Codex app worktree,
   - cloud task,
   - SSH host,
   - maybe later container/VM.

5. Retry/reconciliation:
   - normal continuation retry,
   - failure backoff,
   - slot exhaustion requeue,
   - external state transition stop,
   - stale worker cleanup.

6. Observability:
   - CLI `state` snapshot first,
   - then optional dashboard,
   - include running/retrying, last event, ticket/work item, workspace, tokens,
     runtime, last error, and next action.

7. Prompt template linting:
   - strict variable checks for board runtime prompts,
   - but keep stage-specific skills as the deeper procedural contract.

8. Conformance tests:
   - loader/config,
   - adapter normalization,
   - selector/eligibility,
   - workspace containment,
   - retry/reconciliation,
   - evidence/review gate integration,
   - adapter writeback boundaries.

## Advice Options

### Option A: Stay local and serial for now

Pros:

- low risk,
- preserves Codexter's best quality loops,
- avoids premature daemon complexity,
- compatible with current tickets.

Cons:

- does not answer future Linear/GitHub/Notion adapter needs,
- does not solve retries, observability, or parallel compute,
- leaves `$ralph` as a dispatcher rather than a runner.

### Option B: Add an adapter-ready board runtime profile, still local-first

Pros:

- learns the right lessons from Symphony without cloning the daemon,
- lets filesystem tickets remain first-class,
- creates the seam for Linear/GitHub/Notion later,
- gives `TASK-0081` selective runtime a clearer target,
- can be proven through serial local execution before parallelism.

Cons:

- requires careful scope control,
- adds a new config surface that must not duplicate root policy,
- still needs a later daemon/parallel ticket.

### Option C: Build a Symphony-style daemon now

Pros:

- fastest path to parity with scheduler mechanics,
- natural fit for Linear polling,
- clear operational model.

Cons:

- high complexity,
- risks bypassing Codexter's ticket/proof strengths,
- likely duplicates Codex app automations/worktrees/Linear primitives,
- premature before claims, leases, merge policy, and batch QA are specified.

## Recommendation

Choose Option B.

Codexter should build a board-runtime contract before a board-runtime daemon.
The next useful milestone is not "Elixir-style background service." It is:

> a Codexter-native adapter and board profile that can drive the existing
> serial `$ralph` and `$impl` loop from filesystem tickets today, while making
> Linear/GitHub/Notion and remote compute natural adapters later.

Tradeoff accepted:

- Codexter will still not be a fully autonomous parallel service immediately.
  That is acceptable because the durable win is the abstraction boundary.

## Recommended Roadmap

### Phase 1: Specify the board adapter boundary

Create a spec for:

- `WorkItem`,
- `BoardAdapter`,
- `FileTicketAdapter`,
- adapter read operations,
- optional writeback operations,
- adapter error categories,
- how Codexter tickets map to/from external issues.

Keep it documentation-first. Do not build Linear yet.

### Phase 2: Add a board runtime profile

Define one `BOARD.md` or `.codexter/board-runtime.md` style profile:

- front matter for dispatch/runtime config,
- prompt templates for first run and continuation,
- quality gates linked to existing skills,
- strict variable names,
- hot reload optional later.

This should be much smaller than Symphony `WORKFLOW.md` because Codexter
already has skills, tickets, and review rubrics.

### Phase 3: Wire serial `$ralph` through the adapter

Keep filesystem tickets as Adapter 1:

- current selector behavior should keep working,
- board runtime profile should supply policy,
- output should include skipped reasons and next selected work item,
- no parallelism yet.

### Phase 4: Add runtime snapshot and observability

Start with a local CLI/JSON snapshot:

- selected/running/retrying,
- claim/lease,
- last event,
- workspace,
- verification state,
- last error,
- token/runtime when available.

Only then decide whether the hosted Convex telemetry ticket should resume,
change shape, or retire.

### Phase 5: Add selective compute placement

Use `TASK-0081` as the natural home for:

- local shared checkout,
- local worktree,
- branch runtime,
- Codex app worktree handoff,
- future cloud/SSH adapter.

Do not let compute placement become the board adapter. Keep them separate:

- board adapter says what work exists,
- compute selector says where a work item runs.

### Phase 6: Open the daemon/parallel ticket

Only after Phases 1-5:

- leases,
- max concurrency,
- retry queue,
- stale worker handling,
- merge policy,
- batch/release QA,
- external adapter writeback,
- app-server/SDK runner.

At that point, Symphony becomes a strong reference algorithm for the daemon.

## What Not To Copy

Do not copy:

- Linear as the only first-class board,
- one giant `WORKFLOW.md` that replaces skills,
- daemon-first execution,
- tracker writes buried in the orchestrator,
- scheduler success without Codexter review/evidence gates,
- parallel dispatch before lease/worktree/merge/batch-QA policy exists.

Do copy:

- normalized issue/work item model,
- typed config profile,
- strict prompt rendering,
- workspace containment,
- retry/backoff,
- reconciliation,
- structured logs/snapshot,
- conformance matrix,
- clear implementation-defined trust posture.

## Brainstorm: Where This Could Go

### Direction 1: Codexter as the quality layer over Codex primitives

Codex app handles:

- worktrees,
- Linear cloud tasks,
- automations,
- local environments,
- SDK/app-server execution.

Codexter handles:

- board policy,
- ticket depth,
- planning,
- QA/review,
- evidence,
- completion trust,
- adapter normalization.

This is the best near-term bet.

### Direction 2: Codexter as a portable local daemon

Codexter becomes a Symphony-style daemon that reads adapters and runs agents
locally.

This is powerful, but only worth doing after the board adapter and compute
selector are proven.

### Direction 3: Codexter as a board-independent protocol

Codexter defines `WorkItem`, `ProofPacket`, `ReviewReceipt`, `RuntimeProfile`,
and `ComputeTarget` as portable contracts. Any board can implement them.

This is the long-term clean shape. It makes Linear "just an adapter" instead of
the system identity.

## Final Assessment

Codexter is not behind Symphony overall. It is behind on service mechanics and
ahead on task quality, proof, and operator trust.

The next move is to generalize Codexter's board layer just enough that local
tickets stop being a hardcoded source. Then the system can choose compute per
ticket:

- local checkout for simple work,
- local worktree for parallel or risky changes,
- Codex app worktree/cloud task when platform support is enough,
- remote/SSH/container later when isolation or capacity demands it.

That path keeps the soul of Codexter intact: visible artifacts first, runtime
machinery second, proof before completion.

## Addendum: Re-evaluating `WORKFLOW.md` as a Control-Tower File

Follow-up operator feedback changed the recommendation nuance.

The earlier memo said Codexter should not copy Symphony's giant `WORKFLOW.md`.
That is still true if "copy" means replacing Codexter's skills, tickets,
subagents, QA, and review system with one monolithic prompt. But the operator's
real point is stronger:

> Codexter has many good files, but agents often fail to consistently choose
> the right ones. A central workflow file may reduce that mental and operational
> load by becoming the one obvious front door for a board run.

That is the right lesson to take from Symphony.

### Revised stance

Codexter should adopt a `WORKFLOW.md`-like control-tower file, but define it as
an index and runtime profile over Codexter's existing skills rather than as a
replacement prompt.

Good use:

- one file declares the board adapter, compute strategy, dispatch limits,
  ticket states, skill routing, proof gates, and prompt templates;
- the dispatcher and agents read this file first;
- the file points to canonical skills and docs for deeper behavior;
- missing or invalid fields fail early;
- strict template variables make board-run prompts safer.

Bad use:

- one giant prompt tries to restate every skill;
- the workflow file duplicates review rubrics, QA contracts, and ticket
  template details;
- the file becomes a second source of truth for rules that already have an
  owning skill/spec;
- agents stop using specialized skills because the front door became too large.

### Why it may make Codexter easier to operate

1. **Fewer starting points.**
   Agents currently decide among `AGENTS.md`, `README.md`, `ARCHITECTURE.md`,
   `tickets/README.md`, `impl-plan`, `$impl`, `$ralph`, QA, review, and runtime
   specs. A control-tower file can say "for this board, start here, then route
   to these exact skills."

2. **Adapter clarity.**
   Filesystem, Notion, Linear, GitHub, and future boards can all implement the
   same Kanban-like interface: fetch candidates, read one ticket, claim/update
   one ticket, refresh state, write result links, and release/close. The workflow
   file can choose the adapter without rewriting the harness.

3. **Compute clarity.**
   The board and the compute target should be separate decisions. A ticket can
   be sourced from Notion but run locally, on a Codex worktree, on a cloud
   background agent, through Dagster/Open Claw, or later through SSH/container
   workers. The workflow file can declare the policy for choosing.

4. **Lower operator stress.**
   Instead of remembering whether a ticket should use `$ralph`, `$impl`,
   `pr-runtime`, Open Claw, Dagster, or a cloud agent, the operator tags the
   ticket and the workflow policy decides.

5. **Better automation path.**
   Symphony's poll/reconcile loop and Open Claw's Dagster cron are the same
   family of system: a board reader plus a capacity-aware dispatcher. A
   workflow file gives that loop a stable policy input.

### Suggested `WORKFLOW.md` shape for Codexter

```yaml
---
workflow:
  name: codexter-local-board
  version: 1

board:
  adapter: filesystem | notion | linear | github
  source: tickets/
  active_states: ["review", "building", "documenting"]
  terminal_states: ["done", "failed"]
  delegatable_labels: ["delegatable", "low-priority", "background"]
  human_gate_labels: ["needs-human", "deploy", "spend", "destructive"]

dispatch:
  mode: serial | pooled
  max_concurrent_agents: 3
  poll_interval_ms: 1800000
  claim_ttl_ms: 7200000
  retry_backoff_ms: 300000
  sort: ["priority", "created_at", "identifier"]

compute:
  default: local
  policies:
    - when: label:background
      target: cloud_codex
    - when: label:hands-on
      target: local
    - when: risk:parallel_safe
      target: codex_worktree
    - when: adapter:notion label:open-claw
      target: dagster_open_claw

routing:
  planning: impl-plan
  building: impl
  qa: qa
  review: review
  documenting: close-ticket

quality:
  requires_ticket_evidence: true
  requires_review: true
  requires_qa_from_ticket: true
  completion_receipt: true

prompts:
  first_turn: .codexter/prompts/first-turn.md
  continuation: .codexter/prompts/continue.md
---

# Workflow Prompt

You are running one work item from {{ board.adapter }}.

Use the configured `routing` skills for each phase. Do not restate those skill
contracts here. Treat this file as the board-run policy and the selected ticket
as the task-local source of truth.
```

### How this generalizes Open Claw

Open Claw already behaves like one concrete compute target:

- board adapter: Notion;
- scheduler: Dagster cron every 30 minutes;
- capacity policy: run only when fewer than N agents are active;
- executor: background agent with skills;
- completion target: finish/update the ticket end to end.

Codexter can generalize that by naming Open Claw as one `compute.target`
instead of treating it as a separate mental model. The same board item could
choose:

- `local` for hands-on work,
- `codex_worktree` for isolated local background work,
- `cloud_codex` for low-priority delegatable tickets,
- `dagster_open_claw` for Notion/Dagster-managed recurring background jobs,
- `ssh` or `container` later for remote capacity.

### Event-based versus polling

Polling is the right v1 default because every Kanban source supports it and it
is easy to reason about. Event-driven dispatch should be an adapter
optimization, not a separate system.

Recommended progression:

1. `poll`: fetch candidates every N minutes, respect capacity and claims.
2. `webhook`: adapters that support events enqueue an immediate refresh.
3. `hybrid`: webhooks trigger fast refresh, polling remains the backstop.

This matches the shape of Open Claw's current cron loop and Symphony's polling
loop while leaving room for Linear/Notion/GitHub event triggers later.

### Updated recommendation

The next strategic ticket should be:

> Define Codexter `WORKFLOW.md` as the board-run control-tower file, with
> board adapter, compute target, dispatch policy, skill routing, and quality
> gates. Implement only the filesystem adapter first.

This should come before a full daemon. Once that file exists, the later daemon
or Dagster/Open Claw integration has a stable contract to execute.
