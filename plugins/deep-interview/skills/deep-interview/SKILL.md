---
name: deep-interview
description: Socratic deep interview with mathematical ambiguity gating before execution
tier: 2
source: local
argument-hint: "[--quick|--standard|--deep] [--bootstrap] [--autoresearch] <idea or vague description>"
---

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Read available context before asking: active ticket, `docs/prd.md`,
  `docs/specs/`, project README/AGENTS, and relevant local files.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) for local
  baseline facts instead of asking the user for discoverable project context.
- [ ] Ask one question per round and target the weakest clarity dimension.
- [ ] When a project profile exists in `docs/bootstrap-brief.md` or the user
  names a project type, load
  [project-profiles](../deep-init-project/references/project-profiles.md) and
  ask along the profile's components, advice axes, prototype gates, and
  pipeline handoff.
- [ ] Track the required gates: intent, outcome, scope, constraints, success
  criteria, non-goals, decision boundaries, and one pressure pass.
- [ ] Re-score ambiguity after each answer and keep interviewing until the
  configured threshold and gates are satisfied.
- [ ] Use [advise](../advise/SKILL.md) only when the interview exposes real
  tradeoff options that need a recommendation.
- [ ] Use [review](../review/SKILL.md) before handing off a material interview
  summary as execution-ready.
- [ ] Write the crystallized summary into the active ticket or the next
  canonical artifact owner; do not create hidden sidecar state.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

<Purpose>
Deep Interview is an intent-first Socratic clarification loop before planning or implementation. It turns vague ideas into execution-ready specifications by asking targeted questions about why the user wants a change, how far it should go, what should stay out of scope, and what the agent may decide without confirmation.
</Purpose>

<Use_When>
- The request is broad, ambiguous, or missing concrete acceptance criteria
- The user says "deep interview", "interview me", "ask me everything", "don't assume", or "ouroboros"
- The user wants to avoid misaligned implementation from underspecified requirements
- You need a requirements artifact before handing off to `impl-plan`, `autopilot`, `impl`, or `team`
- You are bootstrapping a new or migrated project and need stack, topology, and
  quality-gate decisions clarified before `deep-init-project` scaffolds files
</Use_When>

<Do_Not_Use_When>
- The request already has concrete file/symbol targets and clear acceptance criteria
- The user explicitly asks to skip planning/interview and execute immediately
- The user asks for lightweight brainstorming only (use `plan` instead)
- A complete PRD/plan already exists and execution should start
</Do_Not_Use_When>

<Why_This_Exists>
Execution quality is usually bottlenecked by intent clarity, not just missing implementation detail. A single expansion pass often misses why the user wants a change, where the scope should stop, which tradeoffs are unacceptable, and which decisions still require user approval. This workflow applies Socratic pressure + quantitative ambiguity scoring so orchestration modes begin with an explicit, testable, intent-aligned spec.
</Why_This_Exists>

<Depth_Profiles>
- **Quick (`--quick`)**: fast pre-PRD pass; target threshold `<= 0.30`; max rounds 5
- **Standard (`--standard`, default)**: full requirement interview; target threshold `<= 0.20`; max rounds 12
- **Deep (`--deep`)**: high-rigor exploration; target threshold `<= 0.15`; max rounds 20
- **Autoresearch (`--autoresearch`)**: same interview rigor as Standard, but specialized for research-brief launch readiness and a Farplane-native handoff through the active ticket or a deliberate `docs/research/` draft when the user explicitly wants durable research artifacts
- **Bootstrap (`--bootstrap`)**: same interview rigor as Standard, but specialized for project bootstrap readiness and a Farplane-native handoff through `docs/bootstrap-brief.md` for `deep-init-project`

If no flag is provided, use **Standard**.

<Mode_Flags>
- **`--bootstrap`**: switch the interview into project-bootstrap mode. In this
  mode, the interview should converge on a scaffold-ready bootstrap brief that
  captures project goal, topology recommendation, stack choices, local quality
  gates, large-file policy, shared utility conventions, and explicit decision
  boundaries for `deep-init-project`.
- **Project profiles:** when `docs/bootstrap-brief.md` names a project profile
  or the user names a project type such as coding app, landing page, video
  project, social campaign, or product-photo shoot, use
  `deep-init-project/references/project-profiles.md` to ask along that
  profile's components and advice axes.
- **`--autoresearch`**: switch the interview into research-intake mode. In this mode, the interview should converge on a launch-ready research mission, keep the current requirements brief on live Farplane surfaces, and preserve the explicit `refine further` vs `launch` boundary for downstream handoff.
</Mode_Flags>
</Depth_Profiles>

<Execution_Policy>
- Ask ONE question per round (never batch)
- Ask about intent and boundaries before implementation detail
- Target the weakest clarity dimension each round after applying the stage-priority rules below
- Treat every answer as a claim to pressure-test before moving on: the next question should usually demand evidence or examples, expose a hidden assumption, force a tradeoff or boundary, or reframe root cause vs symptom
- Do not rotate to a new clarity dimension just for coverage when the current answer is still vague; stay on the same thread until one layer deeper, one assumption clearer, or one boundary tighter
- Before crystallizing, complete at least one explicit pressure pass that revisits an earlier answer with a deeper, assumption-focused, or tradeoff-focused follow-up
- Gather codebase facts via `explore` before asking user about internals
- For simple read-only brownfield fact gathering, prefer focused repo inspection (`rg`, nearby docs, narrow file reads) or the repo's normal explore path; keep prompts narrow and concrete and keep ambiguous investigation on the richer normal path.
- Always run a preflight context intake before the first interview question
- Reduce user effort: ask only the highest-leverage unresolved question, and never ask the user for codebase facts that can be discovered directly
- For brownfield work, prefer evidence-backed confirmation questions such as "I found X in Y. Should this change follow that pattern?"
- In Codex CLI, prefer `request_user_input` when available; if unavailable, fall back to concise plain-text one-question turns
- Re-score ambiguity after each answer and show progress transparently
- Do not hand off to execution while ambiguity remains above threshold unless user explicitly opts to proceed with warning
- Do not crystallize or hand off while `Non-goals` or `Decision Boundaries` remain unresolved, even if the weighted ambiguity threshold is met
- Treat early exit as a safety valve, not the default success path
- Persist mode state for resume safety (`state_write` / `state_read`)
</Execution_Policy>

<Steps>

## Phase 0: Preflight Context Intake

1. Parse `{{ARGUMENTS}}` and derive a short task slug.
2. Attempt to load the latest relevant context from the active ticket, linked docs, and any persisted `state_read(mode="deep-interview")` snapshot.
3. If no snapshot exists, create a minimum context snapshot with:
   - Task statement
   - Desired outcome
   - Stated solution (what the user asked for)
   - Probable intent hypothesis (why they likely want it)
   - Known facts/evidence
   - Constraints
   - Unknowns/open questions
   - Decision-boundary unknowns
   - Likely codebase touchpoints
4. Persist the snapshot in mode state and, when a ticket already exists, mirror the key points into the ticket `Working Notes` instead of creating hidden sidecar context folders.

## Phase 1: Initialize

1. Parse `{{ARGUMENTS}}` and depth profile (`--quick|--standard|--deep`).
2. Detect project context:
   - Run `explore` to classify **brownfield** (existing codebase target) vs **greenfield**.
   - For brownfield, collect relevant codebase context before questioning.
3. Initialize state via `state_write(mode="deep-interview")`:

```json
{
  "active": true,
  "current_phase": "deep-interview",
  "state": {
    "interview_id": "<uuid>",
    "profile": "quick|standard|deep",
    "type": "greenfield|brownfield",
    "initial_idea": "<user input>",
    "rounds": [],
    "current_ambiguity": 1.0,
    "threshold": 0.3,
    "max_rounds": 5,
    "challenge_modes_used": [],
    "codebase_context": null,
    "current_stage": "intent-first",
    "current_focus": "intent",
    "context_surface": "ticket:<path>#Working Notes | state:deep-interview.context_snapshot"
  }
}
```

4. Announce kickoff with profile, threshold, and current ambiguity.

## Phase 2: Socratic Interview Loop

Repeat until ambiguity `<= threshold`, the pressure pass is complete, the readiness gates are explicit, the user exits with warning, or max rounds are reached.

### 2a) Generate next question
Use:
- Original idea
- Prior Q&A rounds
- Current dimension scores
- Brownfield context (if any)
- Activated challenge mode injection (Phase 3)

Target the lowest-scoring dimension, but respect stage priority:
- **Stage 1 — Intent-first:** Intent, Outcome, Scope, Non-goals, Decision Boundaries
- **Stage 2 — Feasibility:** Constraints, Success Criteria
- **Stage 3 — Brownfield grounding:** Context Clarity (brownfield only)

Follow-up pressure ladder after each answer:
1. Ask for a concrete example, counterexample, or evidence signal behind the latest claim
2. Probe the hidden assumption, dependency, or belief that makes the claim true
3. Force a boundary or tradeoff: what would you explicitly not do, defer, or reject?
4. If the answer still describes symptoms, reframe toward essence / root cause before moving on

Prefer staying on the same thread for multiple rounds when it has the highest leverage. Breadth without pressure is not progress.

Detailed dimensions:
- Intent Clarity — why the user wants this
- Outcome Clarity — what end state they want
- Scope Clarity — how far the change should go
- Constraint Clarity — technical or business limits that must hold
- Success Criteria Clarity — how completion will be judged
- Context Clarity — existing codebase understanding (brownfield only)

`Non-goals` and `Decision Boundaries` are mandatory readiness gates. Ask about them early and keep revisiting them until they are explicit.

### 2b) Ask the question
Use structured user-input tooling available in the runtime (`AskUserQuestion` / equivalent) and present:

```
Round {n} | Target: {weakest_dimension} | Ambiguity: {score}%

{question}
```

### 2c) Score ambiguity
Score each weighted dimension in `[0.0, 1.0]` with justification + gap.

Greenfield: `ambiguity = 1 - (intent × 0.30 + outcome × 0.25 + scope × 0.20 + constraints × 0.15 + success × 0.10)`

Brownfield: `ambiguity = 1 - (intent × 0.25 + outcome × 0.20 + scope × 0.20 + constraints × 0.15 + success × 0.10 + context × 0.10)`

Readiness gate:
- `Non-goals` must be explicit
- `Decision Boundaries` must be explicit
- A pressure pass must be complete: at least one earlier answer has been revisited with an evidence, assumption, or tradeoff follow-up
- If either gate is unresolved, or the pressure pass is incomplete, continue interviewing even when weighted ambiguity is below threshold

### 2d) Report progress
Show weighted breakdown table, readiness-gate status (`Non-goals`, `Decision Boundaries`), and the next focus dimension.

### 2e) Persist state
Append round result and updated scores via `state_write`.

### 2f) Round controls
- Do not offer early exit before the first explicit assumption probe and one persistent follow-up have happened
- Round 4+: allow explicit early exit with risk warning
- Soft warning at profile midpoint (e.g., round 3/6/10 depending on profile)
- Hard cap at profile `max_rounds`

## Phase 3: Challenge Modes (assumption stress tests)

Use each mode once when applicable. These are normal escalation tools, not rare rescue moves:

- **Contrarian** (round 2+ or immediately when an answer rests on an untested assumption): challenge core assumptions
- **Simplifier** (round 4+ or when scope expands faster than outcome clarity): probe minimal viable scope
- **Ontologist** (round 5+ and ambiguity > 0.25, or when the user keeps describing symptoms): ask for essence-level reframing

Track used modes in state to prevent repetition.

## Phase 4: Crystallize Artifacts

When threshold is met (or user exits with warning / hard cap):

1. Write interview transcript summary to:
   - the active ticket `Working Notes` / `Handoff` when a ticket already exists
   - otherwise the current response as a compact `Deep-Interview Summary`
2. Write execution-ready spec to:
   - the active ticket when one already exists
   - otherwise the current response handoff plus the next canonical Farplane artifact owner selected for handoff, such as `prd` for `docs/prd.md`

Spec should include:
- Metadata (profile, rounds, final ambiguity, threshold, context type)
- Context snapshot reference/path (for impl-plan/team reuse)
- Clarity breakdown table
- Intent (why the user wants this)
- Desired Outcome
- In-Scope
- Out-of-Scope / Non-goals
- Decision Boundaries (what the agent may decide without confirmation)
- Constraints
- Testable acceptance criteria
- Assumptions exposed + resolutions
- Pressure-pass findings (which answer was revisited, and what changed)
- Brownfield evidence vs inference notes for any repository-grounded confirmation questions
- Technical context findings
- Full or condensed transcript

### Autoresearch specialization

When the clarified task is specifically about a research brief, or the skill is invoked with `--autoresearch`, keep the interview domain-specific and emit launch-consumable artifacts without skipping clarification.

- **Accepted seed inputs:** `topic`, `evaluator`, `keep-policy`, `slug`, existing mission draft text, and prior evaluator examples/templates
- **Required interview focus:** mission clarity, evaluator readiness, keep policy, slug/session naming, and whether the draft is ready to launch now or should refine further
- **Canonical artifact surface:** the active ticket when one exists, or a deliberate draft under `docs/research/` when the user explicitly wants a durable research brief
- **Launch artifact bundle:** one current Farplane brief containing `Mission Draft`, `Evaluator Draft`, `Launch Readiness`, `Seed Inputs`, and `Confirmation Bridge`
- **Launch artifact location:** keep it on the chosen live Farplane surface above; do not create hidden sidecar spec folders
- **Required artifact sections:**
  - `Mission Draft`
  - `Evaluator Draft`
  - `Launch Readiness`
  - `Seed Inputs`
  - `Confirmation Bridge`
- **Required launch content:**
  - `Mission Draft`
  - `Evaluator Draft`
  - `Launch Readiness`
  - `Seed Inputs`
  - `Confirmation Bridge`
- **Launch-readiness rule:** mark the draft as **not launch-ready** while the evaluator command still contains placeholder markers such as `<...>`, `TODO`, `TBD`, `REPLACE_ME`, `CHANGEME`, or `your-command-here`
- **Structured result contract:** the chosen brief should carry the finalized `topic`, `evaluatorCommand`, `keepPolicy`, `slug`, `launchReady`, and `blockedReasons` fields so the downstream research runner can consume it directly
- **Confirmation bridge:** after artifact generation, offer at least `refine further` and `launch`; do not launch detached tmux until the user explicitly confirms `launch`
- **Handoff rule:** downstream execution must preserve the clarified mission intent, evaluator expectations, decision boundaries, and launch-readiness status from this artifact rather than bypassing the draft review step

### Bootstrap specialization

When the clarified task is specifically about starting or migrating a project,
or the skill is invoked with `--bootstrap`, keep the interview bootstrap-specific
and emit a scaffold-consumable artifact without skipping clarification.

- **Required interview focus:** project goal, audience, likely scale, topology
  recommendation, stack defaults, required local checks, optional heavy checks,
  local git-hook activation policy, local-vs-CI/deploy gate split,
  large-file policy, shared utility convention, and what `deep-init-project`
  may decide without further confirmation
- **Profile-specific focus:** select or confirm a `ProjectProfile`, then ask
  material questions across its component set, advice axes, prototype gates,
  and downstream pipeline handoff. Use `advise` for real tradeoff axes, such as
  video hook/asset/sound/edit choices or landing hero/media/motion directions.
- **Canonical artifact surface:** `docs/bootstrap-brief.md`
- **Bootstrap artifact bundle:** one current Farplane brief containing
  `Summary`, `Intent`, `Recommended Shape`, `Stack Decisions`,
  `Validation and Hooks`, `File-Size Policy`, `Shared Utility Policy`,
  `Decision Boundaries`, and `Defaults Chosen`
- **Structured result contract:** the chosen brief should carry the finalized
  `projectShape`, `topologyRecommendation`, `stackDefaults`, `localChecks`,
  `heavyChecks`, `hookPolicy`, `hookActivationChoice`, `deployGatePolicy`,
  `fileSizePolicy`, `utilityPolicy`, and `defaultsChosen` fields so
  `deep-init-project` can scaffold from it directly
- **Handoff rule:** downstream `deep-init-project` scaffolding should preserve the
  clarified bootstrap intent and decision boundaries instead of re-asking the
  same bootstrap questions in a second shallow loop

## Phase 5: Execution Bridge

Present execution options after artifact generation using explicit handoff contracts. Treat the deep-interview spec as the current requirements source of truth and preserve intent, non-goals, decision boundaries, acceptance criteria, and any residual-risk warnings across the handoff.

### 0. **`deep-init-project`**
- **Input Artifact:** `docs/bootstrap-brief.md`
- **Invocation:** `$deep-init-project <repo or migration target>`
- **Consumer Behavior:** Treat the bootstrap brief as the current source of
  truth for scaffold defaults, topology recommendation, validator shape,
  hook-routing policy, CI/deploy gate decisions, and shared utility
  conventions
- **Skipped / Already-Satisfied Stages:** bootstrap ambiguity reduction and
  project-shape intake
- **Expected Output:** scaffolded project files, visible hook samples, and
  bootstrap defaults aligned with the brief
- **Best When:** the task is bootstrap or migration setup rather than feature
  planning
- **Next Recommended Step:** continue with `prd` or `spec-to-ticket` once the
  repo scaffold is in place

### 1. **`$impl-plan` (Recommended)**
- **Input Artifact:** the active ticket path plus the current deep-interview summary / requirements brief
- **Invocation:** `$impl-plan --consensus <ticket-or-brief>`
- **Consumer Behavior:** Treat the deep-interview spec as the requirements source of truth. Do not repeat the interview by default; refine architecture/feasibility around the clarified intent and boundaries instead.
- **Skipped / Already-Satisfied Stages:** Requirements discovery, ambiguity clarification, and early intent-boundary elicitation
- **Expected Output:** an updated ticket plan or other approved Farplane planning artifact that preserves the clarified requirements
- **Best When:** Requirements are clear enough to stop interviewing, but architectural validation / consensus planning is still desirable
- **Next Recommended Step:** Use the approved planning artifacts with `$autopilot`, `$impl`, or `$team` depending on the desired execution style

### 2. **`$autopilot`**
- **Input Artifact:** the current deep-interview summary / requirements brief
- **Invocation:** `$autopilot <brief>`
- **Consumer Behavior:** Use the deep-interview spec as the clarified execution brief. Preserve intent, non-goals, decision boundaries, and acceptance criteria as binding context for planning/execution.
- **Skipped / Already-Satisfied Stages:** Initial requirement discovery and ambiguity reduction
- **Expected Output:** Planning/execution progress, QA evidence, and validation artifacts produced by autopilot
- **Best When:** The clarified spec is already strong enough for direct planning + execution without an additional consensus gate
- **Next Recommended Step:** Continue through autopilot's execution/QA/validation flow; if coordination-heavy execution emerges, prefer a follow-up `$team` or `$impl` pass as appropriate

### 3. **`$impl`**
- **Input Artifact:** the selected ticket plus the current deep-interview summary / requirements brief
- **Invocation:** `$impl <ticket>`
- **Consumer Behavior:** Use the ticket's acceptance criteria and boundary constraints as the execution target. Do not reopen requirements discovery unless the user explicitly asks to refine further.
- **Skipped / Already-Satisfied Stages:** Requirement interview, ambiguity clarification, and initial scope-definition work
- **Expected Output:** iterative execution progress plus QA/review evidence tracked against the clarified criteria
- **Best When:** The task is ready for one selected-ticket build loop with implementation, QA, review, and evidence collection
- **Next Recommended Step:** Continue re-entering the same `$impl` contract until the criteria are satisfied or a real blocker exists

### 4. **`$team`**
- **Input Artifact:** the current deep-interview summary / requirements brief
- **Invocation:** `$team <brief>`
- **Consumer Behavior:** Treat the spec as shared execution context for coordinated parallel work. Preserve the clarified intent, non-goals, decision boundaries, and acceptance criteria as common lane constraints.
- **Skipped / Already-Satisfied Stages:** Requirement clarification and early ambiguity reduction
- **Expected Output:** Coordinated multi-agent execution against the shared spec, with evidence that can later feed an `$impl` verification pass when appropriate
- **Best When:** The task is large, multi-lane, or blocker-sensitive enough to justify coordinated parallel execution instead of a single persistent loop
- **Next Recommended Step:** Follow the team verification path when the coordinated execution phase finishes; escalate to a separate `$impl` re-entry loop only when a later persistent verification/fix owner is still needed

### 5. **Refine further**
- **Input Artifact:** existing ticket context, current interview summary, and the current requirements brief
- **Invocation:** Continue the interview loop
- **Consumer Behavior:** Re-enter questioning to resolve the highest-leverage remaining uncertainty
- **Skipped / Already-Satisfied Stages:** None beyond already-captured context
- **Expected Output:** A lower-ambiguity spec with tighter boundaries and fewer unresolved assumptions
- **Best When:** Residual ambiguity is still too high, the user wants stronger clarity, or the above-threshold / early-exit warning indicates too much risk to proceed cleanly
- **Next Recommended Step:** Return to one of the execution handoff contracts above once the spec is sufficiently clarified

**Residual-Risk Rule:** If the interview ended via early exit, hard-cap completion, or above-threshold proceed-with-warning, explicitly preserve that residual-risk state in the handoff so the downstream skill knows it inherited a partially clarified brief.

**IMPORTANT:** Deep-interview is a requirements mode. On handoff, invoke the selected skill using the contract above. **Do NOT implement directly** inside deep-interview.

</Steps>

<Tool_Usage>
- Use `explore` for codebase fact gathering
- Use `request_user_input` / structured user-input tool for each interview round when available
- If structured question tools are unavailable, use plain-text single-question rounds and keep the same stage order
- Use `state_write` / `state_read` for resumable mode state
- Reuse the active ticket, linked docs, and mode state as the live context surface; do not create hidden sidecar artifacts
- Save durable interview outputs on current Farplane surfaces such as the active ticket, or hand the brief to `prd` when `docs/prd.md` is the next owner
</Tool_Usage>

<Escalation_And_Stop_Conditions>
- User says stop/cancel/abort -> persist state and stop
- Ambiguity stalls for 3 rounds (+/- 0.05) -> force Ontologist mode once
- Max rounds reached -> proceed with explicit residual-risk warning
- All dimensions >= 0.9 -> allow early crystallization even before max rounds
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] Preflight context snapshot exists in mode state and, when applicable, the active ticket
- [ ] Ambiguity score shown each round
- [ ] Intent-first stage priority used before implementation detail
- [ ] Weakest-dimension targeting used within the active stage
- [ ] At least one explicit assumption probe happened before crystallization
- [ ] At least one persistent follow-up / pressure pass deepened a prior answer
- [ ] Challenge modes triggered at thresholds (when applicable)
- [ ] Interview summary written to the active ticket or the current response handoff
- [ ] Requirements brief written to the active ticket or the selected Farplane handoff artifact
- [ ] Brownfield questions use evidence-backed confirmation when applicable
- [ ] Handoff options provided (`$deep-init-project`, `$impl-plan`, `$autopilot`, `$impl`, `$team`)
- [ ] No direct implementation performed in this mode
</Final_Checklist>

<Advanced>
## Suggested Config (optional)

```toml
[farplane.deepInterview]
defaultProfile = "standard"
quickThreshold = 0.30
standardThreshold = 0.20
deepThreshold = 0.15
quickMaxRounds = 5
standardMaxRounds = 12
deepMaxRounds = 20
enableChallengeModes = true
```

## Resume

If interrupted, rerun `$deep-interview`. Resume from persisted mode state via `state_read(mode="deep-interview")`.

## Recommended 3-Stage Pipeline

```
deep-interview -> impl-plan -> autopilot
```

- Stage 1 (deep-interview): clarity gate
- Stage 2 (impl-plan): feasibility + architecture gate
- Stage 3 (autopilot): execution + QA + validation gate
</Advanced>

Task: {{ARGUMENTS}}
