# Documentation Quality

Use this family when reviewing durable documentation changes: README updates,
feature specs, system specs, fundamentals, runbooks, checklists, registry
companions, and public guidance.

Required TAS: `TAS-A` for canonical, public, cross-surface, or policy-bearing
docs. Diagnostic for tiny local typo or link fixes.

## Family TAS Guide

- `TAS-A`: the doc is useful, grounded, well placed, and ready for its reader
  with only minor caveats.
- `TAS-B`: the doc is directionally useful, but one or more required checks fail
  in a repairable way.
- `TAS-C`: the doc is misleading, wrong-scope, ungrounded, bloated enough to
  obscure the current truth, or duplicates another owner in a way likely to
  drift.
- `TAS-D`: the reviewer lacks the target doc, source context, changed diff, or
  evidence needed to judge honestly.

## Checklist Modules

### Required Checks

- [ ] `reader-contract-clear`: Audience, doc type, source of truth, and intended
  next action are clear from the page itself or nearest owner.
- [ ] `current-truth-near-top`: The main definition, decision, workflow, or
  status appears before historical context or implementation detail.
- [ ] `owner-surface-fit`: The content lives in the smallest durable owner with
  the right audience, lifecycle, update cadence, and retrieval path.
- [ ] `grounding-visible`: Local, external, or supplied claims are tied to
  source refs, evidence, or explicit local policy.
- [ ] `terminology-consistent`: Canonical terms, examples, captions, links, and
  code blocks use one vocabulary.
- [ ] `density-fit`: The doc shape matches its job: map, spec, runbook,
  reference, explanation, decision note, or checklist.
- [ ] `metadata-aligned`: Front matter, status, refs, dates, feature refs, and
  generated-registry implications match the local owner schema.
- [ ] `checks-relevant`: Validators, searches, or review routes are named when
  the doc changes links, metadata, canonical policy, or public claims.

### Blocker Checks

- [ ] `wrong-owner`: The doc duplicates or contradicts a clearer source of truth
  instead of linking to it.
- [ ] `ungrounded-policy`: The doc promotes external advice, stale memory, or
  unsupported claims into active Farplane policy.
- [ ] `agent-facing-drift`: A human-facing doc becomes hidden agent instruction
  text that belongs in a skill, prompt, ticket, or runbook.
- [ ] `template-padding`: The doc grows because template sections were filled
  for ceremony rather than reader value.
- [ ] `score-theater`: Numeric scores or metric language replace the reviewer
  decision, evidence, failed checks, or repair hints.

### Evidence Checks

- [ ] `source-docs-inspected`: The reviewer inspected the target doc and nearest
  owner/index or canonical source.
- [ ] `changed-claims-checked`: New or changed claims were checked against the
  relevant local docs, tickets, specs, code, or supplied evidence.
- [ ] `validators-run-or-deferred`: Relevant validators or focused searches ran,
  or the deferral is explicit and proportional.
- [ ] `review-boundary-clear`: For material docs, the review explains whether
  documentation-quality, evidence-quality, integration-readiness, or other
  rubrics are required.

## Evidence and Finding Cues

- Weak documentation evidence usually shows polished prose without source
  ownership, current status, or proof that neighboring docs still agree.
- Strong documentation evidence shows the target diff, owner docs, relevant
  searches or validators, and a concise explanation of what changed for the
  reader.
- Findings should name the failed check, the exact doc surface, and the smallest
  repair: move, link, delete, ground, rename, or split.

## Relationship To Checklists And Metrics

Skill-local documentation QA checklists inspect the artifact during authoring.
This rubric judges readiness after inspection. Metrics can appear as evidence,
but a metric is not the verdict.

Do not average checklist items or convert this rubric into a scalar score. The
reviewer returns one TAS verdict with reasons, failed checks, and next action.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `tas`
- `required_tas`
- `pass`
- `checks`
- `failed_checks`
- `findings`
- `next_action`
