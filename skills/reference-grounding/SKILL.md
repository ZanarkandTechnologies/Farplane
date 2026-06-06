---
name: reference-grounding
version: 0.1.0
description: Tier 1 primitive for grounding recommendations, plans, and claims in local evidence, official docs, peer products, standards, maintained repos, or provided sources before stronger workflow skills consume them.
tier: 1
source: local
skill_template_version: "0.1.0"
allowed-tools: Read, Glob, Grep
---

# Reference Grounding

## Context

`reference-grounding` is a Tier 1 primitive for compact evidence. It should
ground one claim or decision, then hand the result back to the caller rather
than expanding into a full research pass.

Use when a recommendation, plan, or claim needs enough evidence to stop
guessing. This is the small evidence move, not a research router.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the one claim, decision, expectation, or comparison that needs
  grounding.
- [ ] 2. Capture the local baseline from nearby code, tickets, specs, docs, or
  provided sources when repo scope matters.
- [ ] 3. Choose the smallest useful source class: local evidence, official docs,
  standards, maintained repos, peer products, competitors, or user-provided
  sources.
- [ ] 4. Prefer primary sources and real implementations over commentary.
- [ ] 5. Write a compact grounding note with evidence, confidence, and local
  impact.
- [ ] 6. If compact grounding is not enough, surface the exact evidence gap to the
  caller instead of launching a higher-tier research method from this primitive.
- [ ] 7. Review before completion.
  - [ ] For changes to this skill, require a separate review pass before claiming
  the update is ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->
## Source Choice

- Local repo question: inspect code, tickets, specs, docs, and nearby tests.
- API/library behavior: prefer official docs or maintained repos.
- Peer expectation: inspect comparable products or implementations.
- Provided source: use the supplied material first.

Escalate to `research:*` only when the answer needs multiple comparables, source
synthesis, a formal parity/gap brief, or a durable research artifact.

## Stop Condition

Stop when the evidence is strong enough to support, change, or block the active
decision. Do not keep gathering sources for completeness.

## Output

Return a short `Grounding Note`:

- `Question / claim`
- `Local baseline`
- `Sources checked`
- `Evidence`
- `Confidence`
- `Local impact`
- `Escalation needed`

## Templates

Use the `Grounding Note` fields above as the default output template.

## Guardrails

- Do not turn every task into research.
- Do not claim evidence was checked unless it was actually read.
- Do not import peer features wholesale; hand broad parity to `research:parity`.

## Gotchas

- Do not treat stale local memory as stronger than live files or primary docs.
- Do not cite sources that were only searched but not opened or inspected.
- Do not keep collecting evidence after the active decision is grounded.

## Reference Map

- [../research/SKILL.md](../research/SKILL.md) - use when the caller needs a
  formal multi-source research method such as parity, gap, docs, or code
  patterns.
