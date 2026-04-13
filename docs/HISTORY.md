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
2026-04-13 09:55 +0100 | FEAT | add a `pr-splitting` skill for post-build non-stacked PR decomposition with feature-first preference, layer fallbacks, hunk-avoidance rules, and explicit PR-plan output
2026-04-13 12:33 +0100 | FIX | seed selected-ticket runtime ownership on explicit `$impl` control-session invocations, let runtime loading fall through session-only stubs to richer same-session run payloads, and add regressions for the reproduced missing-ownership stop-hook failure
