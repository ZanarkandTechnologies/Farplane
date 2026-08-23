---
title: Skill portfolio rationalization audit
owner: skill-maintenance
status: reviewed
date: 2026-08-20
scope: 125 source/registry Farplane skill packages; live-only drift audited separately
review_route: reviewer
review_tas: TAS-A
reasoning_basis: operator-confirmed surface model + skill contracts + registry + hook evidence
scorecard: 2026-08-20-skill-portfolio-scorecard.csv
implementation_ref: 2026-08-20-skill-portfolio-migration.md
live_catalog_correction_ref: 2026-08-21-live-skill-catalog-drift.md
eval_required: no
eval_skip_reason: planning audit only; no skill behavior changed
---

# Skill Portfolio Rationalization Audit

## Decision

Do not implement the earlier 53-package reduction. It incorrectly treated some
advisor artifacts as parents of implementation-plan artifacts. The corrected
model separates the human entrypoint from the artifact dependency graph.

The recommended source portfolio is 117 packages:

| Treatment | Count | Public behavior |
| --- | ---: | --- |
| Core artifact skills | 42 | Available to ordinary Farplane work. |
| Domain artifact skills | 46 | Equipped through a project profile or specialist agent. |
| Configured integrations | 18 | Enabled in discovery only when the provider/tool profile is selected. |
| Explicit prompt shortcuts | 11 | User-callable only; excluded from skill composition. |
| Merge into an artifact owner | 2 | Preserve unique behavior, then remove the old package. |
| Retire into native/inline behavior | 6 | Remove the package after callers are rewritten. |
| Total | 125 | Every registry row has one disposition. |

This keeps 117 source packages but makes the ordinary composition surface much
smaller: 42 core artifacts. The 11 shortcuts remain in a separate operator
palette, while domain and integration packages appear only with a relevant
agent, project profile, or configured provider.

## Surface model

```text
specialist_agent(conversation, context)
  -> advice + accepted_domain_artifact?
  -> call(artifact_skill | integration_skill)

artifact_skill(inputs, accepted_context)
  -> durable_artifact | verdict + evidence

integration_skill(bound_provider, request)
  -> external_report | gated_side_effect + receipt

prompt_shortcut(explicit_user_text)
  -> transformed_response
```

### Specialist agents

Agents are conversational entrypoints: who the operator wants to talk with.
They own identity, domain judgment, clarification, and orchestration. They do
not replace stable artifact contracts.

The scorecard assigns each retained domain skill to a suggested agent bundle.
Existing roles such as `asset-generator`, `frontend-designer`,
`deep-researcher`, `planner-agent`, `qa-tester`, and `reviewer` should equip the
relevant skills. The main missing entrypoints are advertising, content, growth,
and harness specialists; creating them is a later reviewed implementation, not
part of this audit.

### Artifact skills

An artifact skill survives when it owns a repeatable durable artifact, verdict,
or proof boundary. Advisor-named packages can qualify: the suffix describes
domain judgment, not lifecycle parenthood.

### Integration skills

An integration survives when it owns credentials, provider behavior, external
state, a tool-specific report, or an approval boundary. Low frequency usually
makes it configured/optional, not deletable.

### Prompt shortcuts

`advise`, `brainstorm`, `commit-message`, `deep-interview`,
`deliberative-advice`, `diagramming`, `problem-framing`, `reshape-feasible`,
`skill-registry-ui`, `task-recap`, and `unslop` remain technically
packaged for explicit operator invocation.

They should be minimal, absent from automatic routing and skill-to-skill todo
links, and excluded from composition heat. Their value is prompt compression
and human augmentation, not being reusable workflow dependencies.

### Inline/native behavior

Universal rules, native phases, and thin command mnemonics are not skills.
`bash-efficiency`, `execute`, `find-skills`, `plan`, `summarize`, and `testing`
should retire after their useful rules, references, or callers move to the
native/global owner or an artifact-producing proof workflow.

### CLI wrapper boundary

A package should not survive merely to tell another skill to invoke a CLI.
When the only reusable behavior is command spelling and flags, the caller
should execute the exact command and own its expected output. `summarize` falls
on this side of the boundary: callers can invoke the `summarize` binary
directly, while source-safety, provenance, and quote-limit rules move to the
caller or their shared policy owner.

A CLI-backed skill can still survive when it owns more than command syntax:
credential or account binding, mutable external state, approval or spend
boundaries, asynchronous retry/polling, provider-specific normalization and
error handling, or a reusable receipt. CLI usage is therefore a diagnostic,
not an automatic retirement rule.

### Budget ensemble boundary

`budget-advisor` remains a core artifact skill. It compiles a Budget Program
with route, persona prompts, resolved parameters, synthesis, child-budget
policy, stop condition, guardrails, and blockers. That is a reusable ensemble
execution contract, not caller-owned effort wording or a response format.

## Corrected advisor and implementation-plan ownership

`ad-advisor` and `ad-impl-plan` both score 9/10 and remain separate.

```text
human
  -> advertising specialist agent
  -> ad-advisor
  -> accepted campaign config / campaign lock
  -> ad-impl-plan
  -> canonical campaign ticket
```

The specialist agent is the public conversational entrypoint. `ad-advisor`
owns campaign judgment and its accepted brief. `ad-impl-plan` is the artifact
parent for ticket creation and consumes or blocks on that brief. This is
already the direction of the current `ad-impl-plan` contract; the prior audit
would have inverted it.

Apply the same test elsewhere: keep a specialist artifact separate from an
implementation ticket when each has an independent acceptance point. Do not
merge merely because one calls the other.

## Usefulness score

The scorecard gives every package an operator-usefulness judgment from 1 to 10.
It is deliberately not an opaque composite maintenance score:

- `9-10`: losing it would materially damage a common or critical workflow.
- `7-8`: useful and distinct, but domain-, profile-, or provider-dependent.
- `5-6`: useful behavior exists, but overlap or narrowness makes it a merge or
  optional-package candidate.
- `1-4`: native behavior, thin routing, duplicated output, or maintenance cost
  outweighs a separate public package.

The disposition also considers uniqueness, proof boundary, integration state,
and overlap. Frequency remains a separate raw signal.

In the CSV, `current_surface` classifies what the package primarily does now.
`recommendation` describes its proposed retained treatment. The surface totals
therefore differ from the future portfolio counts above; they are not two
competing inventories.

## Usage evidence and count-hook finding

The repo does not currently have a reliable skill invocation-count hook.

`UserPromptSubmit` recognizes only seven hard-coded `$name` controls. Its regex
requires whitespace before `$`, so it misses the Codex app's linked syntax such
as `[$brainstorm](.../SKILL.md)`. It records explicit request heat, not whether
the agent loaded, ran, or completed the skill.

The root cause is scope drift: this began as a narrow control-surface detector,
then its `skill_requested` events were reused as portfolio heat. The detector
never became registry-driven, and no runtime bridge was added for actual skill
load/completion events. The hook is therefore working at its original narrow
job but is mislabeled and insufficient as invocation telemetry.

Current raw and filtered history contains:

| Skill | Raw request rows | Deduped requests | Non-synthetic requests | Latest non-synthetic |
| --- | ---: | ---: | ---: | --- |
| `impl-plan` | 10 | 9 | 8 | 2026-06-30 |
| `brainstorm` | 7 | 7 | 7 | 2026-06-06 |
| Every other current registry skill | 0 | 0 | 0 | not observed |

The scorecard uses the non-synthetic column. The exact filter is:

```text
read .farplane/events/*.jsonl
keep event_type == "skill_requested"
dedupe by (skill_name, session_id, turn_id)
exclude session_id starting "sess-"
exclude metadata.cwd starting "/var/folders/"
count by skill_name
```

The raw `impl-plan` latest is 2026-07-03 because it includes the excluded
fixture rows; the last filtered operator request is 2026-06-30.

These numbers have low coverage and must not be read as true use. This audit's
recent `lean-check` and `brainstorm` requests were not captured, directly
proving the false-zero problem.

The smallest honest telemetry improvement is two-stage:

1. Count explicit operator requests dynamically from the installed registry,
   supporting both `$name` and `[$name](...)`; label them
   `user_explicit_request`.
2. Where the Codex runtime exposes `item.completed` records with
   `item.type = skill`, ingest them as `agent_selected`; associate a completion
   or artifact reference when available. Do not infer actual execution from a
   prompt mention.

```text
skill_use(skill_id, source, status, outcome_ref?)
  -> timestamped_usage_event

source := user_explicit_request | agent_selected | skill_to_skill
status := requested | loaded | completed | blocked
```

Raw calls should be normalized by opportunity before influencing deletion: a
closeout skill may run rarely but on every completed ticket, while an
integration may be critical despite few eligible tasks.

## Merge candidates: 2

| Remove | Surviving artifact owner | Reason |
| --- | --- | --- |
| `external-patterns` | `research` | Code-pattern evidence is a research output, not a separate lifecycle. |
| `knowledge-tidier` | `consolidate` | Same keep/move/delete artifact cleanup and loss-check boundary. |

No merge folds an implementation-plan ticket into its advisor.

## Contracts that blocked forced merges

The following packages looked adjacent but remain separate after inspecting
their source contracts:

- `agency-opportunity-research` owns an archetype/company OpportunityCase;
  `customer-research` owns a person/ICP conversation report.
- `demo-realism` owns an upstream realism and demo-data pack;
  `functional-ui` owns an interaction model and wireflow.
- `first-value-outreach` owns a pre-commercial useful contribution;
  `personalized-offer` requires an accepted use case and owns a commercial
  offer package.
- `dogfood-review` owns a specialized self-improvement portfolio checkpoint;
  it is not interchangeable with a general Daily/Weekly interval report.
- `optimize-with-human` owns a feedback protocol, phase binding, and Goal
  packet references; `goal-advisor` owns the parent Goal architecture.
- `plan-next-wave` is a pure no-write selector; `pulse-update` is the
  materializer and control loop that consumes its decision.
- `remotion-render` owns the external `inference.sh` compute/spend contract;
  `remotion` owns composition authoring and local proof.
- `web-design-guidelines` owns a source-fresh code audit independent of the
  screenshots required by `visual-qa`.

`skill-registry-ui` is retained as an explicit operator shortcut for opening
and inspecting the generated registry UI. `visual-reasoning` is retained as a
domain artifact skill because it creates a checkpointed visual workspace and
evidence-grounded answer rather than merely reformatting a response.

## Retire candidates: 6

| Remove | Preserve in |
| --- | --- |
| `bash-efficiency` | Global shell guidance and `bash-operator`. |
| `execute` | Native Codex execution phase. |
| `find-skills` | Native skill/plugin discovery and installation. |
| `plan` | Native planning; `impl-plan` remains for a durable ticket artifact. |
| `summarize` | Callers invoke the `summarize` CLI directly and retain the required source-safety and grounding rules. |
| `testing` | Native test selection plus `proof-advisor`/`qa` references; it is a thin router without its own artifact. |

## Migration program

1. Fix request telemetry before using frequency to demote any unique skill.
2. Create the explicit-only shortcut palette and remove shortcut references
   from automatic skill composition without deleting shortcut packages.
3. Bind domain artifact and integration packages to project profiles and
   specialist-agent bundles so they do not crowd every task.
4. Prove the merge shape on `external-patterns -> research`; preserve source
   selection, evidence fields, references, tests, and outputs before deleting
   the old package.
5. Apply `knowledge-tidier -> consolidate` only after a knowledge-pruning
   fixture proves its retention, provenance, and loss-check behavior survives.
6. Retire the six native/inline packages only after active callers and global
   policy have moved. For `summarize`, rewrite callers to execute the CLI
   command directly and relocate its source-safety and grounding rules before
   deleting the package. Use no aliases or fallback parsers.
7. Re-score after at least 30 days of corrected explicit-request telemetry and
   available runtime skill-load evidence. A first zero-use report produces
   `watch`, not deletion.

## Evidence and limits

- Full scored inventory: [portfolio scorecard](2026-08-20-skill-portfolio-scorecard.csv).
- Registry coverage: all 125 rows classified exactly once.
- Current skill-system validation passed before any proposed migration.
- Usage count is low-confidence request heat; actual invocation count is
  unavailable from the current hook surface.
- This audit changes planning artifacts only. It does not delete, edit, or
  reinstall skill packages.
- The accepted plan was subsequently implemented and proved in the
  [migration audit](2026-08-20-skill-portfolio-migration.md).
- Correction: this audit classified the source/registry portfolio, not every
  discoverable package in the live Codex home. Nine previously retired
  top-level packages and three nested test-fixture skills survived outside the
  registry and were physically removed in the
  [live catalog drift audit](2026-08-21-live-skill-catalog-drift.md).

## Skill-maintenance QA

```yaml
expected_behavior: classify every skill under the confirmed agent/artifact/integration/shortcut model
current_behavior: one global catalog conflates entrypoints, artifacts, integrations, shortcuts, and native phases
mode: audit
owner_surface: skill-maintenance audit + scored inventory
first_load_sufficiency: not_applicable
workflow_duplication: pass
composition_clarity: pass
proof_surface_fit: pass
lean_owner_reuse: pass
eval_skip_reason: planning-only audit with no runtime skill changes
highest_risk: low-confidence usage data creates false retirement confidence
mitigation: separate usefulness from raw calls and require corrected telemetry plus repeated review before unique-capability deletion
review_result: TAS-A
```
