---
name: unslop
description: "Rewrite supplied prose so it sounds clear, specific, and human while preserving its meaning, facts, tone, and precise technical terms."
tier: 2
source: local
capability:
  kind: shortcut
upstream_url: https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md
template_uses:
  skill-template: "0.4.3"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.1"
eval: evals/evals.json
qa_checklist: qa_checklist.md
---

# Unslop

## Context

Use this when the operator explicitly asks to unslop, humanize, simplify, or
remove AI-sounding prose. It edits writing, not code architecture. Use
`lean-check` when the question is whether code, a dependency, an abstraction,
or a feature needs to exist.

Preserve the supplied meaning, facts, certainty, intended tone, Markdown, code,
links, and canonical technical terms. Do not add opinions, conclusions,
sources, examples, or next steps that the source does not support.

## Skill Signature

```text
unslop(text, audience?, purpose?, tone?) -> revised_text
reads: supplied prose and any explicit writing constraints
does: rewrites the prose plainly without changing its supported meaning
writes: the requested file when editing, otherwise none
returns: revised text in the source format
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the text, audience, purpose, and intended tone. Infer ordinary
  context; ask only when a missing choice would materially change the result.
- [ ] 2. Find the real tells: puffery, filler, vague attribution, abstract
  jargon, repetition, formulaic framing, generic claims, and sentences that
  require backtracking. If a vague sentence has no concrete supported meaning,
  delete it instead of paraphrasing the vagueness; begin with the first
  supported fact rather than inventing a broad outcome summary. For example,
  do not turn
  “a robust transition across an evolving landscape” into “the data moved
  cleanly”; the second phrase invents a successful outcome.
- [ ] 3. Rewrite with plain, specific words. Name the actor and mechanism when
  the source supports them, vary sentence rhythm naturally, and keep the
  original level of confidence. Copy numbers and quantifiers exactly; never
  infer that a reported count is the total.
- [ ] 4. Match the genre. Human voice may include an existing opinion or some
  natural unevenness; technical docs, status notes, and contracts should remain
  precise rather than becoming chatty.
- [ ] 5. Self-audit: “What still sounds generated?” and “What meaning did I
  change?” Fix the first and restore the second, then return the revised text.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Do not use a banned-word or punctuation checklist. A precise term, em dash,
  heading, or list may be the clearest choice.
- Do not replace one AI tell with forced slang, fake vulnerability, excessive
  first person, sentence fragments, or theatrical opinions.
- Do not shorten away safety, evidence, qualifications, instructions, or useful
  technical detail.
- Do not add or remove quantifiers such as `all`, `only`, `always`, or `never`;
  they change the claim's certainty or scope. “42 tests passed” must not become
  “all 42 tests passed.”
- Do not rewrite code, frontmatter values, commands, URLs, citations, or quoted
  source text unless the operator asks.
- Preserve identifiers and canonical names exactly, even when the surrounding
  prose is awkward.
- If the text is already clear and natural, make little or no change.

## Output

Outside any required conversation ledger, return the revised text without a
change log by default. When editing a file, make the scoped edit and report
only material meaning or structure changes.
