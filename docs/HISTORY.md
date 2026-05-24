2026-03-26 11:20 -0700 | CHORE | bootstrap Codex harness repo scaffold with safe git boundaries, install flow, and docs/ticket board
2026-04-03 03:10 +0100 | FEAT | add opt-in stop-hook continuation with ticket-aware same-scope follow-up and local audio announcements
2026-04-03 03:24 +0100 | FIX | require explicit ticket resolution for assisted continuation and resolve stop-hook path via installed Codex home
2026-04-03 05:05 +0100 | CHORE | quarantine assisted continuation outside v1, remove tracked hook wiring/docs, and close the ticket-metadata foundation as documented work
2026-04-05 12:05 +0100 | CHORE | promote Ralph orchestration blueprint and greenfield/brownfield flow examples from research notes into canonical specs docs
2026-04-05 12:18 +0100 | CHORE | rewrite Ralph flow examples into a dry-run-first visual walkthrough with timelines, verdicts, and diagrams
2026-04-05 12:42 +0100 | CHORE | add Ralph phase prompt files plus run-state and judge-verdict schemas for the thin-wrapper prototype shape
2026-04-05 12:48 +0100 | FIX | remove lingering inline heredoc prompt examples so Ralph specs show only the thin-wrapper canonical handoff model
2026-04-05 13:05 +0100 | CHORE | rewrite Ralph docs into official Codex terms and simplify the top-level model to ralphplan plus ralph with QA subagents and stop-hook judging
2026-04-05 13:20 +0100 | FEAT | wire the tracked Ralph prototype toward actual stop-hook integration, add simpler ralphplan plus ralph prompts, and create a tracked experiments surface
2026-04-05 13:32 +0100 | FEAT | add a 10-case Ralph smoke eval suite, project-local hook logs, and live ~/.codex hook activation for real-session testing
2026-04-05 13:40 +0100 | CHORE | rewrite README into a high-density Ralph system story with minimal text and primary diagrams
2026-04-05 13:48 +0100 | FEAT | add brainstorm and deep-interview skills as the front-end funnel before PRD/spec/ticket work
2026-04-05 19:31 +0100 | FIX | make explicit Ralph ticket selectors override ambient current-run state and decouple smoke eval missing-evidence cases from TASK-0011 closeout
2026-04-05 22:25 +0100 | FIX | stop treating Ralph-mode prose completions without RALPH_RESULT as successful stops and add a regression check for the missing-result path
2026-04-05 23:08 +0100 | FEAT | turn Ralph tmux lanes into real interactive Codex sessions with same-pane follow-up reuse and session-id resume fallback
2026-04-05 23:32 +0100 | FEAT | add stop-hook verdict observability via tmux-visible summaries and a centralized ralph_tmux status command with hook-log fallback
2026-04-05 22:50 +0100 | FIX | make Ralph execution treat the active ticket as the default work unit instead of automatically shrinking coherent tickets into smaller tasks
2026-04-06 02:09 +0100 | FIX | emit Stop-hook systemMessage summaries and replace the vague hook status label with an explicit Ralph verdict evaluation message
2026-04-06 02:20 +0100 | CHORE | add a canonical Ralph v2 direction spec covering todo-list-first execution, future archive flow, dispatcher-v0 claims, planner simplification, and known follow-up bugs
2026-04-06 06:38 +0100 | CHORE | expand README into the full staged Ralph model across spec, ticketization, per-ticket planning, dispatch, and build/proof/review loops
2026-04-07 00:00 +0100 | CHORE | add a canonical spec-first execution-loop spec and begin queue cleanup around the newer work-package model
2026-04-07 00:00 +0100 | CHORE | archive completed and superseded tickets so the active queue only contains the current review-gates, execution-loop, and handoff-policy work
2026-04-06 06:38 +0100 | FEAT | pull the latest OMX base and add the first Codexter-to-OMX bridge exporter for ready Markdown tickets
2026-04-07 04:27 +0100 | CHORE | add a canonical harness-engineering quickstart so agents can tune AGENTS, hooks, subagents, skills, MCP/tooling, and review loops from one practical guide
2026-04-07 20:37 +0100 | CHORE | add a canonical harness-techniques inventory and README pointer so implemented versus proposed harness techniques are documented from repo truth
2026-04-08 01:48 +0100 | CHORE | fold OpenAI harness-engineering findings into the canonical techniques inventory, adding repo-legibility, progressive-disclosure, and mechanical-invariant deltas
2026-04-08 04:20 +0100 | CHORE | add ticket inspiration-source tracking, annotate active harness backlog items with the Ryan Lopopolo podcast, and queue missing CLI ergonomics and inner-loop latency tickets
2026-04-08 02:45 +0100 | CHORE | replace question-style review guidance with anchored 1-to-5 rubric definitions, migrate the live review contract into `skills/review`, and remove the legacy `code-review` skill alias
2026-04-08 04:34 +0100 | FEAT | require Review Packet gates for Ralph completion, add storyboard-grade QA evidence capture, and extend stop-hook role outputs for evidence-quality review
2026-04-08 05:19 +0100 | FEAT | capture current-turn user intent at `UserPromptSubmit`, add stop-hook relevance gating before continuation, and persist intent alignment into Ralph run state
2026-04-08 16:00 +0100 | FEAT | add a grouped runtime claim object, preserve it across lane and hook updates, and expose claim plus saved user-turn input through the canonical stop-hook read path
2026-04-08 16:58 +0100 | FIX | normalize stop-hook roles onto TOML configs, remove the standalone evidence-reviewer, and make reviewer own completion-gate output
2026-04-08 18:03 +0100 | FIX | make the Ralph smoke eval hermetic for planning replay, restore ticket `updated_at` to stop-hook review gates, and unbreak stale timestamp smoke coverage
2026-04-08 18:47 +0100 | FEAT | add consultant-thinking and functional-ui skills, require recommendation plus options appendix in planning surfaces, and route frontend-design behind workflow grounding
2026-04-08 19:01 +0100 | CHORE | audit README against recent review and stop-hook commits, point feature inventory at harness-techniques, and remove the stale hardcoded empty-queue claim
2026-04-08 19:06 +0100 | FEAT | add a narrow canonical-doc parity validator plus test coverage, document the doc-gardening loop, and make README/spec/ticket surface drift mechanically checkable
2026-04-09 03:22 +0100 | FEAT | collapse `ralplan` and `tech-impl-plan` into `impl-plan`, update the ticket template to support richer planning artifacts, and switch live planning/runtime references to the new single planner surface
2026-04-09 03:53 +0100 | CHORE | split the shipped global AGENTS contract into `templates/global/AGENTS.md`, rewrite root `AGENTS.md` as Codexter-local context, and point `install.sh` plus `README.md` at the new boundary
2026-04-09 04:10 +0100 | FEAT | switch runtime lane routing to explicit-run-state then hook-session-id precedence, add per-session state files, and cover concurrent-session prompt capture with regression tests
2026-04-09 04:48 +0100 | CHORE | deepen the live review contract into explicit 1-to-5 score bands, add skeptic questions and evidence cues across all review families, and sync the reviewer prompt plus review-gates spec
2026-04-09 05:18 +0100 | FEAT | add the first explicit delegated-worker runtime contract with `worker_name`, `main_artifact_path`, and Stop-hook-captured `grounding_summary`, and document the new claim fields across impl/runtime surfaces
2026-04-10 01:05 +0100 | FEAT | add advisory stale-wait backpressure metadata with `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary`, derive `over_budget` status in the tmux-helper read path, and document the visible no-watchdog backpressure contract
2026-04-09 17:07 +0100 | CHORE | add a root architecture map, adopt hybrid structural-plus-prompt doc governance, and upgrade init-project to scaffold architecture/specs entry surfaces
2026-04-10 02:55 +0100 | FEAT | add session aliasing on first user-prompt capture, mirror the human-facing claim alias onto tickets as `claimed_by`, and document the runtime-vs-ticket identity split
2026-04-09 17:32 +0100 | FEAT | upgrade the live review contract with a repo-grounded desloppify search playbook, severity-ranked findings, compact search-scope reporting, and synced reviewer/spec/ticket template updates
2026-04-10 01:53 +0100 | FIX | purge stale OMX-era live skill paths from deep-interview and ralph, add local skill docs, and re-anchor the live contract to tickets, docs, and `.ralph/state`
2026-04-10 02:00 +0100 | FEAT | switch the preferred live runtime root from `.ralph` to `.harness`, keep legacy `.ralph` reads as compatibility fallback, and update the live runtime docs/rules accordingly
2026-04-10 02:13 +0100 | FIX | stop ambient `.ralph` runtime fallback from hijacking hook ticket resolution and purge the local `.ralph` runtime tree
2026-04-10 02:15 +0100 | FEAT | add a completion-only impressed-user gate to the stop-hook reviewer contract, require `user_intent_impression` plus a concrete mismatch reason, and document the stricter user-alignment completion policy
2026-04-10 03:05 +0100 | FEAT | fold Palantir- and McKinsey-style decomposition lenses into the public `brainstorm` surface, keep one intake entrypoint, and update the documented intake funnel to treat structured decomposition as a brainstorm branch rather than a second public skill
2026-04-10 04:15 +0100 | FIX | raise the tracked Stop-hook command timeout from 30 seconds to 90 seconds so slow review passes do not fail prematurely
2026-04-10 10:42 +0100 | FEAT | add a narrow harness-invariant validator for root/runtime/ticket boundary rules and reject raw session_id in ticket frontmatter
2026-04-11 02:18 +0100 | FEAT | add a demo-realism skill for believable mvp examples, realistic demo data, and presentation-worthiness rubrics before design/build
2026-04-10 04:18 +0100 | FEAT | make `tmux_helper followup` default to a compact success line, keep structured payloads behind `--json`, preserve actionable failure output, and document the preferred agent-facing command surface
2026-04-10 04:24 +0100 | FEAT | add explicit `$impl` loop activation state to runtime/session captures, gate Stop-hook same-ticket continuation on that flag plus matching claim ownership, and document that tmux `auto_continue` is follow-up plumbing rather than the global build-loop switch
2026-04-10 17:19 +0100 | FEAT | tighten the shipped global agent contract so direct user requests default to action, missed-work complaints trigger fix-first correction recovery, and auto-approval stays limited to obvious same-scope continuation
2026-04-10 17:28 +0100 | FEAT | add a `repent` recovery skill as an explicit operator escape hatch for audit-then-fix mode when the assistant likely missed something obvious on the current task
2026-04-10 18:35 +0100 | FIX | stop `UserPromptSubmit` from persisting approval-review and delegated read-only agent prompts as user turns, and add regression coverage for the polluted `.harness` session cases
2026-04-11 01:32 +0100 | FEAT | gate canonical user-turn/current-run capture to control sessions that start through the public skill entrypoints, persist session origin in runtime state, and keep internal prompt filtering as fallback-only protection
2026-04-11 02:06 +0100 | FEAT | add first-pass skill `todos.md` sidecars as plain natural-language checkbox templates with Markdown skill links, add candidate examples across review/impl/debugging/planning/QA/ticketization skills, and document the anti-parser boundary in repo docs
2026-04-11 02:22 +0100 | FEAT | add a canonical diagram-first planning/spec convention, require top-level Mermaid delta maps for material `impl-plan` tickets, and push inline-signature plus data-flow guidance into the live ticket/template surfaces
2026-04-11 02:50 +0100 | FEAT | add a reusable `diagramming` skill for compact Mermaid delta maps, zoom-ins, numbered data-flow traces, and inline-signature system diagrams
2026-04-13 00:03 +0100 | FIX | make explicit `$impl` activation derive from exact parsed control-skill tokens, stop `$impl-plan` from arming the `$impl` loop, and add runtime-state regressions for exact-dollar-skill capture
2026-04-13 09:51 +0100 | FEAT | reshape `impl-plan` around top-of-ticket `Human` and lower `Agent` lanes, require compact signature sketches for interface-heavy plans, and sync the live planning template/references to the new skim-first contract
2026-04-13 16:47 +0100 | FEAT | update the shipped global AGENTS contract to prefer concise chat plus artifact-first detail, and auto-run `review` at the end of `impl-plan` and `impl` plus broader meaningful-pass sweeps before completion claims
2026-04-13 17:58 +0100 | FEAT | strengthen the Stop-hook reviewer completion gate with explicit obvious-next-step fields so orchestrator routing requires reviewer proof that no clear same-ticket action still remains
2026-04-13 18:41 +0100 | FEAT | make Stop-hook reviewer completion gates explicitly ground through the `review` skill contract and return one consultant-style best immediate next step when continuing same-ticket work
2026-04-13 18:49 +0100 | FEAT | make Stop-hook reviewer completion gates explicitly invoke `$review` before `$consultant-thinking` so continuation advice is grounded first and narrowed second
2026-04-13 19:29 +0100 | FEAT | add session-owned `$loop` runtime capture, early Stop-hook loop routing with deterministic local predicates, and explicit same-session stop handling without relying on Escape
2026-04-13 20:08 +0100 | CHORE | rename the public advisory skill from `consultant-thinking` to `advise`, move the skill module, and update live reviewer/global-contract references to the new name
2026-04-13 09:55 +0100 | FEAT | add a `pr-splitting` skill for post-build non-stacked PR decomposition with feature-first preference, layer fallbacks, hunk-avoidance rules, and explicit PR-plan output
2026-04-13 12:33 +0100 | FIX | seed selected-ticket runtime ownership on explicit `$impl` control-session invocations, let runtime loading fall through session-only stubs to richer same-session run payloads, and add regressions for the reproduced missing-ownership stop-hook failure
2026-04-13 17:49 +0100 | CHORE | review the active ticket board, archive completed recent tickets, keep TASK-0060 as the next active focus, and retain TASK-0031 as lower-priority backlog
2026-04-13 20:33 +0100 | FEAT | add a `coderabbit-review` skill plus an opt-in stage-aware runner and sample git hooks for explicit pre-push or PR CodeRabbit CLI review outside the Stop-hook loop
2026-04-13 20:41 +0100 | FEAT | make `init-project` scaffold optional `.githooks/` samples for CodeRabbit pre-commit/pre-push workflows while keeping hook activation manual and preferring pre-push
2026-04-13 20:54 +0100 | FEAT | make `init-project` scaffold repo-local pre-commit and pre-push validator scripts, route the pre-push hook through local checks first, and chain CodeRabbit only as an explicit optional follow-up
2026-04-13 20:58 +0100 | FIX | decouple `init-project`'s scaffolded CodeRabbit pre-push path from Codexter-owned helpers and invoke the standalone `coderabbit` CLI directly after local validators
2026-04-13 19:43 +0100 | FEAT | make `spec-to-ticket` capability-first by default, keep coherent greenfield fullstack features bundled as one ticket, encode explicit split triggers, and align the module review/todo/invariant surfaces with the new sizing rule
2026-04-13 21:41 +0100 | FIX | add the missing `skills/loop` package, promote `$loop` into the live skill inventory, and align the control-skill docs with the shipped runtime contract
2026-04-13 22:49 +0100 | CHORE | restore the README top-level diagram as a color-coded super stack map that overlays the main flow, durable surfaces, and the major skill groups in one picture
2026-04-13 23:05 +0100 | FEAT | replace `docs-closeout` with the canonical `close-ticket` skill, add a parent closeout todo flow for docs/checks/commit/push, and keep `$docs-closeout` as a runtime compatibility alias
2026-04-14 00:15 +0100 | FEAT | add an `agent-testability-plan` skill plus the canonical `agent-testability-surfaces` doctrine, wire `deep-system-design` to hand off into it, and teach `spec-to-ticket` / `impl-plan` to consume the resulting brief when present
2026-04-14 01:10 +0100 | CHORE | audit the autonomy checklist against the live repo, seed roadmap tickets for the real missing gaps, and slim the README around current state plus roadmap
2026-04-16 01:02 +0100 | FEAT | add a public `desloppify` skill with explicit main-agent versus worker modes, ignore local `.desloppify/` state, and promote the shipped workflow into the canonical inventory
2026-04-16 01:04 +0100 | FEAT | make ticket sizing ambition-aware across `spec-to-ticket`, `impl-plan`, and ticket docs so CRUD stays whole and complex systems split by proof/foundation or real runtime boundaries instead of micro-steps
2026-04-16 01:46 +0100 | FIX | narrow the `desloppify` skill so the main agent delegates one worker, reviewer roles stay out of the workflow, and worker mode hands nested `--runner codex` subjective review back instead of recursing
2026-04-23 02:07 +0100 | FIX | add required top-level names to all custom agent role TOMLs and backstop agent role metadata with the harness invariant checker
2026-04-23 21:55 +0100 | CHORE | reset the active board around file-map-first planning, evidence enforcement, compaction-safe handoffs, and answer-plan-act routing, and archive the superseded roadmap tickets
2026-04-24 15:38 +0100 | CHORE | collapse the ticket plan shape into a compact file-map-first contract, remove empty review/handoff boilerplate from the template, and define per-ticket artifact storage under `tickets/artifacts/`
2026-04-24 17:20 +0100 | CHORE | add a canonical harness-engineering doctrine spec, route root docs toward it, and document the new placement rubric in the live techniques inventory
2026-04-24 19:05 +0100 | FEAT | add a `gap-analysis` planning skill and make feature-gap research a first-class ticket section for missing or parity-driven work
2026-04-24 20:10 +0100 | FEAT | render `config.toml` on every install from a sanitized template plus local env/TOML overlays instead of seed-once local drift
2026-04-24 19:18 +0100 | FIX | align the harness-engineering doctrine equations with the existing quickstart model and add the doctrine to the architecture entry surfaces
2026-04-24 19:31 +0100 | FEAT | require harness brainstorming to compare `AGENTS.md`, skills, subagents, and hooks explicitly and explain why the chosen surface wins over the others
2026-04-24 19:40 +0100 | FIX | move harness-surface comparison guidance out of the shared `brainstorm` skill and into Codexter's local `AGENTS.md`
2026-04-24 19:52 +0100 | FEAT | require a fresh `review` pass before substantive user-facing answers about changed Codexter repo state, exempting only interim progress updates
2026-04-24 21:15 +0100 | FEAT | cut QA and completion gating over to ticket artifact roots, require delegated builder/reviewer/qa lanes in build prompts, and replace legacy `Review Packet` parsing with artifact-linked Stop-hook evidence checks
2026-04-24 22:05 +0100 | FEAT | add an explicit `$impl` execution-phase contract with `requires_qa`, `requires_demo`, `execution_phase`, public `$qa`/`$demo` recovery surfaces, and Stop-hook phase progression from impl to qa to demo before final completion review
2026-04-24 20:01 +0100 | FIX | move the fresh-review-before-final-answer rule into `templates/global/AGENTS.md` and treat repo-local plus global `AGENTS.md` as separate harness-placement candidates
2026-04-24 20:18 +0100 | FIX | narrow the global fresh-review-before-final-answer rule so it applies only after meaningful pass boundaries and no longer conflicts with the no-microscopic-review guardrail
2026-04-24 22:12 +0100 | FEAT | realign impl-plan to the canonical single-surface ticket template and add compact typed data-flow planning through type sketches and golden-path examples
2026-04-24 22:40 +0100 | CHORE | rename the Stop-hook role file from `reviewer` to `completion-reviewer` so it is easier to distinguish from the deeper `code-reviewer` agent
2026-04-24 18:51 +0100 | FEAT | tighten the shipped global response contract so implemented feature summaries default to short bullets with `Before` / `After` framing and a tiny concrete example when helpful
2026-04-24 19:35 +0100 | FEAT | add a visible `qa/` cookbook surface, make Playwright the default browser-regression proof lane, and frame `agent-browser` as the discovery/debugging companion for deterministic UX testing
2026-04-24 19:58 +0100 | FEAT | make `init-project` bootstrap capture agent-experience/testability decisions and scaffold a repo-owned `qa/` cookbook surface by default
2026-04-24 20:28 +0100 | FEAT | tighten bootstrap-to-ticket propagation so `spec-to-ticket` carries bootstrap testability defaults into UI-bearing ticket contracts and matching `qa/cookbook` workflow seeds
2026-04-24 19:42 +0100 | FEAT | add a separate `parity-research` skill, tighten the `gap-analysis` boundary, and document external parity research as a first-class planning surface
2026-04-24 19:43 +0100 | FEAT | make `init-project` use a visible bootstrap brief and deep-interview-quality intake, add a real pre-push template with large-file gates plus soft shared-utility warnings, and keep generated hook guidance aligned with optional CodeRabbit/desloppify follow-up
2026-04-24 20:50 +0100 | CHORE | refresh README and architecture so the top-level repo story reflects shipped file-map-first planning, artifact-first tickets, and visible bootstrap/qa surfaces
2026-04-24 23:35 +0100 | CHORE | migrate the ticket board from flat `TASK-*.md` files plus `tickets/artifacts/` into per-ticket directories with canonical `ticket.md` files, sibling `artifacts/`, and matching runtime/template/doc updates
2026-04-24 21:35 +0100 | FIX | harden Stop-hook output by keeping notification fallback off stdout and emitting explicit allow-stop JSON on Stop-event no-op branches
2026-04-24 22:45 +0100 | FEAT | rename `init-project` to `deep-init-project` and make bootstrap ask explicit local-hook, heavy-check, and CI/deploy-gate questions before scaffolding defaults
2026-04-24 20:23 +0100 | FEAT | strengthen the shipped global modularity doctrine around feature-first modules, extractable UI and backend seams, and subagent-friendly planning boundaries
2026-04-25 01:13 +0100 | FIX | make `impl-plan`, `$impl`, `review`, and the live `AGENTS` contract treat the selected ticket as the default planning/build/review unit instead of shrinking coherent tickets into smaller internal slices
2026-04-25 01:23 +0100 | FIX | make `impl-plan` and the canonical ticket template require detailed, action-oriented plans with explicit execution steps and stronger recommendation tone instead of thin approval-first summaries
2026-04-25 12:15 +0100 | FEAT | add a discoverable `pr-runtime` skill plus a minimal `ticket_runtime` helper for isolated PR follow-up, concurrent-writer checkout safety, ticket-scoped runtime records under `.harness/state/tickets/`, and declared QA target lookup
2026-04-25 12:45 +0100 | FEAT | extend `ticket_runtime` from metadata-only records into a real local launcher that can start and stop configured frontend/backend processes or compose commands, persist process metadata, and publish QA targets from the same ticket runtime record
2026-04-25 12:55 +0100 | FIX | make `ticket_runtime` keep reserved ports when teardown fails, make `qa` report only live targets with explicit runtime status, and persist launch-failure state instead of overstating availability
2026-04-25 01:22 +0100 | FEAT | tighten the shipped global contract around complaint-shaped recovery, skill todo-list loading, and action-ordered ticket plans
2026-04-25 01:29 +0100 | FIX | align `repent`, `impl-plan` README, and the techniques inventory with the new complaint-recovery and skill-checklist doctrine
2026-04-25 02:06 +0100 | FEAT | replace hidden Stop-hook completion-gate review with a visible nonce-backed completion-review receipt flow, teach reviewer lanes to write linked receipt artifacts, and gate completion on that receipt plus targeted stop-hook tests
2026-04-29 17:10 +0800 | CHORE | separate HISTORY and MEMORY formats so change chronology and durable rules use distinct one-line contracts
2026-04-29 06:21 +0800 | FIX | simplify the ticket contract so durable links live in `Refs`, detailed proof lives in `Evidence`, and the validator/runtime surfaces no longer require `linked_docs`
2026-04-29 06:52 +0800 | FEAT | require active impl-loop password echo for Stop-hook completion review so the hook issues the nonce on demand and the next final response must return `COMPLETION_PASSWORD` alongside the linked receipt
2026-04-29 08:08 +0800 | FEAT | make `deep-init-project` require visible canonical app and QA runtime command guidance in the bootstrap brief, project rules, and QA cookbook templates instead of pushing repos toward mandatory Makefile wrappers
2026-04-30 02:35 +0800 | FIX | update the managed Codex config template to register `completion-reviewer` instead of the removed `reviewer` role so fresh installs and re-renders stop pointing at a missing agent file
2026-04-30 14:20 +0800 | FIX | make live `$qa` followups prefer a delegated QA lane and explicitly forbid the coordinating lane from using `agent-browser` directly when `qa-tester` delegation is available
2026-04-30 15:05 +0800 | FIX | make the shipped and repo-local agent contracts state that native `qa-tester` delegation is the default QA path and that tmux lanes are only optional visibility plumbing
2026-04-30 15:40 +0800 | CHORE | bump all tracked and installed subagent role model defaults to `gpt-5.4` so no live Codexter agent remains on `gpt-4.1` or `gpt-5.3`
2026-05-02 03:31 +0800 | CHORE | narrow `docs/HISTORY.md` into a milestone and project-event ledger so routine code deltas stay in git and durable rules stay in `docs/MEMORY.md`
2026-05-03 19:25 +0800 | FEAT | add the autoresearch skill suite with plan, execution, and skill self-improvement workflows grounded in durable session artifacts and mechanical metrics
2026-05-03 22:58 +0800 | FEAT | add the frontend skill topology with frontend-craft orchestration, functional-ui redesign, visual-design taste direction, landing-page planning, and cinematic-landing compatibility routing
2026-05-03 23:29 +0800 | CLEANUP | remove the old cinematic landing compatibility skill and route live landing, animation, and QA prompts through landing-page instead
2026-05-03 23:42 +0800 | FEAT | add best-of-worlds synthesis, prompt-profile self-improvement scaffolding, and skill judgement-question guidance for metric and adoption decisions
2026-05-04 00:03 +0800 | POLICY | codify stable local skill contracts so external skills and repos are imported only through reviewed best-of-worlds decisions, not auto-synced as live dependencies
2026-05-04 01:28 +0800 | FEAT | add Autonomy Readiness across planning surfaces and ship a serial `$ralph` dispatcher skill with a read-only filesystem-ticket selector
2026-05-04 02:37 +0800 | DOCS | restore colored whole-system README and architecture maps with the current skill topology, serial `$ralph`, Autonomy Readiness, autoresearch, best-of-worlds, and frontend routing surfaces
2026-05-04 19:04 +0800 | FEAT | add a structured feature registry plus `harness-scout` source-ingestion workflow for deduping external harness ideas, decision matrices, and manual scorecards
2026-05-04 23:11 +0800 | DOCS | run `harness-scout` against the self-evolving agents video as a duplicate source pass, add a compact technique dedupe table, and seed follow-up tickets for gated skill review plus hook-reminder benchmarking
2026-05-07 19:04 +0800 | FEAT | convert landing-page guidance into a spec-first planner/executor workflow with section-quality QA, designer-judgment scoring, and a landing-spec linter
2026-05-08 01:27 +0800 | FEAT | add a landing-page asset-evidence gate so premium generated-media pages fail when they contain only code-native support visuals
2026-05-08 04:59 +0800 | FEAT | add landing-page reference research, best-of-worlds synthesis, and unique-take planning gates before premium executor handoff
2026-05-08 05:43 +0800 | FEAT | add product-demo media planning gates so premium product landing pages require realistic product shots, assembly or exploded-view sequences, and meaningful product-state scrub
2026-05-08 08:30 +0800 | FEAT | ban hand-authored SVG section graphics from premium landing pages and replace the XR page's lower-section diagrams with generated raster media
2026-05-08 17:10 +0800 | FEAT | require longer staged hero scroll-scrub planning with synchronized effect layers and add a seekable WebGL-enhanced hero scrub to the XR page
2026-05-08 17:33 +0800 | FEAT | add product-clarity and disassembly-score gates to premium landing-page recipes and apply a clearer engineering teardown media pass to the XR page
2026-05-08 21:02 +0800 | FIX | strengthen landing-page scroll-scrub QA to assert pinned-scene visibility and fix the XR page sticky failure caused by horizontal overflow clipping
2026-05-08 21:18 +0800 | FIX | make landing-page asset evidence reject `generated-video` claims backed only by Seedream/image stills plus local ffmpeg assembly
2026-05-11 05:35 +0800 | FEAT | implement the frontend skill parity handoff with stack-facts preflight, current shadcn registry and theme guidance, numeric taste dials, design briefs, component state matrices, and stronger frontend QA gates
2026-05-13 00:03 +0800 | GOVERNANCE | Added the ticket Proof Contract spine so material tickets can declare mechanical metrics, review rubric gates, and required evidence before implementation starts.
2026-05-05 02:02 +0800 | FEAT | add delegate-cli external CLI delegation with a Pi/Kimi delegate-frontend profile, deterministic dry-run helper, templates, docs, and ticket evidence handoff
2026-05-05 04:57 +0800 | FEAT | integrate web-design-guidelines as a source-fresh frontend review metric beside ui-quality and frontend visual QA
2026-05-05 05:28 +0800 | FEAT | add an asset-first cinematic scroll landing guideline based on Terminal Industries and the Nomous agency prototype
2026-05-05 15:33 +0800 | FEAT | add JSON landing-page registries for recipes, taste profiles, and effect stacks with the first industrial mission-control cinematic route
2026-05-06 03:25 +0800 | FEAT | add merged-root video-generation and separate remotion-render skills backed by inference.sh references and frontend asset routing
2026-05-06 04:05 +0800 | FEAT | add merged-root image-generation skill backed by inference.sh image references and best-current model routing
2026-05-07 01:05 +0800 | FEAT | harden inference.sh image and video skills with async job guidance, saved-result examples, upstream-reference guards, Foley discovery, media pipeline routing, and an official Remotion authoring skill
2026-05-07 01:30 +0800 | FEAT | promote inference.sh video guides into domain entry skills and move multi-asset media pipeline orchestration under frontend-craft
2026-05-07 01:33 +0800 | DOCS | reframe Codexter as an explicit ticket invocation layer and park premature branch-runtime scaling work
2026-05-07 01:45 +0800 | FEAT | remove standalone video-prompting skill and move prompting guidance into each video artifact domain skill
2026-05-07 02:00 +0800 | FEAT | factor shared video artifact production workflow into a linked domain-production reference
2026-05-07 02:12 +0800 | DOCS | add capped Codexter V2 milestone and archive completed or premature ticket-board entries
2026-05-07 02:47 +0800 | FEAT | add social, product-photo, and shared prompting references to the media skill topology
2026-05-07 03:08 +0800 | FEAT | demote Three.js from public skill to frontend-craft reference routing and link landing-page 3D asset guidance
2026-05-07 03:14 +0800 | FEAT | land Codexter V2 explicit invocation triggers, board-adapter conformance, Codex Cloud and Symphony handoff recipes, and future-agent misread guardrails
2026-05-07 03:15 +0800 | FEAT | add a manifest-driven Pi/Kimi frontend skill sync script and mount inference.sh image/video/remotion skills into the external frontend profile
2026-05-07 04:17 +0800 | DOCS | archive the visible completion-review receipt ticket and add README/ARCHITECTURE documentation-router sync guidance
2026-05-07 04:41 +0800 | CHORE | split Aikage hook heartbeats into start and stop notifications with shorter heartbeat timeouts
2026-05-07 04:50 +0800 | FEAT | add Terminal-style scroll-scrub QA instrumentation, harden Pi/Kimi frontend delegation around first-write repair gates, and record Terminal parity evidence
2026-05-07 05:38 +0800 | FEAT | add delegate-frontend self-improvement evals, Terminus visual-parity metrics, autoresearch memory, and live Pi/Kimi first-write experiments
2026-05-07 06:51 +0800 | FEAT | add delegate-frontend phase prompt compiler, startup probe tooling, provenance-backed eval rows, and a passing low-thinking Pi/Kimi startup probe fixture
2026-05-07 07:02 +0800 | FIX | correct delegate-frontend self-improve metric semantics so reject-control fixtures count as expected rejections and raw assertion ratio stays diagnostic
2026-05-07 07:16 +0800 | FEAT | capture a live compiled Pi/Kimi spec run as a self-improve reject-control when first-write, spec, and handoff pass but the wrapper exits on timeout
2026-05-07 07:35 +0800 | FEAT | add opt-in external CLI clean completion after expected output plus non-placeholder handoff for bounded delegate-frontend phase runs
2026-05-07 07:43 +0800 | FEAT | capture a live Pi/Kimi compiled spec success as a positive delegate-frontend self-improve fixture before moving to asset phase work
2026-05-07 10:32 +0800 | FEAT | capture seeded Pi/Kimi implementation and bounded mobile repair experiments, add mobile hero phrase-separation QA, and raise delegate-frontend self-improve replay coverage to 29 cases
2026-05-07 12:35 +0800 | FEAT | split landing-page scroll QA into mechanics and Terminal-final readiness, add terminal verdict metrics, and sync the stricter recipe checklist into the Pi/Kimi frontend profile
2026-05-07 14:19 +0800 | FEAT | add a landing-page todo recipe for modern scroll-scrub sites with competitor analysis, ASCII story planning, nested advise, generated hero media, frame conversion, and QA handoff
2026-05-07 15:04 +0800 | FEAT | add a Terminal scroll landing review rubric and score runner so self-improvement loops can target an 80-point observable artifact score
2026-05-07 15:04 +0800 | FIX | make the Pi delegation adapter pass rendered prompt text to `-p` instead of attaching the prompt file, so live runs execute the delegated task and first-write probes become meaningful
2026-05-07 15:58 +0800 | FEAT | add non-destructive Pi/Kimi repair prompt gates, sidecar repair guidance, and a Terminal-score control showing generated-media wiring can pass local desktop/mobile final readiness
2026-05-07 18:05 +0800 | FEAT | add output-quality gates, compact phase-scoped Pi delegation, first-viewport hero-offer QA, and a passing Pi/Kimi sidecar repair scoring `99/100`
2026-05-07 18:27 +0800 | FEAT | mount `agent-browser` into the Pi/Kimi frontend profile and require delegated runnable UI handoffs to capture same-thread browser QA evidence
2026-05-14 04:33 +0800 | FEAT | add feed-scout tracked-profile monitoring recipe with URL-keyed content ledger helpers and Notion proposal templates
2026-05-15 05:53 +0800 | FEAT | reimplement skill hierarchy manually with Tier 1 reference grounding, Tier 2 plan/execute interfaces, method-addressed research, and coding workflow bindings
2026-05-15 21:23 +0800 | FEAT | add a frontmatter-synced skill registry with Tier 3 groups, generated links, and a minimal skill metadata contract
2026-05-15 21:57 +0800 | FEAT | complete Phase 1 content skill todo rollout with linked checklists for marketing, social, image, video, and Remotion skills
2026-05-15 22:27 +0800 | FIX | harden the skill registry check so Tier 3 todos cannot direct-link Tier 1 primitives
2026-05-15 22:32 +0800 | FEAT | add a skill todo tier checker for strict one-level-down dependency audits
2026-05-16 12:30 +0800 | FEAT | add research:user-grounding and codify the Tier 1 promotion rule for reusable skills
2026-05-17 08:45 +0800 | FIX | make research router todos conditional instead of implying every research method should run
2026-05-17 08:48 +0800 | FEAT | add frontend proof-stack todos for browser proof, guideline audit, UX, visual design, frontend references, and frontend orchestration
2026-05-18 22:26 +0800 | FEAT | add skill source metadata and move browser QA wrapper logic into the QA skill
2026-05-19 03:34 +0800 | FEAT | add bulk skill todos, external Convex pointer, and skill-maintenance workflow
2026-05-19 04:06 +0800 | FEAT | add batch-work skill and one-command skill-system validation
2026-05-19 04:26 +0800 | FEAT | add Tier 2 harness-advisor for Codexter improvement placement decisions
2026-05-19 04:47 +0800 | DOCS | slim Codexter AGENTS.md by replacing frontend and invocation rule blocks with owner skill pointers
2026-05-20 19:46 +0800 | DOCS | link harness-scout adopted-feature placement to harness-advisor and refresh generated skill registry graph metadata
2026-05-21 01:15 +0800 | FEAT | add the first skill self-healing pipeline slice with skill capability fixtures, repair-ticket generation, and value-signal scoring for broken skill behavior
2026-05-21 01:15 +0800 | FIX | repair the installed notion-context skill after harness reinstall so missing Notion row-query tools degrade into fallback diagnostics and a repair ticket instead of a hard automation failure
2026-05-21 01:30 +0800 | FEAT | add media-ingest and video-understanding support skills so harness-scout can turn skill-teaching videos into source todos, skill comparisons, and copied-skill handoffs
2026-05-22 02:20 +0800 | FEAT | add algebraic Tier 3 pipeline guidance and pilot it across landing-page method selection plus frontend-craft composed scroll animation
2026-05-22 02:31 +0800 | FEAT | route skill-opportunity sidecar runs to read-only Notion approval tasks with recent-window context
2026-05-22 02:34 +0800 | POLICY | harden skill self-healing boundaries so external or installed skill bodies are mirrored and ticketed, not directly edited, without explicit operator authorization
2026-05-22 02:49 +0800 | DOCS | add a policy index and seed the case-based memory context graph design for connecting harness decisions, features, memories, tickets, sources, and repeated correction cases
2026-05-22 03:00 +0800 | DOCS | audit documentation duplication and collapse the legacy Ralph runtime spec into a compatibility pointer to the canonical runtime-surface spec
2026-05-22 03:01 +0800 | CLEANUP | delete the retired Ralph legacy spec bundle, remove old compatibility env aliases and flat-ticket lookup paths, and rewrite active guardrails in neutral current-system language
2026-05-22 03:01 +0800 | DOCS | expose frontend-craft composed scroll animation as a registry method and add a close-ticket consistency sweep
2026-05-22 03:08 +0800 | FEAT | add profile-driven project planning across deep-init, deep-interview, PRD, and spec-to-ticket
2026-05-22 03:08 +0800 | DOCS | apply the Tier 3 pipeline model to social-content with artifact matrix and method-selection smoke cases
2026-05-22 03:08 +0800 | DOCS | apply the Tier 3 pipeline model to video-production with deliverable matrix and method-selection smoke cases
2026-05-22 03:08 +0800 | DOCS | apply the Tier 3 pipeline model to product-photography with registry-visible shot-family methods
2026-05-22 17:57 +0800 | DOCS | add project lifecycle reference and wire generated project AGENTS/PROJECT_RULES templates to lifecycle ownership
2026-05-22 18:12 +0800 | DOCS | add harness-advisor placement axes for context budget, progressive disclosure, subagents, tools, hooks, docs, and registries
2026-05-22 18:18 +0800 | DOCS | teach harness-advisor to consult the policy index for canonical ownership and drift-sensitive placement decisions
2026-05-23 01:45 +0800 | DOCS | add first-principles planning contract across PRD, ticket slicing, implementation planning, generated project AGENTS, and ticket templates
2026-05-23 16:51 +0800 | FEAT | add a deterministic self-improve hook probe so skill-opportunity sidecar windows, cadence, and dry-run reports can be verified without waiting for live turns
2026-05-23 17:14 +0800 | FIX | add a weak-MCP fallback ladder for notion-context so task-board automation can degrade through data-source query, sparse diagnostics, and local tickets when saved-view auth or tools are unavailable
2026-05-23 18:15 +0800 | FIX | add an API-backed notion-context tasks-this-week fallback that queries Act Time over the last seven days and filters Status != Done when a Notion API token is available
2026-05-23 18:19 +0800 | FEAT | include originating project context and the Notion status-cache path in self-improve hook sidecar inputs while keeping reusable harness improvements as the default task scope
2026-05-24 00:35 +0800 | FIX | remove semantic search from notion-context task-board fallbacks so missing MCP row-query capability returns connector-unavailable or local ticket fallback instead of guessed task candidates
2026-05-24 04:12 +0800 | FEAT | add a Notion pinned-task read-check preflight that incrementally reads pinned task pages by weekly cadence and update markers before task ranking
2026-05-24 04:20 +0800 | FIX | remove public Notion API fallback from notion-context so task, project, goal, and pinned-task context stay MCP-only
