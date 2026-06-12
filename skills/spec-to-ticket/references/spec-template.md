# Spec Template

Use this template to convert `docs/prd.md` into `docs/specs/*.md`.

## Core Rules

1. One topic per file.
2. Topic scope test: one sentence without "and".
3. Stories must be completable in one focused build loop.
4. Order by dependency (schema -> backend -> UI -> aggregation).
5. Every story includes "Typecheck passes".
6. UI stories include explicit agent testability and QA expectations, not just "verify in browser".

## Template

```markdown
# Spec: [Topic Title]

## Overview
[One paragraph summary]

## User Stories
### US-001: [Story Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Success Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Typecheck passes
- [ ] [UI stories only] Ticket defines a compact agent contract for access, inspection, and proof

## Functional Requirements
- FR-1: ...
- FR-2: ...

## Non-Goals
- ...
```

## Story Sizing Guide

Good size:
- Add schema field + migration.
- Add one endpoint/mutation with validation.
- Add one focused UI interaction.

Too large:
- "Build the entire dashboard."
- "Add authentication system end-to-end."

If a story cannot be explained in 2-3 sentences, split it.

## Success Criteria Quality

Good (verifiable):
- "Add `status` column defaulting to `pending`."
- "Filter has All/Active/Completed options."

Bad (vague):
- "Works well."
- "Good UX."

## Checklist

- Stories are small and dependency-ordered.
- Criteria are testable and explicit.
- Non-goals are stated.
- UI stories give enough detail for a later ticket to define access, key screens/states, and review evidence.
