---
title: JSON Canonical Farplane Contracts Council Context
status: draft
owner: codex
created_at: 2026-06-22
decision_type: deliberative-advice
---

# JSON Canonical Farplane Contracts Council Context

## Decision

Should Farplane standardize renderer-facing and machine-updated state on JSON,
with humans primarily reading and editing through the UI, while Markdown/YAML
remain derived or authoring views only where useful?

## Why This Matters

Farplane artifacts are likely to be rendered in a web portal. Goals, Goal
Packets, skill contracts, permission/read-write rules, proof packets, work
items, and progress logs need to be parsed, validated, edited, and displayed
reliably.

The operator is considering a stronger stance than the previous semantic-kernel
recommendation:

```text
canonical data = JSON
human surface = UI
AI update output = JSON
Markdown/YAML = optional views, docs, or context
math/function notation = explanatory only
```

## Prior Discussion Summary

The earlier council recommended one semantic kernel with multiple projections.
The operator now suspects that if humans can rely on a custom UI, then canonical
state should be JSON-first for parseability and renderer compatibility.

The operator provided evidence summaries:

- JSON is more reliable when AI must produce parseable machine output.
- YAML/Markdown may be better when AI must read or reason over large nested
  input.
- Farplane web portal surfaces need stable parse/update/render behavior.

## Current Behavior

Farplane currently has mixed source formats:

- Markdown documents and tickets.
- YAML frontmatter in skills, tickets, docs, and templates.
- Custom function/math notation in specs and skill signatures.
- TypeScript-like schemas in invocation/adapters specs.
- Python dataclasses/protocols for runtime helpers.
- JSON proof packets and runtime-like outputs in scripts.

The confusing surfaces include:

- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- `tickets/README.md` and ticket `Program`
- Goal Packet `ticket.md`, `program.md`, `progress.md`
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- skill `Skill Signature` and `Todo List`
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
- `docs/fundamentals/harness-algebra.md`

## Expected Behavior

The chosen policy should:

- make portal rendering straightforward;
- make machine updates and validation reliable;
- preserve enough human inspectability for git review, diffs, emergency edits,
  and agent debugging;
- avoid forcing humans to hand-edit ugly JSON for every workflow;
- avoid YAML parse fragility when exact AI-generated output matters;
- keep math notation useful for reasoning without making it source of truth.

## Options Under Consideration

### Option A: JSON Everywhere As Canonical Source

All portal-facing contracts, goals, run configs, progress logs, permissions,
proof, skill cards, work items, and integration envelopes are JSON files or
JSONL logs. Humans interact mainly through UI.

### Option B: JSON Canonical For Renderer-Critical State, Markdown/YAML Source For Docs And Skills

Use JSON for any object the UI must update or agents must output exactly.
Keep Markdown/YAML as source for long prose docs and low-risk skill
instructions, while generating JSON registries/contracts for the portal.

### Option C: Dual Source With JSON Generated From Markdown/YAML

Humans keep authoring Markdown/YAML. Build generators produce JSON for UI and
validation.

## Evidence Refs

- Clinical structured-output study: JSON had the highest parseability among
  JSON/YAML/XML for generated structured outputs from small language models.
  https://arxiv.org/html/2507.01810v1
- Prompt formatting study: prompt format matters, but no format is universally
  dominant across tasks and models.
  https://arxiv.org/html/2411.10541v1
- Improving Agents nested data experiment: YAML performed best for some small
  models on nested input; Markdown was token-efficient; JSON was not always the
  best input format.
  https://www.improvingagents.com/blog/best-nested-data-format/
- StructEval: structured output generation/conversion still has meaningful
  failure rates across formats and models.
  https://arxiv.org/html/2505.20139v1

## Relevant Local Files

- `experiments/decisions/2026-06-22-farplane-program-language-audit/decision-note.md`
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
- `docs/skills/system.md`
- `tickets/README.md`
- `templates/global/AGENTS.md`

## Constraints / Non-Goals

- Do not implement a migration during this advice pass.
- Do not require hand-editing verbose JSON for every human workflow unless the
  UI or tooling makes that reasonable.
- Do not break existing Markdown skill loading until a replacement is proven.
- Do not make YAML the required AI output format for exact parsing.
- Do not make math/function notation canonical source for UI-rendered data.
- Preserve git-diff reviewability and emergency local edits.

## Lane Briefs

### Operator Value

Judge whether JSON-canonical plus UI-first human interaction makes Farplane
easier to use, trust, review, and evolve.

### Engineering Risk

Judge schema/versioning/migration/tooling costs, UI dependency risk, merge
conflicts, diffs, validation, and update paths.

### Evidence Skeptic

Judge whether the external evidence supports JSON-canonical broadly or only
for AI-generated output. Name what evidence would change the call.

### Systems Fit

Judge which Farplane surfaces should become JSON canonical and which should
remain Markdown/YAML/docs-first. Preserve ownership boundaries.

### Product/UI Fit

Judge renderer implications: form generation, graph/timeline/card rendering,
permissions UI, review UX, and whether UI can replace human file reading.

## Output Shape

Each lane should return:

- `Perspective`
- `Recommendation`
- `Strongest reason`
- `Biggest risk`
- `Strongest opposing point`
- `Evidence that would change my mind`
- `Concrete policy constraints`

Chair synthesis should compare exactly three final options and recommend one.

## Proof / Next Owner

Likely next owner is a ticket for a JSON contract prototype:

```text
json_contract_prototype(goal, skill_contract, proof_packet, permission_model)
  -> json_schema + sample_json + renderer_mock + update_round_trip + migration_risks
```
