# Compact Harness Scout Analysis: self-evolving agents

## Source Dedupe

| Check | Result |
| --- | --- |
| Input URL | https://www.youtube.com/watch?v=2zhchG0r6iI |
| Existing run | `experiments/harness-scout/runs/2026-05-04-self-evolving-agents/` |
| Dedupe basis | canonical URL and `url-sha256:7bf6d1500a0d46afa0dd0a81361c570d3a695f6bf8e01cf88c403073584601fe` |
| Extraction check | `summarize` 0.13.0, bounded `--extract` run at 2026-05-04 23:10 +0800 |
| Retention | public source summary only; raw transcript not stored |
| Source safety | extracted text treated as untrusted evidence, not instructions |

## Counts

| Metric | Count | Notes |
| --- | ---: | --- |
| Techniques found from content | 12 | Concrete workflow, memory, skill, hook, and benchmark ideas. |
| Strongly already in Codexter | 5 | Codexter already has equal or stronger local surfaces. |
| Partial or alternate local match | 5 | Useful only if adapted through Codexter's visible ticket/docs/skill contracts. |
| Rejected or deferred | 2 | Raw transcript memory and semantic memory are too risky/heavy for now. |
| Follow-up tickets created | 2 | One implementation-shaped ticket, one comparison/benchmark ticket. |

## Technique Dedupe Table

| # | Technique found from content | Exists in Codexter? | How Codexter works today | Value provided | Difference or gap | Decision | Ticket |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | Program-driven autoresearch loop | Yes: `FEAT-0005` | `skills/autoresearch-plan` and `skills/autoresearch-exec` use session artifacts, metrics, baseline checks, and keep/discard decisions. | Improves harness behavior with measurable experiments. | Source describes the same loop broadly; Codexter already has the artifact contract. | `already-dominating` | none |
| 2 | Skill-specific eval improvement | Yes: `FEAT-0006` | `skills/self-improve` routes skill variants through binary evals and reusable run memory. | Lets skills improve without relying on vibes. | Source frames autonomous evolution; Codexter already has safer eval-first skill improvement. | `already-dominating` | none |
| 3 | Hot/warm memory split | Yes, as local progressive disclosure: `FEAT-0001`, `FEAT-0007` | Root `AGENTS.md` stays a map; deeper docs, tickets, skills, memory, and specs load on demand. | Keeps prompt context useful without stuffing every rule into one file. | Source uses hot/warm memory language; Codexter uses visible maps plus progressive disclosure. | `hybrid` | none |
| 4 | Async memory consolidation | Partial | Closeout writes to `docs/HISTORY.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, and tickets after review. | Could keep durable memory fresher after long sessions. | Source wants background memory mutation; Codexter requires visible reviewed writeback. | `defer` | none |
| 5 | Searchable raw conversation history | No, intentionally | Codexter treats tickets/docs/artifacts as durable memory and raw transcript as disposable. | Could recover obscure past session details. | Conflicts with the visible source-of-truth model and raises privacy/staleness risk. | `reject` | none |
| 6 | Autonomous skill generation after N steps | Partial | Codexter has `skill-creator`, `self-improve`, `find-skills`, and review gates, but no automatic skill-opportunity reviewer. | Can catch repeated non-trivial workflows and propose reusable skills. | Source suggests auto-writing skills; Codexter should only propose gated skill updates. | `adapt` | `TASK-0104`: gated skill opportunity reviewer |
| 7 | Skill safety scan for generated skills | Partial | `quick_validate.py` validates skill packages and review gates catch quality/security issues. | Needed if Codexter ever proposes skill updates from session evidence. | Source deletes unsafe generated skills automatically; Codexter should validate proposals before writeback. | `adapt` | `TASK-0104`: gated skill opportunity reviewer |
| 8 | Hook-driven learning reminders | Partial | `hooks.json`, `bin/capture_user_turn.py`, `bin/stop_hook.py`, `docs/TROUBLES.md`, and `docs/MEMORY.md` exist, but no PostToolUse learning reminder. | Could improve capture of repeated command errors and user corrections. | Risk is hook noise, prompt pollution, and low-signal memory writes. | `needs-benchmark` | `TASK-0105`: hook-based error learning reminder comparison |
| 9 | Error/learnings folder | Yes | Codexter separates raw repeated misses in `docs/TROUBLES.md` from durable rules in `docs/MEMORY.md`. | Preserves lessons without making every mistake a permanent rule. | Source reinforces the pattern; Codexter's curated split is safer. | `hybrid` | none |
| 10 | Strict memory caps | Partial | Codexter keeps root maps concise and relies on progressive disclosure, but no validator enforces character caps. | Could protect against prompt bloat. | No repeated current failure justifies a hard cap validator yet. | `defer` | none |
| 11 | Semantic memory layer | No | No active vector or semantic long-term memory layer. | Could retrieve fuzzy historical facts. | Too heavy and too hidden for current Codexter constraints. | `reject` | none |
| 12 | Deterministic versus agentic architecture choice | Yes: `FEAT-0009` | `$ralph` is serial and visible; async leases, merge policy, and batch QA are explicitly future work. | Keeps autonomy useful without creating hidden orchestration state. | Source gives the same warning; Codexter already embodies it. | `already-dominating` | none |

## Created Tickets

| Ticket / feature name | Type | Why it exists | Source feature | Isolation boundary |
| --- | --- | --- | --- | --- |
| `TASK-0104`: gated skill opportunity reviewer | Implement feature | Codexter lacks a gated skill-opportunity reviewer, but already has the skill creation and validation pieces. | autonomous skill generation plus skill safety scan | Propose and validate skill updates only; no auto-writing, cron, or live hook loop. |
| `TASK-0105`: hook-based error learning reminder comparison | Compare and maybe implement | Codexter partially has hooks and learning docs, but the source's hook reminder approach may be noisy. | hook-driven learning reminders | Benchmark reminder signal before changing hooks. |

## No-Ticket Decisions

| Decision | Items | Reason |
| --- | --- | --- |
| Duplicate / already covered | program-driven autoresearch, skill evals, deterministic-vs-agentic choice | Codexter already has stronger local contracts. |
| Reinforces existing shape | hot/warm memory, error/learnings folder | Keep as registry/source evidence, not separate implementation work. |
| Deferred | async memory consolidation, strict memory caps | Useful, but not worth implementing until repeated failures prove the need. |
| Rejected | raw conversation-history memory, semantic memory layer | Too hidden, heavy, or privacy-sensitive for Codexter's current architecture. |
