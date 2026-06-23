---
title: JSON Canonical Farplane Contracts Decision Note
status: draft
owner: codex
created_at: 2026-06-22
context_ref: experiments/decisions/2026-06-22-json-canonical-contracts/context.md
skill: deliberative-advice
---

# JSON Canonical Farplane Contracts Decision Note

## Decision

Use JSON as the canonical format for renderer-critical, machine-updated, and
schema-validated Farplane state.

Do not make all Farplane data JSON yet. Keep Markdown/YAML/docs-first surfaces
where humans and agents need long-form reasoning, instruction, review, and
doctrine until a schema-aware UI proves it can replace direct file reading.

## Stakes

Farplane is likely to render goals, skill contracts, permission models, proof,
progress, and integration state in a web portal. Those surfaces need reliable
parsing, validation, partial updates, and UI projection.

At the same time, Farplane's current strength is visible artifact memory:
operators and agents can inspect files, review diffs, recover from tool
failures, and understand why a workflow exists.

## Grounding

The external evidence supports a split policy:

- JSON is safest when an AI must produce parseable machine output.
- YAML/Markdown may be better when an AI must read nested input or humans need
  compact context.
- Structured output failures still matter across formats and models, so schema
  validation is required either way.

The local evidence supports a split policy too:

- Invocation, compute, work item, proof, eval, and runtime records are already
  object boundaries.
- Tickets, specs, skill instructions, and doctrine are prose-heavy human
  contracts.
- `.farplane/state/**` is runtime state and should not replace durable ticket
  or docs truth.

## Perspectives

### Operator Value

JSON canonical is good for machine confidence and portal rendering, but
UI-first cannot replace file trust until the UI is fast, transparent,
offline-tolerant, diff-aware, and recoverable.

### Engineering Risk

Full JSON canonicalization creates a platform obligation: schemas, version
migrations, validators, editor UX, semantic diffs, conflict handling, JSONL log
rules, and emergency edit paths.

### Evidence Skeptic

The evidence supports JSON for exact generated output, not JSON for all source
truth. Parseability does not prove better comprehension, reviewability, or
semantic correctness.

### Systems Fit

JSON belongs at typed object boundaries between systems, renderers, validators,
adapters, and agents. Markdown remains the durable human contract for
prose-heavy plans, specs, skills, and review reasoning.

### Product/UI Fit

JSON Schema can drive forms, cards, graphs, timelines, permissions panels,
review queues, and proof dashboards. But the UI must be an inspectable editor,
not a pretty viewer over opaque state.

## Critique / Ranking

### Option 1: JSON Canonical For Renderer-Critical State

Recommended.

This captures the parseability and UI benefits without turning all durable
memory into machine backing storage.

### Option 2: JSON Everywhere As Canonical Source

Too risky now.

It may become right later if the portal becomes an excellent schema-aware
editor with semantic diffs, migrations, emergency edit flows, and copyable
agent context. Today it would likely make Farplane less inspectable.

### Option 3: Markdown/YAML Source With Generated JSON

Useful for some existing surfaces, but insufficient for portal-owned objects.

If the portal must edit, filter, validate, and graph state, generated JSON from
Markdown extraction becomes brittle unless the Markdown is constrained enough
to become a worse schema.

## Recommendation

Adopt this policy:

```text
JSON canonical
  iff object is renderer-facing
  OR machine-updated
  OR emitted by AI for exact parsing
  OR runtime/integration/proof state
  OR schema validation is the main safety boundary

Markdown/YAML canonical
  iff object is prose-heavy
  OR instruction-heavy
  OR review/rationale/doctrine-heavy
  OR humans must hand-author and inspect it without tooling
```

## Concrete Classification

### JSON Canonical Now

- `FarplaneRunEnvelope`
- `ProofPacket`
- normalized `WorkItem`
- `ComputeDecision`
- `.farplane/state/**` runtime records
- eval task files and run summaries
- generated registries such as `docs/skills/registry.jsonl`
- future portal-owned permission models
- future portal-editable goal records
- future portal-editable ticket metadata projections

### JSONL Preferred

- append-only event/progress streams that the portal must filter or replay
- proof event history
- automation/run logs

### Markdown/YAML Canonical For Now

- `ticket.md` body contract and reasoning
- `program.md` while it remains operator-readable Goal loop configuration
- `progress.md` while it remains compact narrative execution history
- `SKILL.md` instructions, Todo Lists, and long-form references
- `docs/specs/*`
- `docs/fundamentals/*`
- `README.md`
- `ARCHITECTURE.md`
- decision notes and review narratives

### Derived Or Explanatory Only

- YAML views generated from JSON
- Markdown summaries generated from JSON
- math/function notation such as `skill(input, state) -> output + evidence`
- Mermaid diagrams

## Dissent

The strongest dissent favors JSON everywhere now.

The argument is that the portal is the product surface, exact parsing matters,
and human editing can move into UI forms. That would simplify update paths,
schema enforcement, renderer contracts, permissions, and graph/timeline
visualizations.

The council rejects that as the immediate default because the UI is not yet
proven as a full inspect/edit/diff/validate/recover surface.

## Tradeoff Accepted

Farplane accepts two source styles temporarily:

- JSON for typed object state.
- Markdown/YAML for human reasoning and instruction.

The tradeoff is extra projection work. The benefit is keeping Farplane
inspectable while the portal matures.

## Confidence

Medium-high.

Confidence is high that AI exact-output and portal-edited data should be JSON.
Confidence is medium that some Goal/ticket/skill surfaces should stay
Markdown/YAML long-term, because a strong UI prototype could change that.

## Policy Constraints

- Every JSON-canonical surface needs `$schema`, `schema_version`, stable IDs,
  owner, validator, sample fixture, migration rule, and renderer contract.
- Canonical JSON must be pretty-printed, deterministically ordered, and
  schema-validated.
- AI-generated durable state must be JSON and must pass validation before
  writeback.
- UI must expose raw JSON, validation errors, history/diffs, copyable context,
  and emergency edit guidance.
- Markdown/YAML views generated from JSON must be labeled derived.
- Runtime JSON under `.farplane/state/**` must not replace durable ticket or
  docs truth.
- Math/function notation is explanatory only, never canonical data.
- Permissions and review UX must render from explicit typed fields, not
  inferred prose.

## Next Owner

Create a ticket for a JSON contract prototype before changing the global policy.

Suggested title:

```text
TASK-XXXX Prototype JSON-canonical portal contracts for goals, permissions,
skill cards, and proof
```

## Proof / Evidence Gap

Prototype:

```text
json_contract_prototype(goal, skill_contract, proof_packet, permission_model)
  -> json_schema
   + sample_json
   + renderer_mock
   + schema_validation
   + semantic_diff
   + emergency_edit_flow
   + migration_risks
```

Pass condition:

- UI can create/edit/review the objects.
- JSON validates reliably.
- Git diffs are readable or semantic diffs exist.
- An agent can update the object as JSON without parse failures.
- A human can recover through raw JSON or CLI fallback when the UI is absent.
- Markdown/YAML rendered views are clearly derived and not competing truth.
