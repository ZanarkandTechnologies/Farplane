# Documentation Quality Checklist

Load this reference after the draft or edit pass, before claiming a durable doc
is ready. Do not load it for tiny typo fixes unless the surrounding doc already
looks inconsistent.

## Reader Contract

- Audience is named or obvious from the owning file.
- Doc type is clear: concept, doctrine, spec, reference, runbook, tutorial,
  checklist, decision note, or public guide.
- The intended next action is clear.
- The source of truth is linked or named.
- The main definition, decision, or workflow appears near the top.

## Grounding

- Claims that depend on local repo state cite or align with canonical files.
- Claims that depend on current facts, API behavior, peer norms, or external
  best practice were grounded through `reference-grounding` or a broader
  research method.
- Unsupported claims are removed, softened, or labeled as local policy.
- Historical context is kept only when it helps the reader understand the
  current contract.

## Terms And Definitions

- Each concept has one canonical term.
- Duplicate or competing definitions are removed unless the doc explicitly
  compares alternatives.
- Headings, examples, formulas, tables, links, and captions use the same
  vocabulary.
- Acronyms or symbols are introduced before use.
- Old names are deleted or clearly marked as retired.

## Human-Facing Writing

- The doc speaks to its human reader, not to a future hidden agent.
- Agent-facing commentary, hidden instructions, process excuses, and meta
  narration are removed.
- Harness-internal reminders live in skills, prompts, tickets, or
  implementation notes instead of human-facing doctrine.
- The tone matches the surface: doctrine is crisp, specs are precise, runbooks
  are executable, and public guidance is reader-friendly.

## Structure

- Sections follow the reader's task order.
- Stale sections, repeated setup, low-value boundary notes, and old examples are
  deleted rather than patched around.
- Examples teach the current model.
- Tables, signatures, and checklists make action easier rather than adding
  ceremony.
- Links point to canonical owners instead of duplicating long doctrine.

## Prose

- Sentences use only the words needed to convey the meaning.
- Necessary connectors, context, articles, and caveats remain so the text is
  precise.
- Paragraphs are short enough to scan.
- Semantic line breaks are used where they make Markdown diffs easier to
  review.
- Code blocks and examples are complete enough to be useful.

## Checks To Run

Adapt the patterns to the actual edit:

```bash
rg -n "old_term|duplicate_term|removed_section" path/to/doc.md
rg -n "the agent should|must define|do not introduce|for future agents" path/to/doc.md
rg -n "^## |^### " path/to/doc.md
```

When relevant:

```bash
python3 bin/validators/check_doc_refs.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## Completion Gate

Before completion, confirm:

- Terms are consistent across prose, headings, code blocks, tables, examples,
  links, and captions.
- Every definition has one owner.
- Every example teaches the current model.
- The doc is written for its human reader.
- Stale sections were deleted instead of preserved.
- Touched links, refs, registries, or metadata were refreshed.
- Material docs have the requested review route or an explicit reason review
  was skipped.
