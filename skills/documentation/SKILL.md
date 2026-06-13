---
name: documentation
description: "Turn durable doc-writing or doc-revision work into grounded, concise, human-usable docs with consistency checks and review proof."
tier: 2
source: local
methods: ["documentation:doc-quality"]
---

# Documentation Skill

## Context

`documentation` is the Tier 2 writing and doc-quality workflow. It owns durable
repo docs such as fundamentals, specs, READMEs, skill references, templates,
runbooks, and public guidance.

Doc search is not the core job here. Treat official-doc lookup, local evidence,
and current-source checking as Tier 1 grounding through
[reference-grounding](../reference-grounding/SKILL.md). This skill consumes
that evidence and turns it into clear, consistent, reviewable documentation.

Good technical docs help a reader solve a problem or make a decision quickly
and correctly. Keep first-load context light: write the draft from the reader
contract, then load the detailed quality checklist only for the finish pass.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Define the reader contract: audience, doc type, owning file, source of
  truth, intended next action, canonical terms, and proof surface.
- [ ] 2. Ground the content with the smallest evidence move; use
  [reference-grounding](../reference-grounding/SKILL.md) when claims depend on
  local canonical files, official docs, current facts, peer norms, or
  implementation examples.
- [ ] 3. Draft or revise for the reader's next action: one concept model,
  human-facing prose, current examples, and concise structure.
- [ ] 4. Load
  [references/doc-quality-checklist.md](references/doc-quality-checklist.md)
  for the finish pass when the doc is durable, canonical, or material.
- [ ] 5. Run only the checklist searches and validators relevant to the touched
  doc, then fix issues before completion.
- [ ] 6. Use [advise](../advise/SKILL.md) when the doc has multiple valid
  framing, placement, or term choices.
- [ ] 7. Use the [review protocol](../review/SKILL.md) before claiming material
  durable docs or public guidance are ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Workflow: Write -> Review

Use this workflow for durable docs. Keep tiny prose fixes with the owning file
and run only the checks proportional to the risk.

### 1. Reader Contract

```text
doc_contract = {
  audience,
  doc_type,
  owning_file,
  source_of_truth,
  intended_next_action,
  canonical_terms,
  proof_surface
}
```

### 2. Edit Pass

Prefer:

- one definition per concept
- examples that teach the current contract
- sections that follow the reader's task order
- direct links to canonical sources instead of duplicated doctrine
- concise prose that keeps necessary precision

Avoid:

- agent commentary in human-facing docs
- repeated definitions under different names
- stale "boundaries" sections that restate obvious non-goals
- old examples preserved only because they used to be true
- process narration that belongs in a skill, ticket, or prompt

### 3. Check Pass

Load [references/doc-quality-checklist.md](references/doc-quality-checklist.md)
for the finish pass. Run the relevant searches and validators from that file,
then fix issues before completion.

## Output

Use this shape when a durable review note is useful:

```markdown
## Documentation Review: [File]

### Reader Contract
- Audience:
- Doc type:
- Source of truth:
- Intended next action:

### Findings
- Terms:
- Duplicate definitions:
- Agent-facing commentary:
- Stale sections:
- Examples:
- Links/refs:

### Changes
- [Concise list]

### Verification
- [Searches/checks run]
```

## Quality Guidelines

- **Reader Task First**: The doc should help the reader solve a problem, make a
  decision, or operate a workflow.
- **One Term, One Definition**: Pick the canonical term and remove competitors.
- **Current Model Only**: Examples and formulas should teach the current
  contract, not the historical path.
- **Human Reader First**: Keep agent-operating notes in skills, prompts,
  tickets, or implementation docs.
- **Grounded Claims**: Do not smuggle unsupported external, current, or
  implementation claims into durable docs.

## What Not To Do

- Do not leave duplicate definitions under different names.
- Do not leave agent-facing commentary in human-facing docs.
- Do not keep stale boundaries, research tails, or historical examples just
  because they existed before.
- Do not add unofficial best practices unless the doc clearly labels them as
  local policy or grounded synthesis.
- Do not turn a writing task into broad research when compact grounding is
  enough.
- Do not claim material docs are ready without a check pass or review route.

## Reference Map

- [../reference-grounding/SKILL.md](../reference-grounding/SKILL.md) - use for
  compact local, official-doc, current-source, or peer evidence before writing.
- [../advise/SKILL.md](../advise/SKILL.md) - use when term, frame, placement, or
  structure choices have real tradeoffs.
- [../review/SKILL.md](../review/SKILL.md) - use for material durable docs or
  public guidance.
- [references/doc-quality-checklist.md](references/doc-quality-checklist.md) -
  load for the finish pass before claiming durable docs are ready.
- Ref source: `toss/technical-writing` overview - technical writing should help
  readers solve problems quickly and accurately, with type, structure, and
  sentence quality as core principles.
- Ref source: `quantconnect/documentation` style guide - use only the necessary
  words while preserving the words needed for clear meaning.
- Ref source: `uber-go/guide` contributing guide - semantic line breaks make
  Markdown easier to review and edit.
