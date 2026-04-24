# Harness Engineering Quickstart

Date: 2026-04-07

## Goal

Give an agent a practical way to improve the harness without guessing where to
edit or changing everything at once.

This is the main idea:

- treat the harness as a set of tunable surfaces
- start with the review loop before the generator
- change one meaningful variable at a time
- run a small eval
- write the result back into tickets and durable docs

## Core Model

Use these equations as the compact mental model:

- `harness = instructions + artifacts + tools + review loop`
- `subagent = model + prompt + tool policy + owned output`
- `skill = reusable workflow + references + optional scripts/templates`
- `hook = control point that can inspect artifacts and route the next action`
- `ticket = durable task memory + proof target + progress surface`

In practice, the working specialist is often:

- `specialist behavior = subagent + invoked skill`

The review loop matters most because it decides what the system rewards. A
strong generator with a weak evaluator still drifts, ships shallow work, and
declares success too early.

## The Main Levers

### 1. Review loop

Change this first.

Use:

- `docs/specs/review-gates.md`
- `skills/review/SKILL.md`
- `agents/qa-tester.toml`
- `skills/visual-qa/SKILL.md`
- `hooks.json`
- `bin/stop_hook.py`

This surface controls:

- what evidence must exist
- who gathers evidence
- who judges quality
- when the run continues vs stops

Reach for this lever when the agent:

- says work is done too early
- ships bugs that basic QA should have caught
- gathers weak screenshots/logs and still passes
- does not improve over iterations

Default move:

1. tighten the contract for proof
2. make QA collect stronger evidence
3. make review score against explicit thresholds
4. make the Stop hook refuse weak evidence

### 2. Task shaping and execution contracts

Use:

- `AGENTS.md`
- `tickets/templates/ticket.md`
- `docs/specs/spec-first-execution-loop.md`
- `docs/specs/orchestrator-subagent-loop.md`
- `skills/impl-plan/SKILL.md`
- `skills/impl/SKILL.md`

This surface controls:

- how work gets decomposed
- what one execution unit is
- what "done" means before code is written
- how follow-up passes are routed

Reach for this lever when the agent:

- picks the wrong scope
- micro-slices coherent work into useless crumbs
- starts building before success criteria are legible
- loses the thread across long runs

Default move:

1. make the work package clearer
2. improve the acceptance criteria and proof section
3. define explicit next action and verification targets
4. keep one ticket as the unit of work unless a real blocker forces a split

### 3. Skills

Use:

- `skills/*/SKILL.md`
- skill `references/`
- skill `scripts/`
- skill `templates/`

This surface controls:

- repeatable workflow quality
- whether common tasks are done from memory or from a playbook
- whether the agent can execute a procedure the same way twice

Treat skills as the main place to centralize operational detail. Keep durable
workflow knowledge here instead of bloating root instructions or every
subagent prompt with the same procedure.

Reach for this lever when the agent:

- knows a workflow in theory but executes it inconsistently
- forgets edge cases
- repeats the same exploratory work every run
- needs a stable checklist or helper script

Default move:

1. move repeated operator guidance into one skill
2. keep the top-level skill short
3. push detail into references or scripts
4. make the skill trigger conditions explicit

### 4. Subagents

Use:

- `agents/*.toml`
- `[agents]` and `[agents.<name>]` in `config.toml.example`

This surface controls:

- role separation
- model choice
- sandbox/tool policy
- who owns which artifact

Reach for this lever when the agent:

- mixes implementation, QA, and review into one muddy pass
- accumulates context rot in long runs
- needs parallel specialists with clear ownership

Default move:

1. split only along real responsibility boundaries
2. give each subagent one job and one output
3. keep orchestration authority with the main agent
4. do not create extra roles until a failure mode clearly justifies them

### 5. Hooks

Use:

- `hooks.json`
- `bin/stop_hook.py`
- hook-role configs such as `agents/orchestrator.toml` and `agents/completion-reviewer.toml`

This surface controls:

- what happens at turn boundaries
- how verdicts are normalized
- whether the system stops, continues, blocks, or routes

Reach for this lever when the agent:

- ends after saying it will continue
- continues with the wrong ticket
- cannot turn evidence into a sane next action

Default move:

1. keep the hook small and legible
2. make it consume visible artifacts, not hidden transcript intuition
3. prefer routing and sanity checks over hidden autonomous planning

### 6. MCP and tool surface

Use:

- `[mcp_servers.*]` in `config.toml.example`
- tool-facing skills such as `agent-browser`, `documentation`, `apify`

This surface controls:

- what the agent can inspect
- what environments it can test against
- how much real evidence it can gather

Reach for this lever when the agent:

- cannot access the ground truth it needs
- writes code it cannot verify
- lacks the right browser, docs, or external-data capability

Default move:

1. add tools that improve evidence quality or task execution
2. wire them into skills before expecting consistent use
3. do not add tools just because they are available

### 7. Root instructions and local `AGENTS.md`

Use:

- root `AGENTS.md`
- nearer `AGENTS.md` files when a folder needs tighter local rules
- `PROJECT_RULES.md`
- `rules/default.rules`

This surface controls:

- global policy
- durable repo invariants
- what the agent is allowed to optimize for

Reach for this lever when the failure is truly policy-level:

- the agent repeatedly chooses the wrong priority
- the repo needs a durable invariant
- multiple workflows need the same correction

Default move:

1. prefer the smallest local rule that fixes the real failure
2. promote only stable lessons into root policy
3. avoid turning one-off preferences into global law

## What To Change First

Default harness-tuning order:

1. review loop and proof requirements
2. task shaping and sprint or ticket contracts
3. QA/testability surfaces
4. skill packaging of repeatable workflows
5. subagent role split
6. tool or MCP additions
7. root instruction rewrites

Reason:

- better evaluation changes what the whole system optimizes for
- better contracts reduce wasted work before generation starts
- better skills and subagents help only after the system knows what good looks
  like
- rewriting top-level prompts first usually creates more prose than signal

## Failure Mode -> Best Lever

| Failure mode | Change first | Why |
| --- | --- | --- |
| Agent says "done" with weak proof | review loop, Stop hook | completion policy is too weak |
| Agent builds the wrong thing | ticket/contract shaping | scope and proof were unclear |
| Agent repeats the same mistake across runs | skill or `AGENTS.md` | the lesson is not encoded durably |
| Agent gets lost in long work | subagent split, ticket writeback, hooks | context is not being externalized well |
| QA is shallow or flaky | QA skill, browser/test hooks, review gates | evidence quality is the bottleneck |
| Agent cannot verify reality | MCP/tooling | the harness lacks ground-truth access |
| Too many tiny safe edits, no ownership of hard work | planner/worker split, stronger reviewer | the coordination model rewards low-ambition work |

## Experiment Loop

Run harness experiments like engineering work, not like prompt superstition.

### 1. Pick one concrete failure

Use:

- the current ticket
- recent QA/review findings
- `docs/TROUBLES.md`
- run artifacts and hook logs

Bad target:

- "make the agent smarter"

Good target:

- "the reviewer passes weak evidence for UI tickets"
- "the builder keeps starting before the ticket defines proof"

### 2. Write a harness hypothesis

Template:

```text
Problem:
Current surface:
Hypothesis:
Single variable to change:
Expected improvement:
Eval to rerun:
```

Example:

```text
Problem: UI tickets pass with shallow evidence.
Current surface: QA + reviewer + Stop hook.
Hypothesis: Required screenshots plus an evidence adequacy threshold will force another repair pass.
Single variable to change: review-gate policy for UI work.
Expected improvement: fewer false passes.
Eval to rerun: one recent UI ticket or smoke case.
```

### 3. Change one main variable

Good:

- tighten one rubric threshold
- add one required artifact to QA
- add one missing skill script
- split one muddy subagent into builder and reviewer

Bad:

- rewrite `AGENTS.md`, multiple skills, two hooks, and tool config in one shot

### 4. Run a small eval

Prefer:

- one ticket replay
- one smoke case
- one targeted task that previously failed

Avoid:

- making several harness changes and then judging from vibes

### 5. Write back the result

Use the normal repo surfaces:

- ticket evidence and handoff
- `docs/HISTORY.md` for the durable change log
- `docs/TROUBLES.md` for repeated misses
- `docs/MEMORY.md` only when the lesson becomes a real invariant

### 6. Keep or revert based on proof

Keep a harness change only if the eval meaningfully improved:

- output quality
- proof quality
- convergence speed
- operator trust

## Codexter-Specific Defaults

For this repo, assume these defaults unless evidence says otherwise:

1. the ticket is the durable task memory
2. review-loop quality is the highest-leverage harness variable
3. QA, reviewer, and Stop hook should stay separate roles
4. subagents exist to reduce context rot and improve ownership, not to create a
   fake org chart
5. skills should hold operational detail so top-level prompts stay thin
6. hooks should route and sanity-check; they should not become a hidden planner

## Safe Autonomy Rule

When improving the harness autonomously:

1. read the nearest specs, tickets, and durable memory first
2. prefer changes that strengthen evidence and clarity
3. keep artifacts human-visible
4. avoid hidden continuation behavior unless it is explicitly part of the
   system design
5. do not claim a harness improvement without rerunning at least one concrete
   case

## Source Notes

This quickstart is aligned with:

- Anthropic, "Harness design for long-running application development":
  planner/generator/evaluator separation, negotiated sprint contracts,
  file-based handoffs, hard evaluator thresholds, and the finding that evaluator
  tuning materially improved results
- Cursor, "Scaling long-running autonomous coding":
  flat self-coordination with locks did not scale well; clearer
  planner-versus-worker role separation worked better for long-running work
- existing Codexter specs:
  `review-gates.md`, `spec-first-execution-loop.md`, and
  `orchestrator-subagent-loop.md`

Primary sources:

- https://www.anthropic.com/engineering/harness-design-long-running-apps
- https://cursor.com/blog/long-running-agents
- https://cursor.com/blog/scaling-agents
