---
skill: consolidate
date: 2026-09-20
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: templates/global/AGENTS.md@0.2.41
after_ref: templates/global/AGENTS.md@0.3.0
reasoning_basis: first_principles
proof_artifacts:
  - templates/global/AGENTS.md
  - docs/systems/agent-kernel.md
  - docs/templates/global-agents-qa-checklist.md
  - bin/validators/check_harness_invariants.py
  - bin/validators/test_harness_invariants.py
  - skills/eval/examples/farplane-global-harness/tasks.json
  - skills/diagramming/audits/2026-09-20-mermaid-capability-routing.md
  - skills/consolidate/audits/2026-09-20-global-agents-eval-source-receipt.json
eval_required: yes
---

# Readable Global Agent Routing

## Change

- **Before:** Eight top-level policy sections mixed routing, procedures,
  guardrails, and response rules. Important behavior was present, but similar
  rules appeared in several places and the output contract relied mainly on
  prose.
- **After:** Three reader-facing sections—`Context`, `Behavior`, and `Output
  Formatting`—group the same operating contract. Comparable entry points use
  tables, output rules lead with worked examples, and detailed procedures stay
  with their owning skills, project policy, validators, or evals.
- **Example:** A comparison among direct execution, `impl-plan`, and
  `goal-advisor` now appears as one table with condition, output, and boundary
  columns instead of several separated bullets.
- **Expected:** Agents retain the original authority, safety, grounding,
  workflow, and proof behavior while producing guidance that is easier to scan
  and edit from examples.

The branch started from tracked template version `0.2.41`. An uncommitted
`0.2.43` intent-routing extension was also present in the operator's worktree;
its question-versus-correction behavior and paired evals are preserved in this
change rather than treated as the tracked baseline.

## First-Principles Placement

| Rule type | Placement | Reason |
| --- | --- | --- |
| Needed before any project or skill can route the task | Global template | Omission would change behavior in ordinary tasks. |
| Farplane-specific path, provider, or lifecycle detail | Project policy | It is not a cross-project invariant. |
| Specialized procedure or artifact contract | Owning skill | It should load only when that workflow applies. |
| Mechanical parity or regression condition | Validator or eval | Deterministic proof is stronger and cheaper than repeated prose. |

The rewrite keeps global rules for authority, intent classification,
independent reasoning, current evidence, lean implementation, context loading,
durable task state, skill routing, delegation, workspace safety, response shape,
visual choice, and completion proof. It removes the all-caps autonomy banner;
its behavioral requirements remain in active `Behavior` prose and validator
coverage.

## Feature Fidelity Map

| Original behavior group | New owner | Result |
| --- | --- | --- |
| Autonomy and authority | `Behavior / Classify intent and use authority` | Preserved, including genuine-question versus unfinished-action routing. |
| Decision and grounding | `Behavior / Reason from evidence` | Preserved with source routing in Context. |
| Correction, work, and proof | `Behavior / Execute leanly and prove the claim` | Preserved and consolidated with the build rung. |
| Response contract | `Output Formatting` | Preserved with example-led formats and a table threshold. |
| Context routing | `Context` and `Behavior / Load relevant context` | Preserved with local, docs, browser, and Computer Use routes. |
| Task state and artifacts | `Behavior / Load relevant context and preserve durable state` | Preserved with generic task-system and Goal guidance. |
| Skills and delegation | `Behavior / Use skills and delegation deliberately` | Preserved with phase entry points and bounded delegation. |
| Local workbench and safety | `Behavior / Operate the workspace safely` | Preserved, including checkout, shell, credential, install, and polling boundaries. |

## Readability Rubric

| Check | Pass condition |
| --- | --- |
| Grouping | Only Context, Behavior, and Output Formatting appear as level-two sections. |
| Rules | Each bullet carries one principal instruction with nearby conditions. |
| Multiple routes | Three or more comparable routes use a compact table when scanning improves. |
| Output formats | Material output rules begin with a quoted example before supporting constraints. |
| Change explanation | Policy, prompt, workflow, UX, and architecture changes show Before / After / Example. |
| Visual choice | The form follows the reader question; Mermaid is one supported form rather than the default. |
| Prompt load | Specialist procedures remain in owner surfaces and are referenced compactly. |

## Prompt Tax

| Measure | Tracked 0.2.41 | Candidate 0.3.0 | Tradeoff |
| --- | ---: | ---: | --- |
| Words | 1,835 | 2,892 | `+57.6%`; accepted for route tables, guardrail recovery, and worked output examples. |
| Nonblank lines | 205 | 308 | `+50.2%`; sections are longer but easier to scan by purpose. |
| Rule bullets | 48 | 46 | Slightly fewer bullets; comparable routes moved into nine tables. |

This is a readability expansion rather than prompt compaction. A later trim may
remove prose that merely restates a table, but only after behavior evals show no
loss. The current change favors explicit entry boundaries and inspectable output
formats at roughly 300 nonblank lines.

## Proof Plan

- Run Agent Kernel validator unit tests and the live invariant validator.
- Regenerate template and system registries from their source documents.
- Run the template metadata, system-doc, and skill-package checks.
- Run isolated-source prompt evals for intent routing, independent reasoning,
  lean execution, phase ownership, active-skill checklist behavior, quoted
  completion formatting, and table-based entry routes.
- Obtain an independent review of the final diff and record its verdict here.

The isolated-source suite produced TAS-A for all eight counted cases: independent
reasoning, warranted agreement, lean implementation, genuine and correction-
shaped install questions, phase-route tables, compact active-skill checklists,
and quoted multi-change handoffs. The exact final source hash and run bindings
are recorded in the adjacent eval receipt. Implementation showcase cases were
excluded from the source-only verdict because the temporary target contained no
fixture application or media surface to operate.

## Review Receipt

Independent first-principles rereview on 2026-09-20 returned **TAS-A — pass**
with no remaining blocker. It verified the corrected native Goal ownership,
all 11 required subsection guards, the exact prompt fingerprint, 8/8 counted
TAS-A behavior cases, honest excluded-case boundaries, prompt-tax figures,
diagramming ownership, and the final static checks.
