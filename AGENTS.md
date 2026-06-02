# Farplane AGENTS.md

This file is the project-local context for developing Farplane itself.

The install-time global harness contract now lives at `templates/global/AGENTS.md` and is what `install.sh` links into the live Codex home as `~/.codex/AGENTS.md`.

## Repo Purpose

Farplane is a harness repo for orchestrating Codexes through visible artifacts.
Before public launch, Farplane is the canonical source identity: active docs,
install templates, runtime env vars, Python helpers, conceptual envelopes,
skill IDs, registries, and plugin packages should not retain previous-identity
compatibility naming. Historical archives and external services can migrate
separately. See `MEM-0126`.

The main surfaces are:

- tickets as durable task memory
- docs as the canonical system of record
- skills as reusable workflows
- subagents as bounded specialists
- hooks and scripts as small control points

Prefer improving review loops, ticket contracts, skill packaging, and evidence surfaces before inventing more hidden orchestration code.

Ticketed work should use the ticket `Proof Contract` as the shared scoreboard
for metrics, review TAS gates, and required evidence. Keep full rubric
bodies in `skills/review/references/*` and full autoresearch session details in
the owning autoresearch artifacts; tickets carry handles, TAS gates, and
artifact obligations. Use `Metrics: none mechanical` rather than inventing fake
metrics for judgment-heavy work. See `MEM-0086`.

Do not describe a workflow as a shipped public capability until the repo
actually contains the discoverable `skills/<name>/` package and the canonical
inventory/docs point to it. See `MEM-0044`.

Farplane skills are stable local contracts. Treat external skills, repos,
blogs, and command families as research inputs rather than live dependencies;
import ideas through reviewed `adopt`, `adapt`, `reject`, or `defer` decisions,
usually via `best-of-worlds`. See `MEM-0073`.
Self-healing and capability tests may mirror installed or external skills under
`tests/<skill>/`, create repair tickets, and patch local Farplane wrappers, but
must not directly edit external or installed skill bodies such as
`~/.codex/skills/*` unless the operator explicitly asks for that specific
external-skill edit. Prefer a local wrapper, fixture, registry row, or visible
repair ticket. See `MEM-0107`.

Keep skill dependencies tiered rather than hidden behind nested routers:
Tier 1 primitives cover `advise`, `reference-grounding`, `prototyping`,
`review`, and skill first-load checklist loading; Tier 2 names generic
workflow interfaces such as `brainstorm`, `research:*`, `plan`, and
`execute`; Tier 3 application skills implement those interfaces for a domain.
Tier 3 checklists should usually link Tier 2 surfaces rather than direct Tier
1 primitives, because Tier 2 carries the Tier 1 obligations. In Farplane
today, `spec-to-ticket`, `impl-plan`, `$impl`, and `close-ticket` are coding
workflow skills, not the generic Tier 2 interfaces themselves. Keep
`skill:method` names as explicit addresses inside one owning skill surface.
The skill registry check enforces this by failing when Tier 3 checklists
direct-link Tier 1 primitives. See `MEM-0098`, `MEM-0100`, and `MEM-0125`.
Create new Tier 1 primitives only when multiple Tier 2 interfaces need that
move as a base dependency; otherwise keep common reusable work as a Tier 2
interface or method. User research starts as `research:user-grounding`, not a
Tier 1 primitive. See `MEM-0101`.
Use `skill-maintenance` for periodic bulk skill-system upkeep instead of
expanding the always-loaded prompt. Bulk skill edits should read project and
registry docs first, keep Tier 2 checklists linked to Tier 1 primitives, keep
Tier 3 checklists linked to Tier 2 surfaces plus intentional peer Tier 3
handoffs, and leave external skills without local checklists when wrapper logic
belongs in callers. Run
`python3 skills/skill-maintenance/scripts/check_skills.py --write` after skill
metadata, Markdown links, or checklist changes. See `MEM-0104`.
Local Farplane skills keep required checklist items directly in `SKILL.md`
under a marker-delimited `## Important Checklist` section. Redundant
`todos.md` files should be pruned once their content matches the direct
checklist, and future divergent duplicates must be reconciled manually. External
skills may omit local first-load checklists when wrapper logic belongs in
callers. Run
`check_skills.py --write` and reinstall after source skill edits before judging
live installed behavior. See `MEM-0117` and `MEM-0124`.
Use `harness-advisor` for Farplane improvement placement decisions before
expanding root policy, global templates, skills, subagents, hooks/scripts,
ticket contracts, docs/specs, validators, or registries. It reads the feature
and skill registries plus the harness doctrine, then recommends the primary
owning surface. See `MEM-0106`.

When authoring prompts for subagents, delegated CLIs, AI-powered app behavior,
structured outputs, eval prompts, or agent instruction prompts, load
`rules/prompt-engineering.md` as the shared prompt design reference.

When the operator explicitly wants audit-then-fix recovery mode after a likely
assistant miss, use the `repent` skill rather than inventing ad hoc recovery
behavior.

When planning a missing or partially implemented feature depends on
understanding what a production-grade version should include, use
`research:gap` before locking the ticket plan so current-state gaps and
external comparables are explicit instead of implied.

When the main planning question is broader external parity such as what peer
products, standards, or open-source repos consistently include for a
capability, use `research:parity` first and then route the result into
`research:gap`, `functional-ui`, or `impl-plan`. See `MEM-0097`.

For frontend, landing-page, media, and external frontend delegation work, use
the owning skills instead of copying their detailed rules here:
`frontend-craft`, `functional-ui`, `visual-design`, `landing-page`,
`delegate-frontend`, `visual-qa`, `web-design-guidelines`, and `review`.
Those skills own premium/Terminal landing gates, generated-media proof,
Pi/Kimi first-write rules, browser evidence, and frontend guideline scoring.
See `MEM-0072`, `MEM-0076` through `MEM-0085`, and `MEM-0088` through
`MEM-0096`.
For Farplane invocation, compute selection, board adapters, and future
Symphony/Codex Cloud handoff work, use `farplane-invocation`,
`pr-runtime`, `docs/specs/board-compute-orchestration.md`,
`docs/specs/farplane-v2-milestone.md`, and
`docs/specs/symphony-compatible-farplane-runner.md`. Keep Farplane as an
explicit invocation and proof layer; do not expand it into a daemon, hosted
control plane, scheduler, or hidden cloud wrapper without a new ticketed need.
See `MEM-0077`, `MEM-0081`, and `MEM-0082`.

## Project Structure

- `README.md`: current product shape, setup, and canonical entry points
- `agents/`: subagent role configs and prompt contracts
- `bin/`: hook and runtime scripts
- `docs/`: durable specs, history, memory, troubles, and research
- `experiments/`: smoke runs, eval outputs, and prototype evidence
- `qa/`: reusable browser-QA runbooks, shortcuts, and deterministic test-entry guides
- `rules/`: reusable policy fragments
- `skills/`: operational playbooks, references, scripts, and templates
- `templates/global/`: install-only template artifacts shipped into the live Codex home
- `tickets/`: active task board and archived work history

## Read First

Choose the smallest relevant reading set before editing.

For general repo orientation:

- `README.md`
- `ARCHITECTURE.md`
- `docs/specs/README.md`
- active ticket under `tickets/`
- `docs/MEMORY.md`
- `docs/TROUBLES.md`

For harness tuning and repo-shape changes:

- `docs/specs/harness-engineering-doctrine.md`
- `docs/specs/harness-engineering-quickstart.md`
- `docs/specs/harness-techniques.md`
- `docs/specs/spec-first-execution-loop.md`
- `docs/specs/orchestrator-subagent-loop.md`
- `docs/specs/review-gates.md`

For install and bootstrap work:

- `install.sh`
- `templates/global/AGENTS.md`
- `PROJECT_RULES.md`
- `config.toml.example`
- `skills/deep-init-project/SKILL.md`

For harness-design research and external patterns:

- `docs/research/web-research/2026-04-02_anthropic-harness-comparison.md`
- `docs/research/web-research/2026-04-02_farplane-change-proposal.md`
- `docs/research/web-research/2026-04-02_farplane-vs-omx-gap-analysis.md`

## Local Operating Rules

- No blind edits. Read the relevant spec, ticket, and nearby module docs first.
- Tickets and docs are the source of truth; do not hide state in chat.
- Keep chat concise and put deep detail into visible repo artifacts such as the active ticket and canonical docs.
- Keep chat concise, but make planning artifacts detailed and action-oriented.
  A strong ticket plan should say what will be built, in what order, and how
  it will be proved without falling back to timid "maybe/could" language. See
  `MEM-0062`.
- Preserve the colored whole-system workflow/skill map in both `README.md` and
  `ARCHITECTURE.md`; do not compress it into a tiny linear chart during
  concision passes unless an equally complete replacement exists. See
  `MEM-0075`.
- When summarizing implemented feature changes to the operator, prefer `Before` / `After` / `Example` bullets over one dense prose block. See `MEM-0051`.
- Keep QA and completion proof artifact-first: link ticket-scoped evidence from `tickets/TASK-XXXX/artifacts/`, and for UI/user-visible work keep browser capture separate from final `visual-qa` judgment. See `MEM-0048`.
- For adversarial agent testing, treat `agent-qa-test` as the public proof
  orchestrator and `agent-behavior-test` as the instrumented child-run capture
  primitive. Serious readiness claims should include tester evidence,
  evidence-review critique, captured logs when useful, and a final proof-bundle
  review. See `MEM-0115`.
- In live `$impl` loops, treat `$qa` as a delegated lane: the coordinating lane should hand browser driving and proof capture to `qa-tester` instead of using `agent-browser` directly. See `MEM-0069`.
- Outside tmux or lane-specific runtime flows, keep the same ownership split: native `qa-tester` delegation is the default way to run meaningful QA or browser proof, and the main agent should not personally use `agent-browser` when that QA ownership can be isolated. See `MEM-0070`.
- Treat `$impl` as the public execution surface, with internal `execution_phase` progression through `impl`, `qa`, and `demo` when required. Stop-hook should advance those phases mechanically before final completion review. See `MEM-0049`.
- Treat `$work` as the Work Admission surface that classifies one request,
  ticket, ticket batch, board-selected unit, epic, or metric loop before
  choosing Goal, compute, planning, proof, and downstream skills.
- Treat `$ralph` as the public Goal-backed board context and serial selection
  surface. It selects ready filesystem tickets or safe related tiny-ticket
  batches and hands work units to `$work`; parallel dispatch, leases, merge
  policy, and batch-QA orchestration remain future work. See `MEM-0074`.
- Final Stop-hook completion in Farplane should remain mechanical and visible: after impl/qa/demo gates pass, request one linked nonce-backed completion-review receipt from the visible reviewer lane instead of hiding the final judgment in a background review pass. Only active ticket-backed `impl` loops should receive that nonce, and the next final response must echo it as `COMPLETION_PASSWORD: <nonce>` alongside the matching receipt. See `MEM-0064`, `MEM-0067`.
- Material review should run through the native `reviewer` subagent when
  available. Pass the active ticket or task artifact path, changed files,
  evidence artifacts, review focus, caller-declared rubric families, required
  TAS gates, hard gates, and expected output path; the reviewer validates that
  routing and runs the `review` skill contract. Coordinating lanes should not
  self-approve material work. See `MEM-0127` and `MEM-0129`.
- Once specs are already decomposed into modular tickets, treat the selected
  ticket as the default planning, build, and review unit. `impl-plan` should
  plan the whole ticket, `$impl` should try to land the whole ticket, and
  `review` should judge the whole ticket unless a real blocker, proof
  boundary, safety issue, or explicit follow-up ticket makes narrower scope
  real. See `MEM-0061`.
- Auto-run `review` at the end of `impl-plan` and at the end of `impl` when
  working inside Farplane, using the `reviewer` lane for material review when
  native subagents are available. See `MEM-0127` and `MEM-0129`.
- Keep live repo-owned skills and docs Farplane-native. Retired OMX instructions belong only in archive or research material, not active surfaces.
- Prefer `.harness/` for live runtime state.
- Keep root `AGENTS.md` local and navigational. Global install policy belongs in `templates/global/AGENTS.md`.
- For Farplane harness brainstorming, explicitly compare repo-local `AGENTS.md`, `templates/global/AGENTS.md`, `skills/*`, `agents/*.toml`, and hooks / `bin/*`, then explain why the chosen surface should change now and why the others should not be the primary change surface.
- For harness-surface placement decisions, use `docs/specs/harness-engineering-doctrine.md` before expanding root policy, subagents, hooks, or validators.
- When changing harness behavior, prefer the smallest lever that fixes the real failure:
  - review loop and proof requirements first
  - ticket/task-shaping contracts next
  - skills and subagent boundaries after that
  - root prompt rewrites last
- Do not treat Farplane like an app repo with one central runtime to extend by default. Most work here is about better orchestration surfaces, not more orchestration code.
- For early checklist experiments, prefer plain checkbox lists with Markdown
  links to related skills before inventing parser syntax or persisted workflow
  state.

## Durable Truth

- `tickets/`: active task object, plan, evidence, blockers, and any short
  resume notes when needed, with canonical ticket files at
  `tickets/TASK-XXXX/ticket.md` and `tickets/archive/TASK-XXXX/ticket.md`
- `docs/HISTORY.md`: append-only event ledger for meaningful shipped milestones,
  migrations, and project-shaping decisions; routine code deltas and file-level
  summaries belong in git, not history. See `MEM-0071`.
- `docs/MEMORY.md`: curated invariants and constraints that future work must obey
- `docs/TROUBLES.md`: repeated misses and prevention ideas
- `experiments/`: proof artifacts and smoke outputs

Transient execution state stays outside this file. Keep this file short enough that an agent can use it as a map.

## Stop If

- scope conflicts or is unclear
- API or interface contract is ambiguous
- migration is risky with no rollback
- circular dependency appears

No silent architectural drift.
