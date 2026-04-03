# Research: Codexter vs OMX Gap Analysis

Date: 2026-04-02

## Scope

This memo answers two practical questions:

1. What is the current gap between `Codexter` and `oh-my-codex` (OMX)?
2. Which OMX features are worth stealing, and which behaviors should be avoided, especially OMX's automatic "please continue" / auto-nudge behavior?

This is intended as a planning memo, not just a descriptive summary.

## Short Answer

Codexter is currently stronger as:
- a clean harness repo
- a disciplined filesystem workflow
- a planning/ticket/QA contract

OMX is currently stronger as:
- a runtime system
- a persistent state/memory environment
- a long-running control loop
- a durable multi-agent coordination runtime

The highest-level gap is:

> Codexter has better process structure than runtime machinery.
> OMX has much more runtime machinery than Codexter.

The feature you explicitly dislike in OMX is real and deliberate:

> OMX includes an auto-nudge subsystem that detects assistant stall phrases like "Would you like me to continue?" and injects canned replies into the tmux pane to keep the agent moving.

That behavior is implemented in code and should be treated as a conscious design choice, not an accident.

## The Gap Between Codexter and OMX

## 1. Codexter is a strong protocol; OMX is closer to an operating environment

Codexter today gives you:
- root governance via `AGENTS.md`
- skill/agent catalog
- PRD/spec/ticket board flow
- UI agent-contract and evidence doctrine
- memory/history/troubles logs

Evidence:
- [Codexter/AGENTS.md](/Users/kenjipcx/coding-harness/Codexter/AGENTS.md)
- [Codexter/tickets/templates/ticket.md](/Users/kenjipcx/coding-harness/Codexter/tickets/templates/ticket.md)
- [Codexter/skills/spec-to-ticket/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/spec-to-ticket/SKILL.md)
- [Codexter/skills/visual-qa/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/visual-qa/SKILL.md)

OMX adds a runtime substrate on top of this kind of guidance:
- installed notify hook
- state and memory MCP servers
- `.omx/` mode state, plans, logs, project memory, notepad
- session lifecycle tracking
- durable tmux/worktree team runtime
- watcher/nudge/control-plane upkeep between turns

Evidence:
- [oh-my-codex/README.md](/Users/kenjipcx/coding-harness/oh-my-codex/README.md)
- [oh-my-codex/AGENTS.md](/Users/kenjipcx/coding-harness/oh-my-codex/AGENTS.md)
- [oh-my-codex/src/scripts/notify-hook.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook.ts)
- [oh-my-codex/src/mcp/state-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-server.ts)
- [oh-my-codex/src/team/runtime.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime.ts)

Gap summary:
- Codexter has the workflow logic.
- OMX has more of the runtime enforcement and persistence layer.

## 2. Codexter has better ticket/testability discipline for UI work

Codexter is already better or at least cleaner on:
- explicit UI `Agent Contract`
- `Test hook`
- `Stabilize`
- `Inspect`
- `Key screens/states`
- evidence checklist

Evidence:
- [Codexter/skills/spec-to-ticket/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/spec-to-ticket/SKILL.md)
- [Codexter/agents/qa-tester.toml](/Users/kenjipcx/coding-harness/Codexter/agents/qa-tester.toml)

OMX has strong verification as a principle, but its UI-specific contract surface is not as cleanly specialized as Codexter's ticket-first UI doctrine.

So the gap is not "Codexter needs OMX's QA philosophy."
The gap is:

> Codexter needs more runtime/persistence/control-plane machinery around the strong workflow discipline it already has.

## 3. Codexter lacks several runtime capabilities that OMX already has

The biggest missing pieces in Codexter are:

### A. Installed turn hook / lifecycle hook

OMX installs a real notify hook into Codex config:
- configured in generated `config.toml`
- used to update state every turn

Evidence:
- [oh-my-codex/src/config/generator.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/config/generator.ts)

Codexter does not currently have an equivalent always-on runtime hook layer.

### B. Session-scoped state substrate

OMX has:
- root and session-scoped mode state
- scope resolution
- atomic writes
- MCP access to state

Evidence:
- [oh-my-codex/src/mcp/state-paths.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-paths.ts)
- [oh-my-codex/src/mcp/state-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-server.ts)

Codexter has durable docs and a ticket board, but not this kind of state API.

### C. Memory server / structured runtime memory

OMX has:
- `.omx/project-memory.json`
- `.omx/notepad.md`
- MCP tools to read/write/prune/query them

Evidence:
- [oh-my-codex/src/mcp/memory-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/memory-server.ts)

Codexter has memory docs, but not a runtime memory service.

### D. Team runtime for durable coordination

OMX team mode is a real runtime with:
- tmux workers
- mailboxes
- dispatch
- task claims
- locks
- worktrees
- monitor snapshots
- shutdown/resume logic

Evidence:
- [oh-my-codex/skills/team/SKILL.md](/Users/kenjipcx/coding-harness/oh-my-codex/skills/team/SKILL.md)
- [oh-my-codex/src/team/runtime.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime.ts)
- [oh-my-codex/src/team/state/tasks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/tasks.ts)
- [oh-my-codex/src/team/state/locks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/locks.ts)

Codexter has role and workflow surfaces, but not a durable external coordination runtime.

### E. Runtime-side verification helpers

OMX has verification not only in prompts but also in code helpers such as:
- structured evidence helpers
- verification-oriented completion checks

Evidence:
- [oh-my-codex/src/verification/verifier.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/verification/verifier.ts)

Codexter has verification doctrine, but less runtime tooling around it.

## How the OMX Auto-Continue / Auto-Nudge Works

This is the exact subsystem you said you hate.

## 1. It is implemented on purpose in a dedicated module

The file starts with:

> "Auto-nudge: detect Codex 'asking for permission' stall patterns and automatically send a continuation prompt so the agent keeps working."

Evidence:
- [oh-my-codex/src/scripts/notify-hook/auto-nudge.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook/auto-nudge.ts)

So this is not incidental behavior. It is a declared design goal.

## 2. It looks for "stall phrases" in model output

Default stall patterns include phrases like:
- `if you want`
- `would you like`
- `shall i`
- `should i`
- `do you want`
- `want me to`
- `let me know`
- `next i can`
- `continue with`
- `next step`
- `ready to proceed`
- `keep going`
- `type continue`

Evidence:
- [oh-my-codex/src/scripts/notify-hook/auto-nudge.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook/auto-nudge.ts)

This means OMX is explicitly optimized to suppress "asking permission" behaviors from the agent.

## 3. Default behavior is enabled

When config is missing or unspecified, `normalizeAutoNudgeConfig()` defaults to:
- `enabled: true`
- `response: "yes, proceed"`
- `delaySec: 3`
- `stallMs: 5000`
- `ttlMs: 30000`

Evidence:
- [oh-my-codex/src/scripts/notify-hook/auto-nudge.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook/auto-nudge.ts)

So out of the box, OMX is opinionated in favor of automatic continuation.

## 4. It injects the response directly into the tmux pane

When triggered, OMX resolves a target pane and sends:

`yes, proceed [OMX_TMUX_INJECT]`

or a configured alternative such as:

`continue now [OMX_TMUX_INJECT]`

It then submits the input automatically.

Evidence:
- [oh-my-codex/src/scripts/notify-hook/auto-nudge.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook/auto-nudge.ts)
- [oh-my-codex/src/team/tmux-session.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/tmux-session.ts)
- tests under [oh-my-codex/src/hooks/__tests__/notify-hook-auto-nudge.test.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/hooks/__tests__/notify-hook-auto-nudge.test.ts)

This is exactly the behavior you are reacting against.

## 5. There is also a fallback watcher

OMX has a separate fallback watcher process that can also trigger nudges when:
- a turn appears stalled
- Ralph appears stalled
- the leader appears stale
- team progress stalls

This watcher can synthesize nudges from HUD state and prior state even when the main notify-hook path is not enough.

Evidence:
- [oh-my-codex/src/scripts/notify-fallback-watcher.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-fallback-watcher.ts)

This means the system has multiple layers of continuation pressure, not just one.

## 6. Ralph adds another continue-steer path

The fallback watcher includes a dedicated Ralph steer message:

`Ralph loop active continue`

and sends that with the tmux injection marker.

Evidence:
- [oh-my-codex/src/scripts/notify-fallback-watcher.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-fallback-watcher.ts)

So OMX continuation pressure exists in at least three places:
- auto-nudge stall detection
- fallback watcher auto-nudge
- Ralph continue-steer

## Why This Feels Bad in Practice

From a harness-design perspective, the problem is not just "it continues too much."
The real issue is that OMX crosses an important boundary:

> it sometimes chooses agent continuation on the user's behalf at the runtime layer

That has side effects:
- you lose the sense of being able to interrupt naturally
- runtime autonomy overrides operator intent too aggressively
- the harness becomes harder to reason about because the continuation logic is distributed across hooks and watchers
- it can keep momentum high, but at the cost of operator trust

This is useful for "never stop" workflows.
It is much less good for a harness you want to steer interactively.

## What Codexter Should Steal From OMX

These are the features worth stealing.

## 1. A lightweight runtime state layer

Steal:
- session-scoped mode state
- atomic writes
- explicit mode lifecycle files
- a tiny state API

Do not steal:
- broad complexity before you need it

Best Codexter version:
- `.harness/state/` or `.omx/`-like scoped runtime folder
- `session.json`
- `mode-state.json`
- minimal MCP or CLI helpers for read/write/status

## 2. A memory/notepad substrate

Steal:
- durable project memory
- scratch notepad / working memory
- separate curated memory from ephemeral working notes

Codexter already has:
- `docs/MEMORY.md`
- `docs/HISTORY.md`
- `docs/TROUBLES.md`

What to add:
- a machine-friendly runtime memory layer to complement the docs

## 3. A notify-hook style telemetry hook, but not a command-injection hook

Steal:
- turn-level telemetry
- heartbeat updates
- session metrics
- skill/mode activity tracking
- task progress bookkeeping

Do not steal:
- automatic injected replies like `yes, proceed`
- hidden runtime continuation on the user's behalf

Best Codexter version:
- a passive hook first
- log-only or state-only
- maybe surface "suggested next action" to the user, but never inject it

## 4. Team/runtime concepts, but only if you really want durable parallelism

Steal if needed:
- mailbox pattern
- task claims/leases
- worker identity
- worktree isolation
- shutdown/resume semantics

Do not steal blindly:
- auto-merge/rebase machinery
- over-complex team control plane before you need it

Best Codexter version:
- start with shared task state + worktrees + explicit human-controlled integration
- skip automatic merge/rebase until there is a strong reason

## 5. Verification as runtime-backed evidence

Steal:
- evidence helpers
- explicit "no evidence = not complete" runtime posture
- verification summaries that can be checked by tooling

Codexter already has the doctrine.
What it lacks is more runtime-level support.

## What Codexter Should Not Steal From OMX

## 1. Auto-continue / auto-approval injection

Do not copy:
- stall phrase detection that auto-injects "yes, proceed"
- fallback watcher continue-steers
- hidden continuation behavior in the control plane

If you want a compromise:
- detect stall patterns
- log them
- maybe show a suggestion
- never inject input automatically unless the user explicitly enables a "hands-off" mode

## 2. Prompt-surface sprawl

OMX has accumulated a lot of:
- workflows
- aliases
- layered prompts
- historical mode surfaces

Codexter should stay tighter and only add surfaces that map to distinct behavior.

## 3. Risky auto-integration git behavior

OMX team runtime includes aggressive automation around:
- auto-commit
- merge with conflict strategies
- cherry-pick and rebase automation

That is one of the riskiest parts of the system.

Codexter should prefer:
- worktree isolation
- explicit review/integration
- human or leader-controlled merges

## Proposed Plan for Codexter

This is the practical plan I would recommend right now.

## Phase 1: Close the most obvious harness gap without adding bad autonomy

Build:
- passive runtime hook
- session/runtime state folder
- minimal mode state API
- working-memory/notepad layer

Do not build yet:
- auto-continue
- tmux injection
- fallback watcher
- auto-merge/rebase control plane

Outcome:
- Codexter becomes more runtime-aware without becoming intrusive

## Phase 2: Add explicit orchestrator artifacts

Build:
- run artifacts for long tasks
- per-run summaries
- round/phase status
- explicit "next suggested action" files

Important:
- suggested action is visible, not injected

Outcome:
- you gain resumability and observability
- without giving up operator control

## Phase 3: Add optional durable team mode only if you actually need it

Build only if needed:
- shared task state
- worker mailboxes
- worktree assignment
- explicit shutdown/resume

Avoid at first:
- automatic git integration
- continuation nudges
- hidden control-plane actions

Outcome:
- you get the useful part of OMX team mode
- without adopting its riskiest complexity

## Phase 4: Add explicit autonomy modes

Instead of making continuation universal, define modes:

- `interactive`
  - no automatic continuation
  - never inject replies
  - wait for user when the agent asks a real question

- `assisted-autonomous`
  - may suggest next actions
  - no hidden injected input

- `full-autonomous`
  - optional, explicit, user-enabled
  - only here would something like auto-continue even be considered

This is a much cleaner design than OMX's default-enabled auto-nudge behavior.

## Recommended Product Direction

If the goal is "make Codexter more complete," the right move is:

### Steal

- runtime state
- memory substrate
- hook-based telemetry
- verification helpers
- optional durable team runtime ideas

### Keep

- Codexter's cleaner governance
- filesystem board
- ticket-first planning
- UI testability doctrine

### Reject by default

- auto-continue injection
- fallback watcher continue-steers
- runtime choosing continuation for the user
- aggressive auto-merge/rebase workflows

## Bottom Line

The gap between Codexter and OMX is mostly:

> runtime machinery, not planning quality

OMX's main strengths are:
- persistent state
- hook-driven upkeep
- durable coordination runtime

OMX's most annoying behavior, from your perspective, is also easy to isolate:

> the auto-nudge / continue-steer subsystem is a specific runtime feature, not the essence of the harness

That is good news.

It means you can steal the best parts of OMX without inheriting the part you hate.

The clean Codexter strategy is:

> build a passive runtime substrate first, then add explicit operator-controlled autonomy modes, instead of baking hidden auto-continuation into the default experience.

## Key Sources

Codexter:
- [Codexter/AGENTS.md](/Users/kenjipcx/coding-harness/Codexter/AGENTS.md)
- [Codexter/tickets/templates/ticket.md](/Users/kenjipcx/coding-harness/Codexter/tickets/templates/ticket.md)
- [Codexter/skills/spec-to-ticket/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/spec-to-ticket/SKILL.md)
- [Codexter/docs/research/web-research/2026-04-02_anthropic-harness-comparison.md](/Users/kenjipcx/coding-harness/Codexter/docs/research/web-research/2026-04-02_anthropic-harness-comparison.md)
- [Codexter/docs/research/web-research/2026-04-02_oh-my-codex-harness-analysis.md](/Users/kenjipcx/coding-harness/Codexter/docs/research/web-research/2026-04-02_oh-my-codex-harness-analysis.md)

OMX:
- [oh-my-codex/README.md](/Users/kenjipcx/coding-harness/oh-my-codex/README.md)
- [oh-my-codex/AGENTS.md](/Users/kenjipcx/coding-harness/oh-my-codex/AGENTS.md)
- [oh-my-codex/src/config/generator.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/config/generator.ts)
- [oh-my-codex/src/scripts/notify-hook.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook.ts)
- [oh-my-codex/src/scripts/notify-hook/auto-nudge.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook/auto-nudge.ts)
- [oh-my-codex/src/scripts/notify-fallback-watcher.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-fallback-watcher.ts)
- [oh-my-codex/src/mcp/state-paths.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-paths.ts)
- [oh-my-codex/src/mcp/state-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-server.ts)
- [oh-my-codex/src/mcp/memory-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/memory-server.ts)
- [oh-my-codex/src/team/runtime.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime.ts)
- [oh-my-codex/src/team/state/tasks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/tasks.ts)
- [oh-my-codex/src/team/state/locks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/locks.ts)
