# Harness Techniques

Date: 2026-04-09

## Goal

Catalog the main techniques Farplane uses today and the highest-value
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
- `docs/MEMORY.md`, `docs/TROUBLES.md`, and `docs/LESSONS.md`
- `docs/features/registry.jsonl`
- `docs/sources/registry.jsonl`

## Implemented Techniques

### Intake and planning

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| `AGENTS.md` as a map, not an encyclopedia | Implemented | root `AGENTS.md`, `templates/global/AGENTS.md`, `docs/specs/harness-engineering-doctrine.md` | Keeps top-level instructions short and points agents toward deeper sources of truth | coverage depends on docs staying discoverable and current |
| Harness-engineering routing doctrine | Implemented | `docs/specs/harness-engineering-doctrine.md`, root `AGENTS.md` | Gives one standard question set for deciding whether a change belongs in policy, specs, skills, subagents, hooks, ticket contracts, validators, or tools | intentionally Farplane-first; generalization should wait until the doctrine proves durable |
| Default `answer | plan | act` routing plus complaint recovery | Implemented | `templates/global/AGENTS.md`, root `AGENTS.md`, `docs/MEMORY.md` | Makes direct asks default to action, keeps explicit planning as a separate mode, and treats complaint-shaped missed-work follow-ups as recovery-first instead of literal Q&A | nuanced phrasing still depends on nearby recovery surfaces staying aligned |
| `ARCHITECTURE.md` as the top-level system map | Implemented | `ARCHITECTURE.md`, `README.md`, `docs/specs/README.md` | Gives one current-state architecture entrypoint between the short `AGENTS.md` map and the deeper specs/skills | stays useful only if it remains map-like and current-state-first |
| Repo docs as the system of record | Implemented | `docs/`, tickets, root `AGENTS.md`, `README.md` | Makes intent, plans, and constraints visible to agents instead of hiding them in chat | some knowledge still lives in research notes or discussion before promotion |
| Discovery funnel before execution | Implemented | `skills/brainstorm`, `skills/deep-interview`, `skills/prd`, `README.md` | Pushes ambiguity reduction ahead of build work while keeping one public brainstorm surface that can branch into structured decomposition when needed | still depends on operator choosing the right intake skill |
| Post-system-design agent testability planning | Implemented | `skills/agent-testability-plan`, `docs/specs/agent-testability-surfaces.md`, `skills/spec-to-ticket`, `skills/impl-plan` | Turns system design into reusable control accelerators, state probes, coordination views, and proof surfaces before later ticket/build planning has to guess them | still needs broader rollout and concrete follow-up tickets to prove the doctrine across more repos |
| Autonomy Readiness surfaced before execution | Implemented | `skills/deep-init-project`, `skills/prd`, `skills/spec-to-ticket`, `tickets/templates/ticket.md`, `skills/review` | Forces missing inputs, permissions, compute, tools, QA risks, and human gates to be named before long-running or `$ralph` runs discover them late | useful only when tickets keep readiness concrete instead of decorative |
| Spec-first before ticket execution | Implemented | `docs/specs/spec-first-execution-loop.md`, `README.md` | Keeps execution downstream of clarified specs | broad spec quality still determines downstream ticket quality |
| Symphony-style spec authoring contract | Implemented | `docs/specs/spec-authoring-contract.md`, `skills/deep-system-design`, `skills/spec-to-ticket`, `skills/impl-plan` | Gives complex runtime/service specs explicit depth, domain model, state, config, failure, observability, and conformance sections while keeping PRDs and tickets lighter | useful only when applied selectively; small tickets should not inherit service-runtime ceremony |
| Ticketization with proof/testability front-loaded | Implemented | `skills/spec-to-ticket`, `tickets/templates/ticket.md` | Converts intent into executable work with proof expectations early | ticket quality varies with planning rigor |
| Board, compute, and invocation doctrine | Implemented | `docs/specs/invocation-and-adapters.md`, `WORKFLOW.md`, `skills/farplane-invocation` | Keeps Codex, Farplane, boards, explicit invocation, compute targets, and ProofPackets in one ownership model so future adapter work does not drift | local filesystem and local compute only; external adapters, background scheduling, cloud execution, and parallel dispatch stay deferred until real project pressure justifies them |
| Feature-gap research before implementation planning | Implemented | `skills/research#research:gap`, `skills/impl-plan`, `tickets/templates/ticket.md` | Grounds missing or parity-driven feature work in comparable apps, codebases, and official docs so tickets say what a production-grade version actually needs | depends on the available research tools and disciplined use of real comparables instead of intuition |
| External parity research before local scoping | Implemented | `skills/research#research:parity`, `skills/research#research:gap`, `skills/functional-ui` | Grounds "what do peers include?" questions in comparable products, official docs, standards, and open-source repos before the work collapses into repo-specific scope | depends on good source selection and on keeping parity targets proportional instead of importing every adjacent premium feature |
| Best-of-worlds synthesis | Implemented | `skills/best-of-worlds`, `skills/advise` | Lets agents compare a provided set of projects/repos/blogs, extract transferable features, discover metrics, and make adopt/adapt/reject/defer calls before implementation | depends on source quality and on agents recording decisions instead of copying every attractive feature |
| Structured feature registry and source scouting | Implemented | `docs/features/registry.jsonl`, `docs/features/README.md`, `skills/harness-scout`, `experiments/harness-scout` | Gives source-ingestion passes stable feature IDs, dedupe, provenance, local match evidence, decision matrices, and manual scorecards before opening tickets | manual scorecards are judgment aids, not scientific benchmarks; no cron, feed polling, or async Codex benchmark runner yet |
| Meta-harness automation map | Implemented | `docs/specs/harness-techniques.md`, `docs/specs/self-improvement-contracts.md`, `docs/features/registry.jsonl`, `docs/skills/registry.jsonl`, `skills/skill-maintenance` | Shows how Farplane tracks supported harness features, skill package inventory, skill maintenance, source ingestion, behavior tests, gap analysis, review, and durable memory as one self-growing loop | broad skill feature adoption remains manual/on-contact; current support is cataloged through feature rows and maintenance checks |
| Filesystem lifecycle and drain routing | Implemented | `docs/specs/filesystem-lifecycle.md`, `ARCHITECTURE.md`, `docs/features/registry.jsonl` | Gives agents one router for which durable file to write, read, drain, archive, or delete without replacing owner docs | still relies on agents following owner docs for exact local rules |
| Frontend skill topology | Implemented | `skills/frontend-craft`, `skills/functional-ui`, `skills/visual-design`, `skills/landing-page`, `skills/frontend-design` | Keeps frontend work routed by job: implementation orchestration, UX/workflow redesign, visual taste/system direction, one-page/scrolltelling planning, and app-UI implementation references | depends on agents respecting the wrapper-plus-granular routing instead of treating every UI ask as styling |
| Generated asset skill topology | Implemented | `skills/image-generation`, `skills/video-generation`, `skills/remotion-render`, installed `imagegen` | Keeps image and video assets as category-level routers with provider details in references, separates Remotion code-to-video from model-native video, and ties frontend-bound media back to asset provenance plus QA | external CLI runs are spend-sensitive and model schemas can change, so agents must capability-gate with the owning skill |
| Metric-driven autoresearch sessions | Implemented | `skills/autoresearch-plan`, `skills/autoresearch-exec`, `skills/self-improve` | Gives agents one artifact-backed way to plan, run, and resume keep/discard improvement loops against a mechanical metric | v1 is skill-and-script based, not a full dashboard or extension runtime |
| Gated skill opportunity applier | Implemented | `bin/capture_user_turn.py`, `bin/stop_hook.py`, `bin/user_turn.py`, `agents/skill-opportunity-applier.toml`, `.farplane/state/self-improve/` | Lets the harness turn recent formulas, recipes, cheatsheets, and repeated operator preferences into bounded skill updates or new skill packages | opt-in for applier launches; writes are bounded to `skills/**` and future benchmark/rollback work remains a follow-up |
| Behavior correction and harness optimization loop | Implemented | `skills/gap-analysis`, `skills/harness-advisor`, `skills/optimize-harness`, `skills/eval`, `docs/specs/self-improvement-contracts.md`, `docs/LESSONS.md`, `experiments/hardcases/` | Turns observed versus expected behavior into a gap packet, harness placement recommendation, eval/hardcase seed, implementation route, proof loop, and durable lesson when useful | current loop is skill-and-artifact driven; it does not train models, run hidden background searches, or auto-apply broad harness migrations without proof |
| Project-level system prompt eval suite | Implemented | `.farplane/evals/tasks/harness_tasks.json`, `skills/eval`, `templates/global/AGENTS.md` | Turns always-loaded behavior such as grounding, advice routing, act/holdback, recursive skill todos, whole-thread topic ledgers, and hardcase eval capture into runnable regression tasks | current runner judges final answer/task artifacts; full child-agent traces need `agent-behavior-test` or `agent-qa-test` |
| Whole-thread topic ledger and split discipline | Implemented | `templates/global/AGENTS.md`, `.farplane/evals/tasks/harness_tasks.json` | Keeps long chats from losing original objectives by listing root topics, tangents, current focus, and thread-split candidates before answering substantial multitopic turns | prompt/eval enforced rather than mechanically checked on every chat response |
| Validator-triggered hardcase capture | Implemented | `bin/check_skill_todo_tiers.py`, `skills/skill-maintenance/scripts/check_skills.py`, `experiments/hardcases/` | Makes deterministic skill-contract violations leave deduplicated hardcase seeds instead of disappearing after the local fix | writes data artifacts only; it does not auto-fix or create runnable eval rows |
| Skill judgement questions | Implemented | `skills/skill-creator`, `skills/advise`, `skills/best-of-worlds` | Gives skills a declared list of ambiguity and metric-selection questions that should route through judgement instead of hidden intuition | existing skills adopt the pattern opportunistically; not every older skill has its own questions yet |
| Skill `SKILL.md` checklists as default anti-forgetting scaffolds | Implemented | `templates/global/AGENTS.md`, `skills/*/SKILL.md checklists`, `docs/MEMORY.md` | Gives instruction-following models an explicit ordered checklist during repeated workflows instead of relying on implied steps or chat-local mini-plans | works only when the active skill package keeps its checklist aligned with the live contract |
| Tiered skill dependency loading plus Tier 0 phases | Implemented | `templates/global/AGENTS.md`, `docs/skills/system.md`, `skills/plan`, `skills/reference-grounding`, `skills/research`, `skills/*/SKILL.md checklists` | Keeps lifecycle phases in the universal Tier 0 protocol while numeric skill tiers describe capability ownership; `plan` is a planning prompt-template for todo composition and proof-bearing handoff, while `execute` remains a compatibility wrapper rather than a new skill dependency | still depends on each skill maintaining accurate Markdown links, signatures, phase contracts, and method anchors |
| Unified per-ticket planning via `impl-plan` | Implemented | `skills/impl-plan`, `docs/specs/spec-first-execution-loop.md` | Keeps planning bounded to one work package while keeping approval-first planning and consensus challenge in one public surface | default vs consensus mode still needs tight examples so richer detail does not become policy bloat |

### Execution and orchestration

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Ticket as durable task memory | Implemented | root `AGENTS.md`, `tickets/README.md`, ticket template | Reduces dependence on transcript memory | only as good as ticket writeback discipline |
| Goal crafting for native `/goal` commands | Implemented | `skills/goal-crafter`, `docs/specs/invocation-and-adapters.md` | Turns fuzzy operator intent into a paste-ready Goal with outcome, verification, constraints, boundaries, iteration policy, and blocked stop condition | skill-only preparation surface; native Goal mode owns lifecycle behavior |
| Work Admission via `$work` | Implemented | `skills/work`, `skills/goal-crafter`, `docs/specs/spec-first-execution-loop.md`, `docs/specs/invocation-and-adapters.md` | Classifies one request, ticket, ticket batch, board-selected unit, epic, or metric loop before choosing Goal, compute, planning, proof, testability, and downstream skill | admission and docs only; no daemon, true parallel Ralph, cloud launcher, or scheduler ships here |
| Batch testability ledger | Implemented | `skills/work`, `skills/batch-work`, `skills/ralph`, `tickets/templates/ticket.md` | Lets solo-local batches share setup and regression checks while preserving per-ticket proof rows and blocker attribution | depends on agents maintaining the ledger and not batching unrelated/risky tickets |
| Single-ticket orchestration via `$impl` | Implemented | `skills/impl`, `docs/specs/spec-first-execution-loop.md`, `README.md` | Makes one ticket the execution unit and keeps orchestration visible | no durable multi-ticket dispatcher yet |
| Ticket-scoped isolated checkout workflow | Implemented | `skills/pr-runtime`, `bin/ticket_runtime.py`, `docs/specs/invocation-and-adapters.md` | Gives PR follow-up and concurrent writers one explicit isolated-checkout, runtime-launch, and QA-target workflow instead of ad hoc worktree usage | remains local-first and intentionally avoids becoming a full dispatcher or cloud runtime |
| Farplane invocation contract | Implemented | `WORKFLOW.md`, `skills/farplane-invocation`, `bin/farplane_invocation.py`, `docs/specs/invocation-and-adapters.md` | Gives normal Codex and future external workers one shared request/result seam: envelope in, filesystem work item normalized, compute selected, existing skill route returned, proof packet out | filesystem adapter and local compute only; no daemon, polling, Linear adapter, or cloud execution |
| Explicit worker-lane split | Implemented | `skills/impl`, `docs/specs/spec-first-execution-loop.md` | Separates builder, reviewer, QA, and evidence-check responsibilities | actual staffing and reuse patterns are still evolving |
| Ephemeral orchestrator, visible worker lanes | Implemented | `skills/impl`, `docs/specs/spec-first-execution-loop.md` | Avoids a hidden forever-orchestrator and keeps runs legible | tmux/runtime surfaces are still prototype-weight |
| Same-ticket re-entry via `$impl` + Stop hook | Partial | `skills/impl`, `docs/specs/spec-first-execution-loop.md`, `README.md` | Keeps working on one selected ticket until proof exists instead of stopping on partial progress | runtime/code migration still has some compatibility aliases, but retired prototype specs are gone |
| Goal-backed board context via `$ralph` | Implemented | `skills/ralph`, `skills/work`, `skills/ralph/scripts/select_next_ticket.py`, `tickets/README.md`, `docs/specs/spec-first-execution-loop.md` | Lets an operator drain prepared filesystem tickets by selecting eligible work units and handing them to `$work` while Goal owns the durable stop condition | intentionally serial; no worktree leases, merge queue, external board adapters, or parallel N-agent dispatch yet |

### Review, QA, and proof

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Three-layer review gate: QA -> reviewer -> Stop hook | Implemented | `docs/specs/review-gates.md`, `skills/review`, `hooks.json`, `bin/stop_hook.py` | Makes evidence gathering, quality judgment, and continuation separate decisions | normalized scoring is specified more clearly than it is fully enforced |
| QA separated from implementor | Implemented | `agents/qa-tester.toml`, `docs/specs/review-gates.md` | Reduces self-approval and gathers independent evidence | strongest for UI/browser work today |
| Evidence-check as a separate skepticism lane | Implemented | `docs/specs/spec-first-execution-loop.md`, `skills/impl` | Catches overconfident QA and weak artifacts | dedicated evidence-check implementation is still light |
| Rubric-driven review | Implemented | `skills/review`, `docs/review/rubrics/*`, `docs/specs/review-gates.md` | Prevents “looks fine” review and pushes explicit pass/revise/block outputs | consistent write-back across all work types still needs more use |
| Ticket artifact-first completion gate | Implemented | `tickets/templates/ticket.md`, `docs/specs/review-gates.md`, `docs/MEMORY.md` | Prevents checklist theater or stale evidence from counting as completion | depends on each active ticket linking fresh, traceable evidence artifacts |
| Visual QA as a judgment-only layer | Implemented | `skills/visual-qa`, `agents/qa-tester.toml` | Keeps UI judgment separate from browser driving and implementation | depends on strong ticket contracts and good evidence capture |
| Testability instrumentation as planned work | Implemented | `skills/spec-to-ticket`, `agents/qa-tester.toml` | Treats missing deterministic hooks as a planning failure, not a QA surprise | instrumentation quality varies by ticket |
| Application UI made legible to the agent | Implemented | `skills/agent-browser`, `agents/qa-tester.toml`, `skills/visual-qa` | Lets agents inspect screenshots, DOM state, and browser behavior directly instead of relying on prose | stronger than before, but not yet paired with a full local observability loop |

### Memory, progress, and control surfaces

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Durable memory split by purpose | Implemented | `docs/HISTORY.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, `docs/LESSONS.md`, root `AGENTS.md` | Separates change log, invariants, raw repeated misses, and distilled lessons | relies on disciplined promotion/writeback |
| Progressive disclosure of context | Implemented | short `AGENTS.md`, `ARCHITECTURE.md`, `docs/specs/*`, skill references, tickets | Starts agents from a small stable entry point and teaches where to look next | structural entrypoints are checked, but narrative doc quality still needs active audit |
| Mechanical harness invariant checks | Implemented | `bin/check_harness_invariants.py`, `tickets/scripts/check_ticket_metadata.py`, `AGENTS.md`, `docs/specs/invocation-and-adapters.md`, `tickets/README.md` | Backstops a few repeated repo-critical rules mechanically instead of relying only on prompt memory | intentionally narrow; it catches high-signal boundary drift, not every prose or architecture mistake |
| Mechanical knowledge-base entrypoint checks | Implemented | `bin/check_doc_parity.py`, `docs/specs/doc-governance.md`, `README.md`, `ARCHITECTURE.md`, `docs/specs/README.md`, `tickets/README.md` | Keeps the top-level knowledge-base entry surfaces linked and catches stale queue claims without over-linting all prose | intentionally narrow; it does not replace narrative document review |
| Doc-governance workflow for narrative drift | Implemented | `docs/specs/doc-governance.md`, `docs/specs/README.md` | Gives flexible docs a repeatable audit path without requiring brittle substring validators for every story change | still depends on humans running the audit loop; no recurring maintainer agent yet |
| Stop-hook continuation and judgment | Implemented | `hooks.json`, `bin/stop_hook.py`, `agents/orchestrator.toml`, `agents/completion-reviewer.toml` | Gives visible turn-boundary continuation logic instead of pure transcript intuition | continuation policy is still being simplified and hardened |
| Current-turn intent relevance gate | Implemented | `bin/capture_user_turn.py`, `bin/stop_hook.py`, `docs/specs/context-and-handoff-policy.md`, `docs/MEMORY.md` | Keeps continuation and completion decisions anchored to the user's current ask instead of stale worker momentum | degraded fallback still exists when input-hook capture is missing |
| Explicit ticket selectors outrank ambient state | Implemented | `docs/MEMORY.md`, `bin/stop_hook.py`, `docs/HISTORY.md` | Prevents stale run state from hijacking the wrong ticket | still mainly a runtime safety rule, not a full dispatcher model |
| Lightweight runtime visibility | Partial | `skills/impl/scripts/tmux_helper.py`, `README.md`, `docs/specs/invocation-and-adapters.md` | Exposes active lane/session/verdict without a heavyweight runtime plane | queue-wide runtime state remains minimal by design |

### Skills, subagents, and tools

| Technique | Status | Main surfaces | Why it matters | Current limit |
| --- | --- | --- | --- | --- |
| Skills as operational playbooks | Implemented | `skills/*`, `docs/skills/README.md`, `docs/specs/harness-engineering-doctrine.md` | Centralizes repeatable workflow detail outside root prompts | coverage still depends on which workflows have been encoded |
| On-demand skill plugin packaging | Implemented | `bin/sync_skill_plugins.py`, `bin/install_selected_skills.py`, `install.sh`, `README.md` | Lets users generate ignored repo-local plugin packages or expose selected Farplane bundles through a personal Codex marketplace without tracking duplicate plugin copies | official public Plugin Directory publishing, icons, apps, MCP servers, and hooks remain follow-up work |
| Subagents as bounded specialists | Implemented | `agents/*.toml`, `config.toml.example`, root `AGENTS.md` | Reduces context rot and enforces responsibility boundaries | some roles are richer than others; overlap remains in places |
| CLI cleanup as a delegated worker workflow | Implemented | `skills/desloppify`, `README.md`, `.gitignore` | Gives agents one explicit anti-slop execution surface with a concrete main-agent to worker handoff | depends on local Python 3.11+ plus the external `desloppify` CLI |
| External CLI delegation | Implemented | `skills/delegate-cli`, `skills/delegate-frontend`, `bin/delegate_cli_agent.py`, `templates/external-cli/*` | Lets Farplane route bounded builder work to another local coding-agent CLI while retaining ticket evidence, QA, review, and integration authority | v1 ships only the Pi/Kimi frontend profile; other CLI families need adapter/profile tickets before active use |
| MCP/tool surfaces as capability extensions | Implemented | `config.toml.example`, tool-facing skills, README setup | Extends evidence collection, docs access, browser operation, and external research | tool wiring exists, but some tools are not yet codified into stable loops |
| Tmux-backed visible lanes | Partial | `README.md`, `skills/impl/scripts/tmux_helper.py`, `docs/specs/invocation-and-adapters.md` | Makes long-running worker sessions visible and reusable | still a prototype operational surface rather than a mature dispatcher |

## Proposed Techniques and Experiments

### Highest-value next techniques

| Technique | Status | Delta from current system | Why it is promising | Suggested eval |
| --- | --- | --- | --- | --- |
| Stronger anti-self-agreement review loop | Proposed | Current system separates QA/review, but it still needs more deliberate adversarial critique and stronger refusal of weak evidence | Directly attacks “agent always agrees” and premature completion | replay one weak-proof ticket and measure false-pass reduction |
| Final “would this impress the original user?” check | Partial | Current review gates now carry an explicit completion-gate field for impressed-user judgment, but the path still needs broader use and replay coverage | Adds a user-alignment gate after implementation and QA | compare final artifacts against original ask on a recent ticket |
| Feature-taste review against neighboring features | Proposed | `visual-qa` is taste-aware, but there is no explicit “compare to surrounding product quality” loop | Helps avoid self-congratulatory UI review and local optima | use one UI change and require comparison against existing adjacent screens |
| External design-tool-first workflow for UI | Proposed | Current UI flow can delegate bounded frontend build work through `delegate-cli`, but there is still no upstream design artifact requirement | Better for higher-taste UI work than hand-authoring from CLI alone | design in an external tool, then implement against it and run visual QA |

### Structural follow-ups

| Technique | Status | Delta from current system | Why it is promising | Suggested eval |
| --- | --- | --- | --- | --- |
| Finish removing runtime compatibility aliases from code surfaces | Proposed | public execution has collapsed to `impl`, and retired prototype specs have been deleted; a few code aliases remain for older environment names and persisted state labels | Reduces naming debt without reopening execution-surface design | migrate helpers and env selectors onto the chosen neutral runtime naming |
| Parallel Ralph with N agents | Designed | serial `$ralph` can select and hand off one ticket at a time; `skills/ralph/references/parallel-ralph.md` now specifies the future lease, worktree, merge integration, stale recovery, and batch-QA contract | Promising once the design is split into implementation tickets and proven against fixture conflicts | run two independent tickets in isolated checkouts with explicit claims and a merge/release QA gate |
| Harder evidence-quality enforcement in Stop hook | Proposed | Stop-hook judgment exists, but stricter machine-readable evidence thresholds are still a direction more than a finished system | Tightens the highest-leverage harness lever: completion policy | replay smoke cases with stronger evidence-fail paths |
| One main artifact for subagent grounding | Proposed | Tickets are durable memory already, but not every loop treats one file as the strict context anchor | Reduces context rot and ambiguous handoffs | require subagents to summarize the ticket before acting on one ticket run |
| User-input-to-output impressed-user check | Partial | `last_user_turn` is already captured in runtime state and can now feed completion judgment, but the system still needs stronger rollout and evidence across more tickets | Creates a direct loop between intake and final judgment | replay recent completion cases against the saved user ask |
| Recurring doc-gardening / cleanup agent | Proposed | durable docs exist, but there is no explicit recurring documentation maintenance loop | Prevents stale rules and docs from quietly rotting | schedule one documentation-maintainer pass and measure stale-doc fixes found |
| Broader mechanical architecture and taste invariants | Proposed | Farplane now has a first narrow invariant checker, but higher-level architectural and quality constraints still rely mostly on prompts, review, and narrative docs | High leverage for keeping fast agent output coherent beyond the first root/runtime/ticket boundary checks | extend the validator set only when a repeated failure pattern proves the next rule is worth the noise |
| Agent-visible local observability stack | Proposed | The planning/doctrine step for agent testability surfaces now exists, but a generic runtime observability/helper stack for target apps does not | Would extend “agent legibility” beyond UI into performance and runtime reliability with reusable helper implementations | use the new doctrine to drive one concrete runtime/helper implementation ticket and test a performance or reliability task |

## Reading This Inventory

When deciding what to tune next:

1. start with `docs/specs/harness-engineering-doctrine.md`
2. use this file to identify whether the technique is already live or still only proposed
3. if proposed, ticket the smallest eval that can prove or kill it
4. prefer review-loop and proof changes before broader generation changes

## Self-Growing Harness Map

Farplane grows through visible registries, skills, evals, review, and durable
memory rather than one hidden autonomy loop:

```text
SelfGrowingHarness :=
  FeatureRegistry
+ SkillRegistry
+ SkillMaintenance
+ SourceIngestion
+ EvaluationAndBehaviorTests
+ GapAnalysisAndOptimization
+ ReviewAndProof
+ DurableMemory
```

The owning surfaces are:

- `docs/features/registry.jsonl`: supported harness feature catalog
- `docs/skills/registry.jsonl`: generated skill package inventory
- `skills/skill-maintenance`: bulk skill upkeep, registry sync, and
  skill-system validation
- `skills/harness-scout` and `docs/sources/registry.jsonl`: source ingestion
  before local feature adoption
- `skills/eval`, `skills/agent-behavior-test`, and `skills/agent-qa-test`:
  behavior proof and regression capture
- `skills/gap-analysis`, `skills/harness-advisor`, and
  `skills/optimize-harness`: behavior gap to placement, eval plan, and proof
  loop
- `skills/review` plus ticket proof contracts: anti-self-approval gates
- `docs/HISTORY.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, and
  `docs/LESSONS.md`: durable timeline, invariants, pain logs, and distilled
  learning

Feature rows are provenance and support records, not a substitute for tests,
tickets, or review evidence. Use `feature_refs` in skill frontmatter only for
compact `FEAT-####` handles already present in `docs/features/registry.jsonl`.

## Canonical Companion Docs

- `harness-engineering-doctrine.md` for how to decide which harness surface should own a change
- this file's Self-Growing Harness Map for how feature rows, skill inventory,
  skill maintenance, source ingestion, evals, gap analysis, review, and durable
  memory make Farplane self-growing
- `invocation-and-adapters.md` for BoardAdapter, ComputeSelector, local
  Farplane, Ralph, and future external-runner/shared-board ownership boundaries
- `spec-authoring-contract.md` for PRD/spec/ticket split, spec depth decisions,
  and conformance matrix templates
- `doc-governance.md` for structural versus narrative doc-audit policy
- `review-gates.md` for the QA/reviewer/Stop-hook split
- `spec-first-execution-loop.md` for the end-to-end execution model
- `spec-first-execution-loop.md` for `$impl` lane roles
