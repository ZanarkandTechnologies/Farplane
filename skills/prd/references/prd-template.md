# PRD Template

Use this template to create `docs/prd.md`.

## Workflow

1. Ask 3-8 clarifying questions (only where ambiguity affects implementation).
2. Confirm scope and non-goals.
3. Write PRD using the structure below.
4. Stop after PRD; do not implement in this phase.

## Clarifying Question Pattern

Prefer concise option-based questions when possible:

1. What is the primary user outcome?
   A) ...
   B) ...
   C) ...

2. Which scope do we ship first?
   A) MVP
   B) Expanded
   C) Backend-only
   D) UI-only

## Required Structure

```markdown
# PRD: [Feature Name]

## Problem / Context
[What pain exists and why it matters]

## Audience
[Primary and secondary users]

## JTBD
When [context], I want to [action], so I can [outcome].

## SLC Slice (Next Release)
[Smallest complete valuable slice]

## Goals
- [Measurable objective]

## Non-Goals
- [Explicitly out of scope]

## User Stories
### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] Observable criterion
- [ ] Error-path criterion
- [ ] Typecheck passes
- [ ] [UI stories only] Verify in browser using dev-browser skill

## Functional Requirements
- FR-1: ...
- FR-2: ...

## Constraints
- Security/privacy:
- Performance:
- Platform:
- Budget/time:

## Risks / Unknowns
- [Top unknown that might change approach]

## Backpressure / Evidence to Ship
- Tests:
- QA:
- Perf checks:
```

## Quality Checklist

- Acceptance criteria are verifiable, not vague.
- Non-goals clearly prevent scope creep.
- Success definition is observable.
- Scope aligns to one SLC slice.

## Example

Use the required structure above as the canonical PRD template.
