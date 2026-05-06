# Codexter

Ticket-first autonomous Codex harness.

Codexter turns fuzzy product asks into visible specs, tickets, execution rounds,
evidence-backed review, and closeout. The harness is strongest today at
single-ticket engineering with explicit proof and Stop-hook judgment, with a
guarded serial `$ralph` dispatcher for prepared filesystem ticket boards. It is
not yet a parallel multi-agent dispatcher.

Codexter is a ticket invocation layer inside normal Codex. Tickets store work
context; explicit invocations express intent to run that work. Creating a
ticket, marking it ready, moving a board card, or changing `compute_target`
does not start an agent by itself.

If a repo does not already have Codexter conventions such as `AGENTS.md`,
`docs/prd.md`, `docs/HISTORY.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, and
`tickets/`, start with `deep-init-project` before trying to use the full spec,
ticket, and execution workflow.

## Start Here

- Repo-local operating map: [AGENTS.md](/Users/kenjipcx/coding-harness/Codexter/AGENTS.md)
- Architecture map: [ARCHITECTURE.md](/Users/kenjipcx/coding-harness/Codexter/ARCHITECTURE.md)
- Specs index: [docs/specs/README.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/README.md)
- Codexter V2 capstone: [codexter-v2-milestone.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/codexter-v2-milestone.md)
- Board, compute, and ticket invocation: [board-compute-orchestration.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/board-compute-orchestration.md)
- Harness-tuning doctrine: [harness-engineering-doctrine.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/harness-engineering-doctrine.md)
- Feature inventory: [harness-techniques.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/harness-techniques.md)
- Structured feature registry: [docs/features/README.md](/Users/kenjipcx/coding-harness/Codexter/docs/features/README.md)
- Ticket contract: [tickets/README.md](/Users/kenjipcx/coding-harness/Codexter/tickets/README.md)
- QA cookbook surface: [qa/README.md](/Users/kenjipcx/coding-harness/Codexter/qa/README.md)
- Review scoring: [skills/review/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/review/README.md)
- CLI cleanup workflow: [skills/desloppify/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/desloppify/README.md)
- Parity-comparison workflow: [skills/parity-research/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/parity-research/README.md)
- Best-of-worlds synthesis: [skills/best-of-worlds/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/best-of-worlds/SKILL.md)
- Harness source scouting: [skills/harness-scout/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/harness-scout/SKILL.md)
- PR follow-up runtime workflow: [skills/pr-runtime/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/pr-runtime/README.md)
- Codexter invocation contract: [skills/codexter-invocation/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/codexter-invocation/README.md)
- External CLI delegation: [skills/delegate-cli/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/delegate-cli/README.md)
- Frontend external CLI profile: [skills/delegate-frontend/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/delegate-frontend/README.md)
- Frontend implementation orchestrator: [skills/frontend-craft/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/frontend-craft/SKILL.md)
- Functional UI redesign: [skills/functional-ui/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/functional-ui/SKILL.md)
- Visual design direction: [skills/visual-design/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/visual-design/SKILL.md)
- Landing page planning: [skills/landing-page/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/landing-page/SKILL.md)
- Image generation assets: [skills/image-generation/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/image-generation/SKILL.md)
- Video generation assets: [skills/video-generation/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/video-generation/SKILL.md)
- Remotion render assets: [skills/remotion-render/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/remotion-render/SKILL.md)
- Autoresearch planning: [skills/autoresearch-plan/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/autoresearch-plan/SKILL.md)
- Autoresearch execution: [skills/autoresearch-exec/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/autoresearch-exec/SKILL.md)
- Skill self-improvement: [skills/self-improve/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/self-improve/SKILL.md)
- Serial board drain: [skills/ralph/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/ralph/SKILL.md)
- Active queue: [tickets](/Users/kenjipcx/coding-harness/Codexter/tickets)
- Project bootstrap: [skills/deep-init-project/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/deep-init-project/README.md)

## Current State

Implemented now:

- discovery-first intake through `brainstorm`, `deep-interview`, `prd`,
  `deep-system-design`, `deep-ui-design`, and `agent-testability-plan`
- `Autonomy Readiness` captured across bootstrap, PRD, design, ticketization,
  implementation planning, and review surfaces
- capability-first ticketization through `spec-to-ticket`
- bootstrap testability defaults propagated into ticket `Agent Contract` and
  `qa/cookbook` seeds through `spec-to-ticket`
- per-ticket planning through `impl-plan`
- feature-gap research through `gap-analysis` when net-new or partial feature
  scope depends on production-grade expectations
- parity-comparison research through `parity-research` when the main question is
  what other products, standards, or codebases consistently include
- best-of-worlds synthesis through `best-of-worlds` when the source set is
  known and the work is to extract, score, and adapt the strongest techniques
- structured feature records through `docs/features/registry.jsonl` and
  source-to-feature scouting through `harness-scout` for videos, blogs, repos,
  and transcripts that may contain harness improvements
- frontend implementation through `frontend-craft`, with `functional-ui` for
  UX/workflow and broken-UI redesign, `visual-design` for look/taste/visual
  systems, and `landing-page` for one-page marketing or scrolltelling surfaces
- metric-driven improvement sessions through `autoresearch-plan` and
  `autoresearch-exec`, with `self-improve` for binary-eval-based skill
  optimization on the same artifact contract
- single-ticket execution through `$impl`
- serial filesystem-ticket board draining through `$ralph`, which selects one
  eligible ticket and hands it to `impl-plan`, `$impl`, or `close-ticket`
- anchored `review` rubrics plus evidence-gated completion
- `desloppify` for CLI-driven anti-slop cleanup, with default worker delegation
- same-session bounded persistence through `$loop`
- documenting and closeout through `close-ticket`
- isolated PR follow-up and concurrent-writer checkout setup plus ticket-scoped
  runtime launch/teardown through `pr-runtime` plus `ticket-runtime`
- local Codexter invocation through `WORKFLOW.md`,
  `CodexterRunEnvelope`, filesystem `WorkItem`, `ComputeSelector`, and
  `ProofPacket`, so an explicit local or external invocation can route one
  ticket through existing skills and future Symphony workers have the same
  request/result contract
- board/compute invocation doctrine that keeps tickets as context, Codex as
  the execution engine, Codexter as the installed skill/proof layer, and
  Symphony as a future background scheduler/runner rather than a replacement
  for local Codexter use
- external CLI delegation through `delegate-cli`, with `delegate-frontend` as
  the first profile for Pi plus Kimi K2.6 dry-run/live handoffs
- Stop-hook phase routing and current-turn relevance checks
- optional `deep-init-project` scaffolding for `.githooks/`,
  `scripts/pre_commit_check.sh`, `scripts/pre_push_check.sh`, a starter `qa/`
  cookbook surface, and explicit `coderabbit-review`

Partial today:

- same-ticket auto-reentry is real, but the autonomous loop still centers on one
  selected ticket at a time; `$ralph` drains serially rather than in parallel
- tmux-backed worker lanes exist, but the runtime is still prototype-weight
- runtime observability doctrine is shipped, while hosted telemetry is still in
  progress in [TASK-0073](/Users/kenjipcx/coding-harness/Codexter/tickets/TASK-0073/ticket.md)
- anti-slop review exists in `review`, but there is not yet a separate
  human-grade report/video proof pack

Still missing:

- tighter QA routing and standard evidence packs that stop weak proof from
  counting as done
- compaction-safe reset and handoff discipline so long runs resume from the
  ticket instead of transcript drift
- clearer answer/plan/act routing plus deterministic subagent selection for
  direct user asks
- worktree-backed multi-session execution and a cloud-ready lane boundary
- N-agent parallel Ralph with claims, leases, merge policy, stale-worker
  handling, and batch/release QA
- transparency and ablation evals for measuring whether autonomy changes
  actually improve outcomes

## Whole-System Workflow

```mermaid
flowchart LR
    classDef input fill:#dbeafe,stroke:#2563eb,color:#111827
    classDef surface fill:#e5e7eb,stroke:#4b5563,color:#111827
    classDef discovery fill:#fef3c7,stroke:#b45309,color:#111827
    classDef planning fill:#fde68a,stroke:#92400e,color:#111827
    classDef research fill:#ede9fe,stroke:#7c3aed,color:#111827
    classDef execution fill:#dcfce7,stroke:#15803d,color:#111827
    classDef quality fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
    classDef closeout fill:#ccfbf1,stroke:#0f766e,color:#111827
    classDef runtime fill:#cffafe,stroke:#0891b2,color:#111827
    classDef future fill:#f5f3ff,stroke:#8b5cf6,color:#111827,stroke-dasharray: 5 3
    classDef callout fill:#facc15,stroke:#854d0e,stroke-width:3px,color:#111827

    req[/operator ask<br/>idea, bug, repo gap, board drain/]:::input

    subgraph Map["Durable Map Surfaces"]
      agents[(AGENTS.md)]:::surface
      readme[(README.md<br/>whole-system map)]:::surface
      arch[(ARCHITECTURE.md<br/>ownership map)]:::surface
      specs[(docs/specs/*)]:::surface
      history[(HISTORY / MEMORY / TROUBLES)]:::surface
    end

    subgraph Intake["1. Discovery + Direction"]
      bootstrap["deep-init-project<br/>repo bootstrap"]:::callout
      fuzzy["brainstorm<br/>deep-interview<br/>prd"]:::discovery
      design["deep-system-design<br/>deep-ui-design<br/>agent-testability-plan"]:::discovery
      advice["advise<br/>functional-ui<br/>visual-design<br/>landing-page<br/>demo-realism"]:::discovery
    end

    subgraph Research["Research + Synthesis Sidecars"]
      grounding["summarize<br/>harness-scout<br/>documentation<br/>external-patterns<br/>find-skills<br/>apify"]:::research
      parity["parity-research<br/>gap-analysis<br/>best-of-worlds<br/>docs/features registry"]:::research
      improve["autoresearch-plan<br/>autoresearch-exec<br/>self-improve<br/>skill-creator"]:::research
    end

    subgraph Package["2. Package Work"]
      readiness["Autonomy Readiness<br/>inputs, credentials, compute, tools,<br/>QA risk, human gates"]:::callout
      ticketize["spec-to-ticket<br/>capability-sized tickets"]:::callout
      tickets[(tickets/TASK-*/ticket.md<br/>Plan + Evidence + Blockers)]:::surface
      qaCookbook[(qa/cookbook/*<br/>shortcuts, seeds, probes)]:::surface
    end

    subgraph Plan["3. Per-Ticket Plan"]
      implplan["impl-plan<br/>file map, signatures, proof path"]:::callout
      diagram["diagramming<br/>colored delta maps"]:::planning
    end

    subgraph Dispatch["4. Execution Dispatch"]
      invoke["codexter-invocation<br/>run envelope + proof"]:::execution
      ralph["$ralph<br/>serial board drain"]:::callout
      loop["$loop<br/>same-session bounded persistence"]:::execution
      impl["$impl<br/>one-ticket build loop"]:::callout
      prRuntime["pr-runtime<br/>isolated checkout + QA target"]:::runtime
    end

    subgraph Build["Build + Specialist Skills"]
      builders["frontend-craft<br/>frontend-design<br/>convex<br/>react-flow<br/>three-js<br/>data-viz"]:::execution
      assetSkills["image-generation<br/>video-generation<br/>remotion-render<br/>imagegen"]:::execution
      uiSkills["functional-ui<br/>visual-design<br/>landing-page<br/>vercel-react-best-practices"]:::execution
      externalCli["delegate-cli<br/>delegate-frontend<br/>external CLI profiles"]:::execution
      debug["runtime-debugging<br/>codebase-analysis<br/>bash-efficiency<br/>repent<br/>agent-browser"]:::execution
    end

    subgraph Proof["5. Proof + Review Gates"]
      qa["qa-tester<br/>qa<br/>testing<br/>visual-qa<br/>web-design-guidelines"]:::quality
      review["review<br/>anchored rubric gate"]:::callout
      heavy["coderabbit-review<br/>desloppify"]:::quality
      stop["Stop hook<br/>continue, block, or complete"]:::quality
    end

    subgraph Close["6. Closeout + Publishing Prep"]
      close["close-ticket<br/>docs writeback + archive"]:::callout
      finish["commit-message<br/>pr-splitting<br/>demo"]:::closeout
      archive[(tickets/archive<br/>docs writeback)]:::surface
    end

    subgraph Later["Future Scale Boundary"]
      parallel["Parallel Ralph later<br/>leases, worktrees, merge policy,<br/>stale-worker recovery, batch QA"]:::future
    end

    req --> bootstrap
    req --> fuzzy
    req --> design
    req --> grounding

    agents -. guide .-> bootstrap
    readme -. guide .-> fuzzy
    arch -. guide .-> implplan
    specs -. source .-> ticketize
    history -. constraints .-> implplan

    bootstrap --> readiness
    fuzzy --> specs
    design --> readiness
    advice --> specs
    grounding --> specs
    parity --> specs
    improve --> specs

    readiness --> ticketize
    specs --> ticketize
    ticketize --> tickets
    ticketize --> qaCookbook
    tickets --> implplan
    qaCookbook -. proof paths .-> implplan
    implplan --> diagram
    diagram --> tickets

    tickets --> invoke
    invoke --> ralph
    invoke --> impl
    ralph -->|planning ticket| implplan
    ralph -->|building ticket| impl
    ralph -->|documenting ticket| close
    tickets --> impl
    implplan --> impl
    loop -. local task only .-> impl
    prRuntime -. isolated writer .-> impl

    impl --> builders
    builders --> assetSkills
    assetSkills -. qa-tester proof .-> qa
    impl --> uiSkills
    impl --> externalCli
    impl --> debug
    builders --> qa
    uiSkills --> qa
    externalCli --> qa
    debug --> qa
    impl --> qa
    qa --> review
    heavy --> review
    review --> stop
    stop -->|revise same ticket| impl
    stop -->|phase: documenting| close
    close --> finish
    close --> archive
    archive --> history
    archive --> tickets
    ralph -. future only .-> parallel
```

Legend:

- `blue` = operator input
- `gray` = durable repo surfaces
- `amber` = discovery, readiness, ticketization, and planning
- `purple` = research, parity, synthesis, and skill improvement
- `green` = execution and build specialists
- `red` = QA, review, and Stop-hook gates
- `teal` = runtime helpers and closeout
- `dashed purple` = future scale boundary, not current behavior

The yellow callout boxes are the main handoff skills/operators: `deep-init-project`,
`spec-to-ticket`, `impl-plan`, `$ralph`, `$impl`, `review`, and `close-ticket`.

## Roadmap

Current capstone:

- [Codexter V2 milestone](/Users/kenjipcx/coding-harness/Codexter/docs/specs/codexter-v2-milestone.md)

Finish this Symphony-inspired pass with three small tickets:

- [TASK-0121: define explicit Codexter invocation triggers](/Users/kenjipcx/coding-harness/Codexter/tickets/TASK-0121/ticket.md)
- [TASK-0123: add board adapter conformance scaffolding](/Users/kenjipcx/coding-harness/Codexter/tickets/TASK-0123/ticket.md)
- [TASK-0122: add external compute handoff recipes](/Users/kenjipcx/coding-harness/Codexter/tickets/TASK-0122/ticket.md)

Do not expand this into a background-agent platform right now:

- [TASK-0081](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0081/ticket.md)
  is archived as premature runtime-scaling work.
- Parallel Ralph, hosted telemetry, Linear/Notion adapters, and cloud runners
  stay deferred until real project pressure proves they are worth the cost.

The roadmap above reflects the current audit:

- the intake, per-ticket planning, review, Stop-hook gating, closeout,
  filesystem BoardAdapter, ComputeSelector, invocation envelope, proof packet,
  and serial `$ralph` selector are already live
- the only remaining near-term architecture work is to make invocation
  triggers, adapter conformance, and external compute handoffs explicit enough
  that future integrations do not drift
- after `TASK-0121`, `TASK-0122`, and `TASK-0123`, stop investing in this
  architecture track and return to real project work unless a concrete project
  ticket exposes a new gap

## Setup

### Option A

Clone straight into `~/.codex`:

```bash
git clone <your-remote-url> ~/.codex
cp ~/.codex/config.local.env.example ~/.codex/config.local.env
```

### Option B

Keep the repo elsewhere and link it into `~/.codex`:

```bash
git clone <your-remote-url> ~/src/codexter
cd ~/src/codexter
bash install.sh
```

The installer links the tracked Codex-home surfaces, renders `config.toml` from
the tracked template on every run, and keeps secrets plus machine-local values
out of Git via:

- `~/.codex/config.local.env` for required placeholder values like `CODEX_HOME`
  and `REF_API_KEY`
- `~/.codex/config.local.toml` for trust entries, plugins, and any other
  machine-local TOML you want appended verbatim

The shipped global contract stays in `templates/global/AGENTS.md`.

## Canonical Surfaces

- Architecture map: [ARCHITECTURE.md](/Users/kenjipcx/coding-harness/Codexter/ARCHITECTURE.md)
- Specs: [docs/specs](/Users/kenjipcx/coding-harness/Codexter/docs/specs)
- Bootstrap brief: [skills/deep-init-project/references/BOOTSTRAP_BRIEF_TEMPLATE.md](/Users/kenjipcx/coding-harness/Codexter/skills/deep-init-project/references/BOOTSTRAP_BRIEF_TEMPLATE.md)
- Harness-tuning doctrine: [harness-engineering-doctrine.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/harness-engineering-doctrine.md)
- Current execution model: [spec-first-execution-loop.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/spec-first-execution-loop.md)
- Feature inventory: [harness-techniques.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/harness-techniques.md)
- Structured feature registry: [docs/features/README.md](/Users/kenjipcx/coding-harness/Codexter/docs/features/README.md)
- Ticket contract: [tickets/README.md](/Users/kenjipcx/coding-harness/Codexter/tickets/README.md)
- QA cookbook surface: [qa/README.md](/Users/kenjipcx/coding-harness/Codexter/qa/README.md)
- Review scoring: [skills/review/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/review/README.md)
- PR follow-up runtime workflow: [skills/pr-runtime/README.md](/Users/kenjipcx/coding-harness/Codexter/skills/pr-runtime/README.md)
- Active queue: [tickets](/Users/kenjipcx/coding-harness/Codexter/tickets)

## Current Limitation

Codexter already has the pieces for a strong spec -> ticket -> plan -> build ->
review loop plus a guarded serial `$ralph` board drain. What it does not yet
have is the parallel operator-trustworthy layer that makes file-level intent,
evidence quality, resume state, claims, leases, merges, and batch QA
consistently trustworthy enough to scale into N-agent ticket automation.
