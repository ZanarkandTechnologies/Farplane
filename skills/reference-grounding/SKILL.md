---
name: reference-grounding
version: 0.1.0
description: Tier 1 primitive for grounding recommendations, plans, and claims in local evidence, official docs, peer products, standards, maintained repos, or provided sources before stronger workflow skills consume them.
allowed-tools: Read, Glob, Grep
---

# Reference Grounding

Use this as a Tier 1 primitive when another skill needs evidence before it can
make a recommendation, scope a plan, or claim a result.

This is not a research router and not a replacement for `research:*`. It is the
small grounding move: name what needs evidence, collect enough trustworthy
references to avoid guessing, and hand the compact evidence to the active
workflow.

## Job

1. State the claim, decision, expectation, or comparison that needs grounding.
2. Capture the local baseline when repo scope matters.
3. Pick the smallest source class that can answer it:
   - local code, tickets, specs, or docs
   - official docs or standards
   - maintained repos or code examples
   - peer products or competitor workflows
   - user-provided sources
4. Prefer primary sources and real implementations over commentary.
5. Return a compact grounding note with source confidence and local impact.

## Use When

- `advise` needs current facts or examples before recommending
- `brainstorm` needs examples before option quality is trustworthy
- `plan` or a domain planning skill needs credible expectations before scoping
- `execute` or a domain execution skill needs official behavior or local
  invariants before changing files
- `review` needs to challenge a claim against evidence

## Escalate To Research When

- the question needs multiple comparables or a formal parity/gap brief
- the source set itself needs synthesis
- the answer is broader than one compact grounding note
- the work should produce a durable research artifact

Use `research:parity`, `research:gap`, `research:official-docs`,
`research:code-patterns`, `research:competitor`, or `research:source-synthesis`
for that broader Tier 2 research workflow.

## Output

Produce a short `Grounding Note` with:

- `Question / claim`
- `Local baseline`
- `Sources checked`
- `Evidence`
- `Confidence`
- `Local impact`
- `Escalation needed`

## Guardrails

- Do not turn every task into web research; ground only the claim that matters.
- Do not use vague blog posts when official docs, standards, local code, or
  maintained repos can answer the question.
- Do not import peer features wholesale; hand broad parity questions to
  `research:parity`.
- Do not claim evidence was checked unless it was actually read.
