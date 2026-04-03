# Research: How the oh-my-codex Harness Works

Date: 2026-04-02

## Scope

Study `oh-my-codex` as a harness:
- how it works architecturally
- how it maintains autonomy
- what is runtime-enforced versus prompt-enforced
- how it handles long-running and parallel work
- what makes it special
- which parts seem load-bearing versus likely to go stale

This memo is written to be comparison-friendly against:
- Codexter
- Anthropic's March 24, 2026 harness article

## Executive Summary

`oh-my-codex` is not just a prompt pack and not just a Codex convenience CLI.
It is best understood as a layered harness around Codex CLI with four main pieces:

1. `AGENTS.md` as the orchestration brain
2. role prompts and workflow skills as reusable execution surfaces
3. `.omx/` as the persistent state/memory/logging substrate
4. runtime glue, especially the notify hook and team runtime, that keeps long-running workflows alive across turns

Its strongest differentiator is that it tries to behave like an operating environment for agent work, not merely a set of better prompts.

The most important architectural truth is this:

> OMX is partly a real runtime system and partly a disciplined instruction system.

The runtime side is real and important:
- installed notify hook
- persistent mode state
- MCP state/memory servers
- tmux/worktree team runtime
- mailboxes, task claims, locks, dispatch, shutdown, and monitoring

But a meaningful share of OMX behavior is still enforced mainly through prompt/AGENTS guidance rather than hard pre-execution interception. That distinction matters when comparing it to other harnesses.

## What OMX Is As a Harness

The repo consistently describes Codex as the execution engine and OMX as a workflow/runtime layer around it. The user-facing README says OMX keeps Codex as the engine while adding better prompts, workflows, and runtime help, plus durable `.omx/` storage for plans, logs, memory, and state.

Key evidence:
- [README.md](/Users/kenjipcx/coding-harness/oh-my-codex/README.md)
- [AGENTS.md](/Users/kenjipcx/coding-harness/oh-my-codex/AGENTS.md)

The practical control-plane split looks like this:

- Execution engine: Codex CLI
- Harness brain: root `AGENTS.md`
- Reusable specialist surfaces: `prompts/*.md`
- Reusable workflow surfaces: `skills/*`
- Persistent runtime substrate: `.omx/`
- Long-running control glue: installed hooks and tmux/worktree runtime

That is why OMX feels closer to an agent runtime shell than to a collection of prompts.

## The Autonomy Model

OMX's autonomy model is explicit, not implied.

At the top of [AGENTS.md](/Users/kenjipcx/coding-harness/oh-my-codex/AGENTS.md), the harness tells the agent to:
- execute tasks to completion without asking permission
- try alternatives when blocked
- use native subagents when throughput improves

That autonomy is then narrowed by operating rules:
- prefer the lightest path that preserves quality
- verify before claiming completion
- proceed automatically only on clear, low-risk, reversible steps
- use evidence over assumption

This same posture is reinforced at the role-prompt level. For example:
- [prompts/executor.md](/Users/kenjipcx/coding-harness/oh-my-codex/prompts/executor.md) explicitly says "Explore, implement, verify, and finish"
- it requires fresh verification output before completion
- it mandates retrying materially different approaches before escalating

So OMX autonomy is best described as:

> aggressive execution bounded by verification discipline

## The Orchestration Model

OMX orchestration is layered rather than monolithic.

### 1. Default mode: direct execution

The default posture is to work directly and only delegate when it materially improves safety, quality, or speed.

Evidence:
- [AGENTS.md](/Users/kenjipcx/coding-harness/oh-my-codex/AGENTS.md)

### 2. Bounded native subagents

The harness supports native subagents for bounded in-session parallel work. The child-agent protocol in `AGENTS.md` constrains:
- role choice
- prompt reading
- bounded task shape
- verifiable outputs
- concurrency caps

### 3. Heavy mode: durable team runtime

The big orchestration differentiator is `omx team`.

The team skill explicitly draws a line between:
- native subagents for bounded in-session fanout
- `omx team` for durable tmux workers, shared state, worktrees, and long-running coordination

Evidence:
- [skills/team/SKILL.md](/Users/kenjipcx/coding-harness/oh-my-codex/skills/team/SKILL.md)
- [src/team/runtime.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime.ts)
- [src/cli/team.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/cli/team.ts)

That distinction is load-bearing. OMX does not pretend all parallelism is the same.

## Prompts, Skills, and Routing

OMX is not special because it has prompts. Lots of harnesses have prompts.
It is more interesting because prompt/skill routing is partly implemented in code.

### What is implemented

`AGENTS.md` defines keyword-triggered workflows such as:
- `ralph`
- `plan this`
- `deep interview`
- `team`
- `cancel`
- `fix build`
- `code review`
- `security review`

These are backed by:
- [src/hooks/keyword-registry.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/hooks/keyword-registry.ts)
- [src/hooks/keyword-detector.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/hooks/keyword-detector.ts)

The detector handles:
- explicit `$skill` capture
- prompt invocation suppression in some cases
- intent gating for ambiguous trigger words like `team` and `swarm`
- persistence of active skill state

### The important caveat

This routing layer is real, but it is not the same as hard pre-submit enforcement.
The repo itself makes clear that much of OMX's logic is now embedded into AGENTS/prompt surfaces rather than being fully enforced in a hard pre-execution gate.

This means:
- keyword/state tracking is implemented
- workflow policy is often still advisory text given to the model

That distinction is important when judging robustness.

## Runtime-Enforced vs Prompt-Enforced

This is the most important boundary in the repo.

## Runtime-enforced parts

### 1. Setup installs real runtime behavior

`omx setup` builds Codex config that installs the notify hook and stronger default instruction surfaces.

Evidence:
- [src/config/generator.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/config/generator.ts)
- [src/cli/setup.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/cli/setup.ts)

### 2. Notify hook is genuinely load-bearing

The notify hook is not cosmetic. It:
- increments active mode iterations
- auto-expands Ralph when still progressing
- writes HUD state
- updates team heartbeats
- records active skill state
- drains pending team dispatch
- nudges leaders/workers when stale

Evidence:
- [src/scripts/notify-hook.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook.ts)

This is one of the clearest "runtime, not just prompt" parts of OMX.

### 3. State writes are validated and atomic

Mode state is managed by a real MCP state server with:
- scope resolution
- write locks
- atomic file writes
- per-mode validation
- Ralph normalization

Evidence:
- [src/mcp/state-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-server.ts)
- [src/mcp/state-paths.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-paths.ts)
- [src/ralph/contract.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/ralph/contract.ts)

### 4. Team runtime is a real coordination system

Team mode includes real machinery for:
- task claims and leases
- mailboxes
- dispatch queues
- locks
- monitor snapshots
- worker identities
- shutdown requests and acks
- worktree provisioning
- session/topology guards

Evidence:
- [src/team/runtime.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime.ts)
- [src/team/state/tasks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/tasks.ts)
- [src/team/state/locks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/locks.ts)
- [src/team/worktree.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/worktree.ts)

## Prompt-enforced or mostly prompt-enforced parts

### 1. Much orchestration policy still lives in instructions

Rules like:
- broad-request handling
- lightest-path routing
- many workflow gates
- some "must do X before Y" rules

are primarily enforced because the model is told to do them in `AGENTS.md` and prompts.

### 2. Ralph loop semantics are only partly in code

Ralph has real code for:
- bootstrapping
- canonical artifact creation
- state validation
- mode start/update/cancel

But the actual persistence semantics:
- keep going until done
- architect verification
- deslop pass
- repeated fix/re-verify loops

still depend heavily on [skills/ralph/SKILL.md](/Users/kenjipcx/coding-harness/oh-my-codex/skills/ralph/SKILL.md), not on a strong runtime supervisor.

So Ralph is not "fake," but it is not fully code-supervised either.

## Scoped State Reality Check

OMX's session-scoped state is real, but intentionally porous.

### What is real

State paths can resolve into:
- root scope: `.omx/state/`
- session scope: `.omx/state/sessions/{session_id}/`

Writes target the resolved effective scope.

Evidence:
- [src/mcp/state-paths.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-paths.ts)
- [src/mcp/state-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-server.ts)

### What is intentionally compatibility-blurred

Reads often use fallback precedence:
- explicit session first, sometimes root fallback
- implicit current session first, then root fallback
- root only when no session exists

This means:

> write isolation is real, but read/status/cancel visibility is compatibility-aware rather than strictly isolated

That is a pragmatic design, but it is not a hard isolation boundary.

## How OMX Handles Long-Running Work

OMX has two main long-running paths:

### 1. Ralph

Ralph is the persistent single-owner loop:
- stateful
- retry-oriented
- verification-heavy
- architect-signoff-oriented

Its real code layer includes:
- `omx ralph` bootstrap
- canonical PRD/progress artifacts
- mode-state writes
- cancellation/terminalization

Evidence:
- [src/cli/ralph.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/cli/ralph.ts)
- [src/ralph/persistence.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/ralph/persistence.ts)
- [src/ralph/contract.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/ralph/contract.ts)

But again, the durable execution semantics are still partly prompt-driven.

### 2. Team mode

Team mode is the stronger long-running runtime story.

Concrete durability mechanisms include:
- tmux preconditions
- one-team-per-leader-session guards
- clean-leader-workspace requirement before worker worktrees
- per-worker worktree isolation
- readiness polling
- inbox persistence
- task leases/claims
- monitor-driven reclamation and progress checks
- ack-aware shutdown

Evidence:
- [src/team/runtime.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime.ts)
- [src/team/worktree.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/worktree.ts)
- [src/team/state/tasks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/tasks.ts)
- [src/team/state/locks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/locks.ts)

This is the most runtime-heavy and most unusual part of OMX.

## Verification Model

Verification is a harness invariant in OMX.

It shows up in three layers:

### 1. Root contract

`AGENTS.md` requires:
- identify proof
- run verification
- read the output
- continue iterating if verification fails

### 2. Role prompt contract

`executor.md` requires:
- diagnostics
- tests
- build/typecheck where applicable
- fresh output before claiming completion

### 3. Workflow contract

`skills/ralph` adds:
- mandatory verification
- architect verification
- optional deslop pass
- post-deslop re-verification

### 4. Runtime helper

`src/verification/verifier.ts` encodes a structured evidence model and can heuristically check whether a completion summary actually contains verification evidence.

This is a meaningful differentiator:

> OMX tries to make completion evidence-bearing, not confidence-bearing

## Recovery, Cancel, and Resume

OMX treats recovery as a first-class concern.

### Session lifecycle

There is a session manager that:
- writes `session.json`
- checks stale sessions by PID identity
- archives session history
- resets session metrics/HUD state on launch

Evidence:
- [src/hooks/session.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/hooks/session.ts)

### Cancel

The cancel workflow is scope-aware and mode-aware. It aims to:
- terminalize Ralph cleanly
- leave unrelated sessions alone
- handle team shutdown in staged fashion

Evidence:
- [skills/cancel/SKILL.md](/Users/kenjipcx/coding-harness/oh-my-codex/skills/cancel/SKILL.md)
- [src/cli/index.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/cli/index.ts)

### Team resume/shutdown

Team mode exposes:
- `status`
- `resume`
- `shutdown`

The runtime keeps enough state to attempt resumption, though some resume paths are weaker if live process handles are gone.

Evidence:
- [src/team/runtime.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime.ts)
- [src/cli/team.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/cli/team.ts)

## What Makes OMX Special

What makes OMX genuinely differentiated is not "prompts, skills, agents."
Many harnesses have those.

What is more distinctive is the attempt to turn Codex into a durable operating environment with three coordinated layers:

### 1. A governing contract layer

`AGENTS.md` is explicitly treated as the orchestration brain, with prompts subordinate to it.

### 2. A persistent runtime layer

`.omx/` is not just scratch notes. It is the durable substrate for:
- mode state
- plans
- logs
- team state
- project memory
- notepad

### 3. A turn-by-turn control loop

The notify hook updates state and runtime signals continuously during use.

### 4. An externalized multi-agent runtime

Team mode externalizes coordination into:
- tmux
- worktrees
- claims
- mailboxes
- dispatch
- locks
- monitoring
- shutdown logic

That is the strongest basis for calling OMX a harness runtime rather than just an instruction bundle.

## Load-Bearing vs Optional Components

## Load-bearing

- Root `AGENTS.md`
- role prompt split, especially executor vs architect
- notify-hook runtime
- `.omx/` state and memory model
- MCP state/memory servers
- verification model
- team runtime for durable externalized orchestration

## Optional or additive

- HUD
- OpenClaw integration
- hook plugins/extensibility
- `explore`
- `sparkshell`

Important nuance:
- `team` is core to OMX's strongest differentiation
- but it is optional for ordinary single-session use

## Justified Complexity vs Fragile Complexity

## Justified complexity

These look genuinely load-bearing:

- persistent state and scope handling
- notify-hook lifecycle upkeep
- task/mailbox/dispatch locking for team mode
- verification as a hard harness norm
- worktree isolation for durable multi-worker work

Without these, OMX loses much of its runtime identity.

## Fragile or likely-to-stale complexity

These look more vulnerable:

- prompt-heavy orchestration semantics that are described as if enforced but often remain advisory
- broad workflow taxonomy and naming sprawl
- tmux/operator machinery that may become less necessary as native agent runtimes improve
- auto-integration git strategies in team mode

The biggest risk area in the repo is team auto-integration:
- auto-commit
- merge with `-X theirs`
- cherry-pick with `-X theirs`
- rebase with `-X ours`

This is ambitious and useful, but also the clearest place where runtime power introduces operational risk.

## Comparison-Oriented Bottom Line

Compared with Codexter, OMX is:
- more runtime-heavy
- more orchestration-opinionated
- stronger on durable multi-agent coordination
- more complex
- more exposed to drift where semantics still live in prompts instead of hard enforcement

If Codexter wants to borrow from OMX, the most valuable lesson is not:

> copy more prompts, skills, and modes

It is:

> decide which guarantees should be real runtime guarantees, then build only the minimum state/hook/control-plane needed to make those guarantees true

## Practical Takeaways for Harness Design

If I reduce the OMX lessons to a short list:

1. A harness becomes more serious when it owns durable state, not just prompts.
2. Long-running autonomy improves when there is a hook/runtime layer updating progress and health signals between turns.
3. Externalized multi-agent coordination needs explicit task/mailbox/claim/lock semantics to be trustworthy.
4. Verification must be treated as a system invariant, not a stylistic preference.
5. Prompt-surface complexity can easily outgrow its value if runtime enforcement does not keep pace.

## Open Questions

These still merit deeper inspection if you want an even stronger comparison:

- Is there any true pre-submit enforcement path left for AGENTS-derived routing, or is most heavy-mode gating still advisory text plus post-turn state tracking?
- How often does root-state fallback create misleading session views in real use?
- Are the team auto-merge/rebase strategies production-proven or still effectively experimental despite living in runtime code?
- How much of Ralph's "architect verification" is machine-checkable versus still prompt obligation?
- If notify-hook is disabled or missing, which OMX features degrade softly and which stop working correctly?

## Sources Reviewed

Primary repo surfaces:
- [README.md](/Users/kenjipcx/coding-harness/oh-my-codex/README.md)
- [AGENTS.md](/Users/kenjipcx/coding-harness/oh-my-codex/AGENTS.md)
- [prompts/executor.md](/Users/kenjipcx/coding-harness/oh-my-codex/prompts/executor.md)
- [skills/team/SKILL.md](/Users/kenjipcx/coding-harness/oh-my-codex/skills/team/SKILL.md)
- [skills/ralph/SKILL.md](/Users/kenjipcx/coding-harness/oh-my-codex/skills/ralph/SKILL.md)
- [skills/cancel/SKILL.md](/Users/kenjipcx/coding-harness/oh-my-codex/skills/cancel/SKILL.md)

Key implementation files:
- [src/hooks/keyword-registry.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/hooks/keyword-registry.ts)
- [src/hooks/keyword-detector.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/hooks/keyword-detector.ts)
- [src/hooks/session.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/hooks/session.ts)
- [src/scripts/notify-hook.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/scripts/notify-hook.ts)
- [src/mcp/state-paths.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-paths.ts)
- [src/mcp/state-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/state-server.ts)
- [src/mcp/memory-server.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/mcp/memory-server.ts)
- [src/verification/verifier.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/verification/verifier.ts)
- [src/cli/setup.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/cli/setup.ts)
- [src/config/generator.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/config/generator.ts)
- [src/cli/ralph.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/cli/ralph.ts)
- [src/ralph/persistence.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/ralph/persistence.ts)
- [src/ralph/contract.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/ralph/contract.ts)
- [src/cli/team.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/cli/team.ts)
- [src/team/runtime.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/runtime.ts)
- [src/team/state/tasks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/tasks.ts)
- [src/team/state/locks.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/state/locks.ts)
- [src/team/worktree.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/team/worktree.ts)
- [src/openclaw/index.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/openclaw/index.ts)
- [src/hud/index.ts](/Users/kenjipcx/coding-harness/oh-my-codex/src/hud/index.ts)
