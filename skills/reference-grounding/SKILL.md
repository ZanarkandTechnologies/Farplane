---
name: reference-grounding
version: 0.2.0
description: "Turn claims, plans, or implementation choices into compact evidence notes with the right local, current-web, official, peer, or provided sources."
tier: 1
source: local
skill_template_version: "0.1.0"
allowed-tools: Read, Glob, Grep, web_search, documentation-searcher
---

# Reference Grounding

## Context

`reference-grounding` is a Tier 1 primitive for compact evidence. It should
ground one claim or decision, then hand the result back to the caller rather
than expanding into a full research pass.

Use when a recommendation, plan, or claim needs enough evidence to stop
guessing. This is the small evidence move, not a research router.

For implementation work, local files are only half of the baseline. Unless the
user explicitly asks for local-only work or the change is a tiny same-scope fix,
ground the approach in current external evidence before choosing the design:
official docs for the libraries and APIs involved, maintained examples or
reference repos for implementation patterns, and peer/product examples when the
workflow or UX expectation matters. Then adapt that evidence to the local
codebase instead of inventing from memory.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the one claim, decision, expectation, or comparison that needs
  grounding.
- [ ] 2. Capture the local baseline from nearby code, tickets, specs, docs, or
  provided sources when repo scope matters.
- [ ] 3. Classify the source need before searching.
   - [ ] Local-only evidence is enough only for repo-internal questions, tiny
     same-scope fixes, or user-requested local-only work.
   - [ ] Implementation choices need current official docs or maintained
     implementation examples unless the dependency and pattern are already
     freshly grounded in the active context.
   - [ ] "Best practice", "state of the art", "latest", peer expectation,
     product behavior, standards, pricing, law, API behavior, or current facts
     need web or official-source evidence; local files alone are insufficient.
- [ ] 4. Choose the smallest useful source class: local evidence, current
  official docs, standards, maintained repos, peer products, competitors, web
  sources, or user-provided sources.
- [ ] 5. Prefer primary sources and real implementations over commentary.
- [ ] 6. Write a compact grounding note with evidence, confidence, and local
  impact.
- [ ] 7. If compact grounding is not enough, route the exact evidence gap to the
  caller's next step, usually `research:official-docs`, `research:code-patterns`,
  `research:parity`, `research:gap`, or `research:source-synthesis`.
- [ ] 8. Review before completion.
  - [ ] For changes to this skill, require a separate review pass before claiming
  the update is ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->
## Source Choice

- Local repo question: inspect code, tickets, specs, docs, and nearby tests.
- API/library behavior: prefer official docs or maintained repos.
- Peer expectation: inspect comparable products or implementations.
- Implementation feature work: inspect the local baseline, then check current
  official docs and at least one maintained implementation/example source before
  locking the approach unless the task is a tiny same-scope fix.
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
- `Source need`
- `Sources checked`
- `Evidence`
- `Confidence`
- `Local impact`
- `Escalation needed`

## Templates

Use the `Grounding Note` fields above as the default output template.

## Guardrails

- Do not turn every task into a full research project; do perform compact
  current-source grounding for implementation choices.
- Do not claim evidence was checked unless it was actually read.
- Do not treat local files as sufficient evidence for "best practice",
  "current", "latest", "state of the art", external API behavior, or peer
  implementation expectations.
- Do not import peer features wholesale; hand broad parity to `research:parity`.

## Gotchas

- Do not treat stale local memory as stronger than live files or primary docs.
- Do not cite sources that were only searched but not opened or inspected.
- Do not keep collecting evidence after the active decision is grounded.

## Reference Map

- [../research/SKILL.md](../research/SKILL.md) - use when the caller needs a
  formal multi-source research method such as parity, gap, docs, or code
  patterns.
