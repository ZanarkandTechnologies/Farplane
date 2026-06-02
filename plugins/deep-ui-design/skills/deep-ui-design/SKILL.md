---
name: deep-ui-design
description: Socratic deep UI taste interview with ambiguity gating before visual implementation. Use when workflow is clear but the user's aesthetic direction, taste boundaries, and anti-generic preferences are still unclear.
tier: 2
source: local
argument-hint: "[--quick|--standard|--deep] <product, page, feature, or visual direction>"
allowed-tools: Read, Glob, Grep
---

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Read the current UI/product context first: active ticket, `docs/prd.md`,
  `docs/specs/`, screenshots if present, nearby UI code, and existing taste or
  design notes.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to ground
  observed UI facts and avoid asking the user for discoverable context.
- [ ] Ask one taste question per round and target the weakest taste dimension.
- [ ] Require the gates: emotional tone, originality, references,
  anti-references, anti-goals, taste boundaries, and one pressure pass.
- [ ] Use [advise](../advise/SKILL.md) when competing visual directions need a
  recommended path.
- [ ] Use [review](../review/SKILL.md) before handing off a Taste Brief as
  ready for visual or frontend implementation.
- [ ] Write the Taste Brief into the active ticket, UI spec, or next canonical
  artifact owner.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

<Purpose>
Deep UI Design is a taste-first Socratic clarification loop before visual implementation. It turns vague statements like "make it feel premium" or "I do not want AI slop" into a reusable `Taste Brief` with explicit references, anti-references, typography direction, density, motion, component doctrine, and anti-patterns.
</Purpose>

<Use_When>
- The workflow is already mostly clear, but the look/feel is not
- The user wants a distinctive style instead of generic AI-default UI
- The user says "deep UI design", "extract my taste", "ask me design questions", "figure out the vibe", or "do not make this look the same as everything else"
- `functional-ui` has already clarified how the product should work, but `visual-design` or `frontend-craft` still lacks a strong visual brief
- You need a reusable intermediate spec between product/workflow intent and visual build execution
</Use_When>

<Do_Not_Use_When>
- The task is about workflow, IA, or interaction structure rather than aesthetics; use `functional-ui`
- A strong visual system or brand brief already exists and implementation should begin
- The request is pure visual polish on an already chosen direction; use `visual-design`
- The request is implementation on an already chosen direction; use `frontend-craft`
- The task is a final UI review; use `visual-qa` or `web-design-guidelines`
</Do_Not_Use_When>

<Why_This_Exists>
Strong frontend implementation is usually bottlenecked by taste clarity, not just component availability. A single style pass often misses what the user actually likes, what they reject, how bold they want to be, and which reusable design rules should constrain later page/component generation. This workflow applies Socratic pressure plus ambiguity scoring so visual build modes start from an explicit, non-generic, reusable aesthetic brief.
</Why_This_Exists>

<Depth_Profiles>
- **Quick (`--quick`)**: fast taste pass; target threshold `<= 0.30`; max rounds 5
- **Standard (`--standard`, default)**: full taste interview; target threshold `<= 0.20`; max rounds 12
- **Deep (`--deep`)**: high-rigor taste extraction; target threshold `<= 0.15`; max rounds 20

If no flag is provided, use **Standard**.
</Depth_Profiles>

<Execution_Policy>
- Ask ONE question per round (never batch)
- Ask about emotional tone and anti-slop boundaries before implementation details
- Target the weakest taste dimension each round after applying the stage-priority rules below
- Treat every answer as a claim to pressure-test before moving on: the next question should usually force a reference, anti-reference, tradeoff, or concrete reusable rule
- Do not rotate to a new taste dimension just for coverage when the current answer is still vague; stay on the same thread until the taste becomes reusable
- Before crystallizing, complete at least one explicit pressure pass that revisits an earlier answer with a sharper contradiction, reference interrogation, or safer-vs-bolder tradeoff
- Gather current UI context before asking the user about brownfield internals; do not ask the user for codebase facts you can inspect directly
- For brownfield work, prefer evidence-backed confirmation questions such as "The current product uses dense monochrome tables and restrained motion. Should the new taste brief preserve that discipline or intentionally break from it?"
- Always run a preflight context intake before the first interview question
- Reduce user effort: ask only the highest-leverage unresolved question
- In Codex CLI, prefer `request_user_input` when available; otherwise use concise plain-text one-question turns
- Re-score ambiguity after each answer and show progress transparently
- Do not hand off to implementation while ambiguity remains above threshold unless the user explicitly opts to proceed with warning
- Do not crystallize or hand off while `Anti-goals`, `Taste Boundaries`,
  visual `Autonomy Readiness`, or the required readiness gates remain
  unresolved, even if the weighted ambiguity threshold is met
- Treat early exit as a safety valve, not the default success path
- Persist mode state for resume safety (`state_write` / `state_read`)
</Execution_Policy>

<Steps>

## Phase 0: Preflight Context Intake

1. Parse `{{ARGUMENTS}}` and derive a short task slug.
2. Attempt to load the latest relevant context from the active ticket, linked UI docs, existing taste notes, and any persisted `state_read(mode="deep-ui-design")` snapshot.
3. Inspect the current UI surface when the task is brownfield:
   - relevant tickets/specs
   - `docs/TASTE.md` if present
   - nearby UI code, screenshots, or existing routes/components
4. If no snapshot exists, create a minimum context snapshot with:
   - Task statement
   - Product/workflow context
   - Stated visual ask
   - Probable taste hypothesis
   - Known references or anti-references
   - Constraints
   - Unknowns/open questions
   - Taste-boundary unknowns
   - Likely visual surfaces/components
5. Persist the snapshot in mode state and, when a ticket already exists, mirror the key points into the ticket `Working Notes` instead of creating sidecar runtime artifacts.

## Phase 1: Initialize

1. Parse `{{ARGUMENTS}}` and depth profile (`--quick|--standard|--deep`).
2. Detect project context:
   - classify **brownfield** (existing UI/design system) vs **greenfield**
   - for brownfield, collect the relevant visual context before questioning
3. Initialize state via `state_write(mode="deep-ui-design")`:

```json
{
  "active": true,
  "current_phase": "deep-ui-design",
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
    "visual_context": null,
    "current_stage": "tone-first",
    "current_focus": "emotional-tone",
    "context_surface": "ticket:<path>#Working Notes | state:deep-ui-design.context_snapshot"
  }
}
```

4. Announce kickoff with profile, threshold, and current ambiguity.

## Phase 2: Socratic Taste Loop

Repeat until ambiguity `<= threshold`, the pressure pass is complete, the readiness gates are explicit, the user exits with warning, or max rounds are reached.

### 2a) Generate next question

Use:
- Original idea
- Prior Q&A rounds
- Current dimension scores
- Brownfield visual context (if any)
- Activated challenge mode injection (Phase 3)

Target the lowest-scoring dimension, but respect stage priority:
- **Stage 1 — Tone-first:** Emotional Tone, Originality, Anti-goals, Taste Boundaries
- **Stage 2 — Reference-first:** Reference Quality, Anti-reference Clarity
- **Stage 3 — System taste:** Typography, Color/Material, Density/Spacing, Motion, Texture, Component Doctrine
- **Stage 4 — Brownfield grounding:** Context Clarity (brownfield only)

Follow-up pressure ladder after each answer:
1. Ask for a concrete reference, screenshot style, or real product that demonstrates the claim
2. Ask what specifically is liked or disliked, not just the name of the reference
3. Force a tradeoff: safer vs bolder, denser vs lighter, louder vs more restrained
4. Convert the answer into a reusable rule for pages/components

Prefer staying on the same thread for multiple rounds when it has the highest leverage. Breadth without pressure is not progress.

Detailed dimensions:
- Emotional Tone Clarity — what the interface should feel like
- Originality Clarity — how far from generic/default the design should push
- Reference Quality — strength and specificity of positive references
- Anti-reference Clarity — what must not appear
- Typography Direction Clarity — type families, contrast, hierarchy appetite
- Color/Material Clarity — palette, finish, texture, atmosphere
- Density/Spacing Clarity — compactness, whitespace, rhythm
- Motion Language Clarity — animation appetite, tempo, restraint
- Component Doctrine Clarity — how cards, buttons, panels, navigation, and forms should behave visually
- Context Clarity — existing design-system understanding (brownfield only)

`Anti-goals` and `Taste Boundaries` are mandatory readiness gates. Ask about them early and keep revisiting them until they are explicit.

### 2b) Ask the question

Use structured user-input tooling available in the runtime (`AskUserQuestion` / equivalent) and present:

```text
Round {n} | Target: {weakest_dimension} | Ambiguity: {score}%

{question}
```

### 2c) Score ambiguity

Score each weighted dimension in `[0.0, 1.0]` with justification + gap.

Greenfield:

`ambiguity = 1 - (tone × 0.20 + originality × 0.12 + references × 0.15 + anti_references × 0.10 + typography × 0.10 + color_material × 0.10 + density × 0.08 + motion × 0.05 + component_doctrine × 0.10)`

Brownfield:

`ambiguity = 1 - (tone × 0.18 + originality × 0.10 + references × 0.14 + anti_references × 0.08 + typography × 0.10 + color_material × 0.10 + density × 0.08 + motion × 0.05 + component_doctrine × 0.10 + context × 0.07)`

Readiness gate:
- `Anti-goals` must be explicit
- `Taste Boundaries` must be explicit
- At least two strong positive references must be named or described concretely
- At least one anti-reference must be explicit
- Visual `Autonomy Readiness` must name hard-to-QA surfaces such as motion,
  canvas, drag/drop, timing, responsive breakpoints, screenshots, fixtures,
  browser paths, and human visual-review gates
- A pressure pass must be complete: at least one earlier answer has been revisited with a contradiction, specificity, or tradeoff follow-up
- If any gate is unresolved, continue interviewing even when weighted ambiguity is below threshold

### 2d) Report progress

Show the weighted breakdown table, readiness-gate status (`Anti-goals`, `Taste Boundaries`, `References`, `Anti-references`), and the next focus dimension.

### 2e) Persist state

Append the round result and updated scores via `state_write`.

### 2f) Round controls

- Do not offer early exit before the first explicit reference interrogation and one persistent follow-up have happened
- Round 4+: allow explicit early exit with risk warning
- Soft warning at profile midpoint (e.g. round 3/6/10 depending on profile)
- Hard cap at profile `max_rounds`

## Phase 3: Challenge Modes

Use each mode once when applicable. These are normal escalation tools, not rare rescue moves:

- **Reference Interrogator** (round 2+): challenge vague "I like Stripe/Linear/Apple" references by asking what exact qualities matter
- **Anti-Slop** (round 2+): force explicit rejection of generic patterns, fonts, palettes, or layout habits
- **Extremes** (round 3+): force a choice between safer and bolder variants to expose real taste tolerance
- **Consistency Check** (round 4+): revisit a contradiction between stated references and desired tone
- **Systemizer** (round 5+ or when the user keeps speaking in moods instead of reusable rules): translate mood into component/page doctrine

Track used modes in state to prevent repetition.

## Phase 4: Crystallize Artifacts

When threshold is met (or the user exits with warning / hard cap):

1. Write the interview transcript summary to:
   - the active ticket `Working Notes` / `Handoff` when a ticket already exists
   - otherwise the current response as a compact `Deep-UI-Design Summary`
2. Write the execution-ready taste artifact to:
   - `docs/TASTE.md` when that file exists
   - otherwise the active ticket when one already exists
   - otherwise the current response handoff plus the next canonical artifact owner, usually `visual-design`

### Canonical write-back rule

When the project has been bootstrapped with `deep-init-project`, `docs/TASTE.md` is
the canonical durable home for the full `Taste Brief`.

Use this write-back policy:

- full reusable visual doctrine -> `docs/TASTE.md`
- ticket-local summary, exceptions, or feature-specific deltas -> active ticket
- chat-only fallback -> current response when no durable project surface exists

Do not duplicate the full doctrine into every ticket. Tickets should reference
the shared taste doctrine briefly and only record local exceptions or
feature-specific emphasis.

The `Taste Brief` should include:
- Metadata (profile, rounds, final ambiguity, threshold, context type)
- Context snapshot reference/path
- Clarity breakdown table
- Emotional goal
- Experience adjectives
- Reference set
- Anti-reference set
- Typography doctrine
- Color/material doctrine
- Density/spacing doctrine
- Motion doctrine
- Visual Autonomy Readiness: browser path, stable states, screenshots/clips,
  hard-to-QA motion or responsive behavior, and human visual-review gates
- Component doctrine
- Hero moments
- Anti-goals / anti-slop rules
- Brownfield evidence vs inference notes for any repository-grounded confirmation questions
- Pressure-pass findings (which answer was revisited, and what changed)
- Full or condensed transcript

### Minimum acceptable `Taste Brief`

Do not exit with only aesthetic prose. The minimum brief must contain reusable build rules:

- at least 2 positive references
- at least 1 anti-reference
- explicit typography direction
- explicit density preference
- explicit color/material direction
- explicit motion comfort level
- explicit anti-slop rules
- explicit visual autonomy-readiness notes for motion, canvas, responsive, or
  subjective surfaces that QA cannot prove cheaply
- reusable guidance for buttons, cards/panels, navigation, and forms

If those are missing, the brief is not implementation-ready.

## Phase 5: Execution Bridge

Present execution options after artifact generation using explicit handoff contracts.

### 1. `visual-design` (Recommended)
- **Input Artifact:** the current `Taste Brief` plus any existing workflow plan from `functional-ui`
- **Consumer Behavior:** treat the `Taste Brief` as the visual source of truth; do not re-run taste extraction by default
- **Expected Output:** a visual brief and constraints that follow the extracted doctrine instead of falling back to generic defaults
- **Best When:** the workflow is already clear and the remaining uncertainty is visual execution

### 2. `landing-page`
- **Input Artifact:** the current `Taste Brief`
- **Consumer Behavior:** preserve the extracted emotional tone, references, motion appetite, and anti-slop rules in a narrative landing-page treatment
- **Best When:** the output is a marketing or narrative landing page rather than an app workflow

### 3. `frontend-craft`
- **Input Artifact:** the current `Taste Brief`, any `functional-ui` handoff, and the requested implementation scope
- **Consumer Behavior:** implement the frontend while preserving the taste doctrine and proof target
- **Best When:** the user has approved the direction and wants code now

### 4. `impl-plan`
- **Input Artifact:** the current `Taste Brief` plus the active ticket
- **Consumer Behavior:** preserve the taste doctrine in the plan and proof target; do not weaken it into generic UI language
- **Best When:** a ticket needs approval-ready implementation planning before build starts

## Top Gotchas

1. Do not confuse workflow questions with taste questions; `functional-ui` owns workflow.
2. Do not accept named references without asking what specifically is attractive or repulsive about them.
3. Do not crystallize a brief that lacks explicit anti-slop rules; otherwise `visual-design` or `frontend-craft` will still converge on generic output.

## Outcome Contract

When this skill is used, the response or artifact must include:

1. Interview metadata and final ambiguity score
2. Clarity breakdown table
3. Explicit readiness-gate status
4. A reusable `Taste Brief`, written to `docs/TASTE.md` when that surface exists
5. Reference and anti-reference set
6. Reusable component/page doctrine
7. Visual autonomy-readiness blockers and proof gates
8. Clear handoff target (`visual-design`, `landing-page`, `frontend-craft`, or `impl-plan`)

</Steps>
