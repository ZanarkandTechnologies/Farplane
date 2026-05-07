# Harness Techniques

Date: 2026-04-09

## Goal

Catalog the main techniques Codexter uses today and the highest-value
techniques it is likely to adopt next.

This document is the repo's current-state feature inventory first. It is not a
generic harness wishlist.

For structured feature records, provenance, source references, known limits, and
benchmark metrics, use `docs/features/registry.jsonl`. This Markdown inventory
stays the skimmable human map.

## Status Legend

- `Implemented`: real repo behavior or a documented active contract
- `Partial`: the repo has the shape, but the full loop is not yet proven end to end
- `Proposed`: a candidate technique or experiment, not current behavior

## Audit Basis

This inventory is grounded in:

- root `AGENTS.md`
- `README.md`
- `docs/specs/*`
- `tickets/README.md`
- harness skills under `skills/`
- subagent prompts under `agents/`
- `hooks.json` and `bin/stop_hook.py`
- `docs/MEMORY.md` and `docs/TROUBLES.md`
- `docs/features/registry.jsonl`

## Implemented Techniques

### Intake and planning

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| `AGENTS.md` as a map, not an encyclopedia | Implemented | root `AGENTS.md`, `docs/specs/*`, `docs/specs/harness-engineering-quickstart.md` | Keeps top-level instructions short and points agents toward deeper sources of truth | coverage depends on docs staying discoverable and current |
| Harness-engineering routing doctrine | Implemented | `docs/specs/harness-engineering-doctrine.md`, root `AGENTS.md` | Gives one standard question set for deciding whether a change belongs in policy, specs, skills, subagents, hooks, ticket contracts, validators, or tools | intentionally Codexter-first; generalization should wait until the doctrine proves durable |
| Default `answer | plan | act` routing plus complaint recovery | Implemented | `templates/global/AGENTS.md`, root `AGENTS.md`, `docs/MEMORY.md` | Makes direct asks default to action, keeps explicit planning as a separate mode, and treats complaint-shaped missed-work follow-ups as recovery-first instead of literal Q&A | nuanced phrasing still depends on nearby recovery surfaces staying aligned |
| `ARCHITECTURE.md` as the top-level system map | Implemented | `ARCHITECTURE.md`, `README.md`, `docs/specs/README.md` | Gives one current-state architecture entrypoint between the short `AGENTS.md` map and the deeper specs/skills | stays useful only if it remains map-like and current-state-first |
| Repo docs as the system of record | Implemented | `docs/`, tickets, root `AGENTS.md`, `README.md` | Makes intent, plans, and constraints visible to agents instead of hiding them in chat | some knowledge still lives in research notes or discussion before promotion |
| Discovery funnel before execution | Implemented | `skills/brainstorm`, `skills/deep-interview`, `skills/prd`, `README.md` | Pushes ambiguity reduction ahead of build work while keeping one public brainstorm surface that can branch into structured decomposition when needed | still depends on operator choosing the right intake skill |
| Post-system-design agent testability planning | Implemented | `skills/agent-testability-plan`, `docs/specs/agent-testability-surfaces.md`, `skills/spec-to-ticket`, `skills/impl-plan` | Turns system design into reusable control accelerators, state probes, coordination views, and proof surfaces before later ticket/build planning has to guess them | still needs broader rollout and concrete follow-up tickets to prove the doctrine across more repos |
| Autonomy Readiness surfaced before execution | Implemented | `skills/deep-init-project`, `skills/prd`, `skills/spec-to-ticket`, `tickets/templates/ticket.md`, `skills/review` | Forces missing inputs, permissions, compute, tools, QA risks, and human gates to be named before long-running or `$ralph` runs discover them late | useful only when tickets keep readiness concrete instead of decorative |
| Spec-first before ticket execution | Implemented | `docs/specs/spec-first-execution-loop.md`, `README.md` | Keeps execution downstream of clarified specs | broad spec quality still determines downstream ticket quality |
| Ticketization with proof/testability front-loaded | Implemented | `skills/spec-to-ticket`, `tickets/templates/ticket.md` | Converts intent into executable work with proof expectations early | ticket quality varies with planning rigor |
| Feature-gap research before implementation planning | Implemented | `skills/gap-analysis`, `skills/impl-plan`, `tickets/templates/ticket.md` | Grounds missing or parity-driven feature work in comparable apps, codebases, and official docs so tickets say what a production-grade version actually needs | depends on the available research tools and disciplined use of real comparables instead of intuition |
| External parity research before local scoping | Implemented | `skills/parity-research`, `skills/gap-analysis`, `skills/functional-ui` | Grounds "what do peers include?" questions in comparable products, official docs, standards, and open-source repos before the work collapses into repo-specific scope | depends on good source selection and on keeping parity targets proportional instead of importing every adjacent premium feature |
| Best-of-worlds synthesis | Implemented | `skills/best-of-worlds`, `skills/advise`, `docs/specs/best-of-worlds-workflow.md` | Lets agents compare a provided set of projects/repos/blogs, extract transferable features, discover metrics, and make adopt/adapt/reject/defer calls before implementation | depends on source quality and on agents recording decisions instead of copying every attractive feature |
| Structured feature registry and source scouting | Implemented | `docs/features/registry.jsonl`, `docs/features/README.md`, `skills/harness-scout`, `experiments/harness-scout` | Gives source-ingestion passes stable feature IDs, dedupe, provenance, local match evidence, decision matrices, and manual scorecards before opening tickets | manual scorecards are judgment aids, not scientific benchmarks; no cron, feed polling, or async Codex benchmark runner yet |
| Frontend skill topology | Implemented | `skills/frontend-craft`, `skills/functional-ui`, `skills/visual-design`, `skills/landing-page`, `skills/frontend-design` | Keeps frontend work routed by job: implementation orchestration, UX/workflow redesign, visual taste/system direction, one-page/scrolltelling planning, and app-UI implementation references | depends on agents respecting the wrapper-plus-granular routing instead of treating every UI ask as styling |
| Metric-driven autoresearch sessions | Implemented | `skills/autoresearch-plan`, `skills/autoresearch-exec`, `skills/self-improve`, `docs/specs/autoresearch-skill-suite.md` | Gives agents one artifact-backed way to plan, run, and resume keep/discard improvement loops against a mechanical metric | v1 is skill-and-script based, not a full dashboard or extension runtime |
| Gated skill opportunity reviewer | Implemented | `bin/capture_user_turn.py`, `bin/stop_hook.py`, `bin/user_turn.py`, `agents/skill-opportunity-reviewer.toml`, `.harness/state/self-improve/` | Lets the harness notice recent formulas, recipes, cheatsheets, skill updates, and speedup opportunities from bounded conversation windows | proposal-only and opt-in for reviewer launches; it must not auto-write shipped skills or durable docs |
| Skill judgement questions | Implemented | `skills/skill-creator`, `skills/advise`, `skills/best-of-worlds` | Gives skills a declared list of ambiguity and metric-selection questions that should route through judgement instead of hidden intuition | existing skills adopt the pattern opportunistically; not every legacy skill has its own questions yet |
| Skill `todos.md` checklists as default anti-forgetting scaffolds | Implemented | `templates/global/AGENTS.md`, `skills/*/todos.md`, `docs/MEMORY.md` | Gives instruction-following models an explicit ordered checklist during repeated workflows instead of relying on implied steps or chat-local mini-plans | works only when the active skill package keeps its checklist aligned with the live contract |
| Unified per-ticket planning via `impl-plan` | Implemented | `skills/impl-plan`, `docs/specs/spec-first-execution-loop.md` | Keeps planning bounded to one work package while keeping approval-first planning and consensus challenge in one public surface | default vs consensus mode still needs tight examples so richer detail does not become policy bloat |

### Execution and orchestration

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Ticket as durable task memory | Implemented | root `AGENTS.md`, `tickets/README.md`, ticket template | Reduces dependence on transcript memory | only as good as ticket writeback discipline |
| Bounded same-session persistence via `$loop` | Implemented | `skills/loop`, `docs/specs/runtime-surface.md`, `README.md` | Keeps short deterministic work out of ticket orchestration while staying visible and local | v1 predicates are intentionally narrow and same-session only |
| Single-ticket orchestration via `$impl` | Implemented | `skills/impl`, `docs/specs/orchestrator-subagent-loop.md`, `README.md` | Makes one ticket the execution unit and keeps orchestration visible | no durable multi-ticket dispatcher yet |
| Ticket-scoped isolated checkout workflow | Implemented | `skills/pr-runtime`, `bin/ticket_runtime.py`, `docs/specs/runtime-surface.md` | Gives PR follow-up and concurrent writers one explicit isolated-checkout, runtime-launch, and QA-target workflow instead of ad hoc worktree usage | remains local-first and intentionally avoids becoming a full dispatcher or cloud runtime |
| Explicit worker-lane split | Implemented | `skills/impl`, `docs/specs/orchestrator-subagent-loop.md` | Separates builder, reviewer, QA, and evidence-check responsibilities | actual staffing and reuse patterns are still evolving |
| Ephemeral orchestrator, visible worker lanes | Implemented | `skills/impl`, `docs/specs/orchestrator-subagent-loop.md` | Avoids a hidden forever-orchestrator and keeps runs legible | tmux/runtime surfaces are still prototype-weight |
| Same-ticket re-entry via `$impl` + Stop hook | Partial | `skills/impl`, `docs/specs/spec-first-execution-loop.md`, `README.md` | Keeps working on one selected ticket until proof exists instead of stopping on partial progress | runtime/code migration still needs to finish removing older legacy-named residue |
| Serial board draining via `$ralph` | Implemented | `skills/ralph`, `skills/ralph/scripts/select_next_ticket.py`, `tickets/README.md`, `docs/specs/spec-first-execution-loop.md` | Lets an operator drain one eligible filesystem ticket at a time while preserving `impl-plan`, `$impl`, `close-ticket`, and review as the real phase owners | intentionally serial; no worktree leases, merge queue, external board adapters, or parallel N-agent dispatch yet |

### Review, QA, and proof

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Three-layer review gate: QA -> reviewer -> Stop hook | Implemented | `docs/specs/review-gates.md`, `skills/review`, `hooks.json`, `bin/stop_hook.py` | Makes evidence gathering, quality judgment, and continuation separate decisions | normalized scoring is specified more clearly than it is fully enforced |
| QA separated from implementor | Implemented | `agents/qa-tester.toml`, `docs/specs/review-gates.md` | Reduces self-approval and gathers independent evidence | strongest for UI/browser work today |
| Evidence-check as a separate skepticism lane | Implemented | `docs/specs/orchestrator-subagent-loop.md`, `skills/impl` | Catches overconfident QA and weak artifacts | dedicated evidence-check implementation is still light |
| Rubric-driven review | Implemented | `skills/review`, `skills/review/references/*`, `docs/specs/review-gates.md` | Prevents “looks fine” review and pushes explicit pass/revise/block outputs | consistent write-back across all work types still needs more use |
| Ticket artifact-first completion gate | Implemented | `tickets/templates/ticket.md`, `docs/specs/review-gates.md`, `docs/MEMORY.md` | Prevents checklist theater or stale evidence from counting as completion | depends on each active ticket linking fresh, traceable evidence artifacts |
| Visual QA as a judgment-only layer | Implemented | `skills/visual-qa`, `agents/qa-tester.toml` | Keeps UI judgment separate from browser driving and implementation | depends on strong ticket contracts and good evidence capture |
| Testability instrumentation as planned work | Implemented | `skills/spec-to-ticket`, `agents/qa-tester.toml` | Treats missing deterministic hooks as a planning failure, not a QA surprise | instrumentation quality varies by ticket |
| Application UI made legible to the agent | Implemented | `skills/agent-browser`, `agents/qa-tester.toml`, `skills/visual-qa` | Lets agents inspect screenshots, DOM state, and browser behavior directly instead of relying on prose | stronger than before, but not yet paired with a full local observability loop |

### Memory, progress, and control surfaces

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Durable memory split by purpose | Implemented | `docs/HISTORY.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, root `AGENTS.md` | Separates change log, invariants, and repeated misses | relies on disciplined promotion/writeback |
| Progressive disclosure of context | Implemented | short `AGENTS.md`, `ARCHITECTURE.md`, `docs/specs/*`, skill references, tickets | Starts agents from a small stable entry point and teaches where to look next | structural entrypoints are checked, but narrative doc quality still needs active audit |
| Mechanical harness invariant checks | Implemented | `bin/check_harness_invariants.py`, `tickets/scripts/check_ticket_metadata.py`, `AGENTS.md`, `docs/specs/runtime-surface.md`, `tickets/README.md` | Backstops a few repeated repo-critical rules mechanically instead of relying only on prompt memory | intentionally narrow; it catches high-signal boundary drift, not every prose or architecture mistake |
| Mechanical knowledge-base entrypoint checks | Implemented | `bin/check_doc_parity.py`, `docs/specs/doc-governance.md`, `README.md`, `ARCHITECTURE.md`, `docs/specs/README.md`, `tickets/README.md` | Keeps the top-level knowledge-base entry surfaces linked and catches stale queue claims without over-linting all prose | intentionally narrow; it does not replace narrative document review |
| Doc-governance workflow for narrative drift | Implemented | `docs/specs/doc-governance.md`, `docs/specs/README.md` | Gives flexible docs a repeatable audit path without requiring brittle substring validators for every story change | still depends on humans running the audit loop; no recurring maintainer agent yet |
| Stop-hook continuation and judgment | Implemented | `hooks.json`, `bin/stop_hook.py`, `agents/orchestrator.toml`, `agents/completion-reviewer.toml` | Gives visible turn-boundary continuation logic instead of pure transcript intuition | continuation policy is still being simplified and hardened |
| Current-turn intent relevance gate | Implemented | `bin/capture_user_turn.py`, `bin/stop_hook.py`, `docs/specs/context-and-handoff-policy.md`, `docs/MEMORY.md` | Keeps continuation and completion decisions anchored to the user's current ask instead of stale worker momentum | degraded fallback still exists when input-hook capture is missing |
| Explicit ticket selectors outrank ambient state | Implemented | `docs/MEMORY.md`, `bin/stop_hook.py`, `docs/HISTORY.md` | Prevents stale run state from hijacking the wrong ticket | still mainly a runtime safety rule, not a full dispatcher model |
| Lightweight runtime visibility | Partial | `skills/impl/scripts/tmux_helper.py`, `README.md`, legacy runtime-surface spec | Exposes active lane/session/verdict without a heavyweight runtime plane | queue-wide runtime state remains minimal by design |

### Skills, subagents, and tools

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Skills as operational playbooks | Implemented | `skills/*`, `docs/specs/harness-engineering-quickstart.md` | Centralizes repeatable workflow detail outside root prompts | coverage still depends on which workflows have been encoded |
| Subagents as bounded specialists | Implemented | `agents/*.toml`, `config.toml.example`, root `AGENTS.md` | Reduces context rot and enforces responsibility boundaries | some roles are richer than others; overlap remains in places |
| CLI cleanup as a delegated worker workflow | Implemented | `skills/desloppify`, `README.md`, `.gitignore` | Gives agents one explicit anti-slop execution surface with a concrete main-agent to worker handoff | depends on local Python 3.11+ plus the external `desloppify` CLI |
| MCP/tool surfaces as capability extensions | Implemented | `config.toml.example`, tool-facing skills, README setup | Extends evidence collection, docs access, browser operation, and external research | tool wiring exists, but some tools are not yet codified into stable loops |
| Tmux-backed visible lanes | Partial | `README.md`, `skills/impl/scripts/tmux_helper.py`, legacy v2 direction notes | Makes long-running worker sessions visible and reusable | still a prototype operational surface rather than a mature dispatcher |

## Proposed Techniques and Experiments

### Highest-value next techniques

| Technique | Status | Delta from current system | Why it is promising | Suggested eval |
| --- | --- | --- | --- | --- |
| Stronger anti-self-agreement review loop | Proposed | Current system separates QA/review, but it still needs more deliberate adversarial critique and stronger refusal of weak evidence | Directly attacks “agent always agrees” and premature completion | replay one weak-proof ticket and measure false-pass reduction |
| Final “would this impress the original user?” check | Partial | Current review gates now carry an explicit completion-gate field for impressed-user judgment, but the path still needs broader use and replay coverage | Adds a user-alignment gate after implementation and QA | compare final artifacts against original ask on a recent ticket |
| Feature-taste review against neighboring features | Proposed | `visual-qa` is taste-aware, but there is no explicit “compare to surrounding product quality” loop | Helps avoid self-congratulatory UI review and local optima | use one UI change and require comparison against existing adjacent screens |
| External design-tool-first workflow for UI | Proposed | Current UI flow is CLI-agent build + QA; there is no upstream design artifact requirement | Better for higher-taste UI work than hand-authoring from CLI alone | design in an external tool, then implement against it and run visual QA |

### Structural follow-ups

| Technique | Status | Delta from current system | Why it is promising | Suggested eval |
| --- | --- | --- | --- | --- |
| Finish removing legacy runtime-named residue from runtime/code surfaces | Proposed | public execution has collapsed to `impl`, but runtime helpers, schemas, env vars, and older specs still carry older names | Reduces naming debt without reopening execution-surface design | migrate helpers, env selectors, and remaining specs onto the chosen neutral runtime naming |
| Parallel Ralph with N agents | Proposed | serial `$ralph` can select and hand off one ticket at a time, but does not own leases, worktrees, merge integration, stale-worker recovery, or batch-QA orchestration | Promising once selector correctness and single-ticket handoff prove reliable | run two independent tickets in isolated checkouts with explicit claims and a merge/release QA gate |
| Harder evidence-quality enforcement in Stop hook | Proposed | Stop-hook judgment exists, but stricter machine-readable evidence thresholds are still a direction more than a finished system | Tightens the highest-leverage harness lever: completion policy | replay smoke cases with stronger evidence-fail paths |
| One main artifact for subagent grounding | Proposed | Tickets are durable memory already, but not every loop treats one file as the strict context anchor | Reduces context rot and ambiguous handoffs | require subagents to summarize the ticket before acting on one ticket run |
| User-input-to-output impressed-user check | Partial | `last_user_turn` is already captured in runtime state and can now feed completion judgment, but the system still needs stronger rollout and evidence across more tickets | Creates a direct loop between intake and final judgment | replay recent completion cases against the saved user ask |
| Recurring doc-gardening / cleanup agent | Proposed | durable docs exist, but there is no explicit recurring documentation maintenance loop | Prevents stale rules and docs from quietly rotting | schedule one documentation-maintainer pass and measure stale-doc fixes found |
| Broader mechanical architecture and taste invariants | Proposed | Codexter now has a first narrow invariant checker, but higher-level architectural and quality constraints still rely mostly on prompts, review, and narrative docs | High leverage for keeping fast agent output coherent beyond the first root/runtime/ticket boundary checks | extend the validator set only when a repeated failure pattern proves the next rule is worth the noise |
| Agent-visible local observability stack | Proposed | The planning/doctrine step for agent testability surfaces now exists, but a generic runtime observability/helper stack for target apps does not | Would extend “agent legibility” beyond UI into performance and runtime reliability with reusable helper implementations | use the new doctrine to drive one concrete runtime/helper implementation ticket and test a performance or reliability task |

## Reading This Inventory

When deciding what to tune next:

1. start with `docs/specs/harness-engineering-quickstart.md`
2. use this file to identify whether the technique is already live or still only proposed
3. if proposed, ticket the smallest eval that can prove or kill it
4. prefer review-loop and proof changes before broader generation changes

## Canonical Companion Docs

- `harness-engineering-quickstart.md` for how to tune the harness
- `harness-engineering-doctrine.md` for how to decide which harness surface should own a change
- `doc-governance.md` for structural versus narrative doc-audit policy
- `review-gates.md` for the QA/reviewer/Stop-hook split
- `spec-first-execution-loop.md` for the end-to-end execution model
- `orchestrator-subagent-loop.md` for `$impl` lane roles
- legacy v2 direction notes for open deltas and future runtime shape
