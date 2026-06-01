---
name: reference-grounding
version: 0.1.0
description: Tier 1 primitive for grounding recommendations, plans, and claims in local evidence, official docs, peer products, standards, maintained repos, or provided sources before stronger workflow skills consume them.
tier: 1
source: local
allowed-tools: Read, Glob, Grep
---

# Reference Grounding

Use when a recommendation, plan, or claim needs enough evidence to stop
guessing. This is the small evidence move, not a research router.

## Job

Name the claim that needs grounding, inspect the smallest trustworthy source
set, and return a compact evidence note for the active workflow.

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] State the one claim, decision, expectation, or comparison that needs
  grounding.
- [ ] Capture the local baseline from nearby code, tickets, specs, docs, or
  provided sources when repo scope matters.
- [ ] Choose the smallest useful source class: local evidence, official docs,
  standards, maintained repos, peer products, competitors, or user-provided
  sources.
- [ ] Prefer primary sources and real implementations over commentary.
- [ ] Write a compact grounding note with evidence, confidence, and local
  impact.
- [ ] If compact grounding is not enough, surface the exact evidence gap to the
  caller instead of launching a higher-tier research method from this primitive.
- [ ] For changes to this skill, require a separate review pass before claiming
  the update is ready.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->
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

## Guardrails

- Do not turn every task into research.
- Do not claim evidence was checked unless it was actually read.
- Do not import peer features wholesale; hand broad parity to `research:parity`.
