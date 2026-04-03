# Proposal: Focused Changes To Make Codexter More Complete

Date: 2026-04-02

## Position

Codexter does not need a large harness rewrite. It already has the better planning discipline, file-based workflow, UI testability contract, and cleaner governance model. The missing pieces are mostly runtime and orchestration support.

The right move is to add a small amount of runtime structure around the existing ticket-driven process, not to copy OMX wholesale. In particular, Codexter should **not** copy OMX's default auto-continue / auto-nudge behavior. Passive telemetry and resumability are worth adding. Runtime-injected continuation is not.

## What To Add

### 1. A small run-oriented runtime layer

Add a minimal runtime folder for active and resumable work, for example:

```text
.codexter/
  runs/<RUN_ID>/
    prompt.md
    spec.md
    run-state.json
    summary.md
    rounds/
      01/
        contract.md
        builder-report.md
        evaluator-report.md
        metrics.json
        handoff.md
```

This should become the canonical handoff surface for long-running work. It gives Codexter explicit run memory without replacing tickets or repo docs.

### 2. An explicit planner -> builder -> evaluator loop

Codexter already has planner-like, builder-like, and evaluator-like pieces, but they are not unified as one harness loop. Add a first-class workflow that:

1. turns a short prompt into a clarified spec
2. derives the next executable contract
3. implements one slice
4. evaluates it against explicit criteria
5. either advances or fails the round with concrete follow-up work

This should reuse existing ticket and QA surfaces instead of inventing a second planning system.

### 3. A normalized evaluator scorecard

Keep `qa-tester`, `visual-qa`, and `code-review`, but add one shared report shape so a round ends with a comparable result instead of scattered outputs.

Recommended rubric:
- functionality
- UX / visual quality
- code quality
- evidence completeness
- acceptance-criteria coverage

Each category should have:
- score
- threshold
- pass/fail
- concrete failure reasons
- next required action

### 4. A missing discovery workflow

The research shows Codexter conceptually wants brainstorm/interview behavior but does not ship it as a concrete reusable workflow. Add one lightweight discovery stage for ambiguous prompts.

This should be small:
- clarify intent
- identify constraints
- produce a tighter product or feature brief
- stop before implementation detail bloat

### 5. Passive turn telemetry

Add a passive hook or equivalent lifecycle bookkeeping that records:
- active run
- current phase
- last completed step
- last verification result
- last agent/tool activity timestamp

This is worth stealing from OMX. Hidden continuation is not.

## What To Keep

### 1. Filesystem board and ticket-first execution

Keep the ticket board as the primary execution surface. It is one of Codexter's strongest design choices. The new run layer should coordinate with tickets, not replace them.

### 2. UI agent-contract and evidence doctrine

Keep the `Agent Contract`, `Test hook`, `Stabilize`, `Inspect`, and evidence-checklist model. This is already stronger and cleaner than what either Anthropic's public description or OMX exposes for UI work.

### 3. Root governance and engineering discipline

Keep:
- strong DoD
- memory/history/troubles separation
- planning/build separation
- explicit board movement
- small-slice execution bias

Codexter's problem is not weak process. It is missing runtime support for the process.

### 4. Preference for explicit human-visible artifacts

Keep file-based handoffs and visible artifacts as the source of truth. This is compatible with Anthropic's strongest harness ideas and avoids hidden runtime behavior.

## What To Avoid

### 1. Default auto-continue / auto-nudge behavior

Codexter should **not** copy OMX's auto-continue behavior by default.

Specifically avoid:
- scanning model output for stall phrases and auto-injecting replies
- watcher-driven "continue now" behavior
- runtime choosing continuation on the operator's behalf

This behavior may increase momentum, but it weakens operator trust and makes the system harder to reason about. If Codexter ever supports it, it should be an explicit opt-in autonomy mode, not the default.

### 2. Runtime complexity before it is load-bearing

Avoid importing:
- tmux-heavy control planes
- mailbox/lease/lock systems for single-session work
- fallback watcher layers
- aggressive session-control machinery

Codexter should earn that complexity only if long-running multi-worker orchestration becomes a real bottleneck.

### 3. Risky git automation

Avoid default:
- auto-merge
- auto-rebase
- conflict-strategy integration
- hidden branch reconciliation

If Codexter later adds durable multi-worker execution, integration should stay explicit and reviewable.

### 4. Prompt and mode sprawl

Avoid adding many thin workflow aliases. New surfaces should map to distinct behavior:
- discovery
- run orchestration
- evaluation
- optional autonomy mode

Anything else is likely to become naming overhead.

## Recommended Architecture Changes

### 1. Add a thin runtime substrate, not a second harness

Recommended split:

- `tickets/` remains the work queue and approval surface
- `docs/` remains durable human-readable project memory
- `.codexter/runs/` becomes run-specific machine-friendly state and handoff storage

This preserves Codexter's current strengths while fixing its main weakness: lack of explicit run lifecycle management.

### 2. Introduce run artifacts as the long-task control plane

Each run should have:
- one prompt artifact
- one current spec artifact
- one state artifact
- per-round contract/build/evaluation artifacts
- one final summary artifact

That is enough to support:
- resume after context loss
- explicit phase transitions
- round-by-round comparison
- post-run analysis

### 3. Unify evaluator outputs without collapsing evaluator roles

Do not merge `qa-tester`, `visual-qa`, and `code-review` into one blob. Keep the role separation, but normalize their outputs into one shared evaluator report format.

That preserves specialization while making results measurable.

### 4. Make context policy explicit

Codexter should define when to:
- stay in the current session
- compact into run artifacts
- resume from artifacts in a fresh session

A simple rule is enough:
- stay in-session for short focused work
- compact at phase boundaries and after failed evaluation rounds
- require a `handoff.md` before any deliberate reset or resume

### 5. Treat verification evidence as a runtime concept

Codexter already says verification matters. Make that machine-visible by storing:
- verification targets
- executed checks
- results
- failing threshold categories

This should be small and append-only per round.

## Phased Implementation Plan

### Phase 1: Minimal runtime completeness

Build:
- `.codexter/runs/<RUN_ID>/` artifact structure
- `run-state.json`
- `summary.md`
- passive lifecycle bookkeeping
- shared evaluator report schema

Do not build:
- auto-nudging
- fallback watchers
- team runtime
- git automation

Success condition:
- one long task can be paused and resumed from artifacts without relying on chat history alone

### Phase 2: First-class orchestration workflow

Build:
- lightweight discovery workflow
- explicit planner -> builder -> evaluator run loop
- round creation and transition rules
- evaluator thresholding

Success condition:
- a short prompt can produce a spec, a contract, a build round, and a pass/fail evaluator result

### Phase 3: Comparison and observability

Build:
- per-run metrics
- per-round deltas
- time/cost counters where available
- defect and retry counts

Success condition:
- Codexter can answer which loop steps are load-bearing and where rounds fail

### Phase 4: Optional durable multi-worker support

Only if later justified, build:
- worktree assignment
- shared task state
- explicit worker ownership
- explicit leader-controlled integration

Success condition:
- parallel work is durable and reviewable without hidden git actions

## Minimal Viable Runtime Layer

This should be the smallest useful runtime addition.

### Required artifacts

```text
.codexter/runs/<RUN_ID>/
  prompt.md
  spec.md
  run-state.json
  summary.md
  rounds/01/
    contract.md
    evaluator-report.md
    handoff.md
```

### Required fields in `run-state.json`

```json
{
  "run_id": "string",
  "mode": "interactive|assisted-autonomous|full-autonomous",
  "phase": "discovery|planning|contract|build|evaluate|complete|blocked",
  "round": 1,
  "status": "active|paused|blocked|complete|failed",
  "current_ticket": "optional ticket path",
  "last_updated_at": "ISO timestamp",
  "last_verification": {
    "status": "pass|fail|not-run",
    "summary": "short text"
  },
  "next_visible_action": "short text"
}
```

### Required behavior

- always write the current phase
- always write the next visible action
- always record the latest evaluation outcome
- never inject user input automatically
- never hide continuation decisions in the runtime

That is enough to make Codexter resumable and inspectable.

## Autonomy Modes Proposal

Codexter should make autonomy explicit instead of universal.

### `interactive` (default)

Behavior:
- no auto-continue
- no injected replies
- no hidden runtime steering
- agent can suggest the next action, but waits when a real operator decision is needed

Use for:
- normal interactive development
- collaborative steering
- research and planning work

### `assisted-autonomous`

Behavior:
- stronger forward progress bias
- passive stall detection allowed
- runtime may surface suggested next actions in files or summaries
- still no automatic injected input

Use for:
- longer implementation runs where the operator wants momentum without surrendering control

### `full-autonomous` (explicit opt-in only)

Behavior:
- can run extended loops and retries within a declared scope
- may continue across planned phases without manual re-approval
- still should prefer visible artifact updates over hidden steering

Important:
- even here, Codexter should be cautious about copying OMX-style injected continuation
- if such behavior ever exists, it should be separately enabled and clearly visible

This mode structure is cleaner than OMX's default-enabled auto-nudge approach because it makes the autonomy boundary legible.

## Risks And Tradeoffs

### 1. Added structure can become ceremony

Risk:
- too many run artifacts can slow small tasks

Mitigation:
- use the runtime layer only for long-running or resumable work
- keep the artifact set minimal

### 2. Scorecards can create false precision

Risk:
- numeric evaluation can look more rigorous than it really is

Mitigation:
- require concrete failure reasons and next actions, not just scores
- keep thresholds simple and tied to acceptance criteria

### 3. Runtime state can drift from the board

Risk:
- tickets and run artifacts can disagree

Mitigation:
- define tickets as the work queue source of truth
- define run artifacts as the execution-state source of truth
- require the current ticket path in `run-state.json` when relevant

### 4. Optional autonomy modes can still creep toward hidden behavior

Risk:
- pressure for "just keep going" features can reintroduce intrusive control-plane behavior

Mitigation:
- default to `interactive`
- keep auto-continue disabled by default
- require explicit user opt-in for any stronger autonomy behavior

### 5. Delaying team runtime means some OMX advantages remain unmatched

Risk:
- Codexter will still lag OMX on durable multi-worker orchestration in the short term

Mitigation:
- accept this deliberately
- first close the single-run lifecycle gap, which is smaller, safer, and more obviously useful

## Bottom Line

The smallest coherent improvement is:

1. add a minimal run-state and run-artifact layer
2. make planner -> builder -> evaluator an explicit loop
3. normalize evaluator outputs with thresholds
4. add passive telemetry only
5. keep autonomy mode-explicit and **do not copy OMX auto-nudge by default**

That would make Codexter materially more complete without turning it into a bloated runtime clone of OMX.
