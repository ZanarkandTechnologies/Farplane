---
template_id: human-report-template
template_version: "0.1.0"
feature_refs:
  - FEAT-0060
  - FEAT-0070
kind: human-report
consumer_scope: report-prototype
applies_to:
  - tickets/archive/TASK-0348/artifacts/prototype/dogfood-after.md
---

# Human Report Template

Use this template for analytical reports whose main job is to help a person
understand what matters and decide what happens next. Keep canonical machine
state, exhaustive evidence, and long receipts in linked supporting artifacts.

```text
human_report(source_evidence, report_kind, template)
  -> decision_report + supporting_evidence_refs
```

## Report contract

Start with the answer. A reader should understand the decision, current state,
main risk, and next action without opening supporting evidence.

```markdown
---
ref: <canonical report ref when indexed>
kind: <report kind>
created_at: <ISO-8601 timestamp>
ui_summary: <plain-language result under 100 words>
template_uses:
  human-report-template: "0.1.0"
---

# <Outcome-oriented title>

## Decision

<Two to five sentences: result, why it matters, and the recommended action.>

## Situation map

<One compact Mermaid diagram when relationships, flow, or state are easier to
scan visually. Omit it when prose or a tiny table is clearer.>

## Material findings

| Finding | Why it matters | Evidence |
| --- | --- | --- |
| <only decision-relevant findings> | <impact> | <link or compact ref> |

## Risks and unknowns

- <Only risks or gaps that could change the decision or next action.>

## Next action

- **Owner / action:** <one concrete next move>
- **Proof:** <observable success or stop condition>

## Supporting evidence

- [Canonical receipt](<path>) — include only when the report carries structured
  authority, mutation, validation, or stop state; otherwise omit this row.
- [Source evidence](<path>) — exhaustive detail retained outside the reading path.
```

## Keep, move, remove

| Keep in the report | Move to supporting evidence | Remove |
| --- | --- | --- |
| decision, material findings, decision-changing risks, next action | machine receipts, exhaustive ledgers, raw observations, policy definitions | empty sections, repeated summaries, instructions to the report generator, duplicate evidence |

Do not delete proof to make a report shorter. Link it from the report and keep
the canonical artifact at its owning path.

## Diagram rule

Use at most one primary diagram in the reading path. It should explain a
relationship that prose hides: current-to-next state, competing paths, or the
flow from evidence to decision. Give nodes short human labels. Do not diagram a
single fact or repeat the surrounding paragraph.

## Specialization points

Report-producing skills may add a small domain section only when it changes the
decision, such as an experiment result, ranked candidate table, or failure
reproduction. Domain-specific machine fields belong in the receipt or source
artifact unless a human must read them to act.

## Quality examples

High signal:

> No experiment is active. Admit one immediate Dogfood dedupe eval; do not
> create recovery work because TASK-0338 already owns the failure.

Low signal:

> The report reviewed the portfolio according to the allowed state taxonomy,
> repeated all empty ledgers, restated workflow policy, and then reported that
> no experiment was found.
