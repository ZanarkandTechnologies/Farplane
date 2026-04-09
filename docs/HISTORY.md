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
