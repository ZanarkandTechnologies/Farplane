# Codexter AGENTS.md

This file is the project-local context for developing Codexter itself.

The install-time global harness contract now lives at `templates/global/AGENTS.md` and is what `install.sh` links into the live Codex home as `~/.codex/AGENTS.md`.

## Repo Purpose

Codexter is a harness repo for orchestrating Codexes through visible artifacts.

The main surfaces are:

- tickets as durable task memory
- docs as the canonical system of record
- skills as reusable workflows
- subagents as bounded specialists
- hooks and scripts as small control points

Prefer improving review loops, ticket contracts, skill packaging, and evidence surfaces before inventing more hidden orchestration code.

Do not describe a workflow as a shipped public capability until the repo
actually contains the discoverable `skills/<name>/` package and the canonical
inventory/docs point to it. See `MEM-0044`.

Codexter skills are stable local contracts. Treat external skills, repos,
blogs, and command families as research inputs rather than live dependencies;
import ideas through reviewed `adopt`, `adapt`, `reject`, or `defer` decisions,
usually via `best-of-worlds`. See `MEM-0073`.

When the operator explicitly wants audit-then-fix recovery mode after a likely
assistant miss, use the `repent` skill rather than inventing ad hoc recovery
behavior.

When planning a missing or partially implemented feature depends on understanding
what a production-grade version should include, use `gap-analysis` before
locking the ticket plan so current-state gaps and external comparables are
explicit instead of implied.

When the main planning question is broader external parity such as what peer
products, standards, or open-source repos consistently include for a
capability, use `parity-research` first and then route the result into
`gap-analysis`, `functional-ui`, or `impl-plan`.

For frontend work, use the Codexter frontend topology: `frontend-craft` is the
implementation orchestrator, `functional-ui` owns UX/workflow and broken-UI
redesign, `visual-design` owns look/taste/visual systems, and `landing-page`
owns one-page marketing or scrolltelling surfaces. Keep `frontend-design` as an
app-UI implementation reference. The old cinematic landing skill package was
removed; route those asks to `landing-page`. See `MEM-0072`.
Frontend implementation skills must preserve that topology while requiring stack
facts before build, current shadcn registry/theme discovery, numeric taste dials,
durable design briefs for substantial UI, component state matrices for reusable
UI, and responsive/reduced-motion/theme preflight proof. See `MEM-0085`.
For premium, cinematic, Terminal-style, or externally delegated landing pages,
`landing-page` must use a spec-first planner/executor split: approved
`LANDING_SPEC` before build handoff, then section-quality and designer-judgment
QA before premium claims. See `MEM-0076`.
Premium, cinematic, Terminal-style, or generated-media landing pages also need
generated or real filesystem-backed asset evidence before final quality claims;
code-rendered canvas, WebGL, Three.js, procedural, and HTML/CSS visuals are
support visuals unless the page is explicitly downgraded to prototype. See
`MEM-0077` and `MEM-0080`.
Premium landing-page planning must research competitor/comparable/inspiration
references before story and asset planning, then route patterns through
best-of-worlds adopt/adapt/reject/defer decisions and a brainstormed unique
take before executor handoff. See `MEM-0078`.
Premium product, device, hardware, equipment, or object-focused landing pages
must plan realistic product shots/renders, in-context use, assembly/disassembly
or exploded-view media, highlighted parts/features, and meaningful product-state
scroll/video sequences. Generic infographics, abstract diagrams, dashboards, and
label-only scrubs are support visuals only. See `MEM-0079`.
Premium landing-page graphics must not be hand-authored SVG illustrations, SVG
diagrams, or SVG overlay art. Use generated/real raster media, or real
WebGL/Three.js when a procedural scene is warranted. See `MEM-0080`.
Premium product landing pages must also keep the product visually inspectable:
dark overlays, WebGL effects, video opacity, tiny crops, or inaccessible color
choices cannot obscure the object, and teardown/exploded-view media needs a
disassembly score with no baked readable text. See `MEM-0082`.
Premium cinematic hero scroll-scrub must be a long authored sequence with
named beats, progress ranges, synchronized GSAP/WebGL/Three.js/HTML effect
layers, and QA evidence for media time, active beat, and effect-layer state.
See `MEM-0081`.
Premium scroll-scrub QA must also prove the pinned scene remains visible at
each checkpoint. Media time, labels, or frame-source changes are not enough;
assert pinned-panel and primary-visual viewport intersection, capture visual
region screenshots or hashes, and prefer `overflow-x: clip` over
`overflow-x: hidden` when CSS sticky is involved. See `MEM-0083`.
Premium `generated-video` evidence must come from a real video-generation
model/app or source video. Seedream/image-generator stills or generated frame
sequences assembled with local `ffmpeg` are `frame-sequence`/prototype assets,
not generated-video proof. See `MEM-0084`.

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
- `docs/research/web-research/2026-04-02_codexter-change-proposal.md`
- `docs/research/web-research/2026-04-02_codexter-vs-omx-gap-analysis.md`

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
- In live `$impl` loops, treat `$qa` as a delegated lane: the coordinating lane should hand browser driving and proof capture to `qa-tester` instead of using `agent-browser` directly. See `MEM-0069`.
- Outside tmux or lane-specific runtime flows, keep the same ownership split: native `qa-tester` delegation is the default way to run meaningful QA or browser proof, and the main agent should not personally use `agent-browser` when that QA ownership can be isolated. See `MEM-0070`.
- Treat `$impl` as the public execution surface, with internal `execution_phase` progression through `impl`, `qa`, and `demo` when required. Stop-hook should advance those phases mechanically before final completion review. See `MEM-0049`.
- Treat `$ralph` as the public serial board-draining dispatcher only. It
  selects ready filesystem tickets and hands them to `impl-plan`, `$impl`, or
  `close-ticket`; parallel dispatch, leases, merge policy, and batch-QA
  orchestration remain future work. See `MEM-0074`.
- Final Stop-hook completion in Codexter should remain mechanical and visible: after impl/qa/demo gates pass, request one linked nonce-backed completion-review receipt from the visible reviewer lane instead of hiding the final judgment in a background review pass. Only active ticket-backed `impl` loops should receive that nonce, and the next final response must echo it as `COMPLETION_PASSWORD: <nonce>` alongside the matching receipt. See `MEM-0064`, `MEM-0067`.
- Once specs are already decomposed into modular tickets, treat the selected
  ticket as the default planning, build, and review unit. `impl-plan` should
  plan the whole ticket, `$impl` should try to land the whole ticket, and
  `review` should judge the whole ticket unless a real blocker, proof
  boundary, safety issue, or explicit follow-up ticket makes narrower scope
  real. See `MEM-0061`.
- Auto-run `review` at the end of `impl-plan` and at the end of `impl` when working inside Codexter.
- Keep live repo-owned skills and docs Codexter-native. Retired OMX instructions belong only in archive or research material, not active surfaces.
- Prefer `.harness/` for live runtime state.
- Keep root `AGENTS.md` local and navigational. Global install policy belongs in `templates/global/AGENTS.md`.
- For Codexter harness brainstorming, explicitly compare repo-local `AGENTS.md`, `templates/global/AGENTS.md`, `skills/*`, `agents/*.toml`, and hooks / `bin/*`, then explain why the chosen surface should change now and why the others should not be the primary change surface.
- For harness-surface placement decisions, use `docs/specs/harness-engineering-doctrine.md` before expanding root policy, subagents, hooks, or validators.
- When changing harness behavior, prefer the smallest lever that fixes the real failure:
  - review loop and proof requirements first
  - ticket/task-shaping contracts next
  - skills and subagent boundaries after that
  - root prompt rewrites last
- Do not treat Codexter like an app repo with one central runtime to extend by default. Most work here is about better orchestration surfaces, not more orchestration code.
- For early skill-todo experiments, prefer plain `todos.md` checkbox templates with Markdown links to related skills before inventing parser syntax or persisted workflow state.

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
